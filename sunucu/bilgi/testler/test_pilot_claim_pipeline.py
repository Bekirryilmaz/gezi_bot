from __future__ import annotations

import uuid
from datetime import UTC, datetime, timedelta
from pathlib import Path

from sqlalchemy.orm import Session
from sunucu.admin.workflow import _komutu_uygula
from sunucu.auth.servis import admin_olustur
from sunucu.bilgi.pilot_claimleri import (
    adaylari_yaz,
    kaynak_boolean_normalize,
    kaynak_hakki_uygun_mu,
    kaynak_haklari_uygun_mu,
    osm_politikasini_uygula,
    satirdan_adaylar,
)
from sunucu.bilgi.public import yer_pratik_bilgileri
from sunucu.veritabani.admin_modelleri import IncelemeDosyasi
from sunucu.veritabani.baglanti import motor
from sunucu.veritabani.bilgi_modelleri import Iddia, IddiaSurumu, KanitBaglantisi, KaynakPolitikasi
from sunucu.veritabani.kimlik_modelleri import Sube, YerKimligi
from sunucu.veritabani.modeller import Sehir, Yer, YerKaynak
from sunucu.veritabani.yayin_modelleri import YayinKaydi


def _satir(kaynak_id: str, *, wifi: bool = True) -> dict:
    return {
        "kaynak": "openstreetmap",
        "kaynak_id": kaynak_id,
        "kaynak_url": f"https://www.openstreetmap.org/{kaynak_id}",
        "cekilme_zamani": "2026-08-03T13:05:45+00:00",
        "isim": "Pipeline test yeri",
        "ana_kategori": "yeme_icme",
        "alt_kategori": "kafe",
        "sehir": "Samsun",
        "ilce": "Atakum",
        "adres": "Test Sokak 1",
        "telefon": None,
        "web_sitesi": None,
        "ozellikler": {"wifi": wifi, "engelli_erisimi": None, "ucretsiz": None},
    }


def _oturum():
    baglanti = motor.connect()
    islem = baglanti.begin()
    return baglanti, islem, Session(bind=baglanti)


def _gecici_kaynak_bagi(oturum: Session) -> tuple[Yer, Sube, str]:
    ek = uuid.uuid4().hex
    sehir = Sehir(isim=f"Pilot Claim Sehri {ek}")
    oturum.add(sehir)
    oturum.flush()
    yer = Yer(
        sehir_id=sehir.id,
        isim=f"Pipeline test yeri {ek}",
        ana_kategori="yeme_icme",
        alt_kategori="kafe",
        ilce="Atakum",
        adres="Test Sokak 1",
        konum="SRID=4326;POINT(36.33 41.28)",
    )
    kimlik = YerKimligi(sehir_id=sehir.id)
    oturum.add_all([yer, kimlik])
    oturum.flush()
    sube = Sube(yer_kimligi_id=kimlik.id, legacy_yer_id=yer.id, guncel_isim=yer.isim)
    oturum.add(sube)
    oturum.flush()
    kaynak_id = f"node/{uuid.uuid4().int}"
    oturum.add(
        YerKaynak(
            yer_id=yer.id,
            kaynak="openstreetmap",
            kaynak_id=kaynak_id,
            kaynak_url=f"https://www.openstreetmap.org/{kaynak_id}",
            sube_id=sube.id,
        )
    )
    oturum.flush()
    return yer, sube, kaynak_id


def test_yapilandirilmis_kayit_dogru_candidate_uretir_ve_nlp_degil():
    adaylar = satirdan_adaylar(_satir("node/1"))
    aileler = {aday.aile for aday in adaylar}
    assert {"yer_turu", "amac_destegi", "adres", "wifi"} <= aileler
    assert all(aday.icerik_ozeti["kaynak_alani"] for aday in adaylar)
    assert all("yorum" not in aday.kaynak_alani for aday in adaylar)


