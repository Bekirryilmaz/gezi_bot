"""
Cok boyutlu yer profili cikarma mantigi.

Girdi: veri/duygu_analizi/pipeline_calistir.py'nin urettigi IslenmisYorum
kayitlari (yorum bazli) + veri/esleme/eslestirici.py'nin urettigi BirlesikYer
kataloğu (yer bazli). Cikti: her yer icin veri/ortak/yer_profili_modeli.py::YerProfili.

Iki asamali calisir:
1. `yorumlari_yerlere_bagla`: her yorumu, kaynak+kaynak_id eslesmesiyle ait
   oldugu BirlesikYer'e baglar.
2. `yer_profili_olustur`: bir yere baglanan TUM yorumlari birlikte
   degerlendirip fiyat/ulasim/kalabalik/ziyaretci boyutlarini cikarir.

Tasarim felsefesi konu_analizi.py ile BIREBIR aynidir: BERT/kara kutu bir
model KULLANILMAZ, sadece anahtar kelime/ifade sayimi yapilir; her sonuc
`ornek_ifadeler` alaniyla kaynak metne kadar izlenebilir. Yeterli veri
olmayan boyutlar (`_AZ_VERI_ESIGI` altinda kalanlar) "bilgi_yetersiz"
donulur -- az veriyle uydurma bir izlenim verilmez.
"""

from __future__ import annotations

from collections import Counter, defaultdict

from ortak.sabitler import FiyatAlgisi, UlasimKolayligi, VeriKaynagi
from veri.duygu_analizi.konu_analizi import ifadelere_ayir
from veri.duygu_analizi.profil_sozlukleri import (
    FIYAT_PAHALI_IFADELERI,
    FIYAT_UCUZ_IFADELERI,
    ULASIM_KOLAY_IFADELERI,
    ULASIM_ZOR_IFADELERI,
    YOGUNLUK_IFADELERI,
    ZAMAN_DILIMI_IFADELERI,
    ZAMAN_GUN_TIPI_IFADELERI,
    ZIYARETCI_TIPI_IFADELERI,
)
from veri.duygu_analizi.yer_ismi_tespiti import metinde_gecen_yerleri_bul, yer_isimlerini_indeksle
from veri.ortak.birlesik_yer_modeli import BirlesikYer
from veri.ortak.metin_araclari import turkce_kucuk_harf
from veri.ortak.yer_profili_modeli import BoyutTespiti, YerProfili
from veri.ortak.yorum_modeli import IslenmisYorum

# Bir boyut hakkinda somut bir siniflandirma yapabilmek icin gereken minimum
# bahsedilme/yorum sayisi -- bunun altinda "bilgi_yetersiz" donulur. Diger
# esikler gibi (eslestirici.py, rapor_olustur.py) gercek veriyle test
# edilerek ayarlanmasi beklenir.
_AZ_VERI_ESIGI = 3
# Iki kutuplu (ucuz/pahali, kolay/zor) siniflandirmada net bir yon secmek
# icin bir tarafin digerine oranla en az kac kat fazla olmasi gerektigi;
# altinda kalirsa "orta/karisik" sayilir.
_BASKINLIK_ORANI = 1.5
# guven=1.0'a ulasmak icin gereken bahsedilme sayisi (uzeri de 1.0'da kalir).
_TAM_GUVEN_ESIGI = 10
# Bir zaman diliminin kalabalik/sakin olarak etiketlenebilmesi icin o
# yondeki bahsedilmelerin toplam icindeki payinin en az bu kadar olmasi gerekir.
_ZAMAN_BASKINLIK_ORANI = 0.6


def birlesik_yerleri_kimlige_gore_esle(birlesik_yerler: list[BirlesikYer]) -> dict[str, BirlesikYer]:
    """yer_kimligi -> BirlesikYer eslemesi. Raporlama ve anlatim uretimi
    asamalarinda yerin ismine/kategorisine erismek icin kullanilir."""
    return {yer.yer_kimligi: yer for yer in birlesik_yerler}


