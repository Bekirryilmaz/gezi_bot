"""Development/staging semasini degistirmeden Alembic/model baseline'i denetler."""

from __future__ import annotations

import json

from sqlalchemy import inspect, text
from sqlalchemy.exc import SQLAlchemyError

from sunucu.veritabani.baglanti import motor
from sunucu.veritabani.temel import Taban
import sunucu.veritabani.modeller  # noqa: F401 -- metadata kaydi icin

BEKLENEN_REVIZYON = "0004"
SISTEM_TABLOLARI = {"alembic_version", "spatial_ref_sys"}


def baseline_raporu() -> tuple[dict[str, object], bool]:
    denetci = inspect(motor)
    gercek_tablolar = set(denetci.get_table_names())
    beklenen_tablolar = set(Taban.metadata.tables)
    tablo_sorunlari: dict[str, dict[str, list[str]]] = {}

    for tablo_adi in sorted(beklenen_tablolar & gercek_tablolar):
        tablo = Taban.metadata.tables[tablo_adi]
        beklenen_kolonlar = set(tablo.columns.keys())
        gercek_kolonlar = {kolon["name"] for kolon in denetci.get_columns(tablo_adi)}
        beklenen_indeksler = {indeks.name for indeks in tablo.indexes if indeks.name}
        gercek_indeksler = {
            indeks["name"]
            for indeks in denetci.get_indexes(tablo_adi)
            if indeks.get("name") and not indeks.get("duplicates_constraint")
        }
        sorun = {
            "eksik_kolonlar": sorted(beklenen_kolonlar - gercek_kolonlar),
            "fazla_kolonlar": sorted(gercek_kolonlar - beklenen_kolonlar),
            "eksik_indeksler": sorted(beklenen_indeksler - gercek_indeksler),
            "fazla_indeksler": sorted(gercek_indeksler - beklenen_indeksler),
        }
        if any(sorun.values()):
            tablo_sorunlari[tablo_adi] = sorun

    with motor.connect() as baglanti:
        revizyon = baglanti.execute(text("SELECT version_num FROM alembic_version")).scalar()
        postgis = baglanti.execute(text("SELECT PostGIS_Version()")).scalar()

    rapor: dict[str, object] = {
        "beklenen_revizyon": BEKLENEN_REVIZYON,
        "gercek_revizyon": revizyon,
        "postgis": postgis,
        "eksik_tablolar": sorted(beklenen_tablolar - gercek_tablolar),
        "fazla_tablolar": sorted(gercek_tablolar - beklenen_tablolar - SISTEM_TABLOLARI),
        "tablo_sorunlari": tablo_sorunlari,
    }
    drift_var = bool(
        revizyon != BEKLENEN_REVIZYON
        or not postgis
        or rapor["eksik_tablolar"]
        or rapor["fazla_tablolar"]
        or tablo_sorunlari
    )
    return rapor, drift_var


def main() -> int:
    try:
        rapor, drift_var = baseline_raporu()
    except SQLAlchemyError as hata:
        print(json.dumps({"durum": "erisilemiyor", "hata_turu": type(hata).__name__}, ensure_ascii=False))
        return 2
    print(json.dumps({"durum": "drift" if drift_var else "uyumlu", **rapor}, ensure_ascii=False, indent=2))
    return 1 if drift_var else 0


if __name__ == "__main__":
    raise SystemExit(main())
