from __future__ import annotations

from types import SimpleNamespace

from fastapi.testclient import TestClient

from sunucu.api import rotalar_router
from sunucu.api.uygulama import uygulama
from sunucu.rota_motoru.veri_tipleri import AdayYer, GunSonucu, RotaDuragiSonucu, RotaSonucu
from sunucu.veritabani.baglanti import oturum_al


class SahteOturum:
    def commit(self):
        return None

    def rollback(self):
        return None


def _sahte_oturum():
    yield SahteOturum()


def _tek_gunluk_sonuc() -> RotaSonucu:
    yer = AdayYer(
        id="yer-1",
        isim="Ornek Yer",
        ana_kategori="gezilecek_yer",
        alt_kategori="tarihi_kulturel",
        enlem=41.0,
        boylam=36.0,
        ozellikler={"sponsorlu_mekan": True},
    )
    durak = RotaDuragiSonucu(
        yer=yer,
        sira=1,
        onceki_duraktan_mesafe_metre=0,
        tahmini_ziyaret_suresi_dk=60,
        skor_kirilimi={"ic_skor": 99},
    )
    return RotaSonucu(
        id="rota-1",
        gunler=[GunSonucu(gun_no=1, duraklar=[durak], toplam_mesafe_metre=0, toplam_sure_dakikasi=60)],
    )


def test_public_openapi_yalniz_tek_gunluk_create_gosteriyor():
    sema = uygulama.openapi()
    assert "/v1/gunluk-planlar" in sema["paths"]
    assert "/rotalar/olustur" not in sema["paths"]
    assert "/rotalar/olustur-alternatifler" not in sema["paths"]
    govde = sema["components"]["schemas"]["GunlukPlanTalebi"]["properties"]
    assert "gun_sayisi" not in govde
    assert all("konaklama" not in alan for alan in govde)


def test_gunluk_endpoint_cok_gun_ve_konaklama_alanlarini_reddeder():
    istemci = TestClient(uygulama)
    yanit = istemci.post(
        "/v1/gunluk-planlar",
        headers={"Idempotency-Key": "daily-invalid-1"},
        json={"sehir_anahtari": "samsun", "gun_sayisi": 2, "konaklama_bolge_adi": "Atakum"},
    )
    assert yanit.status_code == 422
    assert yanit.json()["hata"]["kod"] == "istek_dogrulanamadi"


def test_gunluk_endpoint_bir_gun_dondurur_ve_idempotent_tekrarlar(monkeypatch):
    rotalar_router._IDEMPOTENCY_KAYITLARI.clear()
    sayac = {"adet": 0}
    monkeypatch.setattr(
        rotalar_router,
        "_sehir_bul",
        lambda _oturum, _anahtar: (object(), SimpleNamespace(id="sehir-1")),
    )

    def sahte_motor(_oturum, _sehir_id, _tercihler):
        sayac["adet"] += 1
        return _tek_gunluk_sonuc()

    monkeypatch.setattr(rotalar_router, "gunluk_rota_olustur", sahte_motor)
    uygulama.dependency_overrides[oturum_al] = _sahte_oturum
    try:
        istemci = TestClient(uygulama)
        basliklar = {"Idempotency-Key": "daily-repeat-1"}
        ilk = istemci.post("/v1/gunluk-planlar", headers=basliklar, json={"sehir_anahtari": "samsun"})
        tekrar = istemci.post("/v1/gunluk-planlar", headers=basliklar, json={"sehir_anahtari": "samsun"})
    finally:
        uygulama.dependency_overrides.clear()

    assert ilk.status_code == 201
    assert tekrar.status_code == 200
    assert tekrar.json() == ilk.json()
    assert sayac["adet"] == 1
    assert "gunler" not in ilk.json() and "gun_sayisi" not in ilk.json()
    assert "skor_kirilimi" not in ilk.text


def test_legacy_cok_gunlu_create_kontrollu_olarak_kapali():
    istemci = TestClient(uygulama)
    yanit = istemci.post("/rotalar/olustur", json={"sehir_anahtari": "samsun", "gun_sayisi": 2})
    assert yanit.status_code == 410
    assert yanit.json()["hata"]["durum"] == "error"
