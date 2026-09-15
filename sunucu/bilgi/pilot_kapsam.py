"""Pilot tamamlik matrisi, NLP kapsami ve rota hazirlik ozeti. Kamusal skor yoktur."""

from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime
from typing import Any

from ortak.sabitler import (
    RotaHazirlikDurumu,
    TamamlikHucresi,
)
from sqlalchemy import and_
from sqlalchemy.orm import Session

from sunucu.bilgi.calisma_saati import (
    calisma_saati_degerini_al,
    calisma_saati_kaydini_kur,
    calisma_saatini_ayristir,
)
from sunucu.bilgi.pilot_havuzu import PilotAday, kategori_amaci
from sunucu.bilgi.rota_bilinmeyen import akilli_rota_go_degerlendirmesi
from sunucu.bilgi.rota_hazirlik import RotaHazirlikGirdisi, rota_hazirligini_hesapla
from sunucu.bilgi.rota_senaryo import senaryo_setini_olc
from sunucu.bilgi.tamamlik_matrisi import (
    MATRIS_KOLONLARI,
    AlanKaniti,
    eksik_onemli_aileler,
    matris_satirini_kur,
)
from sunucu.bilgi.tarihi_neden import tarihi_mekan_nedenleri
from sunucu.bilgi.ziyaret_suresi import ziyaret_suresini_coz
from sunucu.kimlik.kalite import isim_gecerli_mi, oneriye_uygun_mu
from sunucu.veritabani.bilgi_modelleri import DahiliSinyalOzeti, Iddia, IddiaSurumu
from sunucu.veritabani.kimlik_modelleri import Sube

NLP_DENEYIM_AILELERI = (
    "sessiz_ortam",
    "fiyat_algisi",
    "kalabaliklik",
    "manzara",
    "otopark",
    "aile_uygunlugu",
    "cocuk_uygunlugu",
    "acik_alan",
    "calisma_uygunlugu",
    "kahvalti",
    "canli_muzik",
)

_NLP_MATRIS = {
    "aile_uygunlugu": "aile",
    "cocuk_uygunlugu": "cocuk",
    "calisma_uygunlugu": "calisma",
    "sessiz_ortam": "sessizlik",
    "manzara": "manzara",
    "fiyat_algisi": "fiyat",
    "wifi": "wifi",
    "otopark": "otopark",
    "acik_alan": "acik_alan",
}


def _claim_kaniti(
    surum: IddiaSurumu | None,
    *,
    osm_var: bool = False,
    nlp_var: bool = False,
    aile: str = "",
) -> AlanKaniti:
    if surum is None:
        return AlanKaniti(osm_var=osm_var, nlp_var=nlp_var)
    bilgi = surum.bilgi_durumu
    yayin = surum.yayin_durumu
    if aile == "calisma_saatleri":
        ayristirma = calisma_saatini_ayristir(calisma_saati_degerini_al(surum.deger))
        if yayin in {"yayinlandi", "sinirli"} and not ayristirma.sozdizimi_gecerli:
            bilgi = "celiskili"
        elif yayin in {"yayinlandi", "sinirli"} and ayristirma.sozdizimi_gecerli:
            bilgi = "biliniyor"
    return AlanKaniti(
        yayin_durumu=yayin,
        bilgi_durumu=bilgi,
        osm_var=osm_var,
        nlp_var=nlp_var,
    )


def _zaman_al(deger: Any, anahtar: str) -> datetime | None:
    ham = (deger or {}).get(anahtar) if isinstance(deger, dict) else None
    if not ham or not isinstance(ham, str):
        return None
    try:
        return datetime.fromisoformat(ham.replace("Z", "+00:00"))
    except ValueError:
        return None


def _saat_kaydini_claimden(surum: IddiaSurumu):
    deger = surum.deger
    ham = calisma_saati_degerini_al(deger)
    kaynak = "openstreetmap"
    if isinstance(deger, dict) and deger.get("kaynak"):
        kaynak = str(deger.get("kaynak"))
    return calisma_saati_kaydini_kur(
        ham=ham,
        kaynak=kaynak,
        gozlemlenme_zamani=_zaman_al(deger, "gozlemlenme_zamani"),
        cekilme_zamani=_zaman_al(deger, "cekilme_zamani"),
        ham_referans=(deger.get("ham_referans") if isinstance(deger, dict) else None),
        zaman_dilimi=(deger.get("zaman_dilimi") if isinstance(deger, dict) else None),
    )


