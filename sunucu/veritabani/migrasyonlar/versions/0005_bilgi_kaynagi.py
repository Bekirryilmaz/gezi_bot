"""Kaynak hakki, batch ve gozlem tabani."""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB, UUID

revision = "0005"
down_revision = "0004"
branch_labels = depends_on = None


def upgrade():
    op.create_table("kaynak_politikalari", sa.Column("id", UUID(as_uuid=False), primary_key=True), sa.Column("kaynak", sa.String(50), nullable=False, unique=True), sa.Column("kamusal_gosterim", sa.String(20), nullable=False, server_default="bilinmiyor"), sa.Column("turev_iddia", sa.String(20), nullable=False, server_default="bilinmiyor"), sa.Column("ai_isleme", sa.String(20), nullable=False, server_default="bilinmiyor"), sa.Column("uzun_sureli_saklama", sa.String(20), nullable=False, server_default="bilinmiyor"), sa.Column("dayanak_notu", sa.Text), sa.Column("gecerli_baslangic", sa.DateTime(timezone=True)), sa.Column("gecerli_bitis", sa.DateTime(timezone=True)), sa.Column("olusturulma_zamani", sa.DateTime(timezone=True), server_default=sa.func.now()))
    op.create_table("veri_batchleri", sa.Column("id", UUID(as_uuid=False), primary_key=True), sa.Column("kaynak", sa.String(50), nullable=False), sa.Column("kosu_anahtari", sa.String(255), nullable=False), sa.Column("kok_tanimi", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")), sa.Column("baslama_zamani", sa.DateTime(timezone=True), nullable=False), sa.Column("cekilme_baslangici", sa.DateTime(timezone=True)), sa.Column("cekilme_bitisi", sa.DateTime(timezone=True)), sa.Column("tamamlanma_zamani", sa.DateTime(timezone=True)), sa.Column("sisteme_alinma_zamani", sa.DateTime(timezone=True), server_default=sa.func.now()), sa.UniqueConstraint("kaynak", "kosu_anahtari", name="ux_veri_batch_kaynak_kosu"))
    op.create_table("gozlemler", sa.Column("id", UUID(as_uuid=False), primary_key=True), sa.Column("veri_batch_id", UUID(as_uuid=False), sa.ForeignKey("veri_batchleri.id", ondelete="RESTRICT"), nullable=False), sa.Column("kaynak", sa.String(50), nullable=False), sa.Column("kaynak_kayit_id", sa.String(255), nullable=False), sa.Column("kaynak_url", sa.String(500)), sa.Column("olay_zamani", sa.DateTime(timezone=True)), sa.Column("kaynakta_gozlemlenme_zamani", sa.DateTime(timezone=True)), sa.Column("cekilme_zamani", sa.DateTime(timezone=True), nullable=False), sa.Column("dogrulanma_zamani", sa.DateTime(timezone=True)), sa.Column("sisteme_alinma_zamani", sa.DateTime(timezone=True), server_default=sa.func.now()), sa.Column("icerik_ozeti", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")), sa.Column("icerik_hash", sa.String(64), nullable=False), sa.UniqueConstraint("veri_batch_id", "kaynak", "kaynak_kayit_id", "icerik_hash", name="ux_gozlem_idempotent"))
    op.create_index("ix_gozlem_kaynak_kayit", "gozlemler", ["kaynak", "kaynak_kayit_id"])


def downgrade():
    op.drop_index("ix_gozlem_kaynak_kayit", table_name="gozlemler")
    op.drop_table("gozlemler")
    op.drop_table("veri_batchleri")
    op.drop_table("kaynak_politikalari")

