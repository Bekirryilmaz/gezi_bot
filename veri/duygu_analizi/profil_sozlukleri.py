"""
Yer profili cikarimi icin anahtar kelime/ifade sozlukleri.

`konu_analizi.py`'deki `KONU_ANAHTAR_KELIMELERI`, bir YORUMUN hangi konudan
bahsettigini bulur (yorum bazli, tek yorumun icindeki bir cumleyi degerlendirir).
Buradaki sozlukler ise bir YERIN TUM yorumlari birlikte degerlendirilerek o
yerin fiyat algisi, ulasim kolayligi, kalabalik zamanlari ve ziyaretci profili
gibi YER BAZLI (aggregate) boyutlarini cikarmak icin kullanilir -- bkz.
`veri/duygu_analizi/yer_profili_cikarici.py`.

Ayni felsefe gecerlidir: BERT/kara kutu bir model KULLANILMAZ, sadece anahtar
kelime/ifade eslestirmesi yapilir. Kapsami genisletmek (yeni bir ziyaretci
tipi, yeni bir fiyat ifadesi vb. eklemek) istersen kod degistirmen gerekmez,
sadece asagidaki listelere yeni ifade eklemen yeterlidir.

BILINCLI SINIRLAMA: konu_analizi.py'deki genel duygu kelimelerinin aksine,
buradaki ifadeler icin OLUMSUZLUK (negation) tespiti YAPILMAZ (orn. "hic
pahali degil" ifadesi yine de "pahali" ifadesiyle eslesir). Sebep: bu
boyutlar tekil bir "duygu kutbu" degil, SIK GECEN somut ifadeleri sayarak
COGUNLUK egilimini bulmaya calisir -- buyuk yorum sayilarinda bu basitlestirme
kabul edilebilir gurultu seviyesinde kalir, ayrica tam negation mantigi
eklemek konu_analizi.py'nin karmasikligini burada tekrarlamak anlamina
gelirdi. Zamanla gerek gorulurse ayni negation penceresi buraya da eklenebilir.
"""

from __future__ import annotations

# --- Fiyat algisi -----------------------------------------------------------

FIYAT_UCUZ_IFADELERI: tuple[str, ...] = (
    "ucuz", "hesaplı", "hesapli", "uygun fiyat", "makul fiyat", "ekonomik",
    "cok uygun", "fiyat performans", "cok hesaplı", "cok hesapli", "cok ucuz",
)
FIYAT_PAHALI_IFADELERI: tuple[str, ...] = (
    "pahalı", "pahali", "yüksek fiyat", "yuksek fiyat", "fahiş", "fahis",
    "soygun", "tuzluk", "cok tuttu", "cebi yakan", "fiyatlar yüksek", "fiyatlar yuksek",
)

# --- Ulasim kolayligi --------------------------------------------------------

ULASIM_KOLAY_IFADELERI: tuple[str, ...] = (
    "merkezi konum", "merkeze yakın", "merkeze yakin", "kolay ulaşım", "kolay ulasim",
    "yürüme mesafesinde", "yurume mesafesinde", "otopark bol", "otoparklı", "otoparkli",
    "ulaşımı kolay", "ulasimi kolay", "ulaşımı rahat", "ulasimi rahat",
)
ULASIM_ZOR_IFADELERI: tuple[str, ...] = (
    "ulaşımı zor", "ulasimi zor", "sapa", "bulması zor", "bulmasi zor",
    "otopark sorunu", "otopark yok", "uzak kaldı", "uzak kaldi", "dar yol",
    "yolu bozuk", "ulaşım sıkıntısı", "ulasim sikintisi",
)

# --- Kalabalik zamanlar -------------------------------------------------------
# Zaman ifadesi + yogunluk ifadesi AYNI cumle/ifadede birlikte gectiginde
# anlamli sayilir (bkz. yer_profili_cikarici.py::kalabalik_zamanlari_belirle).

ZAMAN_GUN_TIPI_IFADELERI: dict[str, tuple[str, ...]] = {
    "hafta_ici": ("hafta içi", "hafta ici", "iş günü", "is gunu", "hafta arası", "hafta arasi"),
    "hafta_sonu": ("hafta sonu", "cumartesi", "pazar günü", "pazar gunu"),
}
ZAMAN_DILIMI_IFADELERI: dict[str, tuple[str, ...]] = {
    "sabah": ("sabah",),
    "ogle": ("öğle", "ogle"),
    "aksam": ("akşam", "aksam"),
    "gece": ("gece",),
}
YOGUNLUK_IFADELERI: dict[str, tuple[str, ...]] = {
    "kalabalik": ("kalabalık", "kalabalik", "yoğun", "yogun", "tıklım", "tiklim", "sıra var", "sira var", "izdiham"),
    "sakin": ("sakin", "tenha", "boş", "bos", "rahat rahat", "kimse yoktu", "kimse yok"),
}

# --- Ziyaretci profili --------------------------------------------------------
# Sehirden bagimsiz kalmasi icin (Samsun'a ozel bir kelime YOK) genel
# Turkce ifadeler kullanilir; yeni bir sehir eklendiginde degisiklik gerekmez.

ZIYARETCI_TIPI_IFADELERI: dict[str, tuple[str, ...]] = {
    "aile": ("ailece", "ailemle", "ailemizle", "aile ile", "aile dostu"),
    "cocuklu": ("çocuklarla", "cocuklarla", "çocukla", "cocukla", "çocuklu", "cocuklu", "çocuklarımızla", "cocuklarimizla"),
    "cift": ("eşimle", "esimle", "sevgilimle", "romantik", "çift olarak", "cift olarak", "balayı", "balayi"),
    "arkadas_grubu": ("arkadaşlarla", "arkadaslarla", "arkadaş grubu", "arkadas grubu", "arkadaş ortamı", "arkadas ortami"),
    "yalniz": ("yalnız başıma", "yalniz basima", "tek başıma", "tek basima", "solo gezi"),
    "turist": ("turist", "yabancı misafir", "yabanci misafir", "yabancı turist", "yabanci turist"),
    "yerli": ("yerli halk", "mahalleden", "buranın yerlisi", "buranin yerlisi", "yöre halkı", "yore halki"),
    "ogrenci": ("öğrenci", "ogrenci", "öğrencilere", "ogrencilere", "öğrenci dostu", "ogrenci dostu"),
    "genc": ("genç kesim", "genc kesim", "gençler", "gencler", "genç grubu", "genc grubu"),
    "yasli": ("yaşlı", "yasli", "yaşlılar", "yaslilar", "büyüklerimiz", "buyuklerimiz", "yaşlı ziyaretçi", "yasli ziyaretci"),
}
