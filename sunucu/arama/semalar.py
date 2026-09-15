from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from sunucu.arama.domain import AramaSonucuTuru, EslesmeNedeni
from sunucu.karar_motoru.semalar import CografiBaglamSemasi, TercihSemasi, ZorunluKosulSemasi
from sunucu.karar_motoru.domain import KosulDurumu


class AramaYerKimligiSemasi(BaseModel):
    place_id: str
    canonical_id: str
    branch_id: str
    isim: str


class AramaCografyaSemasi(BaseModel):
    sehir_id: str
    sehir_anahtari: str
    sehir_ismi: str
    ilce_id: str | None = None
    ilce_ismi: str | None = None


class AramaSonucuSemasi(BaseModel):
    sonuc_turu: AramaSonucuTuru
    etiket: str
    yer: AramaYerKimligiSemasi | None = None
    cografya: AramaCografyaSemasi
    ana_kategori: str | None = None
    alt_kategori: str | None = None
    eslesme_nedeni: EslesmeNedeni
    yayin_durumu: Literal["yayinda"] = "yayinda"
    kosul_durumlari: dict[str, KosulDurumu] = Field(default_factory=dict)


class AramaFiltreBaglamiSemasi(BaseModel):
    """KararBaglami'ni kopyalamaz; onun mevcut alt sozlesmelerini tasir."""

    sehir_id: str
    ilce_id: str | None = None
    tur: str | None = None
    cografi_baglam: CografiBaglamSemasi
    zorunlu_kosullar: list[ZorunluKosulSemasi] = Field(default_factory=list)
    tercihler: list[TercihSemasi] = Field(default_factory=list)


class AramaCevabi(BaseModel):
    sorgu: str
    sonuclar: list[AramaSonucuSemasi]
    uygulanan_filtreler: AramaFiltreBaglamiSemasi
    sonraki_cursor: str | None = None
    degerlendirilemeyen_aday_sayisi: int = 0


class FiltreSecenegiSemasi(BaseModel):
    kod: str
    etiket: str
    iddia_ailesi: str


class IlceSecenegiSemasi(BaseModel):
    id: str
    isim: str
    sehir_id: str


class TurSecenegiSemasi(BaseModel):
    kod: str
    etiket: str


class AramaFiltreleriCevabi(BaseModel):
    sehir_id: str
    sehir_anahtari: str
    ilceler: list[IlceSecenegiSemasi]
    turler: list[TurSecenegiSemasi]
    somut_kosullar: list[FiltreSecenegiSemasi]