def yorumlari_yerlere_bagla(
    birlesik_yerler: list[BirlesikYer],
    islenmis_yorumlar: list[IslenmisYorum],
    yer_ismi_tespiti_ile_genislet: bool = True,
) -> tuple[dict[str, list[IslenmisYorum]], int]:
    """Her yorumu, kaynak+kaynak_id eslesmesiyle ait oldugu BirlesikYer'e
    baglar. Donus: (yer_kimligi -> yorum listesi, baglanamayan yorum sayisi).

    Eksi Sozluk'un bolge-geneli entry'leri (kaynak_yer_id = "bolge:...",
    bkz. eksi_sozluk_toplayici.py) hicbir BirlesikYer.kaynaklar girdisiyle
    DOGRUDAN eslesmez -- bunlar bolge profiline (bkz.
    bolge_profili_cikarici.py) ayrica katki saglar. Ama `yer_ismi_tespiti_ile_
    genislet=True` (varsayilan) ise, bu tur bir yorumun metninde BILINEN bir
    yer ismi geciyorsa (bkz. veri/duygu_analizi/yer_ismi_tespiti.py) o yorum
    FIRSATCI olarak o yerin profiline de eklenir -- yani boyle bir yorum HEM
    bolge profiline HEM (eslesirse) ilgili yerin profiline katki saglar."""
    kaynak_haritasi: dict[tuple[VeriKaynagi, str], BirlesikYer] = {}
    for yer in birlesik_yerler:
        for kaynak_ref in yer.kaynaklar:
            kaynak_haritasi[(kaynak_ref.kaynak, kaynak_ref.kaynak_id)] = yer

    yer_indeksi = yer_isimlerini_indeksle(birlesik_yerler) if yer_ismi_tespiti_ile_genislet else []

    sonuc: dict[str, list[IslenmisYorum]] = defaultdict(list)
    baglanamayan_sayisi = 0
    firsatci_baglanan_sayisi = 0
    for yorum in islenmis_yorumlar:
        yer = kaynak_haritasi.get((yorum.kaynak, yorum.kaynak_yer_id))
        if yer is not None:
            sonuc[yer.yer_kimligi].append(yorum)
            continue

        if yer_indeksi and yorum.kaynak_yer_id.startswith("bolge:"):
            eslesen_yer_kimlikleri = metinde_gecen_yerleri_bul(yorum.yorum_metni, yer_indeksi)
            if eslesen_yer_kimlikleri:
                for yer_kimligi in eslesen_yer_kimlikleri:
                    sonuc[yer_kimligi].append(yorum)
                firsatci_baglanan_sayisi += 1
                continue

        baglanamayan_sayisi += 1

    if firsatci_baglanan_sayisi:
        print(
            f"[BILGI] Yer-ismi tespitiyle {firsatci_baglanan_sayisi} bolge-geneli yorum, "
            "ilgili spesifik yer(ler)in profiline de baglandi."
        )

    return dict(sonuc), baglanamayan_sayisi


def _ifade_iceriyor_mu(ifade_kucuk: str, ifadeler: tuple[str, ...]) -> bool:
    return any(aranan in ifade_kucuk for aranan in ifadeler)


def _guven_hesapla(bahsedilme_sayisi: int) -> float:
    return round(min(1.0, bahsedilme_sayisi / _TAM_GUVEN_ESIGI), 2)


