from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import date, datetime, time
from enum import StrEnum
from typing import Any

from sunucu.bilgi.domain import BilgiDurumu
from sunucu.yayin.domain import YayinUygunlukDurumu


class KosulDurumu(StrEnum):
    UYGUN = "uygun"
    UYGUN_DEGIL = "uygun_degil"
    DEGERLENDIRILEMIYOR = "degerlendirilemiyor"


class KararSonucuTuru(StrEnum):
    ONERILEBILIR = "onerilebilir"
    KOSULA_BAGLI_ONERILEBILIR = "kosula_bagli_onerilebilir"
    IHTIYACLA_UYUSMUYOR = "ihtiyacla_uyusmuyor"
    KRITIK_BILGI_BILINMIYOR = "kritik_bilgi_bilinmiyor"
    KAPSAM_DISI = "kapsam_disi"
    NETLESTIRME_GEREKLI = "netlestirme_gerekli"
    SERVIS_GECICI_KULLANILAMIYOR = "servis_gecici_kullanilamiyor"


class Karsilastirma(StrEnum):
    ESITTIR = "esittir"
    ICERIR = "icerir"
    EN_FAZLA = "en_fazla"
    EN_AZ = "en_az"


class NedenKodu(StrEnum):
    YAYIN_UYGUN = "yayin_uygun"
    YAYIN_UYGUN_DEGIL = "yayin_uygun_degil"
    COGRAFI_KAPSAM_DISI = "cografi_kapsam_disi"
    ZAMAN_UYGUN = "zaman_uygun"
    AMAC_DESTEKLENIYOR = "amac_destekleniyor"
    AMAC_DESTEKLENMIYOR = "amac_desteklenmiyor"
    AMAC_BILINMIYOR = "amac_bilinmiyor"
    ZORUNLU_KOSUL_DOGRULANDI = "zorunlu_kosul_dogrulandi"
    ZORUNLU_KOSUL_SAGLANMIYOR = "zorunlu_kosul_saglanmiyor"
    KRITIK_KOSUL_BILINMIYOR = "kritik_kosul_bilinmiyor"
    KRITIK_KOSUL_CELISKILI = "kritik_kosul_celiskili"
    KRITIK_KOSUL_ESKIMIS = "kritik_kosul_eskimis"
    KRITIK_KOSUL_GERI_CEKILMIS = "kritik_kosul_geri_cekilmis"
    TERCIH_DESTEKLENIYOR = "tercih_destekleniyor"
    TERCIH_DESTEKLENMIYOR = "tercih_desteklenmiyor"
    TERCIH_BILINMIYOR = "tercih_bilinmiyor"
    KULLANICI_TARAFINDAN_REDDEDILDI = "kullanici_tarafindan_reddedildi"
    KULLANICI_TARAFINDAN_SABITLENDI = "kullanici_tarafindan_sabitlendi"
    KRITIK_GIRDI_ANLASILMADI = "kritik_girdi_anlasilmadi"
    SERVIS_GECICI_KULLANILAMIYOR = "servis_gecici_kullanilamiyor"


