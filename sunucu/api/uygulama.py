"""
FastAPI uygulamasi -- ana giris noktasi.

Yerel calistirma (repo kokunden):
    uvicorn sunucu.api.uygulama:uygulama --reload

Sonra taraycida http://127.0.0.1:8000/docs adresine gidip Swagger arayuzu
uzerinden tum uc noktalari deneyebilirsin.
"""

from __future__ import annotations

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sunucu.api.rotalar_router import yonlendirici as rotalar_yonlendirici
from sunucu.api.yerler_router import yonlendirici as yerler_yonlendirici

uygulama = FastAPI(
    title="Gezi Platformu API",
    description="Samsun (ve zamanla diger Karadeniz sehirleri) icin gezilecek yer, "
    "konaklama, yeme-icme verisi ve kisisellestirilmis rota olusturma API'si.",
    version="0.1.0",
)

# Faz 3'te Next.js (site/) buradan erisecek -- origin'ler ortam degiskeninden
# okunur ki gelistirme/canli ortamda farkli adresler kullanilabilsin.
_izinli_originler = [
    o.strip()
    for o in os.environ.get(
        "API_IZINLI_ORIGINLER",
        "http://localhost:3000,http://127.0.0.1:3000",
    ).split(",")
    if o.strip()
]

uygulama.add_middleware(
    CORSMiddleware,
    allow_origins=_izinli_originler,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

uygulama.include_router(yerler_yonlendirici)
uygulama.include_router(rotalar_yonlendirici)


@uygulama.get("/", include_in_schema=False)
def kok() -> dict:
    return {"mesaj": "Gezi Platformu API calisiyor. Dokumantasyon icin /docs adresine git."}
