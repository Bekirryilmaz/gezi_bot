"""NLP gozlem adayi pipeline'i.

Ham yorumlari BERT ve seffaf konu kurallariyla isler; ancak ciktisi puan,
claim, yayin veya uygunluk degildir. Her cikti inceleme durumu ``bekliyor``
olan ``AdayGozlem`` kaydidir. Karar Motoru bu pipeline'a bagimli degildir.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from ortak.sabitler import VeriKaynagi
from sqlalchemy import select
from sunucu.bilgi.pilot_claimleri import kaynak_haklari_uygun_mu
from sunucu.veritabani.baglanti import OturumUretici
from sunucu.veritabani.bilgi_modelleri import KaynakPolitikasi
from tqdm import tqdm

from veri.duygu_analizi.gozlem_adayi import yorumdan_aday_gozlemler
from veri.duygu_analizi.model import MODEL_ADI, toplu_duygu_tahmin_et
from veri.ortak.dosya_araclari import bugunun_tarihi_dosya_adi, jsonl_yaz
from veri.ortak.gozlem_adayi_modeli import AdayGozlem
from veri.ortak.metin_araclari import konsolu_guvenli_hale_getir
from veri.ortak.sehir_ayarlari import sehir_getir
from veri.ortak.veri_yukleyiciler import tum_ham_yorumlari_yukle
from veri.ortak.yorum_modeli import HamYorum


def _yorumlari_isle(
    yorumlar: list[HamYorum], yigin_boyutu: int, *, politika: KaynakPolitikasi | None = None
) -> list[AdayGozlem]:
    """Model siniflarini yalniz konuya bagli inceleme adaylarina donusturur."""
    izinli, neden = kaynak_haklari_uygun_mu(politika)
    if not izinli or any(yorum.kaynak.value != politika.kaynak for yorum in yorumlar):
        raise PermissionError(neden or "kaynak_politikasi_eslesmiyor")
    metinler = [yorum.yorum_metni for yorum in yorumlar]
    genel_duygular = toplu_duygu_tahmin_et(metinler, yigin_boyutu=yigin_boyutu)
    adaylar: list[AdayGozlem] = []
    for ham_yorum, (duygu_etiketi, duygu_skoru) in tqdm(
        zip(yorumlar, genel_duygular),
        total=len(yorumlar),
        desc="NLP gozlem adayi",
        unit="yorum",
    ):
        adaylar.extend(yorumdan_aday_gozlemler(ham_yorum, duygu_etiketi, duygu_skoru))
    return adaylar


def _ozet_yazdir(
    sehir_isim: str, kaynak_bazli_adaylar: dict[VeriKaynagi, list[AdayGozlem]]
) -> None:
    tum_adaylar = [aday for liste in kaynak_bazli_adaylar.values() for aday in liste]
    if not tum_adaylar:
        print("[UYARI] Uretilebilen gozlem adayi yok.")
        return
    print(f"\n[BILGI] === '{sehir_isim}' NLP Gozlem Adayi Ozeti ===")
    print(f"[BILGI] Toplam inceleme adayi: {len(tum_adaylar)}")
    for kaynak, liste in kaynak_bazli_adaylar.items():
        print(f"[BILGI] {kaynak.value}: {len(liste)} inceleme adayi")


def calistir(sehir_anahtari: str, yigin_boyutu: int = 16) -> Path | None:
    sehir = sehir_getir(sehir_anahtari)
    with OturumUretici() as oturum:
        politikalar = list(oturum.scalars(select(KaynakPolitikasi)))
        izinli_kaynaklar = {
            kaynak
            for kaynak in VeriKaynagi
            if any(p.kaynak == kaynak.value and kaynak_haklari_uygun_mu(p)[0] for p in politikalar)
        }
    if not izinli_kaynaklar:
        print("[ENGEL] Haklari dogrulanmis kaynak yok; ham yorum okunmadi.")
        return None
    kaynak_bazli_ham = tum_ham_yorumlari_yukle(sehir_anahtari, kaynaklar=izinli_kaynaklar)
    if not kaynak_bazli_ham:
        print("[ENGEL] Haklari dogrulanmis kaynaklardan islenebilir yorum yok; NLP calismadi.")
        return None

    toplam = sum(len(yorumlar) for yorumlar in kaynak_bazli_ham.values())
    print(f"[BILGI] Toplam {toplam} ham yorumdan gozlem adayi uretiliyor (model: {MODEL_ADI})...")
    kaynak_bazli_adaylar: dict[VeriKaynagi, list[AdayGozlem]] = {}
    for kaynak, yorumlar in kaynak_bazli_ham.items():
        print(f"[BILGI] '{kaynak.value}' isleniyor ({len(yorumlar)} yorum)...")
        with OturumUretici() as oturum:
            politika = oturum.scalar(
                select(KaynakPolitikasi).where(KaynakPolitikasi.kaynak == kaynak.value)
            )
            izinli, neden = kaynak_haklari_uygun_mu(politika)
            if not izinli:
                print(f"[ENGEL] {kaynak.value}: {neden}; model ve aday uretimi calismadi.")
                continue
            kaynak_bazli_adaylar[kaynak] = _yorumlari_isle(
                yorumlar, yigin_boyutu, politika=politika
            )

    cikti_dosyasi = (
        Path(__file__).resolve().parents[1]
        / "cikti"
        / "islenmis"
        / "gozlem_adaylari"
        / f"{sehir.anahtar}_{bugunun_tarihi_dosya_adi()}.jsonl"
    )
    tum_adaylar = [aday for liste in kaynak_bazli_adaylar.values() for aday in liste]
    if not tum_adaylar:
        print("[BILGI] Haklari dogrulanmis aday yok; cikti yazilmadi.")
        return None
    jsonl_yaz(cikti_dosyasi, tum_adaylar)
    print(f"[BILGI] Inceleme bekleyen gozlem adaylari yazildi: {cikti_dosyasi}")
    _ozet_yazdir(sehir.isim, kaynak_bazli_adaylar)
    return cikti_dosyasi


def _ana() -> None:
    konsolu_guvenli_hale_getir()
    ayristirici = argparse.ArgumentParser(
        description="Ham yorumlardan inceleme bekleyen gozlem adaylari uretir."
    )
    ayristirici.add_argument(
        "--sehir", default="samsun", help="veri/ortak/sehir_ayarlari.py icindeki sehir anahtari"
    )
    ayristirici.add_argument(
        "--yigin-boyutu", type=int, default=16, help="Modelin bir seferde isleyecegi yorum sayisi"
    )
    argumanlar = ayristirici.parse_args()
    calistir(argumanlar.sehir, yigin_boyutu=argumanlar.yigin_boyutu)


if __name__ == "__main__":
    _ana()