NEDEN_METINLERI: dict[NedenKodu, str] = {
    NedenKodu.YAYIN_UYGUN: "Yer bu karar kapsaminda yayimlanabilir.",
    NedenKodu.YAYIN_UYGUN_DEGIL: "Yer bu karar kapsaminda kullanilamaz.",
    NedenKodu.COGRAFI_KAPSAM_DISI: "Yer istenen sehir veya ilce kapsaminin disinda.",
    NedenKodu.ZAMAN_UYGUN: "Bilinen ziyaret kosullari belirtilen zamanla uyumlu.",
    NedenKodu.AMAC_DESTEKLENIYOR: "Yer belirtilen amaci destekliyor.",
    NedenKodu.AMAC_DESTEKLENMIYOR: "Yer belirtilen ana amaci desteklemiyor.",
    NedenKodu.AMAC_BILINMIYOR: "Yerin bu amaci destekledigini dogrulayamiyoruz.",
    NedenKodu.ZORUNLU_KOSUL_DOGRULANDI: "Zorunlu kosul dogrulandi.",
    NedenKodu.ZORUNLU_KOSUL_SAGLANMIYOR: "Zorunlu kosul saglanmiyor.",
    NedenKodu.KRITIK_KOSUL_BILINMIYOR: "Kritik zorunlu kosul icin yeterli bilgi yok.",
    NedenKodu.KRITIK_KOSUL_CELISKILI: "Kritik zorunlu kosula iliskin bilgiler celisiyor.",
    NedenKodu.KRITIK_KOSUL_ESKIMIS: "Kritik zorunlu kosula iliskin bilgi eskimis.",
    NedenKodu.KRITIK_KOSUL_GERI_CEKILMIS: "Kritik zorunlu kosulun onceki dayanagi geri cekilmis.",
    NedenKodu.TERCIH_DESTEKLENIYOR: "Belirtilen tercih destekleniyor.",
    NedenKodu.TERCIH_DESTEKLENMIYOR: "Belirtilen tercih desteklenmiyor; bu bir zorunlu engel degildir.",
    NedenKodu.TERCIH_BILINMIYOR: "Belirtilen tercih icin yeterli bilgi yok.",
    NedenKodu.KULLANICI_TARAFINDAN_REDDEDILDI: "Bu yer ayni baglamda kullanici tarafindan reddedildi.",
    NedenKodu.KULLANICI_TARAFINDAN_SABITLENDI: "Bu yer kullanici tarafindan secildi; zorunlu kapilar yine uygulandi.",
    NedenKodu.KRITIK_GIRDI_ANLASILMADI: "Karari degistirebilecek kritik bir girdi netlestirilmeli.",
    NedenKodu.SERVIS_GECICI_KULLANILAMIYOR: "Karar icin gereken servis gecici olarak kullanilamiyor.",
}


@dataclass(frozen=True)
class ZamanBaglami:
    ziyaret_tarihi: date | None = None
    baslangic: time | None = None
    bitis: time | None = None
    degerlendirme_zamani: datetime | None = None

    def dogrula(self) -> None:
        if self.baslangic and self.bitis and self.bitis <= self.baslangic:
            raise ValueError("ziyaret saat araligi ileri yonlu olmalidir")


@dataclass(frozen=True)
class CografiBaglam:
    sehir: str
    ilce: str | None = None
    alan: str | None = None


@dataclass(frozen=True)
class ZorunluKosul:
    kod: str
    iddia_ailesi: str
    beklenen_deger: Any
    karsilastirma: Karsilastirma = Karsilastirma.ESITTIR
    kritik: bool = True


@dataclass(frozen=True)
class Tercih:
    kod: str
    iddia_ailesi: str
    beklenen_deger: Any
    karsilastirma: Karsilastirma = Karsilastirma.ESITTIR
    oncelik: int = 1

    def __post_init__(self) -> None:
        if not 1 <= self.oncelik <= 5:
            raise ValueError("tercih onceligi 1 ile 5 arasinda olmalidir")


