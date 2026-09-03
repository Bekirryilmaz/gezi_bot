"""mekan_onerileri: adres tarifi ve ulasim alanlari.

Revizyon: 0006
Onceki revizyon: 0005
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0006"
down_revision: Union[str, None] = "0005"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "mekan_onerileri",
        sa.Column("adres_tarifi", sa.Text(), nullable=False, server_default=""),
    )
    op.add_column(
        "mekan_onerileri",
        sa.Column("araba_erisimi", sa.String(40), nullable=False, server_default=""),
    )
    op.add_column(
        "mekan_onerileri",
        sa.Column("yurume_mesafesi", sa.String(200), nullable=False, server_default=""),
    )
    op.add_column(
        "mekan_onerileri",
        sa.Column("yol_durumu", sa.String(120), nullable=False, server_default=""),
    )
    op.add_column(
        "mekan_onerileri",
        sa.Column("toplu_tasima", sa.String(300), nullable=False, server_default=""),
    )


def downgrade() -> None:
    op.drop_column("mekan_onerileri", "toplu_tasima")
    op.drop_column("mekan_onerileri", "yol_durumu")
    op.drop_column("mekan_onerileri", "yurume_mesafesi")
    op.drop_column("mekan_onerileri", "araba_erisimi")
    op.drop_column("mekan_onerileri", "adres_tarifi")
