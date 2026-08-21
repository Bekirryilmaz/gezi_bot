"""
Tum toplayicilarin (veri/), veritabani semasinin (sunucu/) ve ileride sitenin
(site/) kullanacagi ortak taksonomi sabitleri.

Bu dosya bilerek `veri/` veya `sunucu/` altinda degil, en ust seviyede
`ortak/` altinda tutuluyor: kategori taksonomisi hem veri toplama hem de
sunucu tarafinin ortak "sozlugu" oldugu icin tek bir yerden yonetilmeli.
Boylece iki tarafta ayni seyi iki kere tanimlayip zamanla birbirinden
sapmasini onlemis oluyoruz.

Bu dosya dokumanlar/kategori_taksonomisi.md ile birebir eslesir. Taksonomiyi
degistirdiginde iki dosyayi da guncelle, aralarinda fark olmasin.
"""

from enum import Enum


class AnaKategori(str, Enum):
    """Bir yerin en ust seviye siniflandirmasi."""

    GEZILECEK_YER = "gezilecek_yer"
    KONAKLAMA = "konaklama"
    YEME_ICME = "yeme_icme"


class GezilecekYerAltKategori(str, Enum):
    """AnaKategori.GEZILECEK_YER icin alt kategoriler."""

    TARIHI_KULTUREL = "tarihi_kulturel"
    DOGA_MANZARA = "doga_manzara"
    PLAJ_SU = "plaj_su"
    EGLENCE_AKTIVITE = "eglence_aktivite"
    GECE_HAYATI = "gece_hayati"
    ALISVERIS = "alisveris"
    SPOR_DOGA_YURUYUS = "spor_doga_yuruyus"
    DINI_MANEVI = "dini_manevi"
    FOTOGRAF_NOKTASI = "fotograf_noktasi"


class KonaklamaAltKategori(str, Enum):
    """AnaKategori.KONAKLAMA icin alt kategoriler."""

    OTEL = "otel"
    PANSIYON_APART = "pansiyon_apart"
    KAMP_KARAVAN = "kamp_karavan"
    HOSTEL = "hostel"
    EV_KIRALAMA = "ev_kiralama"


class YemeIcmeAltKategori(str, Enum):
    """AnaKategori.YEME_ICME icin alt kategoriler."""

    RESTORAN_LOKANTA = "restoran_lokanta"
    DENIZ_MAHSULLERI = "deniz_mahsulleri"
    KEBAP_IZGARA = "kebap_izgara"
    EV_YEMEKLERI_ESNAF = "ev_yemekleri_esnaf"
    FINE_DINING_ROMANTIK = "fine_dining_romantik"
    SOKAK_LEZZETI = "sokak_lezzeti"
    KAFE = "kafe"
    TATLI_PASTANE = "tatli_pastane"
    KAHVE_UZMANLIK = "kahve_uzmanlik"
    MEYHANE_BAR = "meyhane_bar"
    CAY_BAHCESI = "cay_bahcesi"


# Ana kategori -> gecerli alt kategoriler eslemesi. Dogrulama (validation)
# icin veri modellerinde kullanilir.
ANA_KATEGORI_ALT_KATEGORILERI: dict[str, type[Enum]] = {
    AnaKategori.GEZILECEK_YER.value: GezilecekYerAltKategori,
    AnaKategori.KONAKLAMA.value: KonaklamaAltKategori,
    AnaKategori.YEME_ICME.value: YemeIcmeAltKategori,
}


class Aktivite(str, Enum):
    """Kullanicinin 'yapmak istedigim bir eylem var' dedigi senaryoda kullanilir."""

    YUZME = "yuzme"
    YURUYUS_TREKKING = "yuruyus_trekking"
    KANO_SUP = "kano_sup"
    DALIS = "dalis"
    AT_BINME = "at_binme"
    BISIKLET = "bisiklet"
    KAMP = "kamp"
    FOTOGRAFCILIK = "fotografcilik"
    KUS_GOZLEMCILIGI = "kus_gozlemciligi"
    TEKNE_TURU = "tekne_turu"
    YAMAC_PARASUTU = "yamac_parasutu"
    KAYAK = "kayak"


class VeriKaynagi(str, Enum):
    """Bir veri parcasinin nereden geldigini gosterir. Izlenebilirlik icin sart."""

    OPENSTREETMAP = "openstreetmap"
    GOOGLE_MAPS = "google_maps"
    EKSI_SOZLUK = "eksi_sozluk"
    TRIPADVISOR = "tripadvisor"
    BOOKING_COM = "booking_com"
    SITE_ICI = "site_ici"
    ELLE_GIRILEN = "elle_girilen"


