from __future__ import annotations

import uuid
from datetime import UTC, datetime

from sqlalchemy.orm import Session
from sunucu.bilgi.ilce_siniri_servisi import guvenli_ilce_backfill, sinirlari_yaz, yer_sinir_siniflari
from sunucu.veritabani.arama_modelleri import Ilce
from sunucu.veritabani.baglanti import motor
from sunucu.veritabani.modeller import Sehir, Yer


def test_unique_ic_nokta_backfill_edilir_sinir_degismez():
    baglanti = motor.connect()
    islem = baglanti.begin()
    oturum = Session(bind=baglanti)
    try:
        ek = uuid.uuid4().hex
        sehir = Sehir(isim=f"Sinir Sehri {ek}")
        oturum.add(sehir)
        oturum.flush()
        ilce = Ilce(sehir_id=sehir.id, isim="Atakum")
        oturum.add(ilce)
        oturum.flush()
        ic_yer = Yer(
            sehir_id=sehir.id,
            isim=f"Ic yer {ek}",
            ana_kategori="yeme_icme",
            alt_kategori="kafe",
            konum="SRID=4326;POINT(36.1 41.1)",
        )
        dis_yer = Yer(
            sehir_id=sehir.id,
            isim=f"Dis yer {ek}",
            ana_kategori="yeme_icme",
            alt_kategori="kafe",
            konum="SRID=4326;POINT(40.0 45.0)",
        )
        oturum.add_all([ic_yer, dis_yer])
        oturum.flush()
        sinirlari_yaz(
            oturum,
            sehir_id=sehir.id,
            kayitlar=[
                {
                    "ilce_adi": "Atakum",
                    "kaynak": "openstreetmap",
                    "kaynak_kayit_id": f"relation/{ek}",
                    "veri_surumu": "test-v1",
                    "checksum": "a" * 64,
                    "wkt": "MULTIPOLYGON(((36.0 41.0,36.2 41.0,36.2 41.2,36.0 41.2,36.0 41.0)))",
                    "cekilme_zamani": datetime.now(UTC).isoformat(),
                    "provenance": {"lisans": "ODbL"},
                }
            ],
        )
        siniflar = yer_sinir_siniflari(oturum, sehir_id=sehir.id)
        assert siniflar[ic_yer.id] == "unique"
        assert siniflar[dis_yer.id] == "zero"
        ozet = guvenli_ilce_backfill(oturum, sehir_id=sehir.id)
        oturum.refresh(ic_yer)
        oturum.refresh(dis_yer)
        assert ic_yer.ilce_id == ilce.id
        assert dis_yer.ilce_id is None
        assert ozet["yazilan"] == 1
    finally:
        oturum.close()
        islem.rollback()
        baglanti.close()
