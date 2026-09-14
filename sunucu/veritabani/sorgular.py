"""
Yer sorgulari icin ortak yardimcilar.

Ozellikle PostGIS `Geography` alanindan (enlem, boylam) cikarma mantigi
burada TEK bir yerde toplanir -- hem `sunucu/api` (yer listeleme/detay)
hem `sunucu/rota_motoru` (skorlama/kumeleme/siralama icin saf Python
enlem/boylam degerlerine ihtiyac duyar) ayni fonksiyonlari kullanir.
"""

from __future__ import annotations

from geoalchemy2 import Geometry
from sqlalchemy import and_, func, or_
from sqlalchemy.orm import Query, Session

from ortak.sabitler import AnaKategori, OzelEtiket
from sunucu.veritabani.modeller import Yer
from sunucu.veritabani.yayin_modelleri import YayinKaydi
from sunucu.yayin.domain import KullanimTuru
from sunucu.yayin.servis import KAMUSAL_DURUMLAR

# Taksonomide duygu_skoru_ortalama -1..+1. Vitrin esigi 80/100:
# (skor + 1) * 50 >= 80  <=>  skor >= 0.6
_KESIF_DUYGU_YUZDE_ESIGI = 80.0
_VITRIN_ETIKETLERI = (
    OzelEtiket.SEHRIN_KLASIGI.value,
    OzelEtiket.KAHVALTI_VERIR.value,
)


def _koordinat_kolonlari() -> tuple:
    """`Yer.konum` (geography) sutunundan enlem/boylam'i ayri sutunlar
    olarak cikarir. `ST_X`/`ST_Y` geography degil geometry bekledigi icin
    once `geometry`'e cast edilir (WGS84/SRID 4326 korunur)."""
    from sqlalchemy import cast

    return (
        func.ST_Y(cast(Yer.konum, Geometry)).label("enlem"),
        func.ST_X(cast(Yer.konum, Geometry)).label("boylam"),
    )


def _ozellik_etiketi_kosulu(anahtar: str):
    """JSONB `ozellikler` icinde etiket true/evet/1 ise eslesir."""
    metin = func.lower(Yer.ozellikler[anahtar].as_string())
    return or_(
        Yer.ozellikler.contains({anahtar: True}),
        metin.in_(("true", "evet", "1")),
    )


def _kesif_vitrin_kosulu():
    """Keşif vitrini: konaklama yok; yeme-icme sadece etiketli veya
    yuksek duygulu; gezilecek_yer kisitsiz."""
    yeme_icme_vitrin = and_(
        Yer.ana_kategori == AnaKategori.YEME_ICME.value,
        or_(
            *[_ozellik_etiketi_kosulu(etiket) for etiket in _VITRIN_ETIKETLERI],
            (Yer.duygu_skoru_ortalama + 1.0) * 50.0 >= _KESIF_DUYGU_YUZDE_ESIGI,
        ),
    )
    return or_(
        Yer.ana_kategori == AnaKategori.GEZILECEK_YER.value,
        yeme_icme_vitrin,
    )


def _kamusal_yayin_kosullari(kullanim: KullanimTuru) -> tuple:
    return (
        YayinKaydi.nesne_turu == "yer",
        YayinKaydi.nesne_id == Yer.id,
        YayinKaydi.aktif_mi.is_(True),
        YayinKaydi.durum.in_(KAMUSAL_DURUMLAR),
        YayinKaydi.izinli_kullanimlar.contains([kullanim.value]),
    )


def _kamusal_yer_listesi_sorgusu(
    oturum: Session,
    sehir_id: str,
    ana_kategoriler: list[str] | None = None,
    alt_kategoriler: list[str] | None = None,
    sadece_kesif: bool = False,
    kullanim: KullanimTuru = KullanimTuru.LISTE,
) -> Query:
    enlem_kolonu, boylam_kolonu = _koordinat_kolonlari()
    sorgu = (
        oturum.query(Yer, enlem_kolonu, boylam_kolonu)
        .join(YayinKaydi, and_(YayinKaydi.nesne_id == Yer.id, YayinKaydi.nesne_turu == "yer"))
        .filter(Yer.sehir_id == sehir_id, *_kamusal_yayin_kosullari(kullanim))
    )
    if ana_kategoriler:
        sorgu = sorgu.filter(Yer.ana_kategori.in_(ana_kategoriler))
    if alt_kategoriler:
        sorgu = sorgu.filter(Yer.alt_kategori.in_(alt_kategoriler))
    if sadece_kesif:
        sorgu = sorgu.filter(_kesif_vitrin_kosulu())
    return sorgu.order_by(Yer.isim)