class FiyatSeviyesi(int, Enum):
    """1=ucuz ... 4=cok pahali. dokumanlar/kategori_taksonomisi.md #2'ye bakiniz."""

    UCUZ = 1
    ORTA = 2
    PAHALI = 3
    COK_PAHALI = 4


class DuyguEtiketi(str, Enum):
    """Duygu analizi pipeline'inin urettigi genel duygu sinifi."""

    OLUMLU = "olumlu"
    NOTR = "notr"
    OLUMSUZ = "olumsuz"


class FiyatAlgisi(str, Enum):
    """Yorumlardan cikarilan OZNEL fiyat algisi. dokumanlar/kategori_taksonomisi.md
    #6'ya bakiniz. NOT: FiyatSeviyesi (yukarida) kaynak verisinden gelen
    OBJEKTIF bir ozellik etiketidir (orn. Google Maps'in 1-4 fiyat isaretlemesi);
    FiyatAlgisi ise ziyaretcilerin YAZDIKLARINA gore sonradan sentezlenen algidir
    -- ikisi farkli kaynaklardan gelir ve birbirinin yerine gecmez."""

    UCUZ = "ucuz"
    ORTA = "orta"
    PAHALI = "pahali"
    BILGI_YETERSIZ = "bilgi_yetersiz"


class UlasimKolayligi(str, Enum):
    """Yorumlardan cikarilan ulasim/erisim kolayligi algisi.
    dokumanlar/kategori_taksonomisi.md #6'ya bakiniz."""

    KOLAY = "kolay"
    ORTA = "orta"
    ZOR = "zor"
    BILGI_YETERSIZ = "bilgi_yetersiz"


class DeneyimEksen(str, Enum):
    """Rota algoritmasinin kullanici tercihleriyle eslestirme yaparken kullandigi
    0-100 arasi puan eksenleri. dokumanlar/kategori_taksonomisi.md #4'e bakiniz."""

    TARIHI_KULTUREL = "tarihi_kulturel_puani"
    EGLENCE = "eglence_puani"
    DOGA_MACERA = "doga_macera_puani"
    GASTRONOMI = "gastronomi_puani"
    GECE_HAYATI = "gece_hayati_puani"
    RAHATLATICI_SAKIN = "rahatlatici_sakin_puani"


# Alt kategori -> varsayilan deneyim eksen puanlari. Yeni bir yer eklendiginde
# (henuz yorum/duygu analizi verisi yokken) baslangic degeri olarak kullanilir.
# Degerler 0-100 arasidir, zamanla duygu analizi ve kuratorlukle guncellenir.
VARSAYILAN_DENEYIM_PUANLARI: dict[str, dict[str, int]] = {
    GezilecekYerAltKategori.TARIHI_KULTUREL.value: {
        DeneyimEksen.TARIHI_KULTUREL.value: 90,
        DeneyimEksen.RAHATLATICI_SAKIN.value: 40,
    },
    GezilecekYerAltKategori.DOGA_MANZARA.value: {
        DeneyimEksen.DOGA_MACERA.value: 80,
        DeneyimEksen.RAHATLATICI_SAKIN.value: 70,
    },
    GezilecekYerAltKategori.PLAJ_SU.value: {
        DeneyimEksen.DOGA_MACERA.value: 70,
        DeneyimEksen.EGLENCE.value: 50,
    },
    GezilecekYerAltKategori.EGLENCE_AKTIVITE.value: {
        DeneyimEksen.EGLENCE.value: 90,
    },
    GezilecekYerAltKategori.GECE_HAYATI.value: {
        DeneyimEksen.GECE_HAYATI.value: 95,
        DeneyimEksen.EGLENCE.value: 60,
    },
    GezilecekYerAltKategori.ALISVERIS.value: {
        DeneyimEksen.EGLENCE.value: 40,
    },
    GezilecekYerAltKategori.SPOR_DOGA_YURUYUS.value: {
        DeneyimEksen.DOGA_MACERA.value: 90,
    },
    GezilecekYerAltKategori.DINI_MANEVI.value: {
        DeneyimEksen.TARIHI_KULTUREL.value: 60,
        DeneyimEksen.RAHATLATICI_SAKIN.value: 60,
    },
    GezilecekYerAltKategori.FOTOGRAF_NOKTASI.value: {
        DeneyimEksen.DOGA_MACERA.value: 50,
        DeneyimEksen.RAHATLATICI_SAKIN.value: 40,
    },
}
