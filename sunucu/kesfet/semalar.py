from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from sunucu.arama.semalar import AramaCografyaSemasi, AramaYerKimligiSemasi
from sunucu.karar_motoru.semalar import KararBaglamiSemasi, KararSonucuSemasi


class KesfetAramaBaglamiSemasi(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ilce_id: str | None = None
    tur: str | None = Field(default=None, max_length=50)


class KesfetDegerlendirmeTalebi(BaseModel):
    model_config = ConfigDict(extra="forbid")

    sorgu: str = Field(min_length=1, max_length=120)
    baglam: KararBaglamiSemasi
    arama: KesfetAramaBaglamiSemasi = Field(default_factory=KesfetAramaBaglamiSemasi)
    hedef_sayi: int = Field(default=5, ge=3, le=5)
    haric_yerler: list[str] = Field(default_factory=list, max_length=100)


class KesfetSecenegiSemasi(BaseModel):
    yer: AramaYerKimligiSemasi
    cografya: AramaCografyaSemasi
    ana_kategori: str | None = None
    alt_kategori: str | None = None
    neden_bu: str
    anlamli_fark: str
    karar_sonucu: KararSonucuSemasi


class KesfetDegerlendirmeCevabi(BaseModel):
    durum: Literal["success", "empty", "insufficient"]
    secenekler: list[KesfetSecenegiSemasi]
    kimlik_eslesmeleri: list[AramaYerKimligiSemasi] = Field(default_factory=list)
    kullanilan_baglam: dict[str, object]
    sinirlama_nedeni: str
    degerlendirilemeyen_aday_sayisi: int = 0
    daha_fazla_var_mi: bool = False
    trace_reference: str | None = None

