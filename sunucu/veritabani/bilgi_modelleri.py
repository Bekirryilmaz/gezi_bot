from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Index, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from sunucu.veritabani.temel import Taban


def _uuid() -> str:
    return str(uuid.uuid4())


class KaynakPolitikasi(Taban):
    __tablename__ = "kaynak_politikalari"
    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=_uuid)
    kaynak: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    kamusal_gosterim: Mapped[str] = mapped_column(String(20), nullable=False, default="bilinmiyor")
    turev_iddia: Mapped[str] = mapped_column(String(20), nullable=False, default="bilinmiyor")
    ai_isleme: Mapped[str] = mapped_column(String(20), nullable=False, default="bilinmiyor")
    uzun_sureli_saklama: Mapped[str] = mapped_column(String(20), nullable=False, default="bilinmiyor")
    dayanak_notu: Mapped[str | None] = mapped_column(Text)
    gecerli_baslangic: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    gecerli_bitis: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    olusturulma_zamani: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class VeriBatch(Taban):
    __tablename__ = "veri_batchleri"
    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=_uuid)
    kaynak: Mapped[str] = mapped_column(String(50), nullable=False)
    kosu_anahtari: Mapped[str] = mapped_column(String(255), nullable=False)
    kok_tanimi: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    baslama_zamani: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    cekilme_baslangici: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    cekilme_bitisi: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    tamamlanma_zamani: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    sisteme_alinma_zamani: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    __table_args__ = (UniqueConstraint("kaynak", "kosu_anahtari", name="ux_veri_batch_kaynak_kosu"),)


class Gozlem(Taban):
    __tablename__ = "gozlemler"
    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=_uuid)
    veri_batch_id: Mapped[str] = mapped_column(ForeignKey("veri_batchleri.id", ondelete="RESTRICT"), nullable=False)
    kaynak: Mapped[str] = mapped_column(String(50), nullable=False)
    kaynak_kayit_id: Mapped[str] = mapped_column(String(255), nullable=False)
    kaynak_url: Mapped[str | None] = mapped_column(String(500))
    olay_zamani: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    kaynakta_gozlemlenme_zamani: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    cekilme_zamani: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    dogrulanma_zamani: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    sisteme_alinma_zamani: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    icerik_ozeti: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    icerik_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    __table_args__ = (UniqueConstraint("veri_batch_id", "kaynak", "kaynak_kayit_id", "icerik_hash", name="ux_gozlem_idempotent"), Index("ix_gozlem_kaynak_kayit", "kaynak", "kaynak_kayit_id"))


class Iddia(Taban):
    __tablename__ = "iddialar"
    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=_uuid)
    sube_id: Mapped[str] = mapped_column(ForeignKey("subeler.id", ondelete="RESTRICT"), nullable=False)
    aile: Mapped[str] = mapped_column(String(40), nullable=False)
    kapsam: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    aktif_surum_no: Mapped[int | None] = mapped_column(Integer)
    olusturulma_zamani: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    __table_args__ = (Index("ix_iddia_sube_aile", "sube_id", "aile"),)


class IddiaSurumu(Taban):
    __tablename__ = "iddia_surumleri"
    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=_uuid)
    iddia_id: Mapped[str] = mapped_column(ForeignKey("iddialar.id", ondelete="CASCADE"), nullable=False)
    surum_no: Mapped[int] = mapped_column(Integer, nullable=False)
    deger: Mapped[dict] = mapped_column(JSONB, nullable=False)
    bilgi_durumu: Mapped[str] = mapped_column(String(20), nullable=False)
    guven_sinifi: Mapped[str] = mapped_column(String(20), nullable=False, default="belirsiz")
    gecerlilik_baslangici: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    gecerlilik_bitisi: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    dogrulanma_zamani: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    sisteme_alinma_zamani: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    yayin_durumu: Mapped[str] = mapped_column(String(30), nullable=False, default="taslak")
    yayin_engeli: Mapped[str | None] = mapped_column(String(100))
    ai_tarafindan_uretildi: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    __table_args__ = (UniqueConstraint("iddia_id", "surum_no", name="ux_iddia_surum_no"),)


class KanitBaglantisi(Taban):
    __tablename__ = "kanit_baglantilari"
    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=_uuid)
    iddia_surumu_id: Mapped[str] = mapped_column(ForeignKey("iddia_surumleri.id", ondelete="CASCADE"), nullable=False)
    gozlem_id: Mapped[str] = mapped_column(ForeignKey("gozlemler.id", ondelete="RESTRICT"), nullable=False)
    rol: Mapped[str] = mapped_column(String(20), nullable=False)
    gerekce: Mapped[str | None] = mapped_column(Text)
    __table_args__ = (UniqueConstraint("iddia_surumu_id", "gozlem_id", "rol", name="ux_kanit_baglantisi"),)

