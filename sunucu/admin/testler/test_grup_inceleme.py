from __future__ import annotations

import uuid
from pathlib import Path

import pytest
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sunucu.admin.grup_inceleme import grup_incelemeyi_uygula
from sunucu.auth.rbac import yetkileri_birlestir
from sunucu.auth.servis import AdminBaglami, admin_olustur, oturum_ac
from sunucu.bilgi.pilot_claimleri import adaylari_yaz, osm_politikasini_uygula
from sunucu.veritabani.admin_modelleri import AdminAuditOlayi, IncelemeDosyasi
from sunucu.veritabani.baglanti import motor
from sunucu.veritabani.bilgi_modelleri import Iddia, IddiaSurumu
from sunucu.veritabani.kimlik_modelleri import Sube, YerKimligi
from sunucu.veritabani.modeller import Sehir, Yer, YerKaynak
from sunucu.veritabani.yayin_modelleri import YayinKaydi


def _oturum():
    baglanti = motor.connect()
    islem = baglanti.begin()
    return baglanti, islem, Session(bind=baglanti)


def _satir(kaynak_id: str, **ozellik) -> dict:
    temel = {"wifi": True, "engelli_erisimi": None, "ucretsiz": None}
    temel.update(ozellik)
    return {
        "kaynak": "openstreetmap",
        "kaynak_id": kaynak_id,
        "kaynak_url": f"https://www.openstreetmap.org/{kaynak_id}",
        "cekilme_zamani": "2026-08-03T13:05:45+00:00",
        "isim": "Grup test yeri",
        "ana_kategori": "yeme_icme",
        "alt_kategori": "kafe",
        "sehir": "Samsun",
        "ilce": "Atakum",
        "adres": "Test Sokak 1",
        "telefon": None,
        "web_sitesi": None,
        "ozellikler": temel,
    }


