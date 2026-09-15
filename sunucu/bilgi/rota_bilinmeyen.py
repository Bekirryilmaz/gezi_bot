"""FAZ 26 icin unknown sozlesmesi. Rota motoru bu fazda yazilmaz."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ortak.sabitler import RotaBilinmeyenDavranis

_SOZLESME: dict[str, tuple[RotaBilinmeyenDavranis, bool, str]] = {
    "calisma_saati_bilinmiyor": (
        RotaBilinmeyenDavranis.SINIRLI_UYARI,
        False,
        "Gitmeden once saatini dogrula",
    ),
    "ziyaret_suresi_tahmini": (
        RotaBilinmeyenDavranis.SINIRLI_UYARI,
        False,
        "Sure yalniz planlama tahmini; fact degil",
    ),
    "gecis_bilinmiyor": (
        RotaBilinmeyenDavranis.SINIRLI_UYARI,
        False,
        "Duraklar arasi gecis suresi bilinmiyor",
    ),
    "rezervasyon_bilinmiyor": (
        RotaBilinmeyenDavranis.SINIRLI_UYARI,
        False,
        "Rezervasyon gerekip gerekmedigi bilinmiyor",
    ),
    "gecici_kapanis_bilinmiyor": (
        RotaBilinmeyenDavranis.SINIRLI_UYARI,
        False,
        "Gecici kapanis bilinmiyor; acik varsayilmaz",
    ),
    "kimlik_karantina": (
        RotaBilinmeyenDavranis.HARD_BLOK,
        False,
        "Kimlik karantina; rota adayi olamaz",
    ),
    "koordinat_gecersiz": (
        RotaBilinmeyenDavranis.HARD_BLOK,
        False,
        "Gecerli koordinat yok",
    ),
    "sube_aktif_degil": (
        RotaBilinmeyenDavranis.HARD_BLOK,
        False,
        "Sube aktif degil",
    ),
}


@dataclass(frozen=True)
class RotaBilinmeyenOzeti:
    konu: str
    davranis: RotaBilinmeyenDavranis
    acik_iddiasi: bool
    uyari: str

    def sozluk(self) -> dict[str, Any]:
        return {
            "konu": self.konu,
            "davranis": self.davranis.value,
            "acik_iddiasi": self.acik_iddiasi,
            "uyari": self.uyari,
        }


def rota_bilinmeyen_davranisi(konu: str) -> RotaBilinmeyenOzeti:
    if konu not in _SOZLESME:
        raise KeyError(konu)
    davranis, acik, uyari = _SOZLESME[konu]
    return RotaBilinmeyenOzeti(
        konu=konu, davranis=davranis, acik_iddiasi=acik, uyari=uyari
    )


def akilli_rota_go_degerlendirmesi(girdi: dict[str, Any]) -> dict[str, Any]:
    """rota_hazir sayisi tek GO kriteri degildir."""
    senaryolar = {
        anahtar: girdi[anahtar]
        for anahtar in ("A", "B", "C", "D", "E", "F")
        if anahtar in girdi
    }
    uygun = {anahtar: int(ozet.get("uygun_aday") or 0) for anahtar, ozet in senaryolar.items()}
    cekirdek = tuple(girdi.get("desteklenen_amaclar") or ())
    desteklenmeyen = tuple(girdi.get("desteklenmeyen_amaclar") or ())
    senaryo_yeter = all(sayi >= 1 for sayi in uygun.values()) if uygun else False
    return {
        "kahvalti_zorunlu": False,
        "calisma_zorunlu": False,
        "cekirdek_amaclar": list(cekirdek),
        "desteklenmeyen_amaclar": list(desteklenmeyen),
        "senaryo_uygun_aday": uygun,
        "senaryo_en_az_bir_aday": senaryo_yeter,
        "rota_hazir_tek_kriter": False,
        "kirilim": {
            "rota_hazir_tek_kriter_degil": True,
            "unknown_limited_route": True,
            "kahvalti_calisma_mvp_disi": True,
        },
    }
