from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Index, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from sunucu.veritabani.temel import Taban


def _uuid() -> str:
    return str(uuid.uuid4())


class YayinKaydi(Taban):
    __tablename__ = "yayin_kayitlari"
    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=_uuid)
    nesne_turu: Mapped[str] = mapped_column(String(30), nullable=False)
    nesne_id: Mapped[str] = mapped_column(UUID(as_uuid=False), nullable=False)
    durum: Mapped[str] = mapped_column(String(40), nullable=False, default="yayinlanamaz")
    neden_kodlari: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    izinli_kullanimlar: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    surum: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    aktif_mi: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    guncellenme_zamani: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    __table_args__ = (
        UniqueConstraint("nesne_turu", "nesne_id", name="ux_yayin_nesnesi"),
        Index("ix_yayin_durum_nesne", "durum", "nesne_turu"),
    )


class GeriCekmeKaydi(Taban):
    __tablename__ = "geri_cekme_kayitlari"
    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=_uuid)
    nesne_turu: Mapped[str] = mapped_column(String(30), nullable=False)
    nesne_id: Mapped[str] = mapped_column(UUID(as_uuid=False), nullable=False)
    kapsam: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    gerekce_kodu: Mapped[str] = mapped_column(String(80), nullable=False)
    gerekce: Mapped[str] = mapped_column(Text, nullable=False)
    aktor_id: Mapped[str] = mapped_column(UUID(as_uuid=False), nullable=False)
    geri_cekme_zamani: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class EtkiBaglantisi(Taban):
    __tablename__ = "etki_baglantilari"
    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=_uuid)
    kaynak_turu: Mapped[str] = mapped_column(String(30), nullable=False)
    kaynak_id: Mapped[str] = mapped_column(UUID(as_uuid=False), nullable=False)
    hedef_turu: Mapped[str] = mapped_column(String(30), nullable=False)
    hedef_id: Mapped[str] = mapped_column(UUID(as_uuid=False), nullable=False)
    bag_turu: Mapped[str] = mapped_column(String(40), nullable=False)
    aktif_mi: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    __table_args__ = (
        UniqueConstraint("kaynak_turu", "kaynak_id", "hedef_turu", "hedef_id", "bag_turu", name="ux_etki_bagi"),
        Index("ix_etki_kaynak", "kaynak_turu", "kaynak_id", "aktif_mi"),
    )


class GecersizlestirmeOlayi(Taban):
    __tablename__ = "gecersizlestirme_olaylari"
    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=_uuid)
    olay_anahtari: Mapped[str] = mapped_column(String(160), nullable=False, unique=True)
    kaynak_turu: Mapped[str] = mapped_column(String(30), nullable=False)
    kaynak_id: Mapped[str] = mapped_column(UUID(as_uuid=False), nullable=False)
    olay_turu: Mapped[str] = mapped_column(String(40), nullable=False)
    payload: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    olusturulma_zamani: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    islenme_zamani: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    deneme_sayisi: Mapped[int] = mapped_column(Integer, nullable=False, default=0)


class PublicProjection(Taban):
    __tablename__ = "public_projectionlar"
    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=_uuid)
    nesne_turu: Mapped[str] = mapped_column(String(30), nullable=False)
    nesne_id: Mapped[str] = mapped_column(UUID(as_uuid=False), nullable=False)
    yayin_surumu: Mapped[int] = mapped_column(Integer, nullable=False)
    etag: Mapped[str] = mapped_column(String(80), nullable=False)
    payload: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    gecersiz_mi: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    gecersizlestirme_zamani: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    __table_args__ = (UniqueConstraint("nesne_turu", "nesne_id", name="ux_public_projection"),)
