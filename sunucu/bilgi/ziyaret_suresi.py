"""Ziyaret suresi kaynaklarini ayirir; kategori tahmini fact degildir."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ortak.sabitler import ZiyaretSuresiKaynagi

# Planner yedegi. Fact gibi sunulmaz; rota motoru bu fazda yazilmaz.
# (minimum, tipik, maksimum) dakika.
PLANLAMA_TAHMINI_ARALIK_DK: dict[str, tuple[int, int, int]] = {
    "tarihi_kulturel": (45, 60, 90),
    "doga_manzara": (30, 45, 75),
    "plaj_su": (60, 90, 150),
    "eglence_aktivite": (60, 90, 150),
    "gece_hayati": (60, 90, 150),
    "alisveris": (30, 45, 75),
    "spor_doga_yuruyus": (60, 90, 150),
    "dini_manevi": (20, 30, 45),
    "fotograf_noktasi": (15, 20, 30),
    "restoran_lokanta": (45, 60, 90),
    "deniz_mahsulleri": (45, 60, 90),
    "kebap_izgara": (45, 60, 90),
    "ev_yemekleri_esnaf": (45, 60, 90),
    "fine_dining_romantik": (60, 90, 150),
    "sokak_lezzeti": (15, 20, 30),
    "kafe": (30, 45, 75),
    "tatli_pastane": (20, 30, 45),
    "kahve_uzmanlik": (30, 45, 75),
    "meyhane_bar": (60, 90, 150),
    "cay_bahcesi": (30, 45, 75),
}


@dataclass(frozen=True)
class ZiyaretSuresiOzeti:
    kaynak: ZiyaretSuresiKaynagi
    dakika: int | None
    fact_mi: bool
    kirilim: dict[str, Any]
    minimum_dk: int | None = None
    tipik_dk: int | None = None
    maksimum_dk: int | None = None
    kullanici_ifadesi: str | None = None

    def sozluk(self) -> dict[str, Any]:
        return {
            "kaynak": self.kaynak.value,
            "dakika": self.dakika,
            "fact_mi": self.fact_mi,
            "minimum_dk": self.minimum_dk,
            "tipik_dk": self.tipik_dk,
            "maksimum_dk": self.maksimum_dk,
            "kullanici_ifadesi": self.kullanici_ifadesi,
            "kirilim": dict(self.kirilim),
        }


def _tahmin_ifadesi(minimum_dk: int, maksimum_dk: int) -> str:
    return f"Planlama icin yaklasik {minimum_dk}–{maksimum_dk} dakika ayirdik"


def ziyaret_suresini_coz(
    *,
    dogrulanmis_dakika: int | None = None,
    alt_kategori: str | None = None,
    kullanici_dakika: int | None = None,
) -> ZiyaretSuresiOzeti:
    if kullanici_dakika is not None and kullanici_dakika > 0:
        return ZiyaretSuresiOzeti(
            kaynak=ZiyaretSuresiKaynagi.KULLANICI_SECIMI,
            dakika=kullanici_dakika,
            fact_mi=False,
            minimum_dk=kullanici_dakika,
            tipik_dk=kullanici_dakika,
            maksimum_dk=kullanici_dakika,
            kullanici_ifadesi=None,
            kirilim={"neden": "kullanici_secimi", "planner_yedegi": False},
        )
    if dogrulanmis_dakika is not None and dogrulanmis_dakika > 0:
        return ZiyaretSuresiOzeti(
            kaynak=ZiyaretSuresiKaynagi.DOGRULANMIS_SURE,
            dakika=dogrulanmis_dakika,
            fact_mi=True,
            minimum_dk=dogrulanmis_dakika,
            tipik_dk=dogrulanmis_dakika,
            maksimum_dk=dogrulanmis_dakika,
            kullanici_ifadesi=None,
            kirilim={"neden": "yayimlanmis_sure_iddiasi"},
        )
    aralik = PLANLAMA_TAHMINI_ARALIK_DK.get(alt_kategori or "")
    if aralik:
        minimum_dk, tipik_dk, maksimum_dk = aralik
        return ZiyaretSuresiOzeti(
            kaynak=ZiyaretSuresiKaynagi.PLANLAMA_TAHMINI,
            dakika=tipik_dk,
            fact_mi=False,
            minimum_dk=minimum_dk,
            tipik_dk=tipik_dk,
            maksimum_dk=maksimum_dk,
            kullanici_ifadesi=_tahmin_ifadesi(minimum_dk, maksimum_dk),
            kirilim={
                "neden": "kategori_planner_yedegi",
                "alt_kategori": alt_kategori,
                "fact_gibi_sunulmaz": True,
            },
        )
    return ZiyaretSuresiOzeti(
        kaynak=ZiyaretSuresiKaynagi.BILINMIYOR,
        dakika=None,
        fact_mi=False,
        kirilim={"neden": "sure_yok"},
    )
