"""
Anahtar kelime tabanli konu (aspect) etiketleme.

Amac: "Manzarasi harikaydi ama fiyatlar biraz yuksekti" gibi bir yorumdan
TEK bir genel duygu skoru cikarmak yerine, konuya ozel duygu cikarmak:
  [{"konu": "manzara", "duygu_etiketi": "olumlu", "gecen_ifade": "manzarasi harikaydi"},
   {"konu": "fiyat", "duygu_etiketi": "olumsuz", "gecen_ifade": "fiyatlar biraz yuksekti"}]

BILINCLI TASARIM KARARI: Bu modul BERT gibi bir "kara kutu" model KULLANMAZ.
Tamamen anahtar kelime + kucuk bir Turkce duygu sozlugu (lexicon) + olumsuzluk
(negation) tespitiyle calisir. Sebep: dokumanlar/plan'da defalarca vurgulandigi
gibi projenin butun veri katmaninin ANLASILIR ve GOZLE DENETLENEBILIR olmasi
isteniyor -- bir konunun neden "olumsuz" etiketlendigini (`gecen_ifade` alani
sayesinde) HER ZAMAN kelimesi kelimesine geriye izleyebilirsin. Bu, buyuk bir
transformer modelinin "neden bu sonucu verdi" sorusuna cevap veremeyen
yapisindan bilinckli bir sapma.

Sinirlamalar (bilerek kabul edilmistir): kucuk sozluk bazi ifadeleri
kacirabilir (orn. deyimler, ironi). Zamanla KONU_ANAHTAR_KELIMELERI ve
POZITIF_KELIMELER/NEGATIF_KELIMELER genisletilerek iyilestirilebilir --
bunlar sadece birer Turkce metin listesi oldugu icin genisletmek
kod degistirmek anlamina gelmez, sadece bu dosyadaki listelere kelime eklemek
yeterlidir.
"""

from __future__ import annotations

import re

from ortak.sabitler import DuyguEtiketi
from veri.ortak.metin_araclari import turkce_kucuk_harf
from veri.ortak.yorum_modeli import KonuDuygusu

# Konu adi (Turkce, ASCII-karaktersiz -- proje genelindeki isimlendirme
# kuralina uyar) -> o konudan bahsedildigini gosteren anahtar kelimeler.
# Bir yorum, restoran/kafe/otel/gezilecek-yer FARKETMEKSIZIN taranir; ilgisiz
# konular zaten metinde hic gecmeyecegi icin zarar vermez.
KONU_ANAHTAR_KELIMELERI: dict[str, list[str]] = {
    "manzara": ["manzara", "manzarası", "manzarasi", "manzaralı", "view", "gorunum", "görünüm"],
    "fiyat": ["fiyat", "fiyatı", "fiyati", "pahalı", "pahali", "ucuz", "hesaplı", "hesapli", "para", "masraf"],
    "lezzet": ["lezzet", "lezzetli", "tat", "tadı", "tadi", "yemek", "yemekler", "porsiyon"],
    "servis": ["servis", "servis hızı", "servis hizi", "hız", "hiz", "bekleme", "sipariş", "siparis"],
    "personel": ["personel", "garson", "çalışan", "calisan", "ilgi", "ilgili", "kaba", "güler yüz", "guler yuz"],
    "temizlik": ["temiz", "temizlik", "hijyen", "kirli", "pis"],
    "atmosfer": ["atmosfer", "ambiyans", "ortam", "dekor", "iç mekan", "ic mekan", "müzik", "muzik"],
    "konum": ["konum", "ulaşım", "ulasim", "merkez", "uzak", "yakın", "yakin", "otopark", "park yeri"],
    "kalabalik": ["kalabalık", "kalabalik", "sıra", "sira", "yoğun", "yogun", "tıklım", "tiklim"],
    "oda_konfor": ["oda", "yatak", "banyo", "konfor", "rahat"],
    "kahvalti": ["kahvaltı", "kahvalti"],
    "gurultu": ["gürültü", "gurultu", "sessiz", "sakin"],
    # --- Bolge Profili (sehir/ilce tanitimi) icin eklenen konu basliklari.
    # Bir yer yorumunda da gecebilirler (orn. "guvenlik" bir otel yorumunda
    # da anlamli olabilir) ama asıl amaci sehir/ilce genel duygu profilidir
    # (bkz. veri/duygu_analizi/bolge_profili_cikarici.py). ---
    "guvenlik": ["güvenli", "guvenli", "güvensiz", "guvensiz", "hırsız", "hirsiz", "kapkaç", "kapkac", "asayiş", "asayis", "tehlike"],
    "trafik": ["trafik", "sıkışıklık", "sikisiklik", "otopark sorunu", "park sorunu", "yol calismasi", "yol çalışması"],
    "doga": ["doğa", "doga", "yeşil", "yesil", "orman", "deniz", "hava kalitesi", "temiz hava"],
    "tarihi_doku": ["tarihi doku", "tarihi", "kültürel", "kulturel", "eski şehir", "eski sehir", "mimari"],
    "gece_hayati": ["gece hayatı", "gece hayati", "eğlence hayatı", "eglence hayati", "bar", "kulüp", "kulup"],
    "yasam_maliyeti": ["yaşam maliyeti", "yasam maliyeti", "geçim", "gecim", "kira", "hayat pahalılığı", "hayat pahaliligi"],
}

