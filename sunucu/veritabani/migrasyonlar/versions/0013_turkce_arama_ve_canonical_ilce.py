"""Turkce arama indeksleri ve canonical ilce baglari.

Revision ID: 0013
Revises: 0012
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

revision = "0013"
down_revision = "0012"
branch_labels = depends_on = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm")
    op.execute(
        """
        CREATE OR REPLACE FUNCTION samandira_arama_normalize(girdi text)
        RETURNS text
        LANGUAGE sql
        IMMUTABLE
        PARALLEL SAFE
        RETURN trim(regexp_replace(
          lower(translate(coalesce(girdi, ''), 'ÇĞİIÖŞÜçğıöşü', 'CGIIOSUcgiosu')),
          '[^a-z0-9]+', ' ', 'g'
        ))
        """
    )

    op.add_column(
        "sehirler",
        sa.Column(
            "arama_isim",
            sa.String(100),
            sa.Computed("samandira_arama_normalize(isim)", persisted=True),
            nullable=False,
        ),
    )
    op.add_column(
        "yerler",
        sa.Column(
            "arama_isim",
            sa.String(255),
            sa.Computed("samandira_arama_normalize(isim)", persisted=True),
            nullable=False,
        ),
    )

    op.create_table(
        "ilceler",
        sa.Column("id", UUID(as_uuid=False), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("sehir_id", UUID(as_uuid=False), sa.ForeignKey("sehirler.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("isim", sa.String(100), nullable=False),
        sa.Column(
            "arama_isim",
            sa.String(100),
            sa.Computed("samandira_arama_normalize(isim)", persisted=True),
            nullable=False,
        ),
        sa.Column("aktif_mi", sa.Boolean, nullable=False, server_default=sa.true()),
        sa.Column("olusturulma_zamani", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint("sehir_id", "arama_isim", name="ux_ilce_sehir_arama_isim"),
    )
    op.create_index("ix_ilceler_sehir_aktif", "ilceler", ["sehir_id", "aktif_mi"])

    resmi_ilceler = (
        "Atakum", "İlkadım", "Canik", "Tekkeköy", "Bafra", "Çarşamba",
        "Terme", "Salıpazarı", "Ayvacık", "Vezirköprü", "Havza", "Kavak",
        "Ladik", "Alaçam", "Yakakent", "19 Mayıs", "Asarcık",
    )
    ilce_degerleri = ",".join(
        "(" + op.inline_literal(isim).compile(dialect=op.get_bind().dialect).string + ")"
        for isim in resmi_ilceler
    )
    op.execute(
        sa.text(
            f"""
            INSERT INTO ilceler (sehir_id, isim)
            SELECT s.id, v.isim
            FROM sehirler s
            CROSS JOIN (VALUES {ilce_degerleri}) AS v(isim)
            WHERE samandira_arama_normalize(s.isim) = 'samsun'
            ON CONFLICT (sehir_id, arama_isim) DO NOTHING
            """
        )
    )

    op.add_column("yerler", sa.Column("ilce_id", UUID(as_uuid=False), nullable=True))
    op.create_foreign_key(
        "fk_yerler_ilce_id_ilceler", "yerler", "ilceler", ["ilce_id"], ["id"], ondelete="RESTRICT"
    )
    op.execute(
        """
        UPDATE yerler y
        SET ilce_id = i.id
        FROM ilceler i
        WHERE i.sehir_id = y.sehir_id
          AND i.arama_isim = samandira_arama_normalize(y.ilce)
        """
    )
    op.create_index("ix_yerler_ilce_id", "yerler", ["ilce_id"])
    op.create_index(
        "ix_yerler_arama_isim_prefix",
        "yerler",
        ["arama_isim"],
        postgresql_ops={"arama_isim": "text_pattern_ops"},
    )
    op.create_index(
        "ix_yerler_arama_isim_trgm",
        "yerler",
        ["arama_isim"],
        postgresql_using="gin",
        postgresql_ops={"arama_isim": "gin_trgm_ops"},
    )


def downgrade() -> None:
    op.drop_index("ix_yerler_arama_isim_trgm", table_name="yerler")
    op.drop_index("ix_yerler_arama_isim_prefix", table_name="yerler")
    op.drop_index("ix_yerler_ilce_id", table_name="yerler")
    op.drop_constraint("fk_yerler_ilce_id_ilceler", "yerler", type_="foreignkey")
    op.drop_column("yerler", "ilce_id")
    op.drop_index("ix_ilceler_sehir_aktif", table_name="ilceler")
    op.drop_table("ilceler")
    op.drop_column("yerler", "arama_isim")
    op.drop_column("sehirler", "arama_isim")
    op.execute("DROP FUNCTION IF EXISTS samandira_arama_normalize(text)")
    # pg_trgm paylasilan bir extension olabilir; guvenli downgrade onu silmez.