def sehir_yer_sayilari(oturum: Session, sehir_id: str) -> tuple[int, int, int]:
    """(toplam yer, kesif vitrinindeki yer, farkli ilce) uclusu."""
    taban = oturum.query(func.count(Yer.id)).join(YayinKaydi, and_(YayinKaydi.nesne_id == Yer.id, YayinKaydi.nesne_turu == "yer"))
    toplam = int(taban.filter(Yer.sehir_id == sehir_id, *_kamusal_yayin_kosullari(KullanimTuru.LISTE)).scalar() or 0)
    kesif = int(
        oturum.query(func.count(Yer.id)).join(YayinKaydi, and_(YayinKaydi.nesne_id == Yer.id, YayinKaydi.nesne_turu == "yer"))
        .filter(Yer.sehir_id == sehir_id, _kesif_vitrin_kosulu(), *_kamusal_yayin_kosullari(KullanimTuru.KESFET))
        .scalar()
        or 0
    )
    ilce = int(
        oturum.query(func.count(func.distinct(Yer.ilce))).join(YayinKaydi, and_(YayinKaydi.nesne_id == Yer.id, YayinKaydi.nesne_turu == "yer"))
        .filter(Yer.sehir_id == sehir_id, Yer.ilce.isnot(None), Yer.ilce != "", *_kamusal_yayin_kosullari(KullanimTuru.LISTE))
        .scalar()
        or 0
    )
    return toplam, kesif, ilce


def yer_ve_koordinat_getir(oturum: Session, yer_id: str, *, kullanim: KullanimTuru = KullanimTuru.DETAY) -> tuple[Yer, float, float] | None:
    enlem_kolonu, boylam_kolonu = _koordinat_kolonlari()
    sonuc = (
        oturum.query(Yer, enlem_kolonu, boylam_kolonu)
        .join(YayinKaydi, and_(YayinKaydi.nesne_id == Yer.id, YayinKaydi.nesne_turu == "yer"))
        .filter(Yer.id == yer_id, *_kamusal_yayin_kosullari(kullanim))
        .first()
    )
    if sonuc is None:
        return None
    yer, enlem, boylam = sonuc
    return yer, float(enlem), float(boylam)


def sehir_yerlerini_getir(
    oturum: Session,
    sehir_id: str,
    ana_kategoriler: list[str] | None = None,
    alt_kategoriler: list[str] | None = None,
    *,
    sadece_kesif: bool = False,
) -> list[tuple[Yer, float, float]]:
    """Bir sehirdeki yerleri, her biri icin (Yer, enlem, boylam) uclusu
    olarak dondurur. Rota motoru `sadece_kesif=False` (varsayilan) ile
    kisitlamasiz ceker; API vitrini `sadece_kesif=True` kullanir."""
    sorgu = _kamusal_yer_listesi_sorgusu(oturum, sehir_id, ana_kategoriler, alt_kategoriler, sadece_kesif, KullanimTuru.ROTA_ADAYI)
    return [(yer, float(enlem), float(boylam)) for yer, enlem, boylam in sorgu.all()]


def sehir_yerlerini_sayfa_getir(
    oturum: Session,
    sehir_id: str,
    ana_kategoriler: list[str] | None = None,
    alt_kategoriler: list[str] | None = None,
    *,
    sadece_kesif: bool = True,
    limit: int = 50,
    offset: int = 0,
) -> tuple[list[tuple[Yer, float, float]], int]:
    """Filtrelenmis kume uzerinde sayfalama. `toplam_sayi` filtre SONRASI adettir."""
    sayim_sorgusu = (
        oturum.query(func.count(Yer.id))
        .join(YayinKaydi, and_(YayinKaydi.nesne_id == Yer.id, YayinKaydi.nesne_turu == "yer"))
        .filter(Yer.sehir_id == sehir_id, *_kamusal_yayin_kosullari(KullanimTuru.LISTE))
    )
    if ana_kategoriler:
        sayim_sorgusu = sayim_sorgusu.filter(Yer.ana_kategori.in_(ana_kategoriler))
    if alt_kategoriler:
        sayim_sorgusu = sayim_sorgusu.filter(Yer.alt_kategori.in_(alt_kategoriler))
    if sadece_kesif:
        sayim_sorgusu = sayim_sorgusu.filter(_kesif_vitrin_kosulu())
    toplam_sayi = int(sayim_sorgusu.scalar() or 0)

    sorgu = _kamusal_yer_listesi_sorgusu(oturum, sehir_id, ana_kategoriler, alt_kategoriler, sadece_kesif, KullanimTuru.LISTE)
    satirlar = sorgu.offset(offset).limit(limit).all()
    return [(yer, float(enlem), float(boylam)) for yer, enlem, boylam in satirlar], toplam_sayi


def yer_yayin_kaydi_getir(oturum: Session, yer_id: str) -> YayinKaydi | None:
    """410/ETag gibi kamusal protokol kararlarinda kullanilir; ham Yer dondurmez."""
    return oturum.query(YayinKaydi).filter_by(nesne_turu="yer", nesne_id=yer_id, aktif_mi=True).first()
