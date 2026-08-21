"""
Yer profilinden ("YerProfili") samimi + profesyonel bir Turkce tanitim
metni ("duygu_ozeti") ureten sablon tabanli kompozisyon.

BILINCLI TASARIM KARARI: Buyuk bir uretici dil modeli (LLM) KULLANILMAZ.
Sebep: (1) Oracle Free ARM sunucuda (CPU, GPU yok) buyuk bir uretici model
CALISTIRMAK ya cok yavas olur ya da kaliteli Turkce ciktisi olan kucuk bir
model bulmak/barindirmak ek risk+bakim yuku getirir, (2) projenin butun veri
katmani BILEREK seffaf/gozle-denetlenebilir tutuluyor (bkz. konu_analizi.py) --
bir LLM'in "neden boyle yazdigi" sorusuna net cevap veremeyecegi icin bu
felsefeyle celisirdi, (3) ek maliyet/bagimlilik gerektirmez, sunucuda anlik
ve ucretsiz calisir.

"Robotik/tekduze" hissini azaltmak icin: her boyut icin BIRDEN FAZLA farkli
ifade varyanti tanimlanir; hangi varyantin secilecegi yerin kimliginden
turetilen SABIT bir rastgele tohum (seed) ile belirlenir -- boylece (a) ayni
yer HER calistirmada AYNI metni alir (kararlilik/tutarlilik), (b) farkli
yerler FARKLI ifade kaliplarina duser (tekduzelik onlenir). Ayrica dogal
baglaclar ve ikinci tekil hitapla ("...gidebilirsin", "...degerlendirebilirsin")
resmi/teknik degil, deneyimlemis biri gibi konusan bir ton hedeflenir.

Sadece yeterli GUVEN duzeyine sahip boyutlar cumleye dahil edilir
(`_MIN_GUVEN`); "bilgi_yetersiz" olan boyutlar hakkinda konusmak yerine
sessizce atlanir -- az veriyle uydurma bir izlenim verilmez.
"""

from __future__ import annotations

import hashlib
import random

from ortak.sabitler import DuyguEtiketi, FiyatAlgisi, UlasimKolayligi
from veri.ortak.bolge_profili_modeli import BolgeProfili
from veri.ortak.yer_profili_modeli import YerProfili

# Bir boyutun cumleye dahil edilebilmesi icin gereken minimum guven duzeyi
# (yer_profili_cikarici.py::BoyutTespiti.guven, 0-1 arasi).
_MIN_GUVEN = 0.3
# Genel acilis cumlesi icin, "yeterli yorum yok" yerine bir izlenim
# verebilmek icin gereken minimum yorum sayisi.
_MIN_YORUM_ACILIS_ICIN = 3

# Anlatimda kendi basina ELE ALINMAYACAK konu_analizi.py konulari -- bunlar
# zaten dedike boyutlarla (fiyat_algisi, ulasim_kolayligi, kalabalik_zamanlar)
# kapsandigi icin burada tekrar edilirse ayni sey iki kere soylenmis olurdu.
KONU_ANLATIMDA_HARIC_TUTULANLAR: frozenset[str] = frozenset({"fiyat", "konum", "kalabalik"})

_KONU_OKUNUR_ISIMLERI: dict[str, str] = {
    "manzara": "Manzara",
    "lezzet": "Lezzet",
    "servis": "Servis hızı",
    "personel": "Personel ilgisi",
    "temizlik": "Temizlik",
    "atmosfer": "Atmosfer",
    "oda_konfor": "Oda konforu",
    "kahvalti": "Kahvaltı",
    "gurultu": "Sessizlik durumu",
}

_ZIYARETCI_TIPI_OKUNUR_ISIMLERI: dict[str, str] = {
    "aile": "aileler",
    "cocuklu": "çocuklu aileler",
    "cift": "çiftler",
    "arkadas_grubu": "arkadaş grupları",
    "yalniz": "tek başına gezenler",
    "turist": "turistler",
    "yerli": "yöre halkı",
    "ogrenci": "öğrenciler",
    "genc": "genç kesim",
    "yasli": "daha olgun yaş grubu",
}

