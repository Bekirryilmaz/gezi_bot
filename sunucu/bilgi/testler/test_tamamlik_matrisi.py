from ortak.sabitler import TamamlikHucresi
from sunucu.bilgi.tamamlik_matrisi import (
    AlanKaniti,
    eksik_onemli_aileler,
    hucreyi_coz,
    matris_satirini_kur,
)


def test_hucre_yayin_dahili_celiski_eskimis():
    assert (
        hucreyi_coz(AlanKaniti(yayin_durumu="yayinlandi", bilgi_durumu="biliniyor"))
        is TamamlikHucresi.BILINIYOR
    )
    assert hucreyi_coz(AlanKaniti(osm_var=True)) is TamamlikHucresi.YALNIZ_DAHILI
    assert hucreyi_coz(AlanKaniti(nlp_var=True)) is TamamlikHucresi.YALNIZ_DAHILI
    assert hucreyi_coz(AlanKaniti(bilgi_durumu="celiskili")) is TamamlikHucresi.CELISKILI
    assert (
        hucreyi_coz(AlanKaniti(yayin_durumu="yayinlandi", bilgi_durumu="eskimis"))
        is TamamlikHucresi.ESKIMIS
    )
    assert hucreyi_coz(AlanKaniti()) is TamamlikHucresi.BILINMIYOR


def test_matris_satiri_ve_eksik_aileler():
    satir = matris_satirini_kur(
        kimlik_sinifi="guclu",
        isim_gecerli=True,
        ilce_id="ilce-1",
        koordinat_gecerli=True,
        alt_kategori="kafe",
        amaclar=("kahve_icmek",),
        claimler={"wifi": AlanKaniti(yayin_durumu="yayinlandi", bilgi_durumu="biliniyor")},
        nlp={"sessiz_ortam": True, "aile_uygunlugu": True},
        osm={"calisma_saatleri": True, "wifi": True},
    )
    assert satir["kimlik"] == "biliniyor"
    assert satir["amac"] == "biliniyor"
    assert satir["wifi"] == "biliniyor"
    assert satir["calisma_saatleri"] == "yalniz_dahili"
    assert satir["sessizlik"] == "yalniz_dahili"
    assert satir["aile"] == "yalniz_dahili"
    assert satir["otopark"] == "bilinmiyor"
    assert "otopark" in eksik_onemli_aileler(satir)
    assert "wifi" not in eksik_onemli_aileler(satir)
    karantina = matris_satirini_kur(
        kimlik_sinifi="karantina",
        isim_gecerli=False,
        ilce_id=None,
        koordinat_gecerli=False,
        alt_kategori="internet_kafe",
        amaclar=(),
        claimler={},
        nlp={},
        osm={},
    )
    assert karantina["kimlik"] == "celiskili"
    assert karantina["amac"] == "bilinmiyor"
