"""
Duygu analizi pipeline'i -- ana calistirma betigi.

veri/cikti/ham/ altindaki TUM ham yorumlari (Eksi Sozluk, Google Maps,
TripAdvisor) okur, her biri icin:
  1. Genel duygu skorunu/etiketini (veri/duygu_analizi/model.py -- Turkce
     BERT tabanli 3-sinifli model) hesaplar,
  2. Konu (aspect) bazli duygulari (veri/duygu_analizi/konu_analizi.py --
     anahtar kelime + kucuk sozluk tabanli, seffaf yontem) cikarir,
ve sonucu veri/ortak/yorum_modeli.py::IslenmisYorum olarak
veri/cikti/islenmis/yorumlar/<sehir>_<tarih>.jsonl dosyasina yazar.

Bu dosya, veritabanina yukleme (import) asamasinda dogrudan `yorumlar`
tablosuna (bkz. sunucu/veritabani/modeller.py::Yorum) aktarilmaya hazir
haldedir.

Calistirma (repo kokunden):
    python -m veri.duygu_analizi.pipeline_calistir --sehir samsun
"""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path

from tqdm import tqdm

from ortak.sabitler import DuyguEtiketi, VeriKaynagi
from veri.duygu_analizi.konu_analizi import konulari_tespit_et
from veri.duygu_analizi.model import MODEL_ADI, toplu_duygu_tahmin_et
from veri.ortak.dosya_araclari import bugunun_tarihi_dosya_adi, jsonl_yaz
from veri.ortak.metin_araclari import konsolu_guvenli_hale_getir
from veri.ortak.sehir_ayarlari import sehir_getir
from veri.ortak.veri_yukleyiciler import tum_ham_yorumlari_yukle
from veri.ortak.yorum_modeli import HamYorum, IslenmisYorum


def _yorumlari_isle(yorumlar: list[HamYorum], yigin_boyutu: int) -> list[IslenmisYorum]:
    metinler = [y.yorum_metni for y in yorumlar]
    genel_duygular = toplu_duygu_tahmin_et(metinler, yigin_boyutu=yigin_boyutu)

    islenmis: list[IslenmisYorum] = []
    for ham_yorum, (duygu_etiketi, duygu_skoru) in tqdm(
        zip(yorumlar, genel_duygular), total=len(yorumlar), desc="Duygu analizi", unit="yorum"
    ):
        konu_duygulari = konulari_tespit_et(ham_yorum.yorum_metni, genel_duygu=duygu_etiketi)
        islenmis.append(
            IslenmisYorum(
                **ham_yorum.model_dump(),
                duygu_skoru=duygu_skoru,
                duygu_etiketi=duygu_etiketi,
                konu_duygulari=konu_duygulari,
                analiz_model_adi=MODEL_ADI,
            )
        )
    return islenmis


def _ozet_yazdir(sehir_isim: str, kaynak_bazli_islenmis: dict[VeriKaynagi, list[IslenmisYorum]]) -> None:
    tum_islenmis = [y for liste in kaynak_bazli_islenmis.values() for y in liste]
    if not tum_islenmis:
        print("[UYARI] Islenecek hicbir yorum bulunamadi.")
        return

    print(f"\n[BILGI] === '{sehir_isim}' Duygu Analizi Ozeti ===")
    print(f"[BILGI] Toplam islenen yorum: {len(tum_islenmis)}")

    for kaynak, liste in kaynak_bazli_islenmis.items():
        dagilim = Counter(y.duygu_etiketi.value for y in liste)
        print(f"[BILGI] {kaynak.value} ({len(liste)} yorum): {dict(dagilim)}")

    genel_dagilim = Counter(y.duygu_etiketi.value for y in tum_islenmis)
    ortalama_skor = sum(y.duygu_skoru for y in tum_islenmis) / len(tum_islenmis)
    print(f"[BILGI] Genel duygu dagilimi: {dict(genel_dagilim)}")
    print(f"[BILGI] Ortalama duygu skoru: {ortalama_skor:.3f} (-1 tamamen olumsuz, +1 tamamen olumlu)")

    konu_sayaci: Counter[str] = Counter()
    konu_duygu_dagilimi: dict[str, Counter] = {}
    for yorum in tum_islenmis:
        for konu_duygusu in yorum.konu_duygulari:
            konu_sayaci[konu_duygusu.konu] += 1
            konu_duygu_dagilimi.setdefault(konu_duygusu.konu, Counter())[konu_duygusu.duygu_etiketi.value] += 1

    if konu_sayaci:
        print("[BILGI] En cok bahsedilen konular:")
        for konu, adet in konu_sayaci.most_common(10):
            print(f"[BILGI]   - {konu} ({adet} kez): {dict(konu_duygu_dagilimi[konu])}")
    else:
        print("[UYARI] Hicbir yorumda taninan bir konu (aspect) tespit edilemedi.")


def calistir(sehir_anahtari: str, yigin_boyutu: int = 16) -> Path | None:
    sehir = sehir_getir(sehir_anahtari)

    kaynak_bazli_ham = tum_ham_yorumlari_yukle(sehir_anahtari)
    if not kaynak_bazli_ham:
        print(f"[UYARI] '{sehir.isim}' icin hicbir kaynaktan ham yorum bulunamadi. Once toplayicilari calistir.")
        return None

    toplam = sum(len(v) for v in kaynak_bazli_ham.values())
    print(f"[BILGI] Toplam {toplam} ham yorum okundu, duygu analizi basliyor (model: {MODEL_ADI})...")

    kaynak_bazli_islenmis: dict[VeriKaynagi, list[IslenmisYorum]] = {}
    for kaynak, yorumlar in kaynak_bazli_ham.items():
        print(f"[BILGI] '{kaynak.value}' isleniyor ({len(yorumlar)} yorum)...")
        kaynak_bazli_islenmis[kaynak] = _yorumlari_isle(yorumlar, yigin_boyutu)

    cikti_dosyasi = (
        Path(__file__).resolve().parents[1] / "cikti" / "islenmis" / "yorumlar" / f"{sehir.anahtar}_{bugunun_tarihi_dosya_adi()}.jsonl"
    )
    tum_islenmis = [y for liste in kaynak_bazli_islenmis.values() for y in liste]
    jsonl_yaz(cikti_dosyasi, tum_islenmis)
    print(f"[BILGI] Islenmis yorumlar yazildi: {cikti_dosyasi}")

    _ozet_yazdir(sehir.isim, kaynak_bazli_islenmis)

    return cikti_dosyasi


def _ana() -> None:
    konsolu_guvenli_hale_getir()
    ayristirici = argparse.ArgumentParser(description="Ham yorumlara duygu analizi ve konu etiketleme uygular.")
    ayristirici.add_argument("--sehir", default="samsun", help="veri/ortak/sehir_ayarlari.py icindeki sehir anahtari")
    ayristirici.add_argument("--yigin-boyutu", type=int, default=16, help="Modelin bir seferde isleyecegi yorum sayisi")
    argumanlar = ayristirici.parse_args()
    calistir(argumanlar.sehir, yigin_boyutu=argumanlar.yigin_boyutu)


if __name__ == "__main__":
    _ana()