@dataclass(frozen=True)
class KararBaglami:
    amac: str | None
    cografi_baglam: CografiBaglam
    zaman: ZamanBaglami = field(default_factory=ZamanBaglami)
    baslangic_noktasi: str | None = None
    ulasim_bicimi: str | None = None
    kisi_sayisi: int | None = None
    butce_ust_siniri: float | None = None
    sure_ust_siniri_dakika: int | None = None
    zorunlu_kosullar: tuple[ZorunluKosul, ...] = ()
    tercihler: tuple[Tercih, ...] = ()
    reddedilen_yerler: frozenset[str] = frozenset()
    sabitlenen_yerler: frozenset[str] = frozenset()
    anlasilmayan_kritik_girdiler: tuple[str, ...] = ()
    bilgi_surumu: str = "bilinmiyor"
    politika_surumu: str = "karar-v1"
    giris_kanali: str | None = None

    def __post_init__(self) -> None:
        self.zaman.dogrula()
        if self.kisi_sayisi is not None and self.kisi_sayisi < 1:
            raise ValueError("kisi_sayisi en az 1 olmalidir")
        if self.butce_ust_siniri is not None and self.butce_ust_siniri < 0:
            raise ValueError("butce siniri negatif olamaz")
        if self.sure_ust_siniri_dakika is not None and self.sure_ust_siniri_dakika < 1:
            raise ValueError("sure siniri pozitif olmalidir")

    def karar_parmak_izi(self) -> str:
        """Kanal ve request metadata'sini bilerek disarida birakir."""
        veri = {
            "amac": self.amac,
            "cografya": self.cografi_baglam.__dict__,
            "zaman": {
                "tarih": self.zaman.ziyaret_tarihi.isoformat() if self.zaman.ziyaret_tarihi else None,
                "baslangic": self.zaman.baslangic.isoformat() if self.zaman.baslangic else None,
                "bitis": self.zaman.bitis.isoformat() if self.zaman.bitis else None,
                "degerlendirme_zamani": self.zaman.degerlendirme_zamani.isoformat() if self.zaman.degerlendirme_zamani else None,
            },
            "baslangic_noktasi": self.baslangic_noktasi,
            "ulasim_bicimi": self.ulasim_bicimi,
            "kisi_sayisi": self.kisi_sayisi,
            "butce": self.butce_ust_siniri,
            "sure": self.sure_ust_siniri_dakika,
            "zorunlu": [k.__dict__ for k in self.zorunlu_kosullar],
            "tercihler": [t.__dict__ for t in self.tercihler],
            "retler": sorted(self.reddedilen_yerler),
            "sabitler": sorted(self.sabitlenen_yerler),
            "anlasilmayan": list(self.anlasilmayan_kritik_girdiler),
            "bilgi_surumu": self.bilgi_surumu,
            "politika_surumu": self.politika_surumu,
        }
        ham = json.dumps(veri, sort_keys=True, ensure_ascii=True, default=str, separators=(",", ":"))
        return hashlib.sha256(ham.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class BilgiReferansi:
    iddia_id: str
    aile: str
    surum_no: int
    deger: Any
    bilgi_durumu: BilgiDurumu
    yayinlanabilir: bool
    yayin_surumu: int | None = None


@dataclass(frozen=True)
class KararAdayi:
    yer_id: str
    canonical_id: str
    sube_id: str
    isim: str
    sehir: str
    ilce: str | None
    yayin_durumu: YayinUygunlukDurumu
    yayin_surumu: int
    bilgiler: tuple[BilgiReferansi, ...] = ()
    sponsorlu: bool = False


@dataclass(frozen=True)
class KararGerekcesi:
    kod: NedenKodu
    mesaj: str
    ilgili_kosul: str | None = None


@dataclass(frozen=True)
class KararSonucu:
    karar_id: str
    yer_id: str | None
    canonical_id: str | None
    sube_id: str | None
    yer_ismi: str | None
    karar_turu: KararSonucuTuru
    uygunluk: KosulDurumu
    anlasilan_ihtiyac: dict[str, Any]
    gerekceler: tuple[KararGerekcesi, ...]
    kritik_engeller: tuple[KararGerekcesi, ...]
    onemli_odunler: tuple[KararGerekcesi, ...]
    bilinmeyenler: tuple[KararGerekcesi, ...]
    zaman_ve_kapsam: dict[str, Any]
    bilgi_surumu: str
    politika_surumu: str
    yayin_surumu: int | None
    kullanilan_iddia_surumleri: tuple[str, ...]
    anlamli_alternatif_farki: str | None = None
    trace_reference: str | None = None


def _deger_eslesiyor(gercek: Any, beklenen: Any, karsilastirma: Karsilastirma) -> bool:
    if isinstance(gercek, dict) and "deger" in gercek:
        gercek = gercek["deger"]
    if karsilastirma is Karsilastirma.ESITTIR:
        return gercek == beklenen
    if karsilastirma is Karsilastirma.ICERIR:
        return beklenen in gercek if isinstance(gercek, (list, tuple, set, str)) else False
    if karsilastirma is Karsilastirma.EN_FAZLA:
        return float(gercek) <= float(beklenen)
    if karsilastirma is Karsilastirma.EN_AZ:
        return float(gercek) >= float(beklenen)
    return False


def _gerekce(kod: NedenKodu, kosul: str | None = None) -> KararGerekcesi:
    return KararGerekcesi(kod=kod, mesaj=NEDEN_METINLERI[kod], ilgili_kosul=kosul)


class KararMotoru:
    """Hard gate -> amac -> tercih -> odun/bilinmeyen sirali saf cekirdek."""

    def degerlendir(self, baglam: KararBaglami, aday: KararAdayi, *, trace_reference: str | None = None) -> KararSonucu:
        gerekceler: list[KararGerekcesi] = []
        engeller: list[KararGerekcesi] = []
        odunler: list[KararGerekcesi] = []
        bilinmeyenler: list[KararGerekcesi] = []
        kullanilan: list[str] = []

        def sonuc(tur: KararSonucuTuru, uygunluk: KosulDurumu) -> KararSonucu:
            karar_ham = f"{baglam.karar_parmak_izi()}:{aday.canonical_id}:{aday.yayin_surumu}:{tur.value}"
            return KararSonucu(
                karar_id=hashlib.sha256(karar_ham.encode()).hexdigest()[:24],
                yer_id=aday.yer_id, canonical_id=aday.canonical_id, sube_id=aday.sube_id,
                yer_ismi=aday.isim, karar_turu=tur, uygunluk=uygunluk,
                anlasilan_ihtiyac={
                    "amac": baglam.amac, "sehir": baglam.cografi_baglam.sehir,
                    "ilce": baglam.cografi_baglam.ilce,
                    "zorunlu_kosullar": [k.kod for k in baglam.zorunlu_kosullar],
                    "tercihler": [t.kod for t in baglam.tercihler],
                },
                gerekceler=tuple(gerekceler), kritik_engeller=tuple(engeller),
                onemli_odunler=tuple(odunler), bilinmeyenler=tuple(bilinmeyenler),
                zaman_ve_kapsam={
                    "ziyaret_tarihi": baglam.zaman.ziyaret_tarihi.isoformat() if baglam.zaman.ziyaret_tarihi else None,
                    "saat_baslangic": baglam.zaman.baslangic.isoformat() if baglam.zaman.baslangic else None,
                    "saat_bitis": baglam.zaman.bitis.isoformat() if baglam.zaman.bitis else None,
                    "degerlendirme_zamani": baglam.zaman.degerlendirme_zamani.isoformat() if baglam.zaman.degerlendirme_zamani else None,
                    "sehir": baglam.cografi_baglam.sehir, "ilce": baglam.cografi_baglam.ilce,
                },
                bilgi_surumu=baglam.bilgi_surumu, politika_surumu=baglam.politika_surumu,
                yayin_surumu=aday.yayin_surumu,
                kullanilan_iddia_surumleri=tuple(sorted(set(kullanilan))), trace_reference=trace_reference,
            )

        # 1. Canonical/publication kapisi.
        if aday.yayin_durumu not in {YayinUygunlukDurumu.YAYINLANABILIR, YayinUygunlukDurumu.SINIRLI_YAYINLANABILIR}:
            engeller.append(_gerekce(NedenKodu.YAYIN_UYGUN_DEGIL))
            return sonuc(KararSonucuTuru.KAPSAM_DISI, KosulDurumu.UYGUN_DEGIL)
        gerekceler.append(_gerekce(NedenKodu.YAYIN_UYGUN))

        istenen_sehir = baglam.cografi_baglam.sehir.casefold().strip()
        aday_sehir = aday.sehir.casefold().strip()
        istenen_ilce = baglam.cografi_baglam.ilce.casefold().strip() if baglam.cografi_baglam.ilce else None
        aday_ilce = aday.ilce.casefold().strip() if aday.ilce else None
        if aday_sehir != istenen_sehir or (istenen_ilce is not None and aday_ilce != istenen_ilce):
            engeller.append(_gerekce(NedenKodu.COGRAFI_KAPSAM_DISI))
            return sonuc(KararSonucuTuru.KAPSAM_DISI, KosulDurumu.UYGUN_DEGIL)

        # Ayni baglamdaki acik ret, kalite yargisi degil tekrar onerme kapisidir.
        if aday.yer_id in baglam.reddedilen_yerler or aday.canonical_id in baglam.reddedilen_yerler:
            engeller.append(_gerekce(NedenKodu.KULLANICI_TARAFINDAN_REDDEDILDI))
            return sonuc(KararSonucuTuru.IHTIYACLA_UYUSMUYOR, KosulDurumu.UYGUN_DEGIL)
        if aday.yer_id in baglam.sabitlenen_yerler or aday.canonical_id in baglam.sabitlenen_yerler:
            gerekceler.append(_gerekce(NedenKodu.KULLANICI_TARAFINDAN_SABITLENDI))

        if baglam.anlasilmayan_kritik_girdiler:
            for girdi in baglam.anlasilmayan_kritik_girdiler:
                bilinmeyenler.append(_gerekce(NedenKodu.KRITIK_GIRDI_ANLASILMADI, girdi))
            return sonuc(KararSonucuTuru.NETLESTIRME_GEREKLI, KosulDurumu.DEGERLENDIRILEMIYOR)

        ailelere: dict[str, list[BilgiReferansi]] = {}
        for bilgi in aday.bilgiler:
            ailelere.setdefault(bilgi.aile, []).append(bilgi)

        # 2-3. Gerceklesebilirlik ve zorunlu kosullar. Tercihler bu sonucu degistiremez.
        for kosul in baglam.zorunlu_kosullar:
            aday_bilgiler = ailelere.get(kosul.iddia_ailesi, [])
            kullanilabilir = [b for b in aday_bilgiler if b.yayinlanabilir and b.bilgi_durumu is BilgiDurumu.BILINIYOR]
            if kullanilabilir:
                bilgi = sorted(kullanilabilir, key=lambda b: (b.surum_no, b.iddia_id))[-1]
                kullanilan.append(f"{bilgi.iddia_id}:{bilgi.surum_no}")
                if _deger_eslesiyor(bilgi.deger, kosul.beklenen_deger, kosul.karsilastirma):
                    gerekceler.append(_gerekce(NedenKodu.ZORUNLU_KOSUL_DOGRULANDI, kosul.kod))
                else:
                    engeller.append(_gerekce(NedenKodu.ZORUNLU_KOSUL_SAGLANMIYOR, kosul.kod))
                    return sonuc(KararSonucuTuru.IHTIYACLA_UYUSMUYOR, KosulDurumu.UYGUN_DEGIL)
                continue
            durumlar = {b.bilgi_durumu for b in aday_bilgiler}
            kod = (
                NedenKodu.KRITIK_KOSUL_GERI_CEKILMIS if BilgiDurumu.GERI_CEKILMIS in durumlar else
                NedenKodu.KRITIK_KOSUL_CELISKILI if BilgiDurumu.CELISKILI in durumlar else
                NedenKodu.KRITIK_KOSUL_ESKIMIS if BilgiDurumu.ESKIMIS in durumlar else
                NedenKodu.KRITIK_KOSUL_BILINMIYOR
            )
            bilinmeyenler.append(_gerekce(kod, kosul.kod))

        if bilinmeyenler:
            return sonuc(KararSonucuTuru.KRITIK_BILGI_BILINMIYOR, KosulDurumu.DEGERLENDIRILEMIYOR)

        # 4. Amac destegi ayri bir iddia ailesidir; yoksa olumlu karar kurulmaz.
        if baglam.amac:
            amac_bilgileri = [b for b in ailelere.get("amac_destegi", ()) if b.yayinlanabilir and b.bilgi_durumu is BilgiDurumu.BILINIYOR]
            if not amac_bilgileri:
                bilinmeyenler.append(_gerekce(NedenKodu.AMAC_BILINMIYOR, baglam.amac))
                return sonuc(KararSonucuTuru.KRITIK_BILGI_BILINMIYOR, KosulDurumu.DEGERLENDIRILEMIYOR)
            amac_bilgisi = sorted(amac_bilgileri, key=lambda b: (b.surum_no, b.iddia_id))[-1]
            kullanilan.append(f"{amac_bilgisi.iddia_id}:{amac_bilgisi.surum_no}")
            if not _deger_eslesiyor(amac_bilgisi.deger, baglam.amac, Karsilastirma.ICERIR):
                engeller.append(_gerekce(NedenKodu.AMAC_DESTEKLENMIYOR, baglam.amac))
                return sonuc(KararSonucuTuru.IHTIYACLA_UYUSMUYOR, KosulDurumu.UYGUN_DEGIL)
            gerekceler.append(_gerekce(NedenKodu.AMAC_DESTEKLENIYOR, baglam.amac))

        # 5-6. Tercihler yalniz hard kapilardan sonra odun/gerekce uretir.
        eslesen_tercih = False
        for tercih in baglam.tercihler:
            bilgiler = [b for b in ailelere.get(tercih.iddia_ailesi, ()) if b.yayinlanabilir and b.bilgi_durumu is BilgiDurumu.BILINIYOR]
            if not bilgiler:
                odunler.append(_gerekce(NedenKodu.TERCIH_BILINMIYOR, tercih.kod))
                continue
            bilgi = sorted(bilgiler, key=lambda b: (b.surum_no, b.iddia_id))[-1]
            kullanilan.append(f"{bilgi.iddia_id}:{bilgi.surum_no}")
            if _deger_eslesiyor(bilgi.deger, tercih.beklenen_deger, tercih.karsilastirma):
                eslesen_tercih = True
                gerekceler.append(_gerekce(NedenKodu.TERCIH_DESTEKLENIYOR, tercih.kod))
            else:
                odunler.append(_gerekce(NedenKodu.TERCIH_DESTEKLENMIYOR, tercih.kod))

        tur = KararSonucuTuru.KOSULA_BAGLI_ONERILEBILIR if odunler or aday.yayin_durumu is YayinUygunlukDurumu.SINIRLI_YAYINLANABILIR else KararSonucuTuru.ONERILEBILIR
        return sonuc(tur, KosulDurumu.UYGUN)

    @staticmethod
    def servis_kullanilamiyor(baglam: KararBaglami, *, trace_reference: str | None = None) -> KararSonucu:
        gerekce = _gerekce(NedenKodu.SERVIS_GECICI_KULLANILAMIYOR)
        return KararSonucu(
            karar_id=hashlib.sha256(f"{baglam.karar_parmak_izi()}:unavailable".encode()).hexdigest()[:24],
            yer_id=None, canonical_id=None, sube_id=None, yer_ismi=None,
            karar_turu=KararSonucuTuru.SERVIS_GECICI_KULLANILAMIYOR,
            uygunluk=KosulDurumu.DEGERLENDIRILEMIYOR,
            anlasilan_ihtiyac={"amac": baglam.amac, "sehir": baglam.cografi_baglam.sehir},
            gerekceler=(), kritik_engeller=(), onemli_odunler=(), bilinmeyenler=(gerekce,),
            zaman_ve_kapsam={"sehir": baglam.cografi_baglam.sehir},
            bilgi_surumu=baglam.bilgi_surumu, politika_surumu=baglam.politika_surumu,
            yayin_surumu=None, kullanilan_iddia_surumleri=(), trace_reference=trace_reference,
        )
