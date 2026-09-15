"""
Sehir bazli ayarlar -- projenin sehir-bagimsiz calismasini saglayan merkezi kayit.

Yeni bir sehir eklemek istedigimizde (orn. Karadeniz genislemesinde Ordu,
Trabzon vb.) tek yapilmasi gereken sey buraya yeni bir SehirAyari eklemektir;
toplayicilarin (osm, google_maps, eksi_sozluk, tripadvisor), eslemenin ve
kalite kontrolun hicbirinin kodu degismez.
"""

from __future__ import annotations

from pydantic import BaseModel, Field

from veri.ortak.metin_araclari import turkce_kucuk_harf


def bolge_slug(bolge_adi: str) -> str:
    """Bir bolge adini (sehir merkezi anahtari veya bir ilce adi, orn.
    '19 Mayıs') `kaynak_yer_id` ve dosya-ici anahtarlarda kullanilan sade,
    bosluksuz bir forma cevirir. Turkce karakterleri KORUR (bu bir dosya adi
    DEGIL, string alan degeri) -- sadece bosluk/tirnak gibi ayirici
    karakterleri temizler. eksi_sozluk_toplayici.py ve bolge_profili_
    cikarici.py arasinda TUTARLI bir anahtar uretmek icin tek dogruluk
    kaynagi burasidir. `turkce_kucuk_harf` kullanilir, bkz. o modulun
    dokstring'i ('İlkadım' gibi isimlerde normal `.lower()` konsol
    cakmasina yol acabilen bir birlesik karakter uretir)."""
    return turkce_kucuk_harf(bolge_adi.strip()).replace(" ", "_").replace("'", "")


