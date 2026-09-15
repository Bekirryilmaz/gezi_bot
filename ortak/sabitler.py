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

from enum import Enum, StrEnum


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
    INTERNET_KAFE = "internet_kafe"
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


class AmacEslemeSeviyesi(StrEnum):
    """Kategori kimliginin amac fact'i uretip uretmedigi."""

    DIRECT_PURPOSE_FACT = "direct_purpose_fact"
    WEAK_CANDIDATE_HINT = "weak_candidate_hint"
    NO_PURPOSE_INFERENCE = "no_purpose_inference"


class KimlikKaliteSinifi(StrEnum):
    """Yalniz dahili karar/operasyon; kamusal skor degildir."""

    DOGRULANMIS = "dogrulanmis"
    GUCLU = "guclu"
    KULLANILABILIR = "kullanilabilir"
    SUPHELI = "supheli"
    KARANTINA = "karantina"


# Yayimlanmis yer.alt_kategori -> acik amac fact'leri (yalniz DIRECT).
# Sozlukte olmayan kategoriden amac uydurulmaz.
# dokumanlar/kategori_taksonomisi.md #8.4
ALT_KATEGORI_AMAC_ESLEMESI: dict[str, tuple[str, ...]] = {
    YemeIcmeAltKategori.KAFE.value: ("kahve_icmek",),
    YemeIcmeAltKategori.KAHVE_UZMANLIK.value: ("kahve_icmek",),
    YemeIcmeAltKategori.RESTORAN_LOKANTA.value: ("yemek_yemek",),
    YemeIcmeAltKategori.KEBAP_IZGARA.value: ("yemek_yemek",),
    YemeIcmeAltKategori.DENIZ_MAHSULLERI.value: ("yemek_yemek",),
    YemeIcmeAltKategori.EV_YEMEKLERI_ESNAF.value: ("yemek_yemek",),
    YemeIcmeAltKategori.SOKAK_LEZZETI.value: ("yemek_yemek",),
    YemeIcmeAltKategori.FINE_DINING_ROMANTIK.value: ("yemek_yemek",),
    YemeIcmeAltKategori.MEYHANE_BAR.value: ("yemek_yemek",),
    YemeIcmeAltKategori.TATLI_PASTANE.value: ("tatli_yemek",),
    GezilecekYerAltKategori.TARIHI_KULTUREL.value: ("tarihi_kulturel_ziyaret",),
    GezilecekYerAltKategori.EGLENCE_AKTIVITE.value: ("eglence",),
    GezilecekYerAltKategori.DOGA_MANZARA.value: ("acik_hava",),
    GezilecekYerAltKategori.PLAJ_SU.value: ("acik_hava",),
}

# Zayif ipucu hard fact degildir; yalniz siralama/operasyon.
ALT_KATEGORI_AMAC_ZAYIF_IPUCU: dict[str, tuple[str, ...]] = {}

ONERIYE_UYGUN_KIMLIK_SINIFLARI: frozenset[str] = frozenset(
    {
        KimlikKaliteSinifi.DOGRULANMIS.value,
        KimlikKaliteSinifi.GUCLU.value,
        KimlikKaliteSinifi.KULLANILABILIR.value,
    }
)


def amac_esleme_seviyesi(alt_kategori: str | None, amac: str | None) -> AmacEslemeSeviyesi:
    if not alt_kategori or not amac:
        return AmacEslemeSeviyesi.NO_PURPOSE_INFERENCE
    if amac in ALT_KATEGORI_AMAC_ESLEMESI.get(alt_kategori, ()):
        return AmacEslemeSeviyesi.DIRECT_PURPOSE_FACT
    if amac in ALT_KATEGORI_AMAC_ZAYIF_IPUCU.get(alt_kategori, ()):
        return AmacEslemeSeviyesi.WEAK_CANDIDATE_HINT
    return AmacEslemeSeviyesi.NO_PURPOSE_INFERENCE


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


