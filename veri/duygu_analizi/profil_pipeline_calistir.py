"""
Yer profili pipeline'i -- ana calistirma betigi.

veri/duygu_analizi/pipeline_calistir.py'nin urettigi EN GUNCEL IslenmisYorum
JSONL'i VE veri/esleme/eslestirici.py'nin urettigi EN GUNCEL BirlesikYer
JSONL'ini okur, yorumlari yerlere baglar (bkz. yer_profili_cikarici.py) ve
her yer icin:
  1. Cok boyutlu YerProfili'ni (fiyat algisi, ulasim kolayligi, kalabalik
     zamanlar, ziyaretci profili) cikarir,
  2. anlatim_uretici.py ile samimi bir Turkce tanitim metni ("duygu_ozeti") uretir,
ve sonucu veri/cikti/islenmis/yer_profilleri/<sehir>_<tarih>.jsonl dosyasina yazar.

Bu betik, mevcut pipeline_calistir.py'nin (yorum bazli) UZERINE insa eder --
onu degistirmez, onun ciktisini girdi olarak kullanir.

Calistirma (repo kokunden, once asagidaki iki komutun calistirilmis olmasi gerekir):
    python -m veri.esleme.eslestirici --sehir samsun
    python -m veri.duygu_analizi.pipeline_calistir --sehir samsun
    python -m veri.duygu_analizi.profil_pipeline_calistir --sehir samsun
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from pathlib import Path

from ortak.sabitler import DuyguEtiketi
from veri.duygu_analizi.anlatim_uretici import yapisal_deneyim_metni_uret, yer_tanitim_metni_uret
from veri.duygu_analizi.tanitim_uretici import yer_tanitim_metni_uret as internet_tanitim_uret
from veri.duygu_analizi.yer_profili_cikarici import (
    birlesik_yerleri_kimlige_gore_esle,
    yer_profili_olustur,
    yorumlari_yerlere_bagla,
)
from veri.ortak.birlesik_yer_modeli import BirlesikYer
from veri.ortak.dosya_araclari import bugunun_tarihi_dosya_adi, jsonl_oku, jsonl_yaz
from veri.ortak.metin_araclari import konsolu_guvenli_hale_getir
from veri.ortak.sehir_ayarlari import sehir_getir
from veri.ortak.yer_profili_modeli import BoyutTespiti, YerProfili
from veri.ortak.yorum_modeli import IslenmisYorum
from ortak.sabitler import FiyatAlgisi, UlasimKolayligi


def _cikti_kok() -> Path:
    # Bu dosya veri/duygu_analizi/ altinda, yani parents[1] = veri/
    return Path(__file__).resolve().parents[1] / "cikti"


def _en_guncel_dosyayi_bul(klasor: Path, desen: str) -> Path | None:
    if not klasor.exists():
        return None
    adaylar = sorted(klasor.glob(desen))  # dosya adlari tarih icerir, siralama = kronolojik
    return adaylar[-1] if adaylar else None


def _birlesik_yerleri_yukle(sehir_anahtari: str) -> list[BirlesikYer]:
    dosya = _en_guncel_dosyayi_bul(_cikti_kok() / "islenmis" / "birlesik_yerler", f"{sehir_anahtari}_*.jsonl")
    if dosya is None:
        return []
    yerler: list[BirlesikYer] = []
    for kayit in jsonl_oku(dosya):
        try:
            yerler.append(BirlesikYer(**kayit))
        except Exception as hata:
            print(f"[UYARI] {dosya.name} icinde okunamayan BirlesikYer kaydi atlandi: {hata}")
    return yerler


def _islenmis_yorumlari_yukle(sehir_anahtari: str) -> list[IslenmisYorum]:
    dosya = _en_guncel_dosyayi_bul(_cikti_kok() / "islenmis" / "yorumlar", f"{sehir_anahtari}_*.jsonl")
    if dosya is None:
        return []
    yorumlar: list[IslenmisYorum] = []
    for kayit in jsonl_oku(dosya):
        try:
            yorumlar.append(IslenmisYorum(**kayit))
        except Exception as hata:
            print(f"[UYARI] {dosya.name} icinde okunamayan IslenmisYorum kaydi atlandi: {hata}")
    return yorumlar


def _on_plana_cikan_konulari_bul(ilgili_yorumlar: list[IslenmisYorum], adet: int = 5) -> list[tuple[str, DuyguEtiketi]]:
    """konu_analizi.py'nin ciktisi olan konu_duygulari'ni bu yerin TUM
    yorumlari uzerinden agregre eder: en cok bahsedilen `adet` konuyu, o
    konu icin en sik gorulen duygu etiketiyle birlikte dondurur (bkz.
    pipeline_calistir.py::_ozet_yazdir'daki benzer mantik)."""
    konu_sayaci: Counter[str] = Counter()
    konu_duygu_dagilimi: dict[str, Counter] = defaultdict(Counter)
    for yorum in ilgili_yorumlar:
        for konu_duygusu in yorum.konu_duygulari:
            konu_sayaci[konu_duygusu.konu] += 1
            konu_duygu_dagilimi[konu_duygusu.konu][konu_duygusu.duygu_etiketi] += 1

    sonuc: list[tuple[str, DuyguEtiketi]] = []
    for konu, _adet in konu_sayaci.most_common(adet):
        baskin_duygu = konu_duygu_dagilimi[konu].most_common(1)[0][0]
        sonuc.append((konu, baskin_duygu))
    return sonuc


def _ozet_yazdir(profiller: list[YerProfili]) -> None:
    print("\n[BILGI] === Yer Profili Ozeti ===")
    print(f"[BILGI] Toplam profil cikarilan yer: {len(profiller)}")

    fiyat_dagilimi = Counter(p.fiyat_algisi.deger for p in profiller)
    ulasim_dagilimi = Counter(p.ulasim_kolayligi.deger for p in profiller)
    print(f"[BILGI] Fiyat algisi dagilimi: {dict(fiyat_dagilimi)}")
    print(f"[BILGI] Ulasim kolayligi dagilimi: {dict(ulasim_dagilimi)}")

    kalabalik_tespit_edilen = sum(1 for p in profiller if p.kalabalik_zamanlar)
    ziyaretci_tespit_edilen = sum(1 for p in profiller if p.ziyaretci_profili)
    print(f"[BILGI] En az 1 kalabalik zaman dilimi tespit edilen yer: {kalabalik_tespit_edilen}/{len(profiller)}")
    print(f"[BILGI] En az 1 ziyaretci tipi tespit edilen yer: {ziyaretci_tespit_edilen}/{len(profiller)}")

    ornek = max(profiller, key=lambda p: p.kullanilan_yorum_sayisi)
    print(f"\n[BILGI] Ornek tanitim metni -- '{ornek.yer_ismi}' ({ornek.kullanilan_yorum_sayisi} yorumdan uretildi):")
    print(f"[BILGI]   {ornek.duygu_ozeti}")


def calistir(sehir_anahtari: str) -> Path | None:
    sehir = sehir_getir(sehir_anahtari)

    birlesik_yerler = _birlesik_yerleri_yukle(sehir_anahtari)
    islenmis_yorumlar = _islenmis_yorumlari_yukle(sehir_anahtari)

    if not birlesik_yerler:
        print(
            f"[UYARI] '{sehir.isim}' icin birlesik yer kataloğu bulunamadi. "
            f"Once 'python -m veri.esleme.eslestirici --sehir {sehir_anahtari}' calistir."
        )
        return None
    if not islenmis_yorumlar:
        print(
            f"[UYARI] '{sehir.isim}' icin islenmis yorum bulunamadi. "
            f"Once 'python -m veri.duygu_analizi.pipeline_calistir --sehir {sehir_anahtari}' calistir."
        )
        return None

    print(f"[BILGI] {len(birlesik_yerler)} yer, {len(islenmis_yorumlar)} islenmis yorum okundu. Yorumlar yerlere baglaniyor...")

    yer_kimlik_haritasi = birlesik_yerleri_kimlige_gore_esle(birlesik_yerler)
    yer_bazli_yorumlar, baglanamayan_sayisi = yorumlari_yerlere_bagla(birlesik_yerler, islenmis_yorumlar)

    if baglanamayan_sayisi:
        print(
            f"[BILGI] {baglanamayan_sayisi} yorum hicbir yere baglanamadi (orn. Eksi Sozluk'un sehir geneli "
            "kayitlari -- bilinen ve bilincli kabul edilmis bir sinirlama, bkz. veri/README.md)."
        )
    if not yer_bazli_yorumlar:
        print("[UYARI] Hicbir yorum bir yere baglanamadigi icin profil uretilemedi.")
        return None

    print(f"[BILGI] {len(yer_bazli_yorumlar)} yer icin profil cikariliyor...")

    profiller: list[YerProfili] = []
    islenen_kimlikler: set[str] = set()
    for yer_kimligi, ilgili_yorumlar in yer_bazli_yorumlar.items():
        yer = yer_kimlik_haritasi[yer_kimligi]
        profil = yer_profili_olustur(yer_kimligi, yer.isim, ilgili_yorumlar)

        duygu_skorlari = [yorum.duygu_skoru for yorum in ilgili_yorumlar]
        genel_duygu_ortalamasi = sum(duygu_skorlari) / len(duygu_skorlari) if duygu_skorlari else None
        on_plana_cikan_konular = _on_plana_cikan_konulari_bul(ilgili_yorumlar)

        if len(ilgili_yorumlar) < 3:
            tanitim = internet_tanitim_uret(yer, wiki_denensin=False)
            profil.duygu_ozeti = yapisal_deneyim_metni_uret(
                yer.isim,
                yer.ana_kategori.value,
                yer.alt_kategori,
                tanitim_metni=tanitim,
                yer_kimligi=yer_kimligi,
            )
        else:
            profil.duygu_ozeti = yer_tanitim_metni_uret(profil, genel_duygu_ortalamasi, on_plana_cikan_konular)
        profiller.append(profil)
        islenen_kimlikler.add(yer_kimligi)

    # Yorumsuz yerler: yapisal kullanici deneyimi fallback'i
    for yer_kimligi, yer in yer_kimlik_haritasi.items():
        if yer_kimligi in islenen_kimlikler:
            continue
        tanitim = internet_tanitim_uret(yer, wiki_denensin=False)
        profil = YerProfili(
            yer_kimligi=yer_kimligi,
            yer_ismi=yer.isim,
            fiyat_algisi=BoyutTespiti(deger=FiyatAlgisi.BILGI_YETERSIZ.value, guven=0.0),
            ulasim_kolayligi=BoyutTespiti(deger=UlasimKolayligi.BILGI_YETERSIZ.value, guven=0.0),
            kullanilan_yorum_sayisi=0,
            duygu_ozeti=yapisal_deneyim_metni_uret(
                yer.isim,
                yer.ana_kategori.value,
                yer.alt_kategori,
                tanitim_metni=tanitim,
                yer_kimligi=yer_kimligi,
            ),
        )
        profiller.append(profil)

    cikti_dosyasi = _cikti_kok() / "islenmis" / "yer_profilleri" / f"{sehir.anahtar}_{bugunun_tarihi_dosya_adi()}.jsonl"
    jsonl_yaz(cikti_dosyasi, profiller)
    print(f"[BILGI] {len(profiller)} yer profili yazildi: {cikti_dosyasi}")

    _ozet_yazdir(profiller)

    return cikti_dosyasi


def _ana() -> None:
    konsolu_guvenli_hale_getir()
    ayristirici = argparse.ArgumentParser(description="Yorumlardan cok boyutlu yer profili ve tanitim metni cikarir.")
    ayristirici.add_argument("--sehir", default="samsun", help="veri/ortak/sehir_ayarlari.py icindeki sehir anahtari")
    argumanlar = ayristirici.parse_args()
    calistir(argumanlar.sehir)


if __name__ == "__main__":
    _ana()