def test_boolean_kaynak_degerleri_explicit_normalize_edilir():
    assert kaynak_boolean_normalize("no", aile="wifi") is False
    assert kaynak_boolean_normalize("false", aile="wifi") is False
    assert kaynak_boolean_normalize("yes", aile="wifi") is True
    assert kaynak_boolean_normalize("true", aile="wifi") is True
    assert kaynak_boolean_normalize("wlan", aile="wifi") is True
    assert kaynak_boolean_normalize("customers", aile="wifi") is None
    assert kaynak_boolean_normalize("limited", aile="tekerlekli_sandalye_erisimi") is None


def test_genisletilmis_amac_aileleri_yalniz_candidate_uretir():
    from sunucu.bilgi.pilot_claimleri import satirdan_adaylar

    taban = {
        "kaynak_id": "node/1",
        "kaynak": "openstreetmap",
        "sehir": "Samsun",
        "ilce": "Atakum",
        "ana_kategori": "yeme_icme",
        "alt_kategori": "tatli_pastane",
        "isim": "Test",
        "enlem": 41.0,
        "boylam": 36.0,
        "cekilme_zamani": "2026-09-15T00:00:00+00:00",
        "ozellikler": {},
    }
    adaylar = satirdan_adaylar(taban)
    amac = next(a for a in adaylar if a.aile == "amac_destegi")
    assert amac.deger == ["tatli_yemek"]


def test_unknown_boolean_ve_gecersiz_iletisim_candidate_uretmez():
    satir = _satir("node/invalid")
    satir["ozellikler"]["wifi"] = "customers"
    satir["telefon"] = "telefon yok"
    satir["web_sitesi"] = "www.ornek.com"
    aileler = {aday.aile for aday in satirdan_adaylar(satir)}
    assert "wifi" not in aileler
    assert "telefon" not in aileler
    assert "web_sitesi" not in aileler


def test_hak_kapisi_kullanim_amacina_gore_ayrilir():
    from types import SimpleNamespace

    from sunucu.bilgi import pilot_claimleri

    google_politikasi = SimpleNamespace(
        kamusal_gosterim="yasak",
        turev_iddia="yasak",
        ai_isleme="izinli",
        uzun_sureli_saklama="bilinmiyor",
        gecerli_baslangic=None,
        gecerli_bitis=None,
    )

    assert pilot_claimleri.kaynak_hakki_uygun_mu(
        google_politikasi, amac="ai_isleme"
    ) == (True, None)
    assert (
        pilot_claimleri.kaynak_hakki_uygun_mu(
            google_politikasi, amac="kamusal_gosterim"
        )[0]
        is False
    )
    assert (
        pilot_claimleri.kaynak_hakki_uygun_mu(
            google_politikasi, amac="turev_iddia"
        )[0]
        is False
    )


def test_google_dahili_nlp_politikasi_public_ve_turev_kapisini_acmaz():
    baglanti, islem, oturum = _oturum()
    try:
        from sunucu.bilgi.pilot_claimleri import google_dahili_nlp_politikasini_uygula

        politika = google_dahili_nlp_politikasini_uygula(oturum)
        assert politika.kaynak == "google_maps"
        assert politika.ai_isleme == "izinli"
        assert politika.kamusal_gosterim != "izinli"
        assert politika.turev_iddia != "izinli"
        assert kaynak_hakki_uygun_mu(politika, amac="ai_isleme") == (True, None)
        assert kaynak_haklari_uygun_mu(politika)[0] is False
    finally:
        islem.rollback()
        baglanti.close()


def test_osm_public_pipeline_tum_gerekli_haklari_korumaya_devam_eder():
    from types import SimpleNamespace

    osm_politikasi = SimpleNamespace(
        kamusal_gosterim="izinli",
        turev_iddia="izinli",
        ai_isleme="izinli",
        uzun_sureli_saklama="izinli",
        gecerli_baslangic=None,
        gecerli_bitis=None,
    )

    assert kaynak_haklari_uygun_mu(osm_politikasi) == (True, None)


