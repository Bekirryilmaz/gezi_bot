"""Mevcut OSM kaynak baglarindaki yapilandirilmis etiketleri ozellikler JSONB'sine yazar."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from sunucu.bilgi.pilot_claimleri import adaylari_yaz
from sunucu.veritabani.modeller import Yer, YerKaynak
from veri.toplayicilar.osm_toplayici import _ozellikleri_cikar, osm_etiketlerini_cek

_YAPISAL_ANAHTARLAR = {
    "opening_hours",
    "wheelchair",
    "outdoor_seating",
    "parking",
    "internet_access",
    "socket",
    "reservation",
    "cuisine",
    "fee",
    "wifi",
    "otopark",
    "acik_alan",
    "rezervasyon_gerekli",
    "engelli_erisimi",
    "ucretsiz",
}


def ozellikleri_birlestir(mevcut: dict[str, Any] | None, yeni: dict[str, Any]) -> dict[str, Any]:
    birlesik = dict(mevcut or {})
    for anahtar, deger in yeni.items():
        if deger is None:
            continue
        if anahtar in _YAPISAL_ANAHTARLAR or birlesik.get(anahtar) in (None, "", [], {}):
            birlesik[anahtar] = deger
    return birlesik


def osm_ozelliklerini_geri_doldur(
    oturum: Session,
    *,
    sehir_id: str,
    dry_run: bool = False,
) -> dict[str, Any]:
    baglar = list(
        oturum.execute(
            select(YerKaynak, Yer)
            .join(Yer, Yer.id == YerKaynak.yer_id)
            .where(YerKaynak.kaynak == "openstreetmap", Yer.sehir_id == sehir_id)
        )
    )
    etiketler = {} if dry_run else osm_etiketlerini_cek([kaynak.kaynak_id for kaynak, _yer in baglar])
    guncellenen = 0
    alan_sayaci: Counter[str] = Counter()
    satirlar: list[dict[str, Any]] = []
    for kaynak, yer in baglar:
        ham = etiketler.get(kaynak.kaynak_id) or {}
        if not ham:
            continue
        ozellik = _ozellikleri_cikar(ham, yer.alt_kategori).model_dump(exclude_none=True)
        birlesik = ozellikleri_birlestir(yer.ozellikler, ozellik)
        for anahtar in _YAPISAL_ANAHTARLAR:
            if birlesik.get(anahtar) not in (None, "", [], {}):
                alan_sayaci[anahtar] += 1
        if birlesik != (yer.ozellikler or {}):
            guncellenen += 1
            if not dry_run:
                yer.ozellikler = birlesik
        satirlar.append(
            {
                "kaynak_id": kaynak.kaynak_id,
                "kaynak_url": f"https://www.openstreetmap.org/{kaynak.kaynak_id}",
                "isim": yer.isim,
                "ana_kategori": yer.ana_kategori,
                "alt_kategori": yer.alt_kategori,
                "sehir": None,
                "ilce": yer.ilce,
                "adres": yer.adres,
                "telefon": yer.telefon,
                "web_sitesi": yer.web_sitesi,
                "enlem": None,
                "boylam": None,
                "ozellikler": birlesik,
            }
        )
    claim_ozet = None
    if not dry_run and satirlar:
        from sunucu.veritabani.modeller import Sehir

        sehir = oturum.get(Sehir, sehir_id)
        for satir in satirlar:
            satir["sehir"] = sehir.isim if sehir is not None else None
        claim_ozet = adaylari_yaz(
            oturum,
            dosya=Path("osm-structured-backfill.jsonl"),
            satirlar=satirlar,
            dry_run=False,
        )
    if not dry_run:
        oturum.flush()
    return {
        "osm_kaynak": len(baglar),
        "etiket_bulunan": len(etiketler),
        "guncellenen_yer": guncellenen,
        "alanlar": dict(alan_sayaci),
        "claim": None if claim_ozet is None else claim_ozet.sozluk(),
    }
