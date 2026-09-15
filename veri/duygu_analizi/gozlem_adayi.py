from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from dataclasses import dataclass
from typing import Any

from ortak.sabitler import (
    AdaySozlesmeSurumu,
    CikarimYontemi,
    DahiliSinyalAilesi,
    DuyguEtiketi,
    GozlemTuru,
    SinyalYonu,
)

from veri.duygu_analizi.konu_analizi import konulari_tespit_et
from veri.duygu_analizi.model import MODEL_ADI
from veri.ortak.gozlem_adayi_modeli import AdayGozlem, CikarimGuvenSinifi
from veri.ortak.yorum_modeli import HamYorum


@dataclass(frozen=True)
class SinyalKurali:
    aile: DahiliSinyalAilesi
    yon: SinyalYonu
    gozlem_turu: GozlemTuru
    deger: Any
    desen: str


# Daha dar desen once gelir. Ayni ailede ilk eslesme explicit polarity'yi
# belirler; genel BERT skoru bu karari degistiremez.
YAPISAL_SINYAL_KURALLARI: tuple[SinyalKurali, ...] = (
    SinyalKurali(
        DahiliSinyalAilesi.WIFI,
        SinyalYonu.COUNTER,
        GozlemTuru.EXPERIENCE_SIGNAL,
        "cok_yavas",
        r"\bwi ?fi cok yavas\b|\binternet cok yavas\b",
    ),
    SinyalKurali(
        DahiliSinyalAilesi.WIFI,
        SinyalYonu.COUNTER,
        GozlemTuru.FACT_SIGNAL,
        False,
        r"\bwi ?fi yok\b|\binternet yok\b",
    ),
    SinyalKurali(
        DahiliSinyalAilesi.WIFI,
        SinyalYonu.COUNTER,
        GozlemTuru.EXPERIENCE_SIGNAL,
        "kotu",
        r"\bwi ?fi kotu\b|\binternet kotu\b",
    ),
    SinyalKurali(
        DahiliSinyalAilesi.WIFI,
        SinyalYonu.COUNTER,
        GozlemTuru.EXPERIENCE_SIGNAL,
        "cekmiyor",
        r"\bwi ?fi cekmiyor\b|\binternet cekmiyor\b",
    ),
    SinyalKurali(
        DahiliSinyalAilesi.WIFI,
        SinyalYonu.SUPPORT,
        GozlemTuru.FACT_SIGNAL,
        True,
        r"\bwi ?fi var\b|\binternet var\b",
    ),
    SinyalKurali(
        DahiliSinyalAilesi.SESSIZ_ORTAM,
        SinyalYonu.COUNTER,
        GozlemTuru.EXPERIENCE_SIGNAL,
        False,
        r"\bgurultu(?:lu)?\b|\bses cok yuksek\b",
    ),
    SinyalKurali(
        DahiliSinyalAilesi.SESSIZ_ORTAM,
        SinyalYonu.SUPPORT,
        GozlemTuru.EXPERIENCE_SIGNAL,
        True,
        r"\b(?:sakin|sessiz|huzurlu)\b",
    ),
    SinyalKurali(
        DahiliSinyalAilesi.AILE_UYGUNLUGU,
        SinyalYonu.COUNTER,
        GozlemTuru.EXPERIENCE_SIGNAL,
        False,
        r"\baile(?:yle|ce) gidilmez\b",
    ),
    SinyalKurali(
        DahiliSinyalAilesi.AILE_UYGUNLUGU,
        SinyalYonu.SUPPORT,
        GozlemTuru.EXPERIENCE_SIGNAL,
        True,
        r"\b(?:ailecek|aileyle|ailemle)\b",
    ),
    SinyalKurali(
        DahiliSinyalAilesi.COCUK_UYGUNLUGU,
        SinyalYonu.COUNTER,
        GozlemTuru.EXPERIENCE_SIGNAL,
        False,
        r"\bcocuk(?:la|larla) gidilmez\b",
    ),
    SinyalKurali(
        DahiliSinyalAilesi.COCUK_UYGUNLUGU,
        SinyalYonu.SUPPORT,
        GozlemTuru.EXPERIENCE_SIGNAL,
        True,
        r"\bcocuk(?:la|larla) cok rahat\b|\boyun alani\b|\bcocuk icin uygun\b",
    ),
    SinyalKurali(
        DahiliSinyalAilesi.CALISMA_UYGUNLUGU,
        SinyalYonu.COUNTER,
        GozlemTuru.EXPERIENCE_SIGNAL,
        False,
        r"\blaptopla calisilmaz\b|\blaptop acilmaz\b",
    ),
    SinyalKurali(
        DahiliSinyalAilesi.CALISMA_UYGUNLUGU,
        SinyalYonu.SUPPORT,
        GozlemTuru.EXPERIENCE_SIGNAL,
        True,
        r"\bders calismak icin ideal\b|\bcalismak icin ideal\b|\bcalismaya uygun\b",
    ),
    SinyalKurali(
        DahiliSinyalAilesi.ACIK_ALAN,
        SinyalYonu.COUNTER,
        GozlemTuru.FACT_SIGNAL,
        False,
        r"\b(?:bahce|teras|acik alan)(?:si)? yok\b",
    ),
    SinyalKurali(
        DahiliSinyalAilesi.ACIK_ALAN,
        SinyalYonu.SUPPORT,
        GozlemTuru.FACT_SIGNAL,
        True,
        r"\b(?:bahce|teras|acik alan|avlu)(?:si)? var\b",
    ),
    SinyalKurali(
        DahiliSinyalAilesi.MANZARA,
        SinyalYonu.COUNTER,
        GozlemTuru.EXPERIENCE_SIGNAL,
        "gorunmuyor",
        r"\bdeniz gorunmuyor\b",
    ),
    SinyalKurali(
        DahiliSinyalAilesi.MANZARA,
        SinyalYonu.COUNTER,
        GozlemTuru.EXPERIENCE_SIGNAL,
        "goremedik",
        r"\bdenizi? goremedik\b",
    ),
    SinyalKurali(
        DahiliSinyalAilesi.MANZARA,
        SinyalYonu.COUNTER,
        GozlemTuru.FACT_SIGNAL,
        False,
        r"\bmanzarasi yok\b|\bmanzara yok\b",
    ),
    SinyalKurali(
        DahiliSinyalAilesi.MANZARA,
        SinyalYonu.SUPPORT,
        GozlemTuru.EXPERIENCE_SIGNAL,
        "guzel",
        r"\bmanzarasi (?:cok )?(?:guzel|harika|mukemmel)",
    ),
    SinyalKurali(
        DahiliSinyalAilesi.MANZARA,
        SinyalYonu.SUPPORT,
        GozlemTuru.FACT_SIGNAL,
        True,
        r"\bmanzarali\b|\bmanzarasi var\b|\bdeniz gor",
    ),
    SinyalKurali(
        DahiliSinyalAilesi.FIYAT_ALGISI,
        SinyalYonu.COUNTER,
        GozlemTuru.EXPERIENCE_SIGNAL,
        "pahali",
        r"\b(?:cok )?pahali\b|\bfiyatlar yuksek\b",
    ),
    SinyalKurali(
        DahiliSinyalAilesi.FIYAT_ALGISI,
        SinyalYonu.SUPPORT,
        GozlemTuru.EXPERIENCE_SIGNAL,
        "uygun",
        r"\b(?:ucuz|uygun fiyatli|hesapli|butce dostu)\b",
    ),
    SinyalKurali(
        DahiliSinyalAilesi.OTOPARK,
        SinyalYonu.COUNTER,
        GozlemTuru.EXPERIENCE_SIGNAL,
        "park_sorunu",
        r"\bpark sorunu\b",
    ),
    SinyalKurali(
        DahiliSinyalAilesi.OTOPARK,
        SinyalYonu.COUNTER,
        GozlemTuru.FACT_SIGNAL,
        False,
        r"\botopark yok\b|\bpark yeri yok\b",
    ),
    SinyalKurali(
        DahiliSinyalAilesi.OTOPARK,
        SinyalYonu.SUPPORT,
        GozlemTuru.FACT_SIGNAL,
        True,
        r"\botopark(?:i)? var\b|\bpark yeri var\b",
    ),
    SinyalKurali(
        DahiliSinyalAilesi.REZERVASYON,
        SinyalYonu.COUNTER,
        GozlemTuru.EXPERIENCE_SIGNAL,
        "rezervasyonsuz_yer_bulunamadi",
        r"\brezervasyonsuz yer bulamadi[mk]\b",
    ),
    SinyalKurali(
        DahiliSinyalAilesi.CANLI_MUZIK,
        SinyalYonu.COUNTER,
        GozlemTuru.EXPERIENCE_SIGNAL,
        "cok_yuksek",
        r"\bcanli muzik cok yuksek\b",
    ),
    SinyalKurali(
        DahiliSinyalAilesi.CANLI_MUZIK,
        SinyalYonu.COUNTER,
        GozlemTuru.FACT_SIGNAL,
        False,
        r"\bcanli muzik yok\b",
    ),
    SinyalKurali(
        DahiliSinyalAilesi.CANLI_MUZIK,
        SinyalYonu.SUPPORT,
        GozlemTuru.FACT_SIGNAL,
        True,
        r"\bcanli muzik (?:var|yapiliyor)\b",
    ),
    SinyalKurali(
        DahiliSinyalAilesi.KALABALIKLIK,
        SinyalYonu.SUPPORT,
        GozlemTuru.EXPERIENCE_SIGNAL,
        "kalabalik",
        r"\b(?:cok )?(?:kalabalik|tiklim tiklim|yogun)\b",
    ),
)

