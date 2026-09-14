"""Kalici canonical yer, sube, alias ve esleme karari."""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB, UUID

revision = "0006"
down_revision = "0005"
branch_labels = depends_on = None


def upgrade():
    op.create_table("yer_kimlikleri", sa.Column("id", UUID(as_uuid=False), primary_key=True), sa.Column("sehir_id", UUID(as_uuid=False), sa.ForeignKey("sehirler.id", ondelete="RESTRICT"), nullable=False), sa.Column("durum", sa.String(20), nullable=False, server_default="aktif"), sa.Column("olusturulma_zamani", sa.DateTime(timezone=True), server_default=sa.func.now()))
    op.create_table("subeler", sa.Column("id", UUID(as_uuid=False), primary_key=True), sa.Column("yer_kimligi_id", UUID(as_uuid=False), sa.ForeignKey("yer_kimlikleri.id", ondelete="RESTRICT"), nullable=False), sa.Column("legacy_yer_id", UUID(as_uuid=False), sa.ForeignKey("yerler.id", ondelete="SET NULL"), unique=True), sa.Column("guncel_isim", sa.String(255), nullable=False), sa.Column("durum", sa.String(20), nullable=False, server_default="aktif"), sa.Column("yonlendirilen_sube_id", UUID(as_uuid=False)), sa.Column("olusturulma_zamani", sa.DateTime(timezone=True), server_default=sa.func.now()))
    op.create_foreign_key("fk_sube_yonlendirme", "subeler", "subeler", ["yonlendirilen_sube_id"], ["id"], ondelete="RESTRICT")
    op.create_table("yer_aliaslari", sa.Column("id", UUID(as_uuid=False), primary_key=True), sa.Column("sube_id", UUID(as_uuid=False), sa.ForeignKey("subeler.id", ondelete="CASCADE"), nullable=False), sa.Column("alias_turu", sa.String(30), nullable=False), sa.Column("alias_degeri", sa.String(255), nullable=False), sa.Column("aktif_mi", sa.Boolean, nullable=False, server_default=sa.true()), sa.UniqueConstraint("alias_turu", "alias_degeri", name="ux_yer_alias_tur_deger"))
    op.create_table("esleme_adaylari", sa.Column("id", UUID(as_uuid=False), primary_key=True), sa.Column("sol_sube_id", UUID(as_uuid=False), sa.ForeignKey("subeler.id", ondelete="RESTRICT"), nullable=False), sa.Column("sag_sube_id", UUID(as_uuid=False), sa.ForeignKey("subeler.id", ondelete="RESTRICT"), nullable=False), sa.Column("confidence", sa.Float, nullable=False), sa.Column("belirsizlik", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")), sa.Column("durum", sa.String(20), nullable=False, server_default="bekliyor"), sa.Column("olusturulma_zamani", sa.DateTime(timezone=True), server_default=sa.func.now()), sa.UniqueConstraint("sol_sube_id", "sag_sube_id", name="ux_esleme_adayi_cift"))
    op.create_table("esleme_kararlari", sa.Column("id", UUID(as_uuid=False), primary_key=True), sa.Column("aday_id", UUID(as_uuid=False), sa.ForeignKey("esleme_adaylari.id", ondelete="SET NULL")), sa.Column("karar", sa.String(30), nullable=False), sa.Column("gerekce", sa.Text, nullable=False), sa.Column("confidence", sa.Float), sa.Column("manuel_override", sa.Boolean, nullable=False, server_default=sa.false()), sa.Column("karar_zamani", sa.DateTime(timezone=True), server_default=sa.func.now()))
    op.create_table("yer_birlestirmeleri", sa.Column("id", UUID(as_uuid=False), primary_key=True), sa.Column("kaynak_sube_id", UUID(as_uuid=False), sa.ForeignKey("subeler.id", ondelete="RESTRICT"), nullable=False), sa.Column("hedef_sube_id", UUID(as_uuid=False), sa.ForeignKey("subeler.id", ondelete="RESTRICT"), nullable=False), sa.Column("karar_id", UUID(as_uuid=False), sa.ForeignKey("esleme_kararlari.id", ondelete="RESTRICT"), nullable=False), sa.Column("tasinan_kaynak_idleri", JSONB, nullable=False, server_default=sa.text("'[]'::jsonb")), sa.Column("aktif_mi", sa.Boolean, nullable=False, server_default=sa.true()), sa.Column("birlestirme_zamani", sa.DateTime(timezone=True), server_default=sa.func.now()), sa.Column("geri_alinma_zamani", sa.DateTime(timezone=True)))
    op.create_index("ix_yer_birlestirme_kaynak_aktif", "yer_birlestirmeleri", ["kaynak_sube_id", "aktif_mi"])
    op.add_column("yer_kaynaklari", sa.Column("kaynakta_gozlemlenme_zamani", sa.DateTime(timezone=True)))
    op.add_column("yer_kaynaklari", sa.Column("sisteme_alinma_zamani", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False))
    op.add_column("yer_kaynaklari", sa.Column("veri_batch_id", UUID(as_uuid=False), sa.ForeignKey("veri_batchleri.id", ondelete="SET NULL")))
    op.add_column("yer_kaynaklari", sa.Column("sube_id", UUID(as_uuid=False), sa.ForeignKey("subeler.id", ondelete="RESTRICT")))


def downgrade():
    for kolon in ("sube_id", "veri_batch_id", "sisteme_alinma_zamani", "kaynakta_gozlemlenme_zamani"):
        op.drop_column("yer_kaynaklari", kolon)
    op.drop_index("ix_yer_birlestirme_kaynak_aktif", table_name="yer_birlestirmeleri")
    for tablo in ("yer_birlestirmeleri", "esleme_kararlari", "esleme_adaylari", "yer_aliaslari", "subeler", "yer_kimlikleri"):
        op.drop_table(tablo)

