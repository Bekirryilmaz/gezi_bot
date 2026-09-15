"""Dahili NLP adaylari, ozetleri ve ilce sinirlari.

Revision ID: 0015
Revises: 0014
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from geoalchemy2 import Geometry
from sqlalchemy.dialects.postgresql import JSONB, UUID

revision = "0015"
down_revision = "0014"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "dahili_gozlem_adaylari",
        sa.Column(
            "id",
            UUID(as_uuid=False),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column(
            "veri_batch_id",
            UUID(as_uuid=False),
            sa.ForeignKey("veri_batchleri.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column(
            "yorum_id",
            UUID(as_uuid=False),
            sa.ForeignKey("yorumlar.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("kaynak", sa.String(50), nullable=False),
        sa.Column("kaynak_kayit_id", sa.String(255), nullable=False),
        sa.Column("kaynak_yer_id", sa.String(255), nullable=False),
        sa.Column(
            "sube_id",
            UUID(as_uuid=False),
            sa.ForeignKey("subeler.id", ondelete="RESTRICT"),
            nullable=True,
        ),
        sa.Column("aile", sa.String(50), nullable=False),
        sa.Column("gozlem_turu", sa.String(30), nullable=False),
        sa.Column("yon", sa.String(20), nullable=False),
        sa.Column("deger", JSONB, nullable=False),
        sa.Column("cikarim_yontemi", sa.String(30), nullable=False),
        sa.Column("model_surumu", sa.String(100), nullable=False),
        sa.Column("kural_surumu", sa.String(100), nullable=False),
        sa.Column("cikarim_guven_sinifi", sa.String(20), nullable=False),
        sa.Column(
            "guven_kirilimi",
            JSONB,
            nullable=False,
            server_default=sa.text("'{}'::jsonb"),
        ),
        sa.Column("temporal_durum", sa.String(30), nullable=False),
        sa.Column("gozlem_zamani", sa.DateTime(timezone=True), nullable=True),
        sa.Column("span_hash", sa.String(64), nullable=False),
        sa.Column("dahili_referans", sa.String(80), nullable=False),
        sa.Column("sube_guven_durumu", sa.String(30), nullable=False),
        sa.Column(
            "kullanim_durumu",
            sa.String(20),
            nullable=False,
            server_default=sa.text("'karantina'"),
        ),
        sa.Column(
            "olusturulma_zamani",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.UniqueConstraint(
            "yorum_id",
            "model_surumu",
            "kural_surumu",
            "aile",
            "gozlem_turu",
            "yon",
            "span_hash",
            name="ux_dahili_gozlem_adayi_idempotent",
        ),
        sa.CheckConstraint(
            "kullanim_durumu IN ('aktif', 'karantina')",
            name="ck_dahili_gozlem_adayi_kullanim",
        ),
    )
    op.create_index(
        "ix_dahili_gozlem_adayi_batch",
        "dahili_gozlem_adaylari",
        ["veri_batch_id"],
    )
    op.create_index(
        "ix_dahili_gozlem_adayi_yorum",
        "dahili_gozlem_adaylari",
        ["yorum_id"],
    )
    op.create_index(
        "ix_dahili_gozlem_adayi_sube_aile_kullanim",
        "dahili_gozlem_adaylari",
        ["sube_id", "aile", "kullanim_durumu"],
    )
    op.create_index(
        "ix_dahili_gozlem_adayi_kaynak_kimlik",
        "dahili_gozlem_adaylari",
        ["kaynak", "kaynak_kayit_id", "kaynak_yer_id"],
    )
    op.create_index(
        "ix_dahili_gozlem_adayi_referans",
        "dahili_gozlem_adaylari",
        ["dahili_referans"],
    )

    op.create_table(
        "dahili_sinyal_ozetleri",
        sa.Column(
            "id",
            UUID(as_uuid=False),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column(
            "sube_id",
            UUID(as_uuid=False),
            sa.ForeignKey("subeler.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("aile", sa.String(50), nullable=False),
        sa.Column("agregasyon_surumu", sa.String(100), nullable=False),
        sa.Column("guven_sinifi", sa.String(20), nullable=False),
        sa.Column("durum", sa.String(30), nullable=False),
        sa.Column(
            "ozet",
            JSONB,
            nullable=False,
            server_default=sa.text("'{}'::jsonb"),
        ),
        sa.Column(
            "kirilim",
            JSONB,
            nullable=False,
            server_default=sa.text("'{}'::jsonb"),
        ),
        sa.Column(
            "hesaplanma_zamani",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.UniqueConstraint(
            "sube_id",
            "aile",
            "agregasyon_surumu",
            name="ux_dahili_sinyal_ozeti_sube_aile_surumu",
        ),
    )
    op.create_index(
        "ix_dahili_sinyal_ozeti_guven_durum",
        "dahili_sinyal_ozetleri",
        ["guven_sinifi", "durum"],
    )
    op.create_table(
        "ilce_sinirlari",
        sa.Column(
            "id",
            UUID(as_uuid=False),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column(
            "ilce_id",
            UUID(as_uuid=False),
            sa.ForeignKey("ilceler.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column(
            "geometri",
            Geometry(
                geometry_type="MULTIPOLYGON",
                srid=4326,
                spatial_index=False,
            ),
            nullable=False,
        ),
        sa.Column("kaynak", sa.String(50), nullable=False),
        sa.Column("kaynak_kayit_id", sa.String(255), nullable=False),
        sa.Column("veri_surumu", sa.String(100), nullable=False),
        sa.Column("checksum", sa.String(64), nullable=False),
        sa.Column(
            "provenance",
            JSONB,
            nullable=False,
            server_default=sa.text("'{}'::jsonb"),
        ),
        sa.Column("cekilme_zamani", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint(
            "kaynak",
            "kaynak_kayit_id",
            "veri_surumu",
            name="ux_ilce_siniri_kaynak_kayit_surumu",
        ),
    )
    op.create_index("ix_ilce_siniri_ilce", "ilce_sinirlari", ["ilce_id"])
    op.create_index(
        "ix_ilce_siniri_geometri",
        "ilce_sinirlari",
        ["geometri"],
        postgresql_using="gist",
    )


_NLP_TABLOLARI = (
    "dahili_gozlem_adaylari",
    "dahili_sinyal_ozetleri",
    "ilce_sinirlari",
)


def _veri_tasiyan_nlp_tablolari() -> list[str]:
    doluluk = (
        op.get_bind()
        .execute(
            sa.text(
                "SELECT "
                "EXISTS (SELECT 1 FROM dahili_gozlem_adaylari) AS aday_var, "
                "EXISTS (SELECT 1 FROM dahili_sinyal_ozetleri) AS ozet_var, "
                "EXISTS (SELECT 1 FROM ilce_sinirlari) AS sinir_var"
            )
        )
        .mappings()
        .one()
    )
    return [
        tablo
        for tablo, dolu_mu in zip(_NLP_TABLOLARI, doluluk.values(), strict=True)
        if dolu_mu
    ]


def _veri_varken_downgrade_yasakla() -> None:
    dolu_tablolar = _veri_tasiyan_nlp_tablolari()
    if dolu_tablolar:
        ayrinti = ", ".join(sorted(dolu_tablolar))
        raise RuntimeError(
            f"0015 downgrade veri kaybina yol acar; yeni tablolar bosaltilmali: {ayrinti}"
        )


def downgrade() -> None:
    # Once kontrol: hicbir DROP calismadan fail-closed. Kilit yalniz bos
    # oldugu dogrulandiktan sonra; kilit altinda tekrar kontrol TOCTOU icin.
    _veri_varken_downgrade_yasakla()
    op.execute(
        sa.text(
            "LOCK TABLE dahili_gozlem_adaylari, dahili_sinyal_ozetleri, "
            "ilce_sinirlari IN ACCESS EXCLUSIVE MODE"
        )
    )
    _veri_varken_downgrade_yasakla()

    op.drop_index("ix_ilce_siniri_geometri", table_name="ilce_sinirlari")
    op.drop_index("ix_ilce_siniri_ilce", table_name="ilce_sinirlari")
    op.drop_table("ilce_sinirlari")

    op.drop_index(
        "ix_dahili_sinyal_ozeti_guven_durum",
        table_name="dahili_sinyal_ozetleri",
    )
    op.drop_table("dahili_sinyal_ozetleri")

    op.drop_index(
        "ix_dahili_gozlem_adayi_referans",
        table_name="dahili_gozlem_adaylari",
    )
    op.drop_index(
        "ix_dahili_gozlem_adayi_kaynak_kimlik",
        table_name="dahili_gozlem_adaylari",
    )
    op.drop_index(
        "ix_dahili_gozlem_adayi_sube_aile_kullanim",
        table_name="dahili_gozlem_adaylari",
    )
    op.drop_index(
        "ix_dahili_gozlem_adayi_yorum",
        table_name="dahili_gozlem_adaylari",
    )
    op.drop_index(
        "ix_dahili_gozlem_adayi_batch",
        table_name="dahili_gozlem_adaylari",
    )
    op.drop_table("dahili_gozlem_adaylari")
