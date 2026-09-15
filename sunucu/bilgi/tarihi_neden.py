"""Tarihi/kulturel rota_hazir=0 neden kodlari."""

from __future__ import annotations

from typing import Any

from ortak.sabitler import TamamlikHucresi


def tarihi_mekan_nedenleri(satir: dict[str, Any]) -> tuple[str, ...]:
    nedenler: list[str] = []
    matris = satir.get("matris") or {}
    kimlik = satir.get("kimlik_sinifi") or ""
    if kimlik in {"karantina", "supheli"} or matris.get("kimlik") in {
        TamamlikHucresi.CELISKILI.value,
        TamamlikHucresi.BILINMIYOR.value,
    }:
        nedenler.append("kimlik_problemi")
    if matris.get("calisma_saatleri") != TamamlikHucresi.BILINIYOR.value:
        nedenler.append("calisma_saati_eksik")
    sure = satir.get("ziyaret_suresi") or {}
    if not sure.get("fact_mi"):
        nedenler.append("ziyaret_suresi_fact_degil")
    if matris.get("amac") != TamamlikHucresi.BILINIYOR.value:
        nedenler.append("amac_eksik")
    hazirlik = satir.get("rota_hazirlik") or {}
    if hazirlik.get("durum") not in {"rota_hazir", "rota_sinirli"}:
        if "yayin_uygun_degil" in (hazirlik.get("neden_kodlari") or []):
            nedenler.append("yayin_eksik")
        nedenler.append("rota_kritik_eksik")
    return tuple(dict.fromkeys(nedenler))
