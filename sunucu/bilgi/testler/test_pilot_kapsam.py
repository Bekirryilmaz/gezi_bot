from ortak.sabitler import TamamlikHucresi
from sunucu.bilgi.pilot_kapsam import (
    matris_kolon_ozeti,
    nlp_kapsam_ozeti,
    rota_durum_ozeti,
    rota_simulasyonu,
)
from sunucu.bilgi.rota_hazirlik import RotaHazirlikGirdisi, rota_hazirligini_hesapla
from sunucu.bilgi.tamamlik_matrisi import eksik_onemli_aileler


def _satir(*, durum: str, amac: str, ilce: str, saat: str) -> dict:
    return {
        "amaclar": [amac],
        "ilce_adi": ilce,
        "matris": {
            "kimlik": TamamlikHucresi.BILINIYOR.value,
            "ilce": TamamlikHucresi.BILINIYOR.value,
            "koordinat": TamamlikHucresi.BILINIYOR.value,
            "amac": TamamlikHucresi.BILINIYOR.value,
            "calisma_saatleri": saat,
        },
        "rota_hazirlik": {"durum": durum, "neden_kodlari": [], "kirilim": {}},
        "nlp": {
            "sessiz_ortam": {
                "guven_sinifi": "orta",
                "durum": "aktif",
                "preference_eligible": True,
            }
        }
        if amac == "kahve_icmek"
        else {},
    }


def test_rota_simulasyonu_amac_ve_ilce_ayirir():
    satirlar = [
        _satir(durum="rota_hazir", amac="kahve_icmek", ilce="Atakum", saat="biliniyor"),
        _satir(durum="rota_sinirli", amac="kahve_icmek", ilce="Ilkadim", saat="yalniz_dahili"),
        _satir(durum="rota_sinirli", amac="yemek_yemek", ilce="Atakum", saat="bilinmiyor"),
        _satir(
            durum="kesif_adayi", amac="tarihi_kulturel_ziyaret", ilce="Ilkadim", saat="bilinmiyor"
        ),
    ]
    sim = rota_simulasyonu(satirlar)
    assert sim["pilot_toplam"] == 4
    assert sim["durum"]["rota_hazir"] == 1
    assert sim["durum"]["rota_sinirli"] == 2
    assert sim["amac"]["kahve_icmek"]["rota_hazir"] == 1
    assert sim["amac"]["kahve_icmek"]["rota_sinirli"] == 1
    assert sim["ilce"]["Atakum"]["aday"] == 2
    assert sim["saat_biliniyor"] == 1
    nlp = nlp_kapsam_ozeti(satirlar)
    assert nlp["mekan_en_az_bir"] == 2
    assert nlp["preference_eligible"]["sessiz_ortam"] == 2
    assert rota_durum_ozeti(satirlar)["kesif_adayi"] == 1
    assert matris_kolon_ozeti(satirlar)["calisma_saatleri"]["biliniyor"] == 1


def test_eksik_aile_ve_saat_siz_hazir_olmaz():
    satir = {
        "calisma_saatleri": TamamlikHucresi.BILINMIYOR.value,
        "wifi": TamamlikHucresi.BILINMIYOR.value,
        "otopark": TamamlikHucresi.YALNIZ_DAHILI.value,
        "acik_alan": TamamlikHucresi.BILINIYOR.value,
        "erisilebilirlik": TamamlikHucresi.BILINMIYOR.value,
        "aile": TamamlikHucresi.BILINMIYOR.value,
        "cocuk": TamamlikHucresi.BILINMIYOR.value,
        "calisma": TamamlikHucresi.BILINMIYOR.value,
        "sessizlik": TamamlikHucresi.BILINMIYOR.value,
        "manzara": TamamlikHucresi.BILINMIYOR.value,
    }
    assert "calisma_saatleri" in eksik_onemli_aileler(satir)
    assert "otopark" not in eksik_onemli_aileler(satir)
    ozet = rota_hazirligini_hesapla(
        RotaHazirlikGirdisi(
            kimlik_sinifi="guclu",
            sube_durum="aktif",
            koordinat_gecerli=True,
            ilce_id="ilce-1",
            amaclar=("kahve_icmek",),
            yayin_uygun=True,
            calisma_saati=TamamlikHucresi.BILINMIYOR,
        )
    )
    assert ozet.durum.value == "rota_sinirli"
    assert ozet.kirilim["kamusal_skor"] is False
