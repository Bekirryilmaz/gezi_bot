from sunucu.kimlik.domain import EslemeSonucu, eslemeyi_degerlendir


def test_ayni_isimli_farkli_sube_kalici_birlesmez():
    sonuc = eslemeyi_degerlendir(ayni_kaynak=False, ayni_kategori=True, isim_benzerligi=100, mesafe_metre=95)
    assert sonuc.sonuc is EslemeSonucu.ADAY


def test_aday_ile_kabul_ayridir():
    aday = eslemeyi_degerlendir(ayni_kaynak=False, ayni_kategori=True, isim_benzerligi=90, mesafe_metre=20)
    kabul = eslemeyi_degerlendir(ayni_kaynak=False, ayni_kategori=True, isim_benzerligi=99, mesafe_metre=10, telefon_eslesiyor=True)
    assert aday.sonuc is EslemeSonucu.ADAY
    assert kabul.sonuc is EslemeSonucu.OTOMATIK_KABUL