class DahiliSinyalAilesi(StrEnum):
    """Yalniz dahili gozlem adaylarinda kullanilan canonical sinyal aileleri."""

    SESSIZ_ORTAM = "sessiz_ortam"
    SOHBET_UYGUNLUGU = "sohbet_uygunlugu"
    CALISMA_UYGUNLUGU = "calisma_uygunlugu"
    AILE_UYGUNLUGU = "aile_uygunlugu"
    COCUK_UYGUNLUGU = "cocuk_uygunlugu"
    PARTNER_UYGUNLUGU = "partner_uygunlugu"
    ARKADAS_GRUBU_UYGUNLUGU = "arkadas_grubu_uygunlugu"
    ACIK_ALAN = "acik_alan"
    MANZARA = "manzara"
    KALABALIKLIK = "kalabaliklik"
    WIFI = "wifi"
    OTOPARK = "otopark"
    PRIZ = "priz"
    REZERVASYON = "rezervasyon"
    CANLI_MUZIK = "canli_muzik"
    KAHVE = "kahve"
    YEMEK = "yemek"
    KAHVALTI = "kahvalti"
    TATLI = "tatli"
    EGLENCE = "eglence"
    TARIHI_KULTUREL = "tarihi_kulturel"
    ACIK_HAVA = "acik_hava"
    FIYAT_ALGISI = "fiyat_algisi"
    GENEL_DUYGU = "genel_duygu"


class GozlemTuru(StrEnum):
    """Dahili sinyalin olgu, deneyim veya genel duygu ayrimi."""

    FACT_SIGNAL = "fact_signal"
    EXPERIENCE_SIGNAL = "experience_signal"
    SENTIMENT_SIGNAL = "sentiment_signal"


class SinyalYonu(StrEnum):
    """Bir spanin ilgili aileyi destekleme veya ona karsi olma yonu."""

    SUPPORT = "support"
    COUNTER = "counter"


class CikarimYontemi(StrEnum):
    """Aday gozlemin yeniden uretilebilir cikarim yontemi."""

    DETERMINISTIK_KURAL = "deterministik_kural"
    DUYGU_MODELI = "duygu_modeli"
    GERIYE_UYUMLU = "geriye_uyumlu"


class ZamansalDurum(StrEnum):
    """Aday sinyalin zaman bakimindan bilinen dar durumu."""

    UNKNOWN = "unknown"
    CURRENT = "current"
    HISTORICAL = "historical"


class AdaySozlesmeSurumu(StrEnum):
    """AdayGozlem parse ve dogrulama sozlesmesi."""

    CANONICAL_V1 = "canonical-v1"
    LEGACY = "legacy"


# (aile, gozlem_turu, yon) -> izinli canonical degerler.
DAHILI_SINYAL_DEGER_SOZLUGU: dict[
    tuple[str, str, str], tuple[bool | str, ...]
] = {
    ("wifi", "fact_signal", "support"): (True,),
    ("wifi", "fact_signal", "counter"): (False,),
    ("wifi", "experience_signal", "support"): (
        "kotu_degil",
        "cok_yavas_degil",
        True,
    ),
    ("wifi", "experience_signal", "counter"): (
        "kotu",
        "cok_yavas",
        "cekmiyor",
        False,
    ),
    ("sessiz_ortam", "experience_signal", "support"): (True,),
    ("sessiz_ortam", "experience_signal", "counter"): (False,),
    ("aile_uygunlugu", "experience_signal", "support"): (True,),
    ("aile_uygunlugu", "experience_signal", "counter"): (False,),
    ("cocuk_uygunlugu", "experience_signal", "support"): (True,),
    ("cocuk_uygunlugu", "experience_signal", "counter"): (False,),
    ("calisma_uygunlugu", "experience_signal", "support"): (True,),
    ("calisma_uygunlugu", "experience_signal", "counter"): (False,),
    ("acik_alan", "fact_signal", "support"): (True,),
    ("acik_alan", "fact_signal", "counter"): (False,),
    ("manzara", "fact_signal", "support"): (True,),
    ("manzara", "fact_signal", "counter"): (False,),
    ("manzara", "experience_signal", "support"): ("guzel",),
    ("manzara", "experience_signal", "counter"): ("gorunmuyor", "goremedik"),
    ("fiyat_algisi", "experience_signal", "support"): ("uygun", "pahali_degil"),
    ("fiyat_algisi", "experience_signal", "counter"): ("pahali",),
    ("otopark", "fact_signal", "support"): (True,),
    ("otopark", "fact_signal", "counter"): (False,),
    ("otopark", "experience_signal", "counter"): ("park_sorunu",),
    ("rezervasyon", "experience_signal", "counter"): (
        "rezervasyonsuz_yer_bulunamadi",
    ),
    ("canli_muzik", "fact_signal", "support"): (True,),
    ("canli_muzik", "fact_signal", "counter"): (False,),
    ("canli_muzik", "experience_signal", "support"): ("cok_yuksek_degil",),
    ("canli_muzik", "experience_signal", "counter"): ("cok_yuksek",),
    ("kalabaliklik", "experience_signal", "support"): ("kalabalik",),
    ("kalabaliklik", "experience_signal", "counter"): ("sakin",),
}

