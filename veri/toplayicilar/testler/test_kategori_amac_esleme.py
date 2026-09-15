from ortak.sabitler import YemeIcmeAltKategori

from veri.toplayicilar.ortak_araclar import metinden_kategori_esle
from veri.toplayicilar.osm_toplayici import _elementten_kategori_bul


def test_kaynak_etiketi_internet_kafe_kafe_alt_dizesinden_once_gelir():
    sonuc = metinden_kategori_esle("Internet cafe")
    assert sonuc is not None
    assert sonuc[1] == YemeIcmeAltKategori.INTERNET_KAFE.value
    assert metinden_kategori_esle("Kafe")[1] == YemeIcmeAltKategori.KAFE.value


def test_kaynak_etiketi_dondurma_ve_pastane_tatli_kategorisidir():
    dondurma = metinden_kategori_esle("Mahalle Dondurma")
    pastane = metinden_kategori_esle("Merkez Pastane")
    assert dondurma is not None and dondurma[1] == YemeIcmeAltKategori.TATLI_PASTANE.value
    assert pastane is not None and pastane[1] == YemeIcmeAltKategori.TATLI_PASTANE.value


def test_osm_amenity_internet_cafe_kahve_kategorisi_degildir():
    kategori = _elementten_kategori_bul({"amenity": "internet_cafe", "name": "Xir"})
    assert kategori is not None
    assert kategori[1] == YemeIcmeAltKategori.INTERNET_KAFE.value
