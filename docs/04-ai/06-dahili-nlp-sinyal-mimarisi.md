---
title: "Şamandıra — Dahili NLP Sinyal Mimarisi"
version: "1.2"
status: "uygulama-sozlesmesi"
phase: "faz-25.2"
last_update: "2026-09-15"
depends:
  - "../00-product/01-bilgi-mimarisi.md"
  - "../00-product/03-karar-motoru.md"
  - "../00-product/04-sistem-mimarisi.md"
  - "./05-ai-bilgi-motoru.md"
  - "../../dokumanlar/kategori_taksonomisi.md"
affects:
  - "../../ortak/sabitler.py"
  - "../../veri/ortak/gozlem_adayi_modeli.py"
  - "../../veri/duygu_analizi/gozlem_adayi.py"
  - "../../veri/duygu_analizi/konu_analizi.py"
  - "../../sunucu/bilgi/domain.py"
  - "../../sunucu/bilgi/pilot_claimleri.py"
author: "Cursor"
---

# Şamandıra — Dahili NLP Sinyal Mimarisi

## Amaç ve sınır

Bu belge, izinli metin işlemeden çıkan sinyali yayımlanmış bilgi ve karar
iddiasından ayıran teknik sözleşmeyi tanımlar. NLP çıktısı yalnız
`AdayGozlem` üretir. Yer puanı, sıralama bonusu, hard constraint, kamusal
metin veya otomatik yayın üretmez.

Canonical aile sözlüğü
`dokumanlar/kategori_taksonomisi.md#8-dahili-gözlem-sinyali-taksonomisi`
bölümündedir. Kod karşılığı `ortak/sabitler.py::DahiliSinyalAilesi` olur.

## Sinyal türleri

- `fact_signal`: Açık varlık/yokluk gibi sonradan doğrulanabilir ifade.
- `experience_signal`: Belirli ziyaret ve bağlamda yaşanan deneyim.
- `sentiment_signal`: Genel veya konuya bağlı kişisel tepki.

`support` ve `counter`, spanın ilgili aileye göre yönüdür; doğruluk veya yayın
kararı değildir. “Güzel”, “mükemmel”, “kaliteli”, “en iyi” ve “romantik”
gibi genel ifadeler yalnız `sentiment_signal` olabilir. Bunlar tek başına
uygunluk iddiasına çevrilmez.

## Safe extractor

Safe extractor Unicode metni deterministik olarak normalize eder ve yalnız
sürümlü, dar desenleri çalıştırır. Her eşleşme aile, yön, değer, gözlem türü,
kural sürümü ve güven kırılımı taşır. Aynı metinde farklı ailelere ait
birden fazla sinyal üretilebilir. Aynı ailede daha dar explicit karşı desen,
geniş destek deseninden önce değerlendirilir.

Genel Türkçe BERT duygu çıktısı explicit aspect polarity için fallback
değildir. BERT çıktısı yalnız canonical `genel_duygu` ailesinde, karar dışı
`sentiment_signal` candidate olarak tutulur; nötr sonuç candidate üretmeyebilir.
Bu aile tercih, sıralama, hard constraint veya public iddia girdisi değildir.
Kural eşleşmesinin güven sınıfı BERT skorundan yükseltilmez.

Safe extractor `degil` yakınlığını tekil ifade regex'leriyle değil, her aspect
eşleşmesinden sonra çalışan ortak negation adımıyla değerlendirir. Boolean
değer güvenle ters çevrilir; string deneyim değeri yalnız sürümlü ters değer
sözlüğünde karşılığı varsa çevrilir, aksi halde aday üretilmez. `park sorunu`
varlık/yokluk olgusu değil, ziyaret bağlamlı `experience_signal counter`
olarak değerlendirilir. Yerel ifade nötr kaldığında aspect sentiment adayı
üretilmez.

## AdayGozlem sözleşmesi

Her kayıt şu izleri taşır:

1. Kaynak, kaynak yorum/kayıt kimliği, kaynak-yer kimliği ve şube adayı.
2. Canonical aile/konu, yön, değer ve gözlem türü.
3. Çıkarım yöntemi, model sürümü ve kural sürümü.
4. Güven sınıfı ve açıklanabilir güven kırılımı.
5. Zaman kapsamı ve zamansal durum.
6. Span hash'i ve dahili referans.

Varsayılan `canonical-v1` sözleşmesi stricttir: canonical alanlar explicit
verilir; aile whitelist'i ile family/type/direction/value sözlüğü birlikte
doğrulanır. Keyfi değer ve yönsüz fact/experience kabul edilmez. Geriye uyumlu
parse, sürüm alanı bulunmayan kayıt yalnız tarihî zorunlu ve opsiyonel alanların
exact shape'ini değiştirmeden taşıyorsa otomatik `legacy` olarak tanınır.
Legacy nesne serialize edildiğinde `sozlesme_surumu=legacy` marker'ı açıkça
korunur; tam model dump şekli, değişmez `otomatik_yayinlanabilir=false` alanı
ve `cikarim_yontemi=geriye_uyumlu` iziyle yeniden parse edilebilir. Bunun
dışında canonical izlerden herhangi birini içeren yeni payload, marker'ı
`legacy` olsa bile canonical strict doğrulamaya girer; marker değişikliği
producer doğrulamasını bypass edemez.

