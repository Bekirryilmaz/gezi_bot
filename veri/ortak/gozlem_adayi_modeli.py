from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ortak.sabitler import VeriKaynagi


class CikarimGuvenSinifi(StrEnum):
    DUSUK = "dusuk"
    ORTA = "orta"
    YUKSEK = "yuksek"


class IncelemeDurumu(StrEnum):
    BEKLIYOR = "bekliyor"
    INCELEMEDE = "incelemede"
    KABUL = "kabul"
    RED = "red"


class AdayGozlem(BaseModel):
    """NLP'nin tek ciktisi; kanit, claim, yayin veya uygunluk degildir."""
    model_config = ConfigDict(extra="forbid")

    kaynak: VeriKaynagi
    kaynak_kayit_id: str | None = None
    yer_adayi: str = Field(description="Kaynak yer kimligi veya eslesme adayi")
    sube_adayi: str | None = None
    span: str = Field(description="Cikarimin baglandigi sinirli kaynak parcasi")
    konu: str
    tahmini_gozlem: dict[str, Any]
    zaman_kapsami: dict[str, Any] = Field(default_factory=dict)
    model_surumu: str
    cikarim_guven_sinifi: CikarimGuvenSinifi
    inceleme_durumu: IncelemeDurumu = IncelemeDurumu.BEKLIYOR
    olusturulma_zamani: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def otomatik_yayinlanabilir(self) -> bool:
        return False
