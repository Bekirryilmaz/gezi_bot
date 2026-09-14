from sqlalchemy.orm import Session

from sunucu.kimlik.servis import aday_kaydet, alias_coz, birlestir, bol
from sunucu.veritabani.baglanti import motor
from sunucu.veritabani.kimlik_modelleri import Sube
from sunucu.veritabani.modeller import YerKaynak


def test_canonical_kimlik_merge_split_alias_ve_isim_degisimi():
    baglanti = motor.connect()
    islem = baglanti.begin()
    oturum = Session(bind=baglanti)
    try:
        kaynaklar = oturum.query(YerKaynak).filter(YerKaynak.sube_id.is_not(None)).limit(2).all()
        assert len(kaynaklar) == 2
        sol, sag = (oturum.get(Sube, kaynak.sube_id) for kaynak in kaynaklar)
        eski_id = sol.yer_kimligi_id
        sol.guncel_isim = "Yeni Isim"
        oturum.flush()
        assert sol.yer_kimligi_id == eski_id
        assert alias_coz(oturum, "legacy_yer_id", str(sol.legacy_yer_id)).yer_kimligi_id == eski_id

        aday = aday_kaydet(oturum, sol.id, sag.id, 0.75, {"risk": "regression"})
        kayit = birlestir(oturum, aday, sol.id, "test", manuel_override=True)
        assert oturum.get(Sube, sag.id).yonlendirilen_sube_id == sol.id
        bol(oturum, kayit, "yanlis sube")
        assert oturum.get(Sube, sag.id).yonlendirilen_sube_id is None
    finally:
        oturum.close()
        islem.rollback()
        baglanti.close()

