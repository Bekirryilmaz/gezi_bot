"""mekan_onerileri blog: slug, gorunurluk, editor notu, yorumlar.

Revizyon: 0007
Onceki revizyon: 0006
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB, UUID

revision: str = "0007"
down_revision: Union[str, None] = "0006"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("mekan_onerileri", sa.Column("slug", sa.String(220), nullable=True))
    op.add_column(
        "mekan_onerileri",
        sa.Column("begeni_sayisi", sa.Integer(), nullable=False, server_default="0"),
    )
    op.add_column(
        "mekan_onerileri",
        sa.Column("gorunur_tarif", sa.Boolean(), nullable=False, server_default=sa.true()),
    )
    op.add_column(
        "mekan_onerileri",
        sa.Column("gorunur_ulasim", sa.Boolean(), nullable=False, server_default=sa.true()),
    )
    op.add_column(
        "mekan_onerileri",
        sa.Column("gorunur_koordinat", sa.Boolean(), nullable=False, server_default=sa.false()),
    )
    op.add_column(
        "mekan_onerileri",
        sa.Column("gorunur_tuyo", sa.Boolean(), nullable=False, server_default=sa.true()),
    )
    op.add_column("mekan_onerileri", sa.Column("tarih_baglam", sa.Text(), nullable=True))
    op.add_column("mekan_onerileri", sa.Column("editor_notu", sa.Text(), nullable=True))
    op.add_column(
        "mekan_onerileri",
        sa.Column("yayin_zamani", sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column(
        "mekan_onerileri",
        sa.Column(
            "onayli_fotograflar",
            JSONB,
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
    )
    op.execute("UPDATE mekan_onerileri SET slug = CAST(id AS varchar) WHERE slug IS NULL")
    op.alter_column("mekan_onerileri", "slug", nullable=False)
    op.create_index("ix_mekan_onerileri_slug", "mekan_onerileri", ["slug"], unique=True)

    op.create_table(
        "oneri_yorumlari",
        sa.Column("id", UUID(as_uuid=False), primary_key=True),
        sa.Column(
            "oneri_id",
            UUID(as_uuid=False),
            sa.ForeignKey("mekan_onerileri.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("yazar_adi", sa.String(80), nullable=False),
        sa.Column("icerik", sa.Text(), nullable=False),
        sa.Column("durum", sa.String(20), nullable=False, server_default="yayinda"),
        sa.Column(
            "olusturulma_zamani",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
        ),
    )
    op.create_index("ix_oneri_yorumlari_oneri", "oneri_yorumlari", ["oneri_id"])


def downgrade() -> None:
    op.drop_index("ix_oneri_yorumlari_oneri", table_name="oneri_yorumlari")
    op.drop_table("oneri_yorumlari")
    op.drop_index("ix_mekan_onerileri_slug", table_name="mekan_onerileri")
    op.drop_column("mekan_onerileri", "onayli_fotograflar")
    op.drop_column("mekan_onerileri", "yayin_zamani")
    op.drop_column("mekan_onerileri", "editor_notu")
    op.drop_column("mekan_onerileri", "tarih_baglam")
    op.drop_column("mekan_onerileri", "gorunur_tuyo")
    op.drop_column("mekan_onerileri", "gorunur_koordinat")
    op.drop_column("mekan_onerileri", "gorunur_ulasim")
    op.drop_column("mekan_onerileri", "gorunur_tarif")
    op.drop_column("mekan_onerileri", "begeni_sayisi")
    op.drop_column("mekan_onerileri", "slug")