class SehirAyari(BaseModel):
    anahtar: str = Field(..., description="Dosya adlarinda ve CLI'da kullanilan kisa anahtar, orn. 'samsun'")
    isim: str = Field(..., description="Goruntulenen tam isim, orn. 'Samsun'")
    plaka_kodu: str
    bolge: str = Field(..., description="Bolgesel gruplama, orn. 'Karadeniz'")

    # OpenStreetMap Overpass API sorgusunda il sinirini bulmak icin kullanilir.
    # Turkiye illeri OSM'de admin_level=4 iliski (relation) olarak bu kodla etiketlidir.
    osm_iso_kodu: str = Field(..., description="Orn. 'TR-55' (Samsun)")

    # Google Maps arama kutusuna yazilacak temel sorgu (toplayicinin sonuna
    # "<kategori> Samsun" gibi ekler yapmasi icin taban metin).
    google_maps_arama_bolgesi: str

    # TripAdvisor'da bu sehrin URL yolu (bulunduktan sonra doldurulur).
    tripadvisor_sehir_yolu: str | None = None

    # Eksi Sozluk'ta taranacak baslik(lar) -- sehir hakkinda genel ve
    # gezilecek yer temali basliklar. Buraya eklenen her baslik gercekten
    # var olmali (eksisozluk.com uzerinde arayarak dogrula); olmayan bir
    # baslik toplayici tarafindan 404 ile atlanir, hata vermez.
    eksi_sozluk_basliklari: list[str] = Field(default_factory=list)

    # Bu ilin ilceleri (resmi isimleriyle). Iki amacla kullanilir:
    #   1) google_maps_toplayici.py --ilce-bazli-arama ile sehir merkezi
    #      disindaki cografi kapsamayi artirmak icin,
    #   2) Eksi Sozluk'ta sehir GENELI degil ILCE ozelinde de yorum toplayip
    #      "Bolge Profili" (bkz. veri/duygu_analizi/bolge_profili_cikarici.py)
    #      uretmek icin.
    # Yeni bir sehir eklerken burasi doldurulmazsa ilce-bazli ozellikler
    # sessizce atlanir (bos liste), hata vermez.
    ilceler: list[str] = Field(default_factory=list)

    # Ekşi Sözlük'te bir bölgenin (şehir merkezi = sehir.anahtar veya bir
    # ilçe adı) hangi başlık(lar) altında arandığını belirtir -- bazı
    # ilçelerin Ekşi'deki başlık adı, resmi isimden farklı/eksik yazılabilir
    # (örn. Türkçe karakter varyasyonları). Burada override edilmeyen her
    # bölge için varsayılan olarak KENDI ADI tek başlık kabul edilir (bkz.
    # `bolge_basliklarini_getir`).
    eksi_sozluk_bolge_basliklari: dict[str, list[str]] = Field(default_factory=dict)

    # Ilce / bolge adi -> [enlem, boylam]. Senaryo 1'de konaklama bolgesi
    # secildiginde rota motoruna merkez koordinat saglamak icin kullanilir.
    # Eksik bir ilce icin haversine ile en yakin bilinen merkez dusulur.
    ilce_merkezleri: dict[str, list[float]] = Field(default_factory=dict)

    def tum_bolge_adlari(self) -> list[str]:
        """Sehir merkezi (kendi anahtari) + tum ilceleri, "bolge" kavraminin
        kapsadigi tam liste olarak dondurur (bkz. Bolge Profili)."""
        return [self.anahtar, *self.ilceler]

    def bolge_adini_slugtan_bul(self, slug: str) -> str:
        """`bolge_slug()` ile uretilmis bir slug'i tekrar okunur bolge adina
        (orn. 'ilkadim' -> 'İlkadım') cevirir -- bolge_profili_cikarici.py
        Eksi Sozluk'ten gelen 'bolge:<sehir>:<slug>' kaynak_yer_id'sini
        insan tarafindan okunabilir bir isme cevirmek icin kullanir. Eslesme
        bulunamazsa (beklenmez ama olasi), slug'in kendisi dondurulur."""
        for bolge_adi in self.tum_bolge_adlari():
            if bolge_slug(bolge_adi) == slug:
                return bolge_adi
        return slug

    def cografi_bbox(self, tampon_derece: float = 0.4) -> tuple[float, float, float, float] | None:
        """Ilce merkezlerinden türetilen (min_enlem, max_enlem, min_boylam, max_boylam)."""
        noktalar = [koordinat for koordinat in self.ilce_merkezleri.values() if len(koordinat) >= 2]
        if not noktalar:
            return None
        enlemler = [float(nokta[0]) for nokta in noktalar]
        boylamlar = [float(nokta[1]) for nokta in noktalar]
        return (
            min(enlemler) - tampon_derece,
            max(enlemler) + tampon_derece,
            min(boylamlar) - tampon_derece,
            max(boylamlar) + tampon_derece,
        )

    def bolge_basliklarini_getir(self, bolge_adi: str) -> list[str]:
        """Bir bolge (sehir merkezi veya bir ilce) icin Eksi Sozluk'te
        aranacak baslik(lar)i dondurur. `eksi_sozluk_bolge_basliklari` icinde
        ozel bir eslesme tanimliysa o kullanilir; tanimli degilse bolgenin
        KENDI ADI varsayilan (tek) baslik olarak kabul edilir -- boylece
        yeni bir ilce eklemek icin cogu zaman hicbir ekstra tanim gerekmez."""
        if bolge_adi == self.anahtar and self.eksi_sozluk_basliklari:
            return list(self.eksi_sozluk_basliklari)
        return list(self.eksi_sozluk_bolge_basliklari.get(bolge_adi, [bolge_adi]))


