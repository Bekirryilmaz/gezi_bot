"""Ic admin identity, rol, session ve append-only audit."""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB, UUID

revision = "0009"
down_revision = "0008"
branch_labels = depends_on = None


def upgrade():
    op.create_table("admin_kullanicilari", sa.Column("id", UUID(as_uuid=False), primary_key=True), sa.Column("eposta", sa.String(255), nullable=False, unique=True), sa.Column("gorunen_ad", sa.String(120), nullable=False), sa.Column("parola_hash", sa.String(128), nullable=False), sa.Column("parola_salt", sa.String(64), nullable=False), sa.Column("kapsam", JSONB, nullable=False, server_default=sa.text("'[]'::jsonb")), sa.Column("aktif_mi", sa.Boolean, nullable=False, server_default=sa.true()), sa.Column("olusturulma_zamani", sa.DateTime(timezone=True), server_default=sa.func.now()))
    op.create_table("admin_rolleri", sa.Column("id", UUID(as_uuid=False), primary_key=True), sa.Column("kod", sa.String(60), nullable=False, unique=True), sa.Column("aciklama", sa.String(255)))
    op.create_table("admin_kullanici_rolleri", sa.Column("kullanici_id", UUID(as_uuid=False), sa.ForeignKey("admin_kullanicilari.id", ondelete="CASCADE"), primary_key=True), sa.Column("rol_id", UUID(as_uuid=False), sa.ForeignKey("admin_rolleri.id", ondelete="CASCADE"), primary_key=True))
    op.create_table("admin_oturumlari", sa.Column("id", UUID(as_uuid=False), primary_key=True), sa.Column("kullanici_id", UUID(as_uuid=False), sa.ForeignKey("admin_kullanicilari.id", ondelete="CASCADE"), nullable=False), sa.Column("token_hash", sa.String(64), nullable=False, unique=True), sa.Column("csrf_hash", sa.String(64), nullable=False), sa.Column("sona_erme_zamani", sa.DateTime(timezone=True), nullable=False), sa.Column("ip_izi", sa.String(64)), sa.Column("user_agent_izi", sa.String(64)), sa.Column("iptal_zamani", sa.DateTime(timezone=True)), sa.Column("olusturulma_zamani", sa.DateTime(timezone=True), server_default=sa.func.now()))
    op.create_index("ix_admin_oturum_kullanici_sona_erme", "admin_oturumlari", ["kullanici_id", "sona_erme_zamani"])
    op.create_table("admin_audit_olaylari", sa.Column("id", UUID(as_uuid=False), primary_key=True), sa.Column("aktor_id", UUID(as_uuid=False), sa.ForeignKey("admin_kullanicilari.id", ondelete="RESTRICT"), nullable=False), sa.Column("eylem", sa.String(80), nullable=False), sa.Column("nesne_turu", sa.String(40), nullable=False), sa.Column("nesne_id", sa.String(100), nullable=False), sa.Column("onceki_durum_ref", sa.String(160)), sa.Column("yeni_durum_ref", sa.String(160)), sa.Column("gerekce", sa.Text, nullable=False), sa.Column("istek_id", sa.String(100), nullable=False), sa.Column("korelasyon_id", sa.String(100), nullable=False), sa.Column("meta", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")), sa.Column("olusturulma_zamani", sa.DateTime(timezone=True), server_default=sa.func.now()))
    op.create_index("ix_admin_audit_nesne", "admin_audit_olaylari", ["nesne_turu", "nesne_id", "olusturulma_zamani"])
    op.execute("""INSERT INTO admin_rolleri (id,kod,aciklama) VALUES (gen_random_uuid(),'gozlemci','Kuyruk goruntuleme'),(gen_random_uuid(),'kimlik_editoru','Kimlik duzeltme'),(gen_random_uuid(),'claim_editoru','Claim inceleme'),(gen_random_uuid(),'yayinci','Yayin ve geri cekme'),(gen_random_uuid(),'risk_onayci','Kritik ikinci inceleme'),(gen_random_uuid(),'auditor','Audit goruntuleme'),(gen_random_uuid(),'yonetici','Tum ic admin yetkileri') ON CONFLICT (kod) DO NOTHING""")
    op.execute("""CREATE FUNCTION admin_audit_degismez() RETURNS trigger AS $$ BEGIN RAISE EXCEPTION 'admin audit append-only'; END; $$ LANGUAGE plpgsql""")
    op.execute("""CREATE TRIGGER trg_admin_audit_degismez BEFORE UPDATE OR DELETE ON admin_audit_olaylari FOR EACH ROW EXECUTE FUNCTION admin_audit_degismez()""")


def downgrade():
    op.execute("DROP TRIGGER IF EXISTS trg_admin_audit_degismez ON admin_audit_olaylari")
    op.execute("DROP FUNCTION IF EXISTS admin_audit_degismez()")
    op.drop_index("ix_admin_audit_nesne", table_name="admin_audit_olaylari")
    op.drop_table("admin_audit_olaylari")
    op.drop_index("ix_admin_oturum_kullanici_sona_erme", table_name="admin_oturumlari")
    op.drop_table("admin_oturumlari")
    op.drop_table("admin_kullanici_rolleri")
    op.drop_table("admin_rolleri")
    op.drop_table("admin_kullanicilari")