def _iki_kutuplu_boyut_belirle(
    yorum_metinleri: list[str],
    pozitif_yonde_ifadeler: tuple[str, ...],
    negatif_yonde_ifadeler: tuple[str, ...],
    pozitif_deger: str,
    negatif_deger: str,
    orta_deger: str,
    bilgi_yetersiz_deger: str,
) -> BoyutTespiti:
    """fiyat_algisi ve ulasim_kolayligi ayni 'iki kutuplu sayim' mantigini
    paylastigi icin ortak bir yardimci fonksiyonda toplanmistir."""
    pozitif_ifadeler: list[str] = []
    negatif_ifadeler: list[str] = []

    for metin in yorum_metinleri:
        for ifade in ifadelere_ayir(metin):
            ifade_kucuk = turkce_kucuk_harf(ifade)
            if _ifade_iceriyor_mu(ifade_kucuk, pozitif_yonde_ifadeler):
                pozitif_ifadeler.append(ifade)
            if _ifade_iceriyor_mu(ifade_kucuk, negatif_yonde_ifadeler):
                negatif_ifadeler.append(ifade)

    toplam = len(pozitif_ifadeler) + len(negatif_ifadeler)
    if toplam < _AZ_VERI_ESIGI:
        return BoyutTespiti(deger=bilgi_yetersiz_deger, guven=0.0, ornek_ifadeler=[])

    if len(pozitif_ifadeler) >= len(negatif_ifadeler) * _BASKINLIK_ORANI:
        deger, ornekler = pozitif_deger, pozitif_ifadeler
    elif len(negatif_ifadeler) >= len(pozitif_ifadeler) * _BASKINLIK_ORANI:
        deger, ornekler = negatif_deger, negatif_ifadeler
    else:
        deger, ornekler = orta_deger, pozitif_ifadeler + negatif_ifadeler

    return BoyutTespiti(deger=deger, guven=_guven_hesapla(toplam), ornek_ifadeler=ornekler[:3])


def fiyat_algisi_belirle(yorum_metinleri: list[str]) -> BoyutTespiti:
    return _iki_kutuplu_boyut_belirle(
        yorum_metinleri,
        pozitif_yonde_ifadeler=FIYAT_UCUZ_IFADELERI,
        negatif_yonde_ifadeler=FIYAT_PAHALI_IFADELERI,
        pozitif_deger=FiyatAlgisi.UCUZ.value,
        negatif_deger=FiyatAlgisi.PAHALI.value,
        orta_deger=FiyatAlgisi.ORTA.value,
        bilgi_yetersiz_deger=FiyatAlgisi.BILGI_YETERSIZ.value,
    )


def ulasim_kolayligi_belirle(yorum_metinleri: list[str]) -> BoyutTespiti:
    return _iki_kutuplu_boyut_belirle(
        yorum_metinleri,
        pozitif_yonde_ifadeler=ULASIM_KOLAY_IFADELERI,
        negatif_yonde_ifadeler=ULASIM_ZOR_IFADELERI,
        pozitif_deger=UlasimKolayligi.KOLAY.value,
        negatif_deger=UlasimKolayligi.ZOR.value,
        orta_deger=UlasimKolayligi.ORTA.value,
        bilgi_yetersiz_deger=UlasimKolayligi.BILGI_YETERSIZ.value,
    )


