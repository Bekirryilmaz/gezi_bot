"""Mekan onerisi icin spam, captcha ve yonetici anahtari kontrolleri."""

from __future__ import annotations

import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict, deque
from threading import Lock

from fastapi import Header, HTTPException, Request

_EPOSTA_DESENI = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
_TURNSTILE_ADRES = "https://challenges.cloudflare.com/turnstile/v0/siteverify"

_kilit = Lock()
_ip_kayitlari: dict[str, deque[float]] = defaultdict(deque)
_eposta_kayitlari: dict[str, deque[float]] = defaultdict(deque)

IP_LIMITI = 5
IP_PENCERE_SN = 3600
EPOSTA_LIMITI = 8
EPOSTA_PENCERE_SN = 86400


def yonetici_anahtari() -> str:
    return os.environ.get("YONETICI_ANAHTAR", "yerel-yonetici").strip()


def istemci_ip(istek: Request) -> str:
    yonlendirilen = istek.headers.get("x-forwarded-for")
    if yonlendirilen:
        return yonlendirilen.split(",")[0].strip()
    if istek.client:
        return istek.client.host
    return "bilinmiyor"


def eposta_gecerli_mi(eposta: str) -> bool:
    return bool(_EPOSTA_DESENI.match(eposta.strip()))


def _pencere_temizle(kuyruk: deque[float], pencere_sn: int) -> None:
    sinir = time.monotonic() - pencere_sn
    while kuyruk and kuyruk[0] < sinir:
        kuyruk.popleft()


def hiz_siniri_kontrol(ip: str, eposta: str) -> None:
    """Ayni IP / e-posta icin kaba hiz limiti. Bellek ici; tek surec icin yeter."""
    simdi = time.monotonic()
    with _kilit:
        ip_kuyruk = _ip_kayitlari[ip]
        _pencere_temizle(ip_kuyruk, IP_PENCERE_SN)
        if len(ip_kuyruk) >= IP_LIMITI:
            raise HTTPException(
                status_code=429,
                detail="Cok fazla oneri gonderildi. Biraz sonra tekrar dene.",
            )

        eposta_kuyruk = _eposta_kayitlari[eposta.lower()]
        _pencere_temizle(eposta_kuyruk, EPOSTA_PENCERE_SN)
        if len(eposta_kuyruk) >= EPOSTA_LIMITI:
            raise HTTPException(
                status_code=429,
                detail="Bu e-posta ile gunluk oneri sinirina ulasildi.",
            )

        ip_kuyruk.append(simdi)
        eposta_kuyruk.append(simdi)


def turnstile_dogrula(jeton: str | None, ip: str) -> None:
    """Cloudflare Turnstile. Gizli anahtar yoksa gelistirme ortaminda atlanir."""
    gizli = os.environ.get("TURNSTILE_GIZLI_ANAHTAR", "").strip()
    if not gizli:
        return
    if not jeton:
        raise HTTPException(status_code=400, detail="Dogrulama (Turnstile) tamamlanmadi.")

    govde = urllib.parse.urlencode(
        {"secret": gizli, "response": jeton, "remoteip": ip}
    ).encode()
    istek = urllib.request.Request(_TURNSTILE_ADRES, data=govde, method="POST")
    try:
        with urllib.request.urlopen(istek, timeout=8) as yanit:
            sonuc = json.loads(yanit.read().decode())
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as hata:
        raise HTTPException(status_code=502, detail="Dogrulama servisine ulasilamadi.") from hata

    if not sonuc.get("success"):
        raise HTTPException(status_code=400, detail="Dogrulama basarisiz. Sayfayi yenileyip tekrar dene.")


def yonetici_gerekli(
    x_yonetici_anahtar: str | None = Header(default=None, alias="X-Yonetici-Anahtar"),
    authorization: str | None = Header(default=None),
) -> None:
    beklenen = yonetici_anahtari()
    gelen = x_yonetici_anahtar
    if not gelen and authorization and authorization.lower().startswith("bearer "):
        gelen = authorization[7:].strip()
    if not gelen or gelen != beklenen:
        raise HTTPException(status_code=401, detail="Yonetici anahtari gecersiz.")
