"""
Bir gun icindeki duraklari en kisa rota olacak sekilde siralar.

Yontem: nearest-neighbor (acgozlu) ile bir baslangic rotasi olusturulur,
ardindan 2-opt ile iyilestirilir. Ikisi de klasik, kutuphanesiz TSP
sezgiselleridir -- adim adim izlenebilir, "kara kutu" degildir. Gunluk
durak sayisi kucuk oldugu icin (tipik olarak <10) 2-opt'un O(n^2) tekrar
maliyeti performans sorunu yaratmaz.
"""

from __future__ import annotations

from ortak.cografya_araclari import haversine_metre
from sunucu.rota_motoru.kumeleme import SkorluYer


def _mesafe(a: SkorluYer, b: SkorluYer) -> float:
    return haversine_metre(a.yer.enlem, a.yer.boylam, b.yer.enlem, b.yer.boylam)


def _baslangictan_mesafe(baslangic_noktasi: tuple[float, float], hedef: SkorluYer) -> float:
    return haversine_metre(baslangic_noktasi[0], baslangic_noktasi[1], hedef.yer.enlem, hedef.yer.boylam)


def _rota_uzunlugu(rota: list[SkorluYer], baslangic_noktasi: tuple[float, float]) -> float:
    if not rota:
        return 0.0
    toplam = _baslangictan_mesafe(baslangic_noktasi, rota[0])
    for onceki, sonraki in zip(rota, rota[1:]):
        toplam += _mesafe(onceki, sonraki)
    return toplam


def _en_yakin_komsu_rotasi(gunluk_yerler: list[SkorluYer], baslangic_noktasi: tuple[float, float]) -> list[SkorluYer]:
    kalanlar = list(gunluk_yerler)
    rota: list[SkorluYer] = []
    su_anki_nokta = baslangic_noktasi
    while kalanlar:
        en_yakin = min(
            kalanlar,
            key=lambda sy: haversine_metre(su_anki_nokta[0], su_anki_nokta[1], sy.yer.enlem, sy.yer.boylam),
        )
        rota.append(en_yakin)
        kalanlar.remove(en_yakin)
        su_anki_nokta = (en_yakin.yer.enlem, en_yakin.yer.boylam)
    return rota


def _iki_opt_iyilestir(rota: list[SkorluYer], baslangic_noktasi: tuple[float, float]) -> list[SkorluYer]:
    """Klasik 2-opt: rotadaki iki durak arasindaki segmenti ters cevirip
    toplam mesafeyi azaltip azaltmadigina bakar, azaltiyorsa uygular.
    Iyilestirme kalmayana kadar tekrarlanir."""
    en_iyi = rota
    iyilesme_var = True
    while iyilesme_var:
        iyilesme_var = False
        for i in range(len(en_iyi) - 1):
            for j in range(i + 1, len(en_iyi)):
                aday = en_iyi[:i] + en_iyi[i : j + 1][::-1] + en_iyi[j + 1 :]
                if _rota_uzunlugu(aday, baslangic_noktasi) < _rota_uzunlugu(en_iyi, baslangic_noktasi):
                    en_iyi = aday
                    iyilesme_var = True
    return en_iyi


def gun_rotasini_sirala(gunluk_yerler: list[SkorluYer], baslangic_noktasi: tuple[float, float]) -> list[SkorluYer]:
    if len(gunluk_yerler) <= 1:
        return list(gunluk_yerler)
    baslangic_rotasi = _en_yakin_komsu_rotasi(gunluk_yerler, baslangic_noktasi)
    return _iki_opt_iyilestir(baslangic_rotasi, baslangic_noktasi)
