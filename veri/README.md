# Veri Katmanı

Bu klasör veri toplama (scraping), kaynaklar arası eşleştirme, duygu analizi ve
veri kalite kontrolünü içerir. Detaylı açıklamalar için `dokumanlar/` klasörüne
bak (özellikle `kategori_taksonomisi.md` ve `veri_sozlugu.md`).

## Kurulum

```bash
cd veri
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
playwright install chromium     # Google Maps ve TripAdvisor toplayicilari icin sart
```

Komutları **repo kökünden** (`gezi_bot/` içinden) çalıştır, çünkü modüller
`ortak.*` ve `veri.*` şeklinde birbirine referans veriyor:

```bash
python -m veri.toplayicilar.osm_toplayici --sehir samsun
```

## Toplayıcılar (`toplayicilar/`)

| Betik | Kaynak | Nasıl çalışır |
|---|---|---|
| `osm_toplayici.py` | OpenStreetMap (Overpass API) | Resmi/ücretsiz API, tek istekte tüm şehri çeker. Hızlı (~15-20 sn), gecikme gerektirmez. |
| `google_maps_toplayici.py` | Google Maps | Playwright ile tarayıcı otomasyonu, insan-taklidi rastgele gecikmelerle arama yapar ve yer detayı + yorumları çeker. ~35 genel arama terimi + (opsiyonel) ilçe bazlı daraltılmış aramalarla geniş coğrafi kapsama hedefler. |
| `eksi_sozluk_toplayici.py` | Ekşi Sözlük | Statik HTML sayfalarını `requests` + `BeautifulSoup` ile çeker. Şehir merkezi + tüm ilçeler için ayrı "bölge" olarak tarar (bkz. Bölge Profili). |
| `tripadvisor_toplayici.py` | TripAdvisor | Playwright ile tarayıcı otomasyonu; öncelikle sayfanın schema.org (JSON-LD) yapısal verisini okur, DOM'a sadece yedek olarak başvurur. **Çok güçlü bot koruması var (ev/rezidansiyel IP'den bile engellendi, bkz. aşağıdaki bilinen kısıt) — varsayılan olarak `tum_kaynaklari_calistir.py`'de ATLANIR.** |
| `booking_toplayici.py` | Booking.com | Playwright ile tarayıcı otomasyonu; konaklama (otel/pansiyon/apart) yer + yorum verisi çeker (temizlik/konum/personel/fiyat-performans alt puanları dahil). **Türkiye'ye özel yasal erişim kısıtlaması nedeniyle Türkiye IP'sinden engellendi, bkz. aşağıdaki bilinen kısıt — varsayılan olarak `tum_kaynaklari_calistir.py`'de ATLANIR.** |

Her toplayıcı çıktısını `veri/cikti/ham/<kaynak>/<sehir>_<tarih>.jsonl` dosyasına
yazar. Her satır bağımsız bir JSON kaydıdır (JSONL formatı), böylece dosyayı
metin editörüyle açıp satır satır gözle kontrol edebilirsin.

### Tüm kaynakları tek komutla çalıştırma (`tum_kaynaklari_calistir.py`)

Çok saatlik, gözetimsiz bir tarama oturumu için tek bir orkestrator:

```bash
python -m veri.toplayicilar.tum_kaynaklari_calistir --sehir samsun
```

