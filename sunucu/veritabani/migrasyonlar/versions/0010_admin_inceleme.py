"""Risk sinifli admin inceleme ve ikinci onay dosyalari."""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB, UUID

revision = "0010"
down_revision = "0009"
branch_labels = depends_on = None


def upgrade():
    op.create_table("inceleme_dosyalari", sa.Column("id", UUID(as_uuid=False), primary_key=True), sa.Column("dosya_turu", sa.String(40), nullable=False), sa.Column("nesne_turu", sa.String(40), nullable=False), sa.Column("nesne_id", sa.String(100), nullable=False), sa.Column("durum", sa.String(30), nullable=False, server_default="bekliyor"), sa.Column("risk_sinifi", sa.String(20), nullable=False, server_default="dusuk"), sa.Column("onerilen_eylem", sa.String(80)), sa.Column("komut_payload", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")), sa.Column("acan_aktor_id", UUID(as_uuid=False), sa.ForeignKey("admin_kullanicilari.id", ondelete="RESTRICT"), nullable=False), sa.Column("atanan_aktor_id", UUID(as_uuid=False), sa.ForeignKey("admin_kullanicilari.id", ondelete="SET NULL")), sa.Column("ikinci_inceleyen_id", UUID(as_uuid=False), sa.ForeignKey("admin_kullanicilari.id", ondelete="RESTRICT")), sa.Column("karar_gerekcesi", sa.Text), sa.Column("surum", sa.Integer, nullable=False, server_default="1"), sa.Column("olusturulma_zamani", sa.DateTime(timezone=True), server_default=sa.func.now()), sa.Column("guncellenme_zamani", sa.DateTime(timezone=True), server_default=sa.func.now()))
    op.create_index("ix_inceleme_kuyruk", "inceleme_dosyalari", ["durum", "dosya_turu", "risk_sinifi"])


def downgrade():
    op.drop_index("ix_inceleme_kuyruk", table_name="inceleme_dosyalari")
    op.drop_table("inceleme_dosyalari")