_ZAMAN_ANAHTARI_OKUNUR_ISIMLERI: dict[str, str] = {
    "genel": "Genel olarak",
    "hafta_ici_genel": "Hafta içi",
    "hafta_sonu_genel": "Hafta sonu",
    "genel_sabah": "Sabahları",
    "genel_ogle": "Öğle saatlerinde",
    "genel_aksam": "Akşamları",
    "genel_gece": "Gece saatlerinde",
    "hafta_ici_sabah": "Hafta içi sabahları",
    "hafta_ici_ogle": "Hafta içi öğle saatlerinde",
    "hafta_ici_aksam": "Hafta içi akşamları",
    "hafta_ici_gece": "Hafta içi gece saatlerinde",
    "hafta_sonu_sabah": "Hafta sonu sabahları",
    "hafta_sonu_ogle": "Hafta sonu öğle saatlerinde",
    "hafta_sonu_aksam": "Hafta sonu akşamları",
    "hafta_sonu_gece": "Hafta sonu gece saatlerinde",
}

_GENEL_ACILIS_OLUMLU: tuple[str, ...] = (
    "Ziyaretçilerin genel izlenimine göre burası gerçekten seviliyor.",
    "Yorumlara bakılırsa buraya gidenlerin çoğu memnun ayrılıyor.",
    "Buraya gidenlerin genel görüşü oldukça olumlu.",
    "Gidenlerin çoğu buradan gülümseyerek ayrılıyor gibi görünüyor.",
)
_GENEL_ACILIS_OLUMSUZ: tuple[str, ...] = (
    "Yorumlara göre burada bazı sorunlar yaşayan ziyaretçiler var, biraz temkinli yaklaşmakta fayda var.",
    "Genel izlenim biraz karışık; gitmeden önce güncel yorumlara göz atmanı öneririz.",
    "Herkes aynı deneyimi yaşamamış, beklentini buna göre ayarlayabilirsin.",
)
_GENEL_ACILIS_NOTR: tuple[str, ...] = (
    "Ziyaretçilerin görüşleri burada birbirinden oldukça farklı.",
    "Yorumlara göre burası standart, ortalama bir deneyim sunuyor.",
    "Kimi çok beğenmiş kimi orta bulmuş, karma bir görüntü var.",
)
_GENEL_ACILIS_YETERSIZ: tuple[str, ...] = (
    "Henüz yeterli sayıda yorum birikmediği için net bir izlenim vermek zor, ama elimizdeki bilgilerle seni bilgilendirelim.",
)

_FIYAT_CUMLELERI: dict[str, tuple[str, ...]] = {
    FiyatAlgisi.UCUZ.value: (
        "Fiyatlar gayet cebi dostu, bütçeni fazla zorlamaz.",
        "Fiyat konusunda oldukça uygun bir yer.",
        "Cebini fazla yakmadan keyifli vakit geçirebileceğin bir yer.",
    ),
    FiyatAlgisi.ORTA.value: (
        "Fiyatlar cebi fazla yakmıyor ama en ucuz seçenek de değil, orta karar bir yer.",
        "Fiyat konusunda ne çok ucuz ne çok pahalı, dengeli bir seviyede.",
    ),
    FiyatAlgisi.PAHALI.value: (
        "Fiyatlar biraz yüksek, bütçe planlarken bunu hesaba katmakta fayda var.",
        "Cebini biraz zorlayabilir, ona göre bütçe ayırmanı öneririz.",
        "Fiyat açısından lüks tarafta, özel bir gün için düşünebilirsin.",
    ),
}

_ULASIM_CUMLELERI: dict[str, tuple[str, ...]] = {
    UlasimKolayligi.KOLAY.value: (
        "Ulaşım açısından oldukça pratik, kolayca gidebilirsin.",
        "Konumu merkezi olduğu için ulaşmak zor olmuyor.",
        "Yol konusunda dertlenmene gerek yok, ulaşımı gayet rahat.",
    ),
    UlasimKolayligi.ORTA.value: (
        "Ulaşım konusunda ne çok kolay ne çok zor, standart bir konumda.",
    ),
    UlasimKolayligi.ZOR.value: (
        "Ulaşım biraz meşakkatli olabiliyor, yol planını önceden yapmakta fayda var.",
        "Biraz sapa bir konumda, ulaşımı önceden planlamanı öneririz.",
        "Kendi aracınla gitmen ulaşımı kolaylaştırabilir, toplu taşıma biraz zorlayabiliyor.",
    ),
}

_KALABALIK_CUMLE_SABLONLARI: tuple[str, ...] = (
    "{zaman} epey hareketli oluyor, sakin bir deneyim istiyorsan başka bir zamanı değerlendirebilirsin.",
    "{zaman} oldukça kalabalıklaşıyor.",
    "{zaman} bayağı yoğun geçiyor, buna göre planlayabilirsin.",
)
_SAKIN_CUMLE_SABLONLARI: tuple[str, ...] = (
    "{zaman} oldukça sakin ve huzurlu geçiyor.",
    "{zaman} tenha olduğu için rahatça vakit geçirebilirsin.",
    "{zaman} gitmek isteyenler için gayet rahat bir ortam var.",
)

