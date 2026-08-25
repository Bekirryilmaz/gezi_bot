"""gunluk_slotlari_diz icin birim testleri -- veritabani gerektirmez."""

from __future__ import annotations

from ortak.sabitler import bekleme_payi_dk
from sunucu.rota_motoru.rota_olusturucu import _durak_maliyeti_dk, gunluk_slotlari_diz
from sunucu.rota_motoru.veri_tipleri import AdayYer, RotaTercihleri


def _yer(**alanlar) -> AdayYer:
    varsayilan = dict(
        id="x",
        isim="x",
        ana_kategori="gezilecek_yer",
        alt_kategori="tarihi_kulturel",
        enlem=41.29,
        boylam=36.33,
        deneyim_puanlari={"tarihi_kulturel_puani": 80},
        ortalama_ziyaret_suresi_dk=30,
    )
    varsayilan.update(alanlar)
    return AdayYer(**varsayilan)


def test_gunluk_slotlar_sabah_ogle_ikindi_aksam_sirasi():
    gezilecek = [
        _yer(id="muze", isim="muze", alt_kategori="tarihi_kulturel", enlem=41.291, boylam=36.331),
        _yer(id="park", isim="park", alt_kategori="doga_manzara", enlem=41.292, boylam=36.332),
    ]
    yeme = [
        _yer(
            id="lokanta",
            isim="lokanta",
            ana_kategori="yeme_icme",
            alt_kategori="restoran_lokanta",
            enlem=41.2905,
            boylam=36.3305,
            deneyim_puanlari={"gastronomi_puani": 90},
        ),
        _yer(
            id="meyhane",
            isim="meyhane",
            ana_kategori="yeme_icme",
            alt_kategori="meyhane_bar",
            enlem=41.293,
            boylam=36.333,
            deneyim_puanlari={"gastronomi_puani": 70},
        ),
        _yer(
            id="kahvalti",
            isim="kahvalti",
            ana_kategori="yeme_icme",
            alt_kategori="kafe",
            enlem=41.289,
            boylam=36.329,
            ozellikler={"kahvalti_verir": True},
        ),
    ]
    kullanilmis: set[str] = set()
    sonuc = gunluk_slotlari_diz(gezilecek, yeme, RotaTercihleri(), (41.29, 36.33), kullanilmis)

    idler = [sy.yer.id for sy in sonuc]
    assert idler[0] in {"muze", "park", "kahvalti"}
    assert "lokanta" in idler
    assert "meyhane" in idler
    assert len(idler) == len(set(idler))


def test_ogle_20_km_otesini_almaz():
    gezilecek = [_yer(id="muze", alt_kategori="tarihi_kulturel")]
    yakin_lokanta = _yer(
        id="yakin",
        ana_kategori="yeme_icme",
        alt_kategori="restoran_lokanta",
        enlem=41.291,
        boylam=36.331,
    )
    uzak_lokanta = _yer(
        id="uzak",
        ana_kategori="yeme_icme",
        alt_kategori="restoran_lokanta",
        enlem=41.50,
        boylam=36.70,
    )
    kullanilmis: set[str] = set()
    sonuc = gunluk_slotlari_diz(
        gezilecek, [uzak_lokanta, yakin_lokanta], RotaTercihleri(), (41.29, 36.33), kullanilmis
    )
    yeme_idler = [sy.yer.id for sy in sonuc if sy.yer.ana_kategori == "yeme_icme"]
    assert yeme_idler[0] == "yakin"


def test_durak_maliyeti_bekleme_payini_ekler():
    yer = _yer(ana_kategori="yeme_icme", alt_kategori="restoran_lokanta")
    yol, ziyaret, tampon = _durak_maliyeti_dk((41.29, 36.33), yer)
    assert tampon == bekleme_payi_dk("yeme_icme")
    assert yol >= 0
    assert ziyaret > 0


def test_konaklama_slota_girmez():
    otel = _yer(id="otel", ana_kategori="konaklama", alt_kategori="otel")
    muze = _yer(id="muze", alt_kategori="tarihi_kulturel")
    kullanilmis: set[str] = set()
    sonuc = gunluk_slotlari_diz([muze], [otel], RotaTercihleri(), (41.29, 36.33), kullanilmis)
    assert all(sy.yer.id != "otel" for sy in sonuc)
