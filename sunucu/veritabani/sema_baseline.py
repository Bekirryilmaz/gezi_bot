"""Development/staging semasini degistirmeden Alembic/model baseline'i denetler."""

from __future__ import annotations

import json
from pathlib import Path

from alembic.config import Config
from alembic.script import ScriptDirectory
from sqlalchemy import inspect, text
from sqlalchemy.engine.reflection import Inspector
from sqlalchemy.exc import SQLAlchemyError

import sunucu.veritabani.modeller  # noqa: F401 -- metadata kaydi icin
from sunucu.veritabani.baglanti import motor
from sunucu.veritabani.temel import Taban

SISTEM_TABLOLARI = {"alembic_version", "spatial_ref_sys"}
SUNUCU_KOKU = Path(__file__).resolve().parents[1]


def _kod_headleri() -> list[str]:
    config = Config(str(SUNUCU_KOKU / "alembic.ini"))
    config.set_main_option("script_location", str(SUNUCU_KOKU / "veritabani" / "migrasyonlar"))
    return sorted(ScriptDirectory.from_config(config).get_heads())


def _model_fkleri(
    tablo_adi: str,
) -> set[tuple[tuple[str, ...], str, tuple[str, ...], str | None]]:
    tablo = Taban.metadata.tables[tablo_adi]
    return {
        (
            tuple(kolon.name for kolon in fk.columns),
            next(iter(fk.elements)).column.table.name,
            tuple(eleman.column.name for eleman in fk.elements),
            fk.ondelete,
        )
        for fk in tablo.foreign_key_constraints
    }


def _gercek_fkler(
    denetci: Inspector, tablo_adi: str
) -> set[tuple[tuple[str, ...], str, tuple[str, ...], str | None]]:
    return {
        (
            tuple(fk["constrained_columns"]),
            fk["referred_table"],
            tuple(fk["referred_columns"]),
            fk.get("options", {}).get("ondelete"),
        )
        for fk in denetci.get_foreign_keys(tablo_adi)
    }


