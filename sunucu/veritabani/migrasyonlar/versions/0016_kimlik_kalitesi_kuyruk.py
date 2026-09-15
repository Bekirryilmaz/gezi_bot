"""Kimlik kalitesi ve inceleme kuyrugu onceligi.

Revision ID: 0016
Revises: 0015
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision = "0016"
down_revision = "0015"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "subeler",
        sa.Column(
            "kimlik_kalite_sinifi",
            sa.String(20),
            nullable=False,
            server_default=sa.text("'kullanilabilir'"),
        ),
    )
    op.add_column(
        "subeler",
        sa.Column(
            "kimlik_kalite_kirilim",
            JSONB,
            nullable=False,
            server_default=sa.text("'{}'::jsonb"),
        ),
    )
    op.create_index(
        "ix_sube_kimlik_kalite",
        "subeler",
        ["kimlik_kalite_sinifi", "durum"],
    )
    op.add_column(
        "inceleme_dosyalari",
        sa.Column(
            "oncelik_puani",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),
    )
    op.add_column(
        "inceleme_dosyalari",
        sa.Column("triyaj_sinifi", sa.String(30), nullable=True),
    )
    op.create_index(
        "ix_inceleme_oncelik",
        "inceleme_dosyalari",
        ["durum", "oncelik_puani"],
    )


def downgrade() -> None:
    op.drop_index("ix_inceleme_oncelik", table_name="inceleme_dosyalari")
    op.drop_column("inceleme_dosyalari", "triyaj_sinifi")
    op.drop_column("inceleme_dosyalari", "oncelik_puani")
    op.drop_index("ix_sube_kimlik_kalite", table_name="subeler")
    op.drop_column("subeler", "kimlik_kalite_kirilim")
    op.drop_column("subeler", "kimlik_kalite_sinifi")
