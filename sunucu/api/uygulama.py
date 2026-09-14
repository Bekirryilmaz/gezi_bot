"""
FastAPI uygulamasi -- ana giris noktasi.

Yerel calistirma (repo kokunden):
    uvicorn sunucu.api.uygulama:uygulama --reload

Sonra taraycida http://127.0.0.1:8000/docs adresine gidip Swagger arayuzu
uzerinden tum uc noktalari deneyebilirsin.
"""

from __future__ import annotations

import os
from urllib.parse import urlparse

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from sunucu.api.altyapi import ApiGuvenlikMiddleware, hata_yakalayicilari_kur, structured_logging_kur
from sunucu.api.rotalar_router import yonlendirici as rotalar_yonlendirici
from sunucu.api.semalar import ApiHataCevabi
from sunucu.api.yerler_router import yonlendirici as yerler_yonlendirici
from sunucu.karar_motoru.router import yonlendirici as karar_yonlendirici
from sunucu.veritabani.baglanti import motor
from sunucu.admin.router import yonlendirici as admin_yonlendirici


def _izinli_originleri_al() -> list[str]:
    ortam = os.environ.get("UYGULAMA_ORTAMI", "development").lower()
    ham = os.environ.get("API_IZINLI_ORIGINLER")
    if ham is None:
        if ortam in {"production", "prod", "canli"}:
            raise RuntimeError("Production ortaminda API_IZINLI_ORIGINLER acikca tanimlanmalidir.")
        ham = "http://localhost:3000,http://127.0.0.1:3000"

    originler = [origin.strip().rstrip("/") for origin in ham.split(",") if origin.strip()]
    for origin in originler:
        ayrik = urlparse(origin)
        if origin == "*" or ayrik.scheme not in {"http", "https"} or not ayrik.netloc or ayrik.path:
            raise RuntimeError(f"Gecersiz CORS origin tanimi: {origin!r}")
        if ortam in {"production", "prod", "canli"} and ayrik.hostname in {"localhost", "127.0.0.1"}:
            raise RuntimeError("Production CORS listesi localhost iceremez.")
    return originler


def hazirlik_kontrolu() -> bool:
    try:
        with motor.connect() as baglanti:
            baglanti.execute(text("SELECT 1"))
            baglanti.execute(text("SELECT PostGIS_Version()"))
        return True
    except SQLAlchemyError:
        return False

structured_logging_kur()
uygulama = FastAPI(
    title="Şamandıra API",
    description=(
        "Karadeniz'in kisisel gezi rehberi — kesfet, oku, gun gun rotani kur. "
        "Yer, bolge ve kisisellestirilmis rota olusturma. Once Samsun, sonra tum kiyi."
    ),
    version="0.1.0",
    responses={
        400: {"model": ApiHataCevabi},
        404: {"model": ApiHataCevabi},
        409: {"model": ApiHataCevabi},
        422: {"model": ApiHataCevabi},
        429: {"model": ApiHataCevabi},
        500: {"model": ApiHataCevabi},
        503: {"model": ApiHataCevabi},
    },
)

# Faz 3'te Next.js (site/) buradan erisecek -- origin'ler ortam degiskeninden
# okunur ki gelistirme/canli ortamda farkli adresler kullanilabilsin.
_izinli_originler = _izinli_originleri_al()

uygulama.add_middleware(
    CORSMiddleware,
    allow_origins=_izinli_originler,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Accept", "Authorization", "Content-Type", "Idempotency-Key", "X-CSRF-Token", "X-Request-ID"],
    expose_headers=["X-Request-ID", "X-Idempotency-Key"],
)
uygulama.add_middleware(ApiGuvenlikMiddleware)
hata_yakalayicilari_kur(uygulama)

uygulama.include_router(yerler_yonlendirici)
uygulama.include_router(rotalar_yonlendirici)
uygulama.include_router(karar_yonlendirici)

admin_uygulama = FastAPI(
    title="Şamandıra İç Admin API",
    description="Public istemcilerden ayrik kimlik, claim, yayin ve audit operasyonlari.",
    version="1.0.0",
)
admin_uygulama.include_router(admin_yonlendirici)
uygulama.mount("/v1/admin", admin_uygulama)


@uygulama.get("/", include_in_schema=False)
def kok() -> dict:
    return {"mesaj": "Samandira API calisiyor. Dokumantasyon icin /docs adresine git."}


@uygulama.get("/health", tags=["sistem"])
def health() -> dict[str, str]:
    """Surecin ayakta oldugunu bildirir; dis bagimliliklara dokunmaz."""
    return {"durum": "ok"}


@uygulama.get("/readiness", tags=["sistem"])
def readiness() -> dict[str, str]:
    """PostgreSQL ve PostGIS erisilebilir olmadikca hazir sayilmaz."""
    if not hazirlik_kontrolu():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Veritabani veya PostGIS su anda kullanilamiyor.",
        )
    return {"durum": "hazir"}