_TERS_DENEYIM_DEGERLERI: dict[tuple[DahiliSinyalAilesi, str], bool | str] = {
    (DahiliSinyalAilesi.WIFI, "kotu"): "kotu_degil",
    (DahiliSinyalAilesi.WIFI, "cok_yavas"): "cok_yavas_degil",
    (DahiliSinyalAilesi.FIYAT_ALGISI, "pahali"): "pahali_degil",
    (DahiliSinyalAilesi.CANLI_MUZIK, "cok_yuksek"): "cok_yuksek_degil",
    (DahiliSinyalAilesi.KALABALIKLIK, "kalabalik"): "sakin",
}
_YAKIN_OLUMSUZLUK = re.compile(r"^\s+(?:hic\s+)?degil(?:di|mis|dir)?\b")
_KARSIT_BAGLAC = re.compile(r"\b(?:ama|fakat|ancak|lakin)\b")

KONU_SINYAL_AILE_ESLEMESI: dict[str, DahiliSinyalAilesi] = {
    "manzara": DahiliSinyalAilesi.MANZARA,
    "fiyat": DahiliSinyalAilesi.FIYAT_ALGISI,
    "lezzet": DahiliSinyalAilesi.YEMEK,
    "kalabalik": DahiliSinyalAilesi.KALABALIKLIK,
    "kahvalti": DahiliSinyalAilesi.KAHVALTI,
    "gurultu": DahiliSinyalAilesi.SESSIZ_ORTAM,
}


