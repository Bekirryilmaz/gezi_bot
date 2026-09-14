import uuid

from sqlalchemy.orm import Session

from sunucu.veritabani.baglanti import motor
from sunucu.veritabani.modeller import Yer
from sunucu.veritabani.sorgular import sehir_yerlerini_getir, yer_ve_koordinat_getir
from sunucu.veritabani.yayin_modelleri import GecersizlestirmeOlayi, PublicProjection, YayinKaydi
from sunucu.yayin.servis import gecersizlestirme_olayi_uret, olayi_isle


def test_public_sorgu_raw_yer_varligini_yayin_saymiyor_ve_rota_da_ayni_kapiyi_kullaniyor():
    baglanti = motor.connect(); islem = baglanti.begin(); oturum = Session(bind=baglanti)
    try:
        yer = oturum.query(Yer).first(); assert yer is not None
        yayin = oturum.query(YayinKaydi).filter_by(nesne_turu="yer", nesne_id=yer.id).one()
        yayin.durum = "yayinlanamaz"; yayin.neden_kodlari = ["test_withdrawn"]; oturum.flush()
        assert yer_ve_koordinat_getir(oturum, yer.id) is None
        assert all(aday.id != yer.id for aday, _, _ in sehir_yerlerini_getir(oturum, yer.sehir_id))
    finally:
        oturum.close(); islem.rollback(); baglanti.close()


def test_invalidation_event_idempotent_ve_cache_projection_gecersiz():
    baglanti = motor.connect(); islem = baglanti.begin(); oturum = Session(bind=baglanti)
    try:
        nesne_id = str(uuid.uuid4())
        projection = PublicProjection(nesne_turu="claim", nesne_id=nesne_id, yayin_surumu=1, etag="test", payload={"olumlu": True})
        oturum.add(projection); oturum.flush()
        olay1 = gecersizlestirme_olayi_uret(oturum, olay_anahtari=f"test:{nesne_id}", kaynak_turu="claim", kaynak_id=nesne_id, olay_turu="test")
        olay2 = gecersizlestirme_olayi_uret(oturum, olay_anahtari=f"test:{nesne_id}", kaynak_turu="claim", kaynak_id=nesne_id, olay_turu="test")
        assert olay1.id == olay2.id
        olayi_isle(oturum, olay1); olayi_isle(oturum, olay1)
        assert projection.gecersiz_mi is True
        assert olay1.deneme_sayisi == 1
        assert oturum.query(GecersizlestirmeOlayi).filter_by(olay_anahtari=f"test:{nesne_id}").count() == 1
    finally:
        oturum.close(); islem.rollback(); baglanti.close()
