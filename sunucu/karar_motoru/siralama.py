from __future__ import annotations

from dataclasses import dataclass

from ortak.sabitler import (
    AmacEslemeSeviyesi,
    KimlikKaliteSinifi,
    amac_esleme_seviyesi,
)
from sunucu.arama.normalizasyon import turkce_arama_normalize
from sunucu.bilgi.domain import BilgiDurumu
from sunucu.karar_motoru.domain import KararAdayi, KararBaglami
from sunucu.kimlik.kalite import oneriye_uygun_mu
from sunucu.yayin.domain import YayinUygunlukDurumu

_KIMLIK_SIRASI = {
    KimlikKaliteSinifi.DOGRULANMIS.value: 0,
    KimlikKaliteSinifi.GUCLU.value: 1,
    KimlikKaliteSinifi.KULLANILABILIR.value: 2,
    KimlikKaliteSinifi.SUPHELI.value: 8,
    KimlikKaliteSinifi.KARANTINA.value: 9,
}


@dataclass(frozen=True)
class SiralamaAnahtari:
    kimlik_sirasi: int
    yayin_sirasi: int
    amac_sirasi: int
    public_fact: int
    deneyim_guclu: int
    deneyim_destek: int
    ilce_uyumu: int
    bilinmeyen_yuku: int
    tamamlik: int
    isim: str
    canonical_id: str

    def sira_demeti(self) -> tuple:
        return (
            self.kimlik_sirasi,
            self.yayin_sirasi,
            self.amac_sirasi,
            -self.public_fact,
            -self.deneyim_guclu,
            -self.deneyim_destek,
            self.ilce_uyumu,
            self.bilinmeyen_yuku,
            -self.tamamlik,
            self.isim,
            self.canonical_id,
        )

    @property
    def zengin_mi(self) -> bool:
        return self.public_fact > 0 or self.deneyim_destek > 0 or self.kimlik_sirasi <= 1


def _deneyim_destekleri(baglam: KararBaglami, aday: KararAdayi) -> tuple[int, int]:
    aileler = {sinyal.aile: sinyal for sinyal in aday.dahili_sinyaller}
    destek = 0
    guc = 0
    for tercih in baglam.tercihler:
        sinyal = aileler.get(tercih.iddia_ailesi)
        if sinyal is None or not sinyal.preference_eligible or not sinyal.destekliyor:
            continue
        if tercih.beklenen_deger is False:
            continue
        destek += 1
        if sinyal.guven_sinifi == "guclu":
            guc += 1
    return destek, guc


def _public_fact_sayisi(aday: KararAdayi) -> int:
    return sum(
        1
        for bilgi in aday.bilgiler
        if bilgi.yayinlanabilir and bilgi.bilgi_durumu is BilgiDurumu.BILINIYOR
    )


def _bilinmeyen_yuku(baglam: KararBaglami, aday: KararAdayi, deneyim_destek: int) -> int:
    yuk = 0
    public_aile = {
        bilgi.aile
        for bilgi in aday.bilgiler
        if bilgi.yayinlanabilir and bilgi.bilgi_durumu is BilgiDurumu.BILINIYOR
    }
    for tercih in baglam.tercihler:
        if tercih.iddia_ailesi in public_aile:
            continue
        if any(
            sinyal.aile == tercih.iddia_ailesi
            and sinyal.preference_eligible
            and sinyal.destekliyor
            for sinyal in aday.dahili_sinyaller
        ):
            continue
        yuk += tercih.oncelik
    if deneyim_destek == 0 and baglam.tercihler:
        yuk += 1
    return yuk


def _tamamlik(
    aday: KararAdayi,
    *,
    public_fact: int,
    deneyim_destek: int,
    amac_direkt: bool,
) -> int:
    kimlik = aday.kimlik_kalite_sinifi or KimlikKaliteSinifi.KULLANILABILIR.value
    puan = 0
    if kimlik == KimlikKaliteSinifi.DOGRULANMIS.value:
        puan += 3
    elif kimlik == KimlikKaliteSinifi.GUCLU.value:
        puan += 2
    elif kimlik == KimlikKaliteSinifi.KULLANILABILIR.value:
        puan += 1
    if aday.ilce:
        puan += 1
    if amac_direkt:
        puan += 1
    puan += min(2, public_fact)
    puan += min(2, deneyim_destek)
    return puan


def siralama_anahtari(baglam: KararBaglami, aday: KararAdayi) -> SiralamaAnahtari:
    kimlik = aday.kimlik_kalite_sinifi or KimlikKaliteSinifi.KULLANILABILIR.value
    deneyim_destek, deneyim_guc = _deneyim_destekleri(baglam, aday)
    public_fact = _public_fact_sayisi(aday)
    seviye = amac_esleme_seviyesi(aday.alt_kategori, baglam.amac)
    amac_direkt = seviye is AmacEslemeSeviyesi.DIRECT_PURPOSE_FACT
    amac_sirasi = 0 if amac_direkt or public_fact else 2
    if seviye is AmacEslemeSeviyesi.WEAK_CANDIDATE_HINT and not amac_direkt:
        amac_sirasi = 1
    istenen_ilce = (baglam.cografi_baglam.ilce or "").casefold().strip()
    aday_ilce = (aday.ilce or "").casefold().strip()
    if istenen_ilce:
        ilce_uyumu = 0 if aday_ilce == istenen_ilce else 2
    else:
        ilce_uyumu = 0
    yayin_sirasi = 0 if aday.yayin_durumu is YayinUygunlukDurumu.YAYINLANABILIR else 1
    return SiralamaAnahtari(
        kimlik_sirasi=_KIMLIK_SIRASI.get(kimlik, 5),
        yayin_sirasi=yayin_sirasi,
        amac_sirasi=amac_sirasi,
        public_fact=public_fact,
        deneyim_guclu=deneyim_guc,
        deneyim_destek=deneyim_destek,
        ilce_uyumu=ilce_uyumu,
        bilinmeyen_yuku=_bilinmeyen_yuku(baglam, aday, deneyim_destek),
        tamamlik=_tamamlik(
            aday,
            public_fact=public_fact,
            deneyim_destek=deneyim_destek,
            amac_direkt=amac_direkt,
        ),
        isim=turkce_arama_normalize(aday.isim),
        canonical_id=aday.canonical_id,
    )


def sirala_adaylar(baglam: KararBaglami, adaylar: list[KararAdayi]) -> list[KararAdayi]:
    return sorted(adaylar, key=lambda aday: siralama_anahtari(baglam, aday).sira_demeti())


def oneri_listesini_sec(
    baglam: KararBaglami,
    adaylar: list[KararAdayi],
    hedef: int = 5,
) -> list[KararAdayi]:
    uygun = [aday for aday in adaylar if oneriye_uygun_mu(aday.kimlik_kalite_sinifi)]
    sirali = sirala_adaylar(baglam, uygun)
    anahtarlar = {id(aday): siralama_anahtari(baglam, aday) for aday in sirali}
    zengin = [aday for aday in sirali if anahtarlar[id(aday)].zengin_mi]
    kaynak = zengin if zengin else sirali
    secilen: list[KararAdayi] = []
    isimler: set[str] = set()
    for aday in kaynak:
        norm = turkce_arama_normalize(aday.isim)
        if not norm or norm in isimler:
            continue
        isimler.add(norm)
        secilen.append(aday)
        if len(secilen) >= hedef:
            break
    return secilen
