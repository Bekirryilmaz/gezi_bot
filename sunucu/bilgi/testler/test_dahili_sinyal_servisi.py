from __future__ import annotations

import uuid
from datetime import UTC, datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Session
from sunucu.bilgi.aggregation import AGREGASYON_SURUMU, dahili_tercih_kapisi
from sunucu.bilgi.dahili_sinyal_servisi import (
    adaylardan_gozlemler,
    dagilimdan_esikler,
    ozetleri_yaz,
    sube_kaynak_audit,
)
from sunucu.veritabani.baglanti import motor
from sunucu.veritabani.bilgi_modelleri import DahiliGozlemAdayi, DahiliSinyalOzeti, VeriBatch
from sunucu.veritabani.kimlik_modelleri import Sube, YerKimligi
from sunucu.veritabani.modeller import Sehir, Yer, YerKaynak, Yorum


def _oturum():
    baglanti = motor.connect()
    islem = baglanti.begin()
    return baglanti, islem, Session(bind=baglanti)


def _temel(oturum: Session):
    ek = uuid.uuid4().hex
    sehir = Sehir(isim=f"Dahili Sinyal Sehri {ek}")
    oturum.add(sehir)
    oturum.flush()
    yer = Yer(
        sehir_id=sehir.id,
        isim=f"Dahili Kafe {ek}",
        ana_kategori="yeme_icme",
        alt_kategori="kafe",
        konum="SRID=4326;POINT(36.33 41.28)",
    )
    kimlik = YerKimligi(sehir_id=sehir.id)
    oturum.add_all([yer, kimlik])
    oturum.flush()
    sube = Sube(yer_kimligi_id=kimlik.id, legacy_yer_id=yer.id, guncel_isim=yer.isim)
    oturum.add(sube)
    oturum.flush()
    oturum.add(
        YerKaynak(
            yer_id=yer.id,
            kaynak="google_maps",
            kaynak_id=f"place-{ek}",
            sube_id=sube.id,
        )
    )
    batch = VeriBatch(
        kaynak="google_maps_internal_nlp",
        kosu_anahtari=f"test-{ek}",
        baslama_zamani=datetime.now(UTC),
    )
    yorum = Yorum(
        yer_id=yer.id,
        kaynak="google_maps",
        kaynak_yorum_id=f"review-{ek}",
        yorum_metni="WiFi var.",
    )
    oturum.add_all([batch, yorum])
    oturum.flush()
    return sehir, yer, sube, batch, yorum


def test_aday_ozet_yazimi_idempotent_ve_karantinayi_atlar():
    baglanti, islem, oturum = _oturum()
    try:
        _, _, sube, batch, yorum = _temel(oturum)
        ortak = dict(
            veri_batch_id=batch.id,
            yorum_id=yorum.id,
            kaynak="google_maps",
            kaynak_kayit_id=yorum.kaynak_yorum_id,
            kaynak_yer_id="place-1",
            sube_id=sube.id,
            aile="wifi",
            gozlem_turu="fact_signal",
            yon="support",
            deger=True,
            cikarim_yontemi="deterministik_kural",
            model_surumu="m1",
            kural_surumu="k1",
            cikarim_guven_sinifi="dusuk",
            guven_kirilimi={},
            temporal_durum="unknown",
            span_hash="a" * 64,
            dahili_referans="ref-aktif",
            sube_guven_durumu="eslesti",
            kullanim_durumu="aktif",
        )
        oturum.add(DahiliGozlemAdayi(**ortak))
        oturum.add(
            DahiliGozlemAdayi(
                **{
                    **ortak,
                    "span_hash": "b" * 64,
                    "dahili_referans": "ref-karantina",
                    "kullanim_durumu": "karantina",
                    "yon": "counter",
                }
            )
        )
        oturum.flush()
        gozlemler = adaylardan_gozlemler(oturum, sube_idleri=[sube.id])
        ozetleri_yaz(oturum, gozlemler)
        ozetleri_yaz(oturum, gozlemler)
        ozetler = list(
            oturum.scalars(
                select(DahiliSinyalOzeti).where(DahiliSinyalOzeti.sube_id == sube.id)
            )
        )
        assert len(ozetler) == 1
        assert ozetler[0].agregasyon_surumu == AGREGASYON_SURUMU
        assert ozetler[0].ozet["unique_review_count"] == 1
        assert ozetler[0].ozet["counter_observation_count"] == 0
        assert ozetler[0].durum == "karar_disi"
        assert dahili_tercih_kapisi(ozetler[0].ozet)["preference_eligible"] is False
    finally:
        islem.rollback()
        baglanti.close()


def test_dagilimdan_esikler_tertile_gore_uretilir_keyfi_degildir():
    esikler = dagilimdan_esikler([1, 1, 2, 3, 8, 12, 20])
    assert esikler["zayif_max_unique_review"] == 2
    assert esikler["orta_max_unique_review"] == 8
    assert esikler["zayif_max_unique_review"] < esikler["orta_max_unique_review"]


def test_sube_kaynak_audit_ayni_konumlu_tekrar_kaydi_guvenli_sayar():
    baglanti, islem, oturum = _oturum()
    try:
        sehir, yer, sube, _, _ = _temel(oturum)
        oturum.add(
            YerKaynak(
                yer_id=yer.id,
                kaynak="google_maps",
                kaynak_id=f"place-alias-{uuid.uuid4().hex}",
                sube_id=sube.id,
            )
        )
        oturum.flush()
        rapor = sube_kaynak_audit(oturum, sehir_id=sehir.id)
        assert rapor["google_coklu_kaynak_sube"] == 1
        assert rapor["fiziksel_sube_supheli"] == 0
    finally:
        islem.rollback()
        baglanti.close()
