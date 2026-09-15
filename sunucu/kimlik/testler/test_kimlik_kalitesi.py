from ortak.sabitler import KimlikKaliteSinifi, YemeIcmeAltKategori
from sunucu.kimlik.kalite import (
    DuplicateKarari,
    duplicate_kararini_ver,
    isim_gecerli_mi,
    kimlik_kalitesini_hesapla,
    oneriye_uygun_mu,
)
from sunucu.kimlik.kalite_servisi import kaynak_etiketinden_kategori_duzelt


def test_kaynak_etiketi_dondurma_kafe_kimligini_tatliya_ceker():
    assert (
        kaynak_etiketinden_kategori_duzelt("Mahalle Dondurma", "kafe")
        == YemeIcmeAltKategori.TATLI_PASTANE.value
    )
    assert kaynak_etiketinden_kategori_duzelt("Internet Cafe", "kafe") == (
        YemeIcmeAltKategori.INTERNET_KAFE.value
    )
    assert kaynak_etiketinden_kategori_duzelt("Sahil Kafe", "kafe") is None


def test_nokta_ve_tek_karakter_isim_gecersizdir():
    assert isim_gecerli_mi(".") is False
    assert isim_gecerli_mi(" ") is False
    assert isim_gecerli_mi("F") is False
    assert isim_gecerli_mi("153") is False
    assert isim_gecerli_mi("...") is False
    assert isim_gecerli_mi("Günevi Atölye") is True
    assert isim_gecerli_mi("153 Restoran") is True


def test_gecersiz_isim_karantinaya_dusurur_ve_oneriye_girmez():
    ozet = kimlik_kalitesini_hesapla(
        isim=".",
        enlem=38.32,
        boylam=26.64,
        sehir_anahtari="samsun",
        alt_kategori="meyhane_bar",
        kaynak_sayisi=1,
        ayni_isim_yakin_cift=0,
    )
    assert ozet.sinif is KimlikKaliteSinifi.KARANTINA
    assert oneriye_uygun_mu(ozet.sinif) is False
    assert "isim_gecersiz" in ozet.kirilim["bayraklar"]
    assert "sehir_disi_koordinat" in ozet.kirilim["bayraklar"]


def test_uzak_ayni_isim_otomatik_birlesmez():
    karar = duplicate_kararini_ver(
        ayni_kaynak_id=False,
        isim_ayni=True,
        mesafe_metre=12_000,
        ayni_telefon=False,
        ayni_website=False,
        ayni_kategori=True,
        ayni_koordinat=False,
    )
    assert karar is DuplicateKarari.AYRI_TUT


def test_guclu_kimlik_eslesmesi_otomatik_birlesir_transitive_olmaz():
    karar = duplicate_kararini_ver(
        ayni_kaynak_id=True,
        isim_ayni=True,
        mesafe_metre=5,
        ayni_telefon=True,
        ayni_website=True,
        ayni_kategori=True,
        ayni_koordinat=True,
    )
    assert karar is DuplicateKarari.OTOMATIK_BIRLESTIR
    yakin_farkli_telefon = duplicate_kararini_ver(
        ayni_kaynak_id=False,
        isim_ayni=True,
        mesafe_metre=40,
        ayni_telefon=False,
        ayni_website=False,
        ayni_kategori=True,
        ayni_koordinat=False,
    )
    assert yakin_farkli_telefon is DuplicateKarari.INSAN_INCELEMESI


def test_zincir_subesi_uzaksa_ayri_kalir():
    karar = duplicate_kararini_ver(
        ayni_kaynak_id=False,
        isim_ayni=True,
        mesafe_metre=3_500,
        ayni_telefon=False,
        ayni_website=True,
        ayni_kategori=True,
        ayni_koordinat=False,
        zincir_marka=True,
    )
    assert karar is DuplicateKarari.AYRI_TUT
