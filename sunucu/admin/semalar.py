from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class AdminLoginTalebi(BaseModel):
    eposta: str = Field(min_length=3, max_length=255)
    parola: str = Field(min_length=1, max_length=256)


class AdminKimlikCevabi(BaseModel):
    id: str
    eposta: str
    gorunen_ad: str
    roller: list[str]
    yetkiler: list[str]
    csrf_token: str | None = None


class IncelemeKomutu(BaseModel):
    eylem: str = Field(min_length=2, max_length=80)
    nesne_turu: str = Field(min_length=2, max_length=40)
    nesne_id: str = Field(min_length=1, max_length=100)
    gerekce: str = Field(min_length=8, max_length=2000)
    payload: dict[str, Any] = Field(default_factory=dict)
    beklenen_surum: int | None = Field(default=None, ge=1)


class IkinciIncelemeTalebi(BaseModel):
    gerekce: str = Field(min_length=8, max_length=2000)
    beklenen_surum: int = Field(ge=1)


class IncelemeDosyasiCevabi(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    dosya_turu: str
    nesne_turu: str
    nesne_id: str
    durum: str
    risk_sinifi: str
    onerilen_eylem: str | None
    karar_gerekcesi: str | None
    surum: int
    olusturulma_zamani: datetime


class EslemeAdayiCevabi(BaseModel):
    id: str
    sol_sube_id: str
    sag_sube_id: str
    confidence: float
    belirsizlik: dict[str, Any]
    durum: str


class ClaimIncelemeCevabi(BaseModel):
    id: str
    sube_id: str
    yer_id: str | None
    mekan_adi: str
    aile: str
    kapsam: dict[str, Any]
    aktif_surum_no: int | None
    surum: dict[str, Any] | None
    supporting_evidence: list[dict[str, Any]]
    counter_evidence: list[dict[str, Any]]
    yayin_onizleme: dict[str, Any]
    public_preview: dict[str, Any]


class ClaimOzetCevabi(BaseModel):
    id: str
    sube_id: str
    yer_id: str | None
    mekan_adi: str
    aile: str
    aktif_surum_no: int | None
    durum: str
    risk_sinifi: str
    kaynak: str | None
    kaynak_kayit_id: str | None
    kaynak_alani: str | None
    candidate_deger: Any


class ClaimSayfasiCevabi(BaseModel):
    kayitlar: list[ClaimOzetCevabi]
    toplam: int
    sayfa: int
    sayfa_boyutu: int


class BirlestirmeCevabi(BaseModel):
    id: str
    kaynak_sube_id: str
    hedef_sube_id: str
    birlestirme_zamani: datetime


class AuditCevabi(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    aktor_id: str
    eylem: str
    nesne_turu: str
    nesne_id: str
    onceki_durum_ref: str | None
    yeni_durum_ref: str | None
    gerekce: str
    istek_id: str
    korelasyon_id: str
    olusturulma_zamani: datetime
