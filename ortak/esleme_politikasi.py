from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class EslemeSonucu(StrEnum):
    REDDEDILDI = "reddedildi"
    ADAY = "aday"
    OTOMATIK_KABUL = "otomatik_kabul"


@dataclass(frozen=True)
class EslemeDegerlendirmesi:
    sonuc: EslemeSonucu
    confidence: float
    gerekceler: tuple[str, ...]


def eslemeyi_degerlendir(*, ayni_kaynak: bool, ayni_kategori: bool, isim_benzerligi: float, mesafe_metre: float, telefon_eslesiyor: bool = False, adres_eslesiyor: bool = False) -> EslemeDegerlendirmesi:
    if ayni_kaynak or not ayni_kategori or mesafe_metre > 150 or isim_benzerligi < 80:
        return EslemeDegerlendirmesi(EslemeSonucu.REDDEDILDI, 0.0, ("temel_esik_disinda",))
    if mesafe_metre <= 30 and isim_benzerligi >= 96 and (telefon_eslesiyor or adres_eslesiyor):
        return EslemeDegerlendirmesi(EslemeSonucu.OTOMATIK_KABUL, 0.99, ("yakin_konum", "guclu_kimlik_sinyali"))
    guven = min(0.94, 0.5 + isim_benzerligi / 250 + max(0.0, 150 - mesafe_metre) / 1000)
    return EslemeDegerlendirmesi(EslemeSonucu.ADAY, round(guven, 3), ("insan_incelemesi_gerekli",))

