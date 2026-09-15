"""Ziyaret suresi kaynaklarini ayirir; kategori sezgiseli fact degildir."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ortak.sabitler import ZiyaretSuresiKaynagi

# Planner yedegi. Fact gibi sunulmaz; rota motoru bu fazda yazilmaz.
# Degerler mevcut tarihsel zaman_butcesi tablosuyla hizalidir.
KATEGORI_ZIYARET_SURESI_SEZGISEL_DK: dict[str, int] = {
    "tarihi_kulturel": 60,
    "doga_manzara": 45,
    "plaj_su": 90,
    "eglence_aktivite": 90,
    "gece_hayati": 90,
    "alisveris": 45,
    "spor_doga_yuruyus": 90,
    "dini_manevi": 30,
    "fotograf_noktasi": 20,
    "restoran_lokanta": 60,
    "deniz_mahsulleri": 60,
    "kebap_izgara": 60,
    "ev_yemekleri_esnaf": 60,
    "fine_dining_romantik": 90,
    "sokak_lezzeti": 20,
    "kafe": 45,
    "tatli_pastane": 30,
    "kahve_uzmanlik": 45,
    "meyhane_bar": 90,
    "cay_bahcesi": 45,
}


@dataclass(frozen=True)
class ZiyaretSuresiOzeti:
    kaynak: ZiyaretSuresiKaynagi
    dakika: int | None
    fact_mi: bool
    kirilim: dict[str, Any]

    def sozluk(self) -> dict[str, Any]:
        return {
            "kaynak": self.kaynak.value,
            "dakika": self.dakika,
            "fact_mi": self.fact_mi,
            "kirilim": dict(self.kirilim),
        }


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
            kirilim={"neden": "kullanici_secimi", "planner_yedegi": False},
        )
    if dogrulanmis_dakika is not None and dogrulanmis_dakika > 0:
        return ZiyaretSuresiOzeti(
            kaynak=ZiyaretSuresiKaynagi.BILINEN_DOGRULANMIS,
            dakika=dogrulanmis_dakika,
            fact_mi=True,
            kirilim={"neden": "yayimlanmis_sure_iddiasi"},
        )
    sezgisel = KATEGORI_ZIYARET_SURESI_SEZGISEL_DK.get(alt_kategori or "")
    if sezgisel:
        return ZiyaretSuresiOzeti(
            kaynak=ZiyaretSuresiKaynagi.KATEGORI_SEZGISEL,
            dakika=sezgisel,
            fact_mi=False,
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
