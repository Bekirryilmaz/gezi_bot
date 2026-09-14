"""API guvenlik, gozlemlenebilirlik ve tipli hata altyapisi."""

from __future__ import annotations

import contextvars
import json
import logging
import os
import re
import time
from collections import defaultdict, deque
from threading import Lock
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException

_REQUEST_ID = contextvars.ContextVar("request_id", default="-")
_GUVENLI_REQUEST_ID = re.compile(r"^[A-Za-z0-9._:-]{8,64}$")
_LOGGER = logging.getLogger("samandira.api")


class JsonLogFormatter(logging.Formatter):
    """Yalniz allow-list alanlari yazan JSON log formatter'i."""

    def format(self, record: logging.LogRecord) -> str:
        veri = {
            "zaman": self.formatTime(record, "%Y-%m-%dT%H:%M:%S%z"),
            "seviye": record.levelname.lower(),
            "olay": getattr(record, "olay", record.getMessage()),
            "request_id": getattr(record, "request_id", _REQUEST_ID.get()),
        }
        for alan in ("metot", "yol", "durum_kodu", "sure_ms", "hata_turu"):
            deger = getattr(record, alan, None)
            if deger is not None:
                veri[alan] = deger
        return json.dumps(veri, ensure_ascii=False, separators=(",", ":"))


def structured_logging_kur() -> None:
    # Uvicorn access log'u query string'i oldugu gibi yazabilir. Istekleri
    # yukaridaki allow-list JSON kaydi kapsadigi icin ham access log kapatilir.
    logging.getLogger("uvicorn.access").disabled = True
    if _LOGGER.handlers:
        return
    handler = logging.StreamHandler()
    handler.setFormatter(JsonLogFormatter())
    _LOGGER.addHandler(handler)
    _LOGGER.setLevel(os.environ.get("LOG_SEVIYESI", "INFO").upper())
    _LOGGER.propagate = False


def _hata_durumu(status_code: int) -> str:
    if status_code == 404:
        return "empty"
    if status_code in (409, 422):
        return "insufficient"
    if status_code in (429, 502, 503, 504):
        return "unavailable"
    return "error"


def hata_cevabi(
    *,
    status_code: int,
    kod: str,
    mesaj: str,
    request_id: str,
    ayrintilar: list[dict[str, str]] | None = None,
) -> JSONResponse:
    icerik: dict[str, object] = {
        "hata": {
            "kod": kod,
            "mesaj": mesaj,
            "durum": _hata_durumu(status_code),
            "request_id": request_id,
        }
    }
    if ayrintilar:
        icerik["hata"]["ayrintilar"] = ayrintilar  # type: ignore[index]
    return JSONResponse(status_code=status_code, content=icerik)


