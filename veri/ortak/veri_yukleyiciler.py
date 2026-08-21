"""
Ham veri (Yer / HamYorum) yukleme yardimcilari.

veri/esleme/eslestirici.py, veri/kalite_kontrol/rapor_olustur.py ve
veri/duygu_analizi/pipeline_calistir.py -- UCU DE veri/cikti/ham/ altindaki
ayni klasor/dosya-adi kurallarina gore veri okur. Bu mantigin UC AYRI
yerde tekrarlanip zamanla birbirinden sapmasini onlemek icin tek bir
yerde toplanmistir.
"""

from __future__ import annotations

from pathlib import Path

from pydantic import ValidationError

from ortak.sabitler import VeriKaynagi
from veri.ortak.dosya_araclari import jsonl_oku
from veri.ortak.yer_modeli import Yer
from veri.ortak.yorum_modeli import HamYorum

# Her kaynagin ham veri klasoru adi (veri/cikti/ham/<klasor>/ altinda).
KAYNAK_KLASORLERI: dict[VeriKaynagi, str] = {
    VeriKaynagi.OPENSTREETMAP: "osm",
    VeriKaynagi.GOOGLE_MAPS: "google_maps",
    VeriKaynagi.EKSI_SOZLUK: "eksi_sozluk",
    VeriKaynagi.TRIPADVISOR: "tripadvisor",
    VeriKaynagi.BOOKING_COM: "booking_com",
}

# Yer (POI) ureten kaynaklarin dosya adi desenleri (Eksi Sozluk Yer uretmez,
# sadece yorum uretir -- bu yuzden burada YOK).
_YER_DOSYA_DESENLERI: dict[VeriKaynagi, str] = {
    VeriKaynagi.OPENSTREETMAP: "{sehir}_*.jsonl",
    VeriKaynagi.GOOGLE_MAPS: "{sehir}_yerler_*.jsonl",
    VeriKaynagi.TRIPADVISOR: "{sehir}_yerler_*.jsonl",
    VeriKaynagi.BOOKING_COM: "{sehir}_yerler_*.jsonl",
}

# Yorum ureten kaynaklarin dosya adi desenleri (OSM yorum uretmez, sadece
# Yer uretir -- bu yuzden burada YOK).
_YORUM_DOSYA_DESENLERI: dict[VeriKaynagi, str] = {
    VeriKaynagi.EKSI_SOZLUK: "{sehir}_*.jsonl",
    VeriKaynagi.GOOGLE_MAPS: "{sehir}_yorumlar_*.jsonl",
    VeriKaynagi.TRIPADVISOR: "{sehir}_yorumlar_*.jsonl",
    VeriKaynagi.BOOKING_COM: "{sehir}_yorumlar_*.jsonl",
}


def _ham_kok() -> Path:
    # Bu dosya veri/ortak/ altinda, yani parents[1] = veri/
    return Path(__file__).resolve().parents[1] / "cikti" / "ham"


def tum_ham_yerleri_yukle(sehir_anahtari: str, sessiz: bool = False) -> dict[VeriKaynagi, list[Yer]]:
    """veri/cikti/ham/<kaynak>/ altindaki, bu sehre ait TUM Yer (POI)
    kayitlarini kaynak bazinda gruplu olarak okur."""
    ham_kok = _ham_kok()
    sonuc: dict[VeriKaynagi, list[Yer]] = {}

    for kaynak, desen_sablonu in _YER_DOSYA_DESENLERI.items():
        klasor = ham_kok / KAYNAK_KLASORLERI[kaynak]
        if not klasor.exists():
            continue
        desen = desen_sablonu.format(sehir=sehir_anahtari)
        yerler: list[Yer] = []
        for dosya in sorted(klasor.glob(desen)):
            for ham_kayit in jsonl_oku(dosya):
                try:
                    yerler.append(Yer(**ham_kayit))
                except ValidationError as hata:
                    if not sessiz:
                        print(f"[UYARI] {dosya.name} icinde gecersiz Yer kaydi atlandi: {hata}")
        if yerler:
            sonuc[kaynak] = yerler

    return sonuc


def tum_ham_yorumlari_yukle(sehir_anahtari: str, sessiz: bool = False) -> dict[VeriKaynagi, list[HamYorum]]:
    """veri/cikti/ham/<kaynak>/ altindaki, bu sehre ait TUM HamYorum
    kayitlarini kaynak bazinda gruplu olarak okur."""
    ham_kok = _ham_kok()
    sonuc: dict[VeriKaynagi, list[HamYorum]] = {}

    for kaynak, desen_sablonu in _YORUM_DOSYA_DESENLERI.items():
        klasor = ham_kok / KAYNAK_KLASORLERI[kaynak]
        if not klasor.exists():
            continue
        desen = desen_sablonu.format(sehir=sehir_anahtari)
        yorumlar: list[HamYorum] = []
        for dosya in sorted(klasor.glob(desen)):
            for ham_kayit in jsonl_oku(dosya):
                try:
                    yorumlar.append(HamYorum(**ham_kayit))
                except ValidationError as hata:
                    if not sessiz:
                        print(f"[UYARI] {dosya.name} icinde gecersiz HamYorum kaydi atlandi: {hata}")
        if yorumlar:
            sonuc[kaynak] = yorumlar

    return sonuc
