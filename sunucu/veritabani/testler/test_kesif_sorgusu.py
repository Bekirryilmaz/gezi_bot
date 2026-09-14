"""Kesif vitrin SQL filtresinin derlenmesi -- veritabani gerektirmez."""

from __future__ import annotations

from sqlalchemy.dialects.postgresql import dialect

from sunucu.veritabani.sorgular import _kesif_vitrin_kosulu


def test_kesif_filtresi_konaklamayi_haric_tutup_yeme_icme_ve_gezilecegi_ayirir():
    derlenmis = _kesif_vitrin_kosulu().compile(dialect=dialect())
    sql = str(derlenmis)
    bagli_degerler = " ".join(str(deger) for deger in derlenmis.params.values())

    assert "konaklama" not in sql and "konaklama" not in bagli_degerler
    assert "gezilecek_yer" in bagli_degerler
    assert "yeme_icme" in bagli_degerler
    assert "sehrin_klasigi" in bagli_degerler
    assert "sponsorlu_mekan" not in sql and "sponsorlu_mekan" not in bagli_degerler
    assert "kahvalti_verir" in bagli_degerler
    assert "duygu_skoru_ortalama" in sql
    assert "@>" in sql

