"""tanitim_metni sutunlarini ekler (yerler + bolge_profilleri).

Revizyon: 0004
Onceki revizyon: 0003
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0004"
down_revision: Union[str, None] = "0003"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("yerler", sa.Column("tanitim_metni", sa.Text(), nullable=True))
    op.add_column("bolge_profilleri", sa.Column("tanitim_metni", sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column("bolge_profilleri", "tanitim_metni")
    op.drop_column("yerler", "tanitim_metni")
