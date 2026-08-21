"""
Yorum (review) verisi icin ortak modeller.

Iki asamali tasarim:
1. HamYorum: toplayicilarin dogrudan kaynaktan cektigi, henuz duygu analizi
   yapilmamis ham yorum.
2. IslenmisYorum: veri/duygu_analizi pipeline'inin HamYorum'a duygu skoru ve
   konu (aspect) etiketleri ekleyerek urettigi son hali. Rota algoritmasini
   besleyen veri budur.
"""

from __future__ import annotations

from datetime import datetime, timezone

from pydantic import BaseModel, Field

from ortak.sabitler import DuyguEtiketi, VeriKaynagi


class HamYorum(BaseModel):
    """Bir kaynaktan oldugu gibi cekilen, islenmemis yorum."""

    kaynak: VeriKaynagi
    kaynak_yer_id: str = Field(..., description="Yorumun ait oldugu yerin kaynaktaki kimligi")
    kaynak_yorum_id: str | None = Field(default=None, description="Kaynakta yorumun kendi kimligi varsa")

    # Gizlilik notu: yazar adi zorunlu degildir, mumkun oldugunca saklanmaz.
    # Sadece kamuya acik takma ad (Google/Eksi Sozluk kullanici adi gibi)
    # tutulur, gercek kisisel bilgi (telefon, e-posta vb.) asla saklanmaz.
    yazar_takma_adi: str | None = None

    yorum_metni: str
    kaynakta_puan: float | None = Field(default=None, ge=0, le=5)
    yorum_tarihi: datetime | None = None
    dil: str = "tr"
    cekilme_zamani: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def benzersiz_anahtar(self) -> str:
        if self.kaynak_yorum_id:
            return f"{self.kaynak.value}:{self.kaynak_yorum_id}"
        # Kaynakta ayri bir yorum id'si yoksa (orn. bazi scraping durumlari),
        # metin + yer + yazar birlesimi tekillik icin yeterince guvenilirdir.
        return f"{self.kaynak.value}:{self.kaynak_yer_id}:{self.yazar_takma_adi}:{hash(self.yorum_metni)}"


class KonuDuygusu(BaseModel):
    """Bir yorumun tek bir konu (aspect) hakkindaki duygusu.

    Orn: "manzarasi harikaydi ama fiyatlar biraz yuksekti" yorumu icin:
      [{"konu": "manzara", "duygu_etiketi": "olumlu"}, {"konu": "fiyat", "duygu_etiketi": "olumsuz"}]
    """

    konu: str
    duygu_etiketi: DuyguEtiketi
    gecen_ifade: str | None = Field(default=None, description="Bu tespiti tetikleyen orijinal ifade (aciklanabilirlik icin)")


class IslenmisYorum(HamYorum):
    """HamYorum + duygu analizi pipeline'inin urettigi ek alanlar."""

    duygu_skoru: float = Field(..., ge=-1, le=1, description="-1 tamamen olumsuz, +1 tamamen olumlu")
    duygu_etiketi: DuyguEtiketi
    konu_duygulari: list[KonuDuygusu] = Field(default_factory=list)
    analiz_model_adi: str = Field(..., description="Kullanilan duygu analizi modelinin adi (izlenebilirlik icin)")
    analiz_zamani: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