def _fk_yaz(
    fkler: set[tuple[tuple[str, ...], str, tuple[str, ...], str | None]],
) -> list[str]:
    return sorted(
        f"{','.join(kolonlar)}->{hedef}({','.join(hedef_kolonlar)})/{ondelete or 'NO ACTION'}"
        for kolonlar, hedef, hedef_kolonlar, ondelete in fkler
    )


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
        beklenen_fkler = _model_fkleri(tablo_adi)
        gercek_fkler = _gercek_fkler(denetci, tablo_adi)
        sorun = {
            "eksik_kolonlar": sorted(beklenen_kolonlar - gercek_kolonlar),
            "fazla_kolonlar": sorted(gercek_kolonlar - beklenen_kolonlar),
            "eksik_indeksler": sorted(beklenen_indeksler - gercek_indeksler),
            "fazla_indeksler": sorted(gercek_indeksler - beklenen_indeksler),
            "eksik_fkler": _fk_yaz(beklenen_fkler - gercek_fkler),
            "fazla_fkler": _fk_yaz(gercek_fkler - beklenen_fkler),
        }
        if any(sorun.values()):
            tablo_sorunlari[tablo_adi] = sorun

    with motor.connect() as baglanti:
        revizyonlar = sorted(
            baglanti.execute(text("SELECT version_num FROM alembic_version")).scalars()
        )
        postgis_extension = baglanti.execute(
            text("SELECT extversion FROM pg_extension WHERE extname='postgis'")
        ).scalar()
        postgis = (
            baglanti.execute(text("SELECT PostGIS_Version()")).scalar()
            if postgis_extension
            else None
        )
        geography = (
            baglanti.execute(
                text(
                    "SELECT type, srid FROM geography_columns "
                    "WHERE f_table_schema=current_schema() AND f_table_name='yerler' "
                    "AND f_geography_column='konum'"
                )
            )
            .mappings()
            .one_or_none()
        )
        gist_indeksi = baglanti.execute(
            text(
                "SELECT pg_get_indexdef(i.indexrelid) AS tanim FROM pg_index i "
                "WHERE i.indrelid='yerler'::regclass "
                "AND i.indexrelid::regclass::text='ix_yerler_konum' "
                "AND i.indisvalid AND i.indisready"
            )
        ).scalar()
        canonical = (
            baglanti.execute(
                text(
                    "SELECT count(*) AS kaynak_baglantisi, "
                    "count(*) FILTER (WHERE yk.sube_id IS NULL) AS null_sube, "
                    "count(*) FILTER (WHERE y.id IS NULL) AS yetim_yer, "
                    "count(*) FILTER (WHERE s.id IS NULL) AS yetim_sube, "
                    "count(*) FILTER (WHERE s.id IS NOT NULL "
                    "AND s.legacy_yer_id IS DISTINCT FROM yk.yer_id) AS legacy_uyusmazligi "
                    "FROM yer_kaynaklari yk "
                    "LEFT JOIN yerler y ON y.id=yk.yer_id "
                    "LEFT JOIN subeler s ON s.id=yk.sube_id"
                )
            )
            .mappings()
            .one()
        )

    sube_kolonu = next(
        (kolon for kolon in denetci.get_columns("yer_kaynaklari") if kolon["name"] == "sube_id"),
        None,
    )
    postgis_sorunlari: list[str] = []
    if not postgis_extension:
        postgis_sorunlari.append("postgis_extension_yok")
    if not geography or geography["type"].upper() != "POINT" or geography["srid"] != 4326:
        postgis_sorunlari.append("yerler.konum_geography_point_4326_degil")
    if not gist_indeksi or "USING gist" not in gist_indeksi:
        postgis_sorunlari.append("ix_yerler_konum_gecerli_gist_degil")

    canonical_sorunlari: list[str] = []
    if sube_kolonu is None or str(sube_kolonu["type"]).upper() != "UUID":
        canonical_sorunlari.append("yer_kaynaklari.sube_id_uuid_degil")
    if sube_kolonu is None or sube_kolonu["nullable"]:
        canonical_sorunlari.append("yer_kaynaklari.sube_id_nullable")
    for alan in ("null_sube", "yetim_yer", "yetim_sube", "legacy_uyusmazligi"):
        if canonical[alan]:
            canonical_sorunlari.append(f"{alan}:{canonical[alan]}")

    headler = _kod_headleri()
    rapor: dict[str, object] = {
        "beklenen_headler": headler,
        "gercek_revizyonlar": revizyonlar,
        "postgis": {"extension": postgis_extension, "surum": postgis},
        "postgis_sorunlari": postgis_sorunlari,
        "eksik_tablolar": sorted(beklenen_tablolar - gercek_tablolar),
        "fazla_tablolar": sorted(gercek_tablolar - beklenen_tablolar - SISTEM_TABLOLARI),
        "tablo_sorunlari": tablo_sorunlari,
        "canonical_kaynak_baglari": dict(canonical),
        "canonical_sorunlari": canonical_sorunlari,
    }
    drift_var = bool(
        revizyonlar != headler
        or postgis_sorunlari
        or rapor["eksik_tablolar"]
        or rapor["fazla_tablolar"]
        or tablo_sorunlari
        or canonical_sorunlari
    )
    return rapor, drift_var


def main() -> int:
    try:
        rapor, drift_var = baseline_raporu()
    except SQLAlchemyError as hata:
        print(
            json.dumps(
                {"durum": "erisilemiyor", "hata_turu": type(hata).__name__},
                ensure_ascii=False,
            )
        )
        return 2
    print(
        json.dumps(
            {"durum": "drift" if drift_var else "uyumlu", **rapor},
            ensure_ascii=False,
            indent=2,
        )
    )
    return 1 if drift_var else 0


if __name__ == "__main__":
    raise SystemExit(main())