def _kaynak_bagi(oturum: Session) -> tuple[Yer, Sube, str]:
    ek = uuid.uuid4().hex
    sehir = Sehir(isim=f"Grup Sehir {ek}")
    oturum.add(sehir)
    oturum.flush()
    yer = Yer(
        sehir_id=sehir.id,
        isim=f"Grup test yeri {ek}",
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
    return yer, sube, kaynak_id


def _baglam(oturum: Session, *, roller: set[str]):
    admin = admin_olustur(
        oturum,
        eposta=f"grup-{uuid.uuid4().hex}@test.local",
        gorunen_ad="Grup",
        parola="cok-guvenli-test-parolasi",
        roller=roller,
    )
    kayit, _token, _csrf = oturum_ac(oturum, admin, ip=None, user_agent=None)
    return AdminBaglami(admin, kayit, frozenset(roller), yetkileri_birlestir(roller))


def _aday_dosyasi(oturum: Session, iddia_id: str) -> IncelemeDosyasi:
    return (
        oturum.query(IncelemeDosyasi)
        .filter_by(dosya_turu="claim_candidate", nesne_id=iddia_id)
        .one()
    )


def test_grup_inceleme_dusuk_risk_yayinlar_kor_otomatik_yayin_yoktur():
    baglanti, islem, oturum = _oturum()
    try:
        osm_politikasini_uygula(oturum)
        _yer, sube, kaynak_id = _kaynak_bagi(oturum)
        adaylari_yaz(oturum, dosya=Path("grup.jsonl"), satirlar=[_satir(kaynak_id)], dry_run=False)
        wifi = oturum.query(Iddia).filter_by(sube_id=sube.id, aile="wifi").one()
        dosya = _aday_dosyasi(oturum, wifi.id)
        baglam = _baglam(oturum, roller={"yonetici"})
        with pytest.raises(HTTPException) as bos:
            grup_incelemeyi_uygula(
                oturum,
                baglam=baglam,
                dosya_idleri=[dosya.id],
                gerekce="kisa",
                istek_id="grup-1",
            )
        assert bos.value.status_code == 422
        sonuc = grup_incelemeyi_uygula(
            oturum,
            baglam=baglam,
            dosya_idleri=[dosya.id],
            gerekce="OSM wifi etiketi sozdizimi ve kanit kontrol edildi",
            istek_id="grup-2",
        )
        assert sonuc.otomatik_yayin is False
        assert dosya.id in sonuc.onaylanan
        yayin = oturum.query(YayinKaydi).filter_by(nesne_turu="claim", nesne_id=wifi.id).one()
        assert yayin.durum == "yayinlanabilir"
        assert (
            oturum.query(AdminAuditOlayi)
            .filter_by(eylem="grup_inceleme", istek_id="grup-2")
            .count()
            == 1
        )
    finally:
        oturum.close()
        islem.rollback()
        baglanti.close()


def test_grup_inceleme_kritik_ve_amac_ve_karisik_aile_reddedilir():
    baglanti, islem, oturum = _oturum()
    try:
        osm_politikasini_uygula(oturum)
        _yer, sube, kaynak_id = _kaynak_bagi(oturum)
        adaylari_yaz(
            oturum,
            dosya=Path("grup-kritik.jsonl"),
            satirlar=[_satir(kaynak_id, engelli_erisimi=True)],
            dry_run=False,
        )
        baglam = _baglam(oturum, roller={"yonetici"})
        tekerlek = (
            oturum.query(Iddia).filter_by(sube_id=sube.id, aile="tekerlekli_sandalye_erisimi").one()
        )
        wifi = oturum.query(Iddia).filter_by(sube_id=sube.id, aile="wifi").one()
        amac = oturum.query(Iddia).filter_by(sube_id=sube.id, aile="amac_destegi").one()
        teker_dosya = _aday_dosyasi(oturum, tekerlek.id)
        sonuc = grup_incelemeyi_uygula(
            oturum,
            baglam=baglam,
            dosya_idleri=[teker_dosya.id],
            gerekce="Tekerlekli sandalye grup testi gerekcesi",
            istek_id="grup-3",
        )
        assert sonuc.onaylanan == []
        assert any(a["neden"] == "kritik_aile_grup_yayini_yasak" for a in sonuc.atlanan)
        with pytest.raises(HTTPException) as karisik:
            grup_incelemeyi_uygula(
                oturum,
                baglam=baglam,
                dosya_idleri=[_aday_dosyasi(oturum, wifi.id).id, _aday_dosyasi(oturum, amac.id).id],
                gerekce="Karisik aile grup testi gerekcesi",
                istek_id="grup-4",
            )
        assert karisik.value.status_code == 422
    finally:
        oturum.close()
        islem.rollback()
        baglanti.close()


def test_grup_inceleme_gecersiz_saati_yayinlamaz_gozlemci_yayinlayamaz():
    baglanti, islem, oturum = _oturum()
    try:
        osm_politikasini_uygula(oturum)
        _yer, sube, kaynak_id = _kaynak_bagi(oturum)
        adaylari_yaz(
            oturum,
            dosya=Path("grup-saat.jsonl"),
            satirlar=[_satir(kaynak_id, opening_hours="Mo-Su 18:00-02:00")],
            dry_run=False,
        )
        saat = oturum.query(Iddia).filter_by(sube_id=sube.id, aile="calisma_saatleri").one()
        dosya = _aday_dosyasi(oturum, saat.id)
        yonetici = _baglam(oturum, roller={"yonetici"})
        sonuc = grup_incelemeyi_uygula(
            oturum,
            baglam=yonetici,
            dosya_idleri=[dosya.id],
            gerekce="Gecersiz OSM saati yayinlanmamali",
            istek_id="grup-5",
        )
        assert sonuc.onaylanan == []
        assert (
            oturum.query(YayinKaydi).filter_by(nesne_turu="claim", nesne_id=saat.id).first() is None
        )
        gozlemci = _baglam(oturum, roller={"gozlemci"})
        with pytest.raises(HTTPException) as yetki:
            grup_incelemeyi_uygula(
                oturum,
                baglam=gozlemci,
                dosya_idleri=[dosya.id],
                gerekce="Yetkisiz grup yayini denenmemeli",
                istek_id="grup-6",
            )
        assert yetki.value.status_code == 403
    finally:
        oturum.close()
        islem.rollback()
        baglanti.close()


def test_grup_inceleme_gecerli_saati_normalize_yazar_kor_yayin_yoktur():
    baglanti, islem, oturum = _oturum()
    try:
        osm_politikasini_uygula(oturum)
        _yer, sube, kaynak_id = _kaynak_bagi(oturum)
        adaylari_yaz(
            oturum,
            dosya=Path("grup-saat-gecerli.jsonl"),
            satirlar=[_satir(kaynak_id, opening_hours="Mo-Fr 09:00-18:00; Sa-Su 10:00-16:00")],
            dry_run=False,
        )
        saat = oturum.query(Iddia).filter_by(sube_id=sube.id, aile="calisma_saatleri").one()
        dosya = _aday_dosyasi(oturum, saat.id)
        baglam = _baglam(oturum, roller={"yonetici"})
        sonuc = grup_incelemeyi_uygula(
            oturum,
            baglam=baglam,
            dosya_idleri=[dosya.id],
            gerekce="Gecerli OSM saati sozdizimi kontrol edildi",
            istek_id="grup-7",
        )
        assert sonuc.otomatik_yayin is False
        assert dosya.id in sonuc.onaylanan
        surum = (
            oturum.query(IddiaSurumu)
            .filter_by(iddia_id=saat.id, surum_no=saat.aktif_surum_no)
            .one()
        )
        assert surum.yayin_durumu == "yayinlandi"
        assert surum.deger.get("sozdizimi_gecerli") is True
        assert surum.deger.get("zaman_kapsami") == "haftalik"
        assert "Mo-Fr 09:00-18:00" in (surum.deger.get("normalize") or "")
    finally:
        oturum.close()
        islem.rollback()
        baglanti.close()


def test_grup_inceleme_birinci_el_saati_site_ici_kaynakla_yazar():
    from sunucu.admin.gozlem_servisi import birinci_el_gozlem_yaz, site_ici_politikasini_uygula

    baglanti, islem, oturum = _oturum()
    try:
        site_ici_politikasini_uygula(oturum)
        _yer, sube, _kaynak_id = _kaynak_bagi(oturum)
        baglam = _baglam(oturum, roller={"yonetici"})
        yazilan = birinci_el_gozlem_yaz(
            oturum,
            baglam=baglam,
            sube_id=sube.id,
            aile="calisma_saatleri",
            deger="Mo-Su 08:30-16:30",
            ozet="Resmi kurum saati birinci el kayit.",
            gerekce="KTB sayfasindan birinci el saat kaydi.",
            istek_id="grup-8",
            kaynak_url="https://samsun.ktb.gov.tr/TR-216752/gazi-muzesi.html",
        )
        assert yazilan["otomatik_yayin"] is False
        sonuc = grup_incelemeyi_uygula(
            oturum,
            baglam=baglam,
            dosya_idleri=[yazilan["inceleme_dosyasi_id"]],
            gerekce="Birinci el resmi saat sozdizimi kontrol edildi",
            istek_id="grup-9",
        )
        assert yazilan["inceleme_dosyasi_id"] in sonuc.onaylanan
        assert sonuc.otomatik_yayin is False
        iddia = oturum.get(Iddia, yazilan["iddia_id"])
        surum = (
            oturum.query(IddiaSurumu)
            .filter_by(iddia_id=iddia.id, surum_no=iddia.aktif_surum_no)
            .one()
        )
        assert surum.yayin_durumu == "yayinlandi"
        assert surum.deger.get("kaynak") == "site_ici"
        assert surum.deger.get("durum") == "known"
        assert (surum.deger.get("ham_referans") or "").endswith("gazi-muzesi.html")
    finally:
        oturum.close()
        islem.rollback()
        baglanti.close()