Google Maps ve Ekşi Sözlük'ü sırayla çalıştırır (TripAdvisor ve Booking.com,
aşağıdaki bilinen kısıtlar nedeniyle varsayılan olarak atlanır — `--tripadvisor-dene`
ve `--booking-dene` ile yine de denenebilir). Her kaynak KENDİ try/except
bloğunda çalışır: biri (örn. bir kaynak IP'den engellenirse) başarısız olursa
diğerleri yine de çalışır, tek bir kaynağın sorunu tüm geceyi boşa harcatmaz.

**Kesintiye dayanıklılık (resume):** Her toplayıcı, aynı isimli bir çıktı
dosyası zaten varsa (önceki bir çalıştırmadan kalan) içindeki kayıtları
"zaten işlenmiş" sayıp atlar — çok saatlik bir tarama yarıda kesintiye
uğrarsa (İnternet kopması, bilgisayarın kapanması vb.) veri kaybı olmadan
kaldığı yerden devam edilebilir. Ayrıca her toplayıcıda **kayıt bazlı**
try/except vardır: tek bir yerin/yorumun işlenmesi hata verirse (bir sonraki
Google güncellemesi, beklenmeyen bir HTML yapısı vb.) sadece o kayıt atlanır,
tüm tarama düşmez. Google Maps'te ayrıca sayfa gezinmesi (`goto`) için 3
denemeli bir yeniden-deneme mekanizması vardır — geçici bir DNS/ağ hatası
(örn. `ERR_NAME_NOT_RESOLVED`) tüm taramayı düşürmez, sadece o arama terimi
atlanır.

**Bot koruması / engel tespiti:** `ortak_araclar.py::engel_metni_var_mi`,
bilinen bot-koruması sistemlerinin (DataDome, reCAPTCHA/hCaptcha, Google'ın
"unusual traffic" sayfası vb.) HTML'de bıraktığı ortak izleri kontrol eder.
Bir toplayıcı engellendiğini tespit ederse, o ana kadar toplanan veriyi
diskte bırakıp **nazikçe durur** — sonsuz deneyip zaman/IP itibarı harcamaz.

### Google Maps nöbetçi (`nobetci_calistir.py`)

Çok saatlik Google Maps taramalarında Playwright bazen tek bir yerde
sessizce takılıp kalabiliyor (ne hata ne zaman aşımı — sadece sonsuz
bekleme). İçeriden thread ile kurtarmak güvenilir değil (Playwright sync
API thread-safe değil). Bu yüzden `nobetci_calistir.py` toplayıcıyı **ayrı
bir alt süreçte** çalıştırır, çıktı dosyasının değişme zamanını izler;
`--durgunluk-esigi` (varsayılan 180 sn) içinde yeni kayıt gelmezse süreci
işletim sistemi seviyesinde zorla öldürüp `--devam-et` ile yeniden
başlatır. Önceden kaydedilmiş yerler tekrar işlenmez.

```bash
python -u -m veri.toplayicilar.nobetci_calistir --sehir samsun --maks-sonuc 25 --maks-yorum 25 --ilce-bazli-arama --durgunluk-esigi 300
```

## Eşleme (`esleme/`) — Kaynaklar Arası Tekilleştirme

Farklı kaynaklardan (OSM, Google Maps, TripAdvisor) çekilen veride aynı
fiziksel yer birden fazla kez geçer. `eslestirici.py` bunları kural tabanlı
olarak (kategori eşitliği + coğrafi yakınlık + bulanık isim benzerliği)
tespit edip tek bir `BirlesikYer` kaydına indirger.

```bash
python -m veri.esleme.eslestirici --sehir samsun
```

Önce toplayıcıları çalıştırıp `veri/cikti/ham/` altında veri biriktirmen
gerekir. Çıktı `veri/cikti/islenmis/birlesik_yerler/<sehir>_<tarih>.jsonl`
dosyasına yazılır; ayrıca birden fazla kaynaktan doğrulanan örnek eşleşmeleri
gözle kontrol edebilmen için `veri/cikti/raporlar/esleme_<sehir>_<tarih>.md`
raporu üretilir. Eşleşme hassasiyetini `--mesafe-esigi` (metre) ve
`--isim-benzerlik-esigi` (0-100) argümanlarıyla ayarlayabilirsin. Detaylı
mantık için `veri/esleme/eslestirici.py` dosyasının en üstündeki notlara
bakabilirsin.

## Kalite Kontrol (`kalite_kontrol/`) — Türkçe Veri Kalite Raporu

`rapor_olustur.py`, veriyi **hiçbir şekilde değiştirmeden**, sadece
inceleyip Türkçe okunabilir bir kalite raporu üretir:

```bash
python -m veri.kalite_kontrol.rapor_olustur --sehir samsun
```

Rapor `veri/cikti/raporlar/kalite_<sehir>_<tarih>.md` dosyasına yazılır ve
şunları içerir:

- **Ham veri kapsaması**: her kaynaktan (OSM/Google Maps/TripAdvisor) kaç
  ham yer kaydı geldiği.
- **Birleşik katalog özeti**: kaç tekil yer var, kategori dağılımı, kaç
  kaynaktan doğrulandığı, temel alanların (adres, telefon, web sitesi,
  özellikler) ne kadarının eksik olduğu.
- **Aykırı/şüpheli kayıtlar**: Türkiye sınırları dışında kalan (muhtemelen
  enlem/boylam hatalı) kayıtlar + veri setinin kendi coğrafi dağılımına göre
  istatistiksel olarak aşırı uzak kalan kayıtlar (medyan/MAD tabanlı, tek bir
  aykırı değerin istatistiği "maskelememesi" için ortalama/standart sapma
  yerine bilinçli olarak medyan/MAD kullanılır).
- **Kaçırılmış olabilecek eşlemeler**: `eslestirici.py`'nin birleştirmediği
  ama yakın+isim-benzer kalan çiftler — belki eşleme eşiklerini gevşetmen
  gerekiyordur.
- **Ham yorum verisi özeti**: kaynak başına toplam yorum, ortalama uzunluk,
  çok kısa yorum oranı, yazarsız yorum oranı.

Bu rapor **düzeltme yapmaz**, sadece işaret eder — ne yapılacağına (kategori
eşlemesini güncellemek, bir toplayıcının seçicisini düzeltmek, eşleme
eşiklerini ayarlamak vb.) her zaman sen karar verirsin.

## Duygu Analizi (`duygu_analizi/`)

Ham yorumlara (Ekşi Sözlük + Google Maps + TripAdvisor) hem genel duygu
skoru hem de konu (aspect) bazlı duygu etiketleri ekler.

```bash
python -m veri.duygu_analizi.pipeline_calistir --sehir samsun
```

İki katmanlı çalışır:

1. **Genel duygu (`model.py`)**: Açık kaynak, ücretsiz bir Türkçe BERT
   modeli (`incidelen/bert-base-turkish-sentiment-analysis-128k-cased` —
   3 sınıflı: olumlu/nötr/olumsuz, CPU üzerinde çalışır, Oracle sunucuya
   uygun). İlk çalıştırmada model (~440MB) HuggingFace'ten indirilip
   önbelleğe alınır, sonrasında internet gerekmez.
2. **Konu (aspect) etiketleme (`konu_analizi.py`)**: BİLİNÇLİ OLARAK BERT
   kullanmaz — tamamen anahtar kelime + küçük bir Türkçe duygu sözlüğü +
   olumsuzluk (negation) tespitiyle çalışır. Sebep: sonucun HER ZAMAN
   şeffaf ve gözle denetlenebilir olması isteniyor (`gecen_ifade` alanı,
   bir konunun neden o duyguyla etiketlendiğini birebir gösterir — kara
   kutu değil). Türkçe'nin eklemeli yapısı (harika → harikaydı, harikaymış)
   nedeniyle tam kelime eşleşmesi değil, KÖK eşleşmesi (`startswith`)
   kullanılır; olumsuzluk eki Türkçe'de genelde kelimeDEN SONRA geldiği
   için (`temiz değildi`) pencere hem öncesine hem sonrasına bakar.

Çıktı `veri/cikti/islenmis/yorumlar/<sehir>_<tarih>.jsonl` dosyasına
(`IslenmisYorum` formatında) yazılır ve konsola kaynak/konu bazlı bir
duygu dağılımı özeti basılır. Konu listesini ve sözlüğü genişletmek
istersen `veri/duygu_analizi/konu_analizi.py` içindeki
`KONU_ANAHTAR_KELIMELERI`/`POZITIF_KOKLER`/`NEGATIF_KOKLER` listelerine
kelime eklemen yeterli, kod değiştirmen gerekmez.

## Yer Profili (`duygu_analizi/`) — Çok Boyutlu Profil ve Tanıtım Metni

`pipeline_calistir.py` yorum BAZLI çalışırken (her yorum için ayrı bir duygu/konu
etiketi), `profil_pipeline_calistir.py` YER BAZLI çalışır: bir yerin TÜM
yorumlarını birlikte değerlendirip o yerin fiyat algısı, ulaşım kolaylığı,
kalabalık zamanları ve ziyaretçi profili gibi somut boyutlarını çıkarır, ardından
bunlardan samimi bir Türkçe tanıtım metni üretir. Detaylı boyut açıklamaları için
`dokumanlar/kategori_taksonomisi.md` #6'ya bakınız.

```bash
python -m veri.esleme.eslestirici --sehir samsun              # once bu (BirlesikYer kataloğu)
python -m veri.duygu_analizi.pipeline_calistir --sehir samsun  # sonra bu (IslenmisYorum)
python -m veri.duygu_analizi.profil_pipeline_calistir --sehir samsun
```

Üç aşamalıdır:

1. **Bağlama (`yer_profili_cikarici.py::yorumlari_yerlere_bagla`)**: Her yorumu,
   kaynak + kaynak kimliği eşleşmesiyle ait olduğu `BirlesikYer` kaydına bağlar.
2. **Boyut çıkarımı (`yer_profili_cikarici.py`)**: Bir yere bağlanan TÜM
   yorumlar birlikte taranıp `fiyat_algisi`, `ulasim_kolayligi`,
   `kalabalik_zamanlar`, `ziyaretci_profili` boyutları çıkarılır. Aynen
   `konu_analizi.py` gibi BİLİNÇLİ OLARAK BERT kullanmaz — anahtar
   kelime/ifade sayımıyla çalışır, her sonuç `ornek_ifadeler` alanıyla kaynak
   cümleye kadar izlenebilir. Yeterli sayıda bahsedilme olmayan boyutlar
   (varsayılan eşik: 3) uydurma bir izlenim vermemek için `bilgi_yetersiz`
   döner ve tanıtım metninde sessizce atlanır.
3. **Anlatım üretimi (`anlatim_uretici.py`)**: Çıkarılan profil + en çok
   bahsedilen konu/duygu çiftlerinden (fiyat/konum/kalabalık hariç, zaten
   dedike boyutlarla kapsandığı için) samimi bir Türkçe paragraf üretir.
   BİLİNÇLİ OLARAK bir üretici dil modeli (LLM) KULLANILMAZ — sebep hem
   Oracle sunucunun CPU'da büyük bir modeli hızlı çalıştıramayacak olması hem
   de projenin şeffaflık ilkesiyle çelişmemesi (detay için dosyanın üst
   notuna bakabilirsin). Bunun yerine her boyut için birden fazla ifade
   varyantı tanımlanır; hangi varyantın seçileceği yerin kimliğinden türetilen
   SABİT bir rastgele tohumla belirlenir — aynı yer her çalıştırmada aynı
   metni alır, farklı yerler farklı ifade kalıplarına düşer (tekdüzelik
   önlenir).

Çıktı `veri/cikti/islenmis/yer_profilleri/<sehir>_<tarih>.jsonl` dosyasına
(`YerProfili` formatında, üretilen tanıtım metni dahil) yazılır ve konsola
fiyat/ulaşım dağılımı + örnek bir tanıtım metni basılır.

**Yer-ismi tespiti ile fırsatçı bağlama:** Ekşi Sözlük yorumları varsayılan
olarak şehir/ilçe genelindedir (bir yere değil bir bölgeye bağlıdır), bu
yüzden doğrudan bir yerin profiline KATILAMAZ. Ancak `yer_ismi_tespiti.py`,
böyle bir bölge-geneli yorumun metninde bilinen bir `BirlesikYer` isminden
(2+ kelimelik, yeterince ayırt edici, örn. "Amazon Koyu") biri geçip
geçmediğini kelime-sınırı farkındalığıyla arar; geçiyorsa o yorum HEM bölge
profiline HEM (fırsatçı olarak) o yerin profiline de katkı sağlar. Bu basit
metin eşleştirmesi olduğu için nadir yanlış-pozitif/negatif üretebilir
(kabul edilebilir, gözle denetlenebilir kalır — hangi yorumun hangi yere
bağlandığı her zaman izlenebilir).

## Bölge Profili (`duygu_analizi/bolge_profili_*.py`) — Şehir/İlçe Tanıtım Duygu Analizi

Belirli bir yerden değil, doğrudan bir şehrin/ilçenin KENDİSİNDEN bahseden
Ekşi Sözlük yorumlarından (bkz. `sehir_ayarlari.py::ilceler` ve
`eksi_sozluk_bolge_basliklari`), o şehri/ilçeyi kullanıcıya tanıtacak genel
bir duygu profili üretir. `Yer Profili`nin (yukarıda) aynı tasarım
felsefesini paylaşır: BERT/LLM kara kutu KULLANMAZ, anahtar kelime + ifade
sayımıyla çalışır, her sonuç kaynak cümleye kadar izlenebilir.

```bash
python -m veri.duygu_analizi.bolge_profili_pipeline_calistir --sehir samsun
```

Girdi olarak `pipeline_calistir.py`'nin ürettiği `IslenmisYorum` kayıtlarını
(kaynak_yer_id'si `"bolge:<sehir>:<bolge_adi>"` biçiminde olanları) kullanır:

1. **Gruplama (`bolge_profili_cikarici.py::yorumlari_bolgelere_bagla`)**: Her
   yorumu `kaynak_yer_id`'sinden ayrıştırdığı bölgeye göre gruplar.
2. **Konu/duygu çıkarımı**: `konu_analizi.py::KONU_ANAHTAR_KELIMELERI`'ne
   bölgeye özel konular eklenmiştir (`guvenlik`, `trafik`, `doga`,
   `tarihi_doku`, `gece_hayati`, `yasam_maliyeti`) — bir ilçenin "sakin/
   güvenli" mi yoksa "gece hayatı canlı" mı olduğu gibi tanıtım amaçlı
   nitelikler bu şekilde çıkarılır.
3. **Anlatım üretimi (`anlatim_uretici.py::bolge_tanitim_metni_uret`)**: Yer
   tanıtımıyla aynı şablon-tabanlı, sabit-tohumlu yaklaşımla ("bu ilçeyi/şehri
   anlatanlar..." gibi) bir tanıtım paragrafı üretir.

Çıktı `veri/cikti/islenmis/bolge_profilleri/<sehir>_<tarih>.jsonl` dosyasına
(`BolgeProfili` formatında) yazılır. Veritabanına `sunucu/veritabani/aktarim/
bolge_profil_aktar.py` ile aktarılır ve `GET /sehirler/{sehir_anahtari}/bolgeler`
API endpoint'i ile (şehir + tüm ilçe profilleri) okunabilir. Bu yapı, ileride
başka şehir/ilçeler eklendiğinde HİÇBİR KOD DEĞİŞİKLİĞİ GEREKTİRMEZ — sadece
`sehir_ayarlari.py`'ye yeni şehrin ilçe listesi eklenir.

Pratik not: bu profilin ana veri kaynağı Ekşi Sözlük'tür; Google Maps ve
Booking.com yorumları BELİRLİ bir yere bağlı olduğu için (bölge-geneli değil)
Bölge Profili'ne katılmaz, sadece Yer Profili'ne katılır.

## Şehir Ekleme

Yeni bir şehir eklemek için tek yapman gereken `veri/ortak/sehir_ayarlari.py`
içindeki `SEHIRLER` sözlüğüne yeni bir `SehirAyari` eklemek. Toplayıcıların
hiçbirinin kodu değişmez.

## Örnek: OSM Toplayıcısını Çalıştırma

```bash
python -m veri.toplayicilar.osm_toplayici --sehir samsun
```

Bu komut Samsun için OpenStreetMap'teki tüm eşlenebilir yerleri (gezilecek
yer, konaklama, restoran/kafe vb.) çekip
`veri/cikti/ham/osm/samsun_<bugunun-tarihi>.jsonl` dosyasına yazar ve
konsola kategori bazlı bir özet basar.

## Örnek: Google Maps Toplayıcısını Çalıştırma

```bash
python -m veri.toplayicilar.google_maps_toplayici --sehir samsun --maks-sonuc 25 --maks-yorum 35 --ilce-bazli-arama
```

Varsayılan arama terimleri listesini (`VARSAYILAN_ARAMA_TERIMLERI`, ~35 terim:
kafe/restoran/otel/plaj + cami/kilise/türbe, AVM, pide/lahmacun/döner,
pastane/çikolatacı, hamam/spa, sinema/tiyatro, şelale/gölet, akvaryum/
hayvanat bahçesi, lunapark vb.) kullanarak Samsun'da arar; her sonucun
detayını (isim, kategori, adres, telefon, web sitesi, puan) ve varsa
yorumlarını çeker. `--ilce-bazli-arama` verilirse en genel 3-4 terim
("gezilecek yerler", "restoranlar", "kafeler", "plajlar") için AYRICA
Samsun'un 17 ilçesiyle daraltılmış aramalar da yapılır — şehir merkezi
dışındaki coğrafi kapsamı artırır. Çıktılar
`veri/cikti/ham/google_maps/samsun_yerler_<tarih>.jsonl` ve
`..._yorumlar_<tarih>.jsonl` dosyalarına yazılır.

Yerelde tarayıcıyı gözle izlemek istersen `--headed` bayrağını ekle. Oracle
sunucu gibi ekransız ortamlarda bayrak eklemeden (varsayılan `headless`)
çalıştır.

**Bilinen kısıt:** Google, oturum açılmamış/otomasyon izlenimi veren
oturumlara bazen "sınırlı görünüm" gösterip yorumları gizleyebiliyor. Bu
toplayıcı yer bilgisini güvenilir şekilde çeker; yorumlar bazı yerlerde boş
dönebilir (hata değildir). Bu yüzden duygu analizinin ana veri kaynağı Ekşi
Sözlük ve zamanla kendi site içi yorumlarımız olacak — Google Maps öncelikle
bir "yer kataloğu" kaynağıdır. Detay için
`veri/toplayicilar/google_maps_toplayici.py` dosyasının en üstündeki notlara
bakabilirsin.

## Örnek: TripAdvisor Toplayıcısını Çalıştırma

```bash
python -m veri.toplayicilar.tripadvisor_toplayici --sehir samsun --kategoriler gezilecek_yer restoran otel
```

Sırasıyla gezilecek yer, restoran ve otel listeleme sayfalarını gezip her
sonucun detay sayfasına girer; veriyi öncelikle sayfanın SEO amaçlı
schema.org (JSON-LD) yapısal verisinden okur (isim, adres, telefon, konum,
puan ortalaması/sayısı ve varsa birkaç örnek yorum) — bu, CSS sınıf
adlarından çok daha kalıcıdır. JSON-LD'de yorum yoksa/azsa, yorum kalıcı
bağlantısının URL desenine (`-r<sayı>-`) dayanan best-effort bir DOM yedek
yöntemi devreye girer.

**Bilinen kısıt (önemli):** TripAdvisor, Google Maps ve Ekşi Sözlük'ten çok
daha agresif bir bot koruması (DataDome) kullanıyor. Bu proje geliştirilirken
paylaşımlı/veri-merkezi IP'lerden gelen istekler **daha ilk sayfa
yüklemesinde** "Erişim geçici olarak kısıtlanmıştır" duvarına takıldı.
**2026-08-03'te kullanıcının kendi EV/rezidansiyel IP'sinden de tekrar test
edildi ve AYNI ŞEKİLDE ENGELLENDİ** — yani bu IP itibarına özgü bir durum
değil, DataDome'un TripAdvisor için genel bir koruma seviyesi. Bu yüzden
`tum_kaynaklari_calistir.py` TripAdvisor'ı **varsayılan olarak atlar**
(`--tripadvisor-dene` ile yine de denenebilir, örn. farklı bir ağdan/VPN'den).
Toplayıcı bu durumu otomatik tespit edip (`_engellenmis_mi`) çalışmayı o anda
**nazikçe durdurur** ve o ana kadar toplanan veriyi kaybetmeden açıklayıcı bir
Türkçe hata basar — sonsuz denemeye devam edip zaman/ağ kaynağı harcamaz.

Pratik sonuç: TripAdvisor'ı projenin **ana** yorum kaynağı olarak
sayma; Ekşi Sözlük (Türkçe serbest metin), Google Maps (yer kataloğu) ve
Booking.com (konaklama yorumları) ana kaynaklar olarak kalsın, TripAdvisor'ı
yalnızca farklı bir ağ/IP'den (örn. mobil veri, farklı bir konum) ek/doğrulama
kaynağı olarak dene. Ayrıca DOM tabanlı yorum seçicileri (`SECICILER`),
TripAdvisor'ın engeli yüzünden canlı DOM üzerinde tam test edilerek
yazılamadı — production'a almadan önce `--headed` bayrağıyla tek bir sayfa
açıp gözle doğrulaman önerilir. Detay için
`veri/toplayicilar/tripadvisor_toplayici.py` dosyasının en üstündeki
notlara bakabilirsin.

## Örnek: Booking.com Toplayıcısını Çalıştırma

```bash
python -m veri.toplayicilar.booking_toplayici --sehir samsun
```

Konaklama kategorisini güçlendirmek için eklenen bu kaynak, otel arama
sonuçlarını gezip her otelin yorumlarını (temizlik/konum/personel/
fiyat-performans alt puanları dahil) çeker; kategori her zaman `KONAKLAMA`,
alt kategori Booking'in "mülk tipi" metninden eşlenir (otel/pansiyon/hostel/
apart/villa).

**Bilinen kısıt (önemli):** Booking.com, Türkiye'deki tesisler için
Türkiye'den gelen istekleri **yasal/düzenleyici bir gerekçeyle** (mahkeme
kararı olabilir) engelliyor — bu bir IP itibarı/bot koruması sorunu DEĞİL,
Türkiye'ye özel bir erişim kısıtlaması; arama sonuçları ve otel sayfaları
Türkiye IP'sinden anasayfaya yönlendiriliyor. 2026-08-03'te kullanıcının kendi
IP'sinden doğrulandı. Bu yüzden `tum_kaynaklari_calistir.py` Booking.com'u da
**varsayılan olarak atlar** (`--booking-dene` ile yine de denenebilir, örn.
yurt dışı bir VPN/sunucudan). Not: engel aşılsa bile Türkiye'deki tesislerin
Booking.com yorumları büyük ölçüde YABANCI dillerde olduğu için, bu kaynağın
Türkçe duygu analizine katkısı sınırlı kalabilir — asıl amacı konaklama
kategorisinin yer/temel bilgi kapsamını (adres, fiyat aralığı, puan) 
artırmaktır.