_ZIYARETCI_CUMLE_SABLONLARI: tuple[str, ...] = (
    "Burayı en çok {tipler} tercih ediyor.",
    "Ziyaretçi profiline bakılırsa {tipler} için gayet uygun bir yer.",
    "Buraya gelenler arasında {tipler} öne çıkıyor.",
)

_KONU_CUMLE_SABLONLARI_OLUMLU: tuple[str, ...] = (
    "{konu} konusunda özellikle beğeniliyor.",
    "{konu} açısından öne çıkan bir yer.",
    "{konu} konusunda ziyaretçileri gayet memnun ediyor.",
)
_KONU_CUMLE_SABLONLARI_OLUMSUZ: tuple[str, ...] = (
    "{konu} konusunda bazı şikayetler var.",
    "{konu} açısından herkesi memnun etmeyebilir.",
    "{konu} konusunda biraz dikkatli olmakta fayda var.",
)


def _tohum_uret(yer_kimligi: str) -> int:
    """random.seed icin PROCESS'ten BAGIMSIZ, deterministik bir sayi uretir
    (Python'un yerlesik hash() fonksiyonu string'ler icin surec basina
    rastgeledir -- ayni yer farkli calistirmalarda farkli metin alirdi)."""
    return int(hashlib.md5(yer_kimligi.encode("utf-8")).hexdigest()[:8], 16)


def _genel_acilis_cumlesi(rastgele: random.Random, kullanilan_yorum_sayisi: int, genel_duygu_ortalamasi: float | None) -> str:
    if kullanilan_yorum_sayisi < _MIN_YORUM_ACILIS_ICIN or genel_duygu_ortalamasi is None:
        return rastgele.choice(_GENEL_ACILIS_YETERSIZ)
    if genel_duygu_ortalamasi >= 0.3:
        return rastgele.choice(_GENEL_ACILIS_OLUMLU)
    if genel_duygu_ortalamasi <= -0.3:
        return rastgele.choice(_GENEL_ACILIS_OLUMSUZ)
    return rastgele.choice(_GENEL_ACILIS_NOTR)


def yer_tanitim_metni_uret(
    yer_profili: YerProfili,
    genel_duygu_ortalamasi: float | None = None,
    on_plana_cikan_konular: list[tuple[str, DuyguEtiketi]] | None = None,
) -> str:
    """YerProfili + (varsa) en cok bahsedilen konu/duygu ciftlerinden samimi
    bir Turkce tanitim paragrafi ("duygu_ozeti") uretir. `on_plana_cikan_konular`,
    konu_analizi.py'nin cikardigi konu_duygulari'ndan pipeline_calistir.py'ye
    benzer sekilde agregre edilip verilir (bkz. profil_pipeline_calistir.py)."""
    rastgele = random.Random(_tohum_uret(yer_profili.yer_kimligi))
    cumleler: list[str] = [
        _genel_acilis_cumlesi(rastgele, yer_profili.kullanilan_yorum_sayisi, genel_duygu_ortalamasi)
    ]

    fiyat = yer_profili.fiyat_algisi
    if fiyat.deger != FiyatAlgisi.BILGI_YETERSIZ.value and fiyat.guven >= _MIN_GUVEN:
        cumleler.append(rastgele.choice(_FIYAT_CUMLELERI[fiyat.deger]))

    ulasim = yer_profili.ulasim_kolayligi
    if ulasim.deger != UlasimKolayligi.BILGI_YETERSIZ.value and ulasim.guven >= _MIN_GUVEN:
        cumleler.append(rastgele.choice(_ULASIM_CUMLELERI[ulasim.deger]))

    # Metnin sismemesi icin kalabalik zamanlardan en fazla 2 tanesi anlatilir;
    # "genel" disinda daha spesifik bir zaman bilgisi varsa o tercih edilir.
    spesifik_zamanlar = {k: v for k, v in yer_profili.kalabalik_zamanlar.items() if k != "genel"}
    secilecek_zamanlar = spesifik_zamanlar or yer_profili.kalabalik_zamanlar
    for zaman_anahtari, yogunluk in list(secilecek_zamanlar.items())[:2]:
        zaman_okunur = _ZAMAN_ANAHTARI_OKUNUR_ISIMLERI.get(zaman_anahtari, "Bazı zamanlarda")
        sablonlar = _KALABALIK_CUMLE_SABLONLARI if yogunluk == "kalabalik" else _SAKIN_CUMLE_SABLONLARI
        cumleler.append(rastgele.choice(sablonlar).format(zaman=zaman_okunur))

    if yer_profili.ziyaretci_profili:
        en_yaygin_ikisi = sorted(yer_profili.ziyaretci_profili.items(), key=lambda kv: -kv[1])[:2]
        tipler_okunur = " ve ".join(_ZIYARETCI_TIPI_OKUNUR_ISIMLERI.get(tip, tip) for tip, _oran in en_yaygin_ikisi)
        cumleler.append(rastgele.choice(_ZIYARETCI_CUMLE_SABLONLARI).format(tipler=tipler_okunur))

    if on_plana_cikan_konular:
        anlatilacak_konular = [
            (konu, duygu) for konu, duygu in on_plana_cikan_konular if konu not in KONU_ANLATIMDA_HARIC_TUTULANLAR
        ][:5]
        for konu, duygu in anlatilacak_konular:
            konu_okunur = _KONU_OKUNUR_ISIMLERI.get(konu, konu.capitalize())
            if duygu == DuyguEtiketi.OLUMLU:
                cumleler.append(rastgele.choice(_KONU_CUMLE_SABLONLARI_OLUMLU).format(konu=konu_okunur))
            elif duygu == DuyguEtiketi.OLUMSUZ:
                cumleler.append(rastgele.choice(_KONU_CUMLE_SABLONLARI_OLUMSUZ).format(konu=konu_okunur))

    if yer_profili.kullanilan_yorum_sayisi >= _MIN_YORUM_ACILIS_ICIN:
        cumleler.append(
            rastgele.choice(
                (
                    f"Bu özet {yer_profili.kullanilan_yorum_sayisi} ziyaretçi yorumundan süzülerek hazırlandı.",
                    f"Toplam {yer_profili.kullanilan_yorum_sayisi} yoruma dayanarak burası hakkında fikir edinebilirsin.",
                )
            )
        )

    return " ".join(cumleler)


