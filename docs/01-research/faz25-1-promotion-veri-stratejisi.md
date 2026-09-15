---
title: FAZ 25.1 — Promotion gate ve veri stratejisi
version: 1.0
status: Development doğrulaması; ürün geçişi engelli
phase: FAZ 25.1
last_update: 2026-09-15
depends: [00-urun-felsefesi, 01-bilgi-mimarisi, 02-product-language, 03-karar-motoru, 04-sistem-mimarisi]
affects: [Bugün Ne Yapalım, NLP, admin review, Akıllı Rota]
author: Codex
---

# Haklar ve veri stratejisi kararı

19.609 yorumun tamamı Google Maps. Development DB'de Google için KaynakPolitikasi yok. Processing, derivative, retention ve public izinleri unknown; hukuki izin varsayılmadı. Yorum metinleri bu turda NLP modeline verilmedi; yalnız kayıt adetleri/kaynak metadata'sı incelendi. Yeni NLP AdayGozlem 0, yeni claim candidate 0, yeni public claim 0. Eski pilotun 41 gözlemi/aday claim'i korunmuştur.

Google verisi mevcut hak kayıtlarıyla ürünün türev claim üretimi için **kullanılabilir sayılmaz**. Bu tüm olası sözleşmeler hakkında hukuki hüküm değildir. Projenin fiili sözleşmesi/izin kapsamı doğrulanmamıştır. [Google Maps Platform şartları](https://cloud.google.com/maps-platform/terms), [Google Maps ek şartları](https://www.google.com/intl/en-US/help/terms_maps/) ve [Places veri politikaları](https://developers.google.com/maps/documentation/places/web-service/policies) kontrol edilmeden scraper verisi, uzun saklama veya türev üretim meşru kabul edilmemelidir. API üzerinden veri almak da kendiliğinden türev/retention hakkı vermez.

Ana NLP CLI artık kaynak politikalarını ham dosya yükleme ve model çalıştırma öncesinde kontrol eder. Gerçek development komutu hakları doğrulanmış işlenebilir yorum olmadığı için modelden önce durdu. Eski farklı collector/profil pipeline'larının tamamı bu değişiklikle kapatılmış değildir; Google cache/profil türevleri rights audit tamamlanmadan yeni yayın dayanağı yapılmamalıdır.

## Gerçek distribution ve promotion kararı

Google metinlerinden aday üretmek yerine mevcut izinli OSM claim/evidence metadata'sı aggregate edildi: 209 branch+family grubu, 206 grupta 1 supporting observation, 3 grupta 2. Hepsi tek kaynak. 209 grupta branch verification, freshness ve verified evidence eksik. 80 grup subjective sınıfta. Admin review promotion uygun 0. Mevcut review kuyruğuna yeni kayıt eklenmedi.

Sayısal destek eşiği kalibre edecek bağımsız doğruluk etiketleri ve kaynak çeşitliliği yok. Bu nedenle “3 yorum yeter” gibi eşik uydurulmadı. Config fail-closed: factual ailelerde dört hakkın izinli olması, branch kimliğinin insan tarafından doğrulanması, gözlem zamanı ve geçerlilik süresinin doğrulanması, destek evidence bulunması, counter conflict olmaması; subjective ailelerde kalibrasyon tamamlanana kadar promotion kapalı. Çelişki inceleme gerektirir, otomatik olumluya çevrilmez. Gate'in geçmesi yalnız admin review uygunluğudur; hiçbir yerde auto-publication sağlamaz.

Aggregate internal alanları: supporting/counter observation count, unique evidence count (source+nativerecord), source diversity, date range, freshness, conflict level, counter share, branch confidence, rights status, verified evidence count. Observation kimliği ile evidence kimliği ayrı tutulur; tekrar span/source kaydı yeni bağımsız evidence sayılmaz. Freshness için keyfi gün sayısı yerine aileye göre açık geçerlilik bilgisi gerekir; bilinmeyen tarih güncel sayılmaz.

## Öncelikli alternatif

1. First-party admin observation ve işletme doğrulaması: doğru şube, lisans/processing/derivative/retention/public izinleri, doğrulayan kişi, gözlem tarihi ve aileye uygun geçerlilik. Wi-Fi, otopark, laptop politikası, menü/fiyat ve saatler ayrı facts.
2. Resmi işletme/müze/municipal kaynaklar: kaynak metadata ve kullanım hakkı doğrulaması sonrası structured facts; resmi olmak sınırsız yeniden kullanım hakkı anlamına gelmez.
3. OSM: lisanslı kimlik, koordinat ve uygun structured tags. [OSM copyright/ODbL](https://www.openstreetmap.org/copyright) attribution ve ilgili share-alike yükümlülükleri değerlendirilir; kalite ve freshness ayrıca doğrulanır. Google yorumları OSM lisansıyla yeniden etiketlenemez.
4. Kullanıcı katkısı: açık izin, source/branch doğrulaması, counter sinyal, moderasyon ve abuse kontrolü; ham yorumdan public claim'e doğrudan yol yok.
5. Google scraper kapsamını artırmak şu an kapasite açığını çözmez; hak ve yayınlanabilir bilgi darboğazını büyütür. Yeni scraper ancak kaynak hakkı ve kimlik/freshness stratejisine göre seçilmeli.

## Canonical ilçe güvenli çözüm

1719 yerden 26 ilce_id var; 1693 eksik. 1692 yerde upstream ilçe metni de yok; bir serbest metin “merkez” canonical ilçeye bağlanmıyor. Koordinat bütün yerlerde var. Importer'da yeni metin eksik geldiğinde mevcut ilce_id'yi silme davranışı düzeltildi. Önceden bağlanmış 26 ilişki coordinate/polygon açısından yeniden doğrulanmış sayılmaz.

Kör string backfill yapılmadı. Güvenilir resmi polygonun sürümü, veri hakkı, CRS, topology ve Samsun canonical district eşlemesi doğrulanamadığından development DB'ye coğrafi backfill uygulanmadı. [TUCBS](https://basic.atlas.gov.tr/?_appToken=&metadataId=%2Feski) veri erişimini metadata/paylaşım koşullarıyla düzenler; erişilebilir doğrulanmış resmi ilçe dataset'i bu turda elde edilmedi. Güvenli uygulama: staging polygon import, ST_Covers ile tek district eşleşmesi, sınır/çoklu/boş eşleşmeleri admin kuyruğuna ayırma, city consistency ve anomaly review, provenance kaydı, ardından yalnız doğrulanmış tekil eşleşmelere additive backfill. Branch koordinat provenance ve doğruluğu da doğrulanmalıdır; nokta varlığı doğru şube veya doğru city garantisi değildir. İlçe stratejisi nettir; veri girdisi eksik olduğu için sorun fiilen kapanmamıştır.

## Geçiş kararı

Genel Bugün Ne Yapalım ihtiyacı için veri yeterli değil. Akıllı Rota'ya geçiş **NO-GO**: branch/coğrafya, güncel saat/süre/ulaşım ve ihtiyaç aileleri doğrulanmadan çok duraklı plan güvenilir sayılamaz. Önce hakları açık küçük bir şehir/şube pilotuyla aile bazlı gerçek doğruluk etiketleri oluşturulmalı; mevcut 126 parser corpus'u promotion veya öneri doğruluk gold'u değildir.

## Belge ilişkileri

Bağlı belgeler: docs/00-product/00-urun-felsefesi.md, 01-bilgi-mimarisi.md, 02-product-language.md, 03-karar-motoru.md, 04-sistem-mimarisi.md.

Etkilediği belgeler: docs/04-ai/05-ai-bilgi-motoru.md, docs/00-product/06-akilli-rota-motoru.md, docs/02-ux/07-ux-karar-akislari.md.

Bundan sonra okunacak belge: bu ölçümle birlikte faz25-1-oneri-gold.md ve faz25-1-promotion-veri-stratejisi.md. Sahada bağımsız öneri doğrulama planı planlanmıştır; gerçekleştirilmiş sayılmaz.
