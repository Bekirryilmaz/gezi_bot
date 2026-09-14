from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Index, String, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from sunucu.veritabani.temel import Taban


def _uuid() -> str:
    return str(uuid.uuid4())


class YerKimligi(Taban):
    __tablename__ = "yer_kimlikleri"
    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=_uuid)
    sehir_id: Mapped[str] = mapped_column(ForeignKey("sehirler.id", ondelete="RESTRICT"), nullable=False)
    durum: Mapped[str] = mapped_column(String(20), nullable=False, default="aktif")
    olusturulma_zamani: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class Sube(Taban):
    __tablename__ = "subeler"
    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=_uuid)
    yer_kimligi_id: Mapped[str] = mapped_column(ForeignKey("yer_kimlikleri.id", ondelete="RESTRICT"), nullable=False)
    legacy_yer_id: Mapped[str | None] = mapped_column(ForeignKey("yerler.id", ondelete="SET NULL"), unique=True)
    guncel_isim: Mapped[str] = mapped_column(String(255), nullable=False)
    durum: Mapped[str] = mapped_column(String(20), nullable=False, default="aktif")
    yonlendirilen_sube_id: Mapped[str | None] = mapped_column(ForeignKey("subeler.id", ondelete="RESTRICT"))
    olusturulma_zamani: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class YerAlias(Taban):
    __tablename__ = "yer_aliaslari"
    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=_uuid)
    sube_id: Mapped[str] = mapped_column(ForeignKey("subeler.id", ondelete="CASCADE"), nullable=False)
    alias_turu: Mapped[str] = mapped_column(String(30), nullable=False)
    alias_degeri: Mapped[str] = mapped_column(String(255), nullable=False)
    aktif_mi: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    __table_args__ = (UniqueConstraint("alias_turu", "alias_degeri", name="ux_yer_alias_tur_deger"),)


class EslemeAdayi(Taban):
    __tablename__ = "esleme_adaylari"
    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=_uuid)
    sol_sube_id: Mapped[str] = mapped_column(ForeignKey("subeler.id", ondelete="RESTRICT"), nullable=False)
    sag_sube_id: Mapped[str] = mapped_column(ForeignKey("subeler.id", ondelete="RESTRICT"), nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    belirsizlik: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    durum: Mapped[str] = mapped_column(String(20), nullable=False, default="bekliyor")
    olusturulma_zamani: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    __table_args__ = (UniqueConstraint("sol_sube_id", "sag_sube_id", name="ux_esleme_adayi_cift"),)


class EslemeKarari(Taban):
    __tablename__ = "esleme_kararlari"
    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=_uuid)
    aday_id: Mapped[str | None] = mapped_column(ForeignKey("esleme_adaylari.id", ondelete="SET NULL"))
    karar: Mapped[str] = mapped_column(String(30), nullable=False)
    gerekce: Mapped[str] = mapped_column(Text, nullable=False)
    confidence: Mapped[float | None] = mapped_column(Float)
    manuel_override: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    karar_zamani: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class YerBirlestirmesi(Taban):
    __tablename__ = "yer_birlestirmeleri"
    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=_uuid)
    kaynak_sube_id: Mapped[str] = mapped_column(ForeignKey("subeler.id", ondelete="RESTRICT"), nullable=False)
    hedef_sube_id: Mapped[str] = mapped_column(ForeignKey("subeler.id", ondelete="RESTRICT"), nullable=False)
    karar_id: Mapped[str] = mapped_column(ForeignKey("esleme_kararlari.id", ondelete="RESTRICT"), nullable=False)
    tasinan_kaynak_idleri: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    aktif_mi: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    birlestirme_zamani: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    geri_alinma_zamani: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    __table_args__ = (Index("ix_yer_birlestirme_kaynak_aktif", "kaynak_sube_id", "aktif_mi"),)
