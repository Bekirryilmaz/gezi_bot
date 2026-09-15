from __future__ import annotations

import re
import unicodedata

from ortak.sabitler import DuyguEtiketi

from veri.duygu_analizi.konu_analizi import konulari_tespit_et
from veri.duygu_analizi.model import MODEL_ADI
from veri.ortak.gozlem_adayi_modeli import AdayGozlem, CikarimGuvenSinifi
from veri.ortak.yorum_modeli import HamYorum

# Genel begeni degil, karar ihtiyaclariyla iliskili gozlenebilir sinyal aileleri.
# Her desen destek/karsi yonunu acikca tasir; "yok" gibi olumsuzluklar olumlu
# keyword sayimina dusmez. Bunlar yine yalniz AdayGozlem'dir, public claim degildir.
YAPISAL_SINYAL_DESENLERI: tuple[tuple[str, str, str], ...] = (
    ("sessiz_ortam", "destek", r"\b(sakin|sessiz|huzurlu)\b"),
    ("sessiz_ortam", "karsi", r"\b(cok )?(sakin|sessiz|huzurlu) degil\b|\bgurultu(?:lu)?\b|\bses cok yuksek\b"),
    ("aile_uygunlugu", "destek", r"\b(ailecek|aileyle|ailemle)\b"),
    ("aile_uygunlugu", "karsi", r"\baile(?:yle|ce) gidilmez\b"),
    ("cocuk_uygunlugu", "destek", r"\bcocuk(?:lar)?la\b|\boyun alani\b"),
    ("cocuk_uygunlugu", "karsi", r"\bcocuk(?:la|larla) gidilmez\b|\bcocuk icin uygun degil\b"),
    ("calisma_uygunlugu", "destek", r"\blaptop\b|\bders calis|\bcalismak icin\b"),
    ("calisma_uygunlugu", "karsi", r"\bcalismaya uygun degil\b|\blaptop acilmaz\b"),
    ("acik_hava", "destek", r"\b(bahce|teras|acik hava|avlu)\b"),
    ("acik_hava", "karsi", r"\b(bahce|teras|acik alan)(?:si)? yok\b"),
    ("manzara", "destek", r"\bmanzarali\b|\bmanzarasi (?:guzel|var)\b|\bdeniz gor"),
    ("manzara", "karsi", r"\bmanzarasi yok\b|\bmanzara yok\b"),
    ("canli_muzik", "destek", r"\bcanli muzik (?:var|yapiliyor|guzel)\b"),
    ("canli_muzik", "karsi", r"\bcanli muzik yok\b"),
    ("kalabaliklik", "destek", r"\b(cok )?(kalabalik|tiklim tiklim|yogun)\b"),
    ("kalabaliklik", "karsi", r"\bkalabalik degil\b|\bsakin(?:di)?\b"),
    ("uygun_fiyat", "destek", r"\b(ucuz|uygun fiyatli|hesapli|butce dostu)\b"),
    ("uygun_fiyat", "karsi", r"\b(cok )?pahali\b|\bfiyatlar yuksek\b"),
    ("otopark", "destek", r"\botopark(?:i)? var\b|\bpark yeri var\b"),
    ("otopark", "karsi", r"\botopark yok\b|\bpark yeri yok\b|\bpark sorunu\b"),
    ("wifi", "destek", r"\bwi ?fi (?:var|iyi|hizli)\b|\binternet (?:var|iyi|hizli)\b"),
    ("wifi", "karsi", r"\bwi ?fi (?:yok|cekmiyor|kotu)\b|\binternet (?:yok|cekmiyor)\b"),
)


def yorumdan_yapisal_sinyal_adaylari(ham_yorum: HamYorum, duygu_skoru: float) -> list[AdayGozlem]:
    metin = (
        unicodedata.normalize("NFKD", ham_yorum.yorum_metni.replace("ı", "i").replace("İ", "I"))
        .encode("ascii", "ignore")
        .decode("ascii")
        .lower()
    )
    bulunan: dict[str, tuple[str, str]] = {}
    # Karsi desenleri ayni ailede destek desenine baskin tutar.
    for aile, yon, desen in YAPISAL_SINYAL_DESENLERI:
        eslesme = re.search(desen, metin)
        if eslesme and (aile not in bulunan or yon == "karsi"):
            bulunan[aile] = (yon, eslesme.group(0))
    return [
        AdayGozlem(
            kaynak=ham_yorum.kaynak,
            kaynak_kayit_id=ham_yorum.kaynak_yorum_id,
            yer_adayi=ham_yorum.kaynak_yer_id,
            span=span[:500],
            konu=aile,
            tahmini_gozlem={"yon": yon, "bilgi_turu": "yapisal_sinyal_adayi"},
            zaman_kapsami={
                "yorum_tarihi": ham_yorum.yorum_tarihi.isoformat()
                if ham_yorum.yorum_tarihi
                else None
            },
            model_surumu="turkce-yapisal-sinyal-v1",
            # Duygu skoru, olgusal sinyalin dogruluk guveni degildir. Bu
            # dogrulanmamis kural eslesmeleri incelemeye kadar dusuk guvenlidir.
            cikarim_guven_sinifi=CikarimGuvenSinifi.DUSUK,
        )
        for aile, (yon, span) in bulunan.items()
    ]


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
    konu_duygulari = konulari_tespit_et(ham_yorum.yorum_metni, genel_duygu=duygu_etiketi)
    adaylar = []
    for konu in konu_duygulari:
        span = (konu.gecen_ifade or ham_yorum.yorum_metni).strip()[:500]
        adaylar.append(
            AdayGozlem(
                kaynak=ham_yorum.kaynak,
                kaynak_kayit_id=ham_yorum.kaynak_yorum_id,
                yer_adayi=ham_yorum.kaynak_yer_id,
                span=span,
                konu=konu.konu,
                tahmini_gozlem={
                    "tepki_sinifi": konu.duygu_etiketi.value,
                    "bilgi_turu": "kisisel_tepki_adayi",
                },
                zaman_kapsami={
                    "yorum_tarihi": ham_yorum.yorum_tarihi.isoformat()
                    if ham_yorum.yorum_tarihi
                    else None
                },
                model_surumu=f"{MODEL_ADI}+konu-kural-v1",
                cikarim_guven_sinifi=guven_sinifi(duygu_skoru),
            )
        )
    # Kisisel tepki ile yapisal sinyal farkli bilgi turleridir. Ayni konu
    # adini tasimalari, ozellikle karsi kaniti dusurme gerekcesi olamaz.
    adaylar.extend(yorumdan_yapisal_sinyal_adaylari(ham_yorum, duygu_skoru))
    return adaylar
