from __future__ import annotations

import uuid

import pytest
from geoalchemy2.elements import WKTElement
from sqlalchemy.orm import Session

from sunucu.arama.servis import ara, filtre_katalogunu_getir
from sunucu.karar_motoru.domain import KosulDurumu
from sunucu.veritabani.arama_modelleri import Ilce
from sunucu.veritabani.baglanti import motor
from sunucu.veritabani.bilgi_modelleri import Iddia, IddiaSurumu
from sunucu.veritabani.kimlik_modelleri import Sube, YerKimligi
from sunucu.veritabani.modeller import Sehir, Yer
from sunucu.veritabani.yayin_modelleri import YayinKaydi


def _yer_ekle(oturum: Session, sehir: Sehir, ilce: Ilce, isim: str, *, sponsorlu=False):
    yer = Yer(
        sehir_id=sehir.id, ilce_id=ilce.id, ilce=ilce.isim, isim=isim,
        ana_kategori="yeme_icme", alt_kategori="kafe",
        konum=WKTElement("POINT(36.3 41.3)", srid=4326),
        ozellikler={"sponsorlu_mekan": sponsorlu}, aktiviteler=[], fotograf_urlleri=[],
    )
    oturum.add(yer); oturum.flush()
    kimlik = YerKimligi(sehir_id=sehir.id, durum="aktif")
    oturum.add(kimlik); oturum.flush()
    sube = Sube(yer_kimligi_id=kimlik.id, legacy_yer_id=yer.id, guncel_isim=isim, durum="aktif")
    oturum.add(sube); oturum.flush()
    yayin = YayinKaydi(
        nesne_turu="yer", nesne_id=yer.id, durum="yayinlanabilir", aktif_mi=True,
        izinli_kullanimlar=["arama"], neden_kodlari=[], surum=1,
    )
    oturum.add(yayin); oturum.flush()
    return yer, sube, yayin


def _claim_ekle(oturum: Session, sube: Sube, aile: str, deger):
    iddia = Iddia(sube_id=sube.id, aile=aile, kapsam={}, aktif_surum_no=1)
    oturum.add(iddia); oturum.flush()
    oturum.add(IddiaSurumu(
        iddia_id=iddia.id, surum_no=1, deger=deger, bilgi_durumu="biliniyor",
        guven_sinifi="dogrulanmis", yayin_durumu="yayinlandi",
    ))
    oturum.add(YayinKaydi(
        nesne_turu="claim", nesne_id=iddia.id, durum="yayinlanabilir", aktif_mi=True,
        izinli_kullanimlar=["karar"], neden_kodlari=[], surum=1,
    ))
    oturum.flush()


@pytest.fixture()
def arama_oturumu():
    baglanti = motor.connect(); islem = baglanti.begin(); oturum = Session(bind=baglanti)
    try:
        yield oturum
    finally:
        oturum.close(); islem.rollback(); baglanti.close()


def test_exact_fuzzy_sube_ayrimi_publication_cursor_ve_sponsor(arama_oturumu: Session):
    sehir = arama_oturumu.query(Sehir).filter(Sehir.arama_isim == "samsun").one()
    atakum = arama_oturumu.query(Ilce).filter_by(sehir_id=sehir.id, arama_isim="atakum").one()
    bafra = arama_oturumu.query(Ilce).filter_by(sehir_id=sehir.id, arama_isim="bafra").one()
    ad = f"Kahve Dünyası Dalga {uuid.uuid4().hex[:8]}"
    yer1, sube1, yayin1 = _yer_ekle(arama_oturumu, sehir, atakum, ad)
    yer2, sube2, _ = _yer_ekle(arama_oturumu, sehir, bafra, ad, sponsorlu=True)

    tam = ara(arama_oturumu, q=ad.upper(), sehir_degeri="samsun", ilce_id=None, tur=None, zorunlu_kosullar=[], tercihler=[], limit=1, cursor=None)
    assert tam.sonuclar[0].eslesme_nedeni.value == "tam_ad"
    assert tam.sonuclar[0].yer is not None and tam.sonuclar[0].yer.branch_id
    assert tam.sonraki_cursor
    ikinci = ara(arama_oturumu, q=ad, sehir_degeri="samsun", ilce_id=None, tur=None, zorunlu_kosullar=[], tercihler=[], limit=1, cursor=tam.sonraki_cursor)
    assert {tam.sonuclar[0].yer.branch_id, ikinci.sonuclar[0].yer.branch_id} == {str(sube1.id), str(sube2.id)}

    prefix = ara(arama_oturumu, q=ad[:-3], sehir_degeri="samsun", ilce_id=None, tur=None, zorunlu_kosullar=[], tercihler=[], limit=10, cursor=None)
    assert any(x.eslesme_nedeni.value == "ad_baslangici" for x in prefix.sonuclar)

    yazim_hatasi = ad.replace("Dünyası", "Dünyas")
    fuzzy = ara(arama_oturumu, q=yazim_hatasi, sehir_degeri="samsun", ilce_id=None, tur=None, zorunlu_kosullar=[], tercihler=[], limit=10, cursor=None)
    assert any(x.eslesme_nedeni.value == "yazim_yakinligi" for x in fuzzy.sonuclar)

    once = [x.yer.branch_id for x in ara(arama_oturumu, q=ad, sehir_degeri="samsun", ilce_id=None, tur=None, zorunlu_kosullar=[], tercihler=[], limit=10, cursor=None).sonuclar]
    yer1.ozellikler = {"sponsorlu_mekan": True}; arama_oturumu.flush()
    sonra = [x.yer.branch_id for x in ara(arama_oturumu, q=ad, sehir_degeri="samsun", ilce_id=None, tur=None, zorunlu_kosullar=[], tercihler=[], limit=10, cursor=None).sonuclar]
    assert once == sonra

    yayin1.durum = "yayinlanamaz"; yayin1.neden_kodlari = ["geri_cekilmis"]; arama_oturumu.flush()
    cekilmis = ara(arama_oturumu, q=ad, sehir_degeri="samsun", ilce_id=None, tur=None, zorunlu_kosullar=[], tercihler=[], limit=10, cursor=None)
    assert all(x.yer is None or x.yer.place_id != str(yer1.id) for x in cekilmis.sonuclar)
    assert "benzerlik" not in cekilmis.model_dump_json() and "internal_score" not in cekilmis.model_dump_json()


