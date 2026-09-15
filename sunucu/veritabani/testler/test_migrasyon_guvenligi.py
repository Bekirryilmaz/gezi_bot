from __future__ import annotations

import json
import os
import subprocess
import sys
import uuid
from collections.abc import Callable, Generator
from pathlib import Path

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL, make_url
from sqlalchemy.exc import SQLAlchemyError
from sunucu.veritabani.baglanti import VERITABANI_URL
from sunucu.veritabani.migrasyonlar.karsilastirma import nesneyi_karsilastir

REPO_KOKU = Path(__file__).resolve().parents[3]
SUNUCU_KOKU = REPO_KOKU / "sunucu"


def _alembic(veritabani_url: str, *komut: str) -> subprocess.CompletedProcess[str]:
    ortam = {**os.environ, "VERITABANI_URL": veritabani_url, "PYTHONDONTWRITEBYTECODE": "1"}
    return subprocess.run(
        [sys.executable, "-m", "alembic", *komut],
        cwd=SUNUCU_KOKU,
        env=ortam,
        capture_output=True,
        text=True,
        check=True,
    )


def _baseline(veritabani_url: str) -> dict[str, object]:
    ortam = {**os.environ, "VERITABANI_URL": veritabani_url, "PYTHONDONTWRITEBYTECODE": "1"}
    sonuc = subprocess.run(
        [sys.executable, "-m", "sunucu.veritabani.sema_baseline"],
        cwd=REPO_KOKU,
        env=ortam,
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(sonuc.stdout)


@pytest.fixture
def gecici_veritabani_uretici() -> Generator[Callable[[], str], None, None]:
    admin_url = make_url(
        os.environ.get(
            "TEST_ADMIN_VERITABANI_URL", "postgresql+psycopg://postgres@localhost:5432/postgres"
        )
    )
    olusturulanlar: list[str] = []
    try:
        admin_motor = create_engine(admin_url, isolation_level="AUTOCOMMIT")
        with admin_motor.connect() as baglanti:
            baglanti.execute(text("SELECT 1"))
    except SQLAlchemyError as hata:
        pytest.fail(f"Gecici PostgreSQL veritabani olusturulamiyor: {type(hata).__name__}")

    uygulama_url = make_url(VERITABANI_URL)
    if not uygulama_url.username:
        pytest.fail("VERITABANI_URL icinde uygulama rolu yok")
    uygulama_rolu = admin_motor.dialect.identifier_preparer.quote(uygulama_url.username)

    def olustur() -> str:
        ad = f"samandira_migration_test_{uuid.uuid4().hex}"
        with admin_motor.connect() as baglanti:
            baglanti.execute(text(f'CREATE DATABASE "{ad}" OWNER {uygulama_rolu}'))
        olusturulanlar.append(ad)
        yeni_admin_url: URL = admin_url.set(database=ad)
        extension_motoru = create_engine(yeni_admin_url, isolation_level="AUTOCOMMIT")
        with extension_motoru.connect() as baglanti:
            baglanti.execute(text("CREATE EXTENSION IF NOT EXISTS postgis"))
        extension_motoru.dispose()
        return uygulama_url.set(database=ad).render_as_string(hide_password=False)

    yield olustur

    with admin_motor.connect() as baglanti:
        for ad in olusturulanlar:
            baglanti.execute(
                text("SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname=:ad"),
                {"ad": ad},
            )
            baglanti.execute(text(f'DROP DATABASE IF EXISTS "{ad}"'))
    admin_motor.dispose()


def test_postgis_sistem_tablosu_dar_kapsamla_haric_tutulur() -> None:
    assert not nesneyi_karsilastir(None, "spatial_ref_sys", "table", True, None)
    assert nesneyi_karsilastir(None, "spatial_ref_sys", "table", False, None)
    assert nesneyi_karsilastir(None, "yerler", "table", True, None)
    assert nesneyi_karsilastir(None, "ix_yerler_konum", "index", True, None)


def test_fresh_db_head_schema_check_ve_baseline(
    gecici_veritabani_uretici: Callable[[], str],
) -> None:
    url = gecici_veritabani_uretici()
    _alembic(url, "upgrade", "head")
    assert "0013" in _alembic(url, "current").stdout
    assert "No new upgrade operations detected" in _alembic(url, "check").stdout

    rapor = _baseline(url)
    assert rapor["durum"] == "uyumlu"
    assert rapor["postgis_sorunlari"] == []
    assert rapor["canonical_sorunlari"] == []


def test_0004_head_roundtrip_kaynak_baglarini_korur(
    gecici_veritabani_uretici: Callable[[], str],
) -> None:
    url = gecici_veritabani_uretici()
    _alembic(url, "upgrade", "0004")
    sehir_id, yer_id = str(uuid.uuid4()), str(uuid.uuid4())
    kaynak_idleri = [str(uuid.uuid4()), str(uuid.uuid4())]
    motor = create_engine(url)
    with motor.begin() as baglanti:
        baglanti.execute(
            text("INSERT INTO sehirler (id, isim) VALUES (:id, 'Test Sehri')"),
            {"id": sehir_id},
        )
        baglanti.execute(
            text(
                "INSERT INTO yerler (id, sehir_id, isim, ana_kategori, alt_kategori, konum) "
                "VALUES (:id, :sehir_id, 'Test Yeri', 'doga', 'park', "
                "ST_GeogFromText('SRID=4326;POINT(36.3 41.3)'))"
            ),
            {"id": yer_id, "sehir_id": sehir_id},
        )
        for sira, kaynak_id in enumerate(kaynak_idleri):
            baglanti.execute(
                text(
                    "INSERT INTO yer_kaynaklari (id, yer_id, kaynak, kaynak_id) "
                    "VALUES (:id, :yer_id, :kaynak, :kaynak_id)"
                ),
                {
                    "id": kaynak_id,
                    "yer_id": yer_id,
                    "kaynak": f"test_{sira}",
                    "kaynak_id": f"kaynak-{sira}",
                },
            )

    _alembic(url, "upgrade", "head")
    with motor.connect() as baglanti:
        baglar = baglanti.execute(
            text("SELECT id::text, yer_id::text, sube_id::text FROM yer_kaynaklari ORDER BY id")
        ).all()
        assert {satir[0] for satir in baglar} == set(kaynak_idleri)
        assert all(satir[1] == yer_id and satir[2] == yer_id for satir in baglar)
        assert (
            baglanti.execute(
                text(
                    "SELECT count(*) FROM yer_kaynaklari yk "
                    "LEFT JOIN subeler s ON s.id=yk.sube_id WHERE s.id IS NULL"
                )
            ).scalar_one()
            == 0
        )

    _alembic(url, "downgrade", "0011")
    with motor.connect() as baglanti:
        assert baglanti.execute(text("SELECT count(*) FROM yer_kaynaklari")).scalar_one() == 2
    _alembic(url, "upgrade", "head")
    _alembic(url, "upgrade", "head")
    assert "No new upgrade operations detected" in _alembic(url, "check").stdout
    with motor.connect() as baglanti:
        assert baglanti.execute(text("SELECT count(*) FROM yer_kaynaklari")).scalar_one() == 2
    motor.dispose()
