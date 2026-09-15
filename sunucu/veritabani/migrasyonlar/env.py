"""
Alembic ortam yapilandirmasi.

Baglanti adresini alembic.ini icine yazmiyoruz -- sifrenin duz metin olarak
dosyada durmasini istemiyoruz. Bunun yerine sunucu/veritabani/baglanti.py
icindeki ayni mantikla (.env / ortam degiskeni) VERITABANI_URL okunur.
"""

from __future__ import annotations

import sys
from logging.config import fileConfig
from pathlib import Path

from alembic import context
from sqlalchemy import engine_from_config, pool

# Repo kokunu (gezi_bot/) modul arama yoluna ekle ki `sunucu` ve `ortak`
# paketleri import edilebilsin -- bu dosya sunucu/veritabani/migrasyonlar/
# altinda oldugu icin 3 seviye yukari cikmak gerekiyor.
REPO_KOKU = Path(__file__).resolve().parents[3]
if str(REPO_KOKU) not in sys.path:
    sys.path.insert(0, str(REPO_KOKU))

from sunucu.veritabani.baglanti import VERITABANI_URL  # noqa: E402
from sunucu.veritabani.temel import Taban  # noqa: E402
from sunucu.veritabani import modeller  # noqa: E402,F401  (tum modelleri Taban.metadata'ya kaydetmek icin import edilir)
from sunucu.veritabani.migrasyonlar.karsilastirma import nesneyi_karsilastir  # noqa: E402

config = context.config
config.set_main_option("sqlalchemy.url", VERITABANI_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Otomatik migration uretimi (autogenerate) icin hedef metadata
target_metadata = Taban.metadata


def run_migrations_offline() -> None:
    """SQL dosyasi olarak uretmek icin (veritabanina baglanmadan)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_object=nesneyi_karsilastir,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Dogrudan veritabanina baglanip migration calistirmak icin (normal kullanim)."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as baglanti:
        # Her revizyon kendi isleminde biter. Boylece 0015 gibi veri
        # korumali bir downgrade hata verince onceki revizyonun (0016)
        # basarili isi geri alinmaz; alembic_version 0015'te kalir ve
        # 0015 tablolari sessizce silinmez.
        context.configure(
            connection=baglanti,
            target_metadata=target_metadata,
            include_object=nesneyi_karsilastir,
            transaction_per_migration=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
