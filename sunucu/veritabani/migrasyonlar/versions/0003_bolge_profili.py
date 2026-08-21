"""bolge_profilleri tablosunu ekler (sehir/ilce tanitim duygu profili)

Revizyon: 0003
Onceki revizyon: 0002
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB, UUID

revision: str = "0003"
down_revision: Union[str, None] = "0002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "bolge_profilleri",
        sa.Column("id", UUID(as_uuid=False), primary_key=True),
        sa.Column("sehir_id", UUID(as_uuid=False), sa.ForeignKey("sehirler.id", ondelete="CASCADE"), nullable=False),
        sa.Column("bolge_adi", sa.String(100), nullable=False),
        sa.Column("ilce_mi", sa.Boolean, nullable=False, server_default=sa.false()),
        sa.Column("genel_duygu_skoru", sa.Float),
        sa.Column("genel_duygu_etiketi", sa.String(20)),
        sa.Column("on_plana_cikan_konular", JSONB, nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("kullanilan_yorum_sayisi", sa.Integer, nullable=False, server_default="0"),
        sa.Column("duygu_ozeti", sa.Text),
        sa.Column("olusturulma_zamani", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("guncellenme_zamani", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint("sehir_id", "bolge_adi", name="ux_bolge_profilleri_sehir_bolge"),
    )


def downgrade() -> None:
    op.drop_table("bolge_profilleri")
