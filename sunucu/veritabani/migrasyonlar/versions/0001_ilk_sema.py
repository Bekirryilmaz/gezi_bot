"""ilk sema: sehirler, yerler, yer_kaynaklari, konaklama_detaylari, yorumlar, sabit_rotalar, kullanici_rotalari

Revizyon: 0001
Onceki revizyon: None
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from geoalchemy2 import Geography
from sqlalchemy.dialects.postgresql import JSONB, UUID

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Cografi (geography) kolonlari icin PostGIS eklentisi sart.
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis")

    op.create_table(
        "sehirler",
        sa.Column("id", UUID(as_uuid=False), primary_key=True),
        sa.Column("isim", sa.String(100), nullable=False, unique=True),
        sa.Column("plaka_kodu", sa.String(2)),
        sa.Column("bolge", sa.String(50)),
        sa.Column("merkez_enlem", sa.Float),
        sa.Column("merkez_boylam", sa.Float),
        sa.Column("aktif_mi", sa.Boolean, nullable=False, server_default=sa.true()),
        sa.Column("olusturulma_zamani", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "yerler",
        sa.Column("id", UUID(as_uuid=False), primary_key=True),
        sa.Column("sehir_id", UUID(as_uuid=False), sa.ForeignKey("sehirler.id", ondelete="CASCADE"), nullable=False),
        sa.Column("isim", sa.String(255), nullable=False),
        sa.Column("ana_kategori", sa.String(30), nullable=False),
        sa.Column("alt_kategori", sa.String(50), nullable=False),
        sa.Column("ilce", sa.String(100)),
        sa.Column("adres", sa.Text),
        sa.Column("aciklama", sa.Text),
        sa.Column("telefon", sa.String(30)),
        sa.Column("web_sitesi", sa.String(500)),
        sa.Column("konum", Geography(geometry_type="POINT", srid=4326), nullable=False),
        sa.Column("ozellikler", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("aktiviteler", JSONB, nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("fotograf_urlleri", JSONB, nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("kaynakta_puan_ortalamasi", sa.Float),
        sa.Column("kaynakta_puan_sayisi", sa.Integer),
        sa.Column("duygu_skoru_ortalama", sa.Float),
        sa.Column("deneyim_puanlari", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("duygu_son_guncelleme", sa.DateTime(timezone=True)),
        sa.Column("olusturulma_zamani", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("guncellenme_zamani", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_yerler_konum", "yerler", ["konum"], postgresql_using="gist")
    op.create_index("ix_yerler_sehir_kategori", "yerler", ["sehir_id", "ana_kategori", "alt_kategori"])

    op.create_table(
        "yer_kaynaklari",
        sa.Column("id", UUID(as_uuid=False), primary_key=True),
        sa.Column("yer_id", UUID(as_uuid=False), sa.ForeignKey("yerler.id", ondelete="CASCADE"), nullable=False),
        sa.Column("kaynak", sa.String(30), nullable=False),
        sa.Column("kaynak_id", sa.String(255), nullable=False),
        sa.Column("kaynak_url", sa.String(500)),
        sa.Column("cekilme_zamani", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint("kaynak", "kaynak_id", name="ux_yer_kaynaklari_kaynak_kimlik"),
    )

    op.create_table(
        "konaklama_detaylari",
        sa.Column("yer_id", UUID(as_uuid=False), sa.ForeignKey("yerler.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("gecelik_fiyat_araligi_min", sa.Float),
        sa.Column("gecelik_fiyat_araligi_max", sa.Float),
        sa.Column("rezervasyon_linkleri", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("oda_sayisi", sa.Integer),
    )

    op.create_table(
        "yorumlar",
        sa.Column("id", UUID(as_uuid=False), primary_key=True),
        sa.Column("yer_id", UUID(as_uuid=False), sa.ForeignKey("yerler.id", ondelete="CASCADE"), nullable=False),
        sa.Column("kaynak", sa.String(30), nullable=False),
        sa.Column("kaynak_yorum_id", sa.String(255)),
        sa.Column("yazar_takma_adi", sa.String(100)),
        sa.Column("yorum_metni", sa.Text, nullable=False),
        sa.Column("kaynakta_puan", sa.Float),
        sa.Column("yorum_tarihi", sa.DateTime(timezone=True)),
        sa.Column("dil", sa.String(5), nullable=False, server_default="tr"),
        sa.Column("duygu_skoru", sa.Float),
        sa.Column("duygu_etiketi", sa.String(20)),
        sa.Column("konu_duygulari", JSONB, nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("analiz_model_adi", sa.String(200)),
        sa.Column("analiz_zamani", sa.DateTime(timezone=True)),
        sa.Column("cekilme_zamani", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint("kaynak", "kaynak_yorum_id", name="ux_yorumlar_kaynak_kimlik"),
    )
    op.create_index("ix_yorumlar_yer", "yorumlar", ["yer_id"])

    op.create_table(
        "sabit_rotalar",
        sa.Column("id", UUID(as_uuid=False), primary_key=True),
        sa.Column("isim", sa.String(255), nullable=False),
        sa.Column("aciklama", sa.Text),
        sa.Column("bolge", sa.String(50)),
        sa.Column("rota_tipi", sa.String(50)),
        sa.Column("duraklar", JSONB, nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("kapak_fotografi_url", sa.String(500)),
        sa.Column("olusturulma_zamani", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "kullanici_rotalari",
        sa.Column("id", UUID(as_uuid=False), primary_key=True),
        sa.Column("sehir_id", UUID(as_uuid=False), sa.ForeignKey("sehirler.id", ondelete="CASCADE"), nullable=False),
        sa.Column("tercihler", JSONB, nullable=False),
        sa.Column("gunler", JSONB, nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("konaklama_onerisi_yer_id", UUID(as_uuid=False), sa.ForeignKey("yerler.id")),
        sa.Column("olusturulma_zamani", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("kullanici_rotalari")
    op.drop_table("sabit_rotalar")
    op.drop_index("ix_yorumlar_yer", table_name="yorumlar")
    op.drop_table("yorumlar")
    op.drop_table("konaklama_detaylari")
    op.drop_table("yer_kaynaklari")
    op.drop_index("ix_yerler_sehir_kategori", table_name="yerler")
    op.drop_index("ix_yerler_konum", table_name="yerler")
    op.drop_table("yerler")
    op.drop_table("sehirler")
