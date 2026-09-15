"""Akilli Rota oncesi pilot mekan havuzu. Sayi keyfi doldurulmaz."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Any

from geoalchemy2 import Geometry
from ortak.sabitler import (
    ALT_KATEGORI_AMAC_ESLEMESI,
    ROTA_AMAC_HAVUZLARI,
    OzelEtiket,
    YemeIcmeAltKategori,
)
from sqlalchemy import and_, cast, func
from sqlalchemy.orm import Session

from sunucu.kimlik.kalite import isim_gecerli_mi, oneriye_uygun_mu
from sunucu.veritabani.arama_modelleri import Ilce
from sunucu.veritabani.bilgi_modelleri import DahiliSinyalOzeti, Iddia, IddiaSurumu
from sunucu.veritabani.kimlik_modelleri import Sube
from sunucu.veritabani.modeller import Sehir, Yer

_ATLANAN_ALT = frozenset(
    {
        YemeIcmeAltKategori.INTERNET_KAFE.value,
        "otel",
        "pansiyon_apart",
        "kamp_karavan",
        "hostel",
        "ev_kiralama",
    }
)
_OSM_ANAHTAR = {
    "opening_hours": "calisma_saatleri",
    "wifi": "wifi",
    "internet_access": "wifi",
    "otopark": "otopark",
    "parking": "otopark",
    "acik_alan": "acik_alan",
    "outdoor_seating": "acik_alan",
    "engelli_erisimi": "tekerlekli_sandalye_erisimi",
    "wheelchair": "tekerlekli_sandalye_erisimi",
    "rezervasyon_gerekli": "rezervasyon",
    "reservation": "rezervasyon",
}
_AMAC_KOTA = 18
_ILCE_KOTA = 24
_HAVUZ_UST = 150
_HAVUZ_ALT_HEDEF = 50
_KALITE_TABAN = 70
_GOLD_UST = 40


@dataclass(frozen=True)
class PilotAday:
    sube_id: str
    yer_id: str
    isim: str
    alt_kategori: str
    ilce_id: str | None
    ilce_adi: str | None
    kimlik_sinifi: str
    puan: int
    amac: str | None
    osm_aileleri: tuple[str, ...]
    nlp_preference: int
    public_claim: int
    kahvalti: bool
    calisma: bool
    koordinat_gecerli: bool


def kategori_amaci(alt_kategori: str | None) -> str | None:
    if not alt_kategori:
        return None
    amaclar = ALT_KATEGORI_AMAC_ESLEMESI.get(alt_kategori)
    if not amaclar:
        return None
    return amaclar[0]


def osm_ailelerini_cek(ozellikler: dict[str, Any] | None) -> tuple[str, ...]:
    oz = ozellikler or {}
    aileler: list[str] = []
    for anahtar, aile in _OSM_ANAHTAR.items():
        if oz.get(anahtar) not in (None, "", [], {}):
            if aile not in aileler:
                aileler.append(aile)
    return tuple(aileler)


def aday_puani(
    *,
    kimlik_sinifi: str,
    ilce_var: bool,
    osm_sayisi: int,
    nlp_preference: int,
    public_claim: int,
    saat_var: bool,
) -> int:
    puan = {"dogrulanmis": 120, "guclu": 100, "kullanilabilir": 40}.get(kimlik_sinifi, 0)
    if ilce_var:
        puan += 20
    puan += min(40, osm_sayisi * 8)
    puan += min(30, nlp_preference * 6)
    puan += min(45, public_claim * 15)
    if saat_var:
        puan += 25
    return puan


def kaliteli_mi(aday: PilotAday) -> bool:
    if not oneriye_uygun_mu(aday.kimlik_sinifi) or not aday.koordinat_gecerli:
        return False
    if not isim_gecerli_mi(aday.isim):
        return False
    if aday.alt_kategori in _ATLANAN_ALT:
        return False
    if aday.puan < _KALITE_TABAN:
        return False
    return bool(
        aday.osm_aileleri
        or aday.nlp_preference
        or aday.public_claim
        or aday.kimlik_sinifi in {"guclu", "dogrulanmis"}
    )


def havuzu_sec(adaylar: list[PilotAday]) -> list[PilotAday]:
    uygun = [a for a in adaylar if kaliteli_mi(a)]
    uygun.sort(key=lambda a: (-a.puan, a.ilce_adi or "", a.isim))
    secilen: list[PilotAday] = []
    amac_say = defaultdict(int)
    ilce_say = defaultdict(int)
    alinan: set[str] = set()

    kabul_amac: set[str] = set()

    def _al(aday: PilotAday, amac: str | None) -> None:
        if aday.sube_id in alinan:
            return
        if len(secilen) >= _HAVUZ_UST:
            return
        ilce_anahtar = aday.ilce_adi or "_yok"
        if ilce_say[ilce_anahtar] >= _ILCE_KOTA:
            return
        if amac and amac_say[amac] >= _AMAC_KOTA:
            return
        secilen.append(aday)
        alinan.add(aday.sube_id)
        ilce_say[ilce_anahtar] += 1
        if amac:
            amac_say[amac] += 1
            kabul_amac.add(amac)

    for amac, _alts in ROTA_AMAC_HAVUZLARI.items():
        kova = [a for a in uygun if a.amac == amac]
        if len(kova) < 4 and not any(a.puan >= 120 for a in kova):
            continue
        for aday in kova:
            _al(aday, amac)
    kahvalti = [a for a in uygun if a.kahvalti]
    if len(kahvalti) >= 3:
        for aday in kahvalti:
            _al(aday, "kahvalti")
    calisma = [a for a in uygun if a.calisma]
    if len(calisma) >= 3:
        for aday in calisma:
            _al(aday, "calisma")
    if len(secilen) < _HAVUZ_ALT_HEDEF:
        for aday in uygun:
            if len(secilen) >= _HAVUZ_ALT_HEDEF:
                break
            if aday.amac in ROTA_AMAC_HAVUZLARI and aday.amac not in kabul_amac:
                continue
            _al(aday, aday.amac)
    return secilen


def gold_sec(havuz: list[PilotAday]) -> list[PilotAday]:
    yapisal = {"calisma_saatleri", "wifi", "acik_alan", "otopark", "rezervasyon"}
    adaylar = [
        a
        for a in havuz
        if a.kimlik_sinifi in {"guclu", "dogrulanmis"} and set(a.osm_aileleri) & yapisal
    ]
    adaylar.sort(key=lambda a: (-a.puan, a.isim))
    return adaylar[:_GOLD_UST]


def sehir_idsini_bul(oturum: Session, sehir_adi: str) -> str:
    sehir = oturum.query(Sehir).filter(Sehir.isim.ilike(sehir_adi.strip())).first()
    if sehir is None:
        raise ValueError(f"Sehir bulunamadi: {sehir_adi}")
    return sehir.id


def veritabanindan_adaylar(oturum: Session, sehir_id: str) -> list[PilotAday]:
    enlem = func.ST_Y(cast(Yer.konum, Geometry))
    boylam = func.ST_X(cast(Yer.konum, Geometry))
    satirlar = (
        oturum.query(Sube, Yer, Ilce, enlem, boylam)
        .join(Yer, Yer.id == Sube.legacy_yer_id)
        .outerjoin(Ilce, Ilce.id == Yer.ilce_id)
        .filter(Yer.sehir_id == sehir_id, Sube.durum == "aktif")
        .all()
    )
    claimler: dict[str, dict[str, str]] = defaultdict(dict)
    for iddia, surum in (
        oturum.query(Iddia, IddiaSurumu)
        .join(
            IddiaSurumu,
            and_(IddiaSurumu.iddia_id == Iddia.id, IddiaSurumu.surum_no == Iddia.aktif_surum_no),
        )
        .join(Sube, Sube.id == Iddia.sube_id)
        .join(Yer, Yer.id == Sube.legacy_yer_id)
        .filter(Yer.sehir_id == sehir_id)
    ):
        claimler[iddia.sube_id][iddia.aile] = surum.yayin_durumu
    nlp: dict[str, int] = defaultdict(int)
    nlp_aile: dict[str, set[str]] = defaultdict(set)
    for ozet in (
        oturum.query(DahiliSinyalOzeti)
        .join(Sube, Sube.id == DahiliSinyalOzeti.sube_id)
        .join(Yer, Yer.id == Sube.legacy_yer_id)
        .filter(Yer.sehir_id == sehir_id)
    ):
        govde = dict(ozet.ozet or {})
        if govde.get("preference_eligible"):
            nlp[ozet.sube_id] += 1
            nlp_aile[ozet.sube_id].add(ozet.aile)
    adaylar: list[PilotAday] = []
    for sube, yer, ilce, _enlem, _boylam in satirlar:
        osm = osm_ailelerini_cek(yer.ozellikler)
        public = sum(
            1 for durum in claimler.get(sube.id, {}).values() if durum in {"yayinlandi", "sinirli"}
        )
        kahvalti = bool((yer.ozellikler or {}).get(OzelEtiket.KAHVALTI_VERIR.value)) or (
            "kahvalti" in nlp_aile.get(sube.id, set())
        )
        calisma = "calisma_uygunlugu" in nlp_aile.get(sube.id, set())
        puan = aday_puani(
            kimlik_sinifi=sube.kimlik_kalite_sinifi,
            ilce_var=bool(yer.ilce_id),
            osm_sayisi=len(osm),
            nlp_preference=nlp.get(sube.id, 0),
            public_claim=public,
            saat_var="calisma_saatleri" in osm,
        )
        kirilim = dict(sube.kimlik_kalite_kirilim or {})
        bayraklar = kirilim.get("bayraklar") or []
        koordinat_gecerli = (
            "koordinat_gecersiz" not in bayraklar and "sehir_disi_koordinat" not in bayraklar
        )
        adaylar.append(
            PilotAday(
                sube_id=sube.id,
                yer_id=yer.id,
                isim=yer.isim,
                alt_kategori=yer.alt_kategori,
                ilce_id=yer.ilce_id,
                ilce_adi=ilce.isim if ilce is not None else yer.ilce,
                kimlik_sinifi=sube.kimlik_kalite_sinifi,
                puan=puan,
                amac=kategori_amaci(yer.alt_kategori),
                osm_aileleri=osm,
                nlp_preference=nlp.get(sube.id, 0),
                public_claim=public,
                kahvalti=kahvalti,
                calisma=calisma,
                koordinat_gecerli=koordinat_gecerli,
            )
        )
    return adaylar


def havuz_ozeti(havuz: list[PilotAday]) -> dict[str, Any]:
    amac = defaultdict(int)
    ilce = defaultdict(int)
    kimlik = defaultdict(int)
    for aday in havuz:
        amac[aday.amac or "amacsiz"] += 1
        ilce[aday.ilce_adi or "ilcesiz"] += 1
        kimlik[aday.kimlik_sinifi] += 1
    return {
        "sayi": len(havuz),
        "amac": dict(amac),
        "ilce": dict(ilce),
        "kimlik": dict(kimlik),
        "osm_en_az_bir": sum(1 for a in havuz if a.osm_aileleri),
        "nlp_preference": sum(1 for a in havuz if a.nlp_preference),
        "public_claim": sum(1 for a in havuz if a.public_claim),
    }
