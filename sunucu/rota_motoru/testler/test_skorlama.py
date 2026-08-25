"""skorlama.py icin birim testleri -- sentetik AdayYer verisiyle,
veritabani gerektirmeden calisir."""

from __future__ import annotations

from sunucu.rota_motoru.skorlama import yer_uygunluk_puani
from sunucu.rota_motoru.veri_tipleri import AdayYer, RotaTercihleri


def _ornek_yer(**gecersiz_kilinanlar) -> AdayYer:
    varsayilanlar = dict(
        id="yer-1",
        isim="Ornek Yer",
        ana_kategori="gezilecek_yer",
        alt_kategori="tarihi_kulturel",
        enlem=41.29,
        boylam=36.33,
        deneyim_puanlari={"tarihi_kulturel_puani": 90, "rahatlatici_sakin_puani": 40},
    )
    varsayilanlar.update(gecersiz_kilinanlar)
    return AdayYer(**varsayilanlar)


def test_zorunlu_durak_en_yuksek_puani_alir():
    yer = _ornek_yer(id="zorunlu-yer")
    tercihler = RotaTercihleri(zorunlu_duraklar=["zorunlu-yer"])

    sonuc = yer_uygunluk_puani(yer, tercihler)

    assert sonuc.zorunlu_mu is True
    assert sonuc.toplam_puan >= 1000


def test_ilgi_agirligi_deneyim_puanini_yansitir():
    tarihi_yer = _ornek_yer(deneyim_puanlari={"tarihi_kulturel_puani": 90})
    eglence_yer = _ornek_yer(id="yer-2", deneyim_puanlari={"eglence_puani": 90})
    tercihler = RotaTercihleri(ilgi_agirliklari={"tarihi_kulturel_puani": 1.0})

    tarihi_sonuc = yer_uygunluk_puani(tarihi_yer, tercihler)
    eglence_sonuc = yer_uygunluk_puani(eglence_yer, tercihler)

    assert tarihi_sonuc.toplam_puan > eglence_sonuc.toplam_puan
    assert "deneyim:tarihi_kulturel_puani" in tarihi_sonuc.kirilim


def test_ucuz_tercihi_pahali_yeri_cezalandirir():
    ucuz_yer = _ornek_yer(id="ucuz", yer_profili={"fiyat_algisi": {"deger": "ucuz", "guven": 1.0}})
    pahali_yer = _ornek_yer(id="pahali", yer_profili={"fiyat_algisi": {"deger": "pahali", "guven": 1.0}})
    tercihler = RotaTercihleri(ucuz_tercih_et=True)

    ucuz_puan = yer_uygunluk_puani(ucuz_yer, tercihler).toplam_puan
    pahali_puan = yer_uygunluk_puani(pahali_yer, tercihler).toplam_puan

    assert ucuz_puan > pahali_puan


def test_ucuz_tercihi_kapaliyken_fiyat_etkisiz_kalir():
    ucuz_yer = _ornek_yer(id="ucuz", yer_profili={"fiyat_algisi": {"deger": "ucuz", "guven": 1.0}})
    tercihler = RotaTercihleri(ucuz_tercih_et=False)

    sonuc = yer_uygunluk_puani(ucuz_yer, tercihler)

    assert "fiyat_tercihi" not in sonuc.kirilim


def test_sakin_tercihi_kalabalik_yeri_cezalandirir():
    sakin_yer = _ornek_yer(id="sakin", yer_profili={"kalabalik_zamanlar": {}})
    kalabalik_yer = _ornek_yer(id="kalabalik", yer_profili={"kalabalik_zamanlar": {"hafta_sonu_aksam": "kalabalik"}})
    tercihler = RotaTercihleri(sakin_tercih_et=True)

    sakin_puan = yer_uygunluk_puani(sakin_yer, tercihler).toplam_puan
    kalabalik_puan = yer_uygunluk_puani(kalabalik_yer, tercihler).toplam_puan

    assert sakin_puan > kalabalik_puan


def test_aktivite_eslesmesi_bonus_verir():
    yer_aktiviteli = _ornek_yer(aktiviteler=["yuzme"])
    yer_aktivitesiz = _ornek_yer(id="yer-2")
    tercihler = RotaTercihleri(aktiviteler=["yuzme"])

    aktiviteli_puan = yer_uygunluk_puani(yer_aktiviteli, tercihler).toplam_puan
    aktivitesiz_puan = yer_uygunluk_puani(yer_aktivitesiz, tercihler).toplam_puan

    assert aktiviteli_puan > aktivitesiz_puan


def test_kaynak_kalitesi_katkisi_esit_skorlari_ayirir():
    yuksek_puanli = _ornek_yer(id="yuksek", kaynakta_puan_ortalamasi=4.8)
    dusuk_puanli = _ornek_yer(id="dusuk", kaynakta_puan_ortalamasi=3.0)
    tercihler = RotaTercihleri()

    assert yer_uygunluk_puani(yuksek_puanli, tercihler).toplam_puan > yer_uygunluk_puani(dusuk_puanli, tercihler).toplam_puan


def test_sponsorlu_mekan_bonus_ekler():
    yer = _ornek_yer(ozellikler={"sponsorlu_mekan": True})
    sonuc = yer_uygunluk_puani(yer, RotaTercihleri())

    assert sonuc.kirilim["sponsorlu_bonusu"] == 30
    assert sonuc.toplam_puan >= 30


def test_sehrin_klasigi_bonus_ekler():
    yer = _ornek_yer(ozellikler={"sehrin_klasigi": "evet"})
    sonuc = yer_uygunluk_puani(yer, RotaTercihleri())

    assert sonuc.kirilim["sehrin_klasigi_bonusu"] == 15


def test_yol_yorgunlugu_skoru_yarilar():
    yer = _ornek_yer(ortalama_ziyaret_suresi_dk=20, kaynakta_puan_ortalamasi=5.0)
    tercihler = RotaTercihleri()
    kisa_yol = yer_uygunluk_puani(yer, tercihler, yol_suresi_dk=10)
    uzun_yol = yer_uygunluk_puani(yer, tercihler, yol_suresi_dk=40)

    assert "yol_yorgunlugu_cezasi" not in kisa_yol.kirilim
    assert "yol_yorgunlugu_cezasi" in uzun_yol.kirilim
    assert uzun_yol.toplam_puan == round(kisa_yol.toplam_puan * 0.5, 2)
