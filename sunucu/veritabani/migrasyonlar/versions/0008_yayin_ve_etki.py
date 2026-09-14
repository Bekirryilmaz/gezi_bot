"""Yayin uygunlugu, tombstone, etki bagi ve outbox."""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB, UUID

revision = "0008"
down_revision = "0007"
branch_labels = depends_on = None


def upgrade():
    op.create_table("yayin_kayitlari", sa.Column("id", UUID(as_uuid=False), primary_key=True), sa.Column("nesne_turu", sa.String(30), nullable=False), sa.Column("nesne_id", UUID(as_uuid=False), nullable=False), sa.Column("durum", sa.String(40), nullable=False), sa.Column("neden_kodlari", JSONB, nullable=False, server_default=sa.text("'[]'::jsonb")), sa.Column("izinli_kullanimlar", JSONB, nullable=False, server_default=sa.text("'[]'::jsonb")), sa.Column("surum", sa.Integer, nullable=False, server_default="1"), sa.Column("aktif_mi", sa.Boolean, nullable=False, server_default=sa.true()), sa.Column("guncellenme_zamani", sa.DateTime(timezone=True), server_default=sa.func.now()), sa.UniqueConstraint("nesne_turu", "nesne_id", name="ux_yayin_nesnesi"))
    op.create_index("ix_yayin_durum_nesne", "yayin_kayitlari", ["durum", "nesne_turu"])
    op.create_table("geri_cekme_kayitlari", sa.Column("id", UUID(as_uuid=False), primary_key=True), sa.Column("nesne_turu", sa.String(30), nullable=False), sa.Column("nesne_id", UUID(as_uuid=False), nullable=False), sa.Column("kapsam", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")), sa.Column("gerekce_kodu", sa.String(80), nullable=False), sa.Column("gerekce", sa.Text, nullable=False), sa.Column("aktor_id", UUID(as_uuid=False), nullable=False), sa.Column("geri_cekme_zamani", sa.DateTime(timezone=True), server_default=sa.func.now()))
    op.create_table("etki_baglantilari", sa.Column("id", UUID(as_uuid=False), primary_key=True), sa.Column("kaynak_turu", sa.String(30), nullable=False), sa.Column("kaynak_id", UUID(as_uuid=False), nullable=False), sa.Column("hedef_turu", sa.String(30), nullable=False), sa.Column("hedef_id", UUID(as_uuid=False), nullable=False), sa.Column("bag_turu", sa.String(40), nullable=False), sa.Column("aktif_mi", sa.Boolean, nullable=False, server_default=sa.true()), sa.UniqueConstraint("kaynak_turu", "kaynak_id", "hedef_turu", "hedef_id", "bag_turu", name="ux_etki_bagi"))
    op.create_index("ix_etki_kaynak", "etki_baglantilari", ["kaynak_turu", "kaynak_id", "aktif_mi"])
    op.create_table("gecersizlestirme_olaylari", sa.Column("id", UUID(as_uuid=False), primary_key=True), sa.Column("olay_anahtari", sa.String(160), nullable=False, unique=True), sa.Column("kaynak_turu", sa.String(30), nullable=False), sa.Column("kaynak_id", UUID(as_uuid=False), nullable=False), sa.Column("olay_turu", sa.String(40), nullable=False), sa.Column("payload", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")), sa.Column("olusturulma_zamani", sa.DateTime(timezone=True), server_default=sa.func.now()), sa.Column("islenme_zamani", sa.DateTime(timezone=True)), sa.Column("deneme_sayisi", sa.Integer, nullable=False, server_default="0"))
    op.create_table("public_projectionlar", sa.Column("id", UUID(as_uuid=False), primary_key=True), sa.Column("nesne_turu", sa.String(30), nullable=False), sa.Column("nesne_id", UUID(as_uuid=False), nullable=False), sa.Column("yayin_surumu", sa.Integer, nullable=False), sa.Column("etag", sa.String(80), nullable=False), sa.Column("payload", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")), sa.Column("gecersiz_mi", sa.Boolean, nullable=False, server_default=sa.false()), sa.Column("gecersizlestirme_zamani", sa.DateTime(timezone=True)), sa.UniqueConstraint("nesne_turu", "nesne_id", name="ux_public_projection"))
    op.execute("""INSERT INTO yayin_kayitlari (id,nesne_turu,nesne_id,durum,neden_kodlari,izinli_kullanimlar,surum,aktif_mi) SELECT gen_random_uuid(),'yer',id,'sinirli_yayinlanabilir','[\"legacy_gecis\"]'::jsonb,'[\"liste\",\"detay\",\"arama\",\"kesfet\",\"rota_adayi\",\"paylasim\",\"cache_projection\",\"karar\"]'::jsonb,1,true FROM yerler ON CONFLICT DO NOTHING""")


def downgrade():
    op.drop_table("public_projectionlar")
    op.drop_table("gecersizlestirme_olaylari")
    op.drop_index("ix_etki_kaynak", table_name="etki_baglantilari")
    op.drop_table("etki_baglantilari")
    op.drop_table("geri_cekme_kayitlari")
    op.drop_index("ix_yayin_durum_nesne", table_name="yayin_kayitlari")
    op.drop_table("yayin_kayitlari")
