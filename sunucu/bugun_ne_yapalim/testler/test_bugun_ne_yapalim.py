from datetime import datetime
from types import SimpleNamespace
from zoneinfo import ZoneInfo

from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.exc import OperationalError

from sunucu.api.altyapi import ApiGuvenlikMiddleware
from sunucu.bugun_ne_yapalim.router import yonlendirici
from sunucu.bugun_ne_yapalim.semalar import BugunNeYapalimTalebi
from sunucu.bugun_ne_yapalim.servis import _coz
from sunucu.karar_motoru.domain import CografiBaglam, KararBaglami, ZamanBaglami
from sunucu.veritabani.baglanti import oturum_al


def _ilceler():
    return [SimpleNamespace(isim="Atakum", arama_isim="atakum")]


def test_serbest_metin_basit_parser_uydurmadan_yapilandirir():
    cozum = _coz(
        BugunNeYapalimTalebi(
            serbest_metin="Atakum'da arkadaşlarla 2 saat kahve, Wi-Fi kesin olsun ve sakin olsun."
        ),
        _ilceler(),
    )
    assert cozum.amac == "kahve_icmek"
    assert cozum.ilce == "Atakum"
    assert cozum.kisi_baglami == "arkadaslar"
    assert cozum.sure_dakika == 120
    assert cozum.zorunlu_kosullar == ("wifi",)
    assert cozum.tercihler == ("sessiz_ortam",)


def test_yapilandirilmis_degerler_parserdan_once_gelir():
    cozum = _coz(
        BugunNeYapalimTalebi(
            serbest_metin="kahve",
            niyet={"amac": "yemek_yemek", "sure_dakika": 90, "sehir": "Samsun"},
        ),
        _ilceler(),
    )
    assert cozum.amac == "yemek_yemek"
    assert cozum.sure_dakika == 90


def test_yetersiz_baglam_tek_amac_netlestirmesine_kalir():
    cozum = _coz(BugunNeYapalimTalebi(serbest_metin="Atakum'da bir yer arıyorum"), _ilceler())
    assert cozum.ilce == "Atakum"
    assert cozum.amac is None


def test_desteklenmeyen_zorunlu_kosul_parserda_sessizce_kaybolmaz():
    cozum = _coz(
        BugunNeYapalimTalebi(
            serbest_metin="kahve",
            niyet={
                "sehir": "Samsun",
                "zorunlu_kosullar": ["cocuk_oyun_alani"],
            },
        ),
        _ilceler(),
    )
    assert cozum.zorunlu_kosullar == ("cocuk_oyun_alani",)


def test_entry_channel_karar_parmak_izini_degistirmez():
    zaman = ZamanBaglami(
        ziyaret_tarihi=datetime(2026, 9, 15).date(),
        degerlendirme_zamani=datetime(2026, 9, 15, 12, tzinfo=ZoneInfo("Europe/Istanbul")),
    )
    ortak = {"amac": "kahve_icmek", "cografi_baglam": CografiBaglam("Samsun"), "zaman": zaman}
    kesfet = KararBaglami(**ortak, giris_kanali="kesfet")
    bugun = KararBaglami(**ortak, giris_kanali="bugun_ne_yapalim")
    assert kesfet.karar_parmak_izi() == bugun.karar_parmak_izi()


def test_endpoint_openapi_sozlesmesi_ve_unavailable(monkeypatch):
    class SahteOturum:
        def rollback(self):
            pass

    def oturum_ver():
        return SahteOturum()

    def patla(*args, **kwargs):
        raise OperationalError("select", {}, Exception("db yok"))

    monkeypatch.setattr("sunucu.bugun_ne_yapalim.router.bugun_ne_yapalim", patla)
    mini = FastAPI()
    mini.add_middleware(ApiGuvenlikMiddleware)
    mini.include_router(yonlendirici)
    mini.dependency_overrides[oturum_al] = oturum_ver
    assert "/v1/bugun-ne-yapalim" in mini.openapi()["paths"]
    yanit = TestClient(mini).post("/v1/bugun-ne-yapalim", json={"serbest_metin": "kahve"})
    assert yanit.status_code == 503
    assert yanit.json()["hata"]["durum"] == "unavailable"
