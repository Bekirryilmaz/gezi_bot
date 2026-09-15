from __future__ import annotations

import uuid

import pytest
from geoalchemy2.elements import WKTElement
from sqlalchemy.orm import Session

from sunucu.karar_motoru.semalar import CografiBaglamSemasi, KararBaglamiSemasi
from sunucu.kesfet.semalar import KesfetDegerlendirmeTalebi
from sunucu.kesfet.servis import kesfet_degerlendir
from sunucu.veritabani.arama_modelleri import Ilce
from sunucu.veritabani.baglanti import motor
from sunucu.veritabani.bilgi_modelleri import Iddia, IddiaSurumu
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


def _yer_ekle(oturum: Session, sehir: Sehir, ilce: Ilce, isim: str, *, amac_var: bool, sponsorlu: bool = False):
    yer = Yer(
        sehir_id=sehir.id, ilce_id=ilce.id, ilce=ilce.isim, isim=isim,
        ana_kategori="yeme_icme", alt_kategori="kafe",
        konum=WKTElement("POINT(36.3 41.3)", srid=4326),
        ozellikler={"sponsorlu_mekan": sponsorlu}, aktiviteler=[], fotograf_urlleri=[],
    )
    oturum.add(yer); oturum.flush()
    kimlik = YerKimligi(sehir_id=sehir.id, durum="aktif"); oturum.add(kimlik); oturum.flush()
    sube = Sube(yer_kimligi_id=kimlik.id, legacy_yer_id=yer.id, guncel_isim=isim, durum="aktif"); oturum.add(sube); oturum.flush()
    yayin = YayinKaydi(nesne_turu="yer", nesne_id=yer.id, durum="yayinlanabilir", aktif_mi=True, izinli_kullanimlar=["arama", "kesfet", "karar", "detay"], neden_kodlari=[], surum=1)
    oturum.add(yayin); oturum.flush()
    if amac_var:
        iddia = Iddia(sube_id=sube.id, aile="amac_destegi", kapsam={}, aktif_surum_no=1); oturum.add(iddia); oturum.flush()
        oturum.add(IddiaSurumu(iddia_id=iddia.id, surum_no=1, deger={"deger": ["uzun_sohbet"]}, bilgi_durumu="biliniyor", guven_sinifi="saglam", yayin_durumu="yayinlandi"))
        oturum.add(YayinKaydi(nesne_turu="claim", nesne_id=iddia.id, durum="yayinlanabilir", aktif_mi=True, izinli_kullanimlar=["karar", "detay"], neden_kodlari=[], surum=1)); oturum.flush()
    return yer, yayin


def _talep(ad: str, sehir: Sehir, *, reddedilen: list[str] | None = None):
    return KesfetDegerlendirmeTalebi(sorgu=ad, baglam=KararBaglamiSemasi(amac="uzun_sohbet", cografi_baglam=CografiBaglamSemasi(sehir=sehir.isim), reddedilen_yerler=reddedilen or [], bilgi_surumu="test-1"))


def test_bes_destekli_aday_besle_sinirlanir_ve_ayni_baglam_deterministiktir(oturum: Session):
    sehir = oturum.query(Sehir).filter(Sehir.arama_isim == "samsun").one()
    ilce = oturum.query(Ilce).filter_by(sehir_id=sehir.id, arama_isim="atakum").one()
    ad = f"Kesfet Dalga {uuid.uuid4().hex[:8]}"
    yerler = [_yer_ekle(oturum, sehir, ilce, f"{ad} {sira}", amac_var=True)[0] for sira in range(6)]
    ilk = kesfet_degerlendir(oturum, _talep(ad, sehir), request_id="r1")
    ikinci = kesfet_degerlendir(oturum, _talep(ad, sehir), request_id="r2")
    assert ilk.durum == "success" and len(ilk.secenekler) == 5
    assert [x.yer.place_id for x in ilk.secenekler] == [x.yer.place_id for x in ikinci.secenekler]
    assert [x.karar_sonucu.karar_id for x in ilk.secenekler] == [x.karar_sonucu.karar_id for x in ikinci.secenekler]
    assert set(x.yer.place_id for x in ilk.secenekler).issubset({str(x.id) for x in yerler})


def test_iki_destekli_aday_varsa_yalniz_iki_ve_unknownlar_doldurmaz(oturum: Session):
    sehir = oturum.query(Sehir).filter(Sehir.arama_isim == "samsun").one()
    ilce = oturum.query(Ilce).filter_by(sehir_id=sehir.id, arama_isim="atakum").one()
    ad = f"Iki Aday {uuid.uuid4().hex[:8]}"
    [_yer_ekle(oturum, sehir, ilce, f"{ad} {sira}", amac_var=sira < 2) for sira in range(5)]
    cevap = kesfet_degerlendir(oturum, _talep(ad, sehir), request_id="iki")
    assert cevap.durum == "insufficient" and len(cevap.secenekler) == 2
    assert cevap.degerlendirilemeyen_aday_sayisi == 3


def test_ret_withdraw_ve_sponsor_sonucu_degistirmez(oturum: Session):
    sehir = oturum.query(Sehir).filter(Sehir.arama_isim == "samsun").one()
    ilce = oturum.query(Ilce).filter_by(sehir_id=sehir.id, arama_isim="atakum").one()
    ad = f"Ret Aday {uuid.uuid4().hex[:8]}"
    yer1, yayin1 = _yer_ekle(oturum, sehir, ilce, f"{ad} A", amac_var=True)
    yer2, _ = _yer_ekle(oturum, sehir, ilce, f"{ad} B", amac_var=True, sponsorlu=True)
    normal = kesfet_degerlendir(oturum, _talep(ad, sehir), request_id="normal")
    yer2.ozellikler = {"sponsorlu_mekan": False}; oturum.flush()
    sponsorsuz = kesfet_degerlendir(oturum, _talep(ad, sehir), request_id="sponsorsuz")
    assert [x.yer.place_id for x in normal.secenekler] == [x.yer.place_id for x in sponsorsuz.secenekler]
    ret = kesfet_degerlendir(oturum, _talep(ad, sehir, reddedilen=[str(yer1.id)]), request_id="ret")
    assert str(yer1.id) not in {x.yer.place_id for x in ret.secenekler}
    yayin1.durum = "yayinlanamaz"; yayin1.neden_kodlari = ["geri_cekilmis"]; oturum.flush()
    cekilmis = kesfet_degerlendir(oturum, _talep(ad, sehir), request_id="withdraw")
    assert str(yer1.id) not in {x.yer.place_id for x in cekilmis.secenekler}
    assert str(yer2.id) in {x.yer.place_id for x in cekilmis.secenekler}


def test_ilk_elli_unknown_amac_claimi_olan_gec_adayi_gizlemez(oturum: Session):
    sehir = oturum.query(Sehir).filter(Sehir.arama_isim == "samsun").one()
    ilce = oturum.query(Ilce).filter_by(sehir_id=sehir.id, arama_isim="atakum").one()
    ek = uuid.uuid4().hex[:8]
    for sira in range(51):
        _yer_ekle(oturum, sehir, ilce, f"A Aday {ek} {sira:02d}", amac_var=False)
    destekli, _ = _yer_ekle(oturum, sehir, ilce, f"Z Destekli {ek}", amac_var=True)
    cevap = kesfet_degerlendir(oturum, _talep(ek, sehir), request_id="ilk-elli")
    assert str(destekli.id) in {x.yer.place_id for x in cevap.secenekler}
