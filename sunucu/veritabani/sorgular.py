"""
Yer sorgulari icin ortak yardimcilar.

Ozellikle PostGIS `Geography` alanindan (enlem, boylam) cikarma mantigi
burada TEK bir yerde toplanir -- hem `sunucu/api` (yer listeleme/detay)
hem `sunucu/rota_motoru` (skorlama/kumeleme/siralama icin saf Python
enlem/boylam degerlerine ihtiyac duyar) ayni fonksiyonlari kullanir.
"""

from __future__ import annotations

from geoalchemy2 import Geometry
from sqlalchemy import cast, func
from sqlalchemy.orm import Session

from sunucu.veritabani.modeller import Yer


def _koordinat_kolonlari() -> tuple:
    """`Yer.konum` (geography) sutunundan enlem/boylam'i ayri sutunlar
    olarak cikarir. `ST_X`/`ST_Y` geography degil geometry bekledigi icin
    once `geometry`'e cast edilir (WGS84/SRID 4326 korunur)."""
    return (
        func.ST_Y(cast(Yer.konum, Geometry)).label("enlem"),
        func.ST_X(cast(Yer.konum, Geometry)).label("boylam"),
    )


def yer_ve_koordinat_getir(oturum: Session, yer_id: str) -> tuple[Yer, float, float] | None:
    enlem_kolonu, boylam_kolonu = _koordinat_kolonlari()
    sonuc = oturum.query(Yer, enlem_kolonu, boylam_kolonu).filter(Yer.id == yer_id).first()
    if sonuc is None:
        return None
    yer, enlem, boylam = sonuc
    return yer, float(enlem), float(boylam)


def sehir_yerlerini_getir(
    oturum: Session,
    sehir_id: str,
    ana_kategoriler: list[str] | None = None,
    alt_kategoriler: list[str] | None = None,
) -> list[tuple[Yer, float, float]]:
    """Bir sehirdeki yerleri, her biri icin (Yer, enlem, boylam) uclusu
    olarak dondurur. `ana_kategoriler`/`alt_kategoriler` verilirse filtrelenir
    (yerler_router.py filtreleme icin, rota_olusturucu.py aday secimi icin
    kullanir)."""
    enlem_kolonu, boylam_kolonu = _koordinat_kolonlari()
    sorgu = oturum.query(Yer, enlem_kolonu, boylam_kolonu).filter(Yer.sehir_id == sehir_id)
    if ana_kategoriler:
        sorgu = sorgu.filter(Yer.ana_kategori.in_(ana_kategoriler))
    if alt_kategoriler:
        sorgu = sorgu.filter(Yer.alt_kategori.in_(alt_kategoriler))
    return [(yer, float(enlem), float(boylam)) for yer, enlem, boylam in sorgu.all()]
