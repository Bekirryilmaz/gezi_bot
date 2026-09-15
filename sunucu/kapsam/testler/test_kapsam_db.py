from __future__ import annotations

import uuid

import pytest
from geoalchemy2.elements import WKTElement
from sqlalchemy.orm import Session

from sunucu.kapsam.servis import ilce_detayi_getir, sehir_kapsami_getir, yer_detayi_getir
from sunucu.veritabani.arama_modelleri import Ilce
from sunucu.veritabani.baglanti import motor
from sunucu.veritabani.kimlik_modelleri import Sube, YerKimligi
from sunucu.veritabani.modeller import Sehir, Yer
from sunucu.veritabani.yayin_modelleri import YayinKaydi


@pytest.fixture()
def oturum():
    baglanti = motor.connect(); islem = baglanti.begin(); session = Session(bind=baglanti)
    try:
        yield session
    finally:
        session.close(); islem.rollback(); baglanti.close()


def _sehir_ilce(oturum: Session, ek: str):
    sehir = Sehir(isim=f"Kapsam Sehri {ek}", aktif_mi=True); oturum.add(sehir); oturum.flush()
    ilce = Ilce(sehir_id=sehir.id, isim=f"Kapsam Ilcesi {ek}"); oturum.add(ilce); oturum.flush()
    return sehir, ilce


def test_sehir_manifesti_kayit_ve_claim_yokken_sahte_kapsam_uretmez(oturum: Session):
    sehir, _ = _sehir_ilce(oturum, uuid.uuid4().hex[:8])
    cevap = sehir_kapsami_getir(oturum, sehir.isim)
    assert cevap.yayinlanmis_yer_sayisi == 0
    assert cevap.desteklenen_iddia_aileleri == []
    assert cevap.ilceler == []
    assert cevap.karar_kapsami_destekleniyor is False


def test_yanlis_sehir_ilce_baglantisi_ve_bos_seo_sayfasi_reddedilir(oturum: Session):
    sehir1, ilce1 = _sehir_ilce(oturum, uuid.uuid4().hex[:8])
    sehir2, _ = _sehir_ilce(oturum, uuid.uuid4().hex[:8])
    with pytest.raises(LookupError, match="canonical"):
        ilce_detayi_getir(oturum, sehir2.isim, str(ilce1.id))
    detay = ilce_detayi_getir(oturum, sehir1.isim, str(ilce1.id))
    assert detay.ayri_sayfa_var is False
    assert str(ilce1.id) in detay.kesfet_url


def test_public_detail_yalniz_allow_list_ve_durust_unknown_tasir(oturum: Session):
    sehir, ilce = _sehir_ilce(oturum, uuid.uuid4().hex[:8])
    yer = Yer(sehir_id=sehir.id, ilce_id=ilce.id, ilce=ilce.isim, isim="Claimsiz Yer", ana_kategori="gezilecek_yer", alt_kategori="doga_manzara", konum=WKTElement("POINT(36.3 41.3)", srid=4326), ozellikler={}, aktiviteler=[], fotograf_urlleri=[])
    oturum.add(yer); oturum.flush()
    kimlik = YerKimligi(sehir_id=sehir.id, durum="aktif"); oturum.add(kimlik); oturum.flush()
    sube = Sube(yer_kimligi_id=kimlik.id, legacy_yer_id=yer.id, guncel_isim=yer.isim, durum="aktif"); oturum.add(sube); oturum.flush()
    oturum.add(YayinKaydi(nesne_turu="yer", nesne_id=yer.id, durum="yayinlanabilir", aktif_mi=True, izinli_kullanimlar=["detay"], neden_kodlari=[], surum=1)); oturum.flush()
    payload = yer_detayi_getir(oturum, str(yer.id)).model_dump()
    assert payload["pratik_bilgiler"] == []
    assert payload["kritik_bilinmeyenler"]
    metin = str(payload)
    for yasak in ("yorum_metni", "duygu_skoru", "guven_sinifi", "sponsor", "internal_score"):
        assert yasak not in metin