def kalabalik_zamanlari_belirle(yorum_metinleri: list[str]) -> dict[str, str]:
    """Bir ifadede yogunluk ifadesi (kalabalik/sakin) geciyorsa, bu her zaman
    genel bir 'genel' kovasina eklenir (zamandan bagimsiz genel egilim); eger
    AYNI ifadede bir zaman referansi (gun tipi ve/veya gunun saati) de
    geciyorsa, ayrica o zamana ozel bir kovaya da eklenir (orn.
    'hafta_sonu_aksam'). Boylece hem 'genelde kalabalik' hem 'ozellikle hafta
    sonu aksamlari kalabalik' gibi farkli detay seviyelerinde bilgi cikar."""
    sayimlar: dict[str, Counter] = defaultdict(Counter)

    for metin in yorum_metinleri:
        for ifade in ifadelere_ayir(metin):
            ifade_kucuk = turkce_kucuk_harf(ifade)

            yogunluk = None
            if _ifade_iceriyor_mu(ifade_kucuk, YOGUNLUK_IFADELERI["kalabalik"]):
                yogunluk = "kalabalik"
            elif _ifade_iceriyor_mu(ifade_kucuk, YOGUNLUK_IFADELERI["sakin"]):
                yogunluk = "sakin"
            if yogunluk is None:
                continue

            gun_tipleri = [
                gun_tipi for gun_tipi, ifadeler in ZAMAN_GUN_TIPI_IFADELERI.items() if _ifade_iceriyor_mu(ifade_kucuk, ifadeler)
            ]
            zaman_dilimleri = [
                zaman_dilimi
                for zaman_dilimi, ifadeler in ZAMAN_DILIMI_IFADELERI.items()
                if _ifade_iceriyor_mu(ifade_kucuk, ifadeler)
            ]

            sayimlar["genel"][yogunluk] += 1
            if gun_tipleri or zaman_dilimleri:
                # Ayni ifadede HEM 'hafta ici' HEM 'hafta sonu' (veya birden
                # fazla gunun saati) geciyorsa hangisine bagli oldugu
                # BELIRSIZDIR (orn. "hafta sonu kalabalik, hafta ici sakin"
                # tek cumlede iki karsit bilgi tasiyabilir) -- boyle bir
                # durumda yanlis bir tarafa yormak yerine 'genel' altina
                # dusurulur, sadece TEK bir eslesme varsa spesifik kabul edilir.
                gun_tipi_parcasi = gun_tipleri[0] if len(gun_tipleri) == 1 else "genel"
                zaman_dilimi_parcasi = zaman_dilimleri[0] if len(zaman_dilimleri) == 1 else "genel"
                if gun_tipi_parcasi != "genel" or zaman_dilimi_parcasi != "genel":
                    sayimlar[f"{gun_tipi_parcasi}_{zaman_dilimi_parcasi}"][yogunluk] += 1

    sonuc: dict[str, str] = {}
    for zaman_anahtari, sayim in sayimlar.items():
        toplam = sum(sayim.values())
        if toplam < _AZ_VERI_ESIGI:
            continue
        baskin_yogunluk, adet = sayim.most_common(1)[0]
        if adet / toplam >= _ZAMAN_BASKINLIK_ORANI:
            sonuc[zaman_anahtari] = baskin_yogunluk

    return sonuc


def ziyaretci_profili_belirle(yorum_metinleri: list[str]) -> dict[str, float]:
    """Her ziyaretci tipi icin, o tipten bahseden yorumlarin TOPLAM yorum
    sayisina orani (0-1). Bir yorum ayni tipten birden fazla ifade icerse
    bile en fazla 1 kez sayilir (bir yorumun "agirlik basmasi" onlenir)."""
    toplam_yorum = len(yorum_metinleri)
    if toplam_yorum < _AZ_VERI_ESIGI:
        return {}

    sayac: Counter[str] = Counter()
    for metin in yorum_metinleri:
        metin_kucuk = turkce_kucuk_harf(metin)
        bulunan_tipler = {
            tip for tip, ifadeler in ZIYARETCI_TIPI_IFADELERI.items() if _ifade_iceriyor_mu(metin_kucuk, ifadeler)
        }
        sayac.update(bulunan_tipler)

    return {tip: round(adet / toplam_yorum, 2) for tip, adet in sayac.items() if adet >= _AZ_VERI_ESIGI}


def yer_profili_olustur(yer_kimligi: str, yer_ismi: str, ilgili_yorumlar: list[IslenmisYorum]) -> YerProfili:
    yorum_metinleri = [yorum.yorum_metni for yorum in ilgili_yorumlar]
    return YerProfili(
        yer_kimligi=yer_kimligi,
        yer_ismi=yer_ismi,
        fiyat_algisi=fiyat_algisi_belirle(yorum_metinleri),
        ulasim_kolayligi=ulasim_kolayligi_belirle(yorum_metinleri),
        kalabalik_zamanlar=kalabalik_zamanlari_belirle(yorum_metinleri),
        ziyaretci_profili=ziyaretci_profili_belirle(yorum_metinleri),
        kullanilan_yorum_sayisi=len(ilgili_yorumlar),
    )