def _yayimli_sure_dakika(surum: IddiaSurumu | None) -> int | None:
    if surum is None or surum.yayin_durumu not in {"yayinlandi", "sinirli"}:
        return None
    deger = surum.deger
    ham: Any = deger
    if isinstance(deger, dict):
        ham = deger.get("dakika") or deger.get("deger") or deger.get("tipik_dk")
    try:
        dakika = int(ham)
    except (TypeError, ValueError):
        return None
    return dakika if dakika > 0 else None


def _amaclar(alt: str | None, kahvalti: bool, calisma: bool) -> tuple[str, ...]:
    degerler: list[str] = []
    temel = kategori_amaci(alt)
    if temel:
        degerler.append(temel)
    if kahvalti and "kahvalti" not in degerler:
        degerler.append("kahvalti")
    if calisma and "calisma" not in degerler:
        degerler.append("calisma")
    return tuple(degerler)


def mekan_kapsamini_kur(
    *,
    aday: PilotAday,
    sube: Sube,
    claimler: dict[str, IddiaSurumu],
    nlp: dict[str, DahiliSinyalOzeti],
) -> dict[str, Any]:
    osm_aile = set(aday.osm_aileleri)
    osm_bool = {aile: True for aile in osm_aile}
    nlp_bool = {_NLP_MATRIS.get(aile, aile): True for aile in nlp}
    kanitlar: dict[str, AlanKaniti] = {}
    for aile, surum in claimler.items():
        kanitlar[aile] = _claim_kaniti(
            surum,
            osm_var=aile in osm_aile,
            nlp_var=aile in nlp or _NLP_MATRIS.get(aile, "") in nlp_bool,
            aile=aile,
        )
    amaclar = _amaclar(aday.alt_kategori, aday.kahvalti, aday.calisma)
    satir = matris_satirini_kur(
        kimlik_sinifi=aday.kimlik_sinifi,
        isim_gecerli=isim_gecerli_mi(aday.isim),
        ilce_id=aday.ilce_id,
        koordinat_gecerli=aday.koordinat_gecerli,
        alt_kategori=aday.alt_kategori,
        amaclar=amaclar,
        claimler=kanitlar,
        nlp=nlp_bool,
        osm=osm_bool,
    )
    saat_hucre = TamamlikHucresi(satir["calisma_saatleri"])
    saat_kaydi = None
    if "calisma_saatleri" in claimler:
        saat_kaydi = _saat_kaydini_claimden(claimler["calisma_saatleri"])
    hazirlik = rota_hazirligini_hesapla(
        RotaHazirlikGirdisi(
            kimlik_sinifi=aday.kimlik_sinifi,
            sube_durum=sube.durum,
            koordinat_gecerli=aday.koordinat_gecerli,
            ilce_id=aday.ilce_id,
            amaclar=amaclar,
            yayin_uygun=oneriye_uygun_mu(aday.kimlik_sinifi),
            calisma_saati=saat_hucre,
            calisma_saati_durumu=saat_kaydi.durum if saat_kaydi else None,
        )
    )
    sure = ziyaret_suresini_coz(
        dogrulanmis_dakika=_yayimli_sure_dakika(claimler.get("ziyaret_suresi")),
        alt_kategori=aday.alt_kategori,
    )
    nlp_ozet = {
        aile: {
            "guven_sinifi": nlp[aile].guven_sinifi,
            "durum": nlp[aile].durum,
            "preference_eligible": bool((nlp[aile].ozet or {}).get("preference_eligible")),
        }
        for aile in NLP_DENEYIM_AILELERI
        if aile in nlp
    }
    return {
        "sube_id": aday.sube_id,
        "yer_id": aday.yer_id,
        "isim": aday.isim,
        "alt_kategori": aday.alt_kategori,
        "ilce_adi": aday.ilce_adi,
        "kimlik_sinifi": aday.kimlik_sinifi,
        "amaclar": list(amaclar),
        "matris": satir,
        "eksik_onemli_aileler": eksik_onemli_aileler(satir),
        "rota_hazirlik": hazirlik.sozluk(),
        "calisma_saati_durumu": saat_kaydi.durum.value if saat_kaydi else None,
        "ziyaret_suresi": sure.sozluk(),
        "nlp": nlp_ozet,
        "gold_aday": False,
    }