class ApiGuvenlikMiddleware(BaseHTTPMiddleware):
    """Request ID, guvenli log, govde limiti ve temel anonim write limiti."""

    def __init__(self, app):
        super().__init__(app)
        self.govde_limiti = int(os.environ.get("API_MAKSIMUM_GOVDE_BYTE", "65536"))
        self.dakikalik_yazma_limiti = int(os.environ.get("API_ANONIM_YAZMA_LIMITI", "20"))
        self._istekler: dict[str, deque[float]] = defaultdict(deque)
        self._kilit = Lock()

    def _request_id(self, request: Request) -> str:
        aday = request.headers.get("X-Request-ID", "")
        return aday if _GUVENLI_REQUEST_ID.fullmatch(aday) else str(uuid4())

    def _limit_asildi(self, request: Request, simdi: float) -> bool:
        if request.method in {"GET", "HEAD", "OPTIONS"}:
            return False
        istemci = request.client.host if request.client else "bilinmeyen"
        with self._kilit:
            zamanlar = self._istekler[istemci]
            while zamanlar and zamanlar[0] <= simdi - 60:
                zamanlar.popleft()
            if len(zamanlar) >= self.dakikalik_yazma_limiti:
                return True
            zamanlar.append(simdi)
        return False

    @staticmethod
    def _guvenlik_basliklarini_ekle(yanit, request_id: str) -> None:
        yanit.headers["X-Request-ID"] = request_id
        yanit.headers["X-Content-Type-Options"] = "nosniff"
        yanit.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

    async def dispatch(self, request: Request, call_next):
        baslangic = time.monotonic()
        request_id = self._request_id(request)
        token = _REQUEST_ID.set(request_id)
        request.state.request_id = request_id
        status_code = 500
        try:
            uzunluk = request.headers.get("content-length")
            try:
                uzunluk_degeri = int(uzunluk) if uzunluk is not None else None
            except ValueError:
                uzunluk_degeri = -1

            if uzunluk_degeri is not None and uzunluk_degeri < 0:
                yanit = hata_cevabi(
                    status_code=400,
                    kod="gecersiz_content_length",
                    mesaj="İstek gövdesi uzunluğu geçersiz.",
                    request_id=request_id,
                )
            elif uzunluk_degeri is not None and uzunluk_degeri > self.govde_limiti:
                yanit = hata_cevabi(
                    status_code=413,
                    kod="istek_govdesi_cok_buyuk",
                    mesaj="İstek gövdesi izin verilen sınırı aşıyor.",
                    request_id=request_id,
                )
            elif self._limit_asildi(request, time.monotonic()):
                yanit = hata_cevabi(
                    status_code=429,
                    kod="yazma_limiti_asildi",
                    mesaj="Çok sık yazma isteği gönderildi; kısa süre sonra yeniden deneyin.",
                    request_id=request_id,
                )
                yanit.headers["Retry-After"] = "60"
            else:
                yanit = await call_next(request)
            status_code = yanit.status_code
            self._guvenlik_basliklarini_ekle(yanit, request_id)
            return yanit
        finally:
            _LOGGER.info(
                "istek_tamamlandi",
                extra={
                    "olay": "istek_tamamlandi",
                    "request_id": request_id,
                    "metot": request.method,
                    "yol": request.url.path,
                    "durum_kodu": status_code,
                    "sure_ms": round((time.monotonic() - baslangic) * 1000, 2),
                },
            )
            _REQUEST_ID.reset(token)


def hata_yakalayicilari_kur(uygulama: FastAPI) -> None:
    @uygulama.exception_handler(StarletteHTTPException)
    async def http_hatasi(request: Request, hata: StarletteHTTPException) -> JSONResponse:
        return hata_cevabi(
            status_code=hata.status_code,
            kod=f"http_{hata.status_code}",
            mesaj=str(hata.detail),
            request_id=getattr(request.state, "request_id", str(uuid4())),
        )

    @uygulama.exception_handler(RequestValidationError)
    async def dogrulama_hatasi(request: Request, hata: RequestValidationError) -> JSONResponse:
        ayrintilar = [
            {
                "alan": ".".join(str(parca) for parca in sorun.get("loc", ())),
                "tur": str(sorun.get("type", "dogrulama_hatasi")),
            }
            for sorun in hata.errors()
        ]
        return hata_cevabi(
            status_code=422,
            kod="istek_dogrulanamadi",
            mesaj="İstek doğrulanamadı.",
            request_id=getattr(request.state, "request_id", str(uuid4())),
            ayrintilar=ayrintilar,
        )

    @uygulama.exception_handler(Exception)
    async def beklenmeyen_hata(request: Request, hata: Exception) -> JSONResponse:
        request_id = getattr(request.state, "request_id", str(uuid4()))
        _LOGGER.error(
            "beklenmeyen_hata",
            extra={
                "olay": "beklenmeyen_hata",
                "request_id": request_id,
                "hata_turu": type(hata).__name__,
            },
        )
        return hata_cevabi(
            status_code=500,
            kod="beklenmeyen_hata",
            mesaj="Beklenmeyen bir hata oluştu.",
            request_id=request_id,
        )
