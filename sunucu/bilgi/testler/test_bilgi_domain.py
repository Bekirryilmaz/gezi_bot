from datetime import datetime, timedelta, timezone

import pytest

from sunucu.bilgi.domain import BilgiDurumu, HakDurumu, KaynakHaklari, KullanimAmaci, ZamanKapsami, yayin_adayi_mi


def test_bilinmeyen_hak_izin_sayilmaz():
    assert not KaynakHaklari().izinli_mi(KullanimAmaci.TUREV_IDDIA)


@pytest.mark.parametrize("durum", [BilgiDurumu.BILINMIYOR, BilgiDurumu.CELISKILI, BilgiDurumu.ESKIMIS, BilgiDurumu.GERI_CEKILMIS])
def test_bilinmeyen_celiskili_eskimis_geri_cekilmis_yayin_adayi_degil(durum):
    assert not yayin_adayi_mi(bilgi_durumu=durum, kaynak_haklari=KaynakHaklari(turev_iddia=HakDurumu.IZINLI), destekleyen_kanit_sayisi=2, ai_tarafindan_uretildi=False)


def test_ai_ciktisi_dogrudan_yayin_adayi_degil():
    assert not yayin_adayi_mi(bilgi_durumu=BilgiDurumu.BILINIYOR, kaynak_haklari=KaynakHaklari(turev_iddia=HakDurumu.IZINLI), destekleyen_kanit_sayisi=1, ai_tarafindan_uretildi=True)


def test_zamanlar_ayri_tutulur_ve_gecersiz_aralik_reddedilir():
    simdi = datetime.now(timezone.utc)
    kapsam = ZamanKapsami(simdi - timedelta(days=3), simdi - timedelta(days=2), simdi - timedelta(days=1), simdi, simdi, simdi, simdi - timedelta(days=1))
    assert kapsam.cekilme_zamani != kapsam.sisteme_alinma_zamani
    with pytest.raises(ValueError):
        kapsam.dogrula()

