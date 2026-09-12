"""slug_uret birim testleri (DB gerektirmez)."""

from ortak.metin_araclari import slug_uret


def test_turkce_karakterler():
    assert slug_uret("Bandırma Vapuru Müzesi") == "bandirma-vapuru-muzesi"


def test_basit_iki_kelime():
    assert slug_uret("Amisos Tepesi") == "amisos-tepesi"


def test_uzun_turkce_ad():
    assert slug_uret("Kızılırmak Deltası Kuş Cenneti") == "kizilirmak-deltasi-kus-cenneti"


def test_s_ve_g():
    assert slug_uret("Şahinkaya Kanyonu") == "sahinkaya-kanyonu"


def test_buyuk_i_combining_dot_yok():
    slug = slug_uret("İlkadım")
    assert slug == "ilkadim"
    assert "̇" not in slug  # combining dot above kalıntısı olmamalı


def test_tekrar_tire_ve_kenar():
    assert slug_uret("  Foo -- Bar!! ") == "foo-bar"


def test_bos_ve_gecersiz():
    assert slug_uret("") == "yer"
    assert slug_uret("!!!") == "yer"


def test_uzunluk_tavani():
    slug = slug_uret("a" * 100)
    assert len(slug) <= 60
    assert not slug.endswith("-")