for _sentiment_ailesi in (
    "manzara",
    "fiyat_algisi",
    "yemek",
    "kalabaliklik",
    "kahvalti",
    "sessiz_ortam",
    "genel_duygu",
):
    DAHILI_SINYAL_DEGER_SOZLUGU[
        (_sentiment_ailesi, "sentiment_signal", "support")
    ] = ("olumlu",)
    DAHILI_SINYAL_DEGER_SOZLUGU[
        (_sentiment_ailesi, "sentiment_signal", "counter")
    ] = ("olumsuz",)

KARAR_DISI_DAHILI_SINYAL_AILELERI: frozenset[str] = frozenset({"genel_duygu"})


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


class OzelEtiket(str, Enum):
    """Kurasyon, ticari ve hizmet etiketleri. `ozellikler` JSONB icinde
    evet/hayir olarak tutulur (bkz. dokumanlar/kategori_taksonomisi.md #2
    ve #2.1). Ana/alt kategori degildir."""

    SEHRIN_KLASIGI = "sehrin_klasigi"
    SPONSORLU_MEKAN = "sponsorlu_mekan"
    KAHVALTI_VERIR = "kahvalti_verir"


OZEL_ETIKETLER: tuple[str, ...] = tuple(etiket.value for etiket in OzelEtiket)


class ZamanDilimi(str, Enum):
    """Gun ici zaman dilimleri. Rota motoru bir duragi hangi saatte
    onerecegini bu anahtarlara gore karar verir.
    dokumanlar/kategori_taksonomisi.md #9."""

    SABAH = "sabah"
    OGLE = "ogle"
    IKINDI = "ikindi"
    AKSAM = "aksam"
    GECE = "gece"