SEHIRLER: dict[str, SehirAyari] = {
    "samsun": SehirAyari(
        anahtar="samsun",
        isim="Samsun",
        plaka_kodu="55",
        bolge="Karadeniz",
        osm_iso_kodu="TR-55",
        google_maps_arama_bolgesi="Samsun, Turkiye",
        # TripAdvisor'in ic "location id"si + URL slug'i (tripadvisor.com'da
        # "Samsun" aratilarak dogrulandi).
        tripadvisor_sehir_yolu="g298035-Samsun_Turkish_Black_Sea_Coast",
        # NOT: "samsun" basligi eksisozluk.com uzerinde dogrulanmistir (var).
        # Daha fazla ilgili baslik (orn. belirli ilceler/plajlar hakkinda)
        # zamanla eksisozluk.com'da arama yapilarak buraya eklenebilir.
        eksi_sozluk_basliklari=["samsun"],
        # Samsun'un 17 ilcesi (resmi isimleriyle) -- ilce-bazli Google Maps
        # aramasi ve Bolge Profili (Eksi Sozluk) icin kullanilir.
        ilceler=[
            "Atakum", "İlkadım", "Canik", "Tekkeköy", "Bafra", "Çarşamba",
            "Terme", "Salıpazarı", "Ayvacık", "Vezirköprü", "Havza", "Kavak",
            "Ladik", "Alaçam", "Yakakent", "19 Mayıs", "Asarcık",
        ],
        # "19 Mayıs" ilcesinin dogal slug'i ("19-mayıs") eksisozluk.com'da
        # 404 doner -- bu isim orada tamamen ayri bir baslik olan ulusal
        # bayrama (19 Mayıs Atatürk'ü Anma Genclik ve Spor Bayramı) ayrilmis.
        # Ilcenin kendisi "ondokuzmayis" basligi altinda konusuluyor (2026-08-03
        # dogrulandi: icerik "samsun'un ilcesi", "engiz", "ballica" gibi
        # ilceye ozgu ifadeler iceriyor) -- bu yuzden override edilir.
        eksi_sozluk_bolge_basliklari={"19 Mayıs": ["ondokuzmayis"]},
        ilce_merkezleri={
            "samsun": [41.2867, 36.3300],
            "Atakum": [41.3400, 36.2800],
            "İlkadım": [41.2860, 36.3300],
            "Canik": [41.2600, 36.3400],
            "Tekkeköy": [41.2100, 36.4600],
            "Bafra": [41.5680, 35.9070],
            "Çarşamba": [41.1990, 36.7220],
            "Terme": [41.2090, 36.9720],
            "Salıpazarı": [41.0830, 36.8330],
            "Ayvacık": [40.9910, 36.6310],
            "Vezirköprü": [41.1430, 35.4550],
            "Havza": [40.9710, 35.6620],
            "Kavak": [41.0780, 36.0400],
            "Ladik": [40.9110, 35.8920],
            "Alaçam": [41.6100, 35.5950],
            "Yakakent": [41.6330, 35.4550],
            "19 Mayıs": [41.5120, 36.0850],
            "Asarcık": [41.0330, 36.2350],
        },
    ),
}


def bolge_merkezini_bul(sehir_anahtari: str, bolge_adi: str) -> tuple[float, float] | None:
    """Ilce/bolge adindan (enlem, boylam) dondurur. Buyuk/kucuk harf ve
    slug farklarina toleranslidir; bulunamazsa None."""
    try:
        ayar = sehir_getir(sehir_anahtari)
    except KeyError:
        return None
    if not ayar.ilce_merkezleri:
        return None
    hedef = turkce_kucuk_harf(bolge_adi.strip())
    for adi, koordinat in ayar.ilce_merkezleri.items():
        if turkce_kucuk_harf(adi) == hedef or bolge_slug(adi) == bolge_slug(bolge_adi):
            if len(koordinat) >= 2:
                return float(koordinat[0]), float(koordinat[1])
    return None


def sehir_getir(anahtar: str) -> SehirAyari:
    anahtar = anahtar.lower().strip()
    if anahtar not in SEHIRLER:
        gecerli = ", ".join(sorted(SEHIRLER))
        raise KeyError(f"'{anahtar}' tanimli bir sehir degil. Gecerli anahtarlar: {gecerli}")
    return SEHIRLER[anahtar]


def sehir_anahtarini_isme_gore_bul(isim: str) -> str | None:
    """`sunucu/veritabani/modeller.py::Sehir.isim` (veritabanindaki tam isim,
    orn. 'Samsun') alanindan CLI/URL'lerde kullanilan kisa anahtara (orn.
    'samsun') geri donus icin kullanilir -- sunucu/api yerler_router.py'de
    API cevaplarina anahtar eklerken kullanilir."""
    for anahtar, ayar in SEHIRLER.items():
        if ayar.isim == isim:
            return anahtar
    return None
