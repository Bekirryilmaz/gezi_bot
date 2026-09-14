from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Index, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from sunucu.veritabani.temel import Taban


def _uuid() -> str:
    return str(uuid.uuid4())


class AdminKullanici(Taban):
    __tablename__ = "admin_kullanicilari"
    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=_uuid)
    eposta: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    gorunen_ad: Mapped[str] = mapped_column(String(120), nullable=False)
    parola_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    parola_salt: Mapped[str] = mapped_column(String(64), nullable=False)
    kapsam: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    aktif_mi: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    olusturulma_zamani: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class AdminRol(Taban):
    __tablename__ = "admin_rolleri"
    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=_uuid)
    kod: Mapped[str] = mapped_column(String(60), nullable=False, unique=True)
    aciklama: Mapped[str | None] = mapped_column(String(255))


class AdminKullaniciRolu(Taban):
    __tablename__ = "admin_kullanici_rolleri"
    kullanici_id: Mapped[str] = mapped_column(ForeignKey("admin_kullanicilari.id", ondelete="CASCADE"), primary_key=True)
    rol_id: Mapped[str] = mapped_column(ForeignKey("admin_rolleri.id", ondelete="CASCADE"), primary_key=True)


class AdminOturum(Taban):
    __tablename__ = "admin_oturumlari"
    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=_uuid)
    kullanici_id: Mapped[str] = mapped_column(ForeignKey("admin_kullanicilari.id", ondelete="CASCADE"), nullable=False)
    token_hash: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    csrf_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    sona_erme_zamani: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    ip_izi: Mapped[str | None] = mapped_column(String(64))
    user_agent_izi: Mapped[str | None] = mapped_column(String(64))
    iptal_zamani: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    olusturulma_zamani: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    __table_args__ = (Index("ix_admin_oturum_kullanici_sona_erme", "kullanici_id", "sona_erme_zamani"),)


class AdminAuditOlayi(Taban):
    __tablename__ = "admin_audit_olaylari"
    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=_uuid)
    aktor_id: Mapped[str] = mapped_column(ForeignKey("admin_kullanicilari.id", ondelete="RESTRICT"), nullable=False)
    eylem: Mapped[str] = mapped_column(String(80), nullable=False)
    nesne_turu: Mapped[str] = mapped_column(String(40), nullable=False)
    nesne_id: Mapped[str] = mapped_column(String(100), nullable=False)
    onceki_durum_ref: Mapped[str | None] = mapped_column(String(160))
    yeni_durum_ref: Mapped[str | None] = mapped_column(String(160))
    gerekce: Mapped[str] = mapped_column(Text, nullable=False)
    istek_id: Mapped[str] = mapped_column(String(100), nullable=False)
    korelasyon_id: Mapped[str] = mapped_column(String(100), nullable=False)
    meta: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    olusturulma_zamani: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    __table_args__ = (Index("ix_admin_audit_nesne", "nesne_turu", "nesne_id", "olusturulma_zamani"),)


class IncelemeDosyasi(Taban):
    __tablename__ = "inceleme_dosyalari"
    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=_uuid)
    dosya_turu: Mapped[str] = mapped_column(String(40), nullable=False)
    nesne_turu: Mapped[str] = mapped_column(String(40), nullable=False)
    nesne_id: Mapped[str] = mapped_column(String(100), nullable=False)
    durum: Mapped[str] = mapped_column(String(30), nullable=False, default="bekliyor")
    risk_sinifi: Mapped[str] = mapped_column(String(20), nullable=False, default="dusuk")
    onerilen_eylem: Mapped[str | None] = mapped_column(String(80))
    komut_payload: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    acan_aktor_id: Mapped[str] = mapped_column(ForeignKey("admin_kullanicilari.id", ondelete="RESTRICT"), nullable=False)
    atanan_aktor_id: Mapped[str | None] = mapped_column(ForeignKey("admin_kullanicilari.id", ondelete="SET NULL"))
    ikinci_inceleyen_id: Mapped[str | None] = mapped_column(ForeignKey("admin_kullanicilari.id", ondelete="RESTRICT"))
    karar_gerekcesi: Mapped[str | None] = mapped_column(Text)
    surum: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    olusturulma_zamani: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    guncellenme_zamani: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    __table_args__ = (Index("ix_inceleme_kuyruk", "durum", "dosya_turu", "risk_sinifi"),)