# Alt kategori -> o kategorinin dogal olarak uyumlu oldugu zaman dilimleri.
# Listede olmayan alt kategoriler icin rota motoru kisit uygulamaz.
KATEGORI_ZAMAN_DILIMLERI: dict[str, list[str]] = {
    YemeIcmeAltKategori.KAHVE_UZMANLIK.value: [
        ZamanDilimi.SABAH.value,
        ZamanDilimi.IKINDI.value,
    ],
    YemeIcmeAltKategori.RESTORAN_LOKANTA.value: [
        ZamanDilimi.OGLE.value,
        ZamanDilimi.AKSAM.value,
    ],
    YemeIcmeAltKategori.KEBAP_IZGARA.value: [
        ZamanDilimi.OGLE.value,
        ZamanDilimi.AKSAM.value,
    ],
    YemeIcmeAltKategori.DENIZ_MAHSULLERI.value: [
        ZamanDilimi.OGLE.value,
        ZamanDilimi.AKSAM.value,
    ],
    YemeIcmeAltKategori.EV_YEMEKLERI_ESNAF.value: [
        ZamanDilimi.OGLE.value,
        ZamanDilimi.AKSAM.value,
    ],
    YemeIcmeAltKategori.SOKAK_LEZZETI.value: [
        ZamanDilimi.OGLE.value,
        ZamanDilimi.AKSAM.value,
    ],
    YemeIcmeAltKategori.FINE_DINING_ROMANTIK.value: [
        ZamanDilimi.AKSAM.value,
        ZamanDilimi.GECE.value,
    ],
    YemeIcmeAltKategori.MEYHANE_BAR.value: [
        ZamanDilimi.AKSAM.value,
        ZamanDilimi.GECE.value,
    ],
    GezilecekYerAltKategori.GECE_HAYATI.value: [
        ZamanDilimi.GECE.value,
    ],
    GezilecekYerAltKategori.TARIHI_KULTUREL.value: [
        ZamanDilimi.SABAH.value,
        ZamanDilimi.OGLE.value,
        ZamanDilimi.IKINDI.value,
    ],
    GezilecekYerAltKategori.DOGA_MANZARA.value: [
        ZamanDilimi.SABAH.value,
        ZamanDilimi.OGLE.value,
        ZamanDilimi.IKINDI.value,
    ],
    GezilecekYerAltKategori.DINI_MANEVI.value: [
        ZamanDilimi.SABAH.value,
        ZamanDilimi.OGLE.value,
        ZamanDilimi.IKINDI.value,
    ],
    GezilecekYerAltKategori.FOTOGRAF_NOKTASI.value: [
        ZamanDilimi.SABAH.value,
        ZamanDilimi.OGLE.value,
        ZamanDilimi.IKINDI.value,
    ],
    GezilecekYerAltKategori.ALISVERIS.value: [
        ZamanDilimi.SABAH.value,
        ZamanDilimi.OGLE.value,
        ZamanDilimi.IKINDI.value,
    ],
    GezilecekYerAltKategori.PLAJ_SU.value: [
        ZamanDilimi.SABAH.value,
        ZamanDilimi.OGLE.value,
        ZamanDilimi.IKINDI.value,
    ],
    GezilecekYerAltKategori.EGLENCE_AKTIVITE.value: [
        ZamanDilimi.SABAH.value,
        ZamanDilimi.OGLE.value,
        ZamanDilimi.IKINDI.value,
    ],
    GezilecekYerAltKategori.SPOR_DOGA_YURUYUS.value: [
        ZamanDilimi.SABAH.value,
        ZamanDilimi.OGLE.value,
        ZamanDilimi.IKINDI.value,
    ],
    YemeIcmeAltKategori.TATLI_PASTANE.value: [
        ZamanDilimi.OGLE.value,
        ZamanDilimi.IKINDI.value,
        ZamanDilimi.AKSAM.value,
    ],
    YemeIcmeAltKategori.CAY_BAHCESI.value: [
        ZamanDilimi.OGLE.value,
        ZamanDilimi.IKINDI.value,
        ZamanDilimi.AKSAM.value,
    ],
}


# Ana kategori -> mekan ici ziyaret suresine EKLENEN lojistik tampon (dk).
# Park, kuyruk, garson/hesap, tuvalet/dinlenme gibi insan payi.
# dokumanlar/kategori_taksonomisi.md #10.
MEKAN_BEKLEME_SURELERI_DK: dict[str, int] = {
    AnaKategori.YEME_ICME.value: 30,
    AnaKategori.GEZILECEK_YER.value: 15,
    AnaKategori.KONAKLAMA.value: 20,
}

_VARSAYILAN_BEKLEME_PAYI_DK = 15


def zaman_dilimi_uygun_mu(alt_kategori: str, zaman_dilimi: str) -> bool:
    """Bu alt kategori verilen dilimde dogal mi? Sozlukte yoksa kisit yok."""
    dilimler = KATEGORI_ZAMAN_DILIMLERI.get(alt_kategori)
    if dilimler is None:
        return True
    return zaman_dilimi in dilimler


