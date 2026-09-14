"""Iddia/kanit tablolari ve kayipsiz legacy canonical baslangici."""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB, UUID

revision = "0007"
down_revision = "0006"
branch_labels = depends_on = None


def upgrade():
    op.execute("INSERT INTO yer_kimlikleri (id,sehir_id,durum) SELECT id,sehir_id,'aktif' FROM yerler ON CONFLICT DO NOTHING")
    op.execute("INSERT INTO subeler (id,yer_kimligi_id,legacy_yer_id,guncel_isim,durum) SELECT id,id,id,isim,'aktif' FROM yerler ON CONFLICT DO NOTHING")
    op.execute("INSERT INTO yer_aliaslari (id,sube_id,alias_turu,alias_degeri,aktif_mi) SELECT gen_random_uuid(),id,'legacy_yer_id',id::text,true FROM yerler ON CONFLICT DO NOTHING")
    op.execute("UPDATE yer_kaynaklari SET sube_id=yer_id WHERE sube_id IS NULL")
    op.alter_column("yer_kaynaklari", "sube_id", nullable=False)
    op.create_table("iddialar", sa.Column("id", UUID(as_uuid=False), primary_key=True), sa.Column("sube_id", UUID(as_uuid=False), sa.ForeignKey("subeler.id", ondelete="RESTRICT"), nullable=False), sa.Column("aile", sa.String(40), nullable=False), sa.Column("kapsam", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")), sa.Column("aktif_surum_no", sa.Integer), sa.Column("olusturulma_zamani", sa.DateTime(timezone=True), server_default=sa.func.now()))
    op.create_index("ix_iddia_sube_aile", "iddialar", ["sube_id", "aile"])
    op.create_table("iddia_surumleri", sa.Column("id", UUID(as_uuid=False), primary_key=True), sa.Column("iddia_id", UUID(as_uuid=False), sa.ForeignKey("iddialar.id", ondelete="CASCADE"), nullable=False), sa.Column("surum_no", sa.Integer, nullable=False), sa.Column("deger", JSONB, nullable=False), sa.Column("bilgi_durumu", sa.String(20), nullable=False), sa.Column("guven_sinifi", sa.String(20), nullable=False, server_default="belirsiz"), sa.Column("gecerlilik_baslangici", sa.DateTime(timezone=True)), sa.Column("gecerlilik_bitisi", sa.DateTime(timezone=True)), sa.Column("dogrulanma_zamani", sa.DateTime(timezone=True)), sa.Column("sisteme_alinma_zamani", sa.DateTime(timezone=True), server_default=sa.func.now()), sa.Column("yayin_durumu", sa.String(30), nullable=False, server_default="taslak"), sa.Column("yayin_engeli", sa.String(100)), sa.Column("ai_tarafindan_uretildi", sa.Boolean, nullable=False, server_default=sa.false()), sa.UniqueConstraint("iddia_id", "surum_no", name="ux_iddia_surum_no"))
    op.create_table("kanit_baglantilari", sa.Column("id", UUID(as_uuid=False), primary_key=True), sa.Column("iddia_surumu_id", UUID(as_uuid=False), sa.ForeignKey("iddia_surumleri.id", ondelete="CASCADE"), nullable=False), sa.Column("gozlem_id", UUID(as_uuid=False), sa.ForeignKey("gozlemler.id", ondelete="RESTRICT"), nullable=False), sa.Column("rol", sa.String(20), nullable=False), sa.Column("gerekce", sa.Text), sa.UniqueConstraint("iddia_surumu_id", "gozlem_id", "rol", name="ux_kanit_baglantisi"))


def downgrade():
    op.drop_table("kanit_baglantilari")
    op.drop_table("iddia_surumleri")
    op.drop_index("ix_iddia_sube_aile", table_name="iddialar")
    op.drop_table("iddialar")
    op.alter_column("yer_kaynaklari", "sube_id", nullable=True)
    op.execute("UPDATE yer_kaynaklari SET sube_id=NULL")
    op.execute("DELETE FROM yer_aliaslari WHERE alias_turu='legacy_yer_id'")
    op.execute("DELETE FROM subeler WHERE legacy_yer_id IS NOT NULL")
    op.execute("DELETE FROM yer_kimlikleri y WHERE NOT EXISTS (SELECT 1 FROM subeler s WHERE s.yer_kimligi_id=y.id)")
