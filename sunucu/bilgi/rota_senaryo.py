"""Rota motoru yazmadan aday uygunluk senaryolari."""

from __future__ import annotations

from typing import Any

from ortak.sabitler import RotaHazirlikDurumu, TamamlikHucresi

_ILCE_ES = {
    "ilkadim": ("İlkadım", "Ilkadim", "ilkadim"),
    "atakum": ("Atakum", "atakum"),
}

SENARYO_TANIMLARI: dict[str, dict[str, Any]] = {
    "A": {"ilce": "atakum", "amaclar": frozenset({"kahve_icmek", "yemek_yemek"})},
    "B": {
        "ilce": "atakum",
        "amaclar": frozenset({"kahve_icmek"}),
        "sessiz": True,
    },
    "C": {
        "ilce": "ilkadim",
        "amaclar": frozenset({"tarihi_kulturel_ziyaret", "yemek_yemek"}),
    },
    "D": {
        "amaclar": frozenset(
            {"tarihi_kulturel_ziyaret", "kahve_icmek", "yemek_yemek"}
        )
    },
    "E": {
        "amaclar": frozenset(
            {"tarihi_kulturel_ziyaret", "kahve_icmek", "yemek_yemek"}
        ),
        "sure_dilimi": "yarim_gun",
    },
    "F": {
        "amaclar": frozenset(
            {"tarihi_kulturel_ziyaret", "kahve_icmek", "yemek_yemek"}
        ),
        "sure_dilimi": "tam_gun",
    },
}


def _ilce_uyar(ilce_adi: str | None, istenen: str | None) -> bool:
    if not istenen:
        return True
    adlar = _ILCE_ES.get(istenen, (istenen,))
    return (ilce_adi or "") in adlar


def _amac_uyar(satir: dict[str, Any], amaclar: frozenset[str] | None) -> bool:
    if not amaclar:
        return True
    return bool(amaclar & set(satir.get("amaclar") or []))


def _sessiz_uyar(satir: dict[str, Any], sessiz: bool) -> bool:
    if not sessiz:
        return True
    kayit = (satir.get("nlp") or {}).get("sessiz_ortam") or {}
    return bool(kayit.get("preference_eligible"))


def senaryo_uygunlugunu_olc(satirlar: list[dict[str, Any]], senaryo_id: str) -> dict[str, Any]:
    tanim = SENARYO_TANIMLARI[senaryo_id]
    filtrelenen = [
        satir
        for satir in satirlar
        if _ilce_uyar(satir.get("ilce_adi"), tanim.get("ilce"))
        and _amac_uyar(satir, tanim.get("amaclar"))
        and _sessiz_uyar(satir, bool(tanim.get("sessiz")))
    ]
    hazir = RotaHazirlikDurumu.ROTA_HAZIR.value
    sinirli = RotaHazirlikDurumu.ROTA_SINIRLI.value
    kapali = RotaHazirlikDurumu.ROTA_KAPALI.value
    uygun = [
        satir
        for satir in filtrelenen
        if (satir.get("rota_hazirlik") or {}).get("durum") in {hazir, sinirli}
    ]
    bloklanan = [
        satir
        for satir in filtrelenen
        if (satir.get("rota_hazirlik") or {}).get("durum") == kapali
    ]
    saat_bilinen = sum(
        1
        for satir in uygun
        if (satir.get("matris") or {}).get("calisma_saatleri")
        == TamamlikHucresi.BILINIYOR.value
    )
    sure_tahmini = sum(
        1
        for satir in uygun
        if (satir.get("ziyaret_suresi") or {}).get("kaynak")
        in {"planlama_tahmini", "dogrulanmis_sure", "kullanici_secimi"}
        or (satir.get("ziyaret_suresi") or {}).get("tipik_dk")
    )
    return {
        "senaryo": senaryo_id,
        "uygun_aday": len(uygun),
        "rota_hazir": sum(
            1 for satir in uygun if (satir.get("rota_hazirlik") or {}).get("durum") == hazir
        ),
        "rota_sinirli": sum(
            1 for satir in uygun if (satir.get("rota_hazirlik") or {}).get("durum") == sinirli
        ),
        "saat_bilinen": saat_bilinen,
        "sure_tahmini_var": sure_tahmini,
        "bloklanan": len(bloklanan),
        "sure_dilimi": tanim.get("sure_dilimi"),
    }


def senaryo_setini_olc(satirlar: list[dict[str, Any]]) -> dict[str, Any]:
    return {kod: senaryo_uygunlugunu_olc(satirlar, kod) for kod in SENARYO_TANIMLARI}
