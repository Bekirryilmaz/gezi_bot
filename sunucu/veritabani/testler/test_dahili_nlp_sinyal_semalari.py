from __future__ import annotations

import os
import subprocess
import sys
import uuid
from collections.abc import Callable, Generator
from datetime import UTC, datetime
from pathlib import Path
from typing import get_type_hints

import pytest
import sunucu.veritabani.modeller as modeller
from geoalchemy2 import Geometry
from sqlalchemy import UniqueConstraint, create_engine, inspect, select, text
from sqlalchemy.engine import URL, Engine, make_url
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session
from sunucu.veritabani.baglanti import VERITABANI_URL
from sunucu.veritabani.temel import Taban
from sunucu.veritabani.testler.gecici_veritabani import admin_url_adaylari

REPO_KOKU = Path(__file__).resolve().parents[3]
SUNUCU_KOKU = REPO_KOKU / "sunucu"


def _alembic(
    veritabani_url: str, *komut: str, check: bool = True
) -> subprocess.CompletedProcess[str]:
    ortam = {
        **os.environ,
        "VERITABANI_URL": veritabani_url,
        "PYTHONDONTWRITEBYTECODE": "1",
    }
    return subprocess.run(
        [sys.executable, "-m", "alembic", *komut],
        cwd=SUNUCU_KOKU,
        env=ortam,
        capture_output=True,
        text=True,
        check=check,
    )


@pytest.fixture
def gecici_veritabani_uretici() -> Generator[Callable[[], str], None, None]:
    olusturulanlar: list[str] = []
    admin_motor: Engine | None = None
    admin_url: URL | None = None
    son_hata: SQLAlchemyError | None = None
    for aday_url in admin_url_adaylari():
        aday_motor = create_engine(aday_url, isolation_level="AUTOCOMMIT")
        try:
            with aday_motor.connect() as baglanti:
                veritabani_acabilir = baglanti.execute(
                    text("SELECT rolsuper FROM pg_roles WHERE rolname = current_user")
                ).scalar_one()
        except SQLAlchemyError as hata:
            son_hata = hata
            aday_motor.dispose()
            continue
        if not veritabani_acabilir:
            aday_motor.dispose()
            continue
        admin_motor = aday_motor
        admin_url = aday_url
        break
    if admin_motor is None or admin_url is None:
        hata_turu = type(son_hata).__name__ if son_hata else "BilinmeyenHata"
        pytest.fail(f"Gecici PostgreSQL veritabani olusturulamiyor: {hata_turu}")

    uygulama_url = make_url(VERITABANI_URL)
    if not uygulama_url.username:
        pytest.fail("VERITABANI_URL icinde uygulama rolu yok")
    uygulama_rolu = admin_motor.dialect.identifier_preparer.quote(uygulama_url.username)

    def olustur() -> str:
        ad = f"samandira_nlp_schema_test_{uuid.uuid4().hex}"
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


def _temel_kayitlari_ekle(
    oturum: Session,
) -> tuple[object, object, object, object]:
    ek = uuid.uuid4().hex
    sehir = modeller.Sehir(isim=f"Test Sehri {ek}")
    oturum.add(sehir)
    oturum.flush()
    ilce = modeller.Ilce(sehir_id=sehir.id, isim=f"Test Ilcesi {ek}")
    yer = modeller.Yer(
        sehir_id=sehir.id,
        isim=f"Test Yeri {ek}",
        ana_kategori="doga_manzara",
        alt_kategori="park",
        konum="SRID=4326;POINT(36.3 41.3)",
    )
    oturum.add_all([ilce, yer])
    oturum.flush()
    yer_kimligi = modeller.YerKimligi(sehir_id=sehir.id)
    oturum.add(yer_kimligi)
    oturum.flush()
    sube = modeller.Sube(
        yer_kimligi_id=yer_kimligi.id,
        legacy_yer_id=yer.id,
        guncel_isim=yer.isim,
    )
    oturum.add(sube)
    oturum.flush()
    simdi = datetime.now(UTC)
    batch = modeller.VeriBatch(
        kaynak="test",
        kosu_anahtari=f"nlp-{ek}",
        baslama_zamani=simdi,
    )
    yorum = modeller.Yorum(
        yer_id=yer.id,
        kaynak="test",
        kaynak_yorum_id=f"yorum-{ek}",
        yorum_metni="Sentetik test yorumu.",
    )
    oturum.add_all([batch, yorum])
    oturum.flush()
    return ilce, sube, batch, yorum