def uygun_zaman_dilimleri(alt_kategori: str) -> list[str]:
    """Alt kategorinin uyumlu dilimleri. Tanimli degilse tum dilimleri verir."""
    dilimler = KATEGORI_ZAMAN_DILIMLERI.get(alt_kategori)
    if dilimler is None:
        return [dilim.value for dilim in ZamanDilimi]
    return list(dilimler)


def bekleme_payi_dk(ana_kategori: str) -> int:
    """Ziyaret suresine eklenecek lojistik tampon (dk). Bilinmiyorsa 15."""
    return MEKAN_BEKLEME_SURELERI_DK.get(ana_kategori, _VARSAYILAN_BEKLEME_PAYI_DK)


class RotaKapsamSinifi(StrEnum):
    """Rota/karar bilgi ailesinin kritikligi. Kamusal skor degildir."""

    ROTA_KRITIK = "rota_kritik"
    KARAR_ONEMLI = "karar_onemli"
    ISTEGE_BAGLI = "istege_bagli"


class RotaHazirlikDurumu(StrEnum):
    """Ic rota hazirlik durumu; kamusal skor veya sira bonusu degildir."""

    ROTA_HAZIR = "rota_hazir"
    ROTA_SINIRLI = "rota_sinirli"
    KESIF_ADAYI = "kesif_adayi"
    ROTA_KAPALI = "rota_kapali"


class TamamlikHucresi(StrEnum):
    """Pilot tamamlik matrisi hucresi."""

    BILINIYOR = "biliniyor"
    BILINMIYOR = "bilinmiyor"
    ESKIMIS = "eskimis"
    CELISKILI = "celiskili"
    YALNIZ_DAHILI = "yalniz_dahili"


class CalismaSaatiDurumu(StrEnum):
    """opening_hours ayrıştırma durumu. Tahmin yoktur."""

    KNOWN = "known"
    PARTIALLY_KNOWN = "partially_known"
    UNKNOWN = "unknown"
    INVALID = "invalid"
    STALE = "stale"


class ZiyaretSuresiKaynagi(StrEnum):
    """Ziyaret suresinin nereden geldigi. Sezgisel fact degildir."""

    DOGRULANMIS_SURE = "dogrulanmis_sure"
    BILINEN_DOGRULANMIS = "dogrulanmis_sure"
    PLANLAMA_TAHMINI = "planlama_tahmini"
    KATEGORI_SEZGISEL = "planlama_tahmini"
    KULLANICI_SECIMI = "kullanici_secimi"
    BILINMIYOR = "bilinmiyor"


class RotaBilinmeyenDavranis(StrEnum):
    """FAZ 26 unknown sozlesmesi. Motor bu fazda yazilmaz."""

    HARD_BLOK = "hard_block"
    SINIRLI_UYARI = "limited_route"


class RotaHazirlikNedeni(StrEnum):
    """Rota hazirlik kirilimi; aciklanabilir reason code."""

    KIMLIK_KARANTINA = "kimlik_karantina"
    KIMLIK_SUPHELI = "kimlik_supheli"
    KIMLIK_UYGUN = "kimlik_uygun"
    SUBE_AKTIF_DEGIL = "sube_aktif_degil"
    KOORDINAT_GECERSIZ = "koordinat_gecersiz"
    KOORDINAT_UYGUN = "koordinat_uygun"
    ILCE_EKSIK = "ilce_eksik"
    ILCE_UYGUN = "ilce_uygun"
    AMAC_BILINMIYOR = "amac_bilinmiyor"
    AMAC_BILINIYOR = "amac_biliniyor"
    YAYIN_UYGUN_DEGIL = "yayin_uygun_degil"
    YAYIN_UYGUN = "yayin_uygun"
    CALISMA_SAATI_BILINIYOR = "calisma_saati_biliniyor"
    CALISMA_SAATI_BILINMIYOR = "calisma_saati_bilinmiyor"
    CALISMA_SAATI_YALNIZ_DAHILI = "calisma_saati_yalniz_dahili"
    CALISMA_SAATI_GECERSIZ = "calisma_saati_gecersiz"
    CALISMA_SAATI_PARCALI = "calisma_saati_parcali"
    CALISMA_SAATI_ESKIMIS = "calisma_saati_eskimis"
    ROTA_KRITIK_EKSIK = "rota_kritik_eksik"


