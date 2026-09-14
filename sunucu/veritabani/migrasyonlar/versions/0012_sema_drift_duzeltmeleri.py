"""Canonical kaynak ve PostGIS indeks metadata drift'lerini kapatir.

Revision ID: 0012
Revises: 0011
"""

from __future__ import annotations

from alembic import op

revision = "0012"
down_revision = "0011"
branch_labels = depends_on = None


def upgrade() -> None:
    # Kaynak baglarinin canonical sube uzerinden aranmasi icin FK indeksi.
    op.create_index("ix_yer_kaynaklari_sube_id", "yer_kaynaklari", ["sube_id"])

    # Geography otomatik idx_* indeksini, model de acik ix_* indeksini
    # uretiyordu. Ayni POINT kolonu uzerindeki iki GiST indeksinden acik
    # tanimli ix_yerler_konum canonical olarak korunur.
    op.drop_index("idx_yerler_konum", table_name="yerler", if_exists=True)


def downgrade() -> None:
    op.create_index("idx_yerler_konum", "yerler", ["konum"], postgresql_using="gist")
    op.drop_index("ix_yer_kaynaklari_sube_id", table_name="yer_kaynaklari")
