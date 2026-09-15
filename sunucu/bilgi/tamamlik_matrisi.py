"""Pilot tamamlik matrisi: known/unknown/stale/conflicting/internal-only."""

from __future__ import annotations

from dataclasses import dataclass

from ortak.sabitler import AmacEslemeSeviyesi, TamamlikHucresi, amac_esleme_seviyesi

MATRIS_KOLONLARI = (
    "kimlik",
    "ilce",
    "koordinat",
    "amac",
    "calisma_saatleri",
    "ziyaret_suresi",
    "wifi",
    "otopark",
    "acik_alan",
    "erisilebilirlik",
    "aile",
    "cocuk",
    "calisma",
    "sessizlik",
    "manzara",
    "fiyat",
    "guncellik",
)

_CLAIM_KOLON = {
    "calisma_saatleri": "calisma_saatleri",
    "wifi": "wifi",
    "otopark": "otopark",
    "acik_alan": "acik_alan",
    "erisilebilirlik": "tekerlekli_sandalye_erisimi",
    "fiyat": "fiyat",
    "ziyaret_suresi": "ziyaret_suresi",
}
_NLP_KOLON = {
    "aile": "aile_uygunlugu",
    "cocuk": "cocuk_uygunlugu",
    "calisma": "calisma_uygunlugu",
    "sessizlik": "sessiz_ortam",
    "manzara": "manzara",
    "fiyat": "fiyat_algisi",
    "wifi": "wifi",
    "otopark": "otopark",
    "acik_alan": "acik_alan",
}


@dataclass(frozen=True)
class AlanKaniti:
    yayin_durumu: str | None = None
    bilgi_durumu: str | None = None
    osm_var: bool = False
    nlp_var: bool = False


def hucreyi_coz(kanit: AlanKaniti) -> TamamlikHucresi:
    durum = kanit.bilgi_durumu or ""
    yayin = kanit.yayin_durumu or ""
    if durum == "celiskili":
        return TamamlikHucresi.CELISKILI
    if durum == "eskimis" and yayin in {"yayinlandi", "sinirli", "yeniden_dogrulama"}:
        return TamamlikHucresi.ESKIMIS
    if yayin in {"yayinlandi", "sinirli"} and durum == "biliniyor":
        return TamamlikHucresi.BILINIYOR
    if kanit.osm_var or kanit.nlp_var:
        return TamamlikHucresi.YALNIZ_DAHILI
    return TamamlikHucresi.BILINMIYOR


def kimlik_hucresi(sinif: str, isim_gecerli: bool) -> TamamlikHucresi:
    if not isim_gecerli or sinif == "karantina":
        return TamamlikHucresi.CELISKILI
    if sinif == "supheli":
        return TamamlikHucresi.CELISKILI
    if sinif in {"dogrulanmis", "guclu", "kullanilabilir"}:
        return TamamlikHucresi.BILINIYOR
    return TamamlikHucresi.BILINMIYOR


def amac_hucresi(alt_kategori: str | None, amaclar: tuple[str, ...]) -> TamamlikHucresi:
    if any(
        amac_esleme_seviyesi(alt_kategori, amac) is AmacEslemeSeviyesi.DIRECT_PURPOSE_FACT
        for amac in amaclar
    ):
        return TamamlikHucresi.BILINIYOR
    if amaclar:
        return TamamlikHucresi.YALNIZ_DAHILI
    return TamamlikHucresi.BILINMIYOR


def guncellik_hucresi(claimler: list[AlanKaniti]) -> TamamlikHucresi:
    if any((k.bilgi_durumu == "celiskili") for k in claimler):
        return TamamlikHucresi.CELISKILI
    if any((k.bilgi_durumu == "eskimis") for k in claimler):
        return TamamlikHucresi.ESKIMIS
    if any(
        (k.yayin_durumu in {"yayinlandi", "sinirli"} and k.bilgi_durumu == "biliniyor")
        for k in claimler
    ):
        return TamamlikHucresi.BILINIYOR
    if any(k.osm_var or k.nlp_var for k in claimler):
        return TamamlikHucresi.YALNIZ_DAHILI
    return TamamlikHucresi.BILINMIYOR


def matris_satirini_kur(
    *,
    kimlik_sinifi: str,
    isim_gecerli: bool,
    ilce_id: str | None,
    koordinat_gecerli: bool,
    alt_kategori: str | None,
    amaclar: tuple[str, ...],
    claimler: dict[str, AlanKaniti],
    nlp: dict[str, bool],
    osm: dict[str, bool],
) -> dict[str, str]:
    satir: dict[str, str] = {}
    satir["kimlik"] = kimlik_hucresi(kimlik_sinifi, isim_gecerli).value
    satir["ilce"] = TamamlikHucresi.BILINIYOR.value if ilce_id else TamamlikHucresi.BILINMIYOR.value
    satir["koordinat"] = (
        TamamlikHucresi.BILINIYOR.value if koordinat_gecerli else TamamlikHucresi.BILINMIYOR.value
    )
    satir["amac"] = amac_hucresi(alt_kategori, amaclar).value

    def _kanit(aile: str) -> AlanKaniti:
        mevcut = claimler.get(aile, AlanKaniti())
        return AlanKaniti(
            yayin_durumu=mevcut.yayin_durumu,
            bilgi_durumu=mevcut.bilgi_durumu,
            osm_var=mevcut.osm_var or bool(osm.get(aile)),
            nlp_var=mevcut.nlp_var or bool(nlp.get(aile)),
        )

    for kolon, aile in _CLAIM_KOLON.items():
        satir[kolon] = hucreyi_coz(_kanit(aile)).value
    for kolon, aile in _NLP_KOLON.items():
        if kolon in satir:
            continue
        satir[kolon] = hucreyi_coz(_kanit(aile)).value
    satir["guncellik"] = guncellik_hucresi(
        [_kanit(aile) for aile in {*_CLAIM_KOLON.values(), *_NLP_KOLON.values()}]
    ).value
    return {kolon: satir.get(kolon, TamamlikHucresi.BILINMIYOR.value) for kolon in MATRIS_KOLONLARI}


def eksik_onemli_aileler(satir: dict[str, str]) -> list[str]:
    onemli = (
        "calisma_saatleri",
        "wifi",
        "otopark",
        "acik_alan",
        "erisilebilirlik",
        "aile",
        "cocuk",
        "calisma",
        "sessizlik",
        "manzara",
    )
    return [kolon for kolon in onemli if satir.get(kolon) == TamamlikHucresi.BILINMIYOR.value]