def _aday_uret(
    *,
    sube_id: str | None,
    batch_id: str,
    yorum_id: str,
    span_hash: str = "a" * 64,
) -> object:
    aday_sinifi = getattr(modeller, "DahiliGozlemAdayi")
    return aday_sinifi(
        veri_batch_id=batch_id,
        yorum_id=yorum_id,
        kaynak="test",
        kaynak_kayit_id="yorum-1",
        kaynak_yer_id="yer-1",
        sube_id=sube_id,
        aile="wifi",
        gozlem_turu="fact_signal",
        yon="support",
        deger=True,
        cikarim_yontemi="kural",
        model_surumu="model-v1",
        kural_surumu="kural-v1",
        cikarim_guven_sinifi="yuksek",
        guven_kirilimi={"desen": "wifi_var"},
        temporal_durum="unknown",
        gozlem_zamani=None,
        span_hash=span_hash,
        dahili_referans=f"aday:{span_hash}",
        sube_guven_durumu="eslesti",
        kullanim_durumu="aktif",
    )


def test_model_metadata_yeni_tablolari_ve_geometry_tipini_tasir() -> None:
    beklenen_tablolar = {
        "dahili_gozlem_adaylari",
        "dahili_sinyal_ozetleri",
        "ilce_sinirlari",
    }
    assert beklenen_tablolar <= set(Taban.metadata.tables)
    geometri = Taban.metadata.tables["ilce_sinirlari"].c.geometri
    assert isinstance(geometri.type, Geometry)
    assert geometri.type.geometry_type == "MULTIPOLYGON"
    assert geometri.type.srid == 4326


def test_aday_unique_anahtari_sube_duzeltmesinden_bagimsiz_ve_pg14_uyumlu() -> None:
    tablo = Taban.metadata.tables["dahili_gozlem_adaylari"]
    kisit = next(
        kisit
        for kisit in tablo.constraints
        if isinstance(kisit, UniqueConstraint) and kisit.name == "ux_dahili_gozlem_adayi_idempotent"
    )
    assert tuple(kolon.name for kolon in kisit.columns) == (
        "yorum_id",
        "model_surumu",
        "kural_surumu",
        "aile",
        "gozlem_turu",
        "yon",
        "span_hash",
    )
    assert "sube_id" not in kisit.columns
    assert not kisit.dialect_options["postgresql"].get("nulls_not_distinct")

    sql = _alembic(VERITABANI_URL, "upgrade", "0014:0015", "--sql").stdout.upper()
    assert "NULLS NOT DISTINCT" not in sql


def test_model_server_defaultlari_migration_sozlesmesini_tasir() -> None:
    beklenenler = {
        "dahili_gozlem_adaylari": {
            "id": "gen_random_uuid()",
            "guven_kirilimi": "'{}'::jsonb",
            "kullanim_durumu": "'karantina'",
            "olusturulma_zamani": "now()",
        },
        "dahili_sinyal_ozetleri": {
            "id": "gen_random_uuid()",
            "ozet": "'{}'::jsonb",
            "kirilim": "'{}'::jsonb",
            "hesaplanma_zamani": "now()",
        },
        "ilce_sinirlari": {
            "id": "gen_random_uuid()",
            "provenance": "'{}'::jsonb",
        },
    }
    for tablo_adi, kolonlar in beklenenler.items():
        tablo = Taban.metadata.tables[tablo_adi]
        for kolon_adi, beklenen in kolonlar.items():
            server_default = tablo.c[kolon_adi].server_default
            assert server_default is not None, f"{tablo_adi}.{kolon_adi}"
            assert str(server_default.arg) == beklenen


