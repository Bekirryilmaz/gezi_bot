"""siralama.py icin birim testleri."""

from __future__ import annotations

from ortak.cografya_araclari import haversine_metre
from sunucu.rota_motoru.kumeleme import SkorluYer
from sunucu.rota_motoru.siralama import gun_rotasini_sirala
from sunucu.rota_motoru.skorlama import SkorSonucu
from sunucu.rota_motoru.veri_tipleri import AdayYer


def _skorlu_yer(id: str, enlem: float, boylam: float) -> SkorluYer:
    yer = AdayYer(id=id, isim=id, ana_kategori="gezilecek_yer", alt_kategori="doga_manzara", enlem=enlem, boylam=boylam)
    return SkorluYer(yer=yer, skor=SkorSonucu(toplam_puan=0))


def _rota_uzunlugu(rota: list[SkorluYer], baslangic: tuple[float, float]) -> float:
    if not rota:
        return 0.0
    toplam = haversine_metre(baslangic[0], baslangic[1], rota[0].yer.enlem, rota[0].yer.boylam)
    for onceki, sonraki in zip(rota, rota[1:]):
        toplam += haversine_metre(onceki.yer.enlem, onceki.yer.boylam, sonraki.yer.enlem, sonraki.yer.boylam)
    return toplam


def test_siralama_kotu_baslangic_sirasini_iyilestirir():
    baslangic = (41.29, 36.33)
    # Bilerek verimsiz bir sira: uzak -> yakin -> orta -- 2-opt bunu duzeltmeli.
    yerler = [
        _skorlu_yer("uzak", 41.50, 36.60),
        _skorlu_yer("yakin", 41.30, 36.34),
        _skorlu_yer("orta", 41.35, 36.40),
    ]

    kotu_uzunluk = _rota_uzunlugu(yerler, baslangic)
    iyilestirilmis = gun_rotasini_sirala(yerler, baslangic)
    iyi_uzunluk = _rota_uzunlugu(iyilestirilmis, baslangic)

    assert iyi_uzunluk <= kotu_uzunluk
    assert {sy.yer.id for sy in iyilestirilmis} == {sy.yer.id for sy in yerler}


def test_tek_durak_degismeden_doner():
    baslangic = (41.29, 36.33)
    yerler = [_skorlu_yer("tek", 41.30, 36.34)]

    assert gun_rotasini_sirala(yerler, baslangic) == yerler


def test_bos_liste_bos_doner():
    assert gun_rotasini_sirala([], (41.29, 36.33)) == []