# Kucuk, elle kuratorlugu yapilmis Turkce duygu sozlugu -- KOK (govde)
# halinde tutulur, TAM KELIME degil. Sebep: Turkce eklemeli bir dildir,
# ayni kok onlarca farkli ek alabilir (harika -> harikaydi, harikaymis,
# harikasiniz...). Tam kelime esitligi bu yuzden coğu gercek yorumu
# KACIRIRDI. Bunun yerine "kelime BU KOKLE BASLIYOR MU" (prefix/startswith)
# kontrolu yapilir (bkz. _kok_ile_baslar_mi) -- tam bir lemmatizer/kok
# bulucu kadar dogru degildir ama ekstra bagimliliksiz, hizli ve seffaf
# calisir; kapsamini genisletmek icin sadece bu listelere kok eklemek yeterli.
POZITIF_KOKLER: tuple[str, ...] = (
    "harika", "muhteşem", "muhtesem", "mükemmel", "mukemmel", "güzel", "guzel", "iyi", "keyifli",
    "lezzetli", "lezzet", "temiz", "hızlı", "hizli", "ilgili", "güler", "guler", "tavsiye", "beğen", "beyen",
    "sevdim", "sevdik", "rahat", "ferah", "şahane", "sahane", "nefis", "başarılı", "basarili", "kaliteli",
    "hesaplı", "hesapli", "samimi", "sıcak", "sicak", "keyif", "memnun", "bayıl", "bayil", "efsane",
    "süper", "super", "huzurlu", "manzaralı", "manzarali", "ucuz", "profesyonel", "temiz",
)
NEGATIF_KOKLER: tuple[str, ...] = (
    "kötü", "kotu", "berbat", "rezalet", "pahalı", "pahali", "yüksek", "yuksek", "kirli", "pis",
    "yavaş", "yavas", "kaba", "ilgisiz", "hayalkırıklığı", "vasat", "soğuk", "soguk", "kalabalık",
    "kalabalik", "gürültülü", "gurultulu", "bozuk", "bayat", "tatsız", "tatsiz", "sıkıntı", "sikinti",
    "üşüt", "usut", "hijyensiz", "kabus", "iğrenç", "igrenc", "rahatsız", "rahatsiz", "gecikme", "eksik",
    "başarısız", "basarisiz", "kirlen",
)

# Bu koklerle baslayan bir kelime, komsu bir duygu kelimesinin kutbunu TERS
# CEVIRIR. NOT: Turkce'de olumsuzluk eki cogunlukla kelimeDEN SONRA gelir
# (Ingilizce'nin aksine): "temiz DEGILDI" (temiz + degil + di), bu yuzden
# _pencerede_olumsuzluk_var_mi hem ONCEKI hem SONRAKI kelimelere bakar.
OLUMSUZLUK_KOKLERI: tuple[str, ...] = ("değil", "degil", "yok", "hiç", "hic", "asla", "olmadı", "olmadi")


def _kok_ile_baslar_mi(kelime: str, kokler: tuple[str, ...]) -> bool:
    return any(kelime.startswith(kok) for kok in kokler)

# Cumleyi/ifadeyi konu bazinda ayirmak icin bolme noktalari: noktalama
# isaretleri VE zit anlam bagli baglaçlar ("ama", "fakat" vb.) -- bir yorumda
# "Manzarası güzeldi ama fiyatlar yüksekti" gibi TEK cumlede IKI FARKLI
# duygu tasiyan iki konu olabilir, bu yuzden sadece noktalama yetmez.
_BOLME_DESENI = re.compile(r"[.!?;\n]|(?:\bama\b|\bfakat\b|\bancak\b|\blakin\b)", flags=re.IGNORECASE)