Ham span geçici dahili işlem belleğinde bulunabilir. Kalıcı candidate
çıktısına yazılması için ayrıca `uzun_sureli_saklama=izinli` gerekir; hak
bilinmiyor veya yasaksa JSONL yalnız span hash'i ve dahili referansı taşır.
Kaynak yazar bilgisi aday sözleşmesinin ve kalıcı candidate çıktısının parçası
değildir. `otomatik_yayinlanabilir` nesne ve JSON serialization düzeyinde
değişmez biçimde `false` olur.

Dahili referans; kaynak/review kimliği, kaynak-yer, şube, aile, gözlem türü,
yön, span hash'i, model sürümü ve kural sürümünün canonical JSON hash'idir.
Dışarıdan gelen span hash'i veya referans yetkili sayılmaz; span ve canonical
alanlardan deterministik olarak yeniden üretilir.

Kaynak review kimliği yoksa producer, kaynak adı + kaynak-yer kimliği + tam
yorum içeriğinden SHA-256 dahili review fingerprint üretir. Tam yorum modelde
ayrı alan olarak saklanmaz. Aynı yorum tekrarı aynı fingerprint'i; aynı aspect
spanını taşısa bile farklı tam yorum içeriği farklı fingerprint ve referansı
üretir. Canonical kayıt source record kimliği veya bu fingerprint'ten birini
taşımak zorundadır.

## Hak kapıları

Hak kontrolü akışın amacıyla yapılır:

- Dahili NLP için `ai_isleme` hakkı aranır.
- Türev iddia için `turev_iddia` hakkı ayrıca aranır.
- Kamusal gösterim için `kamusal_gosterim` hakkı ayrıca aranır.
- Uzun süreli saklama için `uzun_sureli_saklama` hakkı ayrıca aranır.

Bir amaçtaki izin başka bir amaca taşınmaz. Bu nedenle yalnız `ai_isleme`
izni geçici dahili işlemi açabilirken ham span saklama, kamusal veya türev
kapısını açmaz. Kalıcı payload hazırlanırken saklama hakkı ayrıca kontrol
edilir. Bilinmeyen/veri sözlüğü dışı DB hak değeri exception üretmek yerine
fail-closed sonuç verir. Mevcut OSM public pipeline dört gerekli hakkın
tamamını aramaya devam eder ve tek eksik hakta kapanır.

## Hard constraint ve yayın

Hiçbir `AdayGozlem` doğrudan hard constraint değildir.
`experience_signal` ve `sentiment_signal` hard constraint olamaz.
`fact_signal` ancak doğru şubeye bağlanıp güncellik, doğrulama, kaynak hakkı,
iddia sürümü, inceleme ve yayın kapılarından geçtikten sonra Karar Motoruna
girdi olabilir. Karşı sinyal destek sayısıyla silinmez; çelişki olarak
korunur.

## Test ve veri güvenliği

Extractor testleri yalnız sentetik Türkçe ifadeler kullanır. Gerçek kaynak
ham metni veya yazar bilgisi fixture ve dokümana kopyalanmaz. Testler explicit
olumsuzluk, fact/experience ayrımı, aynı metinde iki aspect, genel sentiment
ayrımı, amaç-bazlı hak kontrolü ve otomatik yayın yasağını doğrular.

## Bu dokümanın bağlı olduğu belgeler

- [01 Bilgi Mimarisi](../00-product/01-bilgi-mimarisi.md)
- [03 Karar Motoru](../00-product/03-karar-motoru.md)
- [04 Sistem Mimarisi](../00-product/04-sistem-mimarisi.md)
- [05 AI Bilgi Motoru](./05-ai-bilgi-motoru.md)
- [Kategori Taksonomisi](../../dokumanlar/kategori_taksonomisi.md)

## Bu dokümanın etkilediği belgeler

- [Dokümantasyon Dizini](../README.md)
- `05-api`, `07-backend` ve `08-admin` altındaki planlanan aday inceleme,
  iddia kabulü ve yayın sözleşmeleri.

## Bundan sonra okunması gereken belge

[05 AI Bilgi Motoru](./05-ai-bilgi-motoru.md) ile birlikte okunmalıdır.
Sonraki çalışma, `08-admin` altında planlanan aday inceleme ve hak görünürlüğü
sözleşmesidir; henüz yazılmamıştır.