def havuz_kapsamini_kur(
    oturum: Session,
    havuz: list[PilotAday],
    *,
    gold_idleri: set[str] | None = None,
) -> list[dict[str, Any]]:
    if not havuz:
        return []
    sube_idleri = [a.sube_id for a in havuz]
    subeler = {s.id: s for s in oturum.query(Sube).filter(Sube.id.in_(sube_idleri))}
    claimler: dict[str, dict[str, IddiaSurumu]] = defaultdict(dict)
    for iddia, surum in (
        oturum.query(Iddia, IddiaSurumu)
        .join(
            IddiaSurumu,
            and_(IddiaSurumu.iddia_id == Iddia.id, IddiaSurumu.surum_no == Iddia.aktif_surum_no),
        )
        .filter(Iddia.sube_id.in_(sube_idleri))
    ):
        claimler[iddia.sube_id][iddia.aile] = surum
    nlp_map: dict[str, dict[str, DahiliSinyalOzeti]] = defaultdict(dict)
    for ozet in oturum.query(DahiliSinyalOzeti).filter(DahiliSinyalOzeti.sube_id.in_(sube_idleri)):
        nlp_map[ozet.sube_id][ozet.aile] = ozet
    gold = gold_idleri or set()
    satirlar: list[dict[str, Any]] = []
    for aday in havuz:
        kayit = mekan_kapsamini_kur(
            aday=aday,
            sube=subeler[aday.sube_id],
            claimler=claimler.get(aday.sube_id, {}),
            nlp=nlp_map.get(aday.sube_id, {}),
        )
        kayit["gold_aday"] = aday.sube_id in gold
        satirlar.append(kayit)
    return satirlar


def nlp_kapsam_ozeti(satirlar: list[dict[str, Any]]) -> dict[str, Any]:
    aile_say: dict[str, Counter[str]] = {aile: Counter() for aile in NLP_DENEYIM_AILELERI}
    preference = Counter()
    for satir in satirlar:
        nlp = satir.get("nlp") or {}
        for aile in NLP_DENEYIM_AILELERI:
            kayit = nlp.get(aile)
            if not kayit:
                aile_say[aile]["yok"] += 1
                continue
            sinif = kayit.get("guven_sinifi") or "yok"
            aile_say[aile][sinif] += 1
            if kayit.get("preference_eligible"):
                preference[aile] += 1
    return {
        "aile": {aile: dict(sayac) for aile, sayac in aile_say.items()},
        "preference_eligible": dict(preference),
        "mekan_en_az_bir": sum(1 for s in satirlar if s.get("nlp")),
    }


def matris_kolon_ozeti(satirlar: list[dict[str, Any]]) -> dict[str, dict[str, int]]:
    ozet: dict[str, Counter[str]] = {kolon: Counter() for kolon in MATRIS_KOLONLARI}
    for satir in satirlar:
        for kolon, deger in (satir.get("matris") or {}).items():
            ozet[kolon][deger] += 1
    return {kolon: dict(sayac) for kolon, sayac in ozet.items()}


def rota_durum_ozeti(satirlar: list[dict[str, Any]]) -> dict[str, int]:
    sayac: Counter[str] = Counter()
    for satir in satirlar:
        durum = ((satir.get("rota_hazirlik") or {}).get("durum")) or "yok"
        sayac[durum] += 1
    return {
        RotaHazirlikDurumu.ROTA_HAZIR.value: sayac.get(RotaHazirlikDurumu.ROTA_HAZIR.value, 0),
        RotaHazirlikDurumu.ROTA_SINIRLI.value: sayac.get(RotaHazirlikDurumu.ROTA_SINIRLI.value, 0),
        RotaHazirlikDurumu.KESIF_ADAYI.value: sayac.get(RotaHazirlikDurumu.KESIF_ADAYI.value, 0),
        RotaHazirlikDurumu.ROTA_KAPALI.value: sayac.get(RotaHazirlikDurumu.ROTA_KAPALI.value, 0),
    }


