"""Ham baglam icermeyen asgari karar izi.

Revision ID: 0011
Revises: 0010
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB, UUID

revision = "0011"
down_revision = "0010"
branch_labels = depends_on = None


def upgrade():
    op.create_table(
        "karar_izleri",
        sa.Column("id", UUID(as_uuid=False), primary_key=True),
        sa.Column("trace_reference", sa.String(100), nullable=False, unique=True),
        sa.Column("request_id", sa.String(100), nullable=False),
        sa.Column("correlation_id", sa.String(100), nullable=False),
        sa.Column("context_fingerprint", sa.String(64), nullable=False),
        sa.Column("politika_surumu", sa.String(80), nullable=False),
        sa.Column("bilgi_surumu", sa.String(80), nullable=False),
        sa.Column("claim_surumleri", JSONB, nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("yayin_surumleri", JSONB, nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("reason_kodlari", JSONB, nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("karar_zamani", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_karar_izi_context", "karar_izleri", ["context_fingerprint", "politika_surumu", "bilgi_surumu"])
    op.create_index("ix_karar_izi_karar_zamani", "karar_izleri", ["karar_zamani"])


def downgrade():
    op.drop_index("ix_karar_izi_karar_zamani", table_name="karar_izleri")
    op.drop_index("ix_karar_izi_context", table_name="karar_izleri")
    op.drop_table("karar_izleri")
