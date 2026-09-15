"""Sistem tarafindan acilan claim candidate inceleme dosyalari.

Revision ID: 0014
Revises: 0013
"""

import sqlalchemy as sa
from alembic import op

revision = "0014"
down_revision = "0013"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column("inceleme_dosyalari", "acan_aktor_id", nullable=True)


def downgrade() -> None:
    sistem_adayi_sayisi = op.get_bind().execute(
        sa.text("SELECT count(*) FROM inceleme_dosyalari WHERE acan_aktor_id IS NULL")
    ).scalar_one()
    if sistem_adayi_sayisi:
        raise RuntimeError(
            "0014 downgrade veri kaybetmeden uygulanamiyor: "
            f"{sistem_adayi_sayisi} sistem inceleme adayi once karara baglanmali."
        )
    op.alter_column("inceleme_dosyalari", "acan_aktor_id", nullable=False)