# dokumanlar/kategori_taksonomisi.md #11.1
ROTA_KAPSAM_AILELERI: dict[str, str] = {
    "kimlik": RotaKapsamSinifi.ROTA_KRITIK.value,
    "ilce": RotaKapsamSinifi.ROTA_KRITIK.value,
    "koordinat": RotaKapsamSinifi.ROTA_KRITIK.value,
    "amac": RotaKapsamSinifi.ROTA_KRITIK.value,
    "calisma_saatleri": RotaKapsamSinifi.ROTA_KRITIK.value,
    "ziyaret_suresi": RotaKapsamSinifi.KARAR_ONEMLI.value,
    "rezervasyon": RotaKapsamSinifi.KARAR_ONEMLI.value,
    "wifi": RotaKapsamSinifi.KARAR_ONEMLI.value,
    "otopark": RotaKapsamSinifi.KARAR_ONEMLI.value,
    "acik_alan": RotaKapsamSinifi.KARAR_ONEMLI.value,
    "tekerlekli_sandalye_erisimi": RotaKapsamSinifi.KARAR_ONEMLI.value,
    "aile": RotaKapsamSinifi.KARAR_ONEMLI.value,
    "cocuk": RotaKapsamSinifi.KARAR_ONEMLI.value,
    "calisma": RotaKapsamSinifi.KARAR_ONEMLI.value,
    "sessizlik": RotaKapsamSinifi.KARAR_ONEMLI.value,
    "manzara": RotaKapsamSinifi.KARAR_ONEMLI.value,
    "fiyat": RotaKapsamSinifi.KARAR_ONEMLI.value,
    "web_sitesi": RotaKapsamSinifi.ISTEGE_BAGLI.value,
    "telefon": RotaKapsamSinifi.ISTEGE_BAGLI.value,
}

ROTA_AMAC_HAVUZLARI: dict[str, tuple[str, ...]] = {
    "kahve_icmek": (
        YemeIcmeAltKategori.KAFE.value,
        YemeIcmeAltKategori.KAHVE_UZMANLIK.value,
    ),
    "yemek_yemek": (
        YemeIcmeAltKategori.RESTORAN_LOKANTA.value,
        YemeIcmeAltKategori.KEBAP_IZGARA.value,
        YemeIcmeAltKategori.DENIZ_MAHSULLERI.value,
        YemeIcmeAltKategori.EV_YEMEKLERI_ESNAF.value,
        YemeIcmeAltKategori.SOKAK_LEZZETI.value,
        YemeIcmeAltKategori.FINE_DINING_ROMANTIK.value,
        YemeIcmeAltKategori.MEYHANE_BAR.value,
    ),
    "tatli_yemek": (YemeIcmeAltKategori.TATLI_PASTANE.value,),
    "tarihi_kulturel_ziyaret": (GezilecekYerAltKategori.TARIHI_KULTUREL.value,),
    "acik_hava": (
        GezilecekYerAltKategori.DOGA_MANZARA.value,
        GezilecekYerAltKategori.PLAJ_SU.value,
    ),
    "eglence": (GezilecekYerAltKategori.EGLENCE_AKTIVITE.value,),
}

GRUP_INCELEME_DUSUK_RISK_AILELERI: frozenset[str] = frozenset(
    {
        "web_sitesi",
        "telefon",
        "adres",
        "yer_turu",
        "calisma_saatleri",
        "otopark",
        "acik_alan",
        "wifi",
        "rezervasyon",
    }
)
GRUP_INCELEME_KRITIK_AILELER: frozenset[str] = frozenset(
    {
        "giris_basamak",
        "fiziksel_erisim",
        "tekerlekli_sandalye_erisimi",
        "calisma_saati",
        "ziyaret_kosulu",
        "amac_destegi",
    }
)