def test_hard_unknown_preference_unknown_ve_filtre_katalogu(arama_oturumu: Session):
    sehir = arama_oturumu.query(Sehir).filter(Sehir.arama_isim == "samsun").one()
    atakum = arama_oturumu.query(Ilce).filter_by(sehir_id=sehir.id, arama_isim="atakum").one()
    ad = f"Kosul Test {uuid.uuid4().hex[:8]}"
    _, sube1, _ = _yer_ekle(arama_oturumu, sehir, atakum, ad)
    _, _, _ = _yer_ekle(arama_oturumu, sehir, atakum, ad)
    _claim_ekle(arama_oturumu, sube1, "otopark", {"var": True})

    hard = ara(arama_oturumu, q=ad, sehir_degeri="samsun", ilce_id=None, tur=None, zorunlu_kosullar=["otopark"], tercihler=[], limit=10, cursor=None)
    assert len(hard.sonuclar) == 1
    assert hard.degerlendirilemeyen_aday_sayisi == 1
    assert hard.sonuclar[0].kosul_durumlari["otopark"] is KosulDurumu.UYGUN
    assert hard.uygulanan_filtreler.sehir_id == str(sehir.id)

    tercih = ara(arama_oturumu, q=ad, sehir_degeri="samsun", ilce_id=None, tur=None, zorunlu_kosullar=[], tercihler=["otopark"], limit=10, cursor=None)
    assert tercih.sonuclar[0].kosul_durumlari["otopark"] is KosulDurumu.UYGUN
    assert tercih.sonuclar[1].kosul_durumlari["otopark"] is KosulDurumu.DEGERLENDIRILEMIYOR
    katalog = filtre_katalogunu_getir(arama_oturumu, "samsun")
    assert "otopark" in {x.kod for x in katalog.somut_kosullar}
    assert "sessiz_ortam" not in {x.kod for x in katalog.somut_kosullar}


def test_yanlis_sehir_ilce_bilesimi_reddedilir(arama_oturumu: Session):
    samsun = arama_oturumu.query(Sehir).filter(Sehir.arama_isim == "samsun").one()
    diger = Sehir(isim=f"Test Şehri {uuid.uuid4().hex[:6]}", aktif_mi=True)
    arama_oturumu.add(diger); arama_oturumu.flush()
    yabanci_ilce = Ilce(sehir_id=diger.id, isim="Atakum")
    arama_oturumu.add(yabanci_ilce); arama_oturumu.flush()
    with pytest.raises(ValueError, match="sehre ait degil"):
        ara(arama_oturumu, q="test", sehir_degeri=str(samsun.id), ilce_id=str(yabanci_ilce.id), tur=None, zorunlu_kosullar=[], tercihler=[], limit=10, cursor=None)


def test_sehir_ilce_kategori_sonuclari_anlam_olarak_ayridir(arama_oturumu: Session):
    sehir = ara(arama_oturumu, q="SAMSUN", sehir_degeri="samsun", ilce_id=None, tur=None, zorunlu_kosullar=[], tercihler=[], limit=2, cursor=None)
    assert sehir.sonuclar[0].sonuc_turu.value == "sehir"
    ilce = ara(arama_oturumu, q="Atakum", sehir_degeri="samsun", ilce_id=None, tur=None, zorunlu_kosullar=[], tercihler=[], limit=2, cursor=None)
    assert ilce.sonuclar[0].sonuc_turu.value == "ilce"
    kategori = ara(arama_oturumu, q="kahve", sehir_degeri="samsun", ilce_id=None, tur=None, zorunlu_kosullar=[], tercihler=[], limit=2, cursor=None)
    assert kategori.sonuclar[0].sonuc_turu.value == "kategori"
