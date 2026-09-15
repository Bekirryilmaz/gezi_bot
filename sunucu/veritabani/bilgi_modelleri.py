from __future__ import annotations

import uuid
from datetime import datetime

from geoalchemy2 import Geometry
from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
    text,
)
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
    uzun_sureli_saklama: Mapped[str] = mapped_column(
        String(20), nullable=False, default="bilinmiyor"
    )
    dayanak_notu: Mapped[str | None] = mapped_column(Text)
    gecerli_baslangic: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    gecerli_bitis: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    olusturulma_zamani: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


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
    sisteme_alinma_zamani: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    __table_args__ = (
        UniqueConstraint("kaynak", "kosu_anahtari", name="ux_veri_batch_kaynak_kosu"),
    )


class Gozlem(Taban):
    __tablename__ = "gozlemler"
    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=_uuid)
    veri_batch_id: Mapped[str] = mapped_column(
        ForeignKey("veri_batchleri.id", ondelete="RESTRICT"), nullable=False
    )
    kaynak: Mapped[str] = mapped_column(String(50), nullable=False)
    kaynak_kayit_id: Mapped[str] = mapped_column(String(255), nullable=False)
    kaynak_url: Mapped[str | None] = mapped_column(String(500))
    olay_zamani: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    kaynakta_gozlemlenme_zamani: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    cekilme_zamani: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    dogrulanma_zamani: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    sisteme_alinma_zamani: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    icerik_ozeti: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    icerik_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    __table_args__ = (
        UniqueConstraint(
            "veri_batch_id", "kaynak", "kaynak_kayit_id", "icerik_hash", name="ux_gozlem_idempotent"
        ),
        Index("ix_gozlem_kaynak_kayit", "kaynak", "kaynak_kayit_id"),
    )


class Iddia(Taban):
    __tablename__ = "iddialar"
    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=_uuid)
    sube_id: Mapped[str] = mapped_column(
        ForeignKey("subeler.id", ondelete="RESTRICT"), nullable=False
    )
    aile: Mapped[str] = mapped_column(String(40), nullable=False)
    kapsam: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    aktif_surum_no: Mapped[int | None] = mapped_column(Integer)
    olusturulma_zamani: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    __table_args__ = (Index("ix_iddia_sube_aile", "sube_id", "aile"),)


class IddiaSurumu(Taban):
    __tablename__ = "iddia_surumleri"
    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=_uuid)
    iddia_id: Mapped[str] = mapped_column(
        ForeignKey("iddialar.id", ondelete="CASCADE"), nullable=False
    )
    surum_no: Mapped[int] = mapped_column(Integer, nullable=False)
    deger: Mapped[dict] = mapped_column(JSONB, nullable=False)
    bilgi_durumu: Mapped[str] = mapped_column(String(20), nullable=False)
    guven_sinifi: Mapped[str] = mapped_column(String(20), nullable=False, default="belirsiz")
    gecerlilik_baslangici: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    gecerlilik_bitisi: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    dogrulanma_zamani: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    sisteme_alinma_zamani: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    yayin_durumu: Mapped[str] = mapped_column(String(30), nullable=False, default="taslak")
    yayin_engeli: Mapped[str | None] = mapped_column(String(100))
    ai_tarafindan_uretildi: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    __table_args__ = (UniqueConstraint("iddia_id", "surum_no", name="ux_iddia_surum_no"),)


class KanitBaglantisi(Taban):
    __tablename__ = "kanit_baglantilari"
    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=_uuid)
    iddia_surumu_id: Mapped[str] = mapped_column(
        ForeignKey("iddia_surumleri.id", ondelete="CASCADE"), nullable=False
    )
    gozlem_id: Mapped[str] = mapped_column(
        ForeignKey("gozlemler.id", ondelete="RESTRICT"), nullable=False
    )
    rol: Mapped[str] = mapped_column(String(20), nullable=False)
    gerekce: Mapped[str | None] = mapped_column(Text)
    __table_args__ = (
        UniqueConstraint("iddia_surumu_id", "gozlem_id", "rol", name="ux_kanit_baglantisi"),
    )


