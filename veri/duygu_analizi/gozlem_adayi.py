from __future__ import annotations

from ortak.sabitler import DuyguEtiketi
from veri.duygu_analizi.konu_analizi import konulari_tespit_et
from veri.duygu_analizi.model import MODEL_ADI
from veri.ortak.gozlem_adayi_modeli import AdayGozlem, CikarimGuvenSinifi
from veri.ortak.yorum_modeli import HamYorum


def guven_sinifi(duygu_skoru: float) -> CikarimGuvenSinifi:
    mutlak = abs(duygu_skoru)
    if mutlak >= 0.75:
        return CikarimGuvenSinifi.YUKSEK
    if mutlak >= 0.35:
        return CikarimGuvenSinifi.ORTA
    return CikarimGuvenSinifi.DUSUK


def yorumdan_aday_gozlemler(ham_yorum: HamYorum, duygu_etiketi: DuyguEtiketi, duygu_skoru: float) -> list[AdayGozlem]:
    """Model ciktisini yalniz insan/politika incelemesi bekleyen adaylara cevirir."""
    konu_duygulari = konulari_tespit_et(ham_yorum.yorum_metni, genel_duygu=duygu_etiketi)
    adaylar = []
    for konu in konu_duygulari:
        span = (konu.gecen_ifade or ham_yorum.yorum_metni).strip()[:500]
        adaylar.append(AdayGozlem(
            kaynak=ham_yorum.kaynak,
            kaynak_kayit_id=ham_yorum.kaynak_yorum_id,
            yer_adayi=ham_yorum.kaynak_yer_id,
            span=span,
            konu=konu.konu,
            tahmini_gozlem={"tepki_sinifi": konu.duygu_etiketi.value, "bilgi_turu": "kisisel_tepki_adayi"},
            zaman_kapsami={"yorum_tarihi": ham_yorum.yorum_tarihi.isoformat() if ham_yorum.yorum_tarihi else None},
            model_surumu=f"{MODEL_ADI}+konu-kural-v1",
            cikarim_guven_sinifi=guven_sinifi(duygu_skoru),
        ))
    return adaylar
