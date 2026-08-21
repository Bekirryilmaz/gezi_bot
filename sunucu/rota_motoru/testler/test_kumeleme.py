"""kumeleme.py icin birim testleri."""

from __future__ import annotations

from sunucu.rota_motoru.kumeleme import SkorluYer, agirlik_merkezi_hesapla, gunlere_boluster
from sunucu.rota_motoru.skorlama import SkorSonucu
from sunucu.rota_motoru.veri_tipleri import AdayYer


def _skorlu_yer(id: str, enlem: float, boylam: float, puan: float = 10.0) -> SkorluYer:
    yer = AdayYer(id=id, isim=id, ana_kategori="gezilecek_yer", alt_kategori="doga_manzara", enlem=enlem, boylam=boylam)
    return SkorluYer(yer=yer, skor=SkorSonucu(toplam_puan=puan))


def test_gunlere_boluster_tum_yerleri_dagitir():
    merkez = (41.29, 36.33)
    yerler = [
        _skorlu_yer("kuzey", 41.35, 36.33),
        _skorlu_yer("dogu", 41.29, 36.45),
        _skorlu_yer("guney", 41.20, 36.33),
        _skorlu_yer("bati", 41.29, 36.20),
    ]

    sonuc = gunlere_boluster(yerler, gun_sayisi=4, merkez_nokta=merkez)

    toplam_dagitilan = sum(len(gun_yerleri) for gun_yerleri in sonuc.values())
    assert toplam_dagitilan == len(yerler)
    assert set(sonuc.keys()) == {1, 2, 3, 4}


def test_gunlere_boluster_bos_liste_ile_bos_gunler_dondurur():
    sonuc = gunlere_boluster([], gun_sayisi=3, merkez_nokta=(41.29, 36.33))

    assert set(sonuc.keys()) == {1, 2, 3}
    assert all(gun_yerleri == [] for gun_yerleri in sonuc.values())


def test_gecersiz_gun_sayisi_hata_verir():
    import pytest

    with pytest.raises(ValueError):
        gunlere_boluster([_skorlu_yer("a", 41.0, 36.0)], gun_sayisi=0, merkez_nokta=(41.0, 36.0))


def test_agirlik_merkezi_ortalamayi_dogru_hesaplar():
    yerler = [
        AdayYer(id="a", isim="a", ana_kategori="gezilecek_yer", alt_kategori="doga_manzara", enlem=40.0, boylam=30.0),
        AdayYer(id="b", isim="b", ana_kategori="gezilecek_yer", alt_kategori="doga_manzara", enlem=42.0, boylam=32.0),
    ]

    enlem, boylam = agirlik_merkezi_hesapla(yerler)

    assert enlem == 41.0
    assert boylam == 31.0
