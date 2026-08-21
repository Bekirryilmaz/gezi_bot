"""yerler tablosuna yer_profili ve duygu_ozeti alanlarini ekler

Revizyon: 0002
Onceki revizyon: 0001
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision: str = "0002"
down_revision: Union[str, None] = "0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "yerler",
        sa.Column(
            "yer_profili",
            JSONB,
            nullable=False,
            server_default=sa.text("'{}'::jsonb"),
            comment="dokumanlar/kategori_taksonomisi.md #6 -- YerProfili (fiyat algisi, ulasim, kalabalik zamanlar, ziyaretci profili)",
        ),
    )
    op.add_column(
        "yerler",
        sa.Column(
            "duygu_ozeti",
            sa.Text,
            comment="yer_profili'nden sentezlenen, kullaniciya gosterilecek samimi tanitim metni",
        ),
    )


def downgrade() -> None:
    op.drop_column("yerler", "duygu_ozeti")
    op.drop_column("yerler", "yer_profili")