def yapisal_deneyim_metni_uret(
    yer_ismi: str,
    ana_kategori: str,
    alt_kategori: str,
    tanitim_metni: str | None = None,
    yer_kimligi: str = "yapisal",
) -> str:
    """Yorumu olmayan veya cok az olan yerler icin kullanici deneyimleri
    blogunda gosterilecek yapisal (kategori + tanitim) fallback metin."""
    rastgele = random.Random(_tohum_uret(yer_kimligi or yer_ismi))
    tur = _KONU_OKUNUR_ISIMLERI.get(alt_kategori)  # olmayabilir
    acilis = rastgele.choice(
        (
            f"Henüz yeterli ziyaretçi yorumu birikmediği için {yer_ismi} hakkında net bir kullanıcı deneyimi özeti çıkarmak zor.",
            f"{yer_ismi} için yorum sayısı henüz sınırlı; yine de yerin türüne göre bir ön izlenim paylaşabiliriz.",
        )
    )
    parcalar = [acilis]
    if tanitim_metni:
        kisa = tanitim_metni if len(tanitim_metni) < 280 else tanitim_metni[:277].rsplit(" ", 1)[0] + "…"
        parcalar.append(f"Tanıtımına göre: {kisa}")
    else:
        parcalar.append(
            rastgele.choice(
                (
                    f"Bu bir {alt_kategori.replace('_', ' ')} kategorisindeki yer; gitmeden önce güncel saat ve koşulları kontrol etmek iyi olur.",
                    f"Yapısı itibarıyla {ana_kategori.replace('_', ' ')} grubunda değerlendiriliyor; beklentini buna göre ayarlayabilirsin.",
                )
            )
        )
    if tur:
        parcalar.append(f"{tur} boyutu ziyaretçiler için sıkça öne çıkar.")
    return " ".join(parcalar)


# ---------------------------------------------------------------------------
# Bolge Profili (sehir/ilce tanitim) icin anlatim -- yukaridaki yer_tanitim_
# metni_uret ile AYNI felsefe (sablon+seed tabanli, LLM yok) ama "buraya
# gidenler..." degil "bu sehri/ilceyi anlatanlar..." tonuna uyarlanmistir,
# cunku girdi TEK bir isletmenin degil BUTUN bir bolgenin yorumlarindan gelir.
# ---------------------------------------------------------------------------

_BOLGE_KONU_OKUNUR_ISIMLERI: dict[str, str] = {
    **_KONU_OKUNUR_ISIMLERI,
    "guvenlik": "Güvenlik",
    "trafik": "Trafik durumu",
    "doga": "Doğal güzellikler",
    "tarihi_doku": "Tarihi doku",
    "gece_hayati": "Gece hayatı",
    "yasam_maliyeti": "Yaşam maliyeti",
}

