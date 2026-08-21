"""
Cografi hesaplamalar icin kucuk, bagimsiz yardimci fonksiyonlar.

Bu dosya kok `ortak/` altinda tutulur (once `veri/ortak/` altindaydi) cunku
hem `veri/` (esleme, kalite_kontrol) hem `sunucu/` (rota_motoru) ayni
haversine hesabina ihtiyac duyuyor -- kod tekrarini onlemek icin tek bir
yerde tutulur.
"""

from __future__ import annotations

import math


def haversine_metre(enlem1: float, boylam1: float, enlem2: float, boylam2: float) -> float:
    """Iki (enlem, boylam) noktasi arasindaki gercek Dunya mesafesini
    (metre cinsinden) hesaplar. Duz Oklid mesafesi yerine haversine formulu
    kullanilir cunku enlem/boylam bir kure uzerindeki acisal koordinatlardir."""
    DUNYA_YARICAPI_METRE = 6_371_000.0
    e1, b1, e2, b2 = map(math.radians, (enlem1, boylam1, enlem2, boylam2))
    delta_e = e2 - e1
    delta_b = b2 - b1
    a = math.sin(delta_e / 2) ** 2 + math.cos(e1) * math.cos(e2) * math.sin(delta_b / 2) ** 2
    return 2 * DUNYA_YARICAPI_METRE * math.asin(math.sqrt(a))


def bearing_derece(enlem1: float, boylam1: float, enlem2: float, boylam2: float) -> float:
    """1. noktadan 2. noktaya olan yon acisini (bearing) derece cinsinden
    (0-360, 0=kuzey, 90=dogu) hesaplar.

    `sunucu/rota_motoru/kumeleme.py` tarafindan, bir merkez noktadan
    (konaklama veya agirlik merkezi) her adaya olan yonu bulup yerleri
    acisal dilimlere (sektorlere) bolmek icin kullanilir."""
    e1, b1, e2, b2 = map(math.radians, (enlem1, boylam1, enlem2, boylam2))
    delta_b = b2 - b1
    x = math.sin(delta_b) * math.cos(e2)
    y = math.cos(e1) * math.sin(e2) - math.sin(e1) * math.cos(e2) * math.cos(delta_b)
    aci = math.degrees(math.atan2(x, y))
    return (aci + 360) % 360