class DahiliGozlemAdayi(Taban):
    """NLP ciktisinin yayin ve iddia katmanlarindan ayrik kalici izi."""

    __tablename__ = "dahili_gozlem_adaylari"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        default=_uuid,
        server_default=text("gen_random_uuid()"),
    )
    veri_batch_id: Mapped[str] = mapped_column(
        ForeignKey("veri_batchleri.id", ondelete="RESTRICT"), nullable=False
    )
    yorum_id: Mapped[str] = mapped_column(
        ForeignKey("yorumlar.id", ondelete="RESTRICT"), nullable=False
    )
    kaynak: Mapped[str] = mapped_column(String(50), nullable=False)
    kaynak_kayit_id: Mapped[str] = mapped_column(String(255), nullable=False)
    kaynak_yer_id: Mapped[str] = mapped_column(String(255), nullable=False)
    sube_id: Mapped[str | None] = mapped_column(ForeignKey("subeler.id", ondelete="RESTRICT"))
    aile: Mapped[str] = mapped_column(String(50), nullable=False)
    gozlem_turu: Mapped[str] = mapped_column(String(30), nullable=False)
    yon: Mapped[str] = mapped_column(String(20), nullable=False)
    deger: Mapped[bool | str | dict] = mapped_column(JSONB, nullable=False)
    cikarim_yontemi: Mapped[str] = mapped_column(String(30), nullable=False)
    model_surumu: Mapped[str] = mapped_column(String(100), nullable=False)
    kural_surumu: Mapped[str] = mapped_column(String(100), nullable=False)
    cikarim_guven_sinifi: Mapped[str] = mapped_column(String(20), nullable=False)
    guven_kirilimi: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
        server_default=text("'{}'::jsonb"),
    )
    temporal_durum: Mapped[str] = mapped_column(String(30), nullable=False)
    gozlem_zamani: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    span_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    dahili_referans: Mapped[str] = mapped_column(String(80), nullable=False)
    sube_guven_durumu: Mapped[str] = mapped_column(String(30), nullable=False)
    kullanim_durumu: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="karantina",
        server_default=text("'karantina'"),
    )
    olusturulma_zamani: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    __table_args__ = (
        UniqueConstraint(
            "yorum_id",
            "model_surumu",
            "kural_surumu",
            "aile",
            "gozlem_turu",
            "yon",
            "span_hash",
            name="ux_dahili_gozlem_adayi_idempotent",
        ),
        CheckConstraint(
            "kullanim_durumu IN ('aktif', 'karantina')",
            name="ck_dahili_gozlem_adayi_kullanim",
        ),
        Index("ix_dahili_gozlem_adayi_batch", "veri_batch_id"),
        Index("ix_dahili_gozlem_adayi_yorum", "yorum_id"),
        Index(
            "ix_dahili_gozlem_adayi_sube_aile_kullanim",
            "sube_id",
            "aile",
            "kullanim_durumu",
        ),
        Index(
            "ix_dahili_gozlem_adayi_kaynak_kimlik",
            "kaynak",
            "kaynak_kayit_id",
            "kaynak_yer_id",
        ),
        Index("ix_dahili_gozlem_adayi_referans", "dahili_referans"),
    )


class DahiliSinyalOzeti(Taban):
    """Bir sube ve sinyal ailesi icin surumlu, aciklanabilir toplama sonucu."""

    __tablename__ = "dahili_sinyal_ozetleri"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        default=_uuid,
        server_default=text("gen_random_uuid()"),
    )
    sube_id: Mapped[str] = mapped_column(
        ForeignKey("subeler.id", ondelete="RESTRICT"), nullable=False
    )
    aile: Mapped[str] = mapped_column(String(50), nullable=False)
    agregasyon_surumu: Mapped[str] = mapped_column(String(100), nullable=False)
    guven_sinifi: Mapped[str] = mapped_column(String(20), nullable=False)
    durum: Mapped[str] = mapped_column(String(30), nullable=False)
    ozet: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
        server_default=text("'{}'::jsonb"),
    )
    kirilim: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
        server_default=text("'{}'::jsonb"),
    )
    hesaplanma_zamani: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    __table_args__ = (
        UniqueConstraint(
            "sube_id",
            "aile",
            "agregasyon_surumu",
            name="ux_dahili_sinyal_ozeti_sube_aile_surumu",
        ),
        Index(
            "ix_dahili_sinyal_ozeti_guven_durum",
            "guven_sinifi",
            "durum",
        ),
    )


class IlceSiniri(Taban):
    """Canonical ilcenin surumlu ve provenance tasiyan cografi siniri."""

    __tablename__ = "ilce_sinirlari"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        default=_uuid,
        server_default=text("gen_random_uuid()"),
    )
    ilce_id: Mapped[str] = mapped_column(
        ForeignKey("ilceler.id", ondelete="RESTRICT"), nullable=False
    )
    geometri: Mapped[str] = mapped_column(
        Geometry(geometry_type="MULTIPOLYGON", srid=4326, spatial_index=False),
        nullable=False,
    )
    kaynak: Mapped[str] = mapped_column(String(50), nullable=False)
    kaynak_kayit_id: Mapped[str] = mapped_column(String(255), nullable=False)
    veri_surumu: Mapped[str] = mapped_column(String(100), nullable=False)
    checksum: Mapped[str] = mapped_column(String(64), nullable=False)
    provenance: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
        server_default=text("'{}'::jsonb"),
    )
    cekilme_zamani: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "kaynak",
            "kaynak_kayit_id",
            "veri_surumu",
            name="ux_ilce_siniri_kaynak_kayit_surumu",
        ),
        Index("ix_ilce_siniri_ilce", "ilce_id"),
        Index("ix_ilce_siniri_geometri", "geometri", postgresql_using="gist"),
    )
