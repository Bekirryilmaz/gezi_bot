from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import Boolean, Computed, DateTime, ForeignKey, Index, String, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from sunucu.veritabani.temel import Taban


def _uuid() -> str:
    return str(uuid.uuid4())


class Ilce(Taban):
    """Bir sehre ait canonical ilce; serbest metin filtre anahtari degildir."""

    __tablename__ = "ilceler"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=_uuid)
    sehir_id: Mapped[str] = mapped_column(
        ForeignKey("sehirler.id", ondelete="RESTRICT"), nullable=False
    )
    isim: Mapped[str] = mapped_column(String(100), nullable=False)
    arama_isim: Mapped[str] = mapped_column(
        String(100), Computed("samandira_arama_normalize(isim)", persisted=True)
    )
    aktif_mi: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    olusturulma_zamani: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    __table_args__ = (
        UniqueConstraint("sehir_id", "arama_isim", name="ux_ilce_sehir_arama_isim"),
        Index("ix_ilceler_sehir_aktif", "sehir_id", "aktif_mi"),
    )
