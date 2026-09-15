from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from sunucu.karar_motoru.semalar import KararBaglamiSemasi
from sunucu.kesfet.semalar import KesfetDegerlendirmeCevabi

Amac = Literal["kahve_icmek", "yemek_yemek", "tarihi_kulturel_ziyaret"]


class BugunNiyetiSemasi(BaseModel):
    model_config = ConfigDict(extra="forbid")

    sehir: str = Field(default="Samsun", min_length=1, max_length=100)
    ilce: str | None = Field(default=None, max_length=100)
    amac: Amac | None = None
    kisi_baglami: str | None = Field(default=None, max_length=80)
    istenen_zaman: str | None = Field(default=None, max_length=40)
    sure_dakika: int | None = Field(default=None, ge=1, le=1440)
    ulasim_bicimi: str | None = Field(default=None, max_length=40)
    butce_ust_siniri: float | None = Field(default=None, ge=0)
    zorunlu_kosullar: list[str] = Field(default_factory=list, max_length=20)
    tercihler: list[str] = Field(default_factory=list, max_length=20)


class BugunNeYapalimTalebi(BaseModel):
    model_config = ConfigDict(extra="forbid")

    serbest_metin: str | None = Field(default=None, max_length=500)
    niyet: BugunNiyetiSemasi = Field(default_factory=BugunNiyetiSemasi)
    haric_yerler: list[str] = Field(default_factory=list, max_length=100)


class NetlestirmeSecenegiSemasi(BaseModel):
    deger: Amac
    etiket: str


class NetlestirmeSemasi(BaseModel):
    soru: str
    alan: Literal["amac"]
    secenekler: list[NetlestirmeSecenegiSemasi]


class BugunBaglamiSemasi(BaseModel):
    degerlendirme_zamani: str
    saat_dilimi: str
    ziyaret_tarihi: str
    aciklik_bilgisi: Literal["dogrulanmiyor"] = "dogrulanmiyor"
    aciklik_aciklamasi: str


class BugunNeYapalimCevabi(BaseModel):
    durum: Literal["clarification", "success", "empty", "insufficient"]
    anlasilan_ihtiyac_ozeti: str
    netlestirme: NetlestirmeSemasi | None = None
    baglam: KararBaglamiSemasi
    bugun_baglami: BugunBaglamiSemasi
    kesfet: KesfetDegerlendirmeCevabi | None = None
    kesfet_sorgusu: str | None = None
