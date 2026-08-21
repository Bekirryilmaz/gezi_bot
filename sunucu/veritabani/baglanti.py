"""
Veritabani baglantisini kuran modul.

Baglanti bilgisi ortam degiskeninden (`VERITABANI_URL`) okunur, kod icine asla
sifre/kullanici adi yazilmaz. Yerel gelistirmede `.env` dosyasindan, Oracle
sunucuda ise sistem ortam degiskenlerinden veya `.env` dosyasindan okunabilir.
"""

from __future__ import annotations

import os
from collections.abc import Generator

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

load_dotenv()

VARSAYILAN_VERITABANI_URL = "postgresql+psycopg://gezi_kullanici:gezi_sifre@localhost:5432/gezi_veritabani"

VERITABANI_URL = os.environ.get("VERITABANI_URL", VARSAYILAN_VERITABANI_URL)

# echo=False -> her SQL sorgusunu konsola basmasin. Gelistirme sirasinda SQL
# sorgularini gormek istersen VERITABANI_SQL_LOGLA=1 ortam degiskenini ac.
motor = create_engine(VERITABANI_URL, echo=os.environ.get("VERITABANI_SQL_LOGLA") == "1")

OturumUretici = sessionmaker(bind=motor, autoflush=False, autocommit=False)


def oturum_al() -> Generator[Session, None, None]:
    """FastAPI bagimlilik (dependency) enjeksiyonu icin kullanilan oturum uretici.

    Kullanim (Faz 2, sunucu/api/ icinde):
        @uygulama.get("/yerler")
        def yerleri_listele(oturum: Session = Depends(oturum_al)):
            ...
    """
    oturum = OturumUretici()
    try:
        yield oturum
    finally:
        oturum.close()