_BOLGE_GENEL_ACILIS_OLUMLU: tuple[str, ...] = (
    "Burayı anlatanların genel izlenimi oldukça olumlu.",
    "Buradan bahsedenlerin çoğu bölgeyi sevdiğini belirtiyor.",
    "Genel olarak burası hakkında konuşanların görüşü gayet iyi.",
)
_BOLGE_GENEL_ACILIS_OLUMSUZ: tuple[str, ...] = (
    "Burayı anlatanlar arasında bazı şikayetler öne çıkıyor, temkinli bir beklentiyle yaklaşabilirsin.",
    "Genel izlenim biraz karışık, bölge hakkında olumsuz görüşler de var.",
)
_BOLGE_GENEL_ACILIS_NOTR: tuple[str, ...] = (
    "Bölge hakkında konuşanların görüşleri birbirinden oldukça farklı.",
    "Kimi bölgeyi çok sevmiş kimi ortalama bulmuş, karma bir tablo var.",
)
_BOLGE_GENEL_ACILIS_YETERSIZ: tuple[str, ...] = (
    "Bu bölge hakkında henüz yeterli sayıda yorum birikmedi, ama elimizdeki bilgilerle seni bilgilendirelim.",
)

_BOLGE_KONU_CUMLE_SABLONLARI_OLUMLU: tuple[str, ...] = (
    "{konu} konusunda burayı anlatanlar oldukça memnun.",
    "{konu} açısından bölgenin öne çıkan bir yönü.",
    "{konu} konusunda genel olarak iyi bir izlenim var.",
)
_BOLGE_KONU_CUMLE_SABLONLARI_OLUMSUZ: tuple[str, ...] = (
    "{konu} konusunda bazı şikayetler dile getirilmiş.",
    "{konu} açısından herkesi memnun etmeyen bir bölge.",
    "{konu} konusunda biraz dikkatli olmakta fayda var.",
)


def bolge_tanitim_metni_uret(bolge_profili: BolgeProfili) -> str:
    """BolgeProfili'nden (sehir merkezi veya ilce), o bolgeyi anlatanlarin
    genel goruslerini ozetleyen samimi bir Turkce tanitim paragrafi uretir.
    Ayni tohum (seed) mantigi kullanilir (`bolge_kimligi`) -- ayni bolge her
    calistirmada ayni metni alir."""
    rastgele = random.Random(_tohum_uret(bolge_profili.bolge_kimligi))

    if bolge_profili.kullanilan_yorum_sayisi < _MIN_YORUM_ACILIS_ICIN or bolge_profili.genel_duygu_skoru is None:
        acilis = rastgele.choice(_BOLGE_GENEL_ACILIS_YETERSIZ)
    elif bolge_profili.genel_duygu_etiketi == DuyguEtiketi.OLUMLU:
        acilis = rastgele.choice(_BOLGE_GENEL_ACILIS_OLUMLU)
    elif bolge_profili.genel_duygu_etiketi == DuyguEtiketi.OLUMSUZ:
        acilis = rastgele.choice(_BOLGE_GENEL_ACILIS_OLUMSUZ)
    else:
        acilis = rastgele.choice(_BOLGE_GENEL_ACILIS_NOTR)

    cumleler: list[str] = [acilis]

    anlatilacak_konular = bolge_profili.on_plana_cikan_konular[:5]
    for konu_ozeti in anlatilacak_konular:
        konu_okunur = _BOLGE_KONU_OKUNUR_ISIMLERI.get(konu_ozeti.konu, konu_ozeti.konu.capitalize())
        if konu_ozeti.duygu_etiketi == DuyguEtiketi.OLUMLU:
            cumleler.append(rastgele.choice(_BOLGE_KONU_CUMLE_SABLONLARI_OLUMLU).format(konu=konu_okunur))
        elif konu_ozeti.duygu_etiketi == DuyguEtiketi.OLUMSUZ:
            cumleler.append(rastgele.choice(_BOLGE_KONU_CUMLE_SABLONLARI_OLUMSUZ).format(konu=konu_okunur))

    if bolge_profili.kullanilan_yorum_sayisi >= _MIN_YORUM_ACILIS_ICIN:
        cumleler.append(
            f"Bu özet {bolge_profili.kullanilan_yorum_sayisi} bölge yorumundan derlendi."
        )

    return " ".join(cumleler)
