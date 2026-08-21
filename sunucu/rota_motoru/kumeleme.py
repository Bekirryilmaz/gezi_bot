"""
Yerleri gunlere bolen kumeleme mantigi.

Kutuphanesiz (k-means gibi bir bagimlilik gerektirmeden), acikca izlenebilir
bir yontem kullanilir: merkez noktadan (Senaryo 1'de konaklama, Senaryo
2'de secilen adaylarin agirlik merkezi) her adaya olan YON (bearing)
hesaplanip yerler bu aciya gore siralanir, ardindan `gun_sayisi` kadar
bitisik acisal dilime (sektore) bolunur. Boylece konaklama noktasindan
yelpaze gibi acilan, cografi olarak tutarli gun gruplari olusur -- k-means
gibi rastgele baslangica bagli olmayan, deterministik ve adim adim
aciklanabilir bir sonuc verir.
"""

from __future__ import annotations

from dataclasses import dataclass

from ortak.cografya_araclari import bearing_derece
from sunucu.rota_motoru.skorlama import SkorSonucu
from sunucu.rota_motoru.veri_tipleri import AdayYer
from sunucu.rota_motoru.zaman_butcesi import gun_butcesine_sigar_mi


@dataclass
class SkorluYer:
    yer: AdayYer
    skor: SkorSonucu


def agirlik_merkezi_hesapla(yerler: list[AdayYer]) -> tuple[float, float]:
    if not yerler:
        raise ValueError("Bos liste icin agirlik merkezi hesaplanamaz.")
    ortalama_enlem = sum(y.enlem for y in yerler) / len(yerler)
    ortalama_boylam = sum(y.boylam for y in yerler) / len(yerler)
    return ortalama_enlem, ortalama_boylam


def gunlere_boluster(
    skorlu_yerler: list[SkorluYer],
    gun_sayisi: int,
    merkez_nokta: tuple[float, float],
) -> dict[int, list[SkorluYer]]:
    """`merkez_nokta`dan her yere olan aciya (bearing) gore siralar,
    `gun_sayisi` kadar bitisik dilime boler, sonra her gunu zaman
    butcesine gore budar (bkz. `_zaman_butcesine_gore_budala`)."""
    if gun_sayisi < 1:
        raise ValueError("gun_sayisi en az 1 olmalidir.")
    if not skorlu_yerler:
        return {gun: [] for gun in range(1, gun_sayisi + 1)}

    merkez_enlem, merkez_boylam = merkez_nokta
    acili_yerler = sorted(
        skorlu_yerler,
        key=lambda sy: bearing_derece(merkez_enlem, merkez_boylam, sy.yer.enlem, sy.yer.boylam),
    )

    gunler: dict[int, list[SkorluYer]] = {gun: [] for gun in range(1, gun_sayisi + 1)}
    dilim_boyutu = max(1.0, len(acili_yerler) / gun_sayisi)
    for index, skorlu_yer in enumerate(acili_yerler):
        gun_no = min(gun_sayisi, int(index / dilim_boyutu) + 1)
        gunler[gun_no].append(skorlu_yer)

    return _zaman_butcesine_gore_budala(gunler, merkez_nokta)


def _zaman_butcesine_gore_budala(
    gunler: dict[int, list[SkorluYer]],
    merkez_nokta: tuple[float, float],
) -> dict[int, list[SkorluYer]]:
    """Her gunu, en yuksek skorlu duraktan baslayarak zaman butcesi
    doluncaya kadar sirayla ekler (skor onceliklendirmesi). Zorunlu
    duraklar cok yuksek skorlu olduklari icin (bkz. skorlama.py) neredeyse
    hep ilk secilirler."""
    budanmis: dict[int, list[SkorluYer]] = {}
    for gun_no, gun_yerleri in gunler.items():
        siralanmis = sorted(gun_yerleri, key=lambda sy: sy.skor.toplam_puan, reverse=True)
        secilenler: list[SkorluYer] = []
        onceki_nokta = merkez_nokta
        mevcut_dakika = 0
        for skorlu_yer in siralanmis:
            sigar_mi, yeni_toplam = gun_butcesine_sigar_mi(mevcut_dakika, skorlu_yer.yer, onceki_nokta)
            if sigar_mi or not secilenler:  # gunde en az 1 durak olsun
                secilenler.append(skorlu_yer)
                mevcut_dakika = yeni_toplam
                onceki_nokta = (skorlu_yer.yer.enlem, skorlu_yer.yer.boylam)
        budanmis[gun_no] = secilenler
    return budanmis