def test_bilinmeyen_db_hak_degeri_crash_yerine_fail_closed_doner():
    from types import SimpleNamespace

    politika = SimpleNamespace(
        kamusal_gosterim="beklenmeyen_deger",
        turev_iddia="izinli",
        ai_isleme="izinli",
        uzun_sureli_saklama="izinli",
        gecerli_baslangic=None,
        gecerli_bitis=None,
    )
    uygun, neden = kaynak_hakki_uygun_mu(politika, amac="kamusal_gosterim")
    assert uygun is False
    assert neden == "kaynak_politikasi_hak_degeri_gecersiz"


def test_public_osm_gate_tek_eksik_hakta_kapanir():
    from types import SimpleNamespace

    for eksik_alan in (
        "kamusal_gosterim",
        "turev_iddia",
        "ai_isleme",
        "uzun_sureli_saklama",
    ):
        alanlar = {
            "kamusal_gosterim": "izinli",
            "turev_iddia": "izinli",
            "ai_isleme": "izinli",
            "uzun_sureli_saklama": "izinli",
        }
        alanlar[eksik_alan] = "bilinmiyor"
        politika = SimpleNamespace(
            **alanlar,
            gecerli_baslangic=None,
            gecerli_bitis=None,
        )
        uygun, neden = kaynak_haklari_uygun_mu(politika)
        assert uygun is False, eksik_alan
        assert neden == "display_derivative_processing_retention_hakki_yetersiz"


def test_unknown_ve_geri_cekilmis_hak_candidate_yazmaz():
    baglanti, islem, oturum = _oturum()
    try:
        _, _, kaynak_id = _gecici_kaynak_bagi(oturum)
        politika = oturum.query(KaynakPolitikasi).filter_by(kaynak="openstreetmap").first()
        if politika is None:
            politika = KaynakPolitikasi(kaynak="openstreetmap")
            oturum.add(politika)
        politika.kamusal_gosterim = politika.turev_iddia = politika.ai_isleme = (
            politika.uzun_sureli_saklama
        ) = "bilinmiyor"
        oturum.flush()
        ozet = adaylari_yaz(
            oturum, dosya=Path("test.jsonl"), satirlar=[_satir(kaynak_id)], dry_run=False
        )
        assert ozet.hak_nedeniyle_engellenen == 4
        politika.kamusal_gosterim = politika.turev_iddia = politika.ai_isleme = (
            politika.uzun_sureli_saklama
        ) = "izinli"
        politika.gecerli_bitis = datetime.now(UTC) - timedelta(seconds=1)
        oturum.flush()
        uygun, neden = kaynak_haklari_uygun_mu(politika)
        assert not uygun and "geri_cekilmis" in str(neden)
        ozet = adaylari_yaz(
            oturum, dosya=Path("test.jsonl"), satirlar=[_satir(kaynak_id)], dry_run=False
        )
        assert ozet.geri_cekilmis_kaynak_engeli == 4
    finally:
        oturum.close()
        islem.rollback()
        baglanti.close()


def test_idempotent_rerun_duplicate_uretmez_ve_yanlis_sube_baglanmaz():
    baglanti, islem, oturum = _oturum()
    try:
        osm_politikasini_uygula(oturum)
        _, sube, kaynak_id = _gecici_kaynak_bagi(oturum)
        ilk = adaylari_yaz(
            oturum, dosya=Path("test.jsonl"), satirlar=[_satir(kaynak_id)], dry_run=False
        )
        ikinci = adaylari_yaz(
            oturum, dosya=Path("test.jsonl"), satirlar=[_satir(kaynak_id)], dry_run=False
        )
        assert ilk.yeni_claim == 4 and ilk.yeni_inceleme == 4
        assert ikinci.yeni_claim == 0 and ikinci.yeni_surum == 0 and ikinci.ayni_aday == 4
        assert {
            str(i.sube_id) for i in oturum.query(Iddia).filter(Iddia.sube_id == sube.id).all()
        } == {str(sube.id)}
        once = oturum.query(Iddia).count()
        yanlis = adaylari_yaz(
            oturum,
            dosya=Path("test.jsonl"),
            satirlar=[_satir(f"node/{uuid.uuid4().int}")],
            dry_run=False,
        )
        assert yanlis.eslesmeyen_sube == 1 and oturum.query(Iddia).count() == once
    finally:
        oturum.close()
        islem.rollback()
        baglanti.close()