def rota_simulasyonu(satirlar: list[dict[str, Any]]) -> dict[str, Any]:
    def _filtre(pred) -> list[dict[str, Any]]:
        return [s for s in satirlar if pred(s)]

    def _durum(adaylar: list[dict[str, Any]]) -> dict[str, int]:
        return rota_durum_ozeti(adaylar)

    amac_sim = {}
    for amac in (
        "kahve_icmek",
        "yemek_yemek",
        "kahvalti",
        "tatli_yemek",
        "tarihi_kulturel_ziyaret",
        "acik_hava",
        "eglence",
        "calisma",
    ):
        kova = _filtre(lambda s, a=amac: a in (s.get("amaclar") or []))
        amac_sim[amac] = {
            "aday": len(kova),
            **_durum(kova),
            "saat_biliniyor": sum(
                1
                for s in kova
                if (s.get("matris") or {}).get("calisma_saatleri")
                == TamamlikHucresi.BILINIYOR.value
            ),
        }
    ilce_sim = {}
    for ilce in sorted({s.get("ilce_adi") or "ilcesiz" for s in satirlar}):
        kova = _filtre(lambda s, i=ilce: (s.get("ilce_adi") or "ilcesiz") == i)
        ilce_sim[ilce] = {"aday": len(kova), **_durum(kova)}
    senaryo_af = senaryo_setini_olc(satirlar)
    return {
        "pilot_toplam": len(satirlar),
        "durum": _durum(satirlar),
        "koordinat_gecerli": sum(
            1
            for s in satirlar
            if (s.get("matris") or {}).get("koordinat") == TamamlikHucresi.BILINIYOR.value
        ),
        "ilce_biliniyor": sum(
            1
            for s in satirlar
            if (s.get("matris") or {}).get("ilce") == TamamlikHucresi.BILINIYOR.value
        ),
        "saat_biliniyor": sum(
            1
            for s in satirlar
            if (s.get("matris") or {}).get("calisma_saatleri") == TamamlikHucresi.BILINIYOR.value
        ),
        "saat_yalniz_dahili": sum(
            1
            for s in satirlar
            if (s.get("matris") or {}).get("calisma_saatleri")
            == TamamlikHucresi.YALNIZ_DAHILI.value
        ),
        "amac": amac_sim,
        "ilce": ilce_sim,
        "senaryo": {
            "kahve_yemek_tarih": _durum(
                _filtre(
                    lambda s: bool(
                        set(s.get("amaclar") or {})
                        & {"kahve_icmek", "yemek_yemek", "tarihi_kulturel_ziyaret"}
                    )
                )
            ),
        },
        "senaryo_af": senaryo_af,
        "go": akilli_rota_go_degerlendirmesi(
            {
                **senaryo_af,
                "desteklenen_amaclar": (
                    "kahve_icmek",
                    "yemek_yemek",
                    "tarihi_kulturel_ziyaret",
                    "acik_hava",
                    "tatli_yemek",
                ),
                "desteklenmeyen_amaclar": ("kahvalti", "calisma"),
            }
        ),
    }


def saat_durum_ozeti(satirlar: list[dict[str, Any]]) -> dict[str, int]:
    sayac: Counter[str] = Counter()
    for satir in satirlar:
        sayac[satir.get("calisma_saati_durumu") or "yok"] += 1
    return dict(sayac)


def sure_kaynak_ozeti(satirlar: list[dict[str, Any]]) -> dict[str, int]:
    sayac: Counter[str] = Counter()
    fact = 0
    for satir in satirlar:
        sure = satir.get("ziyaret_suresi") or {}
        sayac[sure.get("kaynak") or "yok"] += 1
        if sure.get("fact_mi"):
            fact += 1
    sayac["fact_olan"] = fact
    return dict(sayac)


def tarihi_neden_ozeti(satirlar: list[dict[str, Any]]) -> dict[str, Any]:
    kova = [
        s for s in satirlar if "tarihi_kulturel_ziyaret" in (s.get("amaclar") or [])
    ]
    neden_say: Counter[str] = Counter()
    kayitlar = []
    for satir in kova:
        nedenler = tarihi_mekan_nedenleri(satir)
        for neden in nedenler:
            neden_say[neden] += 1
        kayitlar.append(
            {
                "isim": satir.get("isim"),
                "ilce_adi": satir.get("ilce_adi"),
                "rota_hazirlik": (satir.get("rota_hazirlik") or {}).get("durum"),
                "nedenler": list(nedenler),
            }
        )
    return {
        "adet": len(kova),
        "neden": dict(neden_say),
        "rota": rota_durum_ozeti(kova),
        "kayitlar": kayitlar,
    }


def kuyruk_sayimi(oturum: Session) -> dict[str, int]:
    from sunucu.veritabani.admin_modelleri import IncelemeDosyasi

    bekleyen = (
        oturum.query(IncelemeDosyasi)
        .filter(
            IncelemeDosyasi.durum != "tamamlandi", IncelemeDosyasi.dosya_turu == "claim_candidate"
        )
        .all()
    )
    sayac: Counter[str] = Counter()
    sayac["bekleyen"] = len(bekleyen)
    for dosya in bekleyen:
        sayac[dosya.triyaj_sinifi or "triyajsiz"] += 1
        sayac[f"durum_{dosya.durum}"] += 1
    return dict(sayac)