def _yorum_parmak_izi_uret(ham_yorum: HamYorum) -> str:
    ham = json.dumps(
        {
            "kaynak": ham_yorum.kaynak.value,
            "kaynak_yer": ham_yorum.kaynak_yer_id,
            "yorum": ham_yorum.yorum_metni,
        },
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(ham.encode("utf-8")).hexdigest()


def _negation_uygula(
    metin: str,
    eslesme: re.Match[str],
    kural: SinyalKurali,
) -> tuple[SinyalYonu, bool | str, str] | None:
    sonrasi = metin[eslesme.end() :]
    olumsuzluk = _YAKIN_OLUMSUZLUK.match(sonrasi)
    if olumsuzluk is None:
        return kural.yon, kural.deger, eslesme.group(0)
    ters_yon = (
        SinyalYonu.COUNTER
        if kural.yon is SinyalYonu.SUPPORT
        else SinyalYonu.SUPPORT
    )
    if isinstance(kural.deger, bool):
        ters_deger: bool | str | None = not kural.deger
    else:
        ters_deger = _TERS_DENEYIM_DEGERLERI.get((kural.aile, kural.deger))
    if ters_deger is None:
        return None
    span_sonu = eslesme.end() + olumsuzluk.end()
    return ters_yon, ters_deger, metin[eslesme.start() : span_sonu]


def _cumleciklere_ayir(metin: str) -> list[str]:
    parcalar = [p.strip() for p in _KARSIT_BAGLAC.split(metin) if p.strip()]
    return parcalar or [metin]


def _aspect_guveni(
    *,
    gozlem_turu: GozlemTuru,
    negation_cevrildi: bool,
    karsit_baglac: bool,
) -> tuple[CikarimGuvenSinifi, dict[str, Any]]:
    if negation_cevrildi or karsit_baglac:
        sinif = CikarimGuvenSinifi.ORTA
        aciklik = "negation_veya_karsit_baglac"
    elif gozlem_turu is GozlemTuru.FACT_SIGNAL:
        sinif = CikarimGuvenSinifi.YUKSEK
        aciklik = "acik_predicate"
    else:
        sinif = CikarimGuvenSinifi.ORTA
        aciklik = "deneyim_predicate"
    return sinif, {
        "desen_eslesmesi": True,
        "explicit_aspect_polarity": True,
        "genel_bert_kullanildi": False,
        "bert_buyuklugunden_turetilmedi": True,
        "negation_cevrildi": negation_cevrildi,
        "karsit_baglac": karsit_baglac,
        "eslesme_acikligi": aciklik,
    }


def yorumdan_yapisal_sinyal_adaylari(ham_yorum: HamYorum, duygu_skoru: float) -> list[AdayGozlem]:
    del duygu_skoru  # Aspect guveni BERT buyuklugunden turetilmez.
    metin = (
        unicodedata.normalize("NFKD", ham_yorum.yorum_metni.replace("ı", "i").replace("İ", "I"))
        .encode("ascii", "ignore")
        .decode("ascii")
        .lower()
    )
    karsit_baglac = bool(_KARSIT_BAGLAC.search(metin))
    bulunan: dict[
        DahiliSinyalAilesi,
        tuple[SinyalKurali, SinyalYonu, bool | str, str, bool],
    ] = {}
    for cumlecik in _cumleciklere_ayir(metin):
        for kural in YAPISAL_SINYAL_KURALLARI:
            eslesme = re.search(kural.desen, cumlecik)
            if not eslesme:
                continue
            sonuc = _negation_uygula(cumlecik, eslesme, kural)
            if sonuc is None:
                continue
            yon, deger, span = sonuc
            onceki = bulunan.get(kural.aile)
            if onceki is not None and onceki[1] is SinyalYonu.COUNTER:
                continue
            bulunan[kural.aile] = (
                kural,
                yon,
                deger,
                span,
                sonuc[0] is not kural.yon,
            )
    yorum_parmak_izi = _yorum_parmak_izi_uret(ham_yorum)
    adaylar = []
    for aile, (kural, yon, deger, span, negation_cevrildi) in bulunan.items():
        sinif, kirilim = _aspect_guveni(
            gozlem_turu=kural.gozlem_turu,
            negation_cevrildi=negation_cevrildi,
            karsit_baglac=karsit_baglac,
        )
        adaylar.append(
            AdayGozlem(
                sozlesme_surumu=AdaySozlesmeSurumu.CANONICAL_V1,
                kaynak=ham_yorum.kaynak,
                kaynak_kayit_id=ham_yorum.kaynak_yorum_id,
                yorum_parmak_izi=yorum_parmak_izi,
                yer_adayi=ham_yorum.kaynak_yer_id,
                span=span[:500],
                konu=aile.value,
                aile=aile,
                yon=yon,
                deger=deger,
                gozlem_turu=kural.gozlem_turu,
                tahmini_gozlem={
                    "yon": "destek" if yon is SinyalYonu.SUPPORT else "karsi",
                    "deger": deger,
                    "bilgi_turu": "yapisal_sinyal_adayi",
                },
                zaman_kapsami={
                    "yorum_tarihi": ham_yorum.yorum_tarihi.isoformat()
                    if ham_yorum.yorum_tarihi
                    else None
                },
                cikarim_yontemi=CikarimYontemi.DETERMINISTIK_KURAL,
                model_surumu="kural-tabanli-nlp-v2",
                kural_surumu="safe-extractor-v2",
                cikarim_guven_sinifi=sinif,
                guven_kirilimi=kirilim,
            )
        )
    return adaylar


def guven_sinifi(duygu_skoru: float) -> CikarimGuvenSinifi:
    mutlak = abs(duygu_skoru)
    if mutlak >= 0.75:
        return CikarimGuvenSinifi.YUKSEK
    if mutlak >= 0.35:
        return CikarimGuvenSinifi.ORTA
    return CikarimGuvenSinifi.DUSUK


def yorumdan_aday_gozlemler(
    ham_yorum: HamYorum, duygu_etiketi: DuyguEtiketi, duygu_skoru: float
) -> list[AdayGozlem]:
    """Model ciktisini yalniz insan/politika incelemesi bekleyen adaylara cevirir."""
    yorum_parmak_izi = _yorum_parmak_izi_uret(ham_yorum)
    konu_duygulari = konulari_tespit_et(
        ham_yorum.yorum_metni,
        genel_duygu=duygu_etiketi,
        genel_duygu_fallback_kullan=False,
    )
    adaylar: list[AdayGozlem] = []
    if duygu_etiketi is not DuyguEtiketi.NOTR:
        genel_yon = (
            SinyalYonu.SUPPORT
            if duygu_etiketi is DuyguEtiketi.OLUMLU
            else SinyalYonu.COUNTER
        )
        adaylar.append(
            AdayGozlem(
                sozlesme_surumu=AdaySozlesmeSurumu.CANONICAL_V1,
                kaynak=ham_yorum.kaynak,
                kaynak_kayit_id=ham_yorum.kaynak_yorum_id,
                yorum_parmak_izi=yorum_parmak_izi,
                yer_adayi=ham_yorum.kaynak_yer_id,
                span=ham_yorum.yorum_metni.strip()[:500],
                konu=DahiliSinyalAilesi.GENEL_DUYGU.value,
                aile=DahiliSinyalAilesi.GENEL_DUYGU,
                yon=genel_yon,
                deger=duygu_etiketi.value,
                gozlem_turu=GozlemTuru.SENTIMENT_SIGNAL,
                tahmini_gozlem={
                    "tepki_sinifi": duygu_etiketi.value,
                    "bilgi_turu": "genel_duygu_adayi",
                    "karar_sinyali": False,
                },
                zaman_kapsami={
                    "yorum_tarihi": ham_yorum.yorum_tarihi.isoformat()
                    if ham_yorum.yorum_tarihi
                    else None
                },
                cikarim_yontemi=CikarimYontemi.DUYGU_MODELI,
                model_surumu=MODEL_ADI,
                kural_surumu="genel-duygu-v1",
                cikarim_guven_sinifi=guven_sinifi(duygu_skoru),
                guven_kirilimi={
                    "genel_bert_kullanildi": True,
                    "model_mutlak_skoru": round(abs(duygu_skoru), 4),
                    "karar_sinyali": False,
                },
            )
        )
    for konu in konu_duygulari:
        aile = KONU_SINYAL_AILE_ESLEMESI.get(konu.konu)
        if aile is None or konu.duygu_etiketi is DuyguEtiketi.NOTR:
            continue
        span = (konu.gecen_ifade or ham_yorum.yorum_metni).strip()[:500]
        adaylar.append(
            AdayGozlem(
                sozlesme_surumu=AdaySozlesmeSurumu.CANONICAL_V1,
                kaynak=ham_yorum.kaynak,
                kaynak_kayit_id=ham_yorum.kaynak_yorum_id,
                yorum_parmak_izi=yorum_parmak_izi,
                yer_adayi=ham_yorum.kaynak_yer_id,
                span=span,
                konu=aile.value,
                aile=aile,
                yon=(
                    SinyalYonu.SUPPORT
                    if konu.duygu_etiketi is DuyguEtiketi.OLUMLU
                    else SinyalYonu.COUNTER
                    if konu.duygu_etiketi is DuyguEtiketi.OLUMSUZ
                    else None
                ),
                deger=konu.duygu_etiketi.value,
                gozlem_turu=GozlemTuru.SENTIMENT_SIGNAL,
                tahmini_gozlem={
                    "tepki_sinifi": konu.duygu_etiketi.value,
                    "bilgi_turu": "kisisel_tepki_adayi",
                },
                zaman_kapsami={
                    "yorum_tarihi": ham_yorum.yorum_tarihi.isoformat()
                    if ham_yorum.yorum_tarihi
                    else None
                },
                cikarim_yontemi=CikarimYontemi.DETERMINISTIK_KURAL,
                model_surumu="turkce-konu-duygu-kural-v2",
                kural_surumu="konu-kural-v2-no-aspect-fallback",
                cikarim_guven_sinifi=CikarimGuvenSinifi.DUSUK,
                guven_kirilimi={
                    "yerel_ifade_duygusu": konu.duygu_etiketi.value,
                    "genel_bert_kullanildi": False,
                    "guven_kaynagi": "explicit_aspect_kurali",
                },
            )
        )
    # Kisisel tepki ile yapisal sinyal farkli bilgi turleridir. Ayni konu
    # adini tasimalari, ozellikle karsi kaniti dusurme gerekcesi olamaz.
    adaylar.extend(yorumdan_yapisal_sinyal_adaylari(ham_yorum, duygu_skoru))
    return adaylar
