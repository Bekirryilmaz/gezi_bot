from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, Index, String, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from sunucu.veritabani.temel import Taban


def _uuid() -> str:
    return str(uuid.uuid4())


class KararIzi(Taban):
    """Ham kullanici metni veya hassas konum icermeyen asgari karar izi."""
    __tablename__ = "karar_izleri"
    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=_uuid)
    trace_reference: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    request_id: Mapped[str] = mapped_column(String(100), nullable=False)
    correlation_id: Mapped[str] = mapped_column(String(100), nullable=False)
    context_fingerprint: Mapped[str] = mapped_column(String(64), nullable=False)
    politika_surumu: Mapped[str] = mapped_column(String(80), nullable=False)
    bilgi_surumu: Mapped[str] = mapped_column(String(80), nullable=False)
    claim_surumleri: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    yayin_surumleri: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    reason_kodlari: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    karar_zamani: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    __table_args__ = (
        Index("ix_karar_izi_context", "context_fingerprint", "politika_surumu", "bilgi_surumu"),
        Index("ix_karar_izi_karar_zamani", "karar_zamani"),
    )
