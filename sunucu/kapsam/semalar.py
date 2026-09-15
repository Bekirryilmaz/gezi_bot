from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from sunucu.karar_motoru.semalar import KararSonucuSemasi, YerKimligiSemasi


class KamusalCografyaSemasi(BaseModel):
    sehir_id: str
    sehir_anahtari: str
    sehir_ismi: str
    ilce_id: str | None = None
    ilce_slug: str | None = None
    ilce_ismi: str | None = None


class YayimlanmisBilgiSemasi(BaseModel):
    aile: str
    deger: Any
    kapsam: dict[str, Any] = Field(default_factory=dict)
    gecerlilik_baslangici: datetime | None = None
    gecerlilik_bitisi: datetime | None = None
    dogrulanma_zamani: datetime | None = None
    guncellik_anlami: str


class DuzeltmeGirisiSemasi(BaseModel):
    etiket: str = "Bilgi hatalı mı?"
    aciklama: str
    href: str | None = None


class KamusalYerDetayiSemasi(BaseModel):
    yer: YerKimligiSemasi
    cografya: KamusalCografyaSemasi
    ana_kategori: str
    alt_kategori: str
    adres: str | None = None
    aciklama: str | None = None
    telefon: str | None = None
    web_sitesi: str | None = None
    enlem: float
    boylam: float
    fotograf_urlleri: list[str] = Field(default_factory=list)
    pratik_bilgiler: list[YayimlanmisBilgiSemasi] = Field(default_factory=list)
    karar_sonucu: KararSonucuSemasi | None = None
    kritik_bilinmeyenler: list[str] = Field(default_factory=list)
    kapsam_anlami: str
    duzeltme_girisi: DuzeltmeGirisiSemasi


class IlceKapsamiSemasi(BaseModel):
    id: str
    isim: str
    slug: str
    yayinlanmis_yer_turleri: list[str]
    ayri_sayfa_var: bool
    kesfet_url: str


class SehirKapsamiSemasi(BaseModel):
    sehir_id: str
    sehir_anahtari: str
    sehir_ismi: str
    manifest_surumu: str
    kimlik_aramasi_destekleniyor: bool
    karar_kapsami_destekleniyor: bool
    yayinlanmis_yer_sayisi: int
    desteklenen_yer_turleri: list[str]
    desteklenen_iddia_aileleri: list[str]
    ilceler: list[IlceKapsamiSemasi]
    kapsam_aciklamasi: str


class IlceDetayiSemasi(BaseModel):
    cografya: KamusalCografyaSemasi
    ayri_sayfa_var: bool
    ozgun_karar_bilgileri: list[str] = Field(default_factory=list)
    yayinlanmis_yer_turleri: list[str] = Field(default_factory=list)
    kesfet_url: str
    kapsam_aciklamasi: str

