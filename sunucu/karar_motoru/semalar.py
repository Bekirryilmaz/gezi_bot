from __future__ import annotations

from datetime import date, time
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from sunucu.karar_motoru.domain import (
    CografiBaglam, Karsilastirma, KararBaglami, KararGerekcesi, KararSonucu,
    KararSonucuTuru, KosulDurumu, Tercih, ZamanBaglami, ZorunluKosul,
)


class ZamanBaglamiSemasi(BaseModel):
    model_config = ConfigDict(extra="forbid")
    ziyaret_tarihi: date | None = None
    baslangic: time | None = None
    bitis: time | None = None


class CografiBaglamSemasi(BaseModel):
    model_config = ConfigDict(extra="forbid")
    sehir: str = Field(min_length=1, max_length=100)
    ilce: str | None = Field(default=None, max_length=100)
    alan: str | None = Field(default=None, max_length=160)


class ZorunluKosulSemasi(BaseModel):
    model_config = ConfigDict(extra="forbid")
    kod: str = Field(min_length=1, max_length=80)
    iddia_ailesi: str = Field(min_length=1, max_length=80)
    beklenen_deger: Any
    karsilastirma: Karsilastirma = Karsilastirma.ESITTIR
    kritik: bool = True


class TercihSemasi(BaseModel):
    model_config = ConfigDict(extra="forbid")
    kod: str = Field(min_length=1, max_length=80)
    iddia_ailesi: str = Field(min_length=1, max_length=80)
    beklenen_deger: Any
    karsilastirma: Karsilastirma = Karsilastirma.ESITTIR
    oncelik: int = Field(default=1, ge=1, le=5)


class KararBaglamiSemasi(BaseModel):
    model_config = ConfigDict(extra="forbid")
    amac: str | None = Field(default=None, max_length=120)
    zaman: ZamanBaglamiSemasi = Field(default_factory=ZamanBaglamiSemasi)
    cografi_baglam: CografiBaglamSemasi
    baslangic_noktasi: str | None = Field(default=None, max_length=300)
    ulasim_bicimi: str | None = Field(default=None, max_length=40)
    kisi_sayisi: int | None = Field(default=None, ge=1, le=100)
    butce_ust_siniri: float | None = Field(default=None, ge=0)
    sure_ust_siniri_dakika: int | None = Field(default=None, ge=1, le=1440)
    zorunlu_kosullar: list[ZorunluKosulSemasi] = Field(default_factory=list, max_length=30)
    tercihler: list[TercihSemasi] = Field(default_factory=list, max_length=30)
    reddedilen_yerler: list[str] = Field(default_factory=list, max_length=100)
    sabitlenen_yerler: list[str] = Field(default_factory=list, max_length=100)
    anlasilmayan_kritik_girdiler: list[str] = Field(default_factory=list, max_length=20)
    bilgi_surumu: str = Field(default="bilinmiyor", max_length=80)
    politika_surumu: str = Field(default="karar-v1", max_length=80)

    def domaine(self, giris_kanali: str | None = None) -> KararBaglami:
        return KararBaglami(
            amac=self.amac,
            cografi_baglam=CografiBaglam(**self.cografi_baglam.model_dump()),
            zaman=ZamanBaglami(**self.zaman.model_dump()),
            baslangic_noktasi=self.baslangic_noktasi, ulasim_bicimi=self.ulasim_bicimi,
            kisi_sayisi=self.kisi_sayisi, butce_ust_siniri=self.butce_ust_siniri,
            sure_ust_siniri_dakika=self.sure_ust_siniri_dakika,
            zorunlu_kosullar=tuple(ZorunluKosul(**k.model_dump()) for k in self.zorunlu_kosullar),
            tercihler=tuple(Tercih(**t.model_dump()) for t in self.tercihler),
            reddedilen_yerler=frozenset(self.reddedilen_yerler),
            sabitlenen_yerler=frozenset(self.sabitlenen_yerler),
            anlasilmayan_kritik_girdiler=tuple(self.anlasilmayan_kritik_girdiler),
            bilgi_surumu=self.bilgi_surumu, politika_surumu=self.politika_surumu,
            giris_kanali=giris_kanali,
        )


class KararDegerlendirmeTalebi(BaseModel):
    model_config = ConfigDict(extra="forbid")
    baglam: KararBaglamiSemasi
    aday_yer_idleri: list[str] = Field(min_length=1, max_length=50)
    giris_kanali: Literal["kesfet", "bugun_ne_yapalim", "akilli_rota", "diger"] = "diger"


class KararGerekcesiSemasi(BaseModel):
    kod: str
    mesaj: str
    ilgili_kosul: str | None = None

    @classmethod
    def domainden(cls, deger: KararGerekcesi) -> "KararGerekcesiSemasi":
        return cls(kod=deger.kod.value, mesaj=deger.mesaj, ilgili_kosul=deger.ilgili_kosul)


class YerKimligiSemasi(BaseModel):
    place_id: str
    canonical_id: str
    branch_id: str
    isim: str


class KararSonucuSemasi(BaseModel):
    """Public allow-list; ic skor, ham kanit, yorum, model confidence ve sponsor yoktur."""
    karar_id: str
    yer: YerKimligiSemasi | None
    karar_turu: KararSonucuTuru
    anlasilan_ihtiyac: dict[str, Any]
    uygunluk: KosulDurumu
    gerekceler: list[KararGerekcesiSemasi]
    kritik_engeller: list[KararGerekcesiSemasi]
    onemli_odunler: list[KararGerekcesiSemasi]
    bilinmeyenler: list[KararGerekcesiSemasi]
    zaman_ve_kapsam: dict[str, Any]
    bilgi_surumu: str
    politika_surumu: str
    yayin_surumu: int | None
    anlamli_alternatif_farki: str | None = None
    trace_reference: str | None

    @classmethod
    def domainden(cls, deger: KararSonucu) -> "KararSonucuSemasi":
        yer = None
        if deger.yer_id and deger.canonical_id and deger.sube_id and deger.yer_ismi:
            yer = YerKimligiSemasi(place_id=deger.yer_id, canonical_id=deger.canonical_id, branch_id=deger.sube_id, isim=deger.yer_ismi)
        return cls(
            karar_id=deger.karar_id, yer=yer, karar_turu=deger.karar_turu,
            anlasilan_ihtiyac=deger.anlasilan_ihtiyac, uygunluk=deger.uygunluk,
            gerekceler=[KararGerekcesiSemasi.domainden(x) for x in deger.gerekceler],
            kritik_engeller=[KararGerekcesiSemasi.domainden(x) for x in deger.kritik_engeller],
            onemli_odunler=[KararGerekcesiSemasi.domainden(x) for x in deger.onemli_odunler],
            bilinmeyenler=[KararGerekcesiSemasi.domainden(x) for x in deger.bilinmeyenler],
            zaman_ve_kapsam=deger.zaman_ve_kapsam, bilgi_surumu=deger.bilgi_surumu,
            politika_surumu=deger.politika_surumu, yayin_surumu=deger.yayin_surumu,
            anlamli_alternatif_farki=deger.anlamli_alternatif_farki,
            trace_reference=deger.trace_reference,
        )


class KararDegerlendirmeCevabi(BaseModel):
    sonuclar: list[KararSonucuSemasi]
    trace_reference: str