def test_aday_deger_orm_tipi_canonical_skalar_jsonbyi_kapsar() -> None:
    deger_tipi = str(get_type_hints(modeller.DahiliGozlemAdayi)["deger"])
    assert "bool" in deger_tipi
    assert "str" in deger_tipi
    assert "dict" in deger_tipi


def test_ozet_unique_sol_prefix_indeksi_tekrar_edilmez() -> None:
    indeksler = Taban.metadata.tables["dahili_sinyal_ozetleri"].indexes
    assert "ix_dahili_sinyal_ozeti_sube_aile" not in {indeks.name for indeks in indeksler}


def test_ci_admin_urlu_uygulama_kullanicisi_ve_postgres_dbden_turetilir(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("TEST_ADMIN_VERITABANI_URL", raising=False)
    monkeypatch.setenv(
        "VERITABANI_URL",
        "postgresql+psycopg://gezi_ci:gizli@postgres.example:5433/gezi_ci",
    )
    adaylar = admin_url_adaylari()
    assert adaylar[0].username == "gezi_ci"
    assert adaylar[0].password == "gizli"
    assert adaylar[0].host == "postgres.example"
    assert adaylar[0].port == 5433
    assert adaylar[0].database == "postgres"
    assert adaylar[-1].username == "postgres"
    assert adaylar[-1].database == "postgres"

    monkeypatch.setenv(
        "TEST_ADMIN_VERITABANI_URL",
        "postgresql+psycopg://ozel_admin:ozel_sifre@db.test:5440/postgres",
    )
    explicit = admin_url_adaylari()
    assert len(explicit) == 1
    assert explicit[0].username == "ozel_admin"
    assert explicit[0].host == "db.test"


def test_0015_fresh_db_schema_modelle_uyumlu_ve_roundtrip_guvenli(
    gecici_veritabani_uretici: Callable[[], str],
) -> None:
    url = gecici_veritabani_uretici()
    _alembic(url, "upgrade", "head")
    assert "0016" in _alembic(url, "current").stdout
    assert "No new upgrade operations detected" in _alembic(url, "check").stdout

    motor = create_engine(url)
    denetci = inspect(motor)
    assert {
        "dahili_gozlem_adaylari",
        "dahili_sinyal_ozetleri",
        "ilce_sinirlari",
    } <= set(denetci.get_table_names())
    sinir_indeksleri = {indeks["name"]: indeks for indeks in denetci.get_indexes("ilce_sinirlari")}
    assert (
        sinir_indeksleri["ix_ilce_siniri_geometri"]["dialect_options"]["postgresql_using"] == "gist"
    )
    sube_kolonlari = {kolon["name"] for kolon in denetci.get_columns("subeler")}
    assert {"kimlik_kalite_sinifi", "kimlik_kalite_kirilim"} <= sube_kolonlari
    motor.dispose()

    _alembic(url, "downgrade", "0014")
    _alembic(url, "upgrade", "head")
    assert "0016" in _alembic(url, "current").stdout


def test_aday_idempotence_fk_ve_karantina_kisitlari_postgreste_caliser(
    gecici_veritabani_uretici: Callable[[], str],
) -> None:
    url = gecici_veritabani_uretici()
    _alembic(url, "upgrade", "head")
    motor = create_engine(url)
    baglanti = motor.connect()
    islem = baglanti.begin()
    oturum = Session(bind=baglanti)
    try:
        _, sube, batch, yorum = _temel_kayitlari_ekle(oturum)
        oturum.add(
            _aday_uret(
                sube_id=sube.id,
                batch_id=batch.id,
                yorum_id=yorum.id,
            )
        )
        oturum.flush()

        # Sube baglama duzeltmesi ayni extraction'i yeni candidate yapmaz.
        # Upsert/update, mevcut satirin sube_id alanini degistirmelidir.
        savepoint = oturum.begin_nested()
        with pytest.raises(IntegrityError):
            oturum.add(
                _aday_uret(
                    sube_id=None,
                    batch_id=batch.id,
                    yorum_id=yorum.id,
                )
            )
            oturum.flush()
        savepoint.rollback()

        savepoint = oturum.begin_nested()
        with pytest.raises(IntegrityError):
            oturum.add(
                _aday_uret(
                    sube_id=sube.id,
                    batch_id=batch.id,
                    yorum_id=str(uuid.uuid4()),
                    span_hash="b" * 64,
                )
            )
            oturum.flush()
        savepoint.rollback()

        gecersiz = _aday_uret(
            sube_id=sube.id,
            batch_id=batch.id,
            yorum_id=yorum.id,
            span_hash="c" * 64,
        )
        gecersiz.kullanim_durumu = "yayinlandi"
        savepoint = oturum.begin_nested()
        with pytest.raises(IntegrityError):
            oturum.add(gecersiz)
            oturum.flush()
        savepoint.rollback()
    finally:
        oturum.close()
        islem.rollback()
        baglanti.close()
        motor.dispose()


def test_ozet_unique_ve_ilce_multipolygon_davranisi_postgreste_caliser(
    gecici_veritabani_uretici: Callable[[], str],
) -> None:
    url = gecici_veritabani_uretici()
    _alembic(url, "upgrade", "head")
    motor = create_engine(url)
    baglanti = motor.connect()
    islem = baglanti.begin()
    oturum = Session(bind=baglanti)
    try:
        ilce, sube, _, _ = _temel_kayitlari_ekle(oturum)
        ozet_sinifi = getattr(modeller, "DahiliSinyalOzeti")
        ortak = {
            "sube_id": sube.id,
            "aile": "wifi",
            "agregasyon_surumu": "agg-v1",
            "guven_sinifi": "destekli",
            "durum": "aktif",
            "ozet": {
                "support": 3,
                "counter": 1,
                "benzersiz_yorum": 4,
                "tarih_araligi": {"ilk": "2026-09-01", "son": "2026-09-15"},
            },
            "kirilim": {
                "celiski": True,
                "kaynak_cesitliligi": 2,
                "dagilim": {"support": 0.75, "counter": 0.25},
            },
        }
        oturum.add(ozet_sinifi(**ortak))
        oturum.flush()
        savepoint = oturum.begin_nested()
        with pytest.raises(IntegrityError):
            oturum.add(ozet_sinifi(**ortak))
            oturum.flush()
        savepoint.rollback()

        sinir_sinifi = getattr(modeller, "IlceSiniri")
        sinir = sinir_sinifi(
            ilce_id=ilce.id,
            geometri="SRID=4326;MULTIPOLYGON(((36 41,37 41,37 42,36 42,36 41)))",
            kaynak="test",
            kaynak_kayit_id="sinir-1",
            veri_surumu="2026-09",
            checksum="d" * 64,
            provenance={"url": "https://example.test/sinir-1"},
            cekilme_zamani=datetime.now(UTC),
        )
        oturum.add(sinir)
        oturum.flush()
        geometri_bilgisi = oturum.execute(
            select(
                text("ST_GeometryType(geometri)"),
                text("ST_SRID(geometri)"),
            ).select_from(Taban.metadata.tables["ilce_sinirlari"])
        ).one()
        assert geometri_bilgisi == ("ST_MultiPolygon", 4326)

        savepoint = oturum.begin_nested()
        with pytest.raises(IntegrityError):
            oturum.add(
                sinir_sinifi(
                    ilce_id=ilce.id,
                    geometri=("SRID=4326;MULTIPOLYGON(((36 41,37 41,37 42,36 42,36 41)))"),
                    kaynak="test",
                    kaynak_kayit_id="sinir-1",
                    veri_surumu="2026-09",
                    checksum="e" * 64,
                    provenance={},
                    cekilme_zamani=datetime.now(UTC),
                )
            )
            oturum.flush()
        savepoint.rollback()
    finally:
        oturum.close()
        islem.rollback()
        baglanti.close()
        motor.dispose()


def test_yeni_tablolar_parent_silinmesini_restrict_ile_engeller(
    gecici_veritabani_uretici: Callable[[], str],
) -> None:
    url = gecici_veritabani_uretici()
    _alembic(url, "upgrade", "head")
    motor = create_engine(url)
    baglanti = motor.connect()
    islem = baglanti.begin()
    oturum = Session(bind=baglanti)
    try:
        ilce, sube, batch, yorum = _temel_kayitlari_ekle(oturum)
        oturum.add(
            _aday_uret(
                sube_id=sube.id,
                batch_id=batch.id,
                yorum_id=yorum.id,
            )
        )
        oturum.add(
            modeller.DahiliSinyalOzeti(
                sube_id=sube.id,
                aile="wifi",
                agregasyon_surumu="agg-v1",
                guven_sinifi="destekli",
                durum="aktif",
            )
        )
        oturum.add(
            modeller.IlceSiniri(
                ilce_id=ilce.id,
                geometri=("SRID=4326;MULTIPOLYGON(((36 41,37 41,37 42,36 42,36 41)))"),
                kaynak="test",
                kaynak_kayit_id="sinir-restrict",
                veri_surumu="v1",
                checksum="f" * 64,
                cekilme_zamani=datetime.now(UTC),
            )
        )
        oturum.flush()

        for parent in (yorum, batch, sube, ilce):
            savepoint = oturum.begin_nested()
            with pytest.raises(IntegrityError):
                oturum.delete(parent)
                oturum.flush()
            savepoint.rollback()
            oturum.expire(parent)
    finally:
        oturum.close()
        islem.rollback()
        baglanti.close()
        motor.dispose()


def _downgrade_guard_kaydi_ekle(oturum: Session, tablo_adi: str) -> None:
    ilce, sube, batch, yorum = _temel_kayitlari_ekle(oturum)
    if tablo_adi == "dahili_gozlem_adaylari":
        oturum.add(
            _aday_uret(
                sube_id=sube.id,
                batch_id=batch.id,
                yorum_id=yorum.id,
            )
        )
    elif tablo_adi == "dahili_sinyal_ozetleri":
        oturum.add(
            modeller.DahiliSinyalOzeti(
                sube_id=sube.id,
                aile="wifi",
                agregasyon_surumu="agg-v1",
                guven_sinifi="sinirli",
                durum="aktif",
            )
        )
    else:
        oturum.add(
            modeller.IlceSiniri(
                ilce_id=ilce.id,
                geometri=("SRID=4326;MULTIPOLYGON(((36 41,37 41,37 42,36 42,36 41)))"),
                kaynak="test",
                kaynak_kayit_id="sinir-guard",
                veri_surumu="v1",
                checksum="0" * 64,
                cekilme_zamani=datetime.now(UTC),
            )
        )


@pytest.mark.parametrize(
    "tablo_adi",
    [
        "dahili_gozlem_adaylari",
        "dahili_sinyal_ozetleri",
        "ilce_sinirlari",
    ],
)
def test_0015_downgrade_veri_varken_sessizce_tablo_silmez(
    gecici_veritabani_uretici: Callable[[], str],
    tablo_adi: str,
) -> None:
    url = gecici_veritabani_uretici()
    _alembic(url, "upgrade", "head")
    motor: Engine = create_engine(url)
    with Session(motor) as oturum:
        _downgrade_guard_kaydi_ekle(oturum, tablo_adi)
        oturum.commit()
    sonuc = _alembic(url, "downgrade", "0014", check=False)
    assert sonuc.returncode != 0
    assert "0015 downgrade veri kaybina yol acar" in sonuc.stderr
    assert tablo_adi in sonuc.stderr
    assert "0015" in _alembic(url, "current").stdout
    with motor.connect() as baglanti:
        kalan = baglanti.execute(text(f"SELECT count(*) FROM {tablo_adi}")).scalar_one()
        assert kalan >= 1
        for ad in (
            "dahili_gozlem_adaylari",
            "dahili_sinyal_ozetleri",
            "ilce_sinirlari",
        ):
            assert baglanti.execute(
                text("SELECT to_regclass(:ad)"), {"ad": ad}
            ).scalar_one()
    motor.dispose()
