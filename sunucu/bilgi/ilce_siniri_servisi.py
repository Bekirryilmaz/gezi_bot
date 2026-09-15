"""Canonical OSM ilce polygonlarini yazar ve yalniz unique ic noktalari backfill eder."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from sqlalchemy import select, text
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from sunucu.veritabani.arama_modelleri import Ilce
from sunucu.veritabani.bilgi_modelleri import IlceSiniri
from sunucu.veritabani.modeller import Yer
from veri.cografya.ilce_siniri import ILCE_SINIRI_SURUMU


def sinirlari_yaz(oturum: Session, *, sehir_id: str, kayitlar: list[dict[str, Any]]) -> int:
    ilceler = {
        ilce.isim: ilce
        for ilce in oturum.scalars(select(Ilce).where(Ilce.sehir_id == sehir_id, Ilce.aktif_mi.is_(True)))
    }
    yazilan = 0
    for kayit in kayitlar:
        ilce = ilceler.get(kayit["ilce_adi"])
        if ilce is None:
            continue
        degerler = {
            "ilce_id": ilce.id,
            "geometri": f"SRID=4326;{kayit['wkt']}",
            "kaynak": kayit["kaynak"],
            "kaynak_kayit_id": kayit["kaynak_kayit_id"],
            "veri_surumu": kayit.get("veri_surumu") or ILCE_SINIRI_SURUMU,
            "checksum": kayit["checksum"],
            "provenance": kayit.get("provenance") or {},
            "cekilme_zamani": datetime.fromisoformat(kayit["cekilme_zamani"])
            if isinstance(kayit["cekilme_zamani"], str)
            else kayit["cekilme_zamani"],
        }
        sorgu = insert(IlceSiniri).values(**degerler)
        oturum.execute(
            sorgu.on_conflict_do_update(
                constraint="ux_ilce_siniri_kaynak_kayit_surumu",
                set_={
                    "ilce_id": degerler["ilce_id"],
                    "geometri": degerler["geometri"],
                    "checksum": degerler["checksum"],
                    "provenance": degerler["provenance"],
                    "cekilme_zamani": degerler["cekilme_zamani"],
                },
            )
        )
        yazilan += 1
    oturum.flush()
    return yazilan


def yer_sinir_siniflari(oturum: Session, *, sehir_id: str) -> dict[str, str]:
    satirlar = oturum.execute(
        text(
            """
            SELECT y.id AS yer_id,
                   COUNT(*) FILTER (
                     WHERE i.id IS NOT NULL
                       AND ST_Contains(s.geometri, y.konum::geometry)
                   ) AS ic_sayisi,
                   COUNT(*) FILTER (
                     WHERE i.id IS NOT NULL
                       AND ST_Covers(s.geometri, y.konum::geometry)
                   ) AS kaplayan_sayisi,
                   COUNT(*) FILTER (
                     WHERE i.id IS NOT NULL
                       AND ST_Covers(s.geometri, y.konum::geometry)
                       AND NOT ST_Contains(s.geometri, y.konum::geometry)
                   ) AS sinir_sayisi
            FROM yerler y
            LEFT JOIN ilce_sinirlari s
              ON ST_Covers(s.geometri, y.konum::geometry)
            LEFT JOIN ilceler i
              ON i.id = s.ilce_id AND i.sehir_id = :sehir_id
            WHERE y.sehir_id = :sehir_id
              AND y.konum IS NOT NULL
            GROUP BY y.id
            """
        ),
        {"sehir_id": sehir_id},
    ).mappings()
    siniflar = {}
    for satir in satirlar:
        ic = int(satir["ic_sayisi"] or 0)
        kaplayan = int(satir["kaplayan_sayisi"] or 0)
        sinir = int(satir["sinir_sayisi"] or 0)
        if kaplayan == 0:
            durum = "zero"
        elif kaplayan > 1:
            durum = "multiple"
        elif sinir == 1:
            durum = "boundary"
        elif ic == 1:
            durum = "unique"
        else:
            durum = "anomaly"
        siniflar[str(satir["yer_id"])] = durum
    return siniflar


def guvenli_ilce_backfill(oturum: Session, *, sehir_id: str) -> dict[str, int]:
    siniflar = yer_sinir_siniflari(oturum, sehir_id=sehir_id)
    eslesme = {}
    for satir in oturum.execute(
        text(
            """
            SELECT y.id AS yer_id, s.ilce_id
            FROM yerler y
            JOIN ilce_sinirlari s
              ON ST_Contains(s.geometri, y.konum::geometry)
            JOIN ilceler i ON i.id = s.ilce_id
            WHERE y.sehir_id = :sehir_id
              AND i.sehir_id = :sehir_id
            """
        ),
        {"sehir_id": sehir_id},
    ).mappings():
        eslesme[str(satir["yer_id"])] = satir["ilce_id"]
    sayac = {"unique": 0, "atlanan": 0, "yazilan": 0}
    yerler = {
        yer.id: yer
        for yer in oturum.scalars(select(Yer).where(Yer.sehir_id == sehir_id))
    }
    for yer_id, durum in siniflar.items():
        if durum != "unique":
            sayac["atlanan"] += 1
            continue
        sayac["unique"] += 1
        yer = yerler.get(yer_id)
        ilce_id = eslesme.get(yer_id)
        if yer is None or ilce_id is None:
            sayac["atlanan"] += 1
            continue
        if yer.ilce_id not in {None, ilce_id}:
            sayac["atlanan"] += 1
            continue
        if yer.ilce_id == ilce_id:
            continue
        yer.ilce_id = ilce_id
        sayac["yazilan"] += 1
    oturum.flush()
    return sayac


def sehir_id_bul(oturum: Session, sehir_anahtari: str) -> str:
    from sunucu.veritabani.modeller import Sehir
    from veri.ortak.sehir_ayarlari import sehir_getir

    isim = sehir_getir(sehir_anahtari).isim
    sehir = oturum.scalar(select(Sehir).where(Sehir.isim == isim))
    if sehir is None:
        raise ValueError(f"Sehir bulunamadi: {sehir_anahtari}")
    return sehir.id


def sehir_ilcelerini_yukle(oturum: Session, *, sehir_anahtari: str) -> dict[str, Any]:
    from collections import Counter

    from veri.cografya.ilce_siniri import ilceleri_cek

    ham = ilceleri_cek(sehir_anahtari)
    sehir_id = sehir_id_bul(oturum, sehir_anahtari)
    yazilan = sinirlari_yaz(oturum, sehir_id=sehir_id, kayitlar=ham["kayitlar"])
    siniflar = yer_sinir_siniflari(oturum, sehir_id=sehir_id)
    backfill = guvenli_ilce_backfill(oturum, sehir_id=sehir_id)
    return {
        "dogrulama": ham["dogrulama"],
        "sinir_yazilan": yazilan,
        "siniflar": dict(Counter(siniflar.values())),
        "backfill": backfill,
    }