def test_deger_degisiminde_supporting_ve_counter_evidence_ile_conflict():
    baglanti, islem, oturum = _oturum()
    try:
        osm_politikasini_uygula(oturum)
        _, sube, kaynak_id = _gecici_kaynak_bagi(oturum)
        adaylari_yaz(
            oturum, dosya=Path("test.jsonl"), satirlar=[_satir(kaynak_id, wifi=True)], dry_run=False
        )
        adaylari_yaz(
            oturum,
            dosya=Path("test-2.jsonl"),
            satirlar=[_satir(kaynak_id, wifi=False)],
            dry_run=False,
        )
        iddia = oturum.query(Iddia).filter_by(sube_id=sube.id, aile="wifi").one()
        surum = oturum.query(IddiaSurumu).filter_by(iddia_id=iddia.id, surum_no=2).one()
        assert surum.bilgi_durumu == "celiskili"
        assert {
            rol
            for (rol,) in oturum.query(KanitBaglantisi.rol)
            .filter_by(iddia_surumu_id=surum.id)
            .all()
        } == {"supporting", "counter"}
    finally:
        oturum.close()
        islem.rollback()
        baglanti.close()


def test_admin_approve_publication_reject_ve_public_dto_raw_evidence_sizdirmaz():
    baglanti, islem, oturum = _oturum()
    try:
        osm_politikasini_uygula(oturum)
        yer, sube, kaynak_id = _gecici_kaynak_bagi(oturum)
        adaylari_yaz(oturum, dosya=Path("test.jsonl"), satirlar=[_satir(kaynak_id)], dry_run=False)
        admin = admin_olustur(
            oturum,
            eposta=f"pilot-{uuid.uuid4().hex}@test.local",
            gorunen_ad="Pilot",
            parola="guvenli-test-parolasi",
            roller={"yonetici"},
        )
        wifi = oturum.query(Iddia).filter_by(sube_id=sube.id, aile="wifi").one()
        komut = IncelemeDosyasi(
            dosya_turu="claim",
            nesne_turu="claim",
            nesne_id=wifi.id,
            durum="isleniyor",
            risk_sinifi="normal",
            onerilen_eylem="claim_approve",
            komut_payload={},
            acan_aktor_id=admin.id,
        )
        oturum.add(komut)
        oturum.flush()
        _komutu_uygula(
            oturum,
            komut,
            admin.id,
            "Yapilandirilmis kanit ve kapsam kontrol edildi",
            f"approve-{uuid.uuid4()}",
        )
        yayin = oturum.query(YayinKaydi).filter_by(nesne_turu="claim", nesne_id=wifi.id).one()
        assert yayin.durum == "yayinlanabilir"
        dto = yer_pratik_bilgileri(oturum, str(yer.id))
        wifi_dto = next(x for x in dto if x["aile"] == "wifi")
        assert wifi_dto["deger"] is True
        assert "icerik_ozeti" not in wifi_dto and "gozlem_id" not in wifi_dto

        adres = oturum.query(Iddia).filter_by(sube_id=sube.id, aile="adres").one()
        red = IncelemeDosyasi(
            dosya_turu="claim",
            nesne_turu="claim",
            nesne_id=adres.id,
            durum="isleniyor",
            risk_sinifi="normal",
            onerilen_eylem="claim_reject",
            komut_payload={},
            acan_aktor_id=admin.id,
        )
        oturum.add(red)
        oturum.flush()
        _komutu_uygula(
            oturum,
            red,
            admin.id,
            "Adres kapsami insan kontrolunde reddedildi",
            f"reject-{uuid.uuid4()}",
        )
        assert (
            oturum.query(YayinKaydi).filter_by(nesne_turu="claim", nesne_id=adres.id).one().durum
            == "yayinlanamaz"
        )
        assert all(x["aile"] != "adres" for x in yer_pratik_bilgileri(oturum, str(yer.id)))
    finally:
        oturum.close()
        islem.rollback()
        baglanti.close()
