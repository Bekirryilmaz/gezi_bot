"""mekan_onerileri tablosu: kullanici onerileri yonetici onayina kadar
ana yerler haritasina dusmez.

Revizyon: 0005
Onceki revizyon: 0004
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB, UUID

revision: str = "0005"
down_revision: Union[str, None] = "0004"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "mekan_onerileri",
        sa.Column("id", UUID(as_uuid=False), primary_key=True),
        sa.Column("baslik", sa.String(200), nullable=False),
        sa.Column("kategori", sa.String(40), nullable=False),
        sa.Column("sehir", sa.String(100), nullable=False),
        sa.Column("ilce", sa.String(100), nullable=False),
        sa.Column("aciklama", sa.Text(), nullable=False),
        sa.Column("ziyaretci_tuyosu", sa.Text(), nullable=True),
        sa.Column("enlem", sa.Float(), nullable=False),
        sa.Column("boylam", sa.Float(), nullable=False),
        sa.Column("fotograf_urlleri", JSONB, nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("gonderen_adi", sa.String(120), nullable=True),
        sa.Column("gonderen_eposta", sa.String(254), nullable=False),
        sa.Column("durum", sa.String(20), nullable=False, server_default="beklemede"),
        sa.Column("red_nedeni", sa.Text(), nullable=True),
        sa.Column("ip_adresi", sa.String(64), nullable=True),
        sa.Column("yer_id", UUID(as_uuid=False), sa.ForeignKey("yerler.id", ondelete="SET NULL"), nullable=True),
        sa.Column("olusturulma_zamani", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_mekan_onerileri_durum", "mekan_onerileri", ["durum"])
    op.create_index("ix_mekan_onerileri_eposta", "mekan_onerileri", ["gonderen_eposta"])


def downgrade() -> None:
    op.drop_index("ix_mekan_onerileri_eposta", table_name="mekan_onerileri")
    op.drop_index("ix_mekan_onerileri_durum", table_name="mekan_onerileri")
    op.drop_table("mekan_onerileri")
