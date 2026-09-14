from __future__ import annotations

import logging

from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest

from sunucu.api.altyapi import ApiGuvenlikMiddleware, JsonLogFormatter, hata_yakalayicilari_kur
from sunucu.api import uygulama as uygulama_modulu
from sunucu.api.uygulama import uygulama
from sunucu.veritabani.baglanti import VARSAYILAN_VERITABANI_URL, veritabani_yapilandirmasini_dogrula


def test_health_request_id_ve_typed_404():
    istemci = TestClient(uygulama)
    health = istemci.get("/health", headers={"X-Request-ID": "test-request-123"})
    bulunamadi = istemci.get("/olmayan-yol", headers={"X-Request-ID": "test-request-456"})

    assert health.status_code == 200
    assert health.json() == {"durum": "ok"}
    assert health.headers["X-Request-ID"] == "test-request-123"
    assert bulunamadi.status_code == 404
    assert bulunamadi.json()["hata"] == {
        "kod": "http_404",
        "mesaj": "Not Found",
        "durum": "empty",
        "request_id": "test-request-456",
    }


def test_readiness_bagimlilik_durumunu_ayirir(monkeypatch):
    istemci = TestClient(uygulama)
    monkeypatch.setattr(uygulama_modulu, "hazirlik_kontrolu", lambda: True)
    assert istemci.get("/readiness").json() == {"durum": "hazir"}

    monkeypatch.setattr(uygulama_modulu, "hazirlik_kontrolu", lambda: False)
    yanit = istemci.get("/readiness")
    assert yanit.status_code == 503
    assert yanit.json()["hata"]["durum"] == "unavailable"


def test_beklenmeyen_hata_tipli_zarfla_doner_ve_ayrinti_sizdirmaz():
    mini = FastAPI()
    mini.add_middleware(ApiGuvenlikMiddleware)
    hata_yakalayicilari_kur(mini)

    @mini.get("/patla")
    def patla():
        raise RuntimeError("veritabani-parolasi-gibi-hassas-ayrinti")

    istemci = TestClient(mini, raise_server_exceptions=False)
    yanit = istemci.get("/patla", headers={"X-Request-ID": "test-request-500"})

    assert yanit.status_code == 500
    assert yanit.json()["hata"] == {
        "kod": "beklenmeyen_hata",
        "mesaj": "Beklenmeyen bir hata oluştu.",
        "durum": "error",
        "request_id": "test-request-500",
    }
    assert "hassas" not in yanit.text


def test_cors_yalniz_izinli_origin_icin_baslik_doner():
    istemci = TestClient(uygulama)
    izinli = istemci.options(
        "/health",
        headers={"Origin": "http://localhost:3000", "Access-Control-Request-Method": "GET"},
    )
    izinsiz = istemci.options(
        "/health",
        headers={"Origin": "https://example.invalid", "Access-Control-Request-Method": "GET"},
    )
    assert izinli.headers["access-control-allow-origin"] == "http://localhost:3000"
    assert "access-control-allow-origin" not in izinsiz.headers


def test_production_cors_wildcard_ve_localhost_reddeder(monkeypatch):
    monkeypatch.setenv("UYGULAMA_ORTAMI", "production")
    monkeypatch.setenv("API_IZINLI_ORIGINLER", "*")
    with pytest.raises(RuntimeError):
        uygulama_modulu._izinli_originleri_al()

    monkeypatch.setenv("API_IZINLI_ORIGINLER", "http://localhost:3000")
    with pytest.raises(RuntimeError):
        uygulama_modulu._izinli_originleri_al()


def test_anonim_write_rate_limit(monkeypatch):
    monkeypatch.setenv("API_ANONIM_YAZMA_LIMITI", "2")
    mini = FastAPI()
    mini.add_middleware(ApiGuvenlikMiddleware)
    hata_yakalayicilari_kur(mini)

    @mini.post("/yaz")
    def yaz():
        return {"durum": "ok"}

    istemci = TestClient(mini)
    assert istemci.post("/yaz").status_code == 200
    assert istemci.post("/yaz").status_code == 200
    sinirli = istemci.post("/yaz")
    assert sinirli.status_code == 429
    assert sinirli.json()["hata"]["kod"] == "yazma_limiti_asildi"


def test_gecersiz_content_length_tipli_ve_request_id_baslikli_doner():
    istemci = TestClient(uygulama)
    yanit = istemci.post(
        "/rotalar/olustur",
        headers={"Content-Length": "gecersiz", "X-Request-ID": "test-request-length"},
        content=b"{}",
    )

    assert yanit.status_code == 400
    assert yanit.json()["hata"]["kod"] == "gecersiz_content_length"
    assert yanit.headers["X-Request-ID"] == "test-request-length"
    assert yanit.headers["X-Content-Type-Options"] == "nosniff"


def test_production_varsayilan_db_parolasiyla_baslamaz(monkeypatch):
    monkeypatch.delenv("VERITABANI_URL", raising=False)
    try:
        veritabani_yapilandirmasini_dogrula(VARSAYILAN_VERITABANI_URL, "production")
    except RuntimeError as hata:
        assert "VERITABANI_URL" in str(hata)
    else:
        raise AssertionError("Production varsayilan DB ayari reddedilmeliydi")


def test_structured_log_allow_list_hassas_ek_alanlari_yazmaz():
    kayit = logging.LogRecord("test", logging.INFO, __file__, 1, "guvenli", (), None)
    kayit.authorization = "Bearer cok-gizli"  # type: ignore[attr-defined]
    kayit.query = "token=cok-gizli"  # type: ignore[attr-defined]
    metin = JsonLogFormatter().format(kayit)
    assert "cok-gizli" not in metin
    assert '"olay":"guvenli"' in metin