def ifadelere_ayir(metin: str) -> list[str]:
    """Bir yorum metnini, konu-duygu eslestirmesi icin daha kucuk anlamli
    parcalara (ifadelere) boler."""
    parcalar = _BOLME_DESENI.split(metin)
    return [p.strip() for p in parcalar if p and p.strip()]


def _kelimelere_ayir(ifade: str) -> list[str]:
    return re.findall(r"[a-zA-ZçÇğĞıİöÖşŞüÜ]+", turkce_kucuk_harf(ifade))


def ifade_duygusunu_belirle(ifade: str) -> DuyguEtiketi:
    """Bir ifadedeki (cumle/yarim cumle) pozitif/negatif kok sayimina ve
    olumsuzluk (negation) tespitine dayanarak o ifadenin duygusunu belirler.

    Basit ama SEFFAF bir yontem: bir duygu kelimesinin HEMEN ONCESINDE VEYA
    SONRASINDA (2'ser kelimelik pencerede) bir olumsuzluk koku varsa, o
    kelimenin kutbu ters cevrilir. Turkce'de olumsuzluk ekinin/kelimesinin
    kelimeDEN SONRA gelmesi COK YAYGIN oldugu icin ('temiz degildi', 'iyi
    degil') sadece ONCEKI kelimelere bakmak yeterli olmazdi.
    """
    kelimeler = _kelimelere_ayir(ifade)
    pozitif_sayisi = 0
    negatif_sayisi = 0

    for i, kelime in enumerate(kelimeler):
        komsu_pencere = kelimeler[max(0, i - 2) : i] + kelimeler[i + 1 : i + 3]
        olumsuzlanmis = any(_kok_ile_baslar_mi(k, OLUMSUZLUK_KOKLERI) for k in komsu_pencere)

        if _kok_ile_baslar_mi(kelime, POZITIF_KOKLER):
            if olumsuzlanmis:
                negatif_sayisi += 1
            else:
                pozitif_sayisi += 1
        elif _kok_ile_baslar_mi(kelime, NEGATIF_KOKLER):
            if olumsuzlanmis:
                pozitif_sayisi += 1
            else:
                negatif_sayisi += 1

    if pozitif_sayisi > negatif_sayisi:
        return DuyguEtiketi.OLUMLU
    if negatif_sayisi > pozitif_sayisi:
        return DuyguEtiketi.OLUMSUZ
    return DuyguEtiketi.NOTR


def konulari_tespit_et(metin: str, genel_duygu: DuyguEtiketi) -> list[KonuDuygusu]:
    """Bir yorum metninde gecen TUM konulari (KONU_ANAHTAR_KELIMELERI'ndeki)
    tespit edip, her biri icin o konunun GECTIGI ifadeye ozel bir duygu
    atar. Ilgili ifadede sozlukten hicbir duygu kelimesi bulunamazsa (NOTR
    donerse), o yorumun GENEL duygusu (modelin tahmini) varsayilan olarak
    kullanilir -- boylece 'guzel bir yerdi, manzarasi da vardi' gibi konu
    ozelinde acik bir duygu ifadesi olmayan ama genel olarak olumlu olan
    durumlar da makul sekilde etiketlenir."""
    ifadeler = ifadelere_ayir(metin)
    konu_duygulari: list[KonuDuygusu] = []
    tespit_edilen_konular: set[str] = set()

    for ifade in ifadeler:
        ifade_kucuk = turkce_kucuk_harf(ifade)
        for konu, anahtar_kelimeler in KONU_ANAHTAR_KELIMELERI.items():
            if konu in tespit_edilen_konular:
                continue  # Ayni konu birden fazla ifadede geciyorsa, ILK gecistigi yeri kullan.
            if any(anahtar in ifade_kucuk for anahtar in anahtar_kelimeler):
                yerel_duygu = ifade_duygusunu_belirle(ifade)
                nihai_duygu = yerel_duygu if yerel_duygu != DuyguEtiketi.NOTR else genel_duygu
                konu_duygulari.append(KonuDuygusu(konu=konu, duygu_etiketi=nihai_duygu, gecen_ifade=ifade))
                tespit_edilen_konular.add(konu)

    return konu_duygulari
