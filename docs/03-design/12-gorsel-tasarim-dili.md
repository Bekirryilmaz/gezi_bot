---
title: "12 Şamandıra — Visual Language"
version: "1.1"
status: "gorsel-dil-onerisi; kullanici-incelemesine-hazir"
phase: "gorsel-tasarim-dili-dokumantasyonu"
last_update: "2026-09-14"
depends:
  - "00-product/00-urun-felsefesi.md"
  - "00-product/01-bilgi-mimarisi.md"
  - "00-product/02-product-language.md"
  - "00-product/03-karar-motoru.md"
  - "00-product/04-sistem-mimarisi.md"
  - "04-ai/05-ai-bilgi-motoru.md"
  - "00-product/06-akilli-rota-motoru.md"
  - "02-ux/07-ux-karar-akislari.md"
  - "03-design/08-tasarim-ilkeleri.md"
  - "09-business/09-urun-ekosistemi.md"
  - "03-design/10-design-system.md"
  - "03-design/11-ekran-mimarisi.md"
  - "README.md (proje kokunde)"
  - "docs/README.md"
  - "plan/00_brief_eki.md (celismeyen marka varligi kilitleri)"
  - "plan/04_marka_ve_tema.md (tarihsel gorsel baglam)"
  - "plan/tasarim/yon.md (tarihsel gorsel baglam)"
affects:
  - "Gorsel uygulama ve bilesen kabul incelemeleri (planlanan)"
  - "UX ve erisilebilirlik dogrulama plani (planlanan)"
  - "Gorsel rol ve durum katalogu (planlanan)"
author: "Codex"
---

# 12 Şamandıra — Visual Language

## İçindekiler

- [Belge Kapsamı ve Referans Sınırları](#belge-kapsamı-ve-referans-sınırları)
- [Marka Kimliği](#marka-kimliği)
- [Tasarım Felsefesi](#tasarım-felsefesi)
- [Görsel İlkeler](#görsel-i̇lkeler)
- [Tasarım Dili](#tasarım-dili)
- [Premium Hissi Nasıl Oluşuyor](#premium-hissi-nasıl-oluşuyor)
- [Beyaz Alan Kullanımı](#beyaz-alan-kullanımı)
- [Grid Sistemi](#grid-sistemi)
- [8pt Grid](#8pt-grid)
- [Layout Kuralları](#layout-kuralları)
- [Kart Tasarımları](#kart-tasarımları)
- [Radius Sistemi](#radius-sistemi)
- [Elevation](#elevation)
- [Shadow Sistemi](#shadow-sistemi)
- [Cam Efekti](#cam-efekti)
- [Blur Kullanımı](#blur-kullanımı)
- [Material You ile İlişki](#material-you-ile-i̇lişki)
- [iOS Human Interface Guidelines ile İlişki](#ios-human-interface-guidelines-ile-i̇lişki)
- [Android Tasarım Uyumu](#android-tasarım-uyumu)
- [Dark Mode Felsefesi](#dark-mode-felsefesi)
- [Light Mode Felsefesi](#light-mode-felsefesi)
- [Tipografi Hiyerarşisi](#tipografi-hiyerarşisi)
- [Font Kullanımı](#font-kullanımı)
- [Satır Yüksekliği](#satır-yüksekliği)
- [Harf Aralıkları](#harf-aralıkları)
- [Başlık Sistemi](#başlık-sistemi)
- [Buton Dili](#buton-dili)
- [CTA Kuralları](#cta-kuralları)
- [Icon Felsefesi](#icon-felsefesi)
- [İkon Boyutları](#i̇kon-boyutları)
- [İkon Kalınlıkları](#i̇kon-kalınlıkları)
- [Boş Durum Tasarımı](#boş-durum-tasarımı)
- [Loading Tasarımları](#loading-tasarımları)
- [Skeleton Yapısı](#skeleton-yapısı)
- [Progress Yapısı](#progress-yapısı)
- [Bildirim Tasarımları](#bildirim-tasarımları)
- [Toast](#toast)
- [Snackbar](#snackbar)
- [Bottom Sheet](#bottom-sheet)
- [Modal](#modal)
- [Dialog](#dialog)
- [FAB Kullanımı](#fab-kullanımı)
- [Navigation Bar](#navigation-bar)
- [Tab Bar](#tab-bar)
- [Search Tasarımı](#search-tasarımı)
- [Harita Bileşenleri](#harita-bileşenleri)
- [Marker Sistemi](#marker-sistemi)
- [Cluster Yapısı](#cluster-yapısı)
- [Route Çizimleri](#route-çizimleri)
- [AI Kartları](#ai-kartları)
- [Seyahat Kartları](#seyahat-kartları)
- [Restoran Kartları](#restoran-kartları)
- [Etkinlik Kartları](#etkinlik-kartları)
- [Otel Kartları](#otel-kartları)
- [Fotoğraf Kullanımı](#fotoğraf-kullanımı)
- [Gradient Kullanımı](#gradient-kullanımı)
- [Renk Psikolojisi](#renk-psikolojisi)
- [Accent Renkleri](#accent-renkleri)
- [Success](#success)
- [Error](#error)
- [Warning](#warning)
- [Info](#info)
- [Animasyon Felsefesi](#animasyon-felsefesi)
- [Hareket Prensipleri](#hareket-prensipleri)
- [Micro Interaction](#micro-interaction)
- [Gesture Davranışları](#gesture-davranışları)
- [Haptic Feedback](#haptic-feedback)
- [Premium Detaylar](#premium-detaylar)
- [UX Kalite Standartları](#ux-kalite-standartları)
- [Görsel Tutarlılık Kuralları](#görsel-tutarlılık-kuralları)
- [Yapılmaması Gerekenler](#yapılmaması-gerekenler)
- [Apple vs Google Yaklaşımı](#apple-vs-google-yaklaşımı)
- [Airbnb vs Booking Yaklaşımı](#airbnb-vs-booking-yaklaşımı)
- [Material vs Cupertino Karşılaştırması](#material-vs-cupertino-karşılaştırması)
- [Belge İlişkileri ve Görsel Doğrulama Kaydı](#belge-i̇lişkileri-ve-görsel-doğrulama-kaydı)
- [Visual Language Review](#visual-language-review)
- [Revision Report](#revision-report)

## Belge Kapsamı ve Referans Sınırları

Bu belge Şamandıra'nın yalnız görsel tasarım dilini tanımlar.
Ürün amacı, bilgi mimarisi, ekran sorumluluğu, kullanıcı akışı ve karar otoritesi kabul edilmiş kaynaklarda kalır.
Mevcut ekranın bileşen sırasını değiştiren bir kompozisyon, yeni sayfa veya yeni navigasyon önerilmez.
Metin, tablo ve yazılı örnekler görsel kararların ifadesidir; ekran çizimi değildir.
Kod, Flutter, HTML, CSS, Figma, SVG, PNG, UI, mockup veya görsel varlık bu çalışmanın çıktısı değildir.
Bu incelemede mevcut Markdown belgesi yerinde revize edilir.
Kaynak belgelerdeki kabul ve öneri etiketleri tarihsel kayıt olarak aynen korunur.
Kullanıcının bu görevde referans gösterdiği kabul edilmiş belgeler esas alınır; bu belge ayrıca inceleme konusu olmaya devam eder.
Belgenin tamamlanması uygulama, kullanıcı araştırması veya erişilebilirlik uygunluk iddiası oluşturmaz.

### İstenen adların depodaki karşılıkları

Belgenin ilk hazırlanışında kullanılan İngilizce referans adları ile deponun numaralandırması birebir aynı değildir.
Aşağıdaki eşleme yeni belge veya yeniden adlandırma oluşturmaz.
Erişilebilirlik için bağımsız bir dosya bulunmadığında mevcut kabul edilmiş bölümler esas alınır.

| İstenen referans | Depodaki gerçek karşılık | Bu belgeye etkisi |
| --- | --- | --- |
| README.md | [Proje README](../../README.md) | Proje bağlamı ve doküman haritası |
| docs/ | [Dokümantasyon dizini](../README.md) ve altındaki kabul edilmiş belgeler | Belge yeri ve referans ilişkisi |
| 01-product-language.md | [02 Product Language](../00-product/02-product-language.md) | Terim ve durum anlamı |
| 02-information-architecture.md | [01 Bilgi Mimarisi](../00-product/01-bilgi-mimarisi.md) | Mevcut sayfa ve bilgi sırası |
| 03-decision-engine.md | [03 Karar Motoru](../00-product/03-karar-motoru.md) | Görselin uygunluk üretmemesi |
| 04-ai-knowledge-engine.md | [05 AI Bilgi Motoru](../04-ai/05-ai-bilgi-motoru.md) | AI, kanıt ve yayın sınırı |
| 05-system-architecture.md | [04 Sistem Mimarisi](../00-product/04-sistem-mimarisi.md) | Sunumun diğer sorumluluklardan ayrılması |
| 06-smart-route-engine.md | [06 Akıllı Rota Motoru](../00-product/06-akilli-rota-motoru.md) | Günlük plan ve değerlendirme ayrımı |
| 07-user-flows.md | [07 UX Karar Akışları](../02-ux/07-ux-karar-akislari.md) | Kontrol, kesinti ve geri dönüş |
| 08-design-principles.md | [08 Tasarım İlkeleri](./08-tasarim-ilkeleri.md) | Okunurluk ve kullanıcı iradesi |
| 09-design-system.md | [10 Design System](./10-design-system.md) | Mevcut görsel değer ve bileşen sözleşmeleri |
| 10-accessibility.md | 10 Design System §55–56; 07 ve 11 içindeki erişilebilirlik hükümleri | Bağımsız dosya varmış gibi gösterilmez |
| 11-ekran-mimarisi.md | [11 Ekran Mimarisi](./11-ekran-mimarisi.md) | Otuz mevcut ekran sözleşmesi korunur |
| Ek ürün referansı | [00 Ürün Felsefesi](../00-product/00-urun-felsefesi.md) | Kişinin doğru kararına yardım |
| Ek iş referansı | [09 Ürün Ekosistemi](../09-business/09-urun-ekosistemi.md) | Premium ve ücretsiz hakların ayrımı |

### Referans önceliği ve korunacak farklılıklar

Depo kökündeki AGENTS.md, kabul edilmiş docs ürün referanslarının tarihsel planlardan önce geldiğini açıklar.
Bu belge o mevcut otoriteyi uygular; yeni bir öncelik kuralı icat etmez.
Çelişmeyen marka varlığı kilitleri korunur.
Tarihsel dosya ile güncel kabul edilmiş sistem arasındaki fark kaynak dosyayı değiştirme talimatı değildir.

| Konu | Tarihsel kayıt | Kabul edilmiş güncel dayanak | Bu belgede işlem |
| --- | --- | --- | --- |
| Ürün paleti | plan/04 ve yon.md bordo, krem ve turuncu rol paleti | 10 §14 mineral yüzey ve yeşil eylem paleti | 10 değerleri aynen korunur; eski dosyalar değişmez |
| Font | Fraunces ve Sora ürün hiyerarşisi | 10 §9 sistem sans başlangıcı | Ürün metni sistem sans; kilitli logo varlığı yeniden dizilmez |
| Küçük etiket | Tarihsel 11 birim, büyük harf ve geniş aralık | 10 §9–13 okunur etiket ve caption | Eski küçük etiket kuralı yeni belgeye aktarılmaz |
| Radius | Tarihsel medya ve marka geometrileri | 10 §20 bileşen rol ölçeği | 0/4/8/12/16 tb rolleri korunur; logo geometrisi ayrı kalır |
| Skeleton | Tarihsel parlayan iskelet anlatısı | 10 B26 statik varsayılan | Yeni belge statik görünümü sürdürür |
| Manyetik öğe | Tarihsel hero ve CTA uygulama kaydı | 10 §19,47 kullanıcıyı izleyen hareket yasağı | Yeni belge manyetik davranış tanımlamaz; uygulama dosyasına dokunulmaz |
| Harita | Tarihsel atlas/hero sunumu | 01, 10 B31 ve 11 §31 yardımcı görünüm | Mevcut sonuç ve filtre otoritesi değişmez |
| Logo | K8 sabit bordo karo ve beyaz çizim | Güncel sistem yeni logo seçmez | Özgün varlığın renk, oran ve çizgisi korunur |
| Marker biçimi | yon.md §5.7 halka + nokta; jenerik damla yasağı | Güncel DS tek aile ister, yeni şekil seçmez | Çelişmeyen halka + nokta kilidi korunur |
| Puan ve sponsorluk | Tarihsel skor ve ticari vurgu anlatısı | 03, 05, 09, 10 puansız ve bağımsız karar sözleşmesi | Genel güven rozeti veya ticari görsel üstünlük üretilmez |
| Hero | yon-v2/v3 kapsamı sınırlı tarihsel kararlar | Bu görev ekran değiştirmeyi yasaklar | Hero yeniden tasarlanmaz; eski üretim mekanizması canlandırılmaz |
| Gezi kapsamı | Tarihsel çok günlük rota anlatıları | 06 ve 11 günlük kişisel plan | Seyahat kartı yeni çok günlük ürün açmaz |

### Görsel kararların statüsü

Devralınan ölçü, önceki kararı değiştirmeyen aynen kullanım anlamındadır.
Görsel uygulama ilkesi, devralınan rolün mevcut bileşen içinde nasıl tutarlı görünmesi gerektiğini açıklar.
İnceleme ölçütü, ileride değerlendirilecek koşuldur; gerçekleşmiş kullanıcı testi değildir.
Koşullu varyant, yalnız kabul edilmiş veri ve ekran bağlamı varsa uygulanabilir görsel sözleşmedir.
Otel ve etkinlik başlıkları yeni katalog, rezervasyon veya bilet akışı oluşturmaz.
FAB başlığının bulunması ürüne FAB ekleme kararı değildir.
Tab Bar başlığı yeni ana navigasyon ailesi üretmez.
“Harita odaklı” hedefi mevcut harita görünümünün kaliteli, okunur ve kullanılabilir olmasını ifade eder.
Harita aynı sonuç kümesinin yardımcı görünümü ve listeyle eşdeğer karar bilgisi olarak kalır.
“AI destekli” hedefi açıklamanın kapsamını görünür kılar; AI onay rozeti veya özel doğruluk sınıfı üretmez.
“Premium his” bütün kullanıcılar için işçilik hedefidir; ücretli hizmet hakkıyla karıştırılmaz.

### Ölçü ve anlatım sözlüğü

| Terim | Bu belgede anlamı | Yanlış yorum |
| --- | --- | --- |
| tb | 10 belgesindeki mantıksal tasarım referansı | Fiziksel ekran pikseli değildir |
| 8pt | 4 tabanlı mevcut ölçeğin sekizli ana ritmi | 4 ve 12 değerlerini kaldırmaz |
| Birincil | İlgili görevde tanımlı görsel rol | Yerin en iyi olduğu anlamına gelmez |
| Seçili | Kullanıcının açık seçimi | Uygun, gidildi veya doğrulandı değildir |
| Başarı | Teyit edilen işlemin kendi kapsamı | Genel yer güveni değildir |
| Kritik sınır | Kararı değiştirebilen mevcut bilgi | Küçük dipnota indirgenecek metadata değildir |
| Caption | İkincil görsel açıklama veya metadata rolü | Düşük kontrast izni değildir |
| Elevation | Etkileşim katmanı ilişkisi | Ticari veya kalite sırası değildir |
| Cupertino | Apple platform geleneği için kısa ad | Teknoloji veya framework seçimi değildir |
| İyi/kötü örnek | Varsayımsal sunum karşılaştırması | Gerçek yer, fiyat veya erişim beyanı değildir |

### Okuma ve sayım yöntemi

V01–V73 kimlikleri görsel konu bölümleridir.
Her konu beş izlenebilir tasarım ilkesi ve üç bölüm sonu öz eleştiri içerir.
V01 ifadesi metinde V1 biçiminde de gösterilebilir; kimlik sayısal olarak aynıdır.
Toplam tasarım ilkesi yalnız “İlke V...” kayıtları sayılarak hesaplanır.
Tablo sayısı Markdown sütun ayırıcı satırlarına göre hesaplanır.
Ana bölümler ikinci düzey başlıklardır; tek birinci düzey başlık belge adıdır. Görsel konu sayımı yalnız V1–V73 bölümlerini kapsar.
Visual Language Review, bölüm eleştirilerine ek kapsamlı sorgulama kaydıdır; sonundaki Revision Report bu editoryal incelemenin sonucunu kaydeder.
Satır sayısı dosyanın fiziksel satırlarıdır; yapay boş satır blokları veya yinelenen dolgu oluşturulmaz.
Her konu kendi gerekçe, bedel, durum ve iyi/kötü örneğiyle okunabilir tutulur.
Ortak erişim yükümlülükleri konular arasında yeniden hatırlatılabilir; bu tekrar farklı durum kapsamını açıklamalıdır.

### Bölüm sonu öz eleştiri

- **Öz eleştiri Ö0.1 — Referans önceliği yanlışlıkla yeni karar gibi okunabilir.**
  Eski ve güncel değerlerin yan yana kaydı bir geçiş uygulaması değildir; bu görev hiçbir kaynak veya ekranı dönüştürmez.

- **Öz eleştiri Ö0.2 — Çok uzun belge bakım yükü yaratır.**
  Sayfa hacmi kalite kanıtı değildir; rol kimlikleri ve kaynak eşlemeleri tutarsızlık bulmayı kolaylaştırmalıdır.

- **Öz eleştiri Ö0.3 — Koşullu bileşen adları özellik vaadi sanılabilir.**
  Otel, etkinlik ve FAB gibi başlıklarda mevcut ürün kapsamı açık kalmadıkça belge doğru yorumlanmış sayılmaz.

## Marka Kimliği

Bölüm kimliği: V1.
Dayanak: 00 Ürün Felsefesi; 02 Product Language; 10 Design System §1, 14; plan/00_brief_eki.md K8.
Şamandıra'nın kimliği, yer hakkında karar vermeyi kolaylaştıran sakin ve açık sunumdan doğar.
Bu bölüm marka adını, kabul edilmiş işareti, sloganı veya ürün konumlandırmasını yeniden seçmez.
Mevcut logo varlığı kendi kilitli renk ve oranlarıyla korunur; işlevsel ürün paleti 10 belgesinden gelir.

### Tasarım ilkeleri

#### İlke V1.1 — Kimliği içerikle taşımak

Karar: Yer adı ve açıklaması marka süsünden daha güçlü okunur.
Gerekçe: Gezginin aradığı bilgi kendi bağlamına uygun yerdir.
Sonuç: Marka özeni bilginin düzeninde hissedilir.
Bedel: Logo görünürlüğü tek başına büyütülerek hatırlanma artırılamaz.

#### İlke V1.2 — Kilitli işareti korumak

Karar: Logo çizgisi, bordo karosu ve oranları değiştirilmeden kullanılır.
Gerekçe: K8 marka varlığını sabitler; yeni görsel dil yeniden markalama yetkisi değildir.
Sonuç: Açık ve koyu temada aynı işaret tanınır.
Bedel: Ürün yeşiliyle renk birliği kurmak için logo yeniden boyanamaz.

#### İlke V1.3 — Marka rengini rolünden ayırmak

Karar: Logonun bordosu işlevsel hata rengi veya yeni CTA rengi yapılmaz.
Gerekçe: Varlık kimliği ile anlamsal renk farklı sorumluluklardır.
Sonuç: Bir hatanın görünümü marka ambleminden çıkarılmaz.
Bedel: İki renk ailesinin birlikte algısı ileride gerçek içerikle incelenmelidir.

#### İlke V1.4 — Turistik kimliği gerçek yerle kurmak

Karar: Fotoğrafı olan mevcut yüzeylerde yerin kendi karakteri görünür.
Gerekçe: Şehirler aynı uçak, valiz ve palmiye klişesiyle anlatılamaz.
Sonuç: Samsun dışındaki yerler de aynı dilin içinde kalır.
Bedel: İçerik üretimi ve gerçek fotoğraf bakımı gerekir.

#### İlke V1.5 — Premium özeni ortak tutmak

Karar: Temel tipografi, hedef boyutu ve okunabilirlik bütün hesap türlerinde aynıdır.
Gerekçe: Ücret farkı kullanıcıya gösterilen özenin tabanını değiştirmez.
Sonuç: Marka tutarlı hizmet kalitesi olarak okunur.
Bedel: Ücretli kapsam görsel üstünlük rozetiyle kolayca pazarlanamaz.

### Karar ve karşılaştırma tablosu

| Konu | Seçilen görsel karşılık | Elenen karşılık ve nedeni |
| --- | --- | --- |
| Marka adı | Şamandıra yazımını koru | Yeni lakap; mevcut ortak dili parçalar |
| Logo | Kilitli varlığın aynı oranı | Yeşile boyanmış yeniden çizim; K8'i değiştirir |
| Kimlik | Sakin metin, gerçek yer, ölçülü vurgu | Her başlıkta deniz metaforu; görevi zorlaştırır |
| Turistik his | Yerel ayrıntının dürüst temsili | Stok tatil kolajı; yere aitlik yanılsaması yaratır |
| Premium | Eşit temel işçilik | Altın taçla güven; ödeme ile doğruluğu karıştırır |

### Durum ve kullanım matrisi

| Koşul | Görsel uygulama sınırı | İnceleme odağı |
| --- | --- | --- |
| Logo küçük alanda | Mevcut varlık kullanım sınırına uy | İşaretin ayrıntıları bozuluyor mu? |
| Koyu tema | Logoyu ters renk filtresinden koru | Bordo kimliği değişiyor mu? |
| Fotoğrafsız yer | Metin kimliği güçlü kalır | Yer eksik ürün gibi mi görünüyor? |
| Yeni şehir | Aynı ürün dili ve gerçek yer bilgisi | Bölgeyi klişeyle mi temsil ediyor? |
| Premium olmayan hesap | Aynı okunabilir yüzeyler | Özen farkı üretilmiş mi? |

### İyi ve kötü örnekler

| Bağlam | İyi örnek | Kötü örnek |
| --- | --- | --- |
| Yer kimliği | Gerçek adı ve şube ayrımı belirgin | Logo büyürken şube adı üç noktayla kesilir |
| Marka hissi | Kontrol sınırları ve aralıklar tutarlı | Her kart başka süsleme taşır |
| Coğrafya | İzinli yer fotoğrafı kendi renginde | Her şehir aynı sahil fotoğrafıyla sunulur |

### Görsel inceleme

- Logonun kullanımında yeni renk, eğim veya gölge bulunmadığını incele.
- Marka metni ile yer kimliğinin aynı anda birbirini bastırmadığını değerlendir.
- Kullanıcıya gösterilen örneklerin gerçek kayıt iddiası taşımadığını kontrol et.

### Bölüm sonu öz eleştiri

- **Öz eleştiri Ö1.1 — Sadelik anonimleşebilir.**
  Kimlik algısı zayıfsa önce içerik dili ve tekrar eden ölçülerin tutarlılığı incelenmelidir; yeni logo üretilmez.

- **Öz eleştiri Ö1.2 — Bordo logo ile yeşil eylem yabancı görünebilir.**
  İki rolün birlikte görünümü gerçek tema koşullarında değerlendirilmelidir; bu belge eski kilitleri birleştirmez.

- **Öz eleştiri Ö1.3 — Turistik temsil dar kalabilir.**
  Yalnız manzara içeren örnekler yerel yaşamı dışlayabilir; fotoğraf seçimi kültürel çeşitlilik açısından sınanmalıdır.

## Tasarım Felsefesi

Bölüm kimliği: V2.
Dayanak: 00 Ürün Felsefesi; 08 Tasarım İlkeleri; 10 Design System §1.
Görsel tasarım, kişinin gerekçeyi, sınırı ve seçeneği birlikte okuyabilmesini destekler.
Sakinlik, önemli uyarının geri çekilmesi anlamına gelmez.
Bu belgedeki ölçüler karar motorunu, kabul edilmiş bilgi sırasını veya geri dönüş akışını değiştirmez.

### Tasarım ilkeleri

#### İlke V2.1 — Karar açıklığını öne almak

Karar: Gerekçe ve kararı değiştiren sınır aynı görsel grupta tutulur.
Gerekçe: Ayrık sunum olumlu iddiayı tek başına hatırlatabilir.
Sonuç: Kullanıcı ödünü açıklamayla birlikte tarar.
Bedel: Kartlar eşit yükseklikte görünmek zorunda kalmaz.

#### İlke V2.2 — Özeni ölçülebilir yapmak

Karar: Premium his hizalama, kontrast ve durum bütünlüğüyle değerlendirilir.
Gerekçe: Beğeni tek başına kullanılabilirliğin kanıtı değildir.
Sonuç: Ekip aynı kusuru aynı görsel kuralla tarif edebilir.
Bedel: Ölçüm kayıtları tasarım bakımının parçası olur.

#### İlke V2.3 — Sakinliği seçici kurmak

Karar: Dekor geri çekilirken görev başlığı ve gerekli kontrol sınırı belirgin kalır.
Gerekçe: Her şeyi soluklaştırmak hiyerarşi üretmez.
Sonuç: Düşük gürültüyle güçlü okunabilirlik birlikte sağlanır.
Bedel: Yalın yüzeyde küçük tutarsızlıklar daha görünür olur.

#### İlke V2.4 — Kontrol hissini görünür tutmak

Karar: Mevcut geri, vazgeçme ve düzeltme eylemleri görsel olarak erişilebilir kalır.
Gerekçe: Kişi yalnız ilerleme çağrısını fark ederse seçenek özgürlüğü zayıflar.
Sonuç: Baskın eylem görünürken alternatif yol anlaşılır.
Bedel: Tek düğmeli tanıtım estetiği her göreve uygulanamaz.

#### İlke V2.5 — Dürüst eksikliği kabul etmek

Karar: Bilgi yokluğu nötr, okunabilir bir sunumla karşılanır.
Gerekçe: Güven hissi sahte olumlu kanıta dönüştürülemez.
Sonuç: Eksik durum da tasarlanmış ve tamamlanmış görünür.
Bedel: Bazı kartlar görsel olarak daha az zengin kalır.

### Karar ve karşılaştırma tablosu

| Konu | Seçilen görsel karşılık | Elenen karşılık ve nedeni |
| --- | --- | --- |
| Sadelik | Gereksiz dekoru azaltma | Kritik sınırı kaldırma; anlam eksilir |
| Hız | Aynı grupta taranabilir gerekçe | Okuma gerektiren bilgiyi gizleme; yanlış karar hızlanır |
| Özgünlük | Puansız ve kapsamlı yer anlatımı | Yeni geri hareketi icat etme; öğrenme maliyeti artar |
| Kalite | Durumlar arasında tutarlı işçilik | Yalnız mutlu durum gösterisi; arızada kimlik çöker |
| Kontrol | Görünür alternatif eylem | Vazgeçmeyi silikleştirme; görsel baskı oluşur |

### Durum ve kullanım matrisi

| Koşul | Görsel uygulama sınırı | İnceleme odağı |
| --- | --- | --- |
| İlk kullanım | Somut görev metni ve tanınır kontrol | Eğitim olmadan ayrım okunuyor mu? |
| Seyrek kullanım | İkon yanında gerekli etiket | Önceki öğrenme varsayılıyor mu? |
| Kritik sınır | Gövde düzeyinde görünür açıklama | Süs tarafından bastırılıyor mu? |
| Eksik veri | Belirsizliğin açık metinsel görünümü | Sahte olumlu görünüm var mı? |
| Dar alan | Kabul edilmiş sırada serbest satır büyümesi | Anlam kesiliyor mu? |

### İyi ve kötü örnekler

| Bağlam | İyi örnek | Kötü örnek |
| --- | --- | --- |
| Gerekçe | Gölge bilgisi ve zaman kapsamı birlikte | Gölge var iddiası büyük, öğleden sonra sınırı dipnot |
| Düzeltme | Mevcut düzenleme eylemi okunur | Düzenleme yalnız görünmez hover alanında |
| Eksiklik | Doğrulanamayan özellik açıkça adlandırılır | Bilinmeyen alan yeşil onayla dolar |

### Görsel inceleme

- İlk taramada olumlu gerekçe kadar kritik sınırın da seçilebildiğini incele.
- Sakin yüzeyin kontrolü sıradan metin gibi göstermediğini kontrol et.
- Bu bölümün yeni görev, izin veya ödeme kararı üretmediğini doğrula.

### Bölüm sonu öz eleştiri

- **Öz eleştiri Ö2.1 — Açıklık uzunluğa dönüşebilir.**
  Her açıklama görünür olmak zorunda değildir; mevcut kritik ve ikincil bilgi ayrımı korunarak görsel yük incelenmelidir.

- **Öz eleştiri Ö2.2 — Ölçü standardı katılaşabilir.**
  Sayısal düzenin aynı görünmesine odaklanmak farklı dillerin okunabilirliğini gözden kaçırabilir.

- **Öz eleştiri Ö2.3 — Sakinlik aciliyeti azaltabilir.**
  Kritik durumun sıradan bilgiyle karıştığı örneklerde metin ve anlamsal işaret birlikte güçlendirilmelidir.

## Görsel İlkeler

Bölüm kimliği: V3.
Dayanak: 10 Design System §4–20, 55; 11 Ekran Mimarisi §36.
Görsel ilkeler aynı anlamın farklı bileşenlerde yeniden tanınmasını sağlar.
Ortaklık bütün yüzeylerin aynı büyüklükte, aynı yoğunlukta veya aynı katmanda görünmesini gerektirmez.
İlke kimlikleri sonraki görsel incelemelerde izlenebilir karar kayıtlarıdır.

### Tasarım ilkeleri

#### İlke V3.1 — Rol önceliği

Karar: Renk ve metin biçimi görünüş adına değil anlamsal rol adına seçilir.
Gerekçe: Aynı yeşil seçim, eylem ve başarıda farklı anlam taşır.
Sonuç: Görünüm değişse de rol ayrımı korunur.
Bedel: Değerlerin yanında kullanım bağlamı da belgelenir.

#### İlke V3.2 — Yakınlık disiplini

Karar: İlişkili açıklama kendi başlığından ilgisiz gruptan daha yakın durur.
Gerekçe: Boşluk bilginin aidiyetini sözsüz anlatır.
Sonuç: Tarama sırasında yanlış iddia eşleştirmesi azalır.
Bedel: Dekoratif eşit boşluk her yerde uygulanamaz.

#### İlke V3.3 — Sınırlı vurgu

Karar: Aynı görünür görevde en fazla üç eşzamanlı tipografik vurgu düzeyi korunur.
Gerekçe: Bütün öğeler öne çıkarsa hiçbiri öncelik taşımaz.
Sonuç: Görev, karar ve destek katı ayrışır.
Bedel: Her içerik sahibinin kendi vurgusunu ekleme özgürlüğü sınırlanır.

#### İlke V3.4 — İkinci anlam kanalı

Karar: Seçim ve durum metin veya tanımlı işaretle de gösterilir.
Gerekçe: Renk farklı ekran ve algı koşullarında kaybolabilir.
Sonuç: Gri ölçekte de durum yorumlanabilir.
Bedel: Küçük ekranda görünür etiket için alan gerekir.

#### İlke V3.5 — Ölçekle birlikte büyüme

Karar: Metin büyüdüğünde kutu ve açıklama alanı içerikle genişler.
Gerekçe: Sabit yükseklik kritik bilgiyi kesebilir.
Sonuç: Aynı içerik farklı kullanıcı ölçeklerinde kalır.
Bedel: Ekranlar eşit sayıda satır göstermeyebilir.

### Karar ve karşılaştırma tablosu

| Konu | Seçilen görsel karşılık | Elenen karşılık ve nedeni |
| --- | --- | --- |
| Hiyerarşi | Boyut, ağırlık ve aralık birlikte | Sadece renk; algı farkında çöker |
| Seçim | İşaret ve seçili durum metni | Yalnız dolgu; başarıyla karışır |
| Yakınlık | İddia–sınır 8–12 tb ilişkisi | Uyarıyı ayrı uzak kutu; bağ kopar |
| Ölçek | İçerik yüksekliği serbest | Kritik metni küçültme; erişim düşer |
| Tutarlılık | Ortak role bağlı değer | Her ekranda özel ton; sistem parçalanır |

### Durum ve kullanım matrisi

| Koşul | Görsel uygulama sınırı | İnceleme odağı |
| --- | --- | --- |
| Normal metin | Rol ölçeği başlangıcı | Hiyerarşi görünür mü? |
| Büyük metin | Satır ve kutu büyür | Kesilen anlam var mı? |
| Gri ölçek | Etiket ve işaret sürer | Seçim başarıdan ayrılıyor mu? |
| Koyu tema | Aynı rolün koyu karşılığı | Önem sırası değişiyor mu? |
| Harita zemini | Opak kontrol ve görünür odak | Kontrol harita ayrıntısında kayboluyor mu? |

### İyi ve kötü örnekler

| Bağlam | İyi örnek | Kötü örnek |
| --- | --- | --- |
| İki uyarı | Her uyarı ilgili iddianın yanında | Sayfanın sonunda toplu belirsizlik paragrafı |
| Seçili yer | Sabit konum, tanımlı seçili işaret | Büyüyüp liste sırasını bozan kart |
| Görünüm | Bütün caption'lar aynı okunur rol | Her kartta farklı solukluk |

### Görsel inceleme

- Bir rol için gerekçesiz yeni değer açılmadığını incele.
- Yalnız renk kaldırıldığında kritik anlamın korunup korunmadığını değerlendir.
- Ölçek büyümesinin kabul edilmiş bilgi sırasını değiştirmediğini denetle.

### Bölüm sonu öz eleştiri

- **Öz eleştiri Ö3.1 — Üç vurgu düzeyi yanlış sayılabilir.**
  Anlamsal başlık katlarıyla görsel vurgu katları karıştırılmamalı; incelemede görünür görev bütünü esas alınmalıdır.

- **Öz eleştiri Ö3.2 — Metinle tekrarlanan durum yük yaratabilir.**
  Her simgeye gereksiz tekrar yazmak yerine yalnız anlam için gerekli etiketi korumak gerekir.

- **Öz eleştiri Ö3.3 — Rol sayısı büyüyebilir.**
  Gerçek bağımsız anlamı olmayan yeni roller birikirse aynı karar farklı adlarla çoğalır.

## Tasarım Dili

Bölüm kimliği: V4.
Dayanak: 02 Product Language; 10 Design System §4, 14, 17, 53.
Görsel dil açık mineral yüzey, koyu metin, ölçülü yeşil eylem ve tutarlı çizgi ikonundan oluşur.
Yerin karakteri fotoğraf ve içerikten gelir; sistem her yeri kendi rengine dönüştürmez.
Bu tanım mevcut ekranların kompozisyonunu yeniden kuran bir sanat yönetimi talimatı değildir.

### Tasarım ilkeleri

#### İlke V4.1 — Mineral yüzey

Karar: Ana içerikte 10 belgesinin opak açık ve koyu yüzeyleri kullanılır.
Gerekçe: Öngörülebilir zemin metnin kontrastını yönetilebilir kılar.
Sonuç: Yüzeyler fotoğrafların yanında sakin kalır.
Bedel: Yoğun atmosfer efektlerine alan ayrılmaz.

#### İlke V4.2 — Koyu ve açık mürekkep

Karar: Tema içindeki birincil metin aynı kimlik ve karar rolünü taşır.
Gerekçe: Temaya göre başlık önemini değiştirmek zihinsel eşleşmeyi bozar.
Sonuç: Gece ve gündüz aynı bilgi taranır.
Bedel: Metin rengi yalnız estetik beğeniyle değiştirilemez.

#### İlke V4.3 — Ölçülü yeşil

Karar: Eylem yeşili sadece tanımlı eylem rolünde baskın kullanılır.
Gerekçe: Her ayrıntının yeşil olması kontrolün farkını azaltır.
Sonuç: CTA içerikten ayırt edilir.
Bedel: Yeni kategori rengi olarak yeşil çoğaltılamaz.

#### İlke V4.4 — Tek ikon ailesi

Karar: Çizgi, köşe ve optik ağırlık aynı ailede tutulur.
Gerekçe: Karışık ikon seti küçük boyutta hizayı ve anlamı dağıtır.
Sonuç: Araçlar tek ürüne ait görünür.
Bedel: Nadir bir simge için kolay bulunan başka stil alınamaz.

#### İlke V4.5 — Gerçek malzeme

Karar: Dijital yüzey mat ve düz; gerçek doku izinli fotoğrafın içindedir.
Gerekçe: Kâğıt gürültüsü ve yapay kabartma küçük metni zorlaştırabilir.
Sonuç: Turistik sıcaklık içeriği bozmadan hissedilir.
Bedel: Doku üzerinden hızlı marka farklılaşması kullanılamaz.

### Karar ve karşılaştırma tablosu

| Konu | Seçilen görsel karşılık | Elenen karşılık ve nedeni |
| --- | --- | --- |
| Yüzey | Düz, rolü belli ve opak | Sürekli cam; harita metni değişkenleşir |
| Renk | Tanımlı çiftler | Görselden rastgele renk çekme; anlam kayar |
| Tipografi | Sistem sans ve ortak hiyerarşi | Her konuya ayrı font; ritim kırılır |
| İkon | Tutarlı çizgi ailesi | Emoji ve farklı kütüphane karışımı; ağırlık tutmaz |
| Doku | Gerçek yerin kendi malzemesi | Dijital halat/kâğıt efekti; dekor baskınlaşır |

### Durum ve kullanım matrisi

| Koşul | Görsel uygulama sınırı | İnceleme odağı |
| --- | --- | --- |
| Yer ayrıntısı | Gövde ve sınır aynı okunur dilde | Fotoğraf ağırlığı dengeli mi? |
| AI açıklaması | Aynı ana yüzey ailesi | Sahte otorite parıltısı var mı? |
| Admin | Aynı metin ve durum rolleri | Yoğunluk kimliği parçalamış mı? |
| Premium | Aynı temel palet | Başarı rengi üyelik işaretine dönmüş mü? |
| Fotoğrafsız kart | Aynı metin kalitesi | Eksik fotoğraf sahte dokuyla örtülmüş mü? |

### İyi ve kötü örnekler

| Bağlam | İyi örnek | Kötü örnek |
| --- | --- | --- |
| AI kartı | Başlık ve kapsam açıklaması sakin | Mor neon çerçeveyle AI onaylı algısı |
| Kontrol | Tek çizgi ailesinde arama ve kapat | Arama ince, kapat kalın ve üç boyutlu |
| Yer atmosferi | Fotoğraf kendi doğal tonunda | Bütün fotoğraflara marka yeşili filtre |

### Görsel inceleme

- Değer değişikliğinin mevcut bir rol yerine görsel hevesle eklenmediğini kontrol et.
- İçerik türlerinin ayrı ürünler gibi görünmediğini karşılaştır.
- Dijital malzemenin gerçek yer koşullarıyla karışmadığını incele.

### Bölüm sonu öz eleştiri

- **Öz eleştiri Ö4.1 — Mat dil soğuk algılanabilir.**
  Bunun çözümü sıcaklık garantisi iddia etmek değil, gerçek içerik ve kullanıcı değerlendirmesiyle algıyı incelemektir.

- **Öz eleştiri Ö4.2 — Tek aile özel anlamı karşılamayabilir.**
  Yeni simge gerektiğinde aile uyumu kadar anlamın metinsel açıklaması da değerlendirilmelidir.

- **Öz eleştiri Ö4.3 — Renk disiplini esnekliği sınırlayabilir.**
  Yeni veri türünde anlam gerçekten farklıysa mevcut rolü zorlamak yerine ayrı görsel karar kaydı gerekir.

## Premium Hissi Nasıl Oluşuyor

Bölüm kimliği: V5.
Dayanak: 08 Tasarım İlkeleri; 09 Ürün Ekosistemi; 10 Design System §1, 57.
Premium his, ürünün bütün durumlarında görülen özen, denge ve öngörülebilirliktir.
Abonelik kapsamıyla görsel kalite algısı ayrı konulardır.
Bu bölüm ücretsiz kullanıcı için daha düşük işçilik veya daha az okunabilir görünüm tarif etmez.

### Tasarım ilkeleri

#### İlke V5.1 — Optik tutarlılık

Karar: İkon, metin ve sınırların hizası yalnız matematiksel kutuyla değil gözle de değerlendirilir.
Gerekçe: Farklı simgeler aynı kutuda farklı ağırlık hissi verebilir.
Sonuç: Küçük tekrarlar profesyonel bütünlük oluşturur.
Bedel: Optik istisnanın gerekçesi kaydedilmelidir.

#### İlke V5.2 — Durumlarda eşit işçilik

Karar: Loading, boş, hata ve offline görünümü ana içerikle aynı tipografiyi paylaşır.
Gerekçe: Kalite yalnız başarı ekranında varsa kesinti güveni zedeler.
Sonuç: Kullanıcı sorunu aynı ürün içinde anlayabilir.
Bedel: Durum kapsamı tasarım incelemesine ek yük getirir.

#### İlke V5.3 — Kararlı hedef

Karar: Metin veya görsel yüklenmesi mevcut kontrolün üzerine başka hedef getirmez.
Gerekçe: Kazara eylem öngörülebilirlik duygusunu bozar.
Sonuç: Tek elle kullanım daha sakin olur.
Bedel: Görsel alanı önceden ayırmak bazen geçici boşluk bırakır.

#### İlke V5.4 — İnceliği okunurlukla sınırlamak

Karar: İnce çizgi ve küçük metin gerekli sınırların yerine geçmez.
Gerekçe: Zarif görünen ayrıntı dış ışıkta kaybolabilir.
Sonuç: Özen farklı koşullarda da kalır.
Bedel: Masaüstü sunumda daha ağır görünen sınır gerekebilir.

#### İlke V5.5 — Gösterişten bağımsız değer

Karar: Premium açıklaması kabul edilmiş ek kolaylığı açık metinle taşır.
Gerekçe: Altın kaplama ve parıltı hizmet kapsamını açıklamaz.
Sonuç: Ücretli değer görsel belirsizlik yaratmadan anlaşılır.
Bedel: Satış anlatısı kısa yoldan lüks simgesine dayanamaz.

### Karar ve karşılaştırma tablosu

| Konu | Seçilen görsel karşılık | Elenen karşılık ve nedeni |
| --- | --- | --- |
| İşçilik | Sabit hiza ve anlamlı ritim | Rastgele animasyon; kalite yerine gürültü |
| Lüks algısı | Eksiksiz durum tasarımı | Her karta gölge; ilişki bulanıklaşır |
| Güven | Gerçek işlem sonucu | Erken onay; doğruluk hissi sahte |
| Özel kapsam | Somut ek kolaylık metni | Taçla üstün öneri; yetki karışır |
| Zarafet | Okunur caption ve sınır | Çok soluk 11 birim metin; dış ortamda kaybolur |

### Durum ve kullanım matrisi

| Koşul | Görsel uygulama sınırı | İnceleme odağı |
| --- | --- | --- |
| Hızlı açılış | Gereksiz giriş gösterisi yok | İçerik hazırken bekleniyor mu? |
| Yavaş görsel | Ayrılmış alan ve net metin | Hedef sıçrıyor mu? |
| Hata | Ana dilde sakin açıklama | Ham teknik metin sızıyor mu? |
| Büyük yazı | Dengeli büyüyen içerik | Premium görünüm uğruna kesiliyor mu? |
| Ücretsiz kullanım | Aynı temel görsel kalite | Eşitsiz özen var mı? |

### İyi ve kötü örnekler

| Bağlam | İyi örnek | Kötü örnek |
| --- | --- | --- |
| Kart | Başlık, sınır ve eylem tutarlı | Gölge kusursuzken yer adı kesilir |
| Bekleme | Gerçek aşama görünür ve sakin | Her işlemde sahte yüzde 99 |
| Üyelik | Kabul edilmiş kapsam okunabilir | Kilitli güven bilgisiyle yükseltme baskısı |

### Görsel inceleme

- Yalnız ideal içerik yerine uzun ad ve hata durumunu da karşılaştır.
- Fotoğrafı kaldırınca temel görsel kalitenin sürüp sürmediğini değerlendir.
- Özenin fiyat veya hesap durumuyla azalmadığını incele.

### Bölüm sonu öz eleştiri

- **Öz eleştiri Ö5.1 — Özen bütçesi pahalılaşabilir.**
  Nadir dekor ayrıntılarına harcanan zaman temel durumları geciktiriyorsa öncelik yanlış kurulmuştur.

- **Öz eleştiri Ö5.2 — Kararlılık boşluk bırakabilir.**
  Ayrılmış fotoğraf alanı uzun bekleyişte anlamsız bir boş levha gibi görünebilir; metnin bağımsız okunması incelenmelidir.

- **Öz eleştiri Ö5.3 — Premium sözcüğü beklentiyi yükseltir.**
  Görsel kalite iddiası gerçek performans ve veri bakımından koparsa sonuç yalnız iyi paketlenmiş eksiklik olur.

## Beyaz Alan Kullanımı

Bölüm kimliği: V6.
Dayanak: 10 Design System §5–8; 11 Ekran Mimarisi §36.
Beyaz alan, renginden bağımsız olarak öğeler arasındaki anlamlı boşluktur.
Koyu temadaki boşluk da aynı gruplama görevini üstlenir.
Sabit bir boş ekran yüzdesi hedeflenmez; mevcut bilgi gruplarının ilişkisi korunur.

### Tasarım ilkeleri

#### İlke V6.1 — Yakın açıklama

Karar: İddia ile kritik kapsamı S2–S3, yani 8–12 tb yakınlıkta tutulur.
Gerekçe: Sınır başka gruba ait sanılmamalıdır.
Sonuç: Olumlu ve sınırlayıcı bilgi aynı bakışta birleşir.
Bedel: Eşit aralıklı dekor düzeni bozulabilir.

#### İlke V6.2 — Grup arası nefes

Karar: Ayrı karar gruplarında S5, yani 24 tb başlangıç aralığı korunur.
Gerekçe: Daha büyük mesafe yeni birimin başladığını anlatır.
Sonuç: Kart ve form grupları daha kolay taranır.
Bedel: Kısa pencerede aynı anda daha az grup görünür.

#### İlke V6.3 — İç ve dış denge

Karar: Dar kartta 16, geniş kartta 24 tb iç boşluk kullanılır.
Gerekçe: Başlık ve metin yüzey kenarına yapışınca kart ilişkisi zayıflar.
Sonuç: Kontrol ve içerik düzenli nefes alır.
Bedel: İçeriği sığdırmak için kenar boşluğu sıfırlanamaz.

#### İlke V6.4 — Erişim alanını saymak

Karar: Görsel boşluk hesabına dokunma hedefinin görünmeyen alanı da katılır.
Gerekçe: Küçük ikonların hedefleri birbirine taşabilir.
Sonuç: Boş görünen alan kazara komşu eylem üretmez.
Bedel: İkonları gözle yakın dizmek her zaman mümkün olmaz.

#### İlke V6.5 — Dekordan tasarruf

Karar: Dar alanda önce dekoratif boşluk azalır; kritik metin aralığı korunur.
Gerekçe: Yer kazanma okunabilirliği bozmamalıdır.
Sonuç: Aynı karar bütünü küçük pencerede kalır.
Bedel: Geniş ekranın ferahlığı birebir taşınamaz.

### Karar ve karşılaştırma tablosu

| Konu | Seçilen görsel karşılık | Elenen karşılık ve nedeni |
| --- | --- | --- |
| İddia–sınır | 8–12 tb yakın grup | 48 tb uzaklık; anlam bağı kopar |
| Kart içi | 16 veya 24 tb | Rastgele her kenarda farklı boşluk; ritim kayar |
| Ana bölüm | 32 veya 48 tb ilgili rol | Her satır 48 tb; tarama parçalanır |
| Dokunma | Hedefler arası gerçek açıklık | Yalnız ikon kenarını ölçme; hedefler çakışır |
| Koyu tema | Aynı anlamsal boşluk | Koyu alanı doldurma; yoğunluk değişir |

### Durum ve kullanım matrisi

| Koşul | Görsel uygulama sınırı | İnceleme odağı |
| --- | --- | --- |
| Dar dikey | 16 tb dış boşluk referansı | Metin kontrol kenarına yapışıyor mu? |
| Geniş okuma | Okuma satırı sınırında merkezlenen alan | Paragraf gereksiz genişliyor mu? |
| Büyük metin | İçerik yüksekliği büyür | İddia ve sınır uzaklaşıyor mu? |
| Harita kontrolü | Kontrol çevresi güvenli ve ayrışmış | Atıf alanı örtülüyor mu? |
| Klavye açık | Mevcut eylemin görünür alanı korunur | Boşluk adına eylem kayboluyor mu? |

### İyi ve kötü örnekler

| Bağlam | İyi örnek | Kötü örnek |
| --- | --- | --- |
| Açıklama | Uyarı kendi iddiasının hemen altında | Uyarı eşit kart boyu için tabana itilir |
| Liste | Kartlar arasında düzenli 24 tb | Görsel yüksekliğine göre değişen tesadüfi boşluk |
| Alt kontrol | Hedef alanı güvenli alanla birlikte incelenir | İkon sığıyor diye sistem kenarına yapıştırılır |

### Görsel inceleme

- İç boşluğun dış grup aralığından daha baskın olup olmadığını incele.
- Görünmez hedef sınırlarının çakışmadığını doğrula.
- Boşluk azaltmanın bilgi gruplarını birleştirip birleştirmediğini değerlendir.

### Bölüm sonu öz eleştiri

- **Öz eleştiri Ö6.1 — Fazla nefes kaydırmayı uzatabilir.**
  Kısa kararlarda ferahlık hedefi toplam tarama çabasını artırıyorsa dekoratif alan gözden geçirilmelidir.

- **Öz eleştiri Ö6.2 — Sabit aralık her metne uymaz.**
  Çok uzun yer adında başlığın kapladığı doğal alanı yok saymak optik dengesizlik yaratabilir.

- **Öz eleştiri Ö6.3 — Görünmez hedefler unutulabilir.**
  Görsel denetim yalnız görünen şekillere bakarsa tek elle kullanım sorununu yakalayamaz.

## Grid Sistemi

Bölüm kimliği: V7.
Dayanak: 10 Design System §6–8; 11 Ekran Mimarisi §35–36.
Grid, mevcut bilgi mimarisinin hizalama aracıdır; ekran kurma veya yeni panel ekleme kararı değildir.
Dar, orta ve geniş alanlar kabul edilmiş 4, 8 ve 12 kolon referansını korur.
Kolon kullanımı mevcut ekranın içerik ve metin ölçeği koşullarına bağlıdır.

### Tasarım ilkeleri

#### İlke V7.1 — Dar grid

Karar: Dar görev için 4 kolon, 16 tb dış boşluk ve 16 tb oluk korunur.
Gerekçe: Az genişlikte tek okuma akışı daha istikrarlıdır.
Sonuç: Metin ve kontroller ortak başlangıç hattını paylaşır.
Bedel: Birden çok yardımcı parça yan yana sıkıştırılamaz.

#### İlke V7.2 — Orta grid

Karar: Orta görev için 8 kolon, 24 tb dış boşluk ve 24 tb oluk korunur.
Gerekçe: Artan alan ilişkili grupların hizasını destekler.
Sonuç: Mevcut iki bölüm yeterli alan bulduğunda düzenli görünür.
Bedel: Ekran büyüdü diye iki panel zorunlu olmaz.

#### İlke V7.3 — Geniş grid

Karar: Geniş görev için 12 kolon, 32 tb dış boşluk ve 24 tb oluk korunur.
Gerekçe: Ortak kolon hattı ana içerik ve izinli yardımcı alanı bağlar.
Sonuç: Geniş pencere rastgele boşluklar üretmez.
Bedel: Daha çok kolon daha çok öneri sunma gerekçesi değildir.

#### İlke V7.4 — Okuma genişliği

Karar: Uzun metin yaklaşık 60–70 karakter satır hedefinde, 75 üst sınır hedefiyle kalır.
Gerekçe: Çok uzun satırda bir sonraki satırın başlangıcını bulmak zorlaşır.
Sonuç: Geniş ekran okuma mesafesini gereksiz büyütmez.
Bedel: Kalan alanı içerikle doldurmak gerekmez.

#### İlke V7.5 — Görev kabı

Karar: Genel görev için 1280 tb, iç admin için 1600 tb başlangıç üst hedefleri korunur.
Gerekçe: İç operasyonun karşılaştırma ihtiyacı tüketici okumasından farklıdır.
Sonuç: Her yüzey kendi işine uygun genişlikte kalır.
Bedel: Sonsuz büyüyen ekranlarda boş kenarlar kalabilir.

### Karar ve karşılaştırma tablosu

| Konu | Seçilen görsel karşılık | Elenen karşılık ve nedeni |
| --- | --- | --- |
| Dar | 4 kolon ve tek ana akış | İki dar kart; gerekçe sıkışır |
| Orta | 8 kolon, içerik sığarsa ayrım | Sırf tablet diye çift panel; okunurluk azalır |
| Geniş | 12 kolon ve sınırlı görev kabı | Sınırsız satır; göz takibi zorlaşır |
| Sonuç listesi | Karşılaştırılabilir dikey düzen | Masonry; anlam karşılaştırması sıçrar |
| Kolon | Hizalama ilişkisi | Yeni sonuç sayısı; karar otoritesi aşılır |

### Durum ve kullanım matrisi

| Koşul | Görsel uygulama sınırı | İnceleme odağı |
| --- | --- | --- |
| 320–390 referans genişlik | Dar grid | Kritik alan yatay taşıyor mu? |
| 600–768 aralığı | Orta koşulları içerikle değerlendirilir | İki parça gerçekten sığıyor mu? |
| 1024 genişlik | 12 kolon izni | Ana 480 + yardımcı 320 + oluk 24 koşulu sağlanıyor mu? |
| 1440 ve üstü | Görev kabı büyümeyi sınırlar | Satır uzunluğu artıyor mu? |
| Büyük metin | Mevcut yeniden akış kuralı | Kolon sayısı uğruna içerik kesiliyor mu? |

### İyi ve kötü örnekler

| Bağlam | İyi örnek | Kötü örnek |
| --- | --- | --- |
| Karşılaştırma | Kart başlıkları aynı mantıksal hizada | Fotoğrafa göre zikzak başlıklar |
| Okuma | Paragraf metin genişliğinde kalır | Paragraf 12 kolonun tamamına yayılır |
| Yan panel | Yalnız sözleşmedeki yardımcı alan | Boş alanı doldurmak için yeni öneri paneli |

### Görsel inceleme

- Grid tarifinin mevcut ekran yerleşimine yeni alan eklemediğini kontrol et.
- Kolonlar yerine gerçek kullanılabilir kap genişliğini incele.
- Türkçe uzun adlar ve büyütülmüş metinle hizanın anlamı koruduğunu değerlendir.

### Bölüm sonu öz eleştiri

- **Öz eleştiri Ö7.1 — Kolon sayısı güven yanılsaması verebilir.**
  Bir yerleşimin 12 kolona oturması iyi okunduğunu kanıtlamaz; görev bütünlüğü ayrıca değerlendirilmelidir.

- **Öz eleştiri Ö7.2 — Admin genişliği gereğinden büyük olabilir.**
  1600 tb hedefi bütün tablolar için doldurulacak alan değildir; kanıt ilişkisi gerektirmiyorsa daha dar kullanım mümkündür.

- **Öz eleştiri Ö7.3 — Karakter sayısı alfabelere eşit davranmaz.**
  Farklı yazı sistemlerinde fiziksel satır ölçüsü ve okunurluk birlikte incelenmelidir.

## 8pt Grid

Bölüm kimliği: V8.
Dayanak: 10 Design System §5; mevcut S0–S8 boşluk ölçeği.
Bu başlık, kabul edilmiş dört birim tabanının üzerinde sekiz birimlik ana ritmi açıklar.
Yeni ve yalnız sekizin katlarına izin veren bir grid sistemine geçilmez.
Buradaki tb mantıksal tasarım birimidir; fiziksel piksel veya bütün platformlarda aynı fiziksel ölçü iddiası değildir.

### Tasarım ilkeleri

#### İlke V8.1 — Mevcut tabanı korumak

Karar: 0, 4, 8, 12, 16, 24, 32, 48, 64 tb ölçeği aynen sürer.
Gerekçe: Kullanıcının 8pt başlığı eski 4 tabanını kaldırma talimatı değildir.
Sonuç: Yakın gruplar ve ana ritim aynı sistemde kalır.
Bedel: Sistemi yalnız 8 çarpanlarıyla basitleştirmek mümkün olmaz.

#### İlke V8.2 — Sekizli ana ritim

Karar: 8,16,24,32,48,64 değerleri belirgin ilişki ve bölüm mesafelerinde kullanılır.
Gerekçe: Büyük aralıkların ortak ritmi dağınıklığı azaltır.
Sonuç: Ekranlar arası geçişte tanıdık yoğunluk oluşur.
Bedel: Her gerçek boşluk sekizin katı olmak zorunda değildir.

#### İlke V8.3 — Dörtlü yakın ilişki

Karar: 4 ve 12 tb değerleri yakın alt ilişkilerde korunur.
Gerekçe: Etiket ve açıklama ana grup kadar ayrılmamalıdır.
Sonuç: Mikro gruplama büyük ritmi bozmadan kurulur.
Bedel: Yanlış kullanılırsa alan fazla sıkılaşabilir.

#### İlke V8.4 — Optik istisna

Karar: 2 tb yalnız optik hizalama ve odak ayrımı için gerekçeli kalır.
Gerekçe: Çizim geometrisi her zaman kutu merkeziyle aynı görünmez.
Sonuç: İkonlar dengeli ve odak algılanabilir olur.
Bedel: 2 tb yeni genel aralık basamağına dönüştürülemez.

#### İlke V8.5 — Metni zorlamamak

Karar: Satır yüksekliği ve kullanıcı metin aralığı 8 katına zorlanmaz.
Gerekçe: Yazı metrikleri ve erişilebilirlik sayısal ızgaradan önce gelir.
Sonuç: Türkçe işaretler ve büyüyen satırlar kesilmez.
Bedel: Tüm yatay hatların aynı ritme oturması beklenemez.

### Karar ve karşılaştırma tablosu

| Konu | Seçilen görsel karşılık | Elenen karşılık ve nedeni |
| --- | --- | --- |
| Taban | 4 birim kabulü korunur | Yalnız 8; mevcut 12/4 ilişkilerini bozar |
| Ana ritim | 8 ve katları rolüne göre | Her aralığı 16 yapma; gruplar eşitlenir |
| Optik | 2 tb gerekçeli istisna | 2, 6, 10 yeni ölçek; bakım dağılır |
| Tipografi | Kabul edilmiş boyut/satır çifti | 13/20'yi 16/24 yapma; eski karar değişir |
| Birim | Mantıksal tasarım referansı | Fiziksel piksel; cihazlar arası yanlış eşitlik |

### Durum ve kullanım matrisi

| Koşul | Görsel uygulama sınırı | İnceleme odağı |
| --- | --- | --- |
| Etiket yakınlığı | 4 tb uygun rol sınırında | Hedefler yanlışlıkla sıkışıyor mu? |
| İkon–metin | 8 tb başlangıç | İkonla metin tek kontrol gibi mi okunuyor? |
| Yakın alt grup | 12 tb korunur | İlgili açıklama kopuyor mu? |
| Kart içi | 16 veya 24 tb | Kart kenarı ve içerik dengeli mi? |
| Kullanıcı satır aralığı | Kullanıcı tercihi öncelikli | Ritim adına kırpma yapılıyor mu? |

### İyi ve kötü örnekler

| Bağlam | İyi örnek | Kötü örnek |
| --- | --- | --- |
| 8pt yorumu | 8 ana ritim, 4 alt ilişki | Bütün değerleri 8'e yuvarlama |
| Odak | 2 kalınlık ve 2 ayrım rolü | 8pt için halkayı 8 kalınlaştırma |
| Caption | 13/20 rolü korunur | 13 tek sayı diye fontu küçültme |

### Görsel inceleme

- Mevcut S1 ve S3 değerlerinin yanlışlıkla sistemden çıkarılmadığını doğrula.
- Ölçülerin cihaz pikseli diye adlandırılmadığını incele.
- Her optik istisnanın amaç ve kapsamının yazıldığını kontrol et.

### Bölüm sonu öz eleştiri

- **Öz eleştiri Ö8.1 — Başlık yanlış anlaşılabilir.**
  8pt ifadesi tek taban sanılabilir; uygulanacak katalogda 4 tabanının açık görünmesi gerekir.

- **Öz eleştiri Ö8.2 — İstisnalar çoğalabilir.**
  Optik gerekçe adı altında her bileşene farklı aralık eklemek sistemin kontrolünü zayıflatır.

- **Öz eleştiri Ö8.3 — Ritim içeriği mekanikleştirebilir.**
  Doğal metin akışını sıkıştıran sayısal düzenleme varsa öncelik sırası ters kurulmuştur.

## Layout Kuralları

Bölüm kimliği: V9.
Dayanak: 10 Design System §6–8, 49; 11 Ekran Mimarisi §34–38.
Layout kuralları yalnız kabul edilmiş yerleşimin görsel bütünlüğünü tanımlar.
Mevcut ekran bölümleri, sırası, girişleri, çıkışları ve navigasyon sahipliği korunur.
Küçük ekran için yeni akış veya masaüstü için ek içerik portali üretilmez.

### Tasarım ilkeleri

#### İlke V9.1 — Mevcut sıraya bağlılık

Karar: Kimlik, kritik durum, gerekçe ve sınırın kabul edilmiş sırası görsel ağırlıkla desteklenir.
Gerekçe: Farklı boyut veya renk fiilen yeni okuma sırası kurabilir.
Sonuç: Mimari ile ilk bakıştaki hiyerarşi örtüşür.
Bedel: Fotoğraf estetiği gerekçeyle sınırın arasına yeni blok sokamaz.

#### İlke V9.2 — Ortak hizalama

Karar: Başlık, açıklama ve ilişkili eylem aynı mantıksal başlangıç çizgisine bağlanır.
Gerekçe: Dağınık başlangıçlar taramayı gereksiz yere uzatır.
Sonuç: Liste ve form birimleri öngörülebilir olur.
Bedel: Her öğeyi bağımsız ortalamak mümkün olmaz.

#### İlke V9.3 — Güvenli alan

Karar: Kenardan kenara haritada bile kontrol ve metnin güvenli alanı korunur.
Gerekçe: Sistem kenarı ve atıflar kullanılabilir alanı azaltır.
Sonuç: Eylem ve kaynak bilgisi görünür kalır.
Bedel: Haritanın kullanılabilir yüzeyi ham pencere kadar değildir.

#### İlke V9.4 — Yükseklik esnekliği

Karar: Uzun yer adı ve kritik açıklama yüzeyi büyütebilir.
Gerekçe: Eşit kart yüksekliği bilgi kesme gerekçesi olamaz.
Sonuç: Gerçek içerik görsel kalıbı kırpmadan taşınır.
Bedel: Liste satırları değişken yükseklikte olabilir.

#### İlke V9.5 — Sabit alanın sınırı

Karar: Mevcut yapışkan öğeler odaklı kontrolü veya kritik metni örtmez.
Gerekçe: Sabitliğin yön bulma faydası örtülen bilgiyle kaybolur.
Sonuç: Tek elle erişim ve okuma birlikte kalır.
Bedel: Kısa pencerede kabul edilmiş akışa katılma kuralı gerekebilir.

### Karar ve karşılaştırma tablosu

| Konu | Seçilen görsel karşılık | Elenen karşılık ve nedeni |
| --- | --- | --- |
| Düzen | Mevcut mimariye görsel tutarlılık | Yeni hero veya akış; görev dışı |
| Başlangıç | Mantıksal ortak kenar | Her satırı farklı merkezleme; tarama dağılır |
| Yükseklik | İçerikle büyüme | Eşit kart için kritik kesme; karar zarar görür |
| Harita | Güvenli kontrol yüzeyi | Atıf üstüne CTA; bilgi örtülür |
| Sabitlik | Odak ve içerik görünür | Sürekli alt çubukla metni kapatma; erişim azalır |

### Durum ve kullanım matrisi

| Koşul | Görsel uygulama sınırı | İnceleme odağı |
| --- | --- | --- |
| Uzun yer adı | Satır sarımı ve şube ayrımı | Yanlış yer eşleşmesi var mı? |
| Klavye açık | Etkin alan ve eylem görünür | Hedef klavye arkasında mı? |
| Yatay telefon | Kısa yüksekliğe mevcut uyarlama | Üst ve alt sabit alan içeriği tüketiyor mu? |
| RTL içerik | Mantıksal hizalar uyarlanır | Coğrafi işaret yanlış aynalanıyor mu? |
| Eşik çevresi | Mevcut dar/orta/geniş kuralları | Görev durumu sıçrıyor mu? |

### İyi ve kötü örnekler

| Bağlam | İyi örnek | Kötü örnek |
| --- | --- | --- |
| Yer başlığı | Gerçek ad sarılır, ilçe görünür | Metin tasarıma sığsın diye şube silinir |
| Alt eylem | Güvenli alan üzerinde okunur | Sistem hareket çizgisine değen düğme |
| Büyük ekran | İzinli yardımcı harita aynı kümede | Boş kenara yeni öneri listesi |

### Görsel inceleme

- Her görsel kararın hangi mevcut ekran sözleşmesine uygulandığını incele.
- Taşmayı metin azaltarak çözme alışkanlığı bulunmadığını kontrol et.
- Sabit yüzeylerin odakla ilişkisini dar ve kısa pencerede değerlendir.

### Bölüm sonu öz eleştiri

- **Öz eleştiri Ö9.1 — Görsel hizalama gizli yeniden sıralama olabilir.**
  Büyük fotoğraf veya vurgu, içerik sırası değişmese bile ilk okunan bilgiyi değiştirebilir.

- **Öz eleştiri Ö9.2 — Uyarlama önerileri kapsamı aşabilir.**
  Bu belge yalnız mevcut yeniden akış kurallarını görünür kılar; yeni alternatif yerleşim kararı burada verilmez.

- **Öz eleştiri Ö9.3 — Değişken yükseklik karşılaştırmayı zorlaştırabilir.**
  Kritik bilgiyi kesmeden başlık ve etiket hizasının taramayı destekleyip desteklemediği ayrıca sınanmalıdır.

## Kart Tasarımları

Bölüm kimliği: V10.
Dayanak: 10 Design System B02–B04, §17–20; 11 Ekran Mimarisi E04,E07.
Kart, bağımsız bir karar biriminin görsel sınırıdır.
Yer ve Rota kartlarının kabul edilmiş anatomisi korunur; bu bölüm yeni kart kompozisyonu çizmez.
Her paragrafı ayrı karta dönüştürmek yerine mevcut açık okuma alanları korunur.

### Tasarım ilkeleri

#### İlke V10.1 — Düz temel

Karar: Sıradan kart E0 düzeyinde ve varsayılan gölgesizdir.
Gerekçe: Kartın sınırı öneri kalitesi veya önem basamağı değildir.
Sonuç: Yerler arasında yapay lüks sıralaması oluşmaz.
Bedel: Yüzey ayrımı için doğru boşluk ve sınır gerekir.

#### İlke V10.2 — On iki radius

Karar: Yer ve Rota kartı 12 tb radius kullanır.
Gerekçe: Ortak köşe dili aynı karar ailesini tanımlar.
Sonuç: Tür değişse de ürün aidiyeti korunur.
Bedel: Otel veya AI için keyfî büyük köşe açılamaz.

#### İlke V10.3 — Tutarlı içerik payı

Karar: Dar kart 16, geniş kart 24 tb iç boşluk kullanır.
Gerekçe: Metin ve kontrolün kenara olan mesafesi karar grubu hissini destekler.
Sonuç: Kartlar fotoğraf durumundan bağımsız tutarlı görünür.
Bedel: Uzun içerik daha yüksek kart gerektirebilir.

#### İlke V10.4 — Seçimin açıklığı

Karar: Seçili kart işaret ve seçim rolüyle ayrılır; yerinden yükselmez.
Gerekçe: Yükselen kart karşılaştırma hizasını bozabilir.
Sonuç: Kullanıcı seçimini bilgi sırası değişmeden görür.
Bedel: Dramatik seçili animasyonu kullanılmaz.

#### İlke V10.5 — Kritik metin bütünlüğü

Karar: Yer kimliği ve gerekli sınır sabit satır sınırıyla kesilmez.
Gerekçe: Benzer adlı yerlerde kesilen ayrıntı yanlış seçime yol açabilir.
Sonuç: Gerçek yer ve kapsam görünür kalır.
Bedel: Fotoğraflı vitrinlerde mekanik eşitlik sağlanamayabilir.

### Karar ve karşılaştırma tablosu

| Konu | Seçilen görsel karşılık | Elenen karşılık ve nedeni |
| --- | --- | --- |
| Sınır | Yüzey farkı ve uygun ayırıcı | Her karta yoğun gölge; yapay katman |
| Köşe | 12 tb ortak rol | Her kategoride farklı radius; dil parçalanır |
| Seçim | Sabit hiza ve tanımlı işaret | Büyüyüp komşuyu itme; karşılaştırma bozulur |
| Metin | Gerekli içerik serbest sarılır | İki satır zorlaması; sınır kaybolur |
| Fotoğraf yokluğu | Metin kartının aynı özeni | Sahte yer görseli; kanıt izlenimi yanlış |

### Durum ve kullanım matrisi

| Koşul | Görsel uygulama sınırı | İnceleme odağı |
| --- | --- | --- |
| Normal | Ana yüzey, 12 radius, E0 | Karar birimi ayırt ediliyor mu? |
| Seçili | Seçim rolü ve açık işaret | Başarı veya uygunluk sanılıyor mu? |
| Odaklı | 2 tb halka ve 2 tb ayrım | Halka kart kapsayıcısında kesiliyor mu? |
| Kritik durum | İlgili gövde metni görünür | Fotoğraf durumu bastırıyor mu? |
| Eksik içerik | Dürüst, aynı ailede görünüm | Eksik bilgi süsle dolduruluyor mu? |

### İyi ve kötü örnekler

| Bağlam | İyi örnek | Kötü örnek |
| --- | --- | --- |
| Rota kartı | Günlük plan özeti aynı yüzeyde | Üç boyutlu bilet formuyla tur satışı algısı |
| Yer kartı | Ad, gerekçe ve sınır birlikte | Gerekçe ön yüzde, uyarı gizli arka yüzde |
| Seçim | İşaret görünür, kart sabit | Manyetik hareketle imleci kovalayan kart |

### Görsel inceleme

- Kartın içerik sırasının B03/B04 ile aynı kaldığını kontrol et.
- Gölge, radius veya fotoğrafın ticari ayrıcalık üretmediğini incele.
- İç içe yüzeylerin sayfa–kart–iç grup sınırını aşmadığını değerlendir.

### Bölüm sonu öz eleştiri

- **Öz eleştiri Ö10.1 — Düz kart zeminden ayrılmayabilir.**
  Özellikle koyu temada gölge eklemekten önce yüzey farkı ve gerekli sınırın algısı incelenmelidir.

- **Öz eleştiri Ö10.2 — Tek kart ailesi içerik farkını örtebilir.**
  Restoran ve rota aynı anatomiyi paylaşmaz; ortak temel onların kabul edilmiş bilgi farkını silemez.

- **Öz eleştiri Ö10.3 — Serbest yükseklik ritmi zayıflatabilir.**
  Çözüm kritik bilgiyi kesmek değil, aynı görevde etiket ve aralıkların tutarlı kalmasını sağlamaktır.

## Radius Sistemi

Bölüm kimliği: V11.
Dayanak: 10 Design System §20; plan/00_brief_eki.md K8 logo kilidi.
Köşe yarıçapı aynı göreve ait yüzeylerin ailesini tanımlar.
Kabul edilmiş ölçek 0, 4, 8, 12, 16 tb ve sınırlı tam yuvarlak kullanımıdır.
Logonun kendi geometrisi bu bileşen ölçeğine uyarlanmaz.

### Tasarım ilkeleri

#### İlke V11.1 — Sınırlı ölçek

Karar: Yalnız mevcut 0, 4, 8, 12, 16 tb roller kullanılır.
Gerekçe: Kontrolsüz ara değerler bileşen akrabalığını zayıflatır.
Sonuç: Aynı rol her yüzeyde tanınır.
Bedel: Tek kartın fotoğrafına göre yeni köşe icat edilemez.

#### İlke V11.2 — Kontrol ailesi

Karar: Buton, input ve menü 8 tb radius paylaşır.
Gerekçe: Bu nesneler etkileşim aracı olarak ortak görünmelidir.
Sonuç: Kontrol yüzeyi içerik kartından ayrılır.
Bedel: Platformda görünür optik farklar ayrıca incelenir.

#### İlke V11.3 — Kart ailesi

Karar: Yer ve Rota kartı 12 tb radius kullanır.
Gerekçe: Karar biriminin kapsayıcı sınırı kontrol köşesinden ayrılır.
Sonuç: Tür değişiminde ortak karakter sürer.
Bedel: Kategoriye göre lüks köşe varyantı açılamaz.

#### İlke V11.4 — Geçici yüzey

Karar: Modal ve bağımsız sheet 16 tb radius kullanır.
Gerekçe: Üst görev yüzeyi daha geniş bir kapsayıcıdır.
Sonuç: Katman rolü köşe ve yüzeyle birlikte anlaşılır.
Bedel: Tam ekran sheet cihaz çerçevesi için körlemesine kırpılmaz.

#### İlke V11.5 — Tam yuvarlak sınırı

Karar: Chip, küçük durum işareti ve gerçek dairesel kontrolde tam yuvarlak korunur.
Gerekçe: Her şeyi kapsül yapmak içerik ve eylem ayrımını siler.
Sonuç: Kısa seçim birimi tanınabilir kalır.
Bedel: Uzun butonlar kapsül modasına göre değiştirilemez.

### Karar ve karşılaştırma tablosu

| Konu | Seçilen görsel karşılık | Elenen karşılık ve nedeni |
| --- | --- | --- |
| Satır | 0–4 tb | Her satıra 16; içerik kartlaşır |
| Kontrol | 8 tb | Her boyuta başka radius; aile kopar |
| Kart | 12 tb | Premium kart 24; eski rol değişir |
| Sheet | 16 tb bağımsız yüzey | Cihaz köşesini taklit etme; içerik kırpılabilir |
| Logo | Kilitli özgün oran | Kart radiusuna uydurma; marka varlığı bozulur |

### Durum ve kullanım matrisi

| Koşul | Görsel uygulama sınırı | İnceleme odağı |
| --- | --- | --- |
| İç fotoğraf | Dış kart sınırından taşmaz | İç/dış köşe optik ilişkisi |
| Büyük metin | Köşe metin alanını kesmez | İç kenarda daralma |
| Odak | Halka yarıçapı sınırı izler | Köşede kırpılan halka |
| Tam ekran yüzey | Mevcut platform çerçevesi korunur | Gereksiz iç kırpma |
| Küçük chip | Etiket ve hedef alanı korunur | Yuvarlama nedeniyle metin sıkışması |

### İyi ve kötü örnekler

| Bağlam | İyi örnek | Kötü örnek |
| --- | --- | --- |
| Yer kartı | 12 tb aynı ailede | Her fotoğraf farklı köşede |
| Buton | 8 tb ve yeterli iç alan | Kapsül köşesi uzun etiketi daraltır |
| Logo | Orijinal bordo karo | Yeni yuvarlak maskede ayrıntısı kesilmiş logo |

### Görsel inceleme

- İç köşenin dış köşeden görsel olarak taşmadığını incele.
- Radius seçiminin uygunluk veya abonelik göstergesi olmadığını kontrol et.
- Tam yuvarlak kullanımın izinli nesne türünde kaldığını doğrula.

### Bölüm sonu öz eleştiri

- **Öz eleştiri Ö11.1 — Az radius rolü sert görünebilir.**
  Farklı ölçeklerde optik algı incelenmeli; rolün sayısal tutarlılığı tek kabul kanıtı sayılmamalıdır.

- **Öz eleştiri Ö11.2 — İç fotoğraf uyumu otomatik değildir.**
  Kart boşluğuna göre köşe ilişkisi değişir; her fotoğrafı aynı kırpma maskesine zorlamak doğru değildir.

- **Öz eleştiri Ö11.3 — Platform görünümü ayrışabilir.**
  Yerel sistem kontrolü farklı görünürse mevcut kanal uyarlaması sınırında değerlendirilmelidir; bu belge yeni native stil seçmez.

## Elevation

Bölüm kimliği: V12.
Dayanak: 10 Design System §17–18; B19–B24.
Elevation etkileşim katmanının görsel ayrımıdır.
E0–E4 sırası teknik yığınlama değeri veya öneri kalitesi değildir.
Mevcut tek etkin modal ve odak sözleşmesi aynen sürer.

### Tasarım ilkeleri

#### İlke V12.1 — Düz içerik

Karar: Sayfa, sıradan kart ve düz içerik E0 kalır.
Gerekçe: Kalıcı bilgiye gereksiz yükseklik vermek katman dilini tüketir.
Sonuç: Geçici yüzey gerektiğinde daha kolay ayrılır.
Bedel: Kartların seçimi yükseklikle gösterilemez.

#### İlke V12.2 — Bağlamsal araç

Karar: Yapışkan görev başlığı ve harita kontrolü E1 rolündedir.
Gerekçe: Bu araçlar içerikle ilişkili kalırken üstte okunmalıdır.
Sonuç: Kontrol bağımsız yeni görev sanılmaz.
Bedel: Araç içeriğin odağını örtemez.

#### İlke V12.3 — Açılır yardımcı

Karar: Menü ve modal olmayan yardımcı panel E2 rolünü taşır.
Gerekçe: Açan kontrolle bağ sürmelidir.
Sonuç: Geçici seçim alanının kaynağı anlaşılır.
Bedel: Büyük gölgeyle gerçek modal izlenimi verilemez.

#### İlke V12.4 — Etkin modal

Karar: Gerçek modal ve modal sheet E3 rolündedir.
Gerekçe: Arka görevle etkileşim ilişkisi burada farklıdır.
Sonuç: Görsel ayrım kabul edilmiş odak sınırını destekler.
Bedel: İkinci bağımsız modal katmanı eklenemez.

#### İlke V12.5 — Göreve bağlı bildirim

Karar: E4 bildirim etkin görevin güvenli alanına bağlıdır.
Gerekçe: İlgisiz yüzey üstünde uyarı göstermek bağlamı bozar.
Sonuç: Bildirim kaynağı ve ilgili eylem birlikte anlaşılır.
Bedel: E4 bütün katmanların üstüne sınırsız çıkış izni değildir.

### Karar ve karşılaştırma tablosu

| Konu | Seçilen görsel karşılık | Elenen karşılık ve nedeni |
| --- | --- | --- |
| E0 | Sayfa ve sıradan kart | Önerilen yere ekstra yükseklik; görsel sıralama |
| E1 | Görev aracı | İçeriği örten sürekli plaka; erişim kaybı |
| E2 | Kontrole bağlı açılır alan | Modal kadar güçlü perde; yanlış görev algısı |
| E3 | Tek modal görev | İç içe bağımsız modallar; odak belirsizliği |
| E4 | Etkin göreve ait bildirim | Her ekran üstünde olay yağmuru; bağlam kaybı |

### Durum ve kullanım matrisi

| Koşul | Görsel uygulama sınırı | İnceleme odağı |
| --- | --- | --- |
| Menü açık | Kaynağı görünür bağlam | Menü hangi eylemden açıldı? |
| Modal açık | Üst yüzey ve arka ayrımı | Arka görev yanlış etkin görünüyor mu? |
| Harita kontrolü | E1 opak zemin | Yer işaretiyle karışıyor mu? |
| Koyu tema | Yüzey tonu ve sınır | Gölge kaybolunca katman sürüyor mu? |
| Zorlanmış renk | Sistem sınırları korunur | Katman sadece tona mı bağlı? |

### İyi ve kötü örnekler

| Bağlam | İyi örnek | Kötü örnek |
| --- | --- | --- |
| Seçili yer | E0, seçim işareti belirgin | E3 gibi yüzen tek yer kartı |
| Menü | Açan kontrolün yakınında bağlı görünüm | Tüm arka planı karartıp modal sanılması |
| Bildirim | Etkin sheet içinde uygun alanda | Kapat düğmesini örten toast |

### Görsel inceleme

- Yüksekliğin ticari önem veya yer kalitesi gibi okunmadığını değerlendir.
- Aktif katmanların sayısını mevcut sözleşmeyle karşılaştır.
- Gölgesiz durumda sınır ve görev ilişkisinin kaldığını incele.

### Bölüm sonu öz eleştiri

- **Öz eleştiri Ö12.1 — Beş rol karmaşıklaşabilir.**
  Her bileşene ayrı görsel yükseklik zorunlu değildir; rol ayrımı gereksiz efekt sayısını artırmamalıdır.

- **Öz eleştiri Ö12.2 — Ton farkı her ekran için yetmeyebilir.**
  Güneş altında veya düşük kaliteli ekranda aynı katman daha güçlü sınır gerektirebilir.

- **Öz eleştiri Ö12.3 — Bildirim en üst rol sanılabilir.**
  E4'ün bağlamsal sınırı unutulursa mevcut modalın kontrolünü kapatma riski doğar.

## Shadow Sistemi

Bölüm kimliği: V13.
Dayanak: 10 Design System §19; §55 odak ve sınır.
Gölge, geçici yüzeyin ayrılmasına yardımcı olan ikincil ipucudur.
Varsayılan sıradan kart gölgesizdir.
Yakın ve geçici katman gölgeleri kaynak belgedeki başlangıç aralıklarını korur.

### Tasarım ilkeleri

#### İlke V13.1 — Gölgesiz başlangıç

Karar: Sıradan kartta gölge kullanılmaz.
Gerekçe: Yüzey farkı ve boşluk aynı işi daha düşük gürültüyle yapabilir.
Sonuç: Liste sakin ve karşılaştırılabilir kalır.
Bedel: Yetersiz sınır gölge olmadan daha görünür kusurdur.

#### İlke V13.2 — Yakın rol

Karar: Yakın gölgede yaklaşık 2 tb düşey uzaklık ve 8 tb bulanıklık referansı korunur.
Gerekçe: Küçük ayrım kontrolün içerik üstündeki ilişkisini gösterebilir.
Sonuç: Araç yüzeyi sayfadan kopmadan anlaşılır.
Bedel: Koyuluk gerçek zeminle optik olarak sınanmalıdır.

#### İlke V13.3 — Geçici katman rolü

Karar: Geçici gölgede yaklaşık 8 tb uzaklık ve 24 tb bulanıklık referansı korunur.
Gerekçe: Daha geniş görev yüzeyi komşu içerikten ayrılmalıdır.
Sonuç: Katman ilişkisi daha okunur hale gelir.
Bedel: Geniş blur maliyeti ve koyu halo riski vardır.

#### İlke V13.4 — Koyu tema ayrımı

Karar: Koyu temada gölgeyi karartmak yerine üst yüzey ve sınır esas alınır.
Gerekçe: Karanlık zemindeki daha koyu alan yeterli ayrım vermez.
Sonuç: Yükseklik rolü gece de anlaşılır.
Bedel: Açık temanın gölgesi birebir kopyalanamaz.

#### İlke V13.5 — İşlevi gölgeye bağlamamak

Karar: Kontrol sınırı ve odak gölgeden bağımsız okunur.
Gerekçe: Zorlanmış renkler ve bazı görüntü koşulları gölgeyi kaldırabilir.
Sonuç: Temel görev görsel efekt olmadan sürer.
Bedel: Gölge tek başına seçili veya basılı durum olamaz.

### Karar ve karşılaştırma tablosu

| Konu | Seçilen görsel karşılık | Elenen karşılık ve nedeni |
| --- | --- | --- |
| Kart | Yok | Sürekli kabartma; dekor artar |
| Yakın | 2/8 tb referans ilişkisi | Büyük ışık halesi; yüzey kopar |
| Geçici | 8/24 tb kontrollü | Birden çok yönlü gölge; malzeme belirsiz |
| Koyu | Ton ve sınır ağırlıklı | Daha siyah blur; ayrım oluşmaz |
| Odak | Tanımlı halka | Yalnız gölge; klavye izi kaybolur |

### Durum ve kullanım matrisi

| Koşul | Görsel uygulama sınırı | İnceleme odağı |
| --- | --- | --- |
| Açık ana yüzey | Hafif ve ortak ışık yönü | Kenarın kirli görünmesi |
| Koyu üst yüzey | Ton farkı, gerekli sınır | Katmanların birleşmesi |
| Harita üstü | Opak araç, gerekirse yakın rol | Harita çizgilerinin halo sanılması |
| Yüksek kontrast | Gölge kaybolsa da sınır | Eylemin algılanabilirliği |
| Hareket | Geniş hareketli blur kullanılmaz | Düşük cihazda görsel maliyet |

### İyi ve kötü örnekler

| Bağlam | İyi örnek | Kötü örnek |
| --- | --- | --- |
| Kart listesi | Yüzeyler aralıkla ayrılır | Her kart farklı yükseklikte gölge |
| Sheet | Tek ortak katman gölgesi | Çok katlı parlak kenar ve siyah halo |
| Klavye odağı | Kesintisiz görünür halka | Gölge büyüyor fakat odak belli değil |

### Görsel inceleme

- Her gölgenin yakın veya geçici rolüyle açıklanabildiğini incele.
- Gölge olmadan kontrol sınırının görünürlüğünü değerlendir.
- Yayılma ve ışık yönünün bileşenler arasında tutarlı kaldığını kontrol et.

### Bölüm sonu öz eleştiri

- **Öz eleştiri Ö13.1 — Sayısal blur görünüşü garanti etmez.**
  İki platformun aynı bulanıklık sayısını farklı işlemesi mümkündür; optik inceleme gereklidir.

- **Öz eleştiri Ö13.2 — Düşük koyuluk aşırı silik kalabilir.**
  Gölgeyi artırmak yerine yüzey ve sınır çözümünün yeterliliği önce değerlendirilmelidir.

- **Öz eleştiri Ö13.3 — Mat görünüm derinliği azaltabilir.**
  Kullanıcı açılır alanı fark edemiyorsa mevcut katman dilinin başka ipuçlarıyla desteklenmesi gerekir.

## Cam Efekti

Bölüm kimliği: V14.
Dayanak: 10 Design System §14, 17, 19; plan/tasarim/yon.md §1.5.
Şamandıra'nın karar yüzeylerinde cam efekti varsayılan değildir.
Eski görsel yönün glassmorphism yasağına ve güncel Design System'in opak yüzey tercihine uyulur.
Apple'ın malzeme yaklaşımı burada bir öğrenme kaynağıdır; ürüne cam kaplama ekleme yetkisi değildir.

### Tasarım ilkeleri

#### İlke V14.1 — Opak karar zemini

Karar: Gerekçe, kritik sınır ve form bilgisi opak yüzeyde kalır.
Gerekçe: Alttaki fotoğraf ve harita değişince saydam metnin kontrastı değişir.
Sonuç: Okunabilirlik içerik sahnesinden bağımsız yönetilir.
Bedel: Camın görsel hafifliği kullanılmaz.

#### İlke V14.2 — Harita aracı ayrımı

Karar: Mevcut harita kontrolleri öngörülebilir opak zemin taşır.
Gerekçe: Yol, etiket ve marker yoğunluğu kontrolün arkasında değişkendir.
Sonuç: Kontrol haritadan ayrılır.
Bedel: Haritanın kontrol altındaki küçük bölümü örtülür.

#### İlke V14.3 — Platform malzemesinin sınırı

Karar: İşletim sisteminin kendi yüzeyi ürün içine özel cam katmanı kopyalama gerekçesi olmaz.
Gerekçe: Yerel kabuk ile ürünün bilgi yüzeyi ayrı sorumluluklardır.
Sonuç: Mevcut kanal sözleşmesi korunur.
Bedel: Tam görsel benzerlik hedefinden vazgeçilir.

#### İlke V14.4 — Saydamlığın anlamsızlığı

Karar: Saydamlık güven, AI yeteneği veya Premium değeri göstermez.
Gerekçe: Parlak malzeme veri doğruluğuna dair kanıt değildir.
Sonuç: Bilgi otoritesi görsel efektle büyütülmez.
Bedel: AI kartı özel parlak vitrinle ayrışamaz.

#### İlke V14.5 — Efektsiz tam karşılık

Karar: Bütün bilgi ve katman ilişkisi efekt olmadan anlaşılır kalır.
Gerekçe: Malzeme desteği veya erişilebilirlik tercihi değişebilir.
Sonuç: Daha sade görünüm tam ürün kalitesini taşır.
Bedel: Efekt odaklı marka iddiası kurulamaz.

### Karar ve karşılaştırma tablosu

| Konu | Seçilen görsel karşılık | Elenen karşılık ve nedeni |
| --- | --- | --- |
| Karar kartı | Opak ana yüzey | Cam; arka içerik metni etkiler |
| Harita aracı | Opak ve kontrastlı | Saydam baloncuk; yol etiketiyle çakışır |
| AI | Ortak kart dili | Işıltılı cam; sahte zekâ otoritesi |
| Premium | Aynı okunabilir zemin | Ücretliye kristal çerçeve; kalite ayrışır |
| Platform | Mevcut yerel kabuğa saygı | Her bileşeni Apple malzemesine benzetme; kapsam aşılır |

### Durum ve kullanım matrisi

| Koşul | Görsel uygulama sınırı | İnceleme odağı |
| --- | --- | --- |
| Yoğun harita | Tam okunur kontrol zemini | Alt çizgi metne karışıyor mu? |
| Fotoğraf üstü | Mevcut opak okuma desteği | Değişken parlaklık etkisi |
| Koyu tema | Koyu üst yüzey rolü | Cam yerine siyah perde baskısı |
| Azaltılmış saydamlık | İşlevin aynı görsel anlamı | Katman aidiyeti korunuyor mu? |
| Düşük performans | Efektsiz normal görünüm | Kalite düşmüş gibi sunuluyor mu? |

### İyi ve kötü örnekler

| Bağlam | İyi örnek | Kötü örnek |
| --- | --- | --- |
| Harita | Yol üstünde opak arama kontrolü | Yol adının düğme yazısına karışması |
| Uyarı | Ana yüzeyde açık hata açıklaması | Fotoğrafı gösteren saydam hata kutusu |
| AI | Metinle kapsamı belirli açıklama | Cam parıltısıyla doğrulanmış bilgi izlenimi |

### Görsel inceleme

- Cam başlığının yeni cam uygulama kararı gibi yazılmadığını kontrol et.
- Karar metninin hiçbir değişken arka plana bağımlı olmadığını incele.
- Malzeme kaldırıldığında katman anlamının sürdüğünü değerlendir.

### Bölüm sonu öz eleştiri

- **Öz eleştiri Ö14.1 — Opaklık haritayı fazla örtebilir.**
  Kontrolün kapladığı alan mevcut mimari içinde incelenmelidir; çözüm kritik metni saydamlaştırmak değildir.

- **Öz eleştiri Ö14.2 — Platformla görsel mesafe oluşabilir.**
  Yeni Apple malzemeleriyle fark, kullanıcıya yabancılık veriyor mu sorusu gerçek görevle değerlendirilmelidir.

- **Öz eleştiri Ö14.3 — Yasak gereğinden geniş yorumlanabilir.**
  İşletim sisteminin kendi izinli kabuğu ürünün özel glassmorphism uygulamasıyla aynı şey değildir.

## Blur Kullanımı

Bölüm kimliği: V15.
Dayanak: 10 Design System §19, 38, 52, 57; 11 Ekran Mimarisi §45.
Blur, gölge bulanıklığı ile arka içerik bulanıklığı olarak ayrı değerlendirilir.
Gölge rolünün sayısal aralığı, bütün ekranın bulanıklaştırılmasına izin vermez.
Mahremiyet veya yetkilendirme yalnız blur efektiyle sağlanmış sayılamaz.

### Tasarım ilkeleri

#### İlke V15.1 — Arka planı açık tutmak

Karar: Karar metni ve harita verisi dekoratif blur altında bırakılmaz.
Gerekçe: Görsel sis veri yokluğu veya pasiflik sanılabilir.
Sonuç: Kullanıcı mevcut içeriği net okuyabilir.
Bedel: Atmosfer yaratmak için arka plan yumuşatılamaz.

#### İlke V15.2 — Gölgeyle sınırlı sayı

Karar: 8 ve 24 tb bulanıklık yalnız kabul edilmiş gölge rollerinin referansıdır.
Gerekçe: Aynı sayı farklı malzemede farklı iş yapar.
Sonuç: Değer aktarımı yanlış efekt üretmez.
Bedel: Tek blur tokenıyla bütün kullanım çözülemez.

#### İlke V15.3 — Mahremiyet ayrımı

Karar: Yetkisiz bilgi erişilebilir metinden de çıkarılan mevcut yetki sözleşmesine tabidir.
Gerekçe: Bulanık görünüm içeriğin hâlâ erişilebilir olmasını engellemez.
Sonuç: Görsel maske güvenlik kontrolü sanılmaz.
Bedel: Mahremiyet amacı salt görsel dokümana indirgenemez.

#### İlke V15.4 — Fotoğraf bütünlüğü

Karar: Teknik mahremiyet maskelemesi varsa kapsam etkisi korunur; koşul gizleyen estetik blur uygulanmaz.
Gerekçe: Giriş veya engelin bulanması yer değerlendirmesini çarpıtabilir.
Sonuç: Fotoğrafın kanıt sınırı görünür kalır.
Bedel: Bazı fotoğraflar kullanılabilirliğini kaybedebilir.

#### İlke V15.5 — Düşük hareket maliyeti

Karar: Geniş alanlı hareketli blur ürün dili değildir.
Gerekçe: Sürekli bulanıklık değişimi okuma ve cihaz yükünü artırabilir.
Sonuç: Metin stabil ve yüzeyler sakin kalır.
Bedel: Sinematik geçiş hissi sınırlanır.

### Karar ve karşılaştırma tablosu

| Konu | Seçilen görsel karşılık | Elenen karşılık ve nedeni |
| --- | --- | --- |
| Gölge blur | Yakın/geçici role bağlı | Ekran genelinde sis; rol karışır |
| Metin | Her durumda net | Blur ile kilit gösterme; bilgi erişimi belirsiz |
| Mahremiyet | Mevcut yetkiyle veri erişimi | Bulanık özel not; yanlış güvence |
| Fotoğraf | Kapsamı açıklanan gerekli maske | Engeli flu yapma; fiziksel koşul çarpılır |
| Hareket | Statik netlik | Sürekli odak değişimi; okuma yorulur |

### Durum ve kullanım matrisi

| Koşul | Görsel uygulama sınırı | İnceleme odağı |
| --- | --- | --- |
| Modal arkası | Mevcut pasiflik ayrımı | Blur olmasa görev sınırı açık mı? |
| Özel kayıt | Yetki sözleşmesinin görünür sonucu | Hassas metin efekt altında kalıyor mu? |
| Fotoğraf maskesi | Kapsam etkisi açıklanır | Yer koşulu artık okunabiliyor mu? |
| Düşük cihaz | Net opak yüzey | Efekt kaldırılınca anlam değişiyor mu? |
| Büyük metin | Keskin harf ve sınır | Yumuşatma okunurluğu azaltıyor mu? |

### İyi ve kötü örnekler

| Bağlam | İyi örnek | Kötü örnek |
| --- | --- | --- |
| Paylaşım | Özel not önizleme kapsamına alınmaz | Özel not yalnız bulanık görünür |
| Giriş fotoğrafı | Basamaklar net veya kapsam eksikliği açık | Basamaklar estetik alan derinliğiyle kaybolur |
| Bekleme | Statik iskelet ve durum metni | Tüm sayfa bulanıklaşıp kullanılabilir alan belirsizleşir |

### Görsel inceleme

- Blur kullanımının yetki veya güvenlik garantisi diye sunulmadığını kontrol et.
- Görsel yumuşatmanın bilgi koşulunu gizlemediğini incele.
- Gölge bulanıklığı ile arka plan efekti adlarının ayrıldığını doğrula.

### Bölüm sonu öz eleştiri

- **Öz eleştiri Ö15.1 — Blur yokluğu sert geçiş yaratabilir.**
  Katman ayrımını yumuşatmak için gerekli olmayan yeni hareket eklenmemeli; yüzey tonunun yeterliliği incelenmelidir.

- **Öz eleştiri Ö15.2 — Mahremiyet maskelemesi kanıtı azaltabilir.**
  Maske kritik ayrıntıyı kapatıyorsa fotoğrafı göstermek kullanıcıya yarardan çok belirsizlik verebilir.

- **Öz eleştiri Ö15.3 — Netlik tek başına doğru algı değildir.**
  Keskin ve kaliteli görünen fotoğraf eski veya farklı girişe ait olabilir; kapsam metni gereksiz sayılmamalıdır.

## Material You ile İlişki

Bölüm kimliği: V16.
Dayanak: 10 Design System §4, 14, 64.1; 11 Ekran Mimarisi §34.
Material You, Şamandıra'nın ürün kararlarının yerine geçen hazır bir görünüm değildir.
Google'ın resmî rehberi dinamik rengi kişiselleştirme imkânı olarak açıklar; bu, mevcut marka paletini değiştirme zorunluluğu değildir. [Android — Dynamic Colors](https://developer.android.com/develop/ui/views/theming/dynamic-colors).
Aşağıdaki tercihler bu kaynaktan hareketle yapılan Şamandıra yorumudur; uygulama veya framework seçimi içermez.

### Tasarım ilkeleri

#### İlke V16.1 — Anlamsal rol disiplini

Karar: Ortak renk, yazı ve yüzey rolleri korunur.
Gerekçe: Sistemler arasında öğrenilebilir yöntem rol tabanlı düşünmedir.
Sonuç: Material örnekleri ürün paletini ezmeden değerlendirilebilir.
Bedel: Hazır temayı doğrudan almanın hızı kullanılmaz.

#### İlke V16.2 — Dinamik renk sınırı

Karar: Bu sürümde duvar kâğıdından üretilmiş renkler kabul edilmiş paletin yerine geçirilmez.
Gerekçe: Mevcut tema çiftleri ve durum rolleri korunmalıdır.
Sonuç: Aynı durum farklı cihazlarda aynı anlamı taşır.
Bedel: Kişiselleştirme alanı genişlemez.

#### İlke V16.3 — Şekli kopyalamamak

Karar: Hazır Material şekil ölçeği mevcut 8/12/16 rol ayrımını değiştirmez.
Gerekçe: Dış sistemin şekli ürünün kabul edilmiş sözleşmesinin önünde değildir.
Sonuç: Kontrol ve kart ailesi tutarlı kalır.
Bedel: Güncel örneklerle birebir görünüm sağlanmaz.

#### İlke V16.4 — Android tanışıklığı

Karar: Yerel sistem kontrollerinin mevcut davranış ve erişim beklentisi korunur.
Gerekçe: Kullanıcı geri ve seçim davranışını yeniden öğrenmemelidir.
Sonuç: Görsel uyarlama tanınır eylemleri destekler.
Bedel: Marka adına bütün yerel kontroller tek kalıba zorlanamaz.

#### İlke V16.5 — Ürün bağımsızlığı

Karar: Material'daki bileşen varlığı o bileşeni Şamandıra'ya ekleme gerekçesi olmaz.
Gerekçe: FAB veya navigation örneği yeni görev ihtiyacı yaratmaz.
Sonuç: Ekran mimarisi değişmez.
Bedel: Hazır katalogdaki her parça kullanılamaz.

### Karar ve karşılaştırma tablosu

| Konu | Seçilen görsel karşılık | Elenen karşılık ve nedeni |
| --- | --- | --- |
| Renk yöntemi | Anlamsal rol ve izinli çift | Rastgele seed rengi; kabul paleti değişir |
| Şekil | Mevcut radius rolleri | Material örneğini aynen kopyalama; sistem değişir |
| Kontrol | Yerel tanışıklık ve erişim | Marka uğruna geri davranışını yeniden yazma |
| Katalog | Mevcut göreve uygun bileşen | FAB var diye ekleme; yeni eylem icadı |
| Uyum | Aynı anlamın Android karşılığı | Her platform aynı piksel; yerel beklenti kaybı |

### Durum ve kullanım matrisi

| Koşul | Görsel uygulama sınırı | İnceleme odağı |
| --- | --- | --- |
| Dinamik sistem teması | Ürün rol paleti korunur | Durum rengi kayıyor mu? |
| Koyu Android | 10 belgesinin koyu çiftleri | Material varsayılanı eski rolü eziyor mu? |
| Sistem seçicisi | Mevcut platform yüzeyi | Ürün yetkisi sanılan yeni işlem var mı? |
| Büyük yazı | Platform metin ölçeğiyle uyum | Hazır bileşen yüksekliği kesiyor mu? |
| Harita kontrolü | Ortak opak araç yüzeyi | Tonal zemin yolla karışıyor mu? |

### İyi ve kötü örnekler

| Bağlam | İyi örnek | Kötü örnek |
| --- | --- | --- |
| Eylem | Kabul edilmiş yeşil ve okunur etiket | Telefon duvar kâğıdıyla kırmızıya dönmüş ana eylem |
| Kart | E0 ve 12 tb | Hazır Material kart gölgesini otomatik alma |
| Navigasyon | Mevcut ana öğelerin yerel sunumu | Kataloğu doldurmak için yeni sekme |

### Görsel inceleme

- Dış kaynaktan alınan yöntemle yeni ürün kararı arasındaki sınırı kontrol et.
- Dinamik renk hakkında uygulamaya geçirilmiş özellik iddiası bulunmadığını incele.
- Android görünümünün bilgi sırasını değiştirmediğini değerlendir.

### Bölüm sonu öz eleştiri

- **Öz eleştiri Ö16.1 — Kişiselleştirme beklentisi karşılanmayabilir.**
  Sabit paletin Android kullanıcı algısına etkisi ileride incelenmelidir; mevcut renkler sessizce değiştirilmez.

- **Öz eleştiri Ö16.2 — Hazır bileşen avantajı küçümsenebilir.**
  Ortak davranışı doğru sağlayan yerel araç sırf görünümü farklı diye reddedilmemelidir.

- **Öz eleştiri Ö16.3 — Material çok geniş bir sistemdir.**
  Bu bölüm yalnız renk, şekil ve uyum ilişkisini ele alır; tüm Material uygulamalarının aynı göründüğü iddiasını taşımaz.

## iOS Human Interface Guidelines ile İlişki

Bölüm kimliği: V17.
Dayanak: 10 Design System §55, 64.2; 11 Ekran Mimarisi §34–38.
iOS uyumu, tanıdık platform davranışı ve okunabilir içerik ilişkisini korumaktır.
Apple HIG malzemeleri Liquid Glass ve standart malzemeler olarak ayırır; kontrollerle içeriğin ilişkisini tarif eder. [Apple — Materials](https://developer.apple.com/design/human-interface-guidelines/materials).
Şamandıra bu ayrımdan rol disiplini öğrenir; mevcut opak karar yüzeyini cam katmana dönüştürmez.

### Tasarım ilkeleri

#### İlke V17.1 — İçeriğin önceliği

Karar: Yer kimliği ve gerekli açıklama platform süsünden daha belirgin kalır.
Gerekçe: Gezginin görevi kontrol malzemesini izlemek değildir.
Sonuç: Gerçek içerik aynı sırayla okunur.
Bedel: Yeni işletim sistemi estetiğini tam taklit etmek amaç olmaz.

#### İlke V17.2 — Yerel metin uyumu

Karar: Sistem sans ve erişilebilir metin ölçeği korunur.
Gerekçe: Platformun kullanıcı tercihi uygulama görünümünden önce gelir.
Sonuç: Büyüyen yazı mevcut bilgiyi taşır.
Bedel: Metin büyüklüğünü marka sabiti olarak kilitlemek mümkün değildir.

#### İlke V17.3 — Geri dönüş tanışıklığı

Karar: Mevcut geri ve kapanış eylemlerinin görsel farkı korunur.
Gerekçe: Geri gitmekle görevi kapatmak aynı anlam taşımayabilir.
Sonuç: Kullanıcı tanıdık platform işaretlerinden yararlanır.
Bedel: Özel denizcilik ikonuyla geri düğmesi değiştirilemez.

#### İlke V17.4 — Katman ölçülülüğü

Karar: Bağımsız sheet ve modal kendi kabul edilmiş 16 tb yüzey rolünü korur.
Gerekçe: HIG örneği yeni katman veya farklı ekran açma yetkisi vermez.
Sonuç: Mevcut odak ve kapanış sözleşmesi desteklenir.
Bedel: Platform görsel varyasyonları için optik inceleme gerekir.

#### İlke V17.5 — Erişim hedefi

Karar: Ürün hedefi 48×48, küçük kontrol alt sınırı 44×44 mantıksal birimdir.
Gerekçe: Şamandıra kendi erişim hedefini platform minimumuyla karıştırmamalıdır.
Sonuç: Dokunma ve karma giriş aynı kaliteyi taşır.
Bedel: Daha küçük görsel kontrolün çevresinde hedef alanı gerekir.

### Karar ve karşılaştırma tablosu

| Konu | Seçilen görsel karşılık | Elenen karşılık ve nedeni |
| --- | --- | --- |
| Tanışıklık | Geri ve kontrol anlamı korunur | Platformu marka metaforuyla değiştirme; öğrenme artar |
| Malzeme | Ürün opaklığı, yerel kabuk ayrımı | Bütün kartları Liquid Glass yapma; kabul sınırı aşılır |
| Font | Sistem sans ve ölçek uyumu | Özel display fontunu bütün metne dayatma |
| Sheet | Mevcut görev katmanı | iOS örneği var diye yeni sheet; akış değişir |
| Hedef | Şamandıra 48 varsayılan | İkon 24 diye hedef 24; erişim zorlaşır |

### Durum ve kullanım matrisi

| Koşul | Görsel uygulama sınırı | İnceleme odağı |
| --- | --- | --- |
| Büyük erişilebilir yazı | Mevcut yeniden akış | Metin veya eylem kesiliyor mu? |
| Sistem geri hareketi | Görsel yol tanışık kalır | Kart hareketiyle rekabet ediyor mu? |
| Koyu tema | Aynı semantik roller | Başlık önemi değişiyor mu? |
| Aktif sheet | Açan görevle görsel ilişki | Kapanış yolu algılanıyor mu? |
| Platform malzemesi | Ürün bilgisini örtmez | Efekt doğruluk algısını şişiriyor mu? |

### İyi ve kötü örnekler

| Bağlam | İyi örnek | Kötü örnek |
| --- | --- | --- |
| Geri | Tanınır yön işareti ve gerekli etiket | Pusula simgesiyle geri eylemi |
| Metin | Büyük ölçekte okunur sınır | iPhone görünümü bozulmasın diye font küçültme |
| Malzeme | Opak kart ve tanınır sistem kabuğu | Yerin güven koşulunu cam parıltısına bağlama |

### Görsel inceleme

- HIG karşılaştırmasının bütün Apple ürünlerine ilişkin genelleme içermediğini kontrol et.
- Platform ölçüsüyle ürün hedefinin açık ayrıldığını incele.
- Görsel uyumun yeni geri veya kapanış davranışı önermediğini doğrula.

### Bölüm sonu öz eleştiri

- **Öz eleştiri Ö17.1 — Platform tanışıklığı herkes için aynı değildir.**
  Android'den geçen veya yardımcı teknoloji kullanan kişilerin işaretleri yorumlaması ayrıca değerlendirilmelidir.

- **Öz eleştiri Ö17.2 — Opak görünüm daha eski algılanabilir.**
  Modernlik beklentisi gerçek okunabilirlikle birlikte sınanmalıdır; malzeme modası tek karar gerekçesi olamaz.

- **Öz eleştiri Ö17.3 — Ortak radius yerel kontrollerle farklılaşabilir.**
  Bu farkın kullanıcıya anlamlı bir sorun oluşturup oluşturmadığı gerçek görev içinde incelenmelidir.

## Android Tasarım Uyumu

Bölüm kimliği: V18.
Dayanak: 10 Design System §55–59, 64.1; 11 Ekran Mimarisi §34–36.
Android uyumu; farklı pencere, yazı ölçeği ve giriş yönteminde aynı kararın okunmasını gerektirir.
Bu bölüm donanım listesi, uygulama çerçevesi veya mobil yayın kararı üretmez.
WCAG 2.2 AA işaretçi hedefi minimumu bazı istisnalarla 24×24 CSS pikselidir; Şamandıra'nın 48/44 hedefleri ayrı ürün standardıdır. [W3C — Target Size Minimum](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html).

### Tasarım ilkeleri

#### İlke V18.1 — Pencereye göre görünüm

Karar: Mevcut dar, orta ve geniş alan kuralları kullanılabilir pencereye uygulanır.
Gerekçe: Telefon veya tablet adı tek başına alanı açıklamaz.
Sonuç: Bölünmüş pencerede içerik kendi kabında okunur.
Bedel: Cihaz adına sabit görünüm paketi tanımlanamaz.

#### İlke V18.2 — Sistem kenarı

Karar: Mevcut eylemler sistem hareket ve güvenli alanlarıyla çakışmaz.
Gerekçe: Kenar geri hareketi ve ürün kontrolü yarışırsa kazara giriş oluşabilir.
Sonuç: Tek elle hedefe erişim öngörülebilir olur.
Bedel: Kenardan kenara görsel hedef bütün alanı kullanamaz.

#### İlke V18.3 — Yazı ölçeği

Karar: Metin boyutu arttığında kutu büyümesi ve kabul edilmiş yeniden akış sürer.
Gerekçe: Android yazı ve ekran ölçeği aynı görünümü farklı boyutlara taşıyabilir.
Sonuç: Gerekçe ve sınır okunur kalır.
Bedel: Daha az satırın aynı anda görünmesi kabul edilir.

#### İlke V18.4 — Karma giriş

Karar: Dokunmatik cihazda fare veya klavye bulunması hedefi küçültmez.
Gerekçe: Aynı kişi giriş yöntemini görev içinde değiştirebilir.
Sonuç: Hedef, odak ve basılı durum tutarlı olur.
Bedel: Yalnız masaüstü yoğunluğu otomatik seçilemez.

#### İlke V18.5 — Durum eşdeğerliği

Karar: Açık, koyu ve yüksek kontrast görünüm aynı işlem durumunu taşır.
Gerekçe: Tema veya üretici görünümü bilgi otoritesini değiştirmez.
Sonuç: Başarı ve belirsizlik her ortamda ayrılır.
Bedel: Platform başına ayrı bir doğruluk göstergesi açılamaz.

### Karar ve karşılaştırma tablosu

| Konu | Seçilen görsel karşılık | Elenen karşılık ve nedeni |
| --- | --- | --- |
| Genişlik | Pencere ve kap ölçüsü | Telefon modeli; gerçek alanı kaçırır |
| Hedef | 48 varsayılan, 44 küçük alt sınır | Sadece WCAG tabanına inme; ürün hedefi azalır |
| Giriş | Dokunma, fare ve odak birlikte | Fare var diye küçük düğme; karma kullanım zorlaşır |
| Sistem kenarı | Güvenli ve görünür hedef | Kenara taşan CTA; sistemle yarışır |
| Tema | Ortak rol karşılığı | Üreticiye göre durum anlamı; tutarlılık kırılır |

### Durum ve kullanım matrisi

| Koşul | Görsel uygulama sınırı | İnceleme odağı |
| --- | --- | --- |
| Bölünmüş pencere | Kendi kabında daralma | Yer adı ve eylem sığıyor mu? |
| Büyük ekran ölçeği | İçerik sınırlarının esnemesi | Yan yana alanlar çakışıyor mu? |
| Klavye bağlı tablet | Görünür odak ve dokunma hedefi | Bir giriş türü ihmal edilmiş mi? |
| Yatay telefon | Kısa yükseklikte mevcut uyarlama | Sabit alan içeriği örtüyor mu? |
| Yüksek kontrast | Sistem renk önceliği | Marka tonu anlamın önüne geçiyor mu? |

### İyi ve kötü örnekler

| Bağlam | İyi örnek | Kötü örnek |
| --- | --- | --- |
| Tablet | Aynı koşul ve bilgi, yeterli genişlik | Tablet diye fazladan öneri sütunu |
| Erişim | 24 tb ikonun 48 tb hedefi | 24 tb ikonun aynı boyda hedefi |
| Sistem geri | Kenar hareketine alan bırakan araç | Harita sürüklemesi tüm kenarı ele geçirir |

### Görsel inceleme

- Platform uyumunun ekran yeniden tasarımına dönüşmediğini denetle.
- Pencere değişirken metin ve odak görünürlüğünü incele.
- WCAG sayıları ile ürün hedeflerinin birbirine eşit sunulmadığını kontrol et.

### Bölüm sonu öz eleştiri

- **Öz eleştiri Ö18.1 — Cihaz çeşitliliği denetimi büyütür.**
  Yalnız en yeni cihazda iyi görünmek hedef kitlenin gerçek kullanımını temsil etmez.

- **Öz eleştiri Ö18.2 — 48 birim her elde kolay değildir.**
  Hedef ölçüsü erişilebilirliğin tek koşulu değildir; mesafe, tutuş ve komşu hedefler de önemlidir.

- **Öz eleştiri Ö18.3 — Üretici farkı bütünüyle kontrol edilemez.**
  Sistem yüzeyleri farklılaşabilir; asıl kabul ölçütü aynı görevin anlam ve erişim bütünlüğüdür.

## Dark Mode Felsefesi

Bölüm kimliği: V19.
Dayanak: 10 Design System §14, 16–19; 11 Ekran Mimarisi E15.
Koyu tema açık görünümün ters renk filtresi değildir.
Sistem tercihi ve kullanıcının mevcut açık tema seçimi sözleşmesi korunur.
Fotoğrafın renkleri ters çevrilmez; koyu tema ücretsiz temel erişimin parçasıdır.

### Tasarım ilkeleri

#### İlke V19.1 — Katmanlı koyu yüzey

Karar: Sayfa #111916, ana #1B2620, iç #15201B ve üst #25342B aynen kullanılır.
Gerekçe: Bu roller karanlıkta yüzey ilişkisini gölgeden bağımsız taşır.
Sonuç: Kalıcı ve geçici içerik ayırt edilir.
Bedel: Her alanı saf siyaha dönüştürmek kabul edilmez.

#### İlke V19.2 — Okunur açık metin

Karar: Birincil #F0F5EF, ikincil #C0CEC2, caption #A6B6A9 rollerini korur.
Gerekçe: İkincil bilgi de okunur kontrast gerektirir.
Sonuç: Metin önemi ton farkıyla anlaşılır.
Bedel: Sakinlik için caption opaklığı azaltılamaz.

#### İlke V19.3 — Eylem çifti

Karar: Birincil eylem #8DD9B5, üzerinde #102B20 metin kullanır.
Gerekçe: Koyu yüzeyde vurgu farklı parlaklık gerektirir.
Sonuç: CTA okunur ve belirgin kalır.
Bedel: Açık temanın beyaz buton metni buraya kopyalanamaz.

#### İlke V19.4 — Gerçek fotoğraf

Karar: Fotoğraf yapay gece görüntüsüne çevrilmez.
Gerekçe: Renk işlemi yerin fiziksel koşullarını yanlış gösterebilir.
Sonuç: Aynı fotoğrafın kapsamı tema değişiminde korunur.
Bedel: Parlak fotoğrafın çevreyle kontrastı ayrıca incelenir.

#### İlke V19.5 — Kontrast önceliği

Karar: Yüksek kontrast ihtiyacında sistem renk ve sınırları marka tonundan önce gelir.
Gerekçe: Tema estetiği erişimi engelleyemez.
Sonuç: Temel durum ve odak okunur kalır.
Bedel: Bütün cihazlarda aynı renk görünümü garanti edilmez.

### Karar ve karşılaştırma tablosu

| Konu | Seçilen görsel karşılık | Elenen karşılık ve nedeni |
| --- | --- | --- |
| Zemin | Katmanlı yeşilimsi koyu yüzey | Tek saf siyah; yüzeyler birleşir |
| Metin | Üç izinli açık rol | Gri opaklığı rastgele azaltma; caption kaybolur |
| Buton | Açık yeşil üstünde koyu metin | Açık yeşil üstünde beyaz; eşleşme bozulur |
| Fotoğraf | Özgün renk ve kapsam | Otomatik karartma; koşul değişir |
| Odak | #A9CAFF görünür halka | Yalnız gölge; odak kaybolur |

### Durum ve kullanım matrisi

| Koşul | Görsel uygulama sınırı | İnceleme odağı |
| --- | --- | --- |
| Normal | #1B2620 ana yüzey | Birincil metin net mi? |
| Geçici katman | #25342B üst yüzey | Ana karttan ayrılıyor mu? |
| Seçim | #233E30 ve işaret | Başarı sanılıyor mu? |
| Güçlü sınır | #829688 | Kontrol tek başına seçilebiliyor mu? |
| Harita gece stili yok | Mevcut liste işlevi korunur | Okunamayan harita zorlanıyor mu? |

### İyi ve kötü örnekler

| Bağlam | İyi örnek | Kötü örnek |
| --- | --- | --- |
| Gece okuma | Caption da açıkça okunur | Premium görünüm için çok karanlık metadata |
| Fotoğraf | Aynı yer fotoğrafı doğal | Gündüz fotoğrafını geceye çevirme |
| Bildirim | Üst yüzey ve görünür metin | Siyah gölge üstünde koyu metin |

### Görsel inceleme

- Koyu değerlerin 10 belgesindeki rollere birebir uyduğunu kontrol et.
- Fotoğrafta tema nedeniyle anlamsal değişim yapılmadığını incele.
- Açık ve koyu görünümün aynı içerik ve hakları taşıdığını değerlendir.

### Bölüm sonu öz eleştiri

- **Öz eleştiri Ö19.1 — Yeşilimsi koyu ton her fotoğrafla dengeli değildir.**
  Farklı doğal renklerde fotoğraf kenarı ve yüzey ilişkisi gerçek içerikle incelenmelidir.

- **Öz eleştiri Ö19.2 — Parlaklık algısı cihazdan cihaza değişir.**
  Hesaplanan kontrast, gece ortamındaki kamaşma veya OLED davranışını tek başına açıklamaz.

- **Öz eleştiri Ö19.3 — Tema eşitliği unutulabilir.**
  Nadir hata ve admin durumlarının yalnız açık görünümde tasarlanması sistemin bütünlüğünü zayıflatır.

## Light Mode Felsefesi

Bölüm kimliği: V20.
Dayanak: 10 Design System §14–17, 55–56.
Açık tema mineral sayfa zemini ve beyaz ana yüzeyle uzun okumayı destekler.
Palet yeni bir marka araştırması sonucu değil, kabul edilmiş 10 belgesinin aynen korunan kararıdır.
Normal metinde 4,5:1; uygun büyük metinde 3:1 kontrast tabanı kullanılır; büyüklük teknik ölçütü ayrıca değerlendirilir. [W3C — Contrast Minimum](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html).

### Tasarım ilkeleri

#### İlke V20.1 — Mineral arka plan

Karar: Sayfa #F6F7F4, ana ve üst yüzey #FFFFFF, iç yüzey #EEF1ED kalır.
Gerekçe: Az ton farkı içerik ilişkisini aşırı kutulamadan gösterebilir.
Sonuç: Fotoğraf ve metin sakin bir çevre bulur.
Bedel: Tarihsel krem palet bu rolü sessizce değiştiremez.

#### İlke V20.2 — Koyu metin

Karar: Birincil #202B28, ikincil #4C5B54, caption #5C6962 korunur.
Gerekçe: Yüksek okunabilirlik açık temanın temel görevidir.
Sonuç: Destekleyici bilgi de rahat taranır.
Bedel: Gri metin estetik için daha fazla soldurulamaz.

#### İlke V20.3 — Eylem kontrastı

Karar: Birincil eylem #185A48 üzerinde #FFFFFF metin taşır.
Gerekçe: Bu izinli çift CTA'nın okunurluğunu destekler.
Sonuç: Vurgu alanı bütün zeminleri boyamadan işlev görür.
Bedel: Yeni hover tonu keyfî alfa değişimiyle üretilemez.

#### İlke V20.4 — Sınır ayrımı

Karar: Güçlü sınır #718078, hafif ayırıcı #D3DAD4 olarak ayrılır.
Gerekçe: Dekoratif ayırıcı kontrolün tek algı sınırı olmamalıdır.
Sonuç: Formlar ve araçlar boş alandan seçilir.
Bedel: Çok hafif çizgiyle her kontrol çözülemez.

#### İlke V20.5 — Dış ortam dikkati

Karar: Güneş altında okunabilirlik için metin, opaklık ve hedef bütünlüğü korunur.
Gerekçe: Turistik kullanım ideal masaüstü ışığıyla sınırlı değildir.
Sonuç: Yer bilgisi hareket halindeki kısa bakışta daha anlaşılır olur.
Bedel: Yalnız hesaplanan oranlar gerçek dış ortam başarısını kanıtlamaz.

### Karar ve karşılaştırma tablosu

| Konu | Seçilen görsel karşılık | Elenen karşılık ve nedeni |
| --- | --- | --- |
| Sayfa | #F6F7F4 mineral | Yeni krem veya bembeyaz her alan; mevcut rol değişir |
| Kart | #FFFFFF ana yüzey | Gereksiz renkli dekor; karar alanı dağılır |
| Caption | #5C6962 okunur rol | Çok soluk gri; dış ortamda kaybolur |
| Eylem | Koyu yeşil ve beyaz çift | Turuncu eski CTA'yı geri alma; kabul kararı aşılır |
| Ayırıcı | Dekor ve güçlü sınır ayrımı | Tek soluk çizgi; kontrol algısı zayıflar |

### Durum ve kullanım matrisi

| Koşul | Görsel uygulama sınırı | İnceleme odağı |
| --- | --- | --- |
| Gövde | Birincil rol ve 16/24 başlangıç | Kontrast ve satır takibi |
| Caption | 13/20 ve izinli koyu ton | İkincil bilgi okunuyor mu? |
| Seçim | #E0EFE7, işaret ve metin | Uygunluk sanılıyor mu? |
| Odak | #164FAD ve 2+2 tb halka | Komşu yüzeyde seçiliyor mu? |
| Fotoğraf yanında | Opak metin alanı | Fotoğraf ışığı okumayı bastırıyor mu? |

### İyi ve kötü örnekler

| Bağlam | İyi örnek | Kötü örnek |
| --- | --- | --- |
| Kontrol | Güçlü sınırla belirgin alan | Sadece beyaz üstüne çok soluk çizgi |
| Metin | Sınır bilgisi gövde ağırlığında | Uyarı küçük gri dipnota küçülür |
| Yer fotoğrafı | Doğal renk, okunur açıklama | Açık tema için fazla parlak filtre |

### Görsel inceleme

- Açık paletin bütün değerlerini rol karşılığıyla karşılaştır.
- Hafif ayırıcının tek kontrol veya odak sınırı olmadığını doğrula.
- Normal metin ve büyük metin kontrast sınıflarını doğru ayır.

### Bölüm sonu öz eleştiri

- **Öz eleştiri Ö20.1 — Açık mineral yüzey kirli görünebilir.**
  Renk algısı ekran ve ışıkla değişir; bu tonun gerçek cihaz değerlendirmesi yapılmış varsayılmamalıdır.

- **Öz eleştiri Ö20.2 — Beyaz kartlar gece rahatsız edebilir.**
  Kullanıcının tema tercihi korunmalı; açık görünüm bütün koşullar için tek doğru seçenek sayılmamalıdır.

- **Öz eleştiri Ö20.3 — Kontrast oranı bütün okunurluk değildir.**
  Font metriği, satır uzunluğu ve görsel dikkat rekabeti ayrıca incelenmeden kalite tamamlandı denemez.

## Tipografi Hiyerarşisi

Tipografi, Şamandıra'nın yer kimliği ile karar gerekçesini aynı bakışta ayrıştırır.
Öncelik fotoğrafın etkisine veya yerin ticari değerine bağlanmaz.
Bu bölüm 10 Design System §9–13 içindeki sayısal ölçeği aynen kullanır.
Başlık büyüklüğü yeni ekran seviyesi veya yeni içerik sırası oluşturmaz.
Görsel vurgu mevcut mimarideki anlamın okunmasını destekler.

### Kapsam ve görsel karar

Birlikte görülen bilgi en fazla üç eşzamanlı vurgu düzeyinde okunur.
İlk düzey mevcut görev veya yer kimliğidir.
İkinci düzey gerekçe ile kararı değiştiren sınırdır.
Üçüncü düzey destekleyici bağlamdır.
Bilinen engelin önceliği, kimlikten sonra belirgin metinle korunur.
İkincil başlık sayısı artsa da bütün metinler aynı anda kalınlaşmaz.
Sayfa ve kart ölçülerinin farklılığı içerik sorumluluğunu anlatır.
Boyutlar normal metin ölçeğindeki başlangıç değerleridir.

### Tasarım ilkeleri

#### İlke V21.1 — Sayısal ölçek kabul edilmiş rollerden alınır.

Gerekçe: Yeni ara boyutlar aynı içeriğe farklı önem yükler.
Bedel: Her dar alana özel görsel kestirme kullanılamaz.
Görsel sonuç: Gövde 16/24, kart başlığı 20/28 olarak tanınır.

#### İlke V21.2 — Gerekçe ve kritik sınır aynı okunabilirlik düzeyini paylaşır.

Gerekçe: Küçük yazılan bilinmeyen, olumlu iddiayı olduğundan kesin gösterir.
Bedel: Karar kartı bazen daha uzun görünür.
Görsel sonuç: Kritik açıklama caption rolüne düşürülmez.

#### İlke V21.3 — Hiyerarşi boyut, ağırlık ve boşluğun ortak etkisiyle kurulur.

Gerekçe: Yalnız renk veya kalınlık bütün ilişkileri taşıyamaz.
Bedel: Her tema ve metin ölçeğinde birlikte inceleme gerekir.
Görsel sonuç: Aynı anlam her yüzeyde benzer vurgu oranını korur.

#### İlke V21.4 — Büyük anlatı ölçüsü yalnız mevcut anlatı bağlamında kullanılır.

Gerekçe: 40/48 düzeyi sık tekrarlanırsa görevin adı geri çekilir.
Bedel: İç görevler tanıtım sayfası kadar gösterişli görünmez.
Görsel sonuç: Dar anlatıda 32/40, dar sayfa başlığında 28/36 korunur.

#### İlke V21.5 — Metin büyütme tipografik ilişkiyi bozamaz.

Gerekçe: Kullanıcının okuma tercihi bilgi azaltma gerekçesi değildir.
Bedel: Kartlar ve geçici yüzeyler daha fazla alan kullanabilir.
Görsel sonuç: Etiket, gerekçe ve başlık kendi kutularıyla birlikte büyür.

### Rol ve durum matrisi

| Rol veya durum | Görsel karşılık | Korunan sınır |
| --- | --- | --- |
| Büyük anlatı | 40/48; dar alanda 32/40; 600 | Tekrarlanan kart başlığı olmaz |
| Sayfa başlığı | 32/40; dar alanda 28/36; 600 | Şube kimliği kesilmez |
| Bölüm başlığı | 24/32; 600 | Yeni görev açmaz |
| Kart başlığı | 20/28; 600 | Diğer kartlara üstünlük vermez |
| Vurgulu gövde | 18/28; 400 veya 600 | Her paragrafta tekrarlanmaz |
| Karar metni | 16/24; 400 | Kritik bilinmeyeni taşır |
| İkincil bilgi | 14/20; 400 | Engel açıklamasının yeri değildir |
| Etiket ve caption | 16/24; 600 ve 13/20; 400 | Roller birbirine karıştırılmaz |

### İyi ve kötü yazılı örnekler

| Bağlam | İyi örnek | Kötü örnek | Neden |
| --- | --- | --- | --- |
| Yer kararı | Yer adı belirgin; akşam bilgisi sınırı gövdede | Dev ad; belirsizlik ince dipnotta | Görsel güven kanıtı aşar |
| Günlük rota | Rota adı, değerlendirme durumu ve süre ayrışır | Bütün toplamlar büyük ve kalın | Birden fazla odak oluşur |
| Kayıt | Kişisel isim kimlik rolünde kalır | Kaydedilen yere vitrin başlığı verilir | Kayıt uygunluk sanılabilir |
| AI açıklaması | Ortak gövde ve sınır dili | AI metni farklı fontla daha büyük | Yardımcı otoriteye dönüşür |
| Uzun ad | Ayırt edici şube adı sarılır | Şube ayrımı üç noktayla kaybolur | Yanlış yere yönelme riski artar |

### Neden ve sonuç değerlendirmesi

Ölçek sayısının sınırlanması bakımda rol eşlemesini kolaylaştırır.
Bu sınırlama bilgi miktarını sabit satır sayısına kilitlemez.
İddianın uzunluğu ile kartların yüksekliği eşit olmak zorunda değildir.
Görsel denge için önce tekrar eden olumlu sıfatlar azaltılır.
Kritik metni küçültmek, doğru bilgiyi fiilen görünmez kılar.
Başlıklar arasındaki boşluk konu ilişkisine göre mevcut aralıklarla seçilir.
Boşluk büyütülerek yeni bir gizli önem derecesi üretilmez.
Eşit ölçek kullanan iki yerin anlamı içerikteki gerçek farkla ayrılır.

### İnceleme sınırı

Bu kararlar uygulanmış ekran ölçümü veya kullanıcı araştırması sonucu değildir.
Gerçek yer adları, uzun Türkçe ekler ve tarih aralıklarıyla incelenmelidir.
Açık ve koyu tema aynı okuma önceliğini taşımalıdır.
Yüzde 200 metinde başlığın taşması küçültme ile kapatılmamalıdır.
Sadece başlıklara bakarak kararın olumlu olduğu izlenimi oluşmamalıdır.
İç admin yoğunluğu tüketici tipografisini küçültme gerekçesi olamaz.

### Bölüm sonu öz eleştiri

- **Öz eleştiri Ö21.1 — Üç vurgu düzeyi karmaşık sınırları yeterince ayırmayabilir; anlama güçleşirse mevcut rollerin kullanımını açıklığa kavuşturmak gerekir.**

- **Öz eleştiri Ö21.2 — Büyük metinle değişken kart boyları taramayı zorlaştırabilir; çözüm kritik metni kesmeden hizalama ilişkisini güçlendirmektir.**

- **Öz eleştiri Ö21.3 — Rol tablosu mekanik uygulanırsa yerin karakteri silinebilir; karakter gerçek ad ve somut açıklamada korunmalıdır.**

## Font Kullanımı

Şamandıra başlangıçta işletim sistemiyle uyumlu sistem sans ailesini kullanır.
Sistem sans kararı ürün metni içindir; mevcut logo ve kelime kilidi varlığını değiştirmez.
Fontun işi Türkçe metni açık, hızlı ve sakin okutabilmektir.
Yer kimliğinin görünürlüğü font indirmesine bağlı kalmaz.
Platformlar arasında optik benzerlik aranır; glif özdeşliği istenmez.

### Kapsam ve görsel karar

10 Design System §9–10 aile seçiminin otoritesidir.
Normal gövde ağırlığı 400, başlık ve etiket hedefi 600'dür.
Kalınlık eşlemesi her platformun gerçek çizimiyle değerlendirilir.
Sahte kalın veya sahte italik üretimi bir kimlik çözümü sayılmaz.
Türkçe İ, ı, Ş, ş, Ğ, ğ, Ö, ö, Ü, ü, Ç ve ç ilk örnek kümesidir.
Para işaretleri, tarih ayraçları ve rakamlar aynı incelemeye dahildir.
Tabular rakam yalnız karşılaştırmalı sayılarda kullanılabilir.
Ürünün tüm metni teknik görünüm için monospace yapılmaz.

### Tasarım ilkeleri

#### İlke V22.1 — Sistem sans ailesi ortak temel olarak korunur.

Gerekçe: Yerel metin tercihleri ve başlangıç erişimi doğrudan desteklenir.
Bedel: Tek font dosyasına dayalı marka özdeşliği kurulmaz.
Görsel sonuç: Özgünlük metin düzeni ve içerik açıklığından doğar.

#### İlke V22.2 — Dil kapsamı görünüş tercihinden önce değerlendirilir.

Gerekçe: Eksik glif veya yanlış Türkçe şekil yer kimliğini zedeler.
Bedel: Bazı alfabelerde uyumlu yedek eşleme gerekir.
Görsel sonuç: Aynı sözcükte kırık veya eksik harf oluşmaz.

#### İlke V22.3 — Ağırlıklar optik olarak dengelenir.

Gerekçe: Aynı 600 değeri farklı sistem ailelerinde aynı koyulukta değildir.
Bedel: Platform örneklerinin birlikte incelenmesi gerekir.
Görsel sonuç: Başlık netleşir; gövdeye gereksiz baskı kurmaz.

#### İlke V22.4 — Font değişimi eylem konumunu sıçratamaz.

Gerekçe: Sonradan değişen metin metriği yanlış dokunmaya neden olabilir.
Bedel: Yedek eşlemede dekoratif font özgürlüğü sınırlanır.
Görsel sonuç: Etiket ve hedef ilişkisi metin boyunca kararlı kalır.

#### İlke V22.5 — Sayısal hizalama ihtiyaca bağlıdır.

Gerekçe: Süre ve maliyetleri karşılaştırmak yer adını teknikleştirmeyi gerektirmez.
Bedel: Aynı aile içinde sayı özelliklerinin bağlamı denetlenir.
Görsel sonuç: Birimli rakamlar birlikte okunur; bütün ürün tabloya dönüşmez.

### İçerik ve durum matrisi

| İçerik veya durum | Font davranışı | Görsel kabul |
| --- | --- | --- |
| Türkçe yer adı | Sistem sans; gerçek harfler | İ/ı ayrımı doğru |
| Uzun rota adı | Aynı aile; doğal sarılma | Kelime biçimi bozulmaz |
| Para aralığı | Gerekirse tabular rakam | Birim rakamdan kopmaz |
| AI gerekçesi | Ortak gövde ailesi | İkinci otorite fontu yok |
| Koyu tema | Aynı aile ve roller | Işık saçan ince çizgi yok |
| Büyük metin | Yerel ölçekle büyüme | Glifler kırpılmaz |
| Yedek aile | Uyumlu metrik ve dil kapsamı | Etiket aniden taşınmaz |
| İç admin | Ortak font ve kritik gövde | Yoğunluk için 12 tb gövde yok |

### İyi ve kötü yazılı örnekler

| Bağlam | İyi örnek | Kötü örnek | Sonuç |
| --- | --- | --- | --- |
| Yer adı | “Çınarlık” Türkçe gliflerle | “CinarIik” benzeri yedek bozulma | Kimlik okunamaz |
| Eylem | 600 ağırlıkta açık etiket | İnce, sıkıştırılmış marka yazısı | Kontrolün anlamı zayıflar |
| Süre | “35–50 dk” birlikte | Rakam monospace, birim uzak | Tahminin kapsamı kopar |
| Destek metni | Sistem sans normal gövde | Uzun italik açıklama | Göz takibi zorlaşır |
| Premium | Ortak bilgi fontu | Daha pahalı aileyle güven vurgusu | Bilgi eşitliği şüpheli görünür |

### Neden ve sonuç değerlendirmesi

Sistem fontu ürünün anonim görünmesini zorunlu kılmaz.
Tutarlı hiyerarşi, doğru boşluk ve yalın dil aynı aileye karakter verir.
Özel fontun olmaması yer fotoğraflarının gerçekliğini öne çıkarabilir.
Bu bir performans ölçümü veya marka araştırması sonucu olarak sunulmaz.
Aileler arasında çok küçük farkların eşitlenmesi bütün incelemeyi tüketmemelidir.
Önce kelimenin tanınması ve kontrol etiketinin okunması değerlendirilir.
Yanlış harf ve kesilme, sadece optik incelik eksikliğinden daha ciddi kusurdur.
Yazı ailesi kullanıcı seçimini veya motor sırasını yeniden yorumlamaz.

### İnceleme sınırı

Font lisansına ilişkin yeni tedarik kararı verilmez.
Örnek cümleler kısa ve uzun yer kimliklerini birlikte içermelidir.
Desteklenen her alfabenin yedek yolu ayrıca incelenmelidir.
Kalın metin ayarı açıkken etiketin kutuya sığdığı kontrol edilmelidir.
Sistem sürümü değişince erişilebilirlik sonucu otomatik varsayılmamalıdır.
Mevcut sayısal ölçek font beğenisiyle sessizce değiştirilemez.

### Bölüm sonu öz eleştiri

- **Öz eleştiri Ö22.1 — Sistem sans kararı marka tanınmasını sınırlayabilir; bunun telafisi gereksiz süs değil tutarlı görsel işçiliktir.**

- **Öz eleştiri Ö22.2 — Optik ağırlık incelemesi kişisel zevke dönüşebilir; örnekler aynı görev ve metinlerle karşılaştırılmalıdır.**

- **Öz eleştiri Ö22.3 — Yedek aileler nadir karakterlerde fark yaratabilir; yalnız Türkçe temel sözcüklerle yetinmek kapsamdaki diğer adları dışlayabilir.**

## Satır Yüksekliği

Satır yüksekliği, metnin nefes alma ve izlenme mesafesidir.
Şamandıra'nın mevcut boyut/satır çiftleri korunur.
Bu değerler içerik kabının sabit yüksekliği değildir.
İddia ve kapsamın birlikte okunması satır ritminin temel amacıdır.
Dar ekran daha sıkışık metin üretme izni vermez.

### Kapsam ve görsel karar

Gövde 16/24, ikincil metin 14/20 ve caption 13/20'dir.
Vurgulu gövde 18/28, kart başlığı 20/28 kullanır.
Bölüm başlığı 24/32; normal sayfa başlığı 32/40'tır.
Dar sayfa başlığının kabul edilmiş karşılığı 28/36'dır.
Büyük anlatı 40/48; dar anlatı 32/40 kalır.
Etiket 16/24 kullanarak gövdeyle ritim ilişkisini sürdürür.
Satırlar arası boşluk paragraf ve grup aralığının yerine geçmez.
Kullanıcı satır aralığını büyüttüğünde kesilme oluşmamalıdır.

### Tasarım ilkeleri

#### İlke V23.1 — Boyut ve satır yüksekliği bir çift olarak uygulanır.

Gerekçe: Boyutu koruyup satırı sıkıştırmak aynı tipografi rolünü korumaz.
Bedel: Dolu kartlarda daha uzun içerik alanı gerekebilir.
Görsel sonuç: 16/24 rolü her gövde örneğinde benzer okuma ritmi taşır.

#### İlke V23.2 — Türkçe üst ve alt uzantılar kırpılmaz.

Gerekçe: Ğ, İ ve ş gibi biçimler satır sınırından etkilenebilir.
Bedel: Optik dikey ortalama bazen kutu merkezinden farklı görünür.
Görsel sonuç: Metin tabanı ve glif alanı birlikte değerlendirilir.

#### İlke V23.3 — Çok satırlı etiket yükselebilir.

Gerekçe: Uzun fiili kısaltmak işlemin kapsamını belirsizleştirebilir.
Bedel: Yan yana kontrollerin boyları yeniden akış gerektirebilir.
Görsel sonuç: Eylem metni sarılır; hedefin içinde sıkışmaz.

#### İlke V23.4 — Yakın anlamlar satır ritmiyle koparılmaz.

Gerekçe: Gerekçeyi sınırdan uzaklaştırmak olumlu okumayı tek başına bırakır.
Bedel: Her açıklamaya geniş editoryal boşluk verilemez.
Görsel sonuç: Aynı iddia bütünlüğü mevcut 8–12 tb ilişkisiyle korunur.

#### İlke V23.5 — Kullanıcı aralık tercihi görsel sistemin üst sınırı değildir.

Gerekçe: Kişisel okunabilirlik ihtiyacı normal ölçeği aşabilir.
Bedel: Sabit kompozisyonların görünümü değişebilir.
Görsel sonuç: Kutular büyür; içerik örtülmez veya düşürülmez.

### Durum ve metin matrisi

| Durum | Görsel karşılık | Kaçınılan sonuç |
| --- | --- | --- |
| Tek satır gövde | 16/24 | Sahte dikey ortalama |
| Üç satır gerekçe | Aynı 24 tb ritim | Son satırın kırpılması |
| Uzun kritik sınır | Gövde rolünde doğal büyüme | Caption'a düşürme |
| İki satır başlık | Kendi başlık çiftinin korunması | Satırların birbirine yaklaşması |
| Çok satır etiket | 16/24 ve büyüyen kontrol | 48 tb içine zorla sığdırma |
| Büyük kullanıcı aralığı | İçerikle büyüyen yüzey | Taşan yazının gizlenmesi |
| Koyu tema | Aynı ritim ve içerik | Tema için sıkıştırma |
| Yoğun yardımcı tablo | İzinli 14/20 | Kritik alanı küçültme |

### İyi ve kötü yazılı örnekler

| Bağlam | İyi örnek | Kötü örnek | Neden |
| --- | --- | --- | --- |
| Erişim sınırı | İki satırda açık gövde | Tek dar satıra sıkıştırma | Kritik bilgi taranamaz |
| Yer adı | İkinci satır aynı başlık ritminde | İkinci satır daha küçük | Kimlik hiyerarşisi bozulur |
| Buton | Tam “Değişiklikleri uygula” etiketi | Satır yüksekliğini yarıya indirme | Dokunma alanı kalabalıklaşır |
| Fotoğraf açıklaması | 13/20 okunabilir caption | 13/13 sık satırlar | Harf uzantıları çarpışır |
| Rota notu | Paragraf ilişkisiyle ayrılan metin | Her satırda ayrı büyük boşluk | Bir cümle farklı konular sanılır |

### Neden ve sonuç değerlendirmesi

Satır yüksekliği yalnız ferahlık aracı değildir.
Ardışık satırların birbirine ait olduğunu da hissettirir.
Aşırı geniş aralık kısa uyarıyı bağımsız satır yığınına çevirebilir.
Aşırı dar aralık ise uzun yer adını tek koyu şekle dönüştürebilir.
Mevcut ölçeğin korunması bu iki risk arasında ortak başlangıç sağlar.
Gerçek dil örnekleriyle görsel kontrol hâlâ gereklidir.
Paragraf boşluğunu artırmak her zaman daha iyi okunma getirmez.
Aynı görevde bütün değişkenler birlikte değerlendirilmelidir.

### İnceleme sınırı

Normal aralıklar ölçülmüş evrensel optimum diye sunulmaz.
Gerçek aygıt ve kullanıcı tercihi bunların algısını değiştirebilir.
Kart, sheet ve dialog aynı metnin kesilmediğini ayrı ayrı göstermelidir.
Yatay kullanımda dikey alan azlığı aralık azaltma gerekçesi olmaz.
Sabit eylem alanının örttüğü son satır kabul edilmez.
Yüklenme sonrası gelen uzun metin kendi alanını büyütebilmelidir.

### Bölüm sonu öz eleştiri

- **Öz eleştiri Ö23.1 — Sayısal çiftlerin korunması bütün yazı sistemlerinde aynı rahatlığı sağlamayabilir; dil örnekleriyle optik inceleme gerekir.**

- **Öz eleştiri Ö23.2 — Satırları ferah tutmak tek elle kullanımda kaydırmayı artırabilir; tekrar metin azaltılmalı, kritik aralıklar sıkıştırılmamalıdır.**

- **Öz eleştiri Ö23.3 — Büyüyen etiketler eylem grubunu ağırlaştırabilir; görsel öncelik metin kesmeden ortak kontrol düzeninde korunmalıdır.**

## Harf Aralıkları

Harf aralığı Şamandıra'da görünür bir süsleme yöntemi değildir.
Sistem fontunun doğal metin ritmi başlangıç kabulüdür.
Bu bölüm yeni bir sayısal tracking ölçeği açmaz.
Amaç kelime şekillerini ve Türkçe karakter ayrımlarını korumaktır.
Küçük yazıyı açarak premium gösterme yaklaşımı kullanılmaz.

### Kapsam ve görsel karar

10 Design System küçük metinde harfleri açmayı ana dil olarak reddeder.
Tamamı büyük harf başlık ve etiket düzeni varsayılan değildir.
Harf aralığı kelimeyi sığdırmanın gizli yolu olamaz.
Uzun adların çözümü doğal sarılmadır.
Tabular rakam kullanımı metnin harf aralığını değiştirmez.
Rota süresi ve birimi tek anlam birimi olarak korunur.
Kullanıcı kendi metin aralığını değiştirdiğinde içerik büyüyebilir.
Görsel tercih yerel yazı yönü ve doğal bağları bozmaz.

### Tasarım ilkeleri

#### İlke V24.1 — Doğal harf aralığı varsayılan olarak korunur.

Gerekçe: Sistem ailesinin kelime biçimleri günlük okumaya uygun ortak tabandır.
Bedel: Logotip benzeri özel bir metin dokusu her başlığa taşınmaz.
Görsel sonuç: Gövde sade, tanıdık ve kesintisiz okunur.

#### İlke V24.2 — Küçük metin dekoratif genişletilmez.

Gerekçe: Harfleri açılmış kısa etiket kelime olarak daha zor taranabilir.
Bedel: Lüks moda markalarına benzeyen etiket görünümü kullanılmaz.
Görsel sonuç: Caption ve yardımcı bilgi sözcük bütünlüğünü korur.

#### İlke V24.3 — Sığdırma için negatif sıkıştırma yapılmaz.

Gerekçe: Alan sorunu harf biçimini bozarak çözülürse ad ayrımı zayıflar.
Bedel: Uzun başlık birden fazla satır kullanabilir.
Görsel sonuç: Aynı yer adı bütün yüzeylerde aynı kelime karakterini taşır.

#### İlke V24.4 — Büyük harf yerel dil kurallarıyla sınırlıdır.

Gerekçe: Türkçe İ ve I dönüşümleri kimlikte anlamlı fark yaratır.
Bedel: Tüm dillere tek dekoratif başlık işlemi uygulanamaz.
Görsel sonuç: Özel adlar ve kullanıcı adlandırması korunur.

#### İlke V24.5 — Kullanıcı aralık ayarı taşmayı gizleyemez.

Gerekçe: Erişilebilir okuma için verilen tercih tüm bileşenlerde çalışmalıdır.
Bedel: Etiket genişliği ve satır sayısı değişir.
Görsel sonuç: Metin genişlerken kontrolün anlamı ve hedefi görünür kalır.

### İçerik ve durum matrisi

| İçerik veya durum | Görsel karar | Sınır |
| --- | --- | --- |
| Gövde | Ailenin doğal aralığı | Dekoratif açma yok |
| Kart başlığı | Doğal kelime şekli | Daraltarak tek satıra zorlama yok |
| Buton etiketi | Doğal cümle düzeni | Harf harf dizme yok |
| Caption | Normal okunabilir aralık | İnce büyük harf şeridi yok |
| Rakam aralığı | Birimle birlikte | Görsel boşlukla kapsam ayırma yok |
| Kullanıcı aralık tercihi | Yeniden akış | Taşmayı kırpma yok |
| Sağdan sola dil | Yazı sistemine uygun ritim | Harf bağlarını zorlama yok |
| Koyu tema | Aynı anlamsal aralık | Tema için geniş tracking yok |

### İyi ve kötü yazılı örnekler

| Bağlam | İyi örnek | Kötü örnek | Etki |
| --- | --- | --- | --- |
| Eylem | “Rotayı kaydet” doğal kelimeler | Harfleri açılmış tamamı büyük etiket | Fiil yavaş tanınır |
| Yer adı | Gerçek özel ad ve sarılma | Harfleri sıkıştırılmış tek satır | Benzer adlar karışır |
| Uyarı | Normal gövde cümlesi | Küçük ve aralıklı slogan | Koşul reklam sanılır |
| Süre | “20–30 dk” açık birim | Rakam ve birim arasında aşırı boşluk | Birim bağı kopar |
| Metadata | Doğal caption | Harf aralığıyla gizlenmiş düşük kontrast | İkincil bilgi kullanılamaz |

### Neden ve sonuç değerlendirmesi

Harf aralığının sakinliği metnin içerik olarak algılanmasını destekler.
Görsel gösteri azalınca anlamı taşıyan fiil öne çıkabilir.
Bunun gerçek okuma hızını artırdığı ölçülmeden iddia edilmez.
Başlıkta aşırı sıkıştırma ilk bakışta güçlü görünebilir.
Ancak uzun Türkçe ekler kapalı bir dokuya dönüşebilir.
Harfleri aşırı açmak da sözcük içi ilişkiyi gevşetebilir.
Bu iki uç yerine sistem ailesinin normal düzeni korunur.
Marka farkı doğal yer adlarını manipüle ederek üretilmez.

### İnceleme sınırı

Optik düzeltme gerekiyorsa tek örneğe değil tekrar eden role bakılmalıdır.
Yeni sayısal değer bu belgede kabul edilmiş token yerine geçirilmez.
Kullanıcının harf ve kelime aralığı birlikte değiştirilerek incelenmelidir.
Uzun etiketler yalnız kısa Türkçe örneklerle doğrulanmamalıdır.
Adres, tarih ve telefon gibi karma içerikler ayrıca okunmalıdır.
Yazı ailesi değişikliği olmadan sahte dar font etkisi yaratılmamalıdır.

### Bölüm sonu öz eleştiri

- **Öz eleştiri Ö24.1 — Doğal aralığa bağlılık bazı büyük başlıklarda optik pürüz bırakabilir; bunun düzeltilmesi yeni genel tracking ölçeği gerektirmez.**

- **Öz eleştiri Ö24.2 — Sıkıştırma yasağı uzun adlarda yüksek kartlar doğurabilir; isim bütünlüğü korunarak yardımcı tekrar azaltılmalıdır.**

- **Öz eleştiri Ö24.3 — Türkçe odaklı inceleme bağlanan yazı sistemlerini yeterince temsil etmeyebilir; desteklenen diller ayrı örneklenmelidir.**

## Başlık Sistemi

Başlık sistemi mevcut sayfa ve görevlerin adını görünür kılar.
Yeni gezinme ailesi, yeni portal veya yeni ekran oluşturmaz.
Görsel boyut ile anlamsal başlık düzeyi aynı kavram değildir.
Bir sheet başlığı kendi görevini tanımlar; yeni ana sayfa sayılmaz.
Başlığın gösterişi içeriğin karar değerinden daha baskın olamaz.

### Kapsam ve görsel karar

10 Design System §11 ve B35 başlık sözleşmesi korunur.
Gerçek yer adı ayırt edici şube veya konumla birlikte okunur.
Başlıkta genel üstünlük, yıldız veya uygunluk yüzdesi bulunmaz.
Uzun ad satıra sarılır; kimlik ayrımı üç noktayla kaybolmaz.
Görsel ölçü sayfa, bölüm veya kart rolünden gelir.
Düzenleme kontrolü başlığın parçası gibi görünmez.
Marka adı mevcut görevin adını sürekli bastırmaz.
Hata ve boş durum başlıkları kullanıcının işini somut adlandırır.

### Tasarım ilkeleri

#### İlke V25.1 — Başlık görevin veya yerin gerçek adını taşır.

Gerekçe: Kullanıcı mevcut bağlamını kısa bakışla tanıyabilmelidir.
Bedel: Pazarlama cümlesi başlık alanını sahiplenemez.
Görsel sonuç: Kimlik ve somut görev adı ilk okunabilir işarettir.

#### İlke V25.2 — Başlık seviyeleri içerik ilişkisini izler.

Gerekçe: Görsel büyüklük bilgi mimarisinin yerine geçemez.
Bedel: Sadece estetik amaçla düzey atlamak mümkün değildir.
Görsel sonuç: Sonuç kartı bölümün altında okunur.

#### İlke V25.3 — Yer adında ayırt edici bilgi korunur.

Gerekçe: Aynı adlı şubeler arasında fotoğraf tek başına yeterli ayrım sağlamaz.
Bedel: Bazı kimlik blokları iki veya daha çok satır gerektirir.
Görsel sonuç: Şube ya da ilçe adı okunamaz son ek haline gelmez.

#### İlke V25.4 — Başlığa eklenen eylem ayrı kontrol olarak görünür.

Gerekçe: Adı okumak ile kaydı değiştirmek farklı kullanıcı niyetleridir.
Bedel: Başlık çevresinde yeterli hedef ve boşluk ayrılır.
Görsel sonuç: Düzenle veya kapat işareti metinle çakışmaz.

#### İlke V25.5 — Durum başlığı sonucu abartmadan anlatır.

Gerekçe: “Hazır” gibi genel bir başlık kayıt ile uygunluğu karıştırabilir.
Bedel: Duruma özgü kısa metinlerin bakımı gerekir.
Görsel sonuç: Bekleme, hata ve boşluk kendi gerçek kapsamıyla adlandırılır.

### Başlık ve durum matrisi

| Bağlam | Görsel başlık rolü | Korunacak anlam |
| --- | --- | --- |
| Yer | Sayfa başlığı | Gerçek ve ayırt edici kimlik |
| Sonuç kartı | 20/28 kart başlığı | Tek sonuç birimi |
| Rota taslağı | Bağlamdaki görev başlığı | Kişisel ad; uygunluk onayı değil |
| Yardımcı bölüm | 24/32 bölüm başlığı | İlgili içerik grubu |
| Sheet | Görevi tanımlayan mevcut rol | Yeni portal değil |
| Boş kayıt | Neden belirten başlık | Kullanıcı eksikliği değil |
| Kayıt belirsizliği | Sonucun doğrulanamadığını anlatan başlık | Kesin başarısızlık değil |
| Kritik değişiklik | Etkilenen koşulu adlandıran başlık | Bütün günün iptali değil |

### İyi ve kötü yazılı örnekler

| Bağlam | İyi örnek | Kötü örnek | Neden |
| --- | --- | --- | --- |
| Rota | “Sahil günü” ve ayrı değerlendirme durumu | “Kusursuz günün hazır” | Kişisel ad güvenceye dönüşür |
| Yer | Gerçek yer adı ve şube | “Şehrin en iyi durağı” | Kimlik yerine üstünlük satılır |
| Boş kayıt | “Henüz kaydettiğin yer yok” | “Gezi profilini tamamla” | Boşluk borç gibi sunulur |
| Paylaşım | “Paylaşılacak içerik” | “Arkadaşlarını etkile” | Kapsam yerine sosyal baskı kurulur |
| Hata | “Kaydı doğrulayamadık” | “Her şey kayboldu” | Bilinmeyen kesinleştirilir |

### Neden ve sonuç değerlendirmesi

Başlık sabitliği geri dönen kişinin bağlamını tanımasına yardım eder.
Görsel vurgu değişebilir; bütün içerik sırası sürekli oynamaz.
Kısa görev adı metnin konusunu açıklayabiliyorsa yeterlidir.
Kısalık kritik kimlik kaybına yol açıyorsa başlık uzar.
Aynı adı paylaşan yerlerde konum metni değersiz metadata değildir.
Şube ayrımı kullanıcının kararını değiştiren kimlik bileşenidir.
Bir gün adının samimiyeti sistemin o gün gerçekleştiğini iddia etmez.
Başlık tasarımı kaydetme, ziyaret ve katkı ayrımını silmez.

### İnceleme sınırı

Başlık örnekleri gerçek uzunluk aralığını kapsamalıdır.
Koyu tema ve büyük yazıda eylemler adın sonuna taşmamalıdır.
Başlıkla beraber okunan alt açıklamanın ilişki mesafesi korunmalıdır.
Uzun görev adı için yeni küçük font türetilmemelidir.
Etiketlenmiş örnek metin gerçek bir mekân hakkında bilgi beyanı değildir.
Mevcut başlık sırası bu belgeyle yeniden tasarlanmamıştır.

### Bölüm sonu öz eleştiri

- **Öz eleştiri Ö25.1 — Somut başlıklar fazla düz görünebilir; sıcaklık doğruluk kaybetmeyen alt açıklamada kurulmalıdır.**

- **Öz eleştiri Ö25.2 — Uzun kimlik satırları ilk görünümü büyütebilir; şube ayrımını silmek bu maliyetin kabul edilebilir çözümü değildir.**

- **Öz eleştiri Ö25.3 — Aynı görsel rol farklı anlamsal seviyelerde yanlış uygulanabilir; başlık ilişkisi yalnız boyut tablosuyla doğrulanmamalıdır.**

## Buton Dili

Buton görünümü kullanıcının başlayacağı işlemi açık biçimde adlandırır.
10 Design System B11'in birincil, ikincil, üçüncül ve tehlikeli varyantları korunur.
Buton sayısı veya konumu üzerinden yeni bir kullanıcı akışı kurulmaz.
Görsel vurgu mevcut görevin eylem önceliğini taşır.
Bir butonun yeşil olması seçimin doğru yer olduğu anlamına gelmez.

### Kapsam ve görsel karar

Birincil varyant kabul edilmiş eylem zemini ve metin eşleşmesini kullanır.
İkincil varyant sınırlı veya çerçeveli yüzey olarak okunur.
Üçüncül varyant metin ağırlıklıdır; görünmez değildir.
Kontrol radius'u 8 tb; yatay iç boşluk başlangıcı 16 tb'dir.
Varsayılan etkileşim hedefi en az 48 × 48 tb'dir.
Küçük kontrolün ürün alt sınırı 44 × 44 tb olarak korunur.
Etiket 16/24 ve 600 ağırlık hedefini kullanır.
Bekleme durumunda etiketin ve hedefin alanı kararlı kalır.

### Tasarım ilkeleri

#### İlke V26.1 — Birincil buton rolü bir etkin görevin baskın işlemine ayrılır.

Gerekçe: Birden fazla eşit vurgu kararın hangi soruya ait olduğunu dağıtır.
Bedel: Her özellik kendi güçlü renkli çağrısını alamaz.
Görsel sonuç: Kullanıcı mevcut ana işlemi kısa bakışla ayırabilir.

#### İlke V26.2 — Buton metni fiil ve gerçek kapsamla okunur.

Gerekçe: Genel bir “Devam” görünümü yanlış işlem beklentisini örtebilir.
Bedel: Bazı etiketler daha geniş veya çok satırlı olabilir.
Görsel sonuç: İşlem nesnesi süsleme lehine kaybolmaz.

#### İlke V26.3 — Hedef büyüklüğü ikon büyüklüğünden bağımsızdır.

Gerekçe: Küçük simge tek elle güvenli erişim için yeterli hedef sağlamaz.
Bedel: İkonlu kontroller de anlamlı yer kaplar.
Görsel sonuç: 16–24 tb ikon, 48 tb hedefin içinde dengelenir.

#### İlke V26.4 — Bekleyen buton önceki kontrolün kimliğini korur.

Gerekçe: Aniden daralan veya kaybolan kontrol tekrar basma eğilimi yaratır.
Bedel: Bekleme etiketi için içerik alanı gözetilir.
Görsel sonuç: “Kaydediliyor” aynı eylem bağlamında okunur.

#### İlke V26.5 — Odak ve tehlike yalnız renk değişikliğiyle anlatılmaz.

Gerekçe: Renk algısı değiştiğinde kontrol anlamı korunmalıdır.
Bedel: Açık etiket ve odak sınırı görsel alan kullanır.
Görsel sonuç: Odak 2 tb halka ve 2 tb ayrımla algılanır.

### Buton durum matrisi

| Durum | Görsel karşılık | Korunan sınır |
| --- | --- | --- |
| Normal birincil | Kabul edilmiş dolu eylem eşleşmesi | Uygunluk rengi değil |
| Normal ikincil | Sınır ve açık metin | Çıkış görünmez olmaz |
| Üçüncül | Okunabilir metin ve hedef | Silik dipnot olmaz |
| Odaklı | 2 tb halka; 2 tb ayrım | Halka kırpılmaz |
| Basılı | Aynı okunabilir çift ve durum göstergesi | Alfa düşürerek okunmazlık yok |
| Bekleyen | Yerinde gerçek işlem etiketi | Erken başarı yok |
| Devre dışı | Kullanılamama durumu ve yakın neden | Sebep yalnız tooltip'te değil |
| Tehlikeli | Hata/tehlike rolü ve açık fiil | Yalnız kırmızı ikon değil |

### İyi ve kötü yazılı örnekler

| Bağlam | İyi örnek | Kötü örnek | Etki |
| --- | --- | --- | --- |
| Kayıt | “Rotayı kaydet” | “Mükemmel!” | İşlem anlaşılamaz |
| Kapatma | “Bağlantıyı kapat” | İsimsiz kırmızı çarpı | Kapsam belirsizleşir |
| Bekleme | “Kaydediliyor” aynı hedefte | Buton yerine yeşil onay | Sonuç erken ilan edilir |
| İkincil yol | Okunabilir “Vazgeç” | Zeminle birleşen minik metin | Baskısız çıkış kaybolur |
| Uzun etiket | Sarılan 16/24 etiket | 11 tb'ye küçültülmüş etiket | Okunabilirlik bozulur |

### Neden ve sonuç değerlendirmesi

Kontrolün hacmi rolü anlatır; yerin parasal değerini anlatmaz.
Birincil eylem rengi ile başarı rengi aynı değeri paylaşabilir.
Anlamsal rollerin ayrı olması görsel yorumda korunmalıdır.
Buton üzerindeki gölge sıradan karttan üstünlük hissi taşımamalıdır.
Hover için bütün kartı yükseltmek buton dilinin parçası değildir.
Metin ve sınır okunabiliyorsa düşük dekor düzeyi yeterli olabilir.
Farklı platformların yerel kontrolleri aynı işlem anlamını taşımalıdır.
Erişilebilir yerel kontrolün kullanımı marka ihlali sayılmaz.

### İnceleme sınırı

Butonlar açık, koyu ve yüksek kontrast durumlarında birlikte ele alınmalıdır.
Görsel hedefin çevresinde görünmeyen çakışan alan bulunmamalıdır.
Klavye açıldığında eylem etiketi örtülmemelidir.
Kullanıcı metni büyüttüğünde kontrol boyu artabilmelidir.
Salt okunur bilgi yanlışlıkla devre dışı buton gibi sunulmamalıdır.
Bu görsel tarif yeni bir onay veya gönderim davranışı eklemez.

### Bölüm sonu öz eleştiri

- **Öz eleştiri Ö26.1 — Tek baskın buton alternatifleri psikolojik olarak zayıflatabilir; ikincil yolların gerçekten bulunabilirliği değerlendirilmelidir.**

- **Öz eleştiri Ö26.2 — Geniş hedefler dar yüzeyde ağır görünebilir; çözüm eylem kapsamını sadeleştirmek, hedefi küçültmek değildir.**

- **Öz eleştiri Ö26.3 — Bekleme etiketinin sabit alanda kalması uzun çevirileri sıkıştırabilir; sabit genişlik yerine kararlı ve büyüyebilen alan aranmalıdır.**

## CTA Kuralları

CTA mevcut işin sonucunu anlaşılır biçimde teklif eder.
Görsel dil yeni çağrı, satış adımı veya kayıt zorunluluğu oluşturmaz.
Kullanıcıya hangi seçimin geçerli olduğunu renk değil gerçek ihtiyaç gösterir.
Başat eylemin görünürlüğü diğer hakların okunabilirliğiyle birlikte değerlendirilir.
Özenli çağrı, acele ettiren çağrı anlamına gelmez.

### Kapsam ve görsel karar

08 Tasarım İlkeleri §27 ve 10 Design System B11 esas alınır.
Bir etkin görevde baskın devam mevcut akıştan devralınır.
Reddetme, düzeltme ve çıkış metinleri açık biçimde okunur.
CTA etiketi eylemin nesnesiyle birlikte anlaşılır olmalıdır.
Sahte kıtlık ve geri sayım görsel dilin parçası değildir.
Premium ek kolaylığı temel karar çağrısını devralamaz.
Ücretsiz yol daha düşük bilgi kontrastıyla sunulmaz.
Eylem, ilgili kapsam açıklamasından görsel olarak koparılmaz.

### Tasarım ilkeleri

#### İlke V27.1 — CTA vurgu düzeyi mevcut görev önceliğinden gelir.

Gerekçe: Ticari veya dekoratif hedef kullanıcının niyetini değiştiremez.
Bedel: Her yüzeyde rota oluşturma veya Premium çağrısı bulunmaz.
Görsel sonuç: Tek yer kararı kendi doğal devamıyla okunur.

#### İlke V27.2 — Etiket sonucu tahmin etmeye yetecek açıklıktadır.

Gerekçe: Kullanıcı gösterişli bir sözcükten işlem kapsamı çıkarmamalıdır.
Bedel: Kısa slogan yerine daha somut metin alanı gerekir.
Görsel sonuç: “Değişiklikleri uygula” gibi kapsamlı fiiller korunur.

#### İlke V27.3 — Vazgeçme yolu görsel olarak cezalandırılmaz.

Gerekçe: Minimalizm kullanıcının iradesini azaltamaz.
Bedel: Baskın eylemin karşısında okunabilir bir alternatif kalır.
Görsel sonuç: Çıkış etiketi küçültülmüş veya düşük kontrastlı değildir.

#### İlke V27.4 — Kapsam açıklaması çağrının yakınında kalır.

Gerekçe: Paylaşım gibi işlemlerde bedel uzak dipnotta görülmeyebilir.
Bedel: Eylem bölgesi tek düğmeden daha fazla içerik taşır.
Görsel sonuç: Somut sonuç ve ilgili kontrol aynı okuma birimindedir.

#### İlke V27.5 — Aciliyet görünümü gerçek ve yetkili anlamı aşamaz.

Gerekçe: Hareket, sayaç ve yoğun renk kararın zaman baskısını uydurabilir.
Bedel: Pazarlama hızlandırıcıları kullanılmaz.
Görsel sonuç: Kullanıcı kendi hızında devam eder veya ayrılır.

### CTA durum matrisi

| Bağlam | Görsel öncelik | Sınır |
| --- | --- | --- |
| Arama gönderimi | Mevcut ana eylem | Profil tamamlama çağrısı eklenmez |
| Rota düzenleme | Mevcut değişiklik işlemi | Yeni gezi tamamlama baskısı yok |
| Paylaşım önizlemesi | Somut kapsamla ilişkili eylem | Özel bilgi dipnota gizlenmez |
| Sonuç yok | İlgili tek düzeltme veya açıklama | Koşul sessizce gevşetilmez |
| Kayıt başarısı | Sonucu gösteren sakin durum | Otomatik yeni görev açılmaz |
| Hata | Gerçek kurtarma yolu | Premium çözüm çağrısı yok |
| Vazgeçme | Okunabilir ikincil kontrol | Silik veya utandırıcı dil yok |
| Ücretli kolaylık | Mevcut kapsam içinde açıklama | Daha güvenilir karar vaadi yok |

### İyi ve kötü yazılı örnekler

| Bağlam | İyi örnek | Kötü örnek | Neden |
| --- | --- | --- | --- |
| Boş sonuç | “Koşulları düzenle” | “Daha iyi sonuç için yükselt” | Bilgi açığı satılamaz |
| Günlük plan | “Taslağı kaydet” | “Gününü tamamla” | Taslak tamamlanma borcu değildir |
| Çıkış | “Vazgeç” | “Fırsatı kaçır” | Karar baskısı oluşturur |
| Paylaşım | “Bağlantı oluştur” gerçek kapsamla | “Hemen herkese duyur” | Açık paylaşım iradesi aşılır |
| Dış yönlendirme | “Yol tarifi aç” | “Ziyareti tamamla” | Uygulama açılması ziyaret değildir |

### Neden ve sonuç değerlendirmesi

CTA'nin okunabilirliği dönüşüm oranıyla tek başına ölçülmez.
Kullanıcı ne olacağını doğru anlayıp vazgeçiyorsa çağrı yine işini yapmış olabilir.
İlgili açıklamayı yakın tutmak işlemi daha uzun gösterir.
Bu bedel yanlış kapsamla ilerleme riskini azaltmayı amaçlar.
Doğru eylem etiketi yeni bir akış yaratmaz.
Mevcut işlemin görünür sözüyle gerçek sonucunu eşleştirir.
CTA hiyerarşisi yerlerin motor sırasını yeniden düzenleyemez.
Fotoğrafı çekici olan kartın eylemi bu nedenle daha güçlü yapılmaz.

### İnceleme sınırı

Çağrı ve ret yolları aynı görev örneğinde birlikte incelenmelidir.
Tek elle erişim değerlendirmesi yalnız baskın düğmeyle sınırlanmamalıdır.
Kritik açıklamanın eylemden önce okunabilir olduğu görülmelidir.
İki satırlı etiket bir satır uğruna anlamını kaybetmemelidir.
Hata durumunda yeni üyelik engeli varmış gibi görünüm kurulmamalıdır.
Bu bölüm fiyat, paket veya satış akışı belirlemez.

### Bölüm sonu öz eleştiri

- **Öz eleştiri Ö27.1 — Somut etiketler bazı küçük görevlerde gereğinden uzun olabilir; nesne zaten açıkken yinelenen ifade azaltılabilir.**

- **Öz eleştiri Ö27.2 — Sakin CTA başlangıçta fark edilmeyebilir; bunun çözümü kontrolü tanınır kılmak, yapay aciliyet eklemek değildir.**

- **Öz eleştiri Ö27.3 — Açıklamayla eylemin yakınlığı mahrem bilgiyi yoğunlaştırabilir; mevcut paylaşım sınırı korunarak yalnız gerekli kapsam gösterilmelidir.**

## Icon Felsefesi

İkon Şamandıra'da metni destekleyen tanıma işaretidir.
Bir yerin genel kalitesini veya AI'nin doğruluğunu onaylayan sembol değildir.
Mevcut B33 sözleşmesi tek çizim ailesi ve tutarlı optik ağırlık ister.
Bu belge ikon dosyası, yeni sembol veya logo üretmez.
Anlamı belirsiz işlerde görünür metin korunur.

### Kapsam ve görsel karar

Varsayılan çizgi ikon ailesi kullanılır.
Dolu karşılık yalnız tanımlı seçili durumda yer alabilir.
Arama, kapatma ve kaydetme aynı anlamla tekrar eder.
Kaydetme beğeni veya ziyaret simgesine dönüştürülmez.
Yıldız, kalp, kalkan ve genel onay işaretlerinin çağrışımı sınırlandırılır.
Fiziksel erişim simgesi bütün yerin erişilebilir olduğunu tek başına söylemez.
Dekoratif ikon ayrı bilgiymiş gibi öne çıkmaz.
Yerel yön simgeleri yazı yönü bağlamında değerlendirilir.

### Tasarım ilkeleri

#### İlke V28.1 — Aynı ikon aynı anlam için kullanılır.

Gerekçe: Kullanıcı yüzey değiştikçe yeni simge sözlüğü öğrenmemelidir.
Bedel: Her içerik türüne ayrı dekoratif simge seçilemez.
Görsel sonuç: Kontrol ailesi sayfalar arasında tanınabilir kalır.

#### İlke V28.2 — Görünür metin belirsizliği gideren asıl destektir.

Gerekçe: Bir sembolün tasarım ekibine tanıdık olması evrensel anlaşıldığını kanıtlamaz.
Bedel: Bazı kontroller ikon kadar küçük olamaz.
Görsel sonuç: Az tanınan ve kritik işlemler fiilleriyle birlikte görünür.

#### İlke V28.3 — İkon iddia kapsamını genişletemez.

Gerekçe: Tek rampa işareti bütün giriş ve dolaşım zincirini doğrulamaz.
Bedel: Özellik satırı kısa açıklamayla desteklenir.
Görsel sonuç: Fiziksel koşul, bilinen bölüm ve sınırıyla okunur.

#### İlke V28.4 — Seçili doluluk yalnız kullanıcı durumunu anlatır.

Gerekçe: Dolu işaretin başarı ve uygunlukla karışması yanlış güven yaratır.
Bedel: Doluluk için açık durum sözlüğü gerekir.
Görsel sonuç: Kaydedildi görünümü ziyaret edildi anlamı taşımaz.

#### İlke V28.5 — Tek ailede optik tutarlılık korunur.

Gerekçe: Farklı çizgi karakterleri aynı görevde gereksiz görsel gürültü üretir.
Bedel: Hazır kütüphanelerden rastgele ikon karıştırılamaz.
Görsel sonuç: Köşe, çizgi ve ağırlık ilişkisi ortak görünür.

### Anlam ve durum matrisi

| İkon bağlamı | Görsel karşılık | Yanlış çıkarım sınırı |
| --- | --- | --- |
| Ara | Tanıdık çizgi işaret ve adı | AI sohbeti zorunlu değildir |
| Kaydet | Kayıt anlamıyla tutarlı işaret | Beğeni değildir |
| Kapat | Görünür kontrol ve kapsamlı ad | Gönderilmiş işlemi geri almaz |
| Seçili öğe | Tanımlı doluluk veya seçim işareti | Yer üstünlüğü değildir |
| Fiziksel koşul | İkonla birlikte somut açıklama | Genel erişim garantisi değildir |
| Kritik uyarı | Metin ve durum rolü | Yalnız üçgen yeterli değildir |
| AI desteği | Ortak bilgi ailesi | Onay kalkanı yoktur |
| Geri yönü | Yerel yazı yönüne uyarlama | Harita coğrafyası aynalanmaz |

### İyi ve kötü yazılı örnekler

| Bağlam | İyi örnek | Kötü örnek | Neden |
| --- | --- | --- | --- |
| Kaydetme | Kayıt simgesi ve “Kaydet” | Kalp ve artan sayı | Sosyal beğeni çağrıştırır |
| Bilgi sınırı | İşaret yanında “Akşam bilgisi yok” | Yeşil kalkan | Genel güvence yaratır |
| Erişim | “Yan girişte rampa bilgisi var” | Tek sandalye simgesiyle tüm yer etiketi | Kapsam genişler |
| AI | Normal bilgi işareti gerekiyorsa | Parlayan yıldız ve “onaylı” | Yardımcı otoriteleşir |
| Kapatma | Tanınır çarpı ve erişilebilir ad | Soyut marka düğümü | Çıkış bulunamaz |

### Neden ve sonuç değerlendirmesi

İkonun küçük olması anlamının da küçük olduğu anlamına gelmez.
Kapatma gibi temel bir işlem tek işaretle görünse bile açık hedef taşır.
Dekoratif ikonların azalması kalan işaretlerin işini kolaylaştırabilir.
Ancak bütün ikonları kaldırmak tanıma avantajını gereksiz azaltabilir.
Seçim her görevde tanınma katkısına göre yapılır.
Bu katkı bir kullanıcı araştırması sonucuymuş gibi ilan edilmez.
Kütüphane veya lisans seçimi sonraki uygulama sorumluluğudur.
Bu belge o seçimi dosya ya da paket adıyla sabitlemez.

### İnceleme sınırı

İkonlar metinsiz yanlış yorum ihtimaliyle birlikte değerlendirilmelidir.
Açık ve koyu tema aynı simgenin algısını korumalıdır.
Gri ölçekte seçim ve hata ayrımı kalmalıdır.
Tek ikonlu kontrolün hedefi metinli kontrol kadar erişilebilir olmalıdır.
Coğrafi yön ve arayüz yönü birlikte aynalanmamalıdır.
Yer türü simgesi yeni kategori veya özellik ilan edemez.

### Bölüm sonu öz eleştiri

- **Öz eleştiri Ö28.1 — Metin desteği çok tekrar ederse küçük eylem alanları kalabalıklaşabilir; yalnız anlamlı destek korunmalıdır.**

- **Öz eleştiri Ö28.2 — Tek çizgi ailesi bazı kültürel işaretleri yeterince temsil etmeyebilir; aile uyumu anlam doğruluğundan önce gelemez.**

- **Öz eleştiri Ö28.3 — Dolu seçili ikon yine başarı sanılabilir; gerçek bağlam ve görünür durum metniyle yanlış yorum incelenmelidir.**

## İkon Boyutları

İkon boyutları mevcut 16, 20 ve 24 tb çizim kutularına bağlıdır.
Bu ölçüler etkileşim hedefi ölçüsü değildir.
Görsel kutu küçüldükçe ayrıntı da sade ve okunabilir kalmalıdır.
Yeni ara boyutlar içerik türlerine statü vermek için eklenmez; mevcut halka ve nokta marker kimliği korunur.
Tek elle kullanım hedefi ikon çevresindeki gerçek kontrol alanında korunur.

### Kapsam ve görsel karar

10 Design System B33 ile §55 birlikte uygulanır.
16 tb kısa satır içi destek için mevcut küçük kutudur.
20 tb orta yoğunluktaki metin ilişkilerine uygundur.
24 tb temel kontrol ailesinin görsel başlangıcıdır.
Bu eşleme her bileşende otomatik ikon zorunluluğu oluşturmaz.
Kontrol varsayılanı 48 × 48 tb'den küçük değildir.
Küçük kontrol alt sınırı 44 × 44 tb olarak kalır.
Karma girişli aygıtta fare varlığı hedef küçültme nedeni olmaz.

### Tasarım ilkeleri

#### İlke V29.1 — Çizim kutusu mevcut üç basamaktan seçilir.

Gerekçe: Tutarlı ölçek aynı işi farklı yüzeylerde tanınabilir kılar.
Bedel: Her kısa etiket için ayrı ikon ölçüsü bulunmaz.
Görsel sonuç: 16, 20 ve 24 tb arasında anlamlı rol farkı oluşur.

#### İlke V29.2 — İkonun görsel merkezi optik olarak dengelenir.

Gerekçe: Dairesel ve köşeli biçimler aynı kutuda eşit büyüklükte algılanmayabilir.
Bedel: Matematiksel ortalamaya ek görsel inceleme gerekir.
Görsel sonuç: İkon metin tabanına ve kontrol kütlesine uyumlu görünür.

#### İlke V29.3 — Dokunma hedefi çizim kutusundan ayrı korunur.

Gerekçe: 24 tb simge, 24 tb dokunma alanını meşru kılmaz.
Bedel: Küçük görünen kontrol çevresinde gerçek boşluk ayrılır.
Görsel sonuç: Yakın kontrollerin hedefleri birbirine karışmaz.

#### İlke V29.4 — Küçük kutuda ayrıntı okunabilirliği önceliklidir.

Gerekçe: Küçültülmüş karmaşık ikon anlamlı çizgilerini kaybedebilir.
Bedel: Görsel ailede küçük kutu için daha sade eşleme gerekebilir.
Görsel sonuç: İşaret bulanık lekeye veya kapalı siyah alana dönüşmez.

#### İlke V29.5 — Büyük metin ikon ilişkisini yeniden değerlendirir.

Gerekçe: Yazı büyüdüğünde küçük ikon bağımsız veya önemsiz görünebilir.
Bedel: Sabit satır yüksekliğiyle kusursuz tek hizalama korunamaz.
Görsel sonuç: İkon, etiket ve hedef birlikte okunabilir kalır.

### Boyut ve durum matrisi

| Bağlam | Çizim kutusu | Kontrol ve anlam sınırı |
| --- | --- | --- |
| Küçük satır içi destek | 16 tb | Kritik bilgi yalnız işaret olmaz |
| Orta metin ilişkisi | 20 tb | Metni gereksiz itmez |
| Temel ikonlu kontrol | 24 tb | Hedef varsayılanı 48 × 48 tb |
| Küçük yoğunluk kontrolü | Uygun mevcut kutu | Hedef alt sınırı 44 × 44 tb |
| Seçili durum | Aynı kutuda durum değişimi | Büyüme üstünlük anlatmaz |
| Harita kontrolü | Ortak kutu ve opak zemin | Atıf ve ölçek örtülmez |
| Büyük kullanıcı metni | Optik ilişki incelenir | Etiket kesilmez |
| Dekoratif ikon | Yalnız katkısı varsa | Daha büyük süs zorunlu değil |

### İyi ve kötü yazılı örnekler

| Bağlam | İyi örnek | Kötü örnek | Etki |
| --- | --- | --- | --- |
| Kapat | 24 tb simge; 48 tb hedef | 16 tb simge ve aynı hedef | Tek elle erişim zayıflar |
| Özellik satırı | 16 veya 20 tb destek | Gövdeden büyük rozet | Koşul üstünlük gibi görünür |
| Seçim | Aynı boyutta tanımlı işaret | Seçilen yerin ikonu iki kat büyür | Liste dengesi bozulur |
| Harita | Ortak kontrol ölçüsü | Dar alan için minik artı | Hareket alternatifi kullanılamaz |
| Büyük metin | İlişkisi korunan ikon | Metnin ortasında kayan küçük şekil | Etiketin bağı zayıflar |

### Neden ve sonuç değerlendirmesi

Üç boyut bakımda karşılaştırmayı kolaylaştırır.
Bu sayı ikonların her görevde aynı görünmesi zorunluluğu değildir.
Optik merkez küçük bir düzeltme gerektirebilir.
Mevcut 2 tb optik istisna yeni yoğunluk basamağına dönüşmez.
İkonun çevresindeki alan boş süs alanı değildir.
Hedeflerin ayrılmasını ve odak halkasının görünmesini sağlar.
Ölçü büyütülerek düşük kontrast telafi edilmiş sayılmaz.
Boyut, çizgi ve renk birlikte algılanabilir olmalıdır.

### İnceleme sınırı

Gerçek aygıtta ikonların keskinliği ve hedef ilişkisi incelenmelidir.
Ekran görüntüsündeki fiziksel piksel sayısı mantıksal birimle karıştırılmamalıdır.
Sağ ve sol elle kullanım aynı kontrol ailesinde ele alınmalıdır.
Bir simgenin içinde okunmaz harf veya sayı saklanmamalıdır.
Kontrol çevresindeki odak halkası kart kırpmasına girmemelidir.
Bu bölüm yeni ikon varyantı veya ikon dosyası oluşturmaz.

### Bölüm sonu öz eleştiri

- **Öz eleştiri Ö29.1 — Üç ölçü bazı özel geometrilerde yeterli optik tutarlılık sağlamayabilir; önce aile içi eşleme incelenmelidir.**

- **Öz eleştiri Ö29.2 — Görünmez hedef alanı kullanıcıya daha büyük görünmeyebilir; kontroller arası gerçek boşluk da korunmalıdır.**

- **Öz eleştiri Ö29.3 — Büyük metinle ikon ilişkisi tek bir sayı kuralına indirgenemez; satır ve hedef bütününde değerlendirme gerekir.**

## İkon Kalınlıkları

İkon kalınlığı tek çizim ailesinin optik ağırlığıyla yönetilir.
Mevcut belgeler bütün ikonlar için yeni evrensel stroke sayısı tanımlamaz.
Bu görsel dil de kabul edilmiş ölçeğin yerine keyfî bir kalınlık koymaz.
Başlangıç görünümü okunabilir çizgi ikonudur.
İncelik premium hissin zorunlu göstergesi değildir.

### Kapsam ve görsel karar

10 Design System B33'ün tutarlı optik ağırlık kararı esas alınır.
16, 20 ve 24 tb kutular aynı aile karakterini paylaşır.
Küçük kutudaki çizgi, büyüğün kör ölçeklenmiş karşılığı olmak zorunda değildir.
Doluluk yalnız tanımlı seçili durumun karşılığıdır.
Koyu tema çizgiyi ışık saçan ince hat haline getirmez.
Yüksek kontrastta işaretin anlamı gölgeye bağlı kalmaz.
Metin ağırlığıyla ikon ağırlığı birbirini bastırmamalıdır.
Tehlike anlamı sadece çizgiyi kalınlaştırarak verilmez.

### Tasarım ilkeleri

#### İlke V30.1 — Tek ailede tutarlı optik çizgi kullanılır.

Gerekçe: Rastgele kalınlıklar aynı eylemlere farklı önem yükler.
Bedel: Farklı kaynaklardan alınan ikonlar incelemesiz karıştırılamaz.
Görsel sonuç: Kontroller arasında sakin bir çizgi ritmi oluşur.

#### İlke V30.2 — İnce çizgi okunabilirlikten üstün tutulmaz.

Gerekçe: Dış ışıkta kaybolan simge zarif olsa da görevini yapamaz.
Bedel: Bazı ikonlar moda örneklerinden daha belirgin görünür.
Görsel sonuç: Kullanıcı normal ve koyu yüzeyde işareti ayırabilir.

#### İlke V30.3 — Boyutlar arasında algısal ağırlık korunur.

Gerekçe: Küçük ikonun kör ölçekle incelmesi tanınmayı zayıflatabilir.
Bedel: Ailenin her boyut karşılığı ayrı gözden geçirilir.
Görsel sonuç: 16 tb ikon büyük ikonun silik kopyası olmaz.

#### İlke V30.4 — Seçim dolulukla desteklenebilir; kapsamı değişmez.

Gerekçe: Dolu biçim kullanıcı seçimini hızlı anlatabilir fakat güvence değildir.
Bedel: Dolu ve çizgi eşleri aynı anlamla yönetilir.
Görsel sonuç: Durum değişir; ikonun nesnesi değişmez.

#### İlke V30.5 — Kalınlık metin ve sınırla birlikte değerlendirilir.

Gerekçe: İkonun tek başına okunması bütün kontrolün anlaşılması anlamına gelmez.
Bedel: İzole ikon beğenisi yeterli kabul ölçüsü olmaz.
Görsel sonuç: Etiket, ikon ve odak birbiriyle yarışmadan görünür.

### Ağırlık ve durum matrisi

| Durum | Görsel karar | Kabul edilmeyen sonuç |
| --- | --- | --- |
| Normal kontrol | Ailenin ortak çizgi ağırlığı | Her eylemde başka kalınlık |
| 16 tb kutu | Küçük ölçekte ayırt edilebilir çizgi | Saç teli benzeri kaybolma |
| 24 tb kutu | Ortak algısal ağırlık | Kalın lekeye dönüşme |
| Seçili | Tanımlı dolu veya seçim işaretli durum | Ziyaret/başarı anlamına kayma |
| Odaklı | Aynı ikon ve ayrı odak halkası | İkonu kalınlaştırmayı tek odak sayma |
| Koyu tema | Aynı rol ve okunabilir eşleşme | Beyaz parıltı efekti |
| Tehlikeli işlem | Durum rengi ve somut etiket | Ağır çizgiyi uyarı sayma |
| Devre dışı | Durum ve açıklama birlikte | Çizgiyi görünmezleştirme |

### İyi ve kötü yazılı örnekler

| Bağlam | İyi örnek | Kötü örnek | Etki |
| --- | --- | --- | --- |
| Eylem grubu | Benzer optik ağırlıktaki işaretler | Biri ince, biri dolu, biri kabartmalı | Gereksiz önem farkı oluşur |
| Dış ortam | Belirgin çizgi ve okunabilir etiket | Aşırı ince gri ikon | Tanıma zayıflar |
| Seçim | Aynı nesnenin tanımlı dolu karşılığı | Yer ikonunu kalkana çevirmek | Güven onayı algısı oluşur |
| Odak | Ayrı görünür halka | Sadece daha kalın ikon | Klavye konumu seçilemez |
| Koyu tema | Kontrollü ağırlık | Çizgiye ışıklı dış parıltı | Kenarlar bulanıklaşır |

### Neden ve sonuç değerlendirmesi

Sayısal stroke seçmemek kararsız bir görsel dil anlamına gelmez.
Buradaki bağlayıcı karar aile ve optik ağırlık tutarlılığıdır.
Kütüphane seçilmeden tek bir kalınlık ilan etmek sahte kesinlik üretir.
Kabul edilmiş değerlerin olmadığı yerde varmış gibi sayı eklenmez.
Aile içi tutarlılık, şekillerin aynı sayıda çizgiden oluşmasını gerektirmez.
Karmaşık işarette sadeleşme bazen ağırlık artırmaktan daha etkilidir.
Hata simgesini kalınlaştırmak metin eksikliğini gidermez.
Gerçek anlam bütün kontrolün ortak görünümünden okunmalıdır.

### İnceleme sınırı

İkonlar 16, 20 ve 24 tb boyutlarda aynı örnek setinde incelenmelidir.
Koyu temada çizgi boşlukları kapanmamalıdır.
Düşük çözünürlüklü görüntü tek başına tasarımın kötü olduğunu kanıtlamaz.
Gerçek cihaz görüntüsü ve görev tanıması birlikte değerlendirilmelidir.
Lisanslı bir aile seçimi bu belgenin yeni ürün çıktısı değildir.
Bu bölüm stroke kodu veya vektör çizimi içermez.

### Bölüm sonu öz eleştiri

- **Öz eleştiri Ö30.1 — Sayısal kalınlık vermemek ekip yorumunu artırabilir; seçilecek aile aynı görev örnekleriyle bağlayıcı biçimde eşlenmelidir.**

- **Öz eleştiri Ö30.2 — Okunabilirlik için güçlenen çizgi küçük kutuda iç ayrıntıyı kapatabilir; sadece kalınlaştırma yeterli çözüm değildir.**

- **Öz eleştiri Ö30.3 — Dolu ve çizgi karşılıklarının eşleşmesi her sembolde eşit olmayabilir; seçili anlam metinle de korunmalıdır.**

## Boş Durum Tasarımı

Boş durum, içeriğin neden görünmediğini belirli bir anlamla açıklar.
Sıfır sonuç, bilgi eksikliği ve bağlantı hatası aynı görünümde eritilmez.
Mevcut B27 sözleşmesi korunur; yeni başlangıç ekranı tasarlanmaz.
Sakin yüzey, kısa neden ve varsa ilgili eylem görsel dilin temelidir.
Boşluk kullanıcının başarısızlığı veya eksik profili gibi sunulmaz.

### Kapsam ve görsel karar

Henüz kayıt bulunmaması nötr bir başlangıç durumudur.
Son durağın kaldırılması geçerli boş taslak anlamını taşır.
Koşullara eşleşme yoksa uygulanmış koşullar görünür kalır.
Kritik bilgi eksikliği “orada yer yok” anlamına gelmez.
Kapsam dışı coğrafya ürün bilgisinin sınırını anlatır.
Yerel hata kendi hata dilini kullanır; boş durum değildir.
İllüstrasyon zorunlu değildir ve gerçek yer bilgisi yerine geçmez.
En fazla bir baskın ilgili eylem mevcut sözleşmeden alınır.

### Tasarım ilkeleri

#### İlke V31.1 — Boşluğun nedeni başlık ve açıklamayla ayrıştırılır.

Gerekçe: Kullanıcı aynı görselden yanlış düzeltme yolunu çıkarmamalıdır.
Bedel: Tek genel boş durum metni bütün alanlarda kullanılamaz.
Görsel sonuç: Kayıt yokluğu ile bilgi yetersizliği farklı okunur.

#### İlke V31.2 — Nötr yüzey kullanıcının seçimine saygı gösterir.

Gerekçe: Boş taslak veya kullanılmamış liste eksiklik değildir.
Bedel: Eğlenceli maskotla her boşluğu doldurma yaklaşımı sınırlanır.
Görsel sonuç: Üzgün karakter, kırmızı hata işareti ve tamamlama baskısı bulunmaz.

#### İlke V31.3 — Korunan bağlam boş görünümde okunabilir kalır.

Gerekçe: Sonuç yokluğu önceki koşulların silindiği izlenimi vermemelidir.
Bedel: En yalın boşluk bile ihtiyaç özetine alan ayırabilir.
Görsel sonuç: Kullanıcı mevcut sorgunun kapsamını görebilir.

#### İlke V31.4 — Eylem gerçek ve ilgiliyse vurgulanır.

Gerekçe: İşlevsiz çağrı boş durumdan çıkış varmış yanılsaması yaratır.
Bedel: Bazı boş durumlarda yalnız açıklama bulunur.
Görsel sonuç: Her boşluk bir satış veya kayıt düğmesiyle kapanmaz.

#### İlke V31.5 — Bilgi eksikliğinin görseli desteklenmeyen içerik üretmez.

Gerekçe: Sahte kart veya temsili mekân fotoğrafı eksikliği saklar.
Bedel: Bazı alanlar daha sade ve az görselli kalır.
Görsel sonuç: Açıklama gerçek kapsamı taşır; olumlu öneri görünümü taklit edilmez.

### Boş durum matrisi

| Durum | Görsel vurgu | İlgili sınır |
| --- | --- | --- |
| Henüz kayıt yok | Nötr başlık ve kısa açıklama | Profil eksikliği değil |
| Bilinçli boş taslak | Taslak kimliği korunur | Otomatik durak doldurma yok |
| Eşleşme yok | Koşul bağlamı ve neden | Kendiliğinden gevşetme yok |
| Kritik bilgi eksik | Neyin doğrulanamadığı | Olumsuz olgu sayılmaz |
| Kapsam dışı alan | Coğrafi kapsam açıklaması | Orada yer yok iddiası yok |
| Ad bulunamadı | Kimlik aramasının sınırı | Hayalî kayıt yok |
| Bağlantı hatası | Hata ailesine ait görünüm | Boş veriyle karışmaz |
| Fotoğraf yok | Metin kararı sürer | Yerin değeri düşürülmez |

### İyi ve kötü yazılı örnekler

| Bağlam | İyi örnek | Kötü örnek | Sonuç |
| --- | --- | --- | --- |
| Kayıt | “Henüz kaydettiğin yer yok” | “Henüz gerçek bir gezgin değilsin” | Statü baskısı doğar |
| Rota | Boş taslak adının korunması | Rastgele üç durak ekleme | Kullanıcı iradesi bozulur |
| Koşul | “Bu koşulu doğrulayamadık” | “Bu bölgede uygun yer yok” | Bilgi açığı olguya dönüşür |
| Kapsam | Desteklenen alanın açıklanması | Boş haritayla tüm bölgeyi yok sayma | Kapsam yanlış anlaşılır |
| Hata | Neyin alınamadığını açıkça söyleme | Neşeli “Keşfe başla” kartı | Sorun gizlenir |

### Neden ve sonuç değerlendirmesi

Boş durumun premium niteliği güzel bir çizimden önce doğru ayrımdır.
Kullanıcı neyin olmadığını anladığında kendi kararını koruyabilir.
Nötr ton bilgi eksikliğinin önemini azaltmaz.
Kararı etkileyen eksik gövde düzeyinde okunur.
İlgili açıklama aynı metin ve yüzey ailesini paylaşır.
Hata rengi yalnız gerçek hata anlamına ayrılır.
Koşul eksikliği bütün yeri tehlikeli gösteren renge dönüşmez.
Öneri sayısını doldurmamak eksik görsel işçilik sayılmaz.

### İnceleme sınırı

Boş durumların kendi aralarındaki anlam farkı karşılaştırılmalıdır.
Gerçek metinler kullanıcıyı suçlayan veya utandıran ifade taşımamalıdır.
Uzun açıklama küçük alanda caption'a düşürülmemelidir.
İllüstrasyon varsa nedeni ve eylemi aşağı itmemelidir.
Hesapsız kullanıcının hakları boş görünümle saklanmamalıdır.
Bu bölüm yeni giriş yolu veya özellik eklemez.

### Bölüm sonu öz eleştiri

- **Öz eleştiri Ö31.1 — Çok sayıda boş durum ayrımı metin bakımını zorlaştırabilir; farklar iç sistem terimleriyle değil karar etkisiyle anlatılmalıdır.**

- **Öz eleştiri Ö31.2 — Nötr görünüm yardım yokmuş hissi verebilir; mevcut gerçek devam yolu yeterince tanınır olmalıdır.**

- **Öz eleştiri Ö31.3 — Sade boşluk kapsam yetersizliğini estetikle normalleştirebilir; ürünün bilgi sınırı açıkça görünür kalmalıdır.**

## Loading Tasarımları

Loading görünümü gerçek işlemin sürdüğünü ve etkilenen alanı anlatır.
Bekleme, AI'nin zekâsını sahneleyen bir gösteri değildir.
10 Design System B25'in süre ve durum sözleşmeleri korunur.
İlk tepki işlemin alındığını gösterir; tamamlandığını iddia etmez.
Yeni bir bekleme akışı veya yapay süreç aşaması oluşturulmaz.

### Kapsam ve görsel karar

Görsel karşılık önce etkilenen yerel alanda kalır.
Sorgu, koşullar ve kullanıcının taslağı okunabilir olmalıdır.
Yaklaşık 300 ms'den uzun işte görsel bekleme göstergesi kullanılabilir.
Bu eşik ilk karşılığı veya işlemin başlamasını geciktirmez.
Yaklaşık 10 saniyede açıklama ve devam seçenekleri gözden geçirilir.
Süre dolması başarı veya kesin hata ilanı değildir.
Beklemeyi bırakma ile işlemi iptal etmenin mevcut farkı korunur.
Ölçülmeyen ilerlemeye yüzde veya kalan süre yazılmaz.

### Tasarım ilkeleri

#### İlke V32.1 — Bekleme göstergesi gerçek etki alanına bağlanır.

Gerekçe: Tek fotoğraf gecikmesi bütün karar metnini kullanılamaz göstermemelidir.
Bedel: Her işlem için tek tam ekran örtü kullanılamaz.
Görsel sonuç: Kullanılabilir içerik ile bekleyen alan ayrılır.

#### İlke V32.2 — Görsel durum işlemin kimliğini korur.

Gerekçe: Kullanıcı neyin işlendiğini anlayamazsa tekrar denemeye yönelebilir.
Bedel: Genel dönen işarete ek kısa metin gerekir.
Görsel sonuç: “Rota yeniden değerlendiriliyor” ilgili bağlamda okunur.

#### İlke V32.3 — Eksik olumlu içerik hız etkisi için gösterilmez.

Gerekçe: Gerekçe önce, kritik sınır sonra gelirse geçici yanlış güven doğar.
Bedel: Bazı karar birimleri birlikte hazır olmayı bekler.
Görsel sonuç: Olumlu cümle ve karar değiştiren sınır aynı anlamla görünür.

#### İlke V32.4 — Beklemenin hareketi anlamın tek taşıyıcısı değildir.

Gerekçe: Azaltılmış harekette de işin durumu anlaşılmalıdır.
Bedel: Statik durum metni ve işaret bakım gerektirir.
Görsel sonuç: Hareket kapalıyken bekleme açıklaması kaybolmaz.

#### İlke V32.5 — Eski değerlendirme yeni taslak gibi görünmez.

Gerekçe: Kararlı düzen uğruna yanlış güncellik korunamaz.
Bedel: Önceki toplamın etiketlenmesi veya kaldırılması gerekebilir.
Görsel sonuç: Güncel kullanıcı seçimiyle önceki sonuç görsel olarak ayrıdır.

### Bekleme durum matrisi

| Durum | Görsel karşılık | Sınır |
| --- | --- | --- |
| İşlem algılandı | Anlık basılı veya işlem durumu | Başarı değil |
| Kısa bekleme | Yerel ve sakin karşılık | Yapay gecikme yok |
| 300 ms'yi aşan iş | Gerektiğinde görsel gösterge | İlk tepki gecikmez |
| Uzayan iş | Somut açıklama ve mevcut devam yolları | Uydurma bitiş süresi yok |
| Mevcut içerik yenileniyor | Yerel durum etiketi | Bütün ekran silinmez |
| Eski toplam | Önceki değerlendirme olarak ayrım | Yeni taslağa aitmiş gibi değil |
| Sonuç belirsiz | İlgili belirsizlik görünümü | Sonsuz loading değil |
| Azaltılmış hareket | Statik durum karşılığı | İşlev kaybı yok |

### İyi ve kötü yazılı örnekler

| Bağlam | İyi örnek | Kötü örnek | Etki |
| --- | --- | --- | --- |
| Rota | Gerçek yeniden değerlendirme etiketi | “En iyi gününü düşünüyorum” | AI otoritesi abartılır |
| Kayıt | Yerinde “Kaydediliyor” | Teyitsiz “Kaydedildi” | Sonuç yanlış bildirilir |
| Harita | Harita beklerken liste okunur | Tüm uygulamayı bulanık kapatma | Temel görev engellenir |
| Süre | Süresi bilinmeyen açık bekleme | “Yüzde 92 tamamlandı” tahmini | Sahte ilerleme oluşur |
| Eski bilgi | Tarihli önceki değerlendirme | Yeni sıra üstünde eski toplam | Yapılabilirlik yanlış okunur |

### Neden ve sonuç değerlendirmesi

Beklemenin görsel tutarlılığı tekrar basma belirsizliğini azaltmayı amaçlar.
Bu etki gerçek görevde ölçülmeden başarı olarak ilan edilmez.
Yerel gösterge daha az dramatik görünür.
Karşılığında kullanıcı sağlam kalan içerikle işini sürdürebilir.
İşlem durumunu anlatan metin altyapı ayrıntısına dönüşmemelidir.
Kullanıcı hangi kaydın veya değerlendirmenin beklendiğini bilmelidir.
Sunucu veya model adı bu anlam için genellikle gerekli değildir.
Bekleme görseli sabit bir sonuç kotası vaat etmez.

### İnceleme sınırı

Yavaş bağlantı, geç yanıt ve birbiri ardına düzenleme birlikte incelenmelidir.
Gösterge hareketi kullanıcının okumasını sürekli çekmemelidir.
Bekleyen alanda kritik eski olumlu iddia kullanılmamalıdır.
Metin büyütmede beklemeyi bırakma kontrolü örtülmemelidir.
Sürekli yinelenen duyurular görsel sadelikle gizlenmemelidir.
Sayılar mevcut DS başlangıçlarıdır; hizmet süresi garantisi değildir.

### Bölüm sonu öz eleştiri

- **Öz eleştiri Ö32.1 — Yerel loading çok sayıda alanda aynı anda görünürse parçalı ve yorucu olabilir; gerçek olaylar ilgili tek bağlamda toplanmalıdır.**

- **Öz eleştiri Ö32.2 — Bekleme metni fazla sık değişirse sakinlik bozulabilir; yalnız anlamlı aşama değişikliği görünürleşmelidir.**

- **Öz eleştiri Ö32.3 — Önceki toplamı korumak bağlamı sürdürse de güncellik yanılgısı doğurabilir; ayrım yeterince açık değilse olumlu toplam kaldırılmalıdır.**

## Skeleton Yapısı

Skeleton bilinen içerik yapısına geçici yer ayırır.
Sahte yer, sahte fotoğraf veya sahte karar metni değildir.
10 Design System B26 uyarınca varsayılan statik iskelettir.
Yeni ekranın çizimi ya da wireframe'i bu bölümün çıktısı değildir.
Karar sadece mevcut bileşenin yüklenme görünümünü açıklar.

### Kapsam ve görsel karar

İçeriğin geleceği ve genel yapısı biliniyorsa skeleton anlamlıdır.
İlk Yer veya ilk sonuç yüklemesinde kullanılabilir.
Görünür alandaki gerçekçi yapı kadar yer ayrılır.
Üç veya beş sonuç varmış izlenimi sayı doldurmak için üretilmez.
Boş veri, yetki reddi ve hata skeleton altında tutulmaz.
Mevcut geçerli içerik yenilenirken bütün alan iskelete dönüştürülmez.
Gerekçe ve önemli sınır birlikte hazır olmadan olumlu metin açılmaz.
Fotoğraf gelmediğinde sonsuz boş dikdörtgen korunmaz.

### Tasarım ilkeleri

#### İlke V33.1 — Skeleton yalnız bilinen yapının yer tutucusudur.

Gerekçe: Bilinmeyen sonuç biçimini çizmek yanlış beklenti yaratır.
Bedel: Her yükleme durumu aynı iskeleti kullanamaz.
Görsel sonuç: Yapı belirsizse sade yerel bekleme metni seçilir.

#### İlke V33.2 — Statik görünüm başlangıçtır.

Gerekçe: Sürekli parlama bilgi eklemeden dikkat ve hareket yükü yaratır.
Bedel: Bekleme daha az canlı görünebilir.
Görsel sonuç: Nötr yüzey blokları tekrarlanan ışık süpürmesi olmadan okunur.

#### İlke V33.3 — Yer tutucu gerçek bilgiye benzetilmez.

Gerekçe: Sahte başlık veya puan geçici de olsa iddia gibi algılanabilir.
Bedel: İskelet daha soyut ve sınırlı kalır.
Görsel sonuç: Gerçek yer adı, yıldız ve AI cümlesi içermez.

#### İlke V33.4 — Yapı gerçek içerik geldiğinde esneyebilir.

Gerekçe: Uzun gerekçe ve kimlik, tahmini blok yüksekliğine sığmayabilir.
Bedel: Bütün içerik değişiminde tam geometrik eşitlik sağlanmaz.
Görsel sonuç: Metin kırpılmaz; alan doğal yüksekliğe geçer.

#### İlke V33.5 — İskeletin son durumu dürüsttür.

Gerekçe: Gelmeyecek içerik için bekleme görünümünü sürdürmek kullanıcıyı yanıltır.
Bedel: Fotoğrafsız ve sınırlı bilgi durumları ayrı ele alınır.
Görsel sonuç: Boşluk gerçek nedeni açıklayan son görünüme dönüşür.

### Skeleton durum matrisi

| Durum | Görsel karşılık | Kullanım sınırı |
| --- | --- | --- |
| İlk içerik; yapı biliniyor | Statik iskelet | Gerçek görünür alan kadar |
| İlk içerik; yapı bilinmiyor | Yerel bekleme açıklaması | Hayalî kart çizilmez |
| Fotoğraf bekliyor | Oranı bilinen alan | Metin gereksiz bekletilmez |
| Fotoğraf gelmeyecek | Fotoğrafsız son görünüm | Sonsuz blok yok |
| Geçerli içerik yenileniyor | İçerik ve yerel durum | Bütün ekran sıfırlanmaz |
| Eşleşme yok | Boş durum açıklaması | İskelet sürmez |
| Yetki veya bağlantı hatası | İlgili hata durumu | İçerik geliyor sanılmaz |
| Azaltılmış hareket | Aynı statik karşılık | Anlam değişmez |

### İyi ve kötü yazılı örnekler

| Bağlam | İyi örnek | Kötü örnek | Neden |
| --- | --- | --- | --- |
| Sonuç | Gerçekçi yapı için nötr yer tutucu | Beş hayalî yer adı | Sonuç sayısı vaat edilir |
| Fotoğraf | Sabit oranlı sade alan | Temsili AI mekân görüntüsü | Gerçeklik yanılgısı oluşur |
| Gerekçe | Tam anlam birimi hazır olunca açma | Olumlu yarım cümleyi gösterme | Sınır geride kalır |
| Yenileme | Mevcut kayıt görünür | Kayıtları yeniden gri blok yapmak | Kullanıcı bağlamını kaybeder |
| Hareket | Statik nötr ton | Durmaksızın parlayan şerit | Bekleme dikkat tüketir |

### Neden ve sonuç değerlendirmesi

Skeleton'un değeri algılanan hızdan önce yerleşim sürekliliğidir.
Kullanıcı okurken eylem hedeflerinin sıçramaması önemlidir.
Ancak düzeni korumak yanlış olumlu içeriği korumak anlamına gelmez.
İskelet yüksekliği kesin içerik sınırı olarak uygulanmaz.
Yüksekliği aşan gerçek metin doğal biçimde büyür.
Nötr blok rengi yüzey ailesi içinden seçilir.
Yeni bir yükleme rengi veya dikkat çekici gradient gerekmez.
İskelet bileşen parçaları ayrı ayrı bilgiymiş gibi sunulmaz.

### İnceleme sınırı

Gerçek kısa ve uzun metinle geçiş ilişkisi gözden geçirilmelidir.
Fotoğraf alanı kaybolduğunda eylem konumu yanlış dokunma üretmemelidir.
İskelet boştan hataya dönüşebilen durumları kapsamalıdır.
Koyu temada bloklar kapalı kontrol izlenimi vermemelidir.
Sahte sayı veya başarılı işlem izi yer tutucuya eklenmemelidir.
Bu tarif UI çizimi veya yeni bileşen şablonu değildir.

### Bölüm sonu öz eleştiri

- **Öz eleştiri Ö33.1 — Statik iskelet bazı kullanıcılara donmuş arayüz gibi gelebilir; bölgenin açık bekleme metni bu ayrımı desteklemelidir.**

- **Öz eleştiri Ö33.2 — Gerçekçi bloklar yine belirli sonuç miktarı ima edebilir; görünür alan ölçüsü sayı kotasına dönüşmemelidir.**

- **Öz eleştiri Ö33.3 — Yerleşim sürekliliği hedefi boş fotoğraf alanını gereksiz koruyabilir; gelmeyecek medya için son görünüm açık olmalıdır.**

## Progress Yapısı

Progress görseli yalnız gerçekten ölçülebilen işlem ilerlemesini anlatır.
Mevcut akışta ölçüm yoksa yüzdelik çubuk üretme izni vermez.
Tamamlanma, kayıt, ziyaret ve bilgi doğrulaması farklı anlamlardır.
Bir günlük rota gezi tamamlama puanına dönüştürülmez.
Bu bölüm yeni süreç veya aşama sayısı tanımlamaz.

### Kapsam ve görsel karar

10 Design System B25 ve B30 durum sınırları korunur.
Bilinen iş miktarı varsa onun gerçek kapsamı açıklanır.
Kalan süre doğrulanmıyorsa tahmin kesin sayaç gibi görünmez.
Görsel doluluk ile işlem başarısı aynı anda varsayılmaz.
Belirsiz işte yerel bekleme metni yeterlidir.
Kısmi başarı bütün çubuğu yeşile dönüştürmez.
İlerleme, katkının yayınlandığı izlenimini veremez.
Yer veya şehir koleksiyonu tamamlanacak görev envanteri değildir.

### Tasarım ilkeleri

#### İlke V34.1 — Ölçülen ilerleme yalnız ölçülen kapsamı anlatır.

Gerekçe: Dosya aktarımının bitmesi inceleme veya yayın sonucunu kanıtlamaz.
Bedel: Tek çubuk bütün işin sonucunu özetleyemez.
Görsel sonuç: Kapsam etiketi dolulukla birlikte okunur.

#### İlke V34.2 — Bilinmeyen ilerlemeye yüzde verilmez.

Gerekçe: Tahmini doluluk sahte kesinlik ve bekleme beklentisi üretir.
Bedel: Bazı işlemler sade bekleme görünümünde kalır.
Görsel sonuç: Hayalî yüzde yerine gerçek işlem adı görünür.

#### İlke V34.3 — Tamamlanma rengi yetkili teyidi izler.

Gerekçe: Çubuğun sona gelmesi kaydın başarıyla korunduğu anlamına gelmeyebilir.
Bedel: Görsel doluluk sonrasında ayrı teyit durumu gerekebilir.
Görsel sonuç: Yeşil başarı yalnız gerçek sonuca bağlanır.

#### İlke V34.4 — Kısmi sonuçlar tek başarı görüntüsüne birleşmez.

Gerekçe: Bazı öğelerin başarısızlığı tam dolu görünümde kaybolabilir.
Bedel: İlgili öğelerin durumları görünür kalır.
Görsel sonuç: Başarılı, başarısız ve belirsiz kapsam ayrıştırılır.

#### İlke V34.5 — İlerleme göstergesi kullanıcıya gezi borcu yüklemez.

Gerekçe: Kaydetmek veya ziyaret etmek tamamlanacak koleksiyon hedefi değildir.
Bedel: Oyunlaştırılmış oran ve seri görselleri kullanılmaz.
Görsel sonuç: Erken bitiş veya tek durak nötr ve geçerli kalır.

### Progress durum matrisi

| Durum | Görsel karşılık | Sınır |
| --- | --- | --- |
| İş miktarı bilinmiyor | Bekleme etiketi | Yüzde yok |
| İş miktarı ölçülüyor | Kapsamlı gerçek ilerleme | Tahmini başarı değil |
| İş bir bölümü tamam | Gerçek kısmi durum | Tüm iş yeşil değil |
| Sonuç teyidi bekleniyor | Açık teyit bekleme | Doluluk başarı sayılmaz |
| Kesin başarısızlık | İlgili hata görünümü | Çubuk sonsuza ilerlemez |
| Sonuç belirsiz | Belirsiz kapsam açıklaması | Kesin başarısızlık değil |
| Günlük plan | Mevcut süre ve durak bilgisi | Tamamlama yüzdesi yok |
| Kişisel koleksiyon | Niyet ve kayıt görünümü | Şehir bitirme rozeti yok |

### İyi ve kötü yazılı örnekler

| Bağlam | İyi örnek | Kötü örnek | Etki |
| --- | --- | --- | --- |
| Ölçülmeyen AI işi | Gerçek bekleme metni | “Yüzde 87 düşünüldü” | Uydurma ölçüm oluşur |
| Katkı | “Gözlemin alındı” teyidi | Yüzde 100 doğrulandı çubuğu | Yayın otoritesi aşılır |
| Rota | Mevcut durak ve zaman özeti | “Gezinin yüzde 60'ı tamam” | Gezi görev listesine döner |
| Kısmi kayıt | Hangi sonucun teyit edildiğini ayırma | Toplu yeşil onay | Eksik sonuç görünmezleşir |
| Kalan süre | Bilinmiyorsa süre vermeme | Sürekli azalan hayalî sayaç | Yanlış zaman beklentisi kurulur |

### Neden ve sonuç değerlendirmesi

Ölçülebilen ilerleme belirsizliği azaltabilir.
Bu yarar yalnız gösterilen ölçü gerçek olduğunda geçerlidir.
Görsel doluluk güçlü bir tamamlanma işaretidir.
Bu nedenle kapsam etiketi küçük dipnot olamaz.
İlerleme renginin sınırlanması daha az kutlama hissi verebilir.
Karşılığında başarı ile sürmekte olan iş birbirine karışmaz.
Rota süreleri ilerleme ölçüsü değil planlama bilgisidir.
Bir kullanıcının erken durması eksik başarı olarak boyanmaz.

### İnceleme sınırı

Ölçüm kaynağı olmayan bir ilerleme varyantı varmış gibi tarif edilmemelidir.
Görsel oran gerçek sayısal değerle aynı kapsamı taşımalıdır.
Yüzde bilinmiyorsa yalnız şekil doluluğuyla gizli oran ima edilmemelidir.
Kısmi başarı metni büyük yazıda da ilgili alanla birlikte kalmalıdır.
Azaltılmış harekette aynı mevcut durum statik okunabilmelidir.
Bu bölüm yeni yükleme adımı veya gezi takibi özelliği eklemez.

### Bölüm sonu öz eleştiri

- **Öz eleştiri Ö34.1 — Ölçüm konusunda sıkı tutum bazı beklemeleri daha belirsiz hissettirebilir; sahte oran yerine kapsam açıklaması güçlendirilmelidir.**

- **Öz eleştiri Ö34.2 — Doluluk ile teyit ayrımı kullanıcıya teknik gelebilir; gerçek işlem sonucu sade sözcüklerle anlatılmalıdır.**

- **Öz eleştiri Ö34.3 — Kısmi sonuçların çokluğu taramayı zorlaştırabilir; ilgili öğeler ortak görsel sırayla sunulmalı, eksikler saklanmamalıdır.**

## Bildirim Tasarımları

Bildirim mevcut kararla ilgili anlamlı değişikliği görünür kılar.
10 Design System B24'ün kanal, mahremiyet ve kalıcılık sözleşmesi korunur.
Bu bölüm yeni bildirim merkezi veya hatırlatma akışı oluşturmaz.
Görsel dil gerçek önem düzeyi ile kullanıcının dikkatini eşler.
Bildirim yokluğu planın güncel veya güvenli olduğunun işareti değildir.

### Kapsam ve görsel karar

Kritik bilgi değişikliği ilgili kart veya görevde kalıcı karşılık taşır.
Sistem bildirimi aynı olayın izinli kanal karşılığıdır.
Kilit ekranı görünümü özel başlangıç ve ayrıntılı planı ifşa etmez.
Okunmuş durum ile çözülmüş durum birbirinden ayrıdır.
Bildirimi kapatmak alttaki kritik koşulu çözmez.
Rastgele öneri, uygulamaya dönüş baskısı ve Premium satışı kapsam dışıdır.
Aynı olay tekrar eden görsel gürültüye dönüşmez.
Bildirim rengi yerin tamamına güven veya tehlike etiketi vermez.

### Tasarım ilkeleri

#### İlke V35.1 — Bildirim görseli etkilenen koşulu adlandırır.

Gerekçe: Genel ünlem kullanıcıya hangi kararın değiştiğini söylemez.
Bedel: Tek kelimelik başlık yerine kısa somut açıklama gerekir.
Görsel sonuç: Değişen alan ilgili kayda bağlanır.

#### İlke V35.2 — Kritik durumun kalıcı karşılığı görünürdür.

Gerekçe: Geçici mesaj kaçırıldığında karar hakkı kaybolmamalıdır.
Bedel: İlgili içerikte güncel durum alanı korunur.
Görsel sonuç: Bildirim kapansa da gerekli sınır okunur.

#### İlke V35.3 — Kilit ekranı mahremiyet bakımından sade kalır.

Gerekçe: Bildirim küçük olsa da yakındaki başka kişilere görünür olabilir.
Bedel: Ayrıntı uygulamadaki mevcut bağlamda okunur.
Görsel sonuç: Kişi adı, sağlık notu ve özel başlangıç görünmez.

#### İlke V35.4 — Durum tonu gerçek önemle sınırlanır.

Gerekçe: Her değişikliği kırmızı göstermek öncelikleri eritir.
Bedel: Nötr, bilgi ve uyarı anlamlarının ayrı bakımı gerekir.
Görsel sonuç: Başlık, metin ve durum işareti birlikte okunur.

#### İlke V35.5 — Bildirim önceki görevin dikkatini gereksiz ele geçirmez.

Gerekçe: Odağı çalan ilgisiz mesaj kullanıcının kararını böler.
Bedel: Tanıtım görünürlüğü bildirim yüzeyinden alınamaz.
Görsel sonuç: Mesaj aktif görevin güvenli alanında ve ilgili kapsamda kalır.

### Bildirim durum matrisi

| Durum | Görsel karşılık | Korunan sınır |
| --- | --- | --- |
| Kritik koşul değişti | İlgili başlık ve kalıcı açıklama | Yalnız toast değil |
| Nötr bilgi | Bilgilendirme rolü ve metin | Alarm görünümü değil |
| Müdahale gerekiyor | Gerçek ilgili eylem | Yeni ilgisiz görev değil |
| İstenen hatırlatma | İzinli kanalın yerel görünümü | Teslim garantisi yok |
| Kilit ekranı | Asgari bağlam | Özel konum/not yok |
| Okundu | Okunma durumu | Sorun çözüldü anlamı yok |
| Kapatıldı | Mesaj kapanışı | Alttaki koşul sürer |
| Sistem izni reddedildi | Uygulamada kritik bilgi görünür | Temel hak eksilmez |

### İyi ve kötü yazılı örnekler

| Bağlam | İyi örnek | Kötü örnek | Neden |
| --- | --- | --- | --- |
| Yer saati değişti | Etkilenen saat kapsamının açıklanması | “Bütün günün tehlikede” | Etki abartılır |
| Kilit ekranı | “Planındaki bir bilgi değişti” | Ev adresi ve özel ihtiyaç dökümü | Mahremiyet bozulur |
| Kapatma | Koşul ilgili kartta sürer | Mesaj kapanınca uyarı da kaybolur | Sorun çözülmüş sanılır |
| İzin reddi | Uygulamada aynı kritik sınır | “Güvenli gezi için bildirimi aç” | İzin baskısı kurulur |
| Kayıt değişikliği | Gerçek kapsamlı bilgi | Premium davetiyle karışık uyarı | Dikkat ticarete yönelir |

### Neden ve sonuç değerlendirmesi

Sakin bildirim dili önemini gizlemek değildir.
İlgili değişikliği açıkça adlandırmak çoğu kez büyük ikonlardan daha anlamlıdır.
Bildirimler aynı yüzey, metin ve radius ailesini paylaşır.
Özel bir “AI uyarısı” estetiği ikinci güven katmanı oluşturmaz.
Kritik değişikliği görsel olarak ayırmak yararlıdır.
Ancak her kartı uyarı yüzeyine çevirmek sürekli alarm etkisi yaratır.
Kullanıcının gerçekten etkilenen koşulu görmesi hedeflenir.
Bu hedef yalnız mesajın ekranda bulunmasıyla karşılanmış sayılmaz.

### İnceleme sınırı

Açık bildirim mevcut ana eylemi ve harita atfını örtmemelidir.
Büyük yazı ve uzun Türkçe açıklama aynı bağlamda incelenmelidir.
Kilit ekranı örneklerinde özel bilgi asgari kalmalıdır.
Okundu ve çözüldü işaretleri aynı yeşil onayla birleşmemelidir.
Tek olayın tekrarları dikkat yarışına dönüşmemelidir.
Yeni sistem bildirimi yeteneği bu görsel tarifle ilan edilmez.

### Bölüm sonu öz eleştiri

- **Öz eleştiri Ö35.1 — Mahremiyet için sadeleştirilmiş bildirim fazla genel kalabilir; uygulamadaki ilgili hedefe bağlanan açıklama güçlü olmalıdır.**

- **Öz eleştiri Ö35.2 — Kalıcı durumlar biriktikçe kartlar ağırlaşabilir; yalnız güncel karar etkisi olan sınırlar öne çıkarılmalıdır.**

- **Öz eleştiri Ö35.3 — Sakin önem tonu bazı kritik değişiklikleri kaçırabilir; vurgu düzeyi gerçek görevde fark edilme üzerinden incelenmelidir.**

## Toast

Toast düşük önem taşıyan kısa işlem bilgisinin geçici görünümüdür.
Mesaj kaçırıldığında kullanıcı hakkı veya temel görev durumu kaybolmaz.
10 Design System B22'nin yaklaşık beş saniyelik başlangıcı korunur.
Bu süre bir hak süresi veya kesin okunma garantisi değildir.
Toast yeni bir görev veya zorunlu karar yüzeyi açmaz.

### Kapsam ve görsel karar

Gerçek yerel sonuç kısa metinle anlatılır.
“Bağlantı kopyalandı” yalnız kopyalama gerçekten tamamlandıysa görünür.
Gönderim, alıcı okuması veya paylaşım başarısı bu ifadeden çıkarılmaz.
Toast içinde zorunlu eylem bulunmaz.
Kritik düzeltme, hata ve tek geri alma yolu toast'a bırakılmaz.
Odak taşınmaz; görünüm kullanıcının mevcut işini kesmez.
Aktif yüzeyin güvenli alanında ana eylemi örtmeden yer alır.
Üst yüzey ve okunabilir metin rolleri birlikte kullanılır.

### Tasarım ilkeleri

#### İlke V36.1 — Toast metni tek gerçek sonuca odaklanır.

Gerekçe: Geçici yüzeyde birden fazla sonuç karışır veya okunmadan kaybolur.
Bedel: Uzun açıklama daha kalıcı mevcut bağlama taşınır.
Görsel sonuç: Kısa, somut ve abartısız teyit okunur.

#### İlke V36.2 — Gösterge sakin ve opak bir yüzeyde durur.

Gerekçe: Harita veya fotoğraf üstünde değişken kontrast kısa okumayı zorlaştırır.
Bedel: Saydam cam benzeri dekor kullanılmaz.
Görsel sonuç: Metin zeminden bağımsız olarak seçilebilir kalır.

#### İlke V36.3 — Toast tek kullanıcı hakkının taşıyıcısı olmaz.

Gerekçe: Yaklaşık beş saniye farklı okuma hızlarını garanti edemez.
Bedel: Önemli sonuç ilgili kalıcı durumda da görünür.
Görsel sonuç: Mesaj kaybolduğunda kullanıcı anlam veya kontrol kaybetmez.

#### İlke V36.4 — Aynı olay gereksiz tekrarlarla yığılmaz.

Gerekçe: Üst üste küçük mesajlar büyük bir dikkat engeline dönüşebilir.
Bedel: Her basış ayrı kutu olarak kutlanmaz.
Görsel sonuç: Aktif görevde sakin ve ilgili geri bildirim görülür.

#### İlke V36.5 — Toast başarıyı yer uygunluğuna genişletmez.

Gerekçe: Başarı rengi yalnız gerçekleşen işlemin sonucudur.
Bedel: Genel kalkan veya büyük onay simgesi kullanılmaz.
Görsel sonuç: Kopyalama teyidi “güvenli rota” görüntüsü üretmez.

### Toast durum matrisi

| Durum | Görsel karşılık | Sınır |
| --- | --- | --- |
| Kopyalama tamamlandı | Kısa gerçek teyit | Gönderildi denmez |
| Kopyalama belirsiz | Uygun yerel durum | Başarı toast'u yok |
| Düşük önem bilgisi | Sakin opak yüzey | Yeni odak yok |
| Kritik bilgi değişikliği | Kalıcı ilgili açıklama | Toast tek taşıyıcı olamaz |
| Geri alma gerekiyor | Snackbar veya mevcut kalıcı karşılık | Toast içinde zorunlu eylem yok |
| Modal açık | Aktif göreve ait güvenli alan | İlgisiz modal üstü mesaj yok |
| Tekrarlanan aynı olay | Birleştirilmiş geri bildirim | Kutu yığını yok |
| Büyük metin | Büyüyen okunabilir metin alanı | Kesilme yok |

### İyi ve kötü yazılı örnekler

| Bağlam | İyi örnek | Kötü örnek | Etki |
| --- | --- | --- | --- |
| Kopyalama | “Bağlantı kopyalandı” | “Arkadaşlarına gönderildi” | Gerçek sonuç aşılır |
| Kısa teyit | Tek cümle | Üç paragraf açıklama | Okunmadan kaybolur |
| Harita | Opak yüzeyde okunabilir metin | Yollar üstünde saydam yazı | Kontrast oynar |
| Kritik saat | İlgili kayıtta kalıcı sınır | Beş saniyelik tek uyarı | Karar bilgisi kaybolur |
| Tekrar | Aynı sonucun sakin teyidi | Ardışık kutularla ekranı kaplama | Eylemler örtülür |

### Neden ve sonuç değerlendirmesi

Toast görselinin küçük kalması işlemin kapsamını korumayı kolaylaştırır.
Ancak çok küçük metin kullanmak bu amaca hizmet etmez.
Gövde okunabilirliği ve mevcut metin ölçeği sürdürülür.
Yüzeyin sınırı harita üzerinde de tanınabilir olmalıdır.
Gölge destekleyici olabilir; okunabilirliğin tek koşulu olamaz.
Mesajın hareketi kısa ve kesilebilir mevcut aileden gelir.
Azaltılmış harekette doğrudan görünür durum yeterlidir.
Toast'un yok olması başka bir işlemin tamamlandığı anlamına gelmez.

### İnceleme sınırı

Beş saniye DS başlangıcıdır; bütün kullanıcılar için yeterli süre iddiası değildir.
Uzun çeviri için anlam önemliyse kalıcı yüzey tercih edilmelidir.
Güvenli alan, klavye ve açık katman aynı örnekte incelenmelidir.
Toast temel navigasyon kontrolünü örtmemelidir.
Bildirim konuşmayı tekrar tekrar kesen duyuruya dönüşmemelidir.
Bu bölüm yeni toast türü veya durum davranışı eklemez.

### Bölüm sonu öz eleştiri

- **Öz eleştiri Ö36.1 — Kısa mesaj işlemin hedefini söylemeden fazla genel kalabilir; gerektiğinde hedef kısa ve somut biçimde eklenmelidir.**

- **Öz eleştiri Ö36.2 — Opak yüzey haritanın küçük bölümünü örtebilir; konumlandırma aktif eylem ve gerekli atıflarla birlikte incelenmelidir.**

- **Öz eleştiri Ö36.3 — Aynı mesajı birleştirmek kullanıcıya son basışın alınmadığını düşündürebilir; mevcut kontrolün anlık karşılığı ayrıca korunmalıdır.**

## Snackbar

Snackbar tamamlanmış geri alınabilir işlemin kısa ilgili eylemli görünümüdür.
10 Design System B23'ün geri alma ve süre sözleşmesi korunur.
Başlangıç görünme süresi yaklaşık on saniyedir.
Bu süre geri alma hakkının sona erme süresi değildir.
Kalıcı görev karşılığı mevcut akışın parçası olarak görünür kalır.

### Kapsam ve görsel karar

Mesaj yapılan işlemi ve ilgili nesneyi somut olarak adlandırır.
“Geri al” eylemi aynı işlemin kapsamına bağlanır.
Odak veya işaretçi içindeyken mesaj kapanmaz.
Erişilebilir zaman tercihi mevcut sözleşmeye göre dikkate alınır.
Geri alma yeni dış gerçekliği geri çeviremez.
Kaldırılan kişisel durak geri gelebilir; yeni kapanma bilgisi eskiye dönmez.
Snackbar birden fazla bağımsız kararı tek kutuda sunmaz.
Ana eylem, klavye ve geçici görev katmanını örtmez.

### Tasarım ilkeleri

#### İlke V37.1 — Mesaj ve eylem aynı geri alınabilir işlemi anlatır.

Gerekçe: Genel “Geri al” hangi değişikliğin döneceğini belirsiz bırakabilir.
Bedel: İşlem nesnesi için yeterli metin alanı ayrılır.
Görsel sonuç: “Durak kaldırıldı” ile ilgili eylem birlikte okunur.

#### İlke V37.2 — Geri alma görünür ama baskısızdır.

Gerekçe: Kullanıcı yeni yaptığı seçimi geri almaya zorlanmamalıdır.
Bedel: Eylem ana görevin baskın çağrısıyla yarışmaz.
Görsel sonuç: Okunabilir etiket ve yeterli hedef sakin biçimde ayrışır.

#### İlke V37.3 — Zamanlı yüzey dışında kontrol korunur.

Gerekçe: On saniyeyi kaçıran kişi kararını düzeltme hakkını kaybetmemelidir.
Bedel: Mevcut kalıcı geri alma karşılığı bulunabilir tutulur.
Görsel sonuç: Mesaj kapanışı işlemi geri dönülmez hale getirmez.

#### İlke V37.4 — Opak zemin ve açık sınır kullanılır.

Gerekçe: Harita veya fotoğraf üstündeki değişken görünüm eylem okunmasını zayıflatır.
Bedel: Cam efekti gibi dekoratif saydamlık kullanılmaz.
Görsel sonuç: Metin ve eylem aynı güvenilir kontrastta görünür.

#### İlke V37.5 — Geri alma kapsamı başarı görünümünden ayrılır.

Gerekçe: Kişisel seçim dönüşü, yeni kanıtın veya paylaşımın geri alınması değildir.
Bedel: Bazı işlemler snackbar ile temsil edilemez.
Görsel sonuç: Geri alınamaz kapsam aynı görsel aileye zorlanmaz.

### Snackbar durum matrisi

| Durum | Görsel karşılık | Sınır |
| --- | --- | --- |
| Durak kaldırıldı | Somut teyit ve “Geri al” | Aynı kişisel düzenleme |
| Listeden çıkarıldı | İlgili kayıt adı veya bağlam | Diğer koleksiyonları silmez |
| Eylem odakta | Okunabilir aktif hedef | Zamanla kapanmaz |
| Mesaj kapandı | Kalıcı görev karşılığı | Geri alma hakkı kaybolmaz |
| Yeni kanıt geldi | Güncel sınır korunur | Eski bilgiye dönülmez |
| Paylaşım geri alınamaz | Uygun kapsam açıklaması | Yanıltıcı “Geri al” yok |
| Birden çok işlem | İlgili ve ayırt edilebilir sonuç | Eski eylemle karışmaz |
| Büyük metin | Mesaj ve eylem birlikte büyür | İki hedef çakışmaz |

### İyi ve kötü yazılı örnekler

| Bağlam | İyi örnek | Kötü örnek | Neden |
| --- | --- | --- | --- |
| Durak kaldırma | İlgili durak ve geri alma | “İşlem yapıldı” ve adsız ok | Kapsam belirsizleşir |
| Süre | Kalıcı geri alma yolu | On saniye sonra hak kaybı | Yavaş okuyan dışlanır |
| Yeni kapanma | Seçimi geri getirip sınırı koruma | Eski açık bilgisini geri getirme | Bilgi yaşamı bozulur |
| Dış kopya | Gerçek geri çekme sınırı | “Story'yi geri al” | Ulaşılamayan sonuç vaat edilir |
| Eylem | 16/24 okunabilir etiket | Küçük alt çizgisiz gri sözcük | Kontrol bulunamaz |

### Neden ve sonuç değerlendirmesi

Snackbar'ın amacı rutin işlemi onay törenine dönüştürmeden kontrolü korumaktır.
Görsel dil bu mevcut davranışı destekler.
Kalıcı geri alma karşılığı yoksa zamanlı mesaj yeterli sayılmaz.
Birden fazla mesajın kuyruğu eski nesneye ait eylem doğurabilir.
Bu nedenle bağlam adı sadece süsleme değildir.
Mesajın görünürlüğü ile ana görevin alanı birlikte değerlendirilir.
Eylem rengi okunabilirliği destekler; yeşil yer kalitesi anlamı taşımaz.
Geri alma etiketine ulaşmak hareket veya hız becerisi istememelidir.

### İnceleme sınırı

On saniye normal başlangıç olarak alınır; evrensel okuma süresi değildir.
Odak, işaretçi ve erişilebilir zaman tercihi görsel durumda kaybolmamalıdır.
Eylem büyük metinde ayrı satıra geçtiğinde kapsam bağı korunmalıdır.
Klavye üstünde kalan snackbar ana gönderim kontrolünü örtmemelidir.
Aynı kullanıcı ardışık düzenleme yaptığında ilgili nesne anlaşılmalıdır.
Bu bölüm yeni geri alma süresi veya işlem yetkisi tanımlamaz.

### Bölüm sonu öz eleştiri

- **Öz eleştiri Ö37.1 — İşlem nesnesini açık yazmak snackbar'ı uzatabilir; kısaltma yalnız kimlik karışıklığı yaratmıyorsa yapılmalıdır.**

- **Öz eleştiri Ö37.2 — Kalıcı geri alma karşılığı mevcut akışta zayıf görünebilir; geçici mesajın varlığı bu bulunabilirlik sorununu kapatamaz.**

- **Öz eleştiri Ö37.3 — Sakin eylem vurgusu hızlı düzeltmeyi zorlaştırabilir; hedef ve metin kontrastı baskın görevle birlikte incelenmelidir.**

## Bottom Sheet

Bottom sheet mevcut bağlamdaki tek sınırlı yardımcı görevin yüzeyidir.
10 Design System B19'un modal ve modal olmayan ayrımı korunur.
Bu bölüm yeni sheet açılışı, ara yüksekliği veya ekran düzeni üretmez.
Görsel dil yüzeyin geçici ilişkisini ve mevcut kapanış yolunu açıklar.
Tek elle ulaşılabilirlik okunabilirliği azaltma gerekçesi değildir.

### Kapsam ve görsel karar

Bağımsız sheet radius'u kabul edilmiş 16 tb değeridir.
Tam ekran görünüm cihaz çerçevesi nedeniyle köşe kırpmak zorunda değildir.
Üst yüzeyin opak ve okunabilir teması kullanılır.
Başlık ve görünür kapat veya vazgeç yolu bulunur.
Sürükleme işareti tek kapatma yolu gibi sunulmaz.
İçerik büyüdüğünde mevcut tam görev yüksekliği uyarlaması korunur.
Modal sheet arka görevi durdurur; modal olmayan önizleme bunu taklit etmez.
Taslak ile uygulanan seçim mevcut sözleşmesine göre görsel ayrım taşır.

### Tasarım ilkeleri

#### İlke V38.1 — Sheet yüzeyi geçici görevi açıkça ayırır.

Gerekçe: Arka içerikle aynı düzlemde görünmek etkin bağlamı belirsizleştirir.
Bedel: Yüzey sınırı ve gerekli ton farkı korunur.
Görsel sonuç: Kullanıcı hangi içerikle çalıştığını anlayabilir.

#### İlke V38.2 — Başlık ve çıkış okunabilir kontrol ailesini kullanır.

Gerekçe: Küçük sürükleme tutamacı tek elle kullanımın tek yolu olamaz.
Bedel: Üst alan açık etiket veya tanınır kontrol için yer ayırır.
Görsel sonuç: Kapatma hedefi simgenin boyutuna indirgenmez.

#### İlke V38.3 — Kritik içerik küçük açıklığa sıkıştırılmaz.

Gerekçe: Dar sheet içinde minik metin karar sınırını fiilen gizler.
Bedel: Yardımcı yüzey daha yüksek görünebilir.
Görsel sonuç: Gövde 16/24 kalır; alan gerektiğinde büyür.

#### İlke V38.4 — Modal niteliği görsel anlamla tutarlıdır.

Gerekçe: Benzer görünen fakat farklı odak kurallı yüzeyler kullanıcıyı şaşırtabilir.
Bedel: Arka planın görünürlüğü ve yüzey ilişkisi görevle birlikte incelenir.
Görsel sonuç: Modal olmayan harita önizlemesi kapalı bir modal gibi davranış vaat etmez.

#### İlke V38.5 — Uygulama ve vazgeçme ayrımı görsel olarak korunur.

Gerekçe: Sheet'i kapatmak mevcut taslak–uygula modelinde uygulamak değildir.
Bedel: Kapatma ve ana eylemin metinleri aynılaşmaz.
Görsel sonuç: “Uygula” ile “Vazgeç” kendi kontrol önceliğinde görünür.

### Sheet durum matrisi

| Durum | Görsel karşılık | Korunan sınır |
| --- | --- | --- |
| Kısa filtre görevi | Başlık, içerik ve mevcut eylemler | Yeni akış yok |
| Modal sheet | Üst görev yüzeyi | Arka görev etkinmiş görünmez |
| Modal olmayan önizleme | Bağlamla ilişkili yardımcı yüzey | Odak tuzağı vaat etmez |
| Uzun metin | Büyüyen görev alanı | Font küçülmez |
| Klavye açık | Etiket ve eylemler görünür | Güvenli alan örtülmez |
| Yön değişti | Aynı taslak ve okunabilir yüzey | Yeni başlangıç yok |
| Koyu tema | Üst yüzey ve sınır farkı | Gölgeye tek başına dayanmaz |
| Azaltılmış hareket | Doğrudan açık durum | Katman anlamı kaybolmaz |

### İyi ve kötü yazılı örnekler

| Bağlam | İyi örnek | Kötü örnek | Etki |
| --- | --- | --- | --- |
| Kapatma | Görünür kontrol ve yeterli hedef | Yalnız ince tutamaç | Sürükleyemeyen dışlanır |
| Filtre | Uygulanan ile taslak ayrımı | Kapat simgesini uygula gibi sunma | Koşul değişimi belirsizleşir |
| Harita | Opak okunabilir üst yüzey | Harita yollarının metinden görünmesi | Kontrast değişir |
| Büyük yazı | Aynı görevde yükselen alan | Uyarıyı 12 tb'ye indirme | Kritik metin kaybolur |
| Klavye | Eylemin görünür kalması | Ana düğmenin klavye altında kalması | Görev tamamlanamaz |

### Neden ve sonuç değerlendirmesi

16 tb köşe yarıçapı geçici yüzeyi sakin bir aileye bağlar.
Köşenin büyüklüğü daha önemli karar veya Premium statüsü anlatmaz.
Katman ilişkisi yüzey ve sınırla görünür olmalıdır.
Gölge kaybolduğunda da görev ayırt edilebilmelidir.
Arka bağlamın görünmesi kullanıcının nereden geldiğini hatırlatabilir.
Ancak saydamlık bu ilişkiyi sağlamanın zorunlu yolu değildir.
Mevcut 240 ms katman rolü gerekiyorsa kullanılabilir.
Hareketin bitmesi eyleme geçişin koşulu değildir.

### İnceleme sınırı

Sheet için yeni yükseklik yüzdeleri bu belgede icat edilmez.
Uzun okuma ve karmaşık form mevcut sözleşmenin sınırında kalır.
Başlık, çıkış ve ana eylem büyük metinde birlikte kontrol edilmelidir.
Harita atfı sheet arkasında kayboluyorsa ilgili yüzey ilişkisi incelenmelidir.
Kapatma görünümü gönderilmiş işlemin iptali gibi anlatılmamalıdır.
Mevcut ekran veya panel mimarisi yeniden düzenlenmemiştir.

### Bölüm sonu öz eleştiri

- **Öz eleştiri Ö38.1 — Sheet'in opaklığı harita bağlamını azaltabilir; okunabilirlik korunarak mevcut görünür alan ilişkisi incelenmelidir.**

- **Öz eleştiri Ö38.2 — Modal ve modal olmayan yüzeylerin ortak biçimi ayrımı zorlaştırabilir; başlık, arka görev ve kapanış anlamı birlikte değerlendirilmelidir.**

- **Öz eleştiri Ö38.3 — Büyüyen içerik tek elle erişimi zorlaştırabilir; metni küçültmeden mevcut tam görev uyarlamasının görünürlüğü korunmalıdır.**

## Modal

Modal mevcut akışta gerekli odaklı karar veya kapsam incelemesini ayırır.
10 Design System B20'nin tek etkin modal görevi korunur.
Görsel dil yeni onay noktası veya gereksiz kesinti oluşturmaz.
Sıradan kayıt ve geri alınabilir düzenleme modal görünümle büyütülmez.
Somut sonuç hazır değilse gösterişli pencere onu anlamlı hale getirmez.

### Kapsam ve görsel karar

Bağımsız modal radius'u 16 tb'dir.
Üst yüzey teması ve okunabilir metin rolleri kullanılır.
Başlık, sonuç açıklaması, net eylem ve anlaşılır vazgeçme birlikte görünür.
Arka görevin durduğu mevcut modal anlamı korunur.
Birden fazla bağımsız modal üst üste yığılmaz.
Tehlikeli eylem varsayılan görsel zafer veya otomatik seçim gibi sunulmaz.
Klavye ve yön değişimi metni veya eylemleri gizleyemez.
Kapanış mevcut odak dönüşünü anlaşılır biçimde destekler.

### Tasarım ilkeleri

#### İlke V39.1 — Modal görünümü gerçek karar kapsamını taşır.

Gerekçe: Belirsiz “Emin misin?” metni sonuç değerlendirmesini kullanıcıya bırakır.
Bedel: Sonucun somut açıklamasına alan gerekir.
Görsel sonuç: Etkilenen nesne ve işlem aynı yüzeyde okunur.

#### İlke V39.2 — Eylem ile vazgeçme birlikte anlaşılırdır.

Gerekçe: Modal kullanıcının tek seçeneğe zorlandığı bir alan olamaz.
Bedel: Baskın eylem karşısında görünür alternatif korunur.
Görsel sonuç: İkincil kontrol düşük kontrastlı dipnot değildir.

#### İlke V39.3 — Opak üst yüzey temel karardır.

Gerekçe: Arkadaki hareketli içerik önemli metnin okunmasını zorlaştırabilir.
Bedel: Cam veya atmosfer etkisi sınırlanır.
Görsel sonuç: Kontrast arka görüntüye bağımlı kalmaz.

#### İlke V39.4 — Modal katmanının sınırı gölgeden bağımsız algılanır.

Gerekçe: Koyu veya zorlanmış renk ortamında gölge görünmeyebilir.
Bedel: Ton ve gerekli sınır ilişkisinin bakımı gerekir.
Görsel sonuç: Etkin yüzey kaybolmuş gibi görünmez.

#### İlke V39.5 — Metin büyütme ve klavye görsel kapsamı korur.

Gerekçe: Sığmayan sonuç açıklaması kararın önemli kısmını silemez.
Bedel: Küçük bir pencere görünümü her koşulda korunamaz.
Görsel sonuç: Mevcut tam görev uyarlaması gerektiğinde okunabilir kalır.

### Modal durum matrisi

| Durum | Görsel karşılık | Sınır |
| --- | --- | --- |
| Kapsam incelemesi | Somut başlık ve sonuç | Soyut onay değil |
| Tehlikeli işlem | Açık fiil ve tehlike rolü | Otomatik seçili tehlike yok |
| Vazgeçme | Okunabilir ikincil kontrol | Gizli çıkış yok |
| Klavye açık | Eylem ve aktif alan görünür | Metin altında kalmaz |
| Uzun içerik | Büyüyen veya mevcut uyarlanan görev | Kritik kısaltma yok |
| Yerel seçici açık | Aynı görevle ilişkili kontrol | İkinci bağımsız modal değil |
| İşlem gönderildi | Gerçek bekleme veya sonuç | Kapatma geri alma sanılmaz |
| Koyu/yüksek kontrast | Üst yüzey ve algılanır sınır | Gölge zorunlu değil |

### İyi ve kötü yazılı örnekler

| Bağlam | İyi örnek | Kötü örnek | Etki |
| --- | --- | --- | --- |
| Silme kapsamı | Hangi kaydın etkilendiğini söyleme | “Emin misin?” tek başına | Kullanıcı sonucu tahmin eder |
| Çıkış | Açık “Vazgeç” | Kapatmayı görünmez yapmak | Kullanıcı baskı altında kalır |
| Premium | Kullanıcı istediğinde mevcut kapsam | Her girişte reklam modali | Görev kesilir |
| Rutin kayıt | Mevcut yerinde teyit | Her kayıtta büyük onay penceresi | Gereksiz sürtünme oluşur |
| Arka plan | Opak okunabilir yüzey | Fotoğrafın metne karışması | Karar açıklaması zayıflar |

### Neden ve sonuç değerlendirmesi

Modalın premium niteliği köşe ve gölge miktarından doğmaz.
Kullanıcının sonucu ve vazgeçme hakkını açık görebilmesinden doğar.
Güçlü yüzey ayrımı bu dikkati destekleyebilir.
Fakat sıradan işi daha önemli gösteren görsel abartı zararlıdır.
Bir modal içeriği uzun olduğunda metin küçültülmez.
Mevcut görev uyarlaması okunabilirliği korumak için vardır.
240 ms katman rolü gösterişli açılış zorunluluğu değildir.
Azaltılmış harekette 0 ms durum karşılığı aynı anlamı taşır.

### İnceleme sınırı

Bu bölüm yeni bir onay akışını gerekçelendirmez.
Somut kapsam mevcut ürün ve UX sözleşmesinden gelmelidir.
Başlangıç odağının anlamı görsel vurgu ile çelişmemelidir.
Tehlikeli eylem yalnız renk üzerinden tanınmamalıdır.
Arka plan yazısının okunması modal metniyle rekabet oluşturmamalıdır.
Kapanışta geri dönülen kontrol görünür biçimde tanınabilmelidir.

### Bölüm sonu öz eleştiri

- **Öz eleştiri Ö39.1 — Opak modal arka bağlamı gereğinden fazla koparabilir; başlık ve nesne adı yeterli sürekliliği sağlamalıdır.**

- **Öz eleştiri Ö39.2 — Somut sonuç açıklamaları sık tekrarlanırsa ezber onayı oluşabilir; gereksiz modal eklemek bu görsel dilin çözümü değildir.**

- **Öz eleştiri Ö39.3 — İkincil eylemin okunabilirliği tek başına baskısız seçim sağlamayabilir; boyut, mesafe ve dil birlikte incelenmelidir.**

## Dialog

Dialog burada mevcut B20 modal sözleşmesinin kısa karar anlatımıdır.
Yeni bağımsız bileşen ailesi veya farklı odak davranışı oluşturmaz.
Modal ile dialog farklı doğruluk veya kullanıcı hakkı taşımaz.
Kısa yüzeyin amacı bir somut sonucu açık biçimde okutabilmektir.
Kısalık kapsamın eksiltilmesiyle sağlanmaz.

### Kapsam ve görsel karar

Mevcut modalın başlık, sonuç ve eylem ilişkisi korunur.
Radius, yüzey ve tipografi aynı kabul edilmiş rollerden gelir.
Kritik açıklama gövde 16/24 düzeyinde kalır.
Başlık mevcut bağımsız görev başlığı rolüyle ilişkilidir.
Eylemler B11'in etiket ve hedef kurallarını paylaşır.
Bir kısa cümleye sığmayan etki küçültülerek gizlenmez.
Yerel platform dialog görünümü ortak anlamı koruduğu ölçüde uyarlanabilir.
Platform aşinalığı yeni işlem veya izin akışı açma yetkisi değildir.

### Tasarım ilkeleri

#### İlke V40.1 — Dialog aynı modal ailesinin kısa kapsamlı görünümüdür.

Gerekçe: Aynı iş için ikinci sözleşme tutarsız kapanış ve odak beklentisi yaratır.
Bedel: Her platform için bağımsız davranışlı yeni stil kurulmaz.
Görsel sonuç: Başlık, içerik ve eylem ilişkisi ortak kalır.

#### İlke V40.2 — Kısa metin somut sonucu taşır.

Gerekçe: Genel onay cümlesi küçük görünse de kullanıcıya düşünme yükü bırakır.
Bedel: Etkilenen kayıt veya kapsam adı yazılmalıdır.
Görsel sonuç: Eylemin sonucu düğmeden önce anlaşılır.

#### İlke V40.3 — Eylem etiketleri açık fiillerle ayrışır.

Gerekçe: “Evet” ve “Hayır” önceki cümleyi hatırlamayı gerektirebilir.
Bedel: Daha uzun işlem adları hedef alanını büyütebilir.
Görsel sonuç: Kullanıcı silme, kapatma veya vazgeçmeyi açıkça ayırır.

#### İlke V40.4 — Yerel aşinalık anlamsal eşitliği korur.

Gerekçe: Platform görünümü değişse de aynı sonuç ve hak görünür olmalıdır.
Bedel: Birebir piksel özdeşliği yerine karşılıklı inceleme gerekir.
Görsel sonuç: Cupertino ve Material uyarlamaları aynı kapsamı taşır.

#### İlke V40.5 — Kısa görünüm büyük metinde esneyebilir.

Gerekçe: Dialog boyunu korumak için kritik metin veya eylem kesilemez.
Bedel: İki satırlık örnek her kullanıcıda iki satır kalmaz.
Görsel sonuç: Kontroller ve açıklama birlikte doğal yükseklik kazanır.

### Dialog durum matrisi

| Durum | Görsel karşılık | Sözleşme sınırı |
| --- | --- | --- |
| Kısa somut karar | Başlık, sonuç ve açık fiil | Yeni işlem yok |
| Uzun nesne adı | Sarılan gerçek kimlik | Üç noktayla yanlış kayıt yok |
| Tehlikeli sonuç | Tehlike rolü ve açık kapsam | Renk tek anlam değil |
| Vazgeçme | Okunabilir eylem | Utandırıcı metin yok |
| Büyük metin | Büyüyen içerik alanı | Sabit kutuda kesilme yok |
| Yerel iOS sunumu | Platforma uygun kontrol görünümü | Ortak haklar aynı |
| Yerel Android sunumu | Platforma uygun kontrol görünümü | Ortak bilgi aynı |
| İşlem sonucu belirsiz | Gerçek durum açıklaması | Evet/hayırla zorla sonuç yok |

### Material ve Cupertino karşılaştırması

Bu tablo güncel bütün platform ekranlarına ilişkin evrensel bir gözlem değildir.
Şamandıra'nın mevcut modal sözleşmesinin iki yerel uyarlamasını karşılaştırır.

| Boyut | Material uyarlamasında korunacak | Cupertino uyarlamasında korunacak | Şamandıra sonucu |
| --- | --- | --- | --- |
| Başlık | Yerel kontrolle açık görev adı | Yerel kontrolle açık görev adı | Aynı somut kapsam |
| Eylem | Platforma uygun yerel beklenti | Platforma uygun yerel beklenti | Fiil ve hak eşitliği |
| Tipografi | Kullanıcı metin tercihine uyum | Kullanıcı metin tercihine uyum | Kritik gövde kesilmez |
| Kapanış | Mevcut modal sözleşmesi | Mevcut modal sözleşmesi | Vazgeçme anlamı değişmez |
| Tema | Okunabilir rol eşleşmesi | Okunabilir rol eşleşmesi | Bilgi rengi güven üretmez |
| Bedel | Yerel görünümün ayrı incelemesi | Yerel görünümün ayrı incelemesi | Piksel özdeşliği aranmaz |

### İyi ve kötü yazılı örnekler

| Bağlam | İyi örnek | Kötü örnek | Neden |
| --- | --- | --- | --- |
| Kayıt kaldırma | Nesne adı ve “Kaldır” | “Evet” tek başına | Sonuç hatırlama yüküne dönüşür |
| Vazgeçme | “Vazgeç” | “Hayır, iyi fikir istemiyorum” | Seçim utandırılır |
| Uzun ad | Adın tam sarılması | Benzer adları aynı kısaltma | Yanlış kayıt riski artar |
| Büyük metin | Yükselen açıklama alanı | Küçültülmüş gövde | Kullanıcı tercihi bozulur |
| Yerel fark | Aynı anlamın uyarlanması | Android'de daha kısa kritik açıklama | Kanal hakkı eksilir |

### Neden ve sonuç değerlendirmesi

Dialog'un kısa oluşu okunabilirliği otomatik sağlamaz.
Az sözcükte belirsiz kapsam varsa kullanıcı yine sonucu tahmin eder.
Somut fiil aynı anda görsel hiyerarşiyi ve anlamı güçlendirir.
Bu yarar yeni onay isteme gerekçesi değildir.
Rutin geri alınabilir işlem mevcut yerinde geri bildirimde kalır.
Modal gerektiren gerçek kapsamda ise kısa görünüm yeterli olabilir.
İçerik uzadığında aile değişmiş gibi ikinci stil icat edilmez.
Mevcut modal uyarlaması aynı anlamla devam eder.

### İnceleme sınırı

Bu bölüm yeni yerel işletim sistemi kuralları ilan etmez.
Görsel uyarlama mevcut ortak sözleşme ve ilgili platform erişimiyle sınanmalıdır.
Uzun ad, büyük metin ve klavye durumu aynı görevde ele alınmalıdır.
Etiketlerin görünen metni erişilebilir adla çelişmemelidir.
Kapanış görünümü gönderilmiş işlemi geri almış gibi anlaşılmamalıdır.
Dialog sayısı veya açılma zamanı bu belgeyle değiştirilmemiştir.

### Bölüm sonu öz eleştiri

- **Öz eleştiri Ö40.1 — Dialog'u modalın kısa görünümü saymak bazı ekiplerde terim karışıklığı yaratabilir; davranış otoritesinin B20 olduğu açık tutulmalıdır.**

- **Öz eleştiri Ö40.2 — Açık fiiller uzun düğmeler üretebilir; eylem hedefini ve kapsamı koruyarak doğal sarılma değerlendirilmelidir.**

- **Öz eleştiri Ö40.3 — Yerel görünüm farkları marka tutarlılığını zayıflatabilir; ortak metin, yüzey rolleri ve hak eşitliğiyle tutarlılık kurulmalıdır.**

## FAB Kullanımı

Bölüm kimliği: V41.
Kapsam: Mevcut eylemin yüzer görsel ifadesi.
Referans: 10 §31, §50; 11 §31.
FAB varlığı bu belgeyle zorunlu hale gelmez.
Tanımlı eylem bulunmuyorsa yüzer kontrol de bulunmaz.

### İlke V41.1 — Yüzer vurgu işin önemini izler.

Karar: Yalnız mevcut görevde yetkili eylem vurgulanır.
Gerekçe: Sürekli yüzmek gereksiz bir önem iddiasıdır.
Bedel: Her bağlam aynı belirgin kontrolü taşımaz.
İyi örnek: Tanımlı harita eylemi okunabilir yüzeyindedir.
Kötü örnek: Her yerde yeni rota başlatan artı.

### İlke V41.2 — Simgeyi hedef boyutu sınırlamaz.

Karar: İkon 24 tb; dokunma hedefi en az 48 tb.
Gerekçe: Yolda kullanım küçük hedeflerin hata bedelini artırır.
Bedel: Haritanın kullanılabilir alanından yer ayrılır.
İyi örnek: Küçük simge rahat hedef içinde görünür.
Kötü örnek: 24 tb simgenin tamamı dokunma hedefidir.

### İlke V41.3 — Opak yüzey hareketli zemini dengeler.

Karar: E1 kontrol yüzeyi kontrastlı ve öngörülebilirdir.
Gerekçe: Harita ayrıntısı kontrolün okunmasını değiştirmemelidir.
Bedel: Alttaki coğrafyanın küçük bölümü örtülür.
İyi örnek: Yazı ve simge sabit yüzeyde okunur.
Kötü örnek: Yol etiketleri cam butonun içinden geçer.

### İlke V41.4 — Göreve ait olmayan vurgu bulunmaz.

Karar: FAB reklam, Premium çağrısı veya AI vitrini olmaz.
Gerekçe: Eylem alanı karar yardımına ayrılmıştır.
Bedel: Sürekli ticari görünürlük fırsatından vazgeçilir.
İyi örnek: Mevcut eylemin anlamı kısa fiille belirtilir.
Kötü örnek: Parlayan AI küresi her görevi bastırır.

### İlke V41.5 — Görsel basılma sonucu taklit etmez.

Karar: Basılı görünüm ve tamamlanmış işlem ayrılır.
Gerekçe: Dokunma kaydın veya konumun doğrulandığını göstermez.
Bedel: Bekleyen ve sonuç durumları ayrıca açıklanır.
İyi örnek: Konum beklenirken kontrol bekleme durumundadır.
Kötü örnek: Dokunur dokunmaz başarı onayı belirir.

### Görsel durum matrisi:

| Durum | Görünüm | Korunan anlam |
| --- | --- | --- |
| Dinlenme | Opak kontrol yüzeyi | Eylem kullanılabilir |
| Odak | Odak sınırı görünür | Klavye hedefi belli |
| Basılı | Okunabilir sabit simge | Girdi alındı |
| Bekleme | Yerel bekleme ifadesi | Sonuç henüz yok |
| Başarısız | Yakın somut açıklama | Tekrar yetkisi korunur |
| Kullanılamaz | Açıklanmış pasiflik | Gizli işlem yapılmaz |
| Yüksek kontrast | Belirgin kontrol sınırı | Gölgeye bağımlılık yok |
| Büyük metin | Metinli varyant büyür | Eylem adı kesilmez |

### Biçim kararları:

| Özellik | Görsel sözleşme | Gerekçe |
| --- | --- | --- |
| Kontrol hedefi | Varsayılan 48 tb | Rahat dokunma |
| Küçük varyant | 44 tb alt sınır | Kabul edilmiş sınır |
| İkon kutusu | 24 tb başlangıç | Eylem tanınması |
| Yüzey | Harita kontrol yüzeyi | Zemin ayrımı |
| Elevation | E1 rolü | İçerik üstü kontrol |
| Gölge | Varsa yakın rol | Katman desteği |
| Odak | Ayrı odak vurgusu | Seçimle karışmama |
| Renk | Mevcut anlamsal rol | Yeni marka tonu yok |

### İyi ve kötü uygulama karşılaştırması:

| Bağlam | İyi | Kötü |
| --- | --- | --- |
| Atıf yakınlığı | Atıf görünür kalır | Sağlayıcı adı örtülür |
| Harita etiketi | Kontrol sınırı nettir | Yazılar birbirine karışır |
| Alt güvenli alan | Mevcut yerleşim korunur | Hedef sistem alanına taşar |
| Modal açık | Etkin görevin kontrolü | Arka görev FAB'ı parlar |
| Uzun etiket | Etiket gerektiğince büyür | Anlam üç noktayla kaybolur |
| Tek elle | Hedef çakışması yoktur | Bir dokunma iki eylemi tetikler |
| Premium | Aynı kontrol kalitesi | Ücretsiz kontrol daha silik |
| Hareket azaltma | Sabit durum değişimi | Zıplayan kontrol sürer |

Yüzer yüzey mevcut yerleşimin görev ilişkisini değiştirmez.
Yeni sabit konum veya yeni CTA sırası tanımlanmaz.
Aynı eylemi ikinci yüzer kopyayla çoğaltmak gerekmez.
Gölge silindiğinde kontrol hâlâ seçilebilir görünmelidir.
Haritanın gece görünümü kontrolü görünmez kılamaz.
Dairesel biçim yalnız gerçek dairesel kontrolü anlatır.
Dikdörtgen metinli kontrol otomatik kapsüle dönüştürülmez.
Simgenin merkezi ile optik ağırlığı birlikte değerlendirilir.
Kritik eylem anlaşılmıyorsa görünür adı korunur.
Apple ve Google benzetmesi yeni FAB ihtiyacı doğurmaz.
Material'ın belirgin eylem fikri görev yetkisiyle sınırlanır.
Cupertino benzeri sadelik mevcut eylemin kaybına dönüşmez.
Neden-sonuç: Kontrastlı yüzey, karmaşık zemindeki aramayı azaltır.
Bedel değerlendirmesi: Görünürlük için ayrılan alan sınırlıdır.
Kabul: Kontrol harita kullanmadan erişilen görevi değiştirmez.

- **Öz eleştiri Ö41.1 — FAB ölçülü kaldığında bulunabilirliği düşebilir; eylemi arama süresi incelenmelidir.**

- **Öz eleştiri Ö41.2 — Opak kontrol küçük haritada önemli ayrıntıyı kapatabilir; örtüşme kontrol edilmelidir.**

- **Öz eleştiri Ö41.3 — Tek simge farklı kullanıcıya farklı anlam taşıyabilir; adın yeterliliği sınanmalıdır.**

## Navigation Bar

Bölüm kimliği: V42.
Kapsam: Kabul edilmiş navigasyonun görsel tutarlılığı.
Referans: 01 §11; 11 §31.
Şamandıra, Keşfet, Neden Şamandıra? ve Ara korunur.
Bu bölüm yeni menü maddesi veya yerleşim üretmez.

### İlke V42.1 — Etkin konum açık ve sakin görünür.

Karar: Etkin bölüm metin, durum ve vurgu ile ayrılır.
Gerekçe: Kullanıcı yalnız marka renginden yerini çıkarmamalıdır.
Bedel: Etkinlik için küçük fakat tutarlı alan gerekir.
İyi örnek: Keşfet'in etkinliği renk kaybolsa da anlaşılır.
Kötü örnek: Yalnız çok hafif yeşil farkı kullanılır.

### İlke V42.2 — Ara bir eylem olarak görünür.

Karar: Ara'nın görsel hali sorgu başlatmayı açıklar.
Gerekçe: Arama ikinci sonuç merkezi değildir.
Bedel: Dört öğeyi birebir eşitleyen dekoratif simetri sınırlanır.
İyi örnek: Ara eylemi mevcut Keşfet bağlamını taşır.
Kötü örnek: Ara bağımsız keşif ürünü gibi adlandırılır.

### İlke V42.3 — Marka görev başlığını bastırmaz.

Karar: Marka kimliği sabit, içerik başlığı görev odaklıdır.
Gerekçe: Yer inceleyen kişi önce yeri tanımalıdır.
Bedel: Her görünümde büyük logo kullanımı terk edilir.
İyi örnek: Uzun yer adı okunabilir ağırlıkta kalır.
Kötü örnek: Logo gölgesi yer başlığından daha baskındır.

### İlke V42.4 — Geri ile hedef bağlantısı ayrılır.

Karar: Görsel etiket gerçek navigasyon anlamını izler.
Gerekçe: Doğrudan girişte hayalî geçmiş oluşturulamaz.
Bedel: Tek ok simgesini her bağlama yaymak mümkün değildir.
İyi örnek: Gerçek Keşfet hedefi adıyla görünür.
Kötü örnek: Ana sayfa bağlantısı geri oku gibi görünür.

### İlke V42.5 — Sabit yüzey içerik görünürlüğünü korur.

Karar: Mevcut sabit başlık E1 dilini kullanır.
Gerekçe: Başlık katmanı odaklı kontrolü örtememelidir.
Bedel: Dar alanda görsel sadelik daha sık sınanır.
İyi örnek: Başlık sınırı ince ve okunur kalır.
Kötü örnek: Büyük saydam başlık metnin üzerine yayılır.

### Görsel durum matrisi:

| Durum | Görünüm | Anlam |
| --- | --- | --- |
| Ana sayfa | Şamandıra kimliği | Mevcut ana hedef |
| Keşfet | Etkin bölüm göstergesi | Tek keşif alanı |
| Ara açık | Eylem durumu belirgin | Keşfet sorgu görevi |
| Yöntem bağlantısı | Bağlamsal bağlantı | Ana menüye eklenmez |
| Odak | Kesilmeyen vurgu | Geçerli giriş hedefi |
| Pasif öğe | Normal okunabilir metin | Hâlâ kullanılabilir |
| Bekleyen geçiş | Yerel durum işareti | Yeni sayfa kesinleşmedi |
| Uzun dil | Metin korunur | Ad değişmez |

### Görsel rol tablosu:

| Parça | Karar | Gerekçe |
| --- | --- | --- |
| Marka | Sistemle uyumlu sabit kimlik | Tutarlı tanınma |
| Eylem etiketi | Mevcut metin | Yeni kavram yok |
| Etkin işaret | Metni tamamlayan biçim | Renk dışı ayrım |
| Ayırıcı | Hafif ayırıcı rolü | Sakin sınır |
| Odak | Odak rengi | Etkinlikle ayrım |
| Üst yüzey | Opak ana/üst yüzey | Okunabilirlik |
| İkon | 20 veya 24 tb rolü | Tutarlı optik ağırlık |
| Hedef | 48 tb varsayılan | Tek elle erişim |

### Karşılaştırma:

| Gerilim | Benimsenen yön | Kaçınılan sonuç |
| --- | --- | --- |
| Apple tipi sadelik | Az eşzamanlı vurgu | Gizli görev adı |
| Google tipi bulunabilirlik | Açık eylem anlamı | Menü çoğaltma |
| Marka ve yer | Görev başlığı yeterli | Logo egemenliği |
| İkon ve metin | Açık adlar korunur | Şifre gibi simgeler |
| Masaüstü ve mobil | Aynı hedef anlamları | Ayrı ürün haritası |
| Sabitlik ve okuma | Sınır kontrollü | İçerik örtülmesi |
| Etkinlik ve odak | İki ayrı gösterge | Tek renk rolü |
| Premium ve ücretsiz | Eşit navigasyon kalitesi | Ücretli ana kapı |

Navigasyon etiketi reklam diliyle uzatılmaz.
Neden Şamandıra? sorusu kısaltılarak anlam kaybetmez.
Şehir adları ana navigasyon için yeni etiket değildir.
Kaydettiklerin mevcut Keşfet görevinde aynı dili sürdürür.
Profil görseli yeni bir kamusal profil merkezi ima etmez.
Bildirim göstergesi varsa gerçek durum anlamını taşır.
Okunmamış sayı motivasyon veya sosyal statü sayacı değildir.
Yüksek kontrastta seçili bölüm sınırı korunur.
Koyu temada etkinlik için neon parıltı eklenmez.
Etiket ağırlığı tüm satırı kalınlaştırmaya dönüşmez.
Uzun metin aynı görevde taşma yaratmamalıdır.
Navigasyon yüksekliği sabit metin kutusu değildir.
Neden-sonuç: Açık hedef dili yanlış geri beklentisini azaltır.
Bedel değerlendirmesi: Mutlak geometrik simetri amaç değildir.
Kabul: Menü adları ve görev ilişkileri referansla aynıdır.

- **Öz eleştiri Ö42.1 — Uzun Neden Şamandıra? etiketi dar alanda baskınlaşabilir; optik denge incelenmelidir.**

- **Öz eleştiri Ö42.2 — Etkinlik ve odak işaretleri birlikte karmaşıklaşabilir; ayrım öğrenilebilir olmalıdır.**

- **Öz eleştiri Ö42.3 — Sakin marka görünümü ilk ziyaretçide kimliği zayıflatabilir; tanınma araştırılmalıdır.**

## Tab Bar

Bölüm kimliği: V43.
Kapsam: Mevcut eş düzey türlerin sekme görsel dili.
Referans: 11 §31 ve §46; 10 §55.
Yeni alt navigasyon veya yeni portal önerilmez.
Rotalar, Gezeceğim Yerler ve Gezdiğim Yerler anlamı korunur.

### İlke V43.1 — Sekmeler aynı görevin türlerini gösterir.

Karar: Aynı düzeydeki mevcut türler görsel akrabalık taşır.
Gerekçe: Sekme yeni bir bağımsız ürün merkezi olmamalıdır.
Bedel: Her tür için ayrı marka dekoru kullanılamaz.
İyi örnek: Kayıt türleri aynı tipografiyle karşılaştırılır.
Kötü örnek: Rotalar sekmesi ayrı uygulama kapağına dönüşür.

### İlke V43.2 — Seçili tür kullanıcı durumudur.

Karar: Seçim dolgu, sınır veya işaretle desteklenir.
Gerekçe: Yeşil dolgu içerik kalitesini onaylamaz.
Bedel: Seçili ve başarı görünümleri dikkatle ayrılır.
İyi örnek: Gezdiğim Yerler etkin tür olarak okunur.
Kötü örnek: Seçili sekme tamamlanmış gezi rozeti taşır.

### İlke V43.3 — Etiketler kısaltmayla belirsizleşmez.

Karar: Gezeceğim ve Gezdiğim ayrımı tam okunur.
Gerekçe: Niyet ile gerçekleşmiş ziyaret aynı kayıt değildir.
Bedel: Metin büyütmede daha fazla alan gerekir.
İyi örnek: İki türün zaman anlamı görünür kalır.
Kötü örnek: İkisi yalnız benzer yer imi ikonlarıdır.

### İlke V43.4 — Sayaç yalnız kayıt miktarını açıklar.

Karar: Varsa sayı nötr metadata olarak görünür.
Gerekçe: Kayıt sayısı sosyal başarı veya borç değildir.
Bedel: Rekabet yaratan güçlü sayı vurgusundan vazgeçilir.
İyi örnek: Sayı etiketin okunmasını destekler.
Kötü örnek: Az gezi kırmızı eksiklik sayacıyla belirtilir.

### İlke V43.5 — Platform görünümü anlamı değiştirmez.

Karar: Native uyum aynı sekme isimlerini korur.
Gerekçe: Cihaz değişince görevler yeniden öğrenilmemelidir.
Bedel: Platform bileşenine körü körüne uyum mümkün değildir.
İyi örnek: Aynı tür her temada aynı seçimi taşır.
Kötü örnek: Android'de kayıtlar yeni ana menüye taşınır.

### Görsel durum matrisi:

| Durum | Görünüm | Sınır |
| --- | --- | --- |
| Seçilmemiş | Okunabilir etiket | Pasif değildir |
| Seçilmiş | Renk dışı işaret | Başarı değildir |
| Klavye odağı | Ayrı odak sınırı | Seçim zorlanmaz |
| Basılı | Yerel giriş tepkisi | Kayıt silinmez |
| Boş tür | Normal sekme dili | Tür cezalandırılmaz |
| Yükleniyor | İçerik durumu yakın | Sekme adı korunur |
| Hata | İlgili içerikte açıklama | Diğer türler silinmez |
| Büyük metin | Yüksekliği büyüyen etiket | Zaman anlamı korunur |

### Görsel ayrımlar:

| Kavram | İfade | Gerekçe |
| --- | --- | --- |
| Rotalar | Günlük taslak arşivi adı | Çalışma göreviyle ayrım |
| Gezeceğim Yerler | Niyet türü adı | Ziyaret iddiası yok |
| Gezdiğim Yerler | Kullanıcı beyanı türü | Memnuniyet iddiası yok |
| Aktiflik | Tek ilgili tür vurgusu | Okuma yönü |
| Kayıt sayısı | İkincil nötr bilgi | Yargı üretmeme |
| Ayırıcı | İlişkiyi gösteren sınır | Üç ayrı kart değil |
| Dokunma | 48 tb hedef | Rahat seçim |
| İkon | Metni destekler | Zaman kipini tek başına taşımaz |

### İyi ve kötü örnekler:

| Durum | İyi | Kötü |
| --- | --- | --- |
| Boş Rotalar | Nötr içerik durumu | Soluk ve erişilemez sekme |
| Çok kayıt | Okunabilir sayı | Taşan rozet |
| Uzun çeviri | Anlamlı metin korunur | Tür adı değişir |
| Koyu tema | Yüzey ve işaret ayrılır | Neon aktif hat |
| Hareket | Sınırlı durum geçişi | Her seçimde sallanma |
| Renk kaybı | Seçim işareti kalır | Tüm türler aynı görünür |
| Premium | Aynı görsel kalite | Ücretli sekme altınlaşır |
| Dönüş | Önceki tür belirgindir | Rastgele sekme vurgulanır |

Sekme kabuğu mevcut içerik yerleşimini yeniden tarif etmez.
Kaydırılabilirlik kararı kabul edilmiş davranışı izler.
Yeni kaydırma hareketi tek erişim yolu olarak önerilmez.
Aktif gösterge etiketin altını okunmaz hale getirmez.
Görsel yakınlık aynı göreve aidiyeti destekler.
Sekme aralığı dokunma hedeflerini birbirine bindirmez.
Tam yuvarlak stil ancak mevcut chip rolüyle tutarlıdır.
Sekme için otomatik yeni radius basamağı açılmaz.
Gezdiğim türünde kupa ve madalya bulunmaz.
Kaydetme başarısı otomatik tür değişimini görselleştirmez.
Kullanıcının mevcut seçimi yetkili durumu izler.
Material ile Cupertino kıyası burada anlam tutarlılığıdır.
Neden-sonuç: Açık kipler niyet ve ziyaret karışmasını azaltır.
Bedel değerlendirmesi: Kısa ikon dizisi kadar kompakt değildir.
Kabul: Üç kayıt türü hiçbir görsel durumda birleşmez.

- **Öz eleştiri Ö43.1 — Tam etiketler alan tüketir; büyütülmüş metindeki okunma sırası sınanmalıdır.**

- **Öz eleştiri Ö43.2 — Nötr sayaçlar kayıt miktarını az görünür yapabilir; bulunabilirlik gözlenmelidir.**

- **Öz eleştiri Ö43.3 — Ortak biçim tür farkını zayıflatabilir; metin ayrımının anlaşıldığı gösterilmelidir.**

## Search Tasarımı

Bölüm kimliği: V44.
Kapsam: Mevcut Keşfet sorgu durumunun görsel dili.
Referans: 01 §7; 11 E03; 10 B07.
Ad bulma ve ihtiyaca göre öneri aynı değildir.
Bu bölüm ikinci sonuç ekranı oluşturmaz.

### İlke V44.1 — Yazılan söz görünür kalır.

Karar: Sorgu metni okunabilir ana metin rolündedir.
Gerekçe: Kullanıcı yanlış anlaşılmayı kendi sözüyle karşılaştırır.
Bedel: Çok uzun sorgu daha fazla alan gerektirebilir.
İyi örnek: Anlaşılamayan ifade de metinde korunur.
Kötü örnek: AI özeti kullanıcının cümlesini görünmez kılar.

### İlke V44.2 — Kimlik önerisi uygunluk kartı değildir.

Karar: Ad, tür ve şube konumu birlikte görünür.
Gerekçe: Aynı ad yanlış yeri seçtirebilir.
Bedel: Kimlik satırı yalnız isimden daha uzundur.
İyi örnek: Aynı kafenin ilçeleri açıkça ayrılır.
Kötü örnek: İlk ad eşleşmesi en iyi sonuç rozetlidir.

### İlke V44.3 — Uygulanan koşul taslaktan ayrılır.

Karar: Mevcut durumu anlatan etiketler açık biçimde farklıdır.
Gerekçe: Yazmak koşulların uygulanması anlamına gelmez.
Bedel: Görsel sadelik içinde durum ayrımı taşınır.
İyi örnek: Sonuçların hangi sorguya ait olduğu anlaşılır.
Kötü örnek: Yeni metnin altında eski sonuç güncel görünür.

### İlke V44.4 — Alan etiketi yer tutucuya yüklenmez.

Karar: Sorgunun amacı alan doluyken de anlaşılır.
Gerekçe: Kaybolan örnek kalıcı etiket görevini göremez.
Bedel: Kısa açıklamaya görünür alan ayrılır.
İyi örnek: Genel arama ile yerel kayıt araması ayrılır.
Kötü örnek: İki arama da yalnız büyüteç gösterir.

### İlke V44.5 — AI yeteneği sakin durumlarla anlatılır.

Karar: Anlama, öneri bekleme ve sonuç ayrı okunur.
Gerekçe: Parıltı ve yazıyor gösterisi kanıt üretmez.
Bedel: Teknik olarak karmaşık işlem sade görünebilir.
İyi örnek: Gerekli netleştirme kısa ve belirgindir.
Kötü örnek: Sürekli ışıldayan alan sınırsız anlayış vaat eder.

### Görsel durum matrisi:

| Durum | Görünüm | Anlam |
| --- | --- | --- |
| Boş alan | Açık etiket ve örnek | Başlangıç |
| Yazılıyor | Kullanıcının metni | Henüz uygulanmadı |
| Odak | Belirgin alan sınırı | Etkin giriş |
| Kimlik önerisi | Ad ve konum | Bulma desteği |
| Öneri bekliyor | Yerel durum | Kesin sonuç değil |
| Sonuç bekliyor | Sorguyla bağlı durum | Güncel değerlendirme |
| Eşleşme yok | Sorgu ve kapsam korunur | Dünya hakkında yokluk değil |
| Offline | Yerel kapsam açık | İnternet araması değil |

### Arama görsel sözleşmesi:

| Parça | Karar | Gerekçe |
| --- | --- | --- |
| Alan gövdesi | 16/24 başlangıç | Ana giriş okunabilirliği |
| Alan radiusu | 8 tb | Kontrol ailesi |
| İç boşluk | Mevcut 16 tb başlangıç | Rahat giriş |
| Büyüteç | 20 veya 24 tb | Tanıdık eylem |
| Temizle | Ayrı anlaşılır hedef | Sorgu kontrolü |
| Şube bilgisi | Yeterli görünür konum | Kimlik ayrımı |
| Kritik koşul | Gövde düzeyi | Sessiz kaybı önleme |
| Odak tonu | Anlamsal odak rengi | Seçimden ayrım |

### İyi ve kötü karşılaştırması:

| Girdi | İyi görsel karşılık | Kötü görsel karşılık |
| --- | --- | --- |
| Yer adı | Şube açıklaması | Uygunluk yüzdesi |
| İhtiyaç cümlesi | Anlaşılan kapsam | Süslü slogan |
| Belirsiz şehir | Kısa açık ayrım | Otomatik tahmin vurgusu |
| Zorunlu koşul | Okunur koşul metni | Küçük silik chip |
| Sonuçsuzluk | Nötr açıklama | Kırmızı kullanıcı hatası |
| Servis arızası | Somut sorun | Boş sonuç gibi sessizlik |
| Geçmiş | Kullanıcı kapsamı belli | Trend arama görünümü |
| Büyük metin | Alan genişliği içinde sarım | Küçültülen sorgu |

Arama kutusu bir sohbet uygulaması kişiliğine dönüştürülmez.
Başlangıç örnekleri mevcut kapsamı aşan vaat içermez.
Kişisel hassas sorgu dekoratif öneri olarak yinelenmez.
Geçmiş satırı sorgunun tamamını kamusal örnek yapmaz.
Klavye önerisi ile gerçek sonuç aynı rozetle sunulmaz.
Türkçe karakterler sistem sans içinde açık seçilir.
Uzun yer adındaki ayırt edici son bölüm kesilmez.
Sorgu arka planı fotoğraf veya harita olmaz.
Hata sınırı yalnız kırmızı konturla anlatılmaz.
Doldurulmuş alan kilitli kontrol gibi gösterilmez.
AI yokluğu genel arama eylemini görsel olarak söndürmez.
Premium açıklaması arama sonucuna renk önceliği katmaz.
Neden-sonuç: Sorgu ve durum birlikteliği eski yanıt yanılmasını azaltır.
Bedel değerlendirmesi: Tek satırlık sade arama görüntüsü sınırlanır.
Kabul: Kullanıcı neyin arandığını ve neyin uygulandığını ayırır.

- **Öz eleştiri Ö44.1 — Sürekli kapsam göstermek alanı ağırlaştırabilir; gerekli bilgi önceliği sınanmalıdır.**

- **Öz eleştiri Ö44.2 — Kimlik ayrıntısı hızlı aramayı yavaşlatabilir; yanlış şube riskiyle birlikte değerlendirilmelidir.**

- **Öz eleştiri Ö44.3 — Sakin AI dili yeteneği görünmez kılabilir; anlaşılabilirlik parıltısız kanıtlanmalıdır.**

## Harita Bileşenleri

Bölüm kimliği: V45.
Kapsam: Aynı sonuçların yardımcı coğrafi görünümü.
Referans: 10 B31; 11 §31, §36, §40.
Harita odaklı kalite, okunur coğrafi ilişkiler demektir.
Ana navigasyonun harita portalına dönüşmesi anlamına gelmez.

### İlke V45.1 — Coğrafya karar metnini destekler.

Karar: Yer adları ve karar sınırları listede de bulunur.
Gerekçe: Harita okuryazarlığı temel görevin şartı olamaz.
Bedel: Aynı anlam iki sunumda tutarlı tutulur.
İyi örnek: Seçili yer iki görünümde aynı kimliktedir.
Kötü örnek: Kritik erişim yalnız harita işaretindedir.

### İlke V45.2 — Kontroller zeminden optik olarak ayrılır.

Karar: Kontroller opak harita yüzeyi dilini kullanır.
Gerekçe: Sokak ve etiket yoğunluğu değişkendir.
Bedel: Kontrol yüzeyi altındaki ayrıntı görünmez olur.
İyi örnek: Yakınlaştırma hedefi açık sınırla seçilir.
Kötü örnek: Soluk simge arazi dokusuna karışır.

### İlke V45.3 — Harita hareketi yeni sonuç iddiası değildir.

Karar: Mevcut kapsamla uygulanacak alan görsel olarak ayrılır.
Gerekçe: Pan, kullanıcının arama koşulunu sessizce değiştirmez.
Bedel: Coğrafi niyet ile uygulanan kapsam birlikte anlaşılmalıdır.
İyi örnek: Bu alanda ara mevcut eylem anlamını korur.
Kötü örnek: Harita kayınca sonuçlar habersiz yeniden sıralanır.

### İlke V45.4 — Konum kesinliği olduğundan güçlü görünmez.

Karar: Yaklaşık konumun görsel işareti metinle açıklanır.
Gerekçe: Noktanın hassas görünmesi adresi doğrulamaz.
Bedel: Kesin olmayan konum daha az yalın sunulur.
İyi örnek: Yaklaşık konum işareti uygun kapsamı taşır.
Kötü örnek: Geniş belirsizlik tek kesin giriş pini olur.

### İlke V45.5 — Tema coğrafi anlamı korur.

Karar: Gece görünümünde yol, su ve etiket ayrımı sürer.
Gerekçe: Koyu tema yalnız tüm görüntüyü karartmak değildir.
Bedel: Sağlayıcı görünümü ayrıca denetlenir.
İyi örnek: Gece haritasında seçili yer açıkça bulunur.
Kötü örnek: İnce yol çizgileri marka karanlığında kaybolur.

### Görsel durum matrisi:

| Durum | Görünüm | Korunan anlam |
| --- | --- | --- |
| Hazır | Okunur zemin ve kontrol | Aynı sonuç kümesi |
| Seçili yer | Ortak seçim vurgusu | Listeyle aynı yer |
| Pan sonrası | Uygulanan kapsam ayrımı | Sessiz arama yok |
| Harita bekliyor | Yerel yükleme alanı | Liste çalışabilir |
| Harita hatası | Açık sınırlılık | Yer bilgisi silinmez |
| Konum verilmedi | Nötr mevcut coğrafya | İzin zorunlu değil |
| Yaklaşık konum | Kapsamlı işaret | Kesin adres değil |
| Offline | Tarihli kullanılabilir kapsam | Canlılık iddiası yok |

### Katman ilişkileri:

| Katman | Görsel görev | Gerekçe |
| --- | --- | --- |
| Zemin | Coğrafi bağlam | Yön bulma |
| Yol ağı | Gerçek bağlantı | Yakınlığı anlamlandırma |
| Yer işareti | Doğru kimliğe erişim | Nokta ve yer ilişkisi |
| Seçim | İlgili yeri ayırma | Ortak durum |
| Rota | Sıra ve bağlantı | Günlük plan ilişkisi |
| Kontrol | E1 opak yüzey | Etkileşim okunabilirliği |
| Atıf | Gerekli görünür bilgi | Kaynak yükümlülüğü |
| Ölçek | Mesafe bağlamı | Yanlış yakınlık algısını azaltma |

### Yaklaşım karşılaştırması:

| Tasarım gerilimi | Şamandıra kararı | Kaçınılan yorum |
| --- | --- | --- |
| Apple ve Google | Coğrafi okunabilirlik alınır | İç motor üstünlüğü iddiası |
| Harita ve liste | Aynı sonucun iki ifadesi | İki ayrı öneri otoritesi |
| Zenginlik ve sadelik | İlgili coğrafya görünür | Bütün işaretleri gizleme |
| Marka ve sağlayıcı | Roller uyumlu | Atıf kaldırma |
| Gece ve gündüz | Aynı anlam | Negatif görüntü filtresi |
| Konum ve kimlik | Kapsam ayrı açıklanır | Nokta eşittir giriş |
| Yakınlık ve erişim | Fark korunur | Yakın eşittir yürünebilir |
| Premium ve ücretsiz | Aynı kritik okunabilirlik | Ücretli harita netliği |

Harita varsayılan olarak bütün ekranların arka planı değildir.
Görsel turistik his gerçek coğrafya ve içerikten gelir.
Kontrol yüzeyi önemli yol etiketlerini gereksiz kapatmaz.
Harita üzerinde tam paragraf duvarı oluşturulmaz.
Kısa özet kritik sınırı metin karşılığında korur.
Gri ölçekte seçili yer şekille ayırt edilir.
Yakınlaştırma simgeleri hedefleriyle birlikte değerlendirilir.
Harita atıfları düşük kontrastlı dekorasyona çevrilmez.
Kullanıcı konumunun görünümü yer kalitesiyle eşleşmez.
Harita kaydırma animasyonu azaltılmış harekette sürdürülmez.
Fotoğraf veya doku yol ağının yerini almaz.
Renkler coğrafi tehlike hakkında yeni iddia üretmez.
Yeni harita kumandası bu bölümle eklenmez.
İki görünümde farklı güncellik varsa sınır açık kalır.
Okunamayan sağlayıcı katmanı marka efektiyle örtülmez.
Yerel kayıt kapsamı haritada ülke kapsamı gibi görünmez.
Neden-sonuç: Katman ayrımı hareket sırasında görsel aramayı azaltır.
Bedel değerlendirmesi: Fazla sadelik coğrafi ayrıntıyı azaltabilir.
Kabul: Harita yokken temel karar bilgisi ulaşılabilir kalır.

- **Öz eleştiri Ö45.1 — Yardımcı harita coğrafi düşünen kişiye ikincil gelebilir; erişimin görünürlüğü incelenmelidir.**

- **Öz eleştiri Ö45.2 — Zemin sadeleştirme gerekli geçiş ayrıntısını silebilir; gerçek çevre örnekleri değerlendirilmelidir.**

- **Öz eleştiri Ö45.3 — Opak kontroller küçük alanı kaplayabilir; örtüşme ve okunabilirlik birlikte sınanmalıdır.**

## Marker Sistemi

Bölüm kimliği: V46.
Kapsam: Mevcut yer ve durakların harita işaretleri.
Referans: 10 B31, B33; 02 §6, §8.
Marker kimlik ve seçim taşır; kalite notu taşımaz.
Yeni yer sınıfı veya genel güven rozeti oluşturulmaz.

### İlke V46.1 — İşaret bir yeri açıkça temsil eder.

Karar: Görsel işaretin adı ve konumu aynı kimliğe bağlıdır.
Gerekçe: Yanlış şube bütün karar bilgisini geçersizleştirir.
Bedel: Birbirine yakın adların ayrımı ek açıklama ister.
İyi örnek: Halka + nokta işareti doğru ilçe bilgisiyle eşleşir.
Kötü örnek: Benzer adlı iki şube tek işaret olur.

### İlke V46.2 — Seçim renk dışı farkla görünür.

Karar: Seçili işarette sınır veya biçim farkı bulunur.
Gerekçe: Renk körlüğü seçim bilgisini ortadan kaldıramaz.
Bedel: Seçim sınırının komşu hedefi örtmediği doğrulanır.
İyi örnek: Renk kalkınca seçili halka + nokta yine ayrılır.
Kötü örnek: Yeşilin iki yakın tonu tek ayrımdır.

### İlke V46.3 — Boyut kaliteyi derecelendirmez.

Karar: Marker büyüklüğü etkileşim ve yoğunluk ihtiyacına bağlıdır.
Gerekçe: İşaret büyüklüğü daha iyi yer anlamına gelmemelidir.
Bedel: Pazarlama önceliği görsel hacimle verilemez.
İyi örnek: Seçili yer mevcut sınır ve işaretle ayrılır.
Kötü örnek: Ücretli restoran dev işaretle öne çıkarılır.

### İlke V46.4 — Durak sayısı yalnız sıra bilgisidir.

Karar: Rota numarası sıralı ziyaret ilişkisini anlatır.
Gerekçe: Birinci durak en iyi yer değildir.
Bedel: Sıra işareti kategori simgesinden ayrılır.
İyi örnek: Üçüncü durak listede de üçüncüdür.
Kötü örnek: Bir numaralı işaret şampiyon rozeti taşır.

### İlke V46.5 — Durum simgesi geniş güvence üretmez.

Karar: Bilinmeyen ve engel açıklaması ilgili metinde bulunur.
Gerekçe: Tek simge erişim zincirini doğrulayamaz.
Bedel: Bazı durumlar daha uzun açıklama gerektirir.
İyi örnek: Giriş bilgisi kapsamıyla açıklanır.
Kötü örnek: Erişim simgeli işaret tüm yeri onaylar.

### Görsel durum matrisi:

| Durum | Görünüm | Anlam |
| --- | --- | --- |
| Normal yer | Ortak marker ailesi | Yer kimliği |
| Seçili yer | Sınır veya biçim farkı | Kullanıcı seçimi |
| Odaklı yer | Ayrı odak işareti | Yardımcı giriş hedefi |
| Rota durağı | Okunur sıra numarası | Ziyaret sırası |
| Kayıtlı niyet | Varsa nötr kayıt durumu | Gidildi demek değil |
| Ziyaret beyanı | Ayrı mevcut durum | Beğeni demek değil |
| Kritik sınır | Metinle eşlenen işaret | Genel kötü yer değil |
| Yakın kümelenme | Cluster sözleşmesi | Kimlik kaybolmaz |

### Marker karar tablosu:

| Parça | Karar | Gerekçe |
| --- | --- | --- |
| İç simge | 16/20/24 ailesinden | Ortak ikon dili |
| Görsel gövde | Mevcut halka + nokta | K8 işaret kilidi |
| Dokunma hedefi | 48 tb varsayılan hedef | Rahat kullanım |
| Dar hedef | 44 tb alt sınırı | Ürün sınırını koruma |
| Seçim sınırı | Algılanabilir kontur | Renk dışı anlam |
| Rakam | Sistem sans ve açık biçim | Sıra okunması |
| Etiket | Doğru yer adı | Kimlik doğrulama |
| Zemin ilişkisi | Tema içinde karşıtlık | Haritadan ayrışma |

### İyi ve kötü karşılaştırması:

| Konu | İyi | Kötü |
| --- | --- | --- |
| Restoran türü | Nötr tür simgesi | Lezzet yıldızı |
| Otel türü | Aynı Yer ailesi | Lüks altın işaret |
| Seçim | Açık durum işareti | Güven mührü |
| Fotoğrafsız yer | Eşit marker görünürlüğü | Önemsiz küçük nokta |
| Yeni kayıt | Aynı kimlik standardı | Parlayan yeni cevher |
| Rota numarası | Dizi konumu | Kalite sıralaması |
| Bilgi eksikliği | İlgili sınır açıklaması | Genel soru işaretli kötü yer |
| Premium | Aynı marker dili | Ödeme ile boyut artışı |

Yerin koordinatı bina girişini göstermeyebilir.
İşaret biçimi bu kapsam farkını gizlemez.
Yakın marker hedefleri birbirini örten alanlara dönüşmez.
Yoğunlukta görünürlüğün çözümü keyfî yer gizleme değildir.
Cluster ile tek yer işaretinin anlamı ayrılır.
Bir marker aynı anda bütün durum rozetlerini taşımaz.
Kritik sınırın metin karşılığı her zaman korunur.
Koyu temada marker sınırı açık zemindekiyle eşdeğerdir.
Gölge marker görünürlüğünün tek güvencesi değildir.
Dolu simge yalnız tanımlı seçili anlamda kullanılır.
Kayıtlı niyet kalp biçimiyle beğeniye dönüşmez.
Ziyaret sayısı marker çevresinde prestij halkası üretmez.
Kategori renkleri yeni uygunluk sözlüğü kurmaz.
İkon çizgisi yoğun haritada parçalanmadan seçilmelidir.
Seçim değişince coğrafi nokta başka yere sıçramaz.
Marker şekli K8 ve plan/tasarim/yon.md §5.7 içindeki halka + nokta kilidini korur.
Neden-sonuç: Biçimle desteklenen seçim tarama hatasını azaltır.
Bedel değerlendirmesi: Tek biçim ailesi kategori çeşitliliğini sınırlar.
Kabul: Halka + nokta korunur; jenerik damla pin kullanılmaz.

- **Öz eleştiri Ö46.1 — Tek aile farklı yer türlerini benzeştirebilir; kimlik etiketinin yeterliliği sınanmalıdır.**

- **Öz eleştiri Ö46.2 — Seçim sınırı yoğun alanda komşu işareti örtebilir; hedef ayrımı korunmalıdır.**

- **Öz eleştiri Ö46.3 — Sıra numarası kalite olarak okunabilir; kullanıcı anlatımıyla anlam doğrulanmalıdır.**

## Cluster Yapısı

Bölüm kimliği: V47.
Kapsam: Mevcut sonuç işaretlerinin görsel gruplaması.
Referans: 10 B31; 11 §40.
Cluster yeni sonuç kümesi veya öneri sınıfı değildir.
Bu bölüm algoritma, eşik veya yeni açılma akışı tanımlamaz.

### İlke V47.1 — Küme sayısı yalnız yer adedidir.

Karar: Sayı gruptaki mevcut sonuç miktarını gösterir.
Gerekçe: Yoğun yer kümesi popülerlik göstergesi değildir.
Bedel: Görsel yoğunluk için duygusal renkler kullanılamaz.
İyi örnek: Küme sayısı nötr rakamla okunur.
Kötü örnek: Çok yer sıcak renkli cazibe alanıdır.

### İlke V47.2 — Küme tek yerden ayırt edilir.

Karar: Grup gövdesi marker ailesiyle akraba fakat farklıdır.
Gerekçe: Kullanıcı bir işaretin tek kimlik olmadığını anlamalıdır.
Bedel: Görsel sözlükte küçük ek ayrım gerekir.
İyi örnek: Birden fazla öğe anlamı sayıdan anlaşılır.
Kötü örnek: Küme normal yer fotoğrafı gibi görünür.

### İlke V47.3 — Seçili kimlik kümede kaybolmaz.

Karar: Mevcut seçimin grupla ilişkisi açık biçimde korunur.
Gerekçe: Yakınlaştırma düzeyi karar bağlamını silemez.
Bedel: Seçim ile küme durumu birlikte düşünülür.
İyi örnek: Liste seçimi harita yoğunluğunda da anlaşılır.
Kötü örnek: Küme oluşunca seçili yer belirsizleşir.

### İlke V47.4 — Sayılar okunabilir kalır.

Karar: Rakam alanı basamak sayısını kesmeden taşır.
Gerekçe: 9 ile 99 aynı görsel alana zorlanmamalıdır.
Bedel: Küme ölçüsü içerik uzunluğuna uyarlanabilir.
İyi örnek: Rakam ve çevresi dengeli boşluk taşır.
Kötü örnek: Üç basamak küçük daire dışına taşar.

### İlke V47.5 — Gruplama erişim alternatifini gizlemez.

Karar: Aynı öğeler listede anlaşılır biçimde bulunur.
Gerekçe: Küme çözümlemek tek seçim yolu olamaz.
Bedel: Harita ve liste ilişkisi sürekli doğrulanır.
İyi örnek: Kümedeki yerlerin adları eşdeğer listede okunur.
Kötü örnek: Küme açılmadan hiçbir yer adı öğrenilemez.

### Görsel durum matrisi:

| Durum | Görünüm | Anlam |
| --- | --- | --- |
| Küçük küme | Okunur adet | Birden çok sonuç |
| Yoğun küme | Aynı nötr aile | Daha iyi bölge değil |
| Seçim içeriyor | Seçim ilişkisi görünür | Seçili yer korunur |
| Odak | Belirgin odak sınırı | Geçerli hedef |
| Yakınlaştırma değişimi | Tutarlı grup geçişi | Aynı kimlikler |
| Sonuç yenileme | Bağlamlı bekleme | Adet kesinleşmedi |
| Veri hatası | Eski kapsam ayrımı | Sıfır sonuç sanılmaz |
| Yüksek kontrast | Sayı ve sınır korunur | Dolguya bağımlı değil |

### Görsel gruplama tablosu:

| Özellik | Karar | Gerekçe |
| --- | --- | --- |
| Sayı dili | Nötr sistem sans | Hızlı miktar okuma |
| Vurgu | Seçim veya odak için | Popülerlik üretmeme |
| Kenar | Zeminle ayrışan sınır | Grup görünürlüğü |
| İç boşluk | Rakamı sıkıştırmayan ölçek | Basamak okunabilirliği |
| Renk | Mevcut anlamsal roller | Yeni ısı haritası yok |
| Gölge | İkincil destek | Sınırın yerini almama |
| Dokunma | Ortak hedef sözleşmesi | Harita kullanım kolaylığı |
| Etiket | Grup anlamı | Tek yer yanılmasını önleme |

### İyi ve kötü örnekler:

| Bağlam | İyi | Kötü |
| --- | --- | --- |
| Şehir merkezi | Nötr yoğunluk | En iyi bölge parıltısı |
| Az kayıt | Aynı görsel değer | Soluk önemsiz çevre |
| Seçili küme | Açık seçim ilişkisi | Genel onay işareti |
| Üç basamak | Rakamın tamamı | Kesilmiş sayı |
| Koyu tema | Kontrollü ton farkı | Siyah içinde kaybolma |
| Fotoğraf | Grup nötr kalır | Rastgele yer fotoğrafı |
| Premium | Aynı küme kalitesi | Ücretli özel kümeler |
| Hata | Kapsamlı açıklama | Sessiz boş harita |

Küme adedi yer kalitesinin vekili olarak kullanılamaz.
Kapsanmayan çevre boş ve değersiz çevre gibi anlatılmaz.
Görsel yoğunluk mevcut sonuç sayısından türetilir.
Yeni arama sonucu sayısı bu belgeyle artırılmaz.
Küme rengi restoran, otel veya gezi fiyatını derecelendirmez.
Rakam boyutu gövde ölçeğinden bağımsız keyfî küçülmez.
Kontrol hedefleri yoğunlaşınca birbirine bindirilmez.
Grup çözülmesinin hareketi minimum görsel değişim taşır.
Azaltılmış harekette patlayan pin animasyonu kullanılmaz.
Seçim dışındaki yerler yok olmuş gibi silikleştirilmez.
Harita sağlayıcısının gruplaması ürün kararını değiştiremez.
Aynı kümedeki bütün yerlerin aynı koşulu taşıdığı varsayılmaz.
Genel erişim simgesi cluster üzerine damgalanmaz.
Küme bilgisi satır içi metinle de açıklanabilir.
Ekran büyümesi gruplamanın anlamını değiştirmez.
Birlikte görünmek aynı rota içinde bulunmak değildir.
Neden-sonuç: Nötr adet kullanımı popülerlik yanılmasını sınırlar.
Bedel değerlendirmesi: Isı haritası kadar çarpıcı görünmez.
Kabul: Küme tek yer veya uygunluk notu gibi okunmaz.

- **Öz eleştiri Ö47.1 — Nötr gruplar yoğunluk farkını az gösterebilir; rakam tarama başarısı araştırılmalıdır.**

- **Öz eleştiri Ö47.2 — Seçimi kümede korumak işaret karmaşıklığı yaratabilir; yakın alanlarda incelenmelidir.**

- **Öz eleştiri Ö47.3 — Değişken rakam genişliği görsel ritmi bozabilir; okunabilirlik önce değerlendirilmelidir.**

## Route Çizimleri

Bölüm kimliği: V48.
Kapsam: Mevcut günlük rotanın görsel bağlantı dili.
Referans: 06 §5, §9; 10 B04/B31; 11 E07/E08.
Bu bölüm çizim üretmez; çizgilerin anlamını tanımlar.
Rota geometrisi yürünebilirlik veya güvenlik kanıtı değildir.

### İlke V48.1 — Çizgi gerçek bilginin kapsamını taşır.

Karar: Bilinen geometri ile şematik ilişki aynı görünmez.
Gerekçe: İki nokta arasındaki çizgi geçerli yol kanıtlamaz.
Bedel: Eksik bağlantı daha az tamamlanmış görünebilir.
İyi örnek: Bilinmeyen geçiş metin karşılığıyla açıklanır.
Kötü örnek: Kuş uçuşu çizgi kesin yürüyüş güzergâhıdır.

### İlke V48.2 — Sıra listede ve haritada aynıdır.

Karar: Durak numarası aynı yetkili diziyi temsil eder.
Gerekçe: Görsel güzellik için sıra değiştirilemez.
Bedel: Haritada çizgiler her zaman temiz ayrışmayabilir.
İyi örnek: İkinci durak iki görünümde aynı yerdir.
Kötü örnek: Kesişimi azaltmak için durak sırası değiştirilir.

### İlke V48.3 — Ana hat diğer bilgiyi örtmez.

Karar: Hat kalınlığı yer adları ve yol ayrımını korur.
Gerekçe: Rota okunurken çevre ilişkisi de anlaşılmalıdır.
Bedel: En kalın ve parlak çizgi kullanılmaz.
İyi örnek: Hat izlenir, altındaki önemli kavşak anlaşılır.
Kötü örnek: Işıklı kalın şerit bütün sokakları kapatır.

### İlke V48.4 — Taslak ve değerlendirme ayrılır.

Karar: Yeni kişisel sıra eski olumlu sonuçla boyanmaz.
Gerekçe: Düzenleme sonrası yapılabilirlik yeniden değerlendirilir.
Bedel: Bekleme halinde tam rota güveni görüntüsü oluşmaz.
İyi örnek: Yeni dizi beklerken önceki süre ayrılır.
Kötü örnek: Sürüklenen durak anında onaylı yeşile döner.

### İlke V48.5 — İlerleme tamamlatma baskısı yaratmaz.

Karar: Kullanıcı beyanı ve kalan plan nötr ayrılır.
Gerekçe: Erken bitiş başarısız gezi değildir.
Bedel: Oyunlaştırılmış tamamlama görselleri kullanılmaz.
İyi örnek: Bitirilmiş ziyaret geçmişteki yerini korur.
Kötü örnek: Atlanan durak kırmızı kayıp puan üretir.

### Görsel durum matrisi:

| Durum | Görünüm | Anlam |
| --- | --- | --- |
| Bilinen bağlantı | Açık izlenebilir hat | Bilinen yol kapsamı |
| Eksik geometri | Sınırı belirtilen ilişki | Yol garanti değil |
| Seçili bölüm | Kontrollü yerel vurgu | İncelenen geçiş |
| Taslak değişti | Bekleme ayrımı | Yeni sonuç henüz yok |
| Önceki değerlendirme | Tarihli bağlam | Bugünkü onay değil |
| Bilinen engel | Metinle eşlenen durum | İlgili dizi etkilenir |
| Beyan edilen ziyaret | Nötr geçmiş durumu | Memnuniyet değil |
| Offline düzenleme | Cihaz kapsamı belirgin | Canlı hesap yok |

### Çizgi ve bilgi ilişkisi:

| Parça | Görsel karar | Gerekçe |
| --- | --- | --- |
| Ana rota | İzlenebilir tek vurgu | Dizi okunması |
| Alternatif | İkincil fakat seçilir | Seçim eşitliği |
| Durak numarası | Açık sistem rakamı | Liste eşleşmesi |
| Başlangıç | Kapsamıyla belirtilir | Kapıdan kapıya yanılmasını önleme |
| Bitiş | Açık mevcut seçim | Dönüş varsaymama |
| Süre | Birimi ve aralığıyla | Tahmin kesinleşmez |
| Uyarı | İlgili bölümle bağlı | Genel rota puanı yok |
| Harita kontrolü | E1 yüzey | Çizgiden ayrım |

### İyi ve kötü karşılaştırması:

| Gerilim | İyi | Kötü |
| --- | --- | --- |
| Estetik ve gerçeklik | Geometriye sadık hat | Güzel görünen uydurma yol |
| Kısa ve doğru | Kapsamlı süre | Dönüşü saklayan toplam |
| Erişim ve yakınlık | Ayrı bilgi | Yeşil hatla erişim onayı |
| Sıra ve kalite | Durak numarası | Birinciye altın rozet |
| Bekleme ve başarı | Sonuç ayrımı | Peşin uygunluk ışığı |
| Alternatif ve ana | Açık fark | Geri plana gömülen seçenek |
| Koyu tema | Yol çevresi korunur | Neon ve parıltı |
| Erken bitiş | Nötr kalan dizi | Eksik görev kırmızısı |

Rota çizgisi animasyonu sürekli takip hissi yaratmaz.
Canlı güncelleme yoksa nabız atan konum kullanılmaz.
Mesafe rakamının birimi metinden koparılmaz.
Yürüyüş ile araç bağlantısı veri kapsamını izler.
Farklı ulaşım modu yeni marka rengi gerektirmez.
Kesişen hatlarda sıra metinle doğrulanabilir kalır.
Gidiş ve dönüş yalnız gerçekten dahilse gösterilir.
Tarihsiz fikir bugünün güzergâhı gibi başlıklandırılmaz.
Sabitlenen saat, sıra numarasından ayrı anlam taşır.
Kullanıcının tercihi uygunluk rengiyle onaylanmaz.
Yer silme görünümü geçmiş ziyareti yeniden yazmaz.
Kayıtlı rota kapağı bugünkü kontrol tarihi değildir.
Çizgi inceyse yüksek kontrastta sınırı korunmalıdır.
Renk kaybında ana ve alternatif ilişki anlaşılır kalır.
Yol sağlayıcısı atfı rota çizgisinin altında kaybolmaz.
Çok günlük otel takvimi bu görsel sözleşmeye girmez.
Neden-sonuç: Kapsamlı hat dili sahte yapılabilirlik algısını azaltır.
Bedel değerlendirmesi: Eksik bilgi görsel bütünlüğü kesebilir.
Kabul: Güzel rota görünümü kanıtsız süre veya erişim üretmez.

- **Öz eleştiri Ö48.1 — Sınırları ayrı anlatmak rotayı karmaşık gösterebilir; temel sıra okunması sınanmalıdır.**

- **Öz eleştiri Ö48.2 — İnce hat yoğun şehirde kaybolabilir; gerçek harita örneklerinde kontrast incelenmelidir.**

- **Öz eleştiri Ö48.3 — Nötr geçmiş gösterimi tamamlanan ziyareti zayıflatabilir; hatırlama kolaylığı değerlendirilmelidir.**

## AI Kartları

Bölüm kimliği: V49.
Kapsam: Mevcut AI açıklamalarının görsel ifade sözleşmesi.
Referans: 03 §8, §15; 10 §15; 11 E03/E04/E07.
AI kartı yeni sohbet merkezi veya bilgi otoritesi değildir.
Aynı karar bilgisi bütün kanallarda aynı sınırı taşır.

### İlke V49.1 — AI görünümü kanıttan güçlü değildir.

Karar: Açıklama ortak kart yüzeyinde sade biçimde sunulur.
Gerekçe: Parlayan çerçeve metne sahte doğruluk atfedebilir.
Bedel: AI yeteneği ayrı görsel gösteri kazanmaz.
İyi örnek: Gerekçe ve ilgili belirsizlik birlikte okunur.
Kötü örnek: Mor parıltı altında AI onaylı etiketi.

### İlke V49.2 — Olumlu ve sınırlayıcı bilgi birlikte görünür.

Karar: Kritik ödün ve bilinmeyen gövde düzeyinde kalır.
Gerekçe: Çekici özet sonradan açıklanan engeli telafi etmez.
Bedel: Bazı kartların yüksekliği artar.
İyi örnek: Sohbet gerekçesinin yanında akşam sınırı vardır.
Kötü örnek: Olumlu başlık büyük, erişim belirsizliği diptedir.

### İlke V49.3 — Üretim süreci gösteri değildir.

Karar: Bekleme ve tamamlanmış açıklama açıkça ayrılır.
Gerekçe: Akıcı yazılma gerçek kararın doğruluğunu kanıtlamaz.
Bedel: Sürekli hareketli üretim hissi kullanılmaz.
İyi örnek: Yanıt beklemesi ilgili görevle adlandırılır.
Kötü örnek: Model düşüncesi dekoratif satırlarla akıtılır.

### İlke V49.4 — İç değerlendirmeler vitrine çıkmaz.

Karar: Yüzde, güven sayacı ve yıldız bulunmaz.
Gerekçe: Güven tek iddiaya, uygunluk ziyaret bağlamına aittir.
Bedel: Tek bakışlık sayısal kıyas yerine metin gerekir.
İyi örnek: Kısa yol karşılığındaki ses farkı anlatılır.
Kötü örnek: %98 sana uygun kart rozeti.

### İlke V49.5 — Eksik açıklama gerçek içerikle sınırlanır.

Karar: Bilinen kimlik AI yanıtı yokken de okunur.
Gerekçe: AI katmanı bütün yer bilgisini bekletemez.
Bedel: Kart bazen daha az zengin görünür.
İyi örnek: Yer bilgisi açık, değerlendirme sınırı bellidir.
Kötü örnek: Fotoğraf ve kimlik sonsuz shimmer altında kalır.

### Görsel durum matrisi:

| Durum | Görünüm | Anlam |
| --- | --- | --- |
| Desteklenen açıklama | Ortak karar kartı | İlgili dayanak var |
| Koşullu anlatım | Koşul yakın gövde | Kapsam sınırlı |
| Bilinmeyen | Nötr somut açıklama | Olumlu hüküm yok |
| Yeni yanıt bekliyor | Yerel bekleme | Önceki yanıt ayrılır |
| Kısmi bilgi | Bilinen bölüm görünür | Tam cevap iddiası yok |
| Hizmet hatası | İlgili sorun açıklaması | Yer kötü değildir |
| Kullanıcı düzeltmesi | Düzeltilen bağlam belirgin | AI sözü değişmez otorite değil |
| Offline | Tarihli okunabilir kapsam | Güncel değerlendirme yok |

### AI kartı görsel rolleri:

| Parça | Karar | Gerekçe |
| --- | --- | --- |
| Yüzey | Ana yüzey, E0 | Ortak karar hiyerarşisi |
| Radius | 12 tb | Kart ailesi |
| İç boşluk | 16/24 tb | Dar/geniş ritim |
| Başlık | 20/28, 600 | Karar adı |
| Açıklama | 16/24, 400 | Rahat okuma |
| Kritik sınır | Ana gövde karşıtlığı | Gizlenmeyen belirsizlik |
| Destek bilgisi | İkincil rol | Kontrollü ayrıntı |
| Durum | Metin ve mevcut rol | Yeni AI rengi yok |

### İyi ve kötü karşılaştırması:

| Konu | İyi | Kötü |
| --- | --- | --- |
| Bilgi türü | Çıkarım kapsamıyla | Doğrulanmış mühür |
| Kart başlığı | Somut gerekçe | Kusursuz seçim |
| Bekleme | Göreve bağlı | Sihirli düşünce gösterisi |
| Kaynak | Gerekli yöntem/atıf | Ham yorum dökümü |
| Premium | Aynı bilgi standardı | Daha doğru AI vaadi |
| Kimlik | Doğru yer | Yapay kişilik avatarı |
| Belirsizlik | Yakın açık cümle | Silik dipnot |
| Eylem | Mevcut kullanıcı kararı | Habersiz rota ekleme |

AI etiketi yalnız üretim yöntemi gerçekten ilgiliyse kullanılır.
Süs ikonu doğrulama statüsü gibi görünmez.
Kartın renkli kenarı uygunluk ölçeği kurmaz.
Açıklama fazla uzunsa anlamlı paragraf grupları kullanılır.
Bu gruplama mevcut bilgi sırasını değiştirmez.
Yanıtın cümle cümle gelişi kritik sınırı geciktiremez.
Kullanıcının kendi ihtiyacı görsel olarak geri plana itilmez.
Düzeltme hakkı devre dışı veya önemsiz görünmez.
İç muhakeme kullanıcı güveni için sergilenmez.
Anlaşılamayan koşul gerçekleşmiş koşul gibi gösterilmez.
Yöntem bağlantısı her iddianın eksiğini devralamaz.
AI açıklamasında özel veriler dekorasyon için tekrarlanmaz.
Doğru bilgi kötü tipografiyle cezalandırılmaz.
Ticari ilişki kartın renk gücünü artırmaz.
Kısa açıklama tam uygunluk garantisine dönüşmez.
Kullanıcının ret eylemi hata rengiyle yargılanmaz.
Neden-sonuç: Ortak yüzey AI'ı kararın okunabilir parçası yapar.
Bedel değerlendirmesi: Ayrı AI görünürlüğü sınırlıdır.
Kabul: Kart bilgiyi gerekçesi ve sınırıyla birlikte anlatır.

- **Öz eleştiri Ö49.1 — Ortak kart dili AI yardımını görünmez kılabilir; yeteneğin anlaşılması araştırılmalıdır.**

- **Öz eleştiri Ö49.2 — Belirsizlik metni kartı uzatabilir; kritik bilgi taraması ölçülmelidir.**

- **Öz eleştiri Ö49.3 — Sayısal puan olmadan kıyas bazı kullanıcılara zor gelebilir; ortak karar ölçütleri sınanmalıdır.**

## Seyahat Kartları

Bölüm kimliği: V50.
Kapsam: Mevcut günlük rota, taslak ve kayıt özetlerinin dili.
Referans: 06 §15–20; 11 E07/E08 ve §46.
Seyahat kartı adı çok günlük seyahat yönetimi açmaz.
Mevcut günlük karar ve kayıt bağlamı korunur.

### İlke V50.1 — Kart günün amacını açıklar.

Karar: Başlık mevcut amaç veya kullanıcının verdiği addır.
Gerekçe: Seyahat güzelliği yapılacak işi gizlememelidir.
Bedel: Her kayıt pazarlama başlığı taşımaz.
İyi örnek: Kısa yürüyüş ve sohbet amacı okunur.
Kötü örnek: Kaçırılmayacak mükemmel gün başlığı.

### İlke V50.2 — Kayıt yaşamı uygunluktan ayrılır.

Karar: Kayıtlı taslak ve güncel değerlendirme farklı açıklanır.
Gerekçe: Kaydetmek bugün için yapılabilirlik onayı değildir.
Bedel: Tarih ve kapsam bilgisine yer ayrılır.
İyi örnek: Tarihsiz taslak açıkça belirtilir.
Kötü örnek: Eski kayıt güncel onay işaretiyle görünür.

### İlke V50.3 — Toplamlar kapsamıyla okunur.

Karar: Süre aralığı ve dönüş kapsamı birlikte gösterilir.
Gerekçe: Eksik toplam yanlış zaman beklentisi yaratır.
Bedel: Büyük tek rakamdan daha fazla metin gerekir.
İyi örnek: İlk duraktan itibaren, dönüş hariç süre.
Kötü örnek: Başlangıç bilinmezken kapıdan kapıya toplam.

### İlke V50.4 — Fotoğraf kaydı onaylamaz.

Karar: Varsa gerçek fotoğraf karar metnine eşlik eder.
Gerekçe: Güzel kapak güncel yol ve ücret kanıtı değildir.
Bedel: Fotoğrafsız kayıtlar da eşit kalitede sunulur.
İyi örnek: Metinli taslak aynı hiyerarşiyi korur.
Kötü örnek: Kapaksız rota soluk ve eksik görünür.

### İlke V50.5 — Paylaşım türü görünür anlamını korur.

Karar: Özel taslak ve paylaşılan seçim karıştırılmaz.
Gerekçe: Görsel birliktelik istemeden yayın izlenimi doğurmamalıdır.
Bedel: Kayıt durumları için net metin gerekir.
İyi örnek: Paylaşılan sürümün kapsamı açık kalır.
Kötü örnek: Her düzenlenen kart yayınlandı işareti taşır.

### Görsel durum matrisi:

| Durum | Görünüm | Anlam |
| --- | --- | --- |
| Boş taslak | Nötr başlık ve durum | Saklanabilir çalışma |
| Tarihsiz taslak | Açık zaman sınırı | Bugüne onay yok |
| Değerlendirilmiş | Gerekçe ve koşul | Belirli kapsam |
| Düzenlenmiş | Yeni seçim görünür | Eski sonuç ayrılır |
| Kaydediliyor | İşlem durumu | Kayıt henüz teyitsiz |
| Kayıtlı | Somut kayıt teyidi | Ziyaret değil |
| Paylaşılan | Seçili paylaşım kapsamı | Özel kopya değil |
| Bitirilmiş | Nötr geçmiş | Başarı puanı değil |

### Kart bilgi rolleri:

| Parça | Görsel karar | Gerekçe |
| --- | --- | --- |
| Amaç/ad | Kart başlığı | Kaydı tanıma |
| Şehir | Görünür kimlik bağlamı | Yanlış coğrafyayı önleme |
| Tarih | Gerçek kapsamıyla | Eskiyi yeni sanmama |
| Süre | Birim ve aralık | Tahmin anlamı |
| Duraklar | Mevcut sıra/özet | Plan ilişkisi |
| Kritik koşul | Ana gövde | Yapılabilirlik sınırı |
| Kayıt durumu | Nötr açıklama | Yaşam döngüsü |
| Kapak | Gerçek ve isteğe bağlı | Temsil desteği |

### İyi ve kötü örnekler:

| Konu | İyi | Kötü |
| --- | --- | --- |
| Başlık | Kullanıcının günü | Genel tur paketi |
| Durak sayısı | Nötr miktar | Tamamlama hedefi |
| Bütçe | Kapsamlı bilinen tutar | Eksik ücreti sıfır sayma |
| Tarih | Kaydın gerçek tarihi | Bugüne otomatik taşıma |
| Erken bitiş | Nötr geçmiş | Eksik seri rozeti |
| Premium | Aynı temel kart kalitesi | Altın güven kapağı |
| Paylaşım | Açık kapsam | Otomatik kamusal görünüm |
| Offline | Cihazdaki taslak | Güncel rota sözü |

Kart radiusu 12 tb, sıradan yüzeyi E0'dır.
Dar iç boşluk 16 tb, geniş iç boşluk 24 tb'dir.
Başlık 20/28 ve gövde 16/24 başlangıcını sürdürür.
Tarih veya durak adı küçük yazıya sıkıştırılmaz.
Gezeceğim listesi rota arşivi olarak yeniden adlandırılmaz.
Gezdiğim ziyaretleri otomatik bu günün durakları değildir.
Bir İz katkı sayısı seyahat kartını derecelendirmez.
Kullanıcının verdiği özel ad kamusal slogan sayılmaz.
Paylaşımda hassas başlangıç bilgisi süs metni yapılmaz.
Görsel özet kaybolan durakları tam rota gibi sunmaz.
Kritik koşul sığmıyorsa olumlu anlatım daralır.
Kayıt tarihi bütün yerlerin kontrol tarihi değildir.
Fotoğraf varlığı ödeme veya rezervasyon teyidi değildir.
Rota görseli yeni şehirler arası kapsam yaratmaz.
Kart işlemleri mevcut eylem sırasını izler.
Yeni rezervasyon CTA'sı bu bölümle eklenmez.
Neden-sonuç: Yaşam durumu ayrımı eski kayda aşırı güveni azaltır.
Bedel değerlendirmesi: Kapak ağırlıklı gezi kartı kadar kısa değildir.
Kabul: Kart günlük karar, kayıt ve güncelliği karıştırmaz.

- **Öz eleştiri Ö50.1 — Çok durum bilgisi arşiv taramasını ağırlaştırabilir; kimlik önceliği sınanmalıdır.**

- **Öz eleştiri Ö50.2 — Tarihsiz kartlar eksik ürün gibi algılanabilir; taslak anlamı araştırılmalıdır.**

- **Öz eleştiri Ö50.3 — Fotoğrafsız eşitlik duygusal tanınmayı azaltabilir; ad ve amaçla geri bulma incelenmelidir.**

## Restoran Kartları

Bölüm kimliği: V51.
Kapsam: Mevcut Yer modelindeki restoran varyantı.
Referans: 01 §2, §6; 02 §4–9; 11 E04.
Restoran ayrı katalog, puan veya rezervasyon ürünü değildir.
Yalnız eldeki karar bilgisi görsel olarak düzenlenir.

### İlke V51.1 — Yer kimliği yemekten önce tanınır.

Karar: Ad, tür ve şube konumu birlikte okunur.
Gerekçe: Çekici yemek fotoğrafı doğru işletmeyi belirlemez.
Bedel: Fotoğrafın baskınlığı sınırlanır.
İyi örnek: Aynı adlı restoranların ilçeleri görünür.
Kötü örnek: Büyük tabak görseli şube bilgisini saklar.

### İlke V51.2 — Yemek görseli genel kalite puanı değildir.

Karar: Gerçek fotoğraf somut görünümü destekler.
Gerekçe: İyi ışık lezzet veya hizmet garantisi vermez.
Bedel: Fotoğraf çekiciliği organik vurguyu satın alamaz.
İyi örnek: Gerçek salona ait bağlamlı fotoğraf.
Kötü örnek: Yapay yemek görseli gerçek menü gibi görünür.

### İlke V51.3 — Beslenme koşulu kapsamıyla görünür.

Karar: Doğrulanmış koşul ve bilinmeyen ayrı açıklanır.
Gerekçe: Bir menü seçeneği geniş sağlık güvencesi değildir.
Bedel: Kısa ikon dizisi bütün anlamı taşıyamaz.
İyi örnek: Bilinen olanak ile doğrulanmayan kapsam ayrıdır.
Kötü örnek: Yeşil yaprak bütün ihtiyaçlara uygunluk mührüdür.

### İlke V51.4 — Fiyat rolü gerçek kapsamı taşır.

Karar: Tutarın kişi/ürün, para birimi ve tarihi korunur.
Gerekçe: Fiyat algısı kullanıcının bütçe sınırı değildir.
Bedel: Tek para simgesi yeterli sayılmaz.
İyi örnek: Tarihli kapsamlı fiyat bilgisi okunur.
Kötü örnek: Belirsiz pahalı simgesi kesin toplam yerine geçer.

### İlke V51.5 — Rezervasyon bilgisi işlem teyidi değildir.

Karar: Mevcut kullanım koşulu nötr açık metinle görünür.
Gerekçe: Gereklilik yer ayrıldığı anlamına gelmez.
Bedel: Rezervasyon sitesine benzeyen hızlı satış dili kullanılmaz.
İyi örnek: Önceden rezervasyon gerektiği açıklanır.
Kötü örnek: Gerekli koşul yeşil rezerve edildi rozetidir.

### Görsel durum matrisi:

| Durum | Görünüm | Sınır |
| --- | --- | --- |
| Kimlik bulundu | Ad ve şube | Önerilmiş sayılmaz |
| Amaç destekleniyor | Somut gerekçe | Genel lezzet puanı yok |
| Akşam sesi belirsiz | Yakın bilgi sınırı | Gündüz bilgisi taşınmaz |
| Fiyat eski | Tarihli kapsam | Bütçe uyumu yok |
| Rezervasyon gerekli | Açık kullanım koşulu | İşlem yapılmadı |
| Beslenme bilgisi eksik | Somut bilinmeyen | Uygunluk varsayılmaz |
| Kapalı | Erken ziyaret engeli | Fotoğrafın ardına gizlenmez |
| Fotoğraf yok | Eşit metin kartı | Kalite düşüklüğü değil |

### Restoran bilgisi görsel rolleri:

| Bilgi | Rol | Gerekçe |
| --- | --- | --- |
| Ad/şube | Kart başlığı ve konum | Doğru kimlik |
| Tür | Nötr açıklama | Temel beklenti |
| Sohbet gerekçesi | Gövde | Amaç ilişkisi |
| Ses koşulu | Kapsamlı gövde | Saat ayrımı |
| Maliyet | Birimli gerçek bilgi | Bütçe karşılaştırması |
| Kullanım kuralı | İlgili karar bilgisi | Olanağın sınırı |
| Erişim | Somut alan kapsamı | Genel güvence yok |
| Fotoğraf | Gerçek bağlam | Görünüm desteği |

### İyi ve kötü örnekler:

| Konu | İyi | Kötü |
| --- | --- | --- |
| Kalabalık | Zaman kapsamıyla | Popülerlik ateşi |
| Lezzet | Dayanaklı somut anlatım | Beş yıldız |
| Bütçe | Kişi/toplam ayrımı | Pahalı eşittir premium |
| Diyet | Doğrulanmış dar koşul | Genel güvenlik rozeti |
| Bekleme | Süre kapsamıyla | Kesin yer bulma vaadi |
| Menü | Gerçek bilgi | Üretilmiş tabak fotoğrafı |
| Şube | Açık konum | Birleştirilmiş kimlik |
| Ticari ilişki | Karar vurgusundan ayrı | Sponsor parlak çerçevesi |

Restoran kartı ortak 12 tb radiusu kullanır.
Yüzeyi sıradan Yer kartıyla aynı E0 düzeyindedir.
Yemek türü için yeni özel yazı ailesi açılmaz.
Restoran adı metin büyütmede kesilmez.
Fotoğraf üzerinde fiyat veya kritik sınır taşınmaz.
Bilinen kapanma estetik bütünlük uğruna küçültülmez.
Basamaksız giriş bütün salonlara erişim anlamına gelmez.
Çocuk sandalyesi genel aile dostu rozeti üretmez.
Düşük müzik boş masa bulunduğunu kanıtlamaz.
Masa bulunması bilgisayarla çalışma izni değildir.
İlgili kullanım koşulu görsel hiyerarşide yerini korur.
Bir İz katkısı yorum yıldızı olarak gösterilmez.
Kullanıcının kaydı işletmeye kalite puanı vermez.
Premium kullanıcı farklı restoran gerçeği görmez.
Bu varyant yeni yemek siparişi akışı yaratmaz.
Dış bağlantı mevcut pratik bilgi sözleşmesini izler.
Neden-sonuç: Ortak ölçütler fotoğrafın karar üzerindeki baskısını sınırlar.
Bedel değerlendirmesi: Ticari menü kataloglarından daha az gösterişlidir.
Kabul: Restoran kartı nedeni, ödünü ve sınırı birlikte taşır.

- **Öz eleştiri Ö51.1 — Az fotoğraf vurgusu yemek kararının duygusal yönünü azaltabilir; gerçek seçim ihtiyacı incelenmelidir.**

- **Öz eleştiri Ö51.2 — Beslenme sınırları metni uzatabilir; yanlış güvenceyi önleme başarısı ölçülmelidir.**

- **Öz eleştiri Ö51.3 — Yıldızsız kıyas alışkanlığı zorlayabilir; somut farkların anlaşılması sınanmalıdır.**

## Etkinlik Kartları

Bölüm kimliği: V52.
Kapsam: Varsa mevcut Yer bağlamındaki zamanlı faaliyet bilgisi.
Referans: 02 §4; 06 §4–5; 11 E04/E07.
Bağımsız etkinlik ekranı veya bilet akışı oluşturulmaz.
Veri ve kabul edilmiş bağlam yoksa bu varyant uygulanmaz.

### İlke V52.1 — Zaman kimliğin parçası olarak okunur.

Karar: Gerçek tarih ve saat kapsamı açık görünür.
Gerekçe: Aynı yerdeki farklı günler farklı deneyimlerdir.
Bedel: Fotoğrafın yanında zaman bilgisi için alan gerekir.
İyi örnek: Belirli yerin belirli tarihli faaliyeti.
Kötü örnek: Tarihsiz etkinlik posteri güncel görünür.

### İlke V52.2 — Faaliyet yeriyle karıştırılmaz.

Karar: Etkinlik adı ve ev sahibi Yer kimliği ayrılır.
Gerekçe: Program varlığı mekânın her günkü niteliği değildir.
Bedel: Tek büyük başlık bütün bilgiyi taşıyamaz.
İyi örnek: Yer adı konumuyla ayrıca okunur.
Kötü örnek: Konser adı restoranın yeni kimliği olur.

### İlke V52.3 — Katılım koşulu karar metnidir.

Karar: Varsa giriş, yaş, saat veya rezervasyon koşulu görünürdür.
Gerekçe: Güzel afiş kullanım sınırını geçersiz kılamaz.
Bedel: Promosyon gibi kısa kart görünümü sınırlanır.
İyi örnek: Son giriş saati ilgili tarihle okunur.
Kötü örnek: Önemli koşul küçük afiş yazısına bırakılır.

### İlke V52.4 — Kapasite yalnız dayanak kadar anlatılır.

Karar: Canlı yer ve bilet durumu uydurulmaz.
Gerekçe: Program duyurusu boş kapasite kanıtı değildir.
Bedel: Hızlı satış uyandıran sayı rozetleri kullanılmaz.
İyi örnek: Katılım durumu bilinmiyorsa sınır açıklanır.
Kötü örnek: Son iki bilet sayacı veri olmadan görünür.

### İlke V52.5 — Süresi geçen bilgi nötr ayrılır.

Karar: Geçmiş tarih güncel seçenek gibi parlamaz.
Gerekçe: Eski faaliyet bugünün ziyaret gerekçesi olamaz.
Bedel: Bazı kayıtlar görsel olarak daha sakin görünür.
İyi örnek: Geçmiş program açık tarihli bilgi olarak kalır.
Kötü örnek: Eski afiş bugün katıl çağrısı taşır.

### Görsel durum matrisi:

| Durum | Görünüm | Anlam |
| --- | --- | --- |
| Geçerli tarihli bilgi | Tarih ve yer açık | Program kapsamı |
| Saat bilinmiyor | Somut bilgi eksiği | Zaman uydurulmaz |
| Katılım şartlı | Koşul yakın gövde | Otomatik katılım yok |
| Kapasite bilinmiyor | Nötr sınır | Yer garantisi yok |
| Erteleme doğrulanmış | Değişen tarih açık | Eski bilgi kullanılmaz |
| İptal doğrulanmış | Erken ziyaret engeli | Afiş baskın değil |
| Tarih geçmiş | Geçmiş bağlamı | Bugünkü öneri değil |
| Veri yok | Varyant kullanılmaz | Yeni katalog yok |

### Bilgi görsel rolleri:

| Parça | Karar | Gerekçe |
| --- | --- | --- |
| Faaliyet adı | Somut kısa başlık | Kimlik |
| Yer adı | Açık ayrı bağlam | Ev sahibiyle ayrım |
| Tarih | Gerçek yerel kapsam | Zaman doğruluğu |
| Saat | Birimi ve tarih ilişkisi | Yanlış gün yanılmasını önleme |
| Son giriş | Kritik koşul | Ziyaret yapılabilirliği |
| Maliyet | Kapsamlı tutar | Bütçe ilişkisi |
| Afiş/fotoğraf | İzinli gerçek medya | Somut temsil |
| Durum | Metinle desteklenen rol | Renk yeterli değil |

### İyi ve kötü örnekler:

| Konu | İyi | Kötü |
| --- | --- | --- |
| Tarih | Gün ve kapsam açık | Sadece cuma |
| Saat | Yerel anlamı belli | Belirsiz zaman dilimi |
| Afiş | Metin erişilebilir karşılık | Bütün bilgi resimde |
| İlgi | Mevcut amaçla gerekçe | Viral rozet |
| Bilet | Yalnız bilinen koşul | Satın alma akışı icadı |
| İptal | Erken açık bilgi | Kırpılmış küçük dipnot |
| Fotoğraf | Gerçek faaliyet bağı | Stok kalabalık |
| Kapsam | Yer varyantı | Bağımsız etkinlik portalı |

Kart gövdesi ortak Yer kartı rolündedir.
Radius 12 tb, normal akış E0 olarak kalır.
Afişin yazı stili ürün tipografisine aktarılmaz.
Metinsel tarih afişten ayrı okunabilir kalır.
Renkli etkinlik posteri CTA rengini belirlemez.
Tema değişimi gerçek afiş renklerini tersine çevirmez.
Gece yarısı geçişi tarih bağlamını kaybetmez.
Etkinlik süresi ulaşım ve bekleme toplamı değildir.
Program saati kullanıcının rezervasyon teyidi değildir.
Kalabalık fotoğrafı olağan yoğunluk ölçümü değildir.
Çocukların görünmesi çocuklar için uygunluk üretmez.
Katılım şartı varsa dayanağı aşan simge kullanılmaz.
Etkinlik kaydı tamamlandı gezi rozetine dönüşmez.
Rota içinde geçiş ve varış ayrı değerlendirilir.
Gösterişli afiş kritik belirsizliği örtemez.
Yeni takvim veya bilet kategorisi bu bölümle açılmaz.
Neden-sonuç: Zamanın açık kimliği eski program yanılmasını azaltır.
Bedel değerlendirmesi: Poster odaklı karttan daha çok metin taşır.
Kabul: Tarih, yer ve katılım sınırı aynı okumada anlaşılır.

- **Öz eleştiri Ö52.1 — Koşullu varyant eksik içerik izlenimi yaratabilir; veri olmadan sunum açılmamalıdır.**

- **Öz eleştiri Ö52.2 — Tarih ayrıntısı başlığı bastırabilir; tarama sırası değerlendirilmelidir.**

- **Öz eleştiri Ö52.3 — Afişin metinsel karşılığı tekrar yaratabilir; erişilebilir bilgiyle gereksiz tekrar ayrılmalıdır.**

## Otel Kartları

Bölüm kimliği: V53.
Kapsam: Varsa mevcut Yer modelindeki konaklama varyantı.
Referans: 01 §6; 02 §4, §15; 11 E04.
Otel varyantı bağımsız katalog veya rezervasyon merkezi değildir.
Veri bulunmuyorsa yeni ticari alan veya eylem üretilmez.

### İlke V53.1 — Konaklama ortak Yer dilini korur.

Karar: Kimlik, gerekçe, ödün ve sınır aynı sıradadır.
Gerekçe: Tür değişimi uygunluk yaklaşımını değiştirmez.
Bedel: Alışılmış otel satış düzeni aynen kopyalanmaz.
İyi örnek: Otelin konumu ve kullanım koşulu okunur.
Kötü örnek: Oda fiyatı bütün karar bilgisini bastırır.

### İlke V53.2 — Ticari yıldız genel üstünlük değildir.

Karar: Genel değerlendirme yıldızı veya güven puanı üretilmez.
Gerekçe: Yüksek fiyat ve sınıf kişisel uygunluğu kanıtlamaz.
Bedel: Hızlı prestij kıyasına dayanılmaz.
İyi örnek: Kullanıcının amacıyla ilgili somut koşul.
Kötü örnek: Altın beş yıldız en iyi seçenek iddiası.

### İlke V53.3 — Oda fotoğrafı kapsamıyla sunulur.

Karar: Gösterilen alan bütün konaklama deneyimine genellenmez.
Gerekçe: Bir oda resmi tüm odaları doğrulamaz.
Bedel: Fotoğraf bağlamı için kısa açıklama gerekebilir.
İyi örnek: Gösterilen bölüm biliniyorsa açık belirtilir.
Kötü örnek: En geniş oda tüm odaların standardıdır.

### İlke V53.4 — Fiyat ve müsaitlik uydurulmaz.

Karar: Yalnız mevcut kapsamlı bilgi gösterilir.
Gerekçe: Eski ücret bugün boş oda olduğu anlamına gelmez.
Bedel: Satış sitesindeki hızlı fiyat avantajı kullanılmaz.
İyi örnek: Tarihli fiyat sınırı açıkça okunur.
Kötü örnek: Güncel veri olmadan gecelik fırsat etiketi.

### İlke V53.5 — Erişim yalnız doğrulanan yolu kapsar.

Karar: Giriş, oda veya tesis bilgisi ayrı kapsam taşır.
Gerekçe: Basamaksız lobi bütün odalara erişimi kanıtlamaz.
Bedel: Tek erişilebilir otel rozeti yeterli değildir.
İyi örnek: Bilinen giriş ile bilinmeyen kat ayrılır.
Kötü örnek: Rampa fotoğrafı bütün tesisi onaylar.

### Görsel durum matrisi:

| Durum | Görünüm | Anlam |
| --- | --- | --- |
| Kimlik bulundu | Ad ve konum | Doğru Yer kaydı |
| Amaç ilgili | Somut gerekçe | Genel en iyi değil |
| Fiyat tarihli | Kapsamlı maliyet | Bugünkü teklif değil |
| Fiyat bilinmiyor | Nötr sınır | Ücretsiz sayılmaz |
| Müsaitlik bilinmiyor | Açık bilgi eksiği | Boş oda garantisi yok |
| Giriş koşulu var | Yakın koşul metni | İşlem yapılmış değil |
| Erişim eksik | İlgili bölüm açıklaması | Genel olumlu hüküm yok |
| Varyant verisi yok | Ortak bilinen içerik | Ticari katalog açılmaz |

### Otel kartı rolleri:

| Bilgi | Görsel karar | Gerekçe |
| --- | --- | --- |
| Yer adı | Kart başlığı | Kimlik |
| Konum | Şube/şehir bağlamı | Yanlış oteli önleme |
| Tür | Nötr yer türü | Beklenti çerçevesi |
| Kullanım koşulu | İlgili gövde | Ziyaret sınırı |
| Maliyet | Tarih ve kapsam | Fiyat yanılmasını önleme |
| Fiziksel erişim | Somut dar bilgi | Genel mühür yok |
| Fotoğraf | Gerçek alan | Temsil açıklığı |
| Eylem | Yalnız mevcut Yer eylemi | Yeni rezervasyon yok |

### Airbnb ve Booking üzerinden tasarım okuması:

| Tasarım gerilimi | Şamandıra tercihi | Bedel |
| --- | --- | --- |
| Deneyim hissi / bilgi yoğunluğu | Gerçek fotoğraf ve kısa koşul | Sınırlı görsel alan |
| Kişilik / karşılaştırma | Ortak ölçütlerle yer karakteri | Serbest stil azalır |
| İlham / fiyat taraması | Amaç ve maliyet kapsamı birlikte | Tek rakam yeterli değil |
| Konaklama / günlük karar | Mevcut Yer kapsamı | Seyahat yönetimi yok |
| Fotoğraf / kanıt | Görünüm destekleyici | Güvence vermez |
| Aciliyet / özerklik | Nötr gerçek durum | Dönüşüm baskısı yok |
| Yorum / içgörü | Gerekçe ve bilgi sınırı | Ham sosyal kanıt yok |
| Marka / uygunluk | Aynı kart ailesi | Prestij dekoru sınırlı |

Bu kıyas güncel rakip özelliklerinin eksiksiz envanteri değildir.
Karşılaştırma iki tasarım gerilimini düşünme aracıdır.
Airbnb tarzı yakınlık kişisel ev sahibi kurgusu doğurmaz.
Booking tarzı yoğunluk rezervasyon alanı açma gerekçesi değildir.
Bu belgede otel rezervasyonu yapılmış gibi gösterilmez.
Otelin koşulu günlük rota toplamından ayrı değerlendirilir.
Çok günlük takvim, uçuş ve transfer kartları eklenmez.
Kart radiusu 12 tb ve yüzeyi E0 olarak kalır.
Fiyat için yeni dev sayı hiyerarşisi oluşturulmaz.
Fotoğraf üstüne kritik kullanım kuralı yerleştirilmez.
Tema değişikliği odanın gerçek ışığını değiştirmez.
Lüks fotoğraf daha koyu veya büyük kart gerektirmez.
Az bilgili yer görsel olarak düşük kalite sınıfına konmaz.
Güncel veri eksikliği görsel fırsat etiketiyle örtülmez.
Kullanıcının niyet kaydı oda ayrılması değildir.
Premium ücretsiz kullanıcıdan daha doğru otel bilgisi satmaz.
Neden-sonuç: Ortak Yer dili türler arasında karar kıyasını korur.
Bedel değerlendirmesi: Otel satış sitelerinin katalog yoğunluğu alınmaz.
Kabul: Otel varyantı yeni rezervasyon veya seyahat kapsamı yaratmaz.

- **Öz eleştiri Ö53.1 — Ortak kart konaklamanın özel ihtiyaçlarını eksik gösterebilir; yalnız mevcut kapsamda sınanmalıdır.**

- **Öz eleştiri Ö53.2 — Fiyat belirsizliği kullanıcıya yetersiz gelebilir; görsel güven yerine bilgi açığı izlenmelidir.**

- **Öz eleştiri Ö53.3 — Prestij sembollerini kaldırmak tanınmayı azaltabilir; somut koşullarla kıyas araştırılmalıdır.**

## Fotoğraf Kullanımı

Bölüm kimliği: V54.
Kapsam: Gerçek yerlerin izinli fotoğraf dili.
Referans: 10 B32 ve §52; 11 E04.
Bu görev fotoğraf veya görsel dosya üretmez.
Kararlar mevcut gerçek medyanın kullanım sınırlarıdır.

### İlke V54.1 — Gerçeklik çekicilikten önce gelir.

Karar: Fotoğraf doğru yere ve ilgili bölüme ait olmalıdır.
Gerekçe: Başka yerin güzelliği yanlış beklenti üretir.
Bedel: Fotoğrafsız kart sayısı artabilir.
İyi örnek: Doğru girişe ait bağlamlı çekim.
Kötü örnek: Stok sahil gerçek park fotoğrafı olarak görünür.

### İlke V54.2 — Kırpma karar bilgisini korur.

Karar: Kartta 4:3 başlangıç, gerektiğinde anlamı koruyan oran.
Gerekçe: Giriş basamağını kesmek koşulu yanlış anlatır.
Bedel: Bütün fotoğraflar birebir eş biçimli kalmayabilir.
İyi örnek: Erişim ayrıntısı görünür kadrajda tutulur.
Kötü örnek: Simetri için merdiven fotoğraftan çıkarılır.

### İlke V54.3 — Renk düzeni mekânı yeniden yaratmaz.

Karar: Anlam değiştiren sıcaklık, ışık ve içerik müdahalesi yapılmaz.
Gerekçe: Geceyi gündüz veya kalabalığı sakin göstermek yanıltır.
Bedel: Fotoğraflar ortak filtre estetiği taşımaz.
İyi örnek: Gerçek ışık koşulu korunur.
Kötü örnek: Bütün mekânlar sıcak ve boş hale getirilir.

### İlke V54.4 — Metin fotoğrafın insafına bırakılmaz.

Karar: Kritik karar bilgisi opak okunabilir yüzeyde kalır.
Gerekçe: Değişen kadraj metnin kontrastını oynatır.
Bedel: Tam görsel kart yaklaşımı sınırlanır.
İyi örnek: Kapanma açıklaması fotoğraftan bağımsızdır.
Kötü örnek: Kırmızı uyarı renkli afişin üzerindedir.

### İlke V54.5 — Alternatif anlatım görüneni açıklar.

Karar: Anlamlı fotoğraf somut metin karşılığı taşır.
Gerekçe: Görselden çıkarılmayan erişim veya güvence eklenemez.
Bedel: Medya başına içerik değerlendirmesi gerekir.
İyi örnek: Ana girişte görünen basamak anlatılır.
Kötü örnek: Görselden bütün yer erişilebilir diye yazılır.

### Görsel durum matrisi:

| Durum | Görünüm | Sınır |
| --- | --- | --- |
| Doğru fotoğraf | Anlamlı kadraj | Gerçek yer |
| Tarihi biliniyor | İlgili tarih bilgisi | Genel güncellik değil |
| Tarihi bilinmiyor | Tarih uydurulmaz | Güncel çekim iddiası yok |
| Fotoğraf yok | Nitelikli metin kartı | Sahte gerçeklik yok |
| Yükleniyor | Ayrılmış medya alanı | Metin beklemez |
| Yükleme hatası | Nötr medya durumu | Yer bilgisi silinmez |
| Hak geri çekildi | İzinli kapsam güncellenir | Eski görsel kullanılmaz |
| Koyu tema | Gerçek renk korunur | Ters filtre yok |

### Fotoğraf rolleri:

| Rol | Görsel karar | Gerekçe |
| --- | --- | --- |
| Kart fotoğrafı | 4:3 başlangıç | Tutarlı kıyas |
| Ayrıntı fotoğrafı | Doğal anlamlı oran | İçeriği koruma |
| Giriş fotoğrafı | Giriş bütünü görünür | Fiziksel koşul |
| Ortam fotoğrafı | Doğru bölüm | Yanlış genelleme önleme |
| Yemek fotoğrafı | Gerçek sunum | Temsil dürüstlüğü |
| Caption | 13/20 başlangıç | Okunur bağlam |
| Kritik bağlam | Gövdeye de taşınır | Dipnotla gizlememe |
| Eksik medya | Nötr yer tutucu veya metin | Kalite yargısı yok |

### İyi ve kötü örnekler:

| Konu | İyi | Kötü |
| --- | --- | --- |
| Kalabalık | Gerçek anın kapsamı | İnsanları silerek sakinlik |
| Işık | Çekim koşulu korunur | Sürekli altın saat filtresi |
| Giriş | Basamak görünür | Engel dışarı kırpılır |
| Hak | İzinli medya | Bulunan her fotoğraf |
| Yapay üretim | Gerçek yer yerine kullanılmaz | AI restoran fotoğrafı |
| Mahremiyet | Gerekli maskeleme sınırı açık | İnsan kimliği dekor olur |
| Galeri | Mevcut kontrollü gezinme | Otomatik carousel |
| Temsil | Doğru şube | İsim benzerliğiyle fotoğraf |

Görsel turistik his gerçek çevrenin niteliğinden doğar.
Bütün fotoğrafları tek marka tonuna boyamak gerekmez.
Fotoğraf başına görünmeyen kalite skoru oluşturulmaz.
Yüksek çözünürlük düşük kontrastlı metni mazur göstermez.
Büyük medya kullanımı çekirdek karar bilgisini geciktirmez.
Hedefler fotoğraf yüklenince yer değiştirmemelidir.
Fotoğraf yokluğu sayfayı boş durum haline getirmez.
Erişim kanıtı görselin varlığından ayrıca değerlendirilir.
Açık alan fotoğrafı yağmurda kullanım garantisi değildir.
Boş salon fotoğrafı güncel kapasite iddiası değildir.
Geniş açı alan büyüklüğüne ilişkin beklentiyi çarpıtabilir.
Bu risk kadraj ve açıklamada dikkate alınır.
Tekrarlanan dekoratif görsel gereksiz sesli tekrar yaratmaz.
Anlamlı görsel dekoratif diye erişimden çıkarılmaz.
Renkli fotoğraf durum paletini yeniden tanımlamaz.
Fotoğraf seçimi ticari görünürlük avantajı yaratamaz.
Neden-sonuç: Anlamı koruyan kadraj yanlış fiziksel beklentiyi azaltır.
Bedel değerlendirmesi: Kusursuz eş kapak estetiği sınırlanabilir.
Kabul: Görsel yerin koşulunu olduğundan iyi göstermez.

- **Öz eleştiri Ö54.1 — Eşit oranı esnetmek kart ritmini bozabilir; anlam korunurken kıyas incelenmelidir.**

- **Öz eleştiri Ö54.2 — Fotoğrafsız sunum bazı yerleri unutulur yapabilir; geri bulma araştırılmalıdır.**

- **Öz eleştiri Ö54.3 — Bağlam açıklamaları fotoğrafı ağırlaştırabilir; kritik ve ikincil ayrım sınanmalıdır.**

## Gradient Kullanımı

Bölüm kimliği: V55.
Kapsam: Mevcut yüzeylerde ton geçişinin görsel sınırı.
Referans: 10 §14, §19, §51.
Gradient yeni marka paleti veya bilgi katmanı değildir.
Varsayılan karar yüzeyleri düz ve okunabilirdir.

### İlke V55.1 — Düz yüzey temel karar taşıyıcısıdır.

Karar: Gerekçe ve kritik koşul opak düz yüzeyde okunur.
Gerekçe: Ton değişimi metin kontrastını öngörülemez yapar.
Bedel: Parlak ve gösterişli yüzey çeşitliliği sınırlanır.
İyi örnek: Kart metni sabit ana yüzeydedir.
Kötü örnek: Her paragraf farklı renk geçişinde yüzmektedir.

### İlke V55.2 — Gradient anlam üretmez.

Karar: Renk geçişi kalite veya uygunluk derecesi değildir.
Gerekçe: Sıcak-soğuk geçişi gizli değerlendirme ölçeği kurabilir.
Bedel: Tek bakışlık duygusal puanlama kullanılmaz.
İyi örnek: Anlamın tamamı metin ve durumdadır.
Kötü örnek: Yeşile yakın yer daha güvenilir görünür.

### İlke V55.3 — Medya koruması kanıtı kapatmaz.

Karar: Görsel ton örtüsü kritik fiziksel ayrıntıyı gizleyemez.
Gerekçe: Okunur başlık için merdiveni karartmak yanıltır.
Bedel: Fotoğraf üstü yazı kullanımı daralır.
İyi örnek: Önemli giriş ayrıntısı değişmeden kalır.
Kötü örnek: Koyu geçiş erişim engelini görünmez yapar.

### İlke V55.4 — Hareketli geçiş varsayılan değildir.

Karar: Sürekli renk akışı karar bileşenlerinde kullanılmaz.
Gerekçe: Hareket dikkati metinden ayırır ve maliyet üretir.
Bedel: AI veya Premium gösterisi daha sade kalır.
İyi örnek: Bekleme açık durum metniyle anlatılır.
Kötü örnek: AI kartı hiç durmayan gökkuşağı taşır.

### İlke V55.5 — Tema ayrı eşleşme gerektirir.

Karar: İzinli geçiş bütün örnek zeminlerde değerlendirilir.
Gerekçe: Açık temada çalışan ton koyu temada yetmeyebilir.
Bedel: Her varyant bakım ve kontrol yükü taşır.
İyi örnek: Aynı metin koyu temada da okunur.
Kötü örnek: Gradient yalnız ters renk filtresi alır.

### Görsel durum matrisi:

| Durum | Görünüm | Sınır |
| --- | --- | --- |
| Normal karar kartı | Düz ana yüzey | Gradient gerekmez |
| Kritik bilgi | Opak metin yüzeyi | Ton geçişi altında değil |
| Fotoğraf | Gerçek görünüm korunur | Koşul örtülmez |
| Dekoratif anlatı | Varsa ölçülü geçiş | Yeni bilgi taşımaz |
| Odak | Ayrı açık sınır | Gradient odak değil |
| Başarı | Semantik metin | Yeşile akış yeterli değil |
| Koyu tema | Doğrulanmış eşleşme | Rastgele ters çevirme yok |
| Hareket azaltma | Statik ifade | Sürekli akış yok |

### Kullanım kararı tablosu:

| Alan | Karar | Gerekçe |
| --- | --- | --- |
| Yer kartı | Düz yüzey başlangıcı | Ortak karşılaştırma |
| Rota özeti | Düz yüzey başlangıcı | Kapsam okunması |
| AI açıklaması | Parıltı yok | Sahte otoriteyi önleme |
| Ana CTA | Mevcut eylem çifti | Kontrast kararlılığı |
| Uyarı | Düz yüzeyde semantik rol | Anlam açıklığı |
| Harita kontrolü | Opak yüzey | Değişken zeminden ayrım |
| Fotoğraf caption | Okunabilir bağımsız metin | Kadrajdan bağımsızlık |
| Premium ayrımı | Kalite gradienti yok | Doğruluk satmama |

### İyi ve kötü karşılaştırması:

| Tasarım dürtüsü | İyi karşılık | Kötü karşılık |
| --- | --- | --- |
| Derinlik | Yüzey ve boşluk | Çok renkli sis |
| Premium his | Titiz hizalama | Altın geçişli her kart |
| AI görünürlüğü | Açık görev adı | Gökkuşağı kontur |
| Harita katmanı | Opak kontrol | Saydam ton bulutu |
| Fotoğraf metni | Bağımsız okunur alan | Ağır siyah örtü |
| Durum ayrımı | Etiket ve ikon | Rengin yavaş değişimi |
| Gece hissi | Koyu tema rolleri | Neon duman |
| Marka imzası | Tutarlı accent | Her yerde farklı geçiş |

Gradient zorunluluğu tasarım dilinin hedefi değildir.
Bir efektin yokluğu düşük üretim kalitesi sayılmaz.
Metin kontrastı geçişin en zayıf noktasında değerlendirilir.
Ortalama renk kontrastı yeterli kabul edilmez.
Kritik kontrol sınırı arka planın tonuna bağımlı değildir.
Düşük güçlü cihaz için bilgi hiyerarşisi değişmez.
Efekt kaldırıldığında aynı işlev ve anlam kalmalıdır.
Gradient marka ile durum renklerini birbirine karıştırmaz.
Başarı yeşilinden hata kırmızısına geçiş ölçek oluşturmaz.
Kategori türleri renk geçişi şiddetiyle derecelendirilmez.
Fotoğraf hakkı ve gerçeklik sınırı efektle değişmez.
Blur ile gradient katmanları birikmez.
Cam yüzey içindeki geçiş kontrolü görünmez kılamaz.
Koyu zeminde parlak çekirdek göz yorucu baskı yaratmamalıdır.
Yeni renk çifti yalnız süs isteğiyle eklenmez.
Mevcut DS tonları bu bölümde yeniden tanımlanmaz.
Neden-sonuç: Düz yüzey karar metninin okunmasını kararlı tutar.
Bedel değerlendirmesi: Gösterişli kampanya estetiği sınırlanır.
Kabul: Efekt kapatıldığında hiçbir karar bilgisi kaybolmaz.

- **Öz eleştiri Ö55.1 — Gradienti sınırlamak görsel kimliği fazla sakinleştirebilir; tanınma başka araçlarla sınanmalıdır.**

- **Öz eleştiri Ö55.2 — Tam düz yüzeyler katman ilişkisini zayıflatabilir; boşluk ve sınır yeterliliği incelenmelidir.**

- **Öz eleştiri Ö55.3 — İzinli az kullanım zamanla yayılabilir; gerekçe ve zemin kontrolleri korunmalıdır.**

## Renk Psikolojisi

Bölüm kimliği: V56.
Kapsam: Kabul edilmiş paletin algısal kullanım mantığı.
Referans: 10 §14–16; 00 §5–9.
Renk çağrışımı kültür ve bağlama göre değişebilir.
Bu bölüm evrensel psikolojik etki veya ölçülmüş sonuç iddia etmez.

### İlke V56.1 — Renk anlamı destekler.

Karar: Yeşil eylem, başarı ve seçim farklı rollerle kullanılır.
Gerekçe: Aynı ton tek başına aynı durumu anlatamaz.
Bedel: Metin ve biçim desteği gerekir.
İyi örnek: Kaydedildi somut işlem adıyla yeşil görünür.
Kötü örnek: Yeşil yer kartı güvenli yer demektir.

### İlke V56.2 — Sakinlik düşük kontrast değildir.

Karar: Mineral yüzeyler koyu okunur metinle eşleşir.
Gerekçe: Premium his silik metinle kurulamaz.
Bedel: Çok hafif editoryal görünüm sınırlanır.
İyi örnek: Caption rahat okunur karşıtlıktadır.
Kötü örnek: Zarafet için açık gri kritik koşul.

### İlke V56.3 — İnsanlar renklerle yargılanmaz.

Karar: Bütçe, ziyaret sayısı ve tercih ahlaki renk almaz.
Gerekçe: Ürün kişiyi tüketim veya zevkiyle derecelendirmez.
Bedel: Motivasyon adına kırmızı eksiklik kullanılamaz.
İyi örnek: Az kayıt nötr sayı olarak görünür.
Kötü örnek: Düşük bütçe kırmızı sorun etiketi taşır.

### İlke V56.4 — Yerler marka tonuyla homojenleştirilmez.

Karar: Gerçek fotoğraf kendi renk karakterini korur.
Gerekçe: Doğa yeşili bütün mekânların ortamını temsil etmez.
Bedel: Medyalar arasında görsel çeşitlilik kalır.
İyi örnek: Müze ve sahil gerçek tonlarıyla görünür.
Kötü örnek: Bütün fotoğraflara aynı yeşil filtre uygulanır.

### İlke V56.5 — Aciliyet yalnız gerçek duruma bağlıdır.

Karar: Kırmızı ve uyarı tonları tanımlı anlamda kullanılır.
Gerekçe: Sürekli alarm gerçek kritik bilgiyi görünmezleştirir.
Bedel: Dikkat çekmek için alarm renkleri kullanılamaz.
İyi örnek: İlgili işlem hatası açık kırmızı etiketlidir.
Kötü örnek: Normal öneri kaçırma korkusuyla kırmızıdır.

### Algı ve durum matrisi:

| Durum | Görsel yorum | Önlenen yanlış çıkarım |
| --- | --- | --- |
| Yeşil eylem | Kullanılabilir ana fiil | Tek doğru seçim |
| Yeşil başarı | Gerçek işlem sonucu | Yer güvenliği |
| Seçim zemini | Kullanıcının tercihi | Kanıt onayı |
| Kırmızı hata | Belirli sorun | Kötü kullanıcı |
| Uyarı tonu | Dikkat isteyen koşul | Genel uygunsuz yer |
| Bilgi mavisi | Nötr açıklama | Daha akıllı AI |
| Koyu yüzey | Tema tercihi | Premium ayrıcalığı |
| Nötr metadata | Destekleyici bilgi | Önemsiz gerçek |

### Palet anlam tablosu:

| Rol | Açık / koyu | Kullanım nedeni |
| --- | --- | --- |
| Sayfa | #F6F7F4 / #111916 | Sakin okuma zemini |
| Ana yüzey | #FFFFFF / #1B2620 | İçerik ayrımı |
| Ana metin | #202B28 / #F0F5EF | Güçlü okunabilirlik |
| Eylem | #185A48 / #8DD9B5 | Ölçülü vurgu |
| Seçim | #E0EFE7 / #233E30 | Kullanıcı durumu |
| Hata | #A52E34 / #FFADB0 | Açık problem |
| Uyarı | #805400 / #EDC879 | İlgili koşul |
| Bilgi | #245B83 / #9ACFF2 | Nötr bağlam |

### İyi ve kötü örnekler:

| Çağrışım | İyi kullanım | Kötü kullanım |
| --- | --- | --- |
| Doğa | Ölçülü marka yeşili | Sağlıklı yer garantisi |
| Güven | Açık gerekçe ve sınır | Yeşil mühür |
| Premium | Titiz okunabilirlik | Altın fiyat hiyerarşisi |
| Sakinlik | Boşluk ve düzen | Soluk metin |
| Uyarı | Gerçek etki | Satış baskısı |
| Keşif | Gerçek yer çeşitliliği | Turuncu viral rozet |
| AI | Açıklanabilir yardım | Mor üstünlük |
| Başarı | Tamamlanan eylem | Çok gezi yapma ödülü |

Renkler tek başına güven inşa eden sihirli araç değildir.
Güven anlatının doğruluğu ve sınır açıklığıyla birikir.
Kullanıcı koyu temayı seçtiğinde hakları değişmez.
Renk paleti tüketicinin sosyal sınıfını ima etmez.
Ücretsiz yerler soluk veya ucuz görünümlü sunulmaz.
Pahalı yerler otomatik geniş renk alanı kazanmaz.
Gri ölçekte bilgi sırası aynı kalmalıdır.
Renk görme farklılığında kritik anlam metinle sürer.
Tema eşleşmelerinin kontrastı kaynak DS sınırını izler.
Psikolojik çağrışım kontrast doğrulamasının yerine geçmez.
Harita su ve yeşil alan tonları marka onayı değildir.
Kültürel işaretler tek ülke varsayımıyla genellenmez.
Uyarı tonu kullanıcının seçimini suçlayıcı olamaz.
Ret ve vazgeçme nötr kullanıcı kararlarıdır.
Zorunlu koşul kırmızı görünmeden de önemli olabilir.
Önemin tek ölçüsü renk doygunluğu değildir.
Neden-sonuç: Anlamsal disiplin yanlış olumlu güveni sınırlar.
Bedel değerlendirmesi: Renkle hızlı duygusal ikna azaltılır.
Kabul: Renkler bilgi ve eylemi destekler, kalite hükmü üretmez.

- **Öz eleştiri Ö56.1 — Yeşilin güven çağrışımı yine oluşabilir; kullanıcı yorumlarıyla sınanmalıdır.**

- **Öz eleştiri Ö56.2 — Sınırlı palet yer çeşitliliğini zayıf hissettirebilir; gerçek medya katkısı incelenmelidir.**

- **Öz eleştiri Ö56.3 — Renk dışı açıklamalar bilgi yükünü artırabilir; anlam kaybetmeden kısa tutulmalıdır.**

## Accent Renkleri

Bölüm kimliği: V57.
Kapsam: Mevcut anlamsal vurguların kullanım disiplini.
Referans: 10 §14–16; §31.
Accent yeni renk seçmek veya paleti değiştirmek değildir.
Mevcut tonlar görev rolleriyle birlikte korunur.

### İlke V57.1 — Ana vurgu görev önceliğine bağlıdır.

Karar: Birincil eylem mevcut eylem rengiyle görünür.
Gerekçe: Her kontrol aynı baskınlıkta olursa öncelik kaybolur.
Bedel: İkincil eylemler daha sakin görünür.
İyi örnek: Mevcut ana fiil açık bir vurgu taşır.
Kötü örnek: Bütün bağlantılar dolu yeşil buton olur.

### İlke V57.2 — Aynı ton farklı anlamları birleştirmez.

Karar: Eylem ve başarı aynı değeri ayrı rollerle kullanır.
Gerekçe: Yeşil buton tamamlanmış işlem değildir.
Bedel: Etiket ve durum ayrımı ayrıca görünür olmalıdır.
İyi örnek: Kaydet eylemi ile kaydedildi sonucu ayrılır.
Kötü örnek: Yeşil görünen bütün kartlar onaylanmıştır.

### İlke V57.3 — Odak bağımsız görünür.

Karar: Odak rengi seçim ve CTA renginden ayrıdır.
Gerekçe: Klavye hedefi ile kullanıcı seçimi aynı değildir.
Bedel: Aynı bileşende iki vurgu birlikte bulunabilir.
İyi örnek: Seçili öğenin odağı ayrıca anlaşılır.
Kötü örnek: Odaklanmak seçilmiş gibi yeşile boyar.

### İlke V57.4 — Accent dozajı yüzeyleri yarıştıramaz.

Karar: Renk alanı bilgi hiyerarşisini destekleyecek kadar kullanılır.
Gerekçe: Geniş renk blokları gerekçe metnini bastırabilir.
Bedel: Marka rengi ekranın çoğunu kaplamaz.
İyi örnek: Eylem, seçim ve durum gerektiği yerde ayrılır.
Kötü örnek: Her kartın çevresi parlak marka çerçevesidir.

### İlke V57.5 — Tema rengi eşleşmesi birlikte korunur.

Karar: Eylem zemini yalnız eşleşmiş metin rengini kullanır.
Gerekçe: Aynı beyaz metni tüm temalara taşımak kontrastı bozar.
Bedel: Renk kararları tek başına kopyalanamaz.
İyi örnek: Koyu tema eylem metni kendi eşidir.
Kötü örnek: Açık yeşil üzerine beyaz etiket kullanılır.

### Vurgu durum matrisi:

| Durum | Görsel rol | Anlam |
| --- | --- | --- |
| Ana eylem | Birincil eylem çifti | Mevcut fiil |
| İkincil eylem | Sakin okunabilir kontrol | Geçerli alternatif |
| Seçili | Seçim zemini ve işaret | Kullanıcı tercihi |
| Odaklı | Odak vurgusu | Giriş hedefi |
| Başarılı | Başarı metni | Gerçek sonuç |
| Hatalı | Hata rolü ve açıklama | Belirli sorun |
| Bekleyen | Nötr durum | Sonuç yok |
| Devre dışı | Açıklanmış durum | Gizli yetki yok |

### Kabul edilmiş eşleşmeler:

| Rol | Açık tema | Koyu tema |
| --- | --- | --- |
| Eylem zemini | #185A48 | #8DD9B5 |
| Eylem metni | #FFFFFF | #102B20 |
| Seçim zemini | #E0EFE7 | #233E30 |
| Odak | #164FAD | #A9CAFF |
| Ana metin | #202B28 | #F0F5EF |
| İkincil metin | #4C5B54 | #C0CEC2 |
| Güçlü sınır | #718078 | #829688 |
| Hafif ayırıcı | #D3DAD4 | #405247 |

### İyi ve kötü karşılaştırması:

| Konu | İyi | Kötü |
| --- | --- | --- |
| CTA | Yetkili ana fiil | Rastgele vurgu |
| Seçim | Kullanıcı durumu | Kalite onayı |
| Odak | Bağımsız sınır | Seçimin kopyası |
| AI | Ortak renk rolleri | Yeni mor otorite |
| Premium | Aynı okunabilirlik | Altın üstünlük |
| Fotoğraf | Gerçek renkler | Markaya boyama |
| Harita | Kontrollü eylem | Tüm çevre yeşil |
| Ret | Nötr meşru seçim | Kırmızı suçlama |

Accent renkleri toplam yer sırasını yeniden düzenlemez.
İlk kart daha yoğun renkle en iyi ilan edilmez.
Sadece seçili olan kartta kullanıcı durumu vurgulanır.
Eylem rengi ticari ilişkinin sonucu değildir.
Bütçe sınırı otomatik uyarı rengi taşımaz.
Gerçek uyuşmazlık kendi bağlamıyla açıklanır.
Renk şiddeti kanıt yeterliliğinin görsel puanı değildir.
Yeni kategori için otomatik yeni accent açılmaz.
Harita sağlayıcısının tonları eylem rolünü belirlemez.
Hafif ayırıcı tek kontrol sınırı olarak kullanılmaz.
Hover durumunda metin alfa azaltımıyla silikleştirilmez.
Basılı kontrol kontrastını korur.
Uzun etiket birincil vurgudan taşmamalıdır.
Yüksek kontrastta sistem renklerinin işlevi korunur.
Renkler marka karosunun özgün varlığını yeniden çizmez.
Accent sözlüğü logo renklerini değiştirme yetkisi vermez.
Neden-sonuç: Sınırlı vurgu gözün görev sırasını bulmasını kolaylaştırır.
Bedel değerlendirmesi: Daha az renkli görünüm ilk anda sakin gelebilir.
Kabul: Ana eylem, odak ve seçim farklı anlamları korur.

- **Öz eleştiri Ö57.1 — Eylem ve başarı aynı yeşili paylaştığında anlam karışabilir; etiket ayrımı sınanmalıdır.**

- **Öz eleştiri Ö57.2 — Az accent bazı bağlantıları zor buldurabilir; etkileşim tanınması incelenmelidir.**

- **Öz eleştiri Ö57.3 — Odak ve seçim birlikteliği fazla vurgu yaratabilir; öncelik kontrol edilmelidir.**

## Success

Bölüm kimliği: V58.
Kapsam: Gerçekten tamamlanmış mevcut işlemin görsel teyidi.
Referans: 10 B30; 11 §41, §46.
Başarı yerin kalitesi veya kullanıcının yaşam performansı değildir.
Başarı görünümü yalnız teyit edilen işlem kapsamını taşır.

### İlke V58.1 — Sonuç eylemin gerçeğini söyler.

Karar: Tamamlanmış işlem açık adıyla belirtilir.
Gerekçe: Kaydetmek ziyaret etmek veya rezervasyon yapmak değildir.
Bedel: Her durum tek tamamlandı sözüyle karşılanamaz.
İyi örnek: Yer Gezeceğim'e kaydedildi.
Kötü örnek: Kayıt sonrası ziyaret onaylandı.

### İlke V58.2 — Bekleme başarı gibi renklendirilmez.

Karar: Teyitsiz sonuç nötr bekleme veya belirsizlik taşır.
Gerekçe: Görsel onay kullanıcının sonraki kararını etkiler.
Bedel: Hızlı başarı hissi gecikebilir.
İyi örnek: Uzak kayıt teyidi gelince sonuç açıklanır.
Kötü örnek: Dokunma anında yeşil onay verilir.

### İlke V58.3 — Yeşil sonuç metinle tamamlanır.

Karar: Başarı rengi ve ikon işlem açıklamasını destekler.
Gerekçe: Renk kaybolduğunda sonuç anlaşılır kalmalıdır.
Bedel: Simge tek başına yeterli değildir.
İyi örnek: Onay simgesi yanında somut kayıt sonucu.
Kötü örnek: Açıklamasız yeşil halka.

### İlke V58.4 — Kutlama ölçülüdür.

Karar: Rutin işlem teyidi sakin ve kısa görünür.
Gerekçe: Tekrar eden konfeti dikkat ve tamamlama baskısı yaratır.
Bedel: Ödül hissi ürünün ana çekiciliği olmaz.
İyi örnek: Kopyalandı sonucu açıkça okunur.
Kötü örnek: Her kayıtta kupalar ve yıldız yağmuru.

### İlke V58.5 — İşlem sonucu bilgi sınırını silmez.

Karar: Kaydedilen taslağın belirsizliği görünür kalır.
Gerekçe: Başarılı saklama yapılabilir rotayı kanıtlamaz.
Bedel: Aynı kartta başarı ve uyarı birlikte bulunabilir.
İyi örnek: Taslak kaydedildi; geçiş bilgisi hâlâ eksik.
Kötü örnek: Kayıt başarısı bütün uyarıları yeşile çevirir.

### Başarı durum matrisi:

| İşlem | Görsel teyit | Anlam sınırı |
| --- | --- | --- |
| Gezeceğim kaydı | Niyet kaydedildi | Ziyaret değil |
| Gezdiğim beyanı | Beyan kaydedildi | Memnuniyet değil |
| Rota kaydı | Taslak saklandı | Yapılabilirlik değil |
| Bir İz gönderimi | Gözlem alındı | Yayımlandı değil |
| Metin kopyalama | Kopyalandı | Gönderildi değil |
| Paylaşım hazırlama | Hazırlandı | Dışarı yayımlandı değil |
| Düzenleme | Seçim kaydedildi | Yeni kanıt değil |
| Yerel kayıt | Cihazda saklandı | Hesapta eşitlendi değil |

### Başarı görsel rolleri:

| Parça | Karar | Gerekçe |
| --- | --- | --- |
| Renk açık | #185A48 | Mevcut başarı rolü |
| Renk koyu | #8DD9B5 | Tema eşdeğerliği |
| Metin | Somut sonuç cümlesi | Kapsam açıklığı |
| İkon | Tanımlı onay desteği | Hızlı tanıma |
| Yüzey | Aktif göreve bağlı | Bağlamı koruma |
| Hareket | Ölçülü durum geçişi | Dikkati tüketmeme |
| Kritik sınır | Gövde okunurluğu | Başarıyla silinmeme |
| Tekrar | Aynı işlem kimliği | Çift sonuç yanılmasını önleme |

### İyi ve kötü örnekler:

| Konu | İyi | Kötü |
| --- | --- | --- |
| Dil | Kaydedildi | Harika seçim yaptın |
| Renk | Gerçek sonuca bağlı | Her olumlu iddia yeşil |
| Ölçek | Kısa teyit | Tam ekran ödül |
| Bir İz | Alındı | Gerçekliği onaylandı |
| Rota | Taslak saklandı | Kusursuz gün hazır |
| Paylaşım | Link hazır | Arkadaşlarına gönderildi |
| Premium | Eşit teyit kalitesi | Ücretli özel kutlama |
| Kayıt sınırı | Cihaz kapsamı açık | Her yerde kalıcı vaadi |

Başarı başlığı kullanıcıyı daha çok geziye zorlamaz.
Aynı eylemin tekrar basılması yeni ödül üretmez.
Teyit mevcut toast veya snackbar sözleşmesini izler.
Bu bölüm yeni bildirim kanalı yaratmaz.
Kayıt hedefi bağlama göre açık adlandırılır.
Sunucu sonucu bilinmiyorsa sessiz onay yoktur.
Hata sonrası tekrarın başarısı eski girişleri korur.
Kısmi başarı tam işlem olmuş gibi gösterilmez.
Kapatılmış paylaşım tekrar canlandı gibi anlatılmaz.
Geri alma kullanıcının işleminin kapsamıyla sınırlıdır.
Yeni kapanma bilgisi başarı görünümüyle geri alınamaz.
Kullanıcı işlemi bitirip uygulamadan ayrılabilir.
Başarı görünümü sonraki ticari teklife dönüşmez.
Renk yalnız izinli yüzey eşleşmelerinde kullanılır.
Yüksek kontrastta onay metni görünür kalır.
Haptik yokken teyit anlaşılır olmalıdır.
Neden-sonuç: Kesin işlem dili gereğinden fazla onay çıkarımını azaltır.
Bedel değerlendirmesi: Coşkulu pazarlama dili daha az kullanılır.
Kabul: Başarı yalnız gerçekten tamamlanan işlemi açıklar.

- **Öz eleştiri Ö58.1 — Çok sakin teyit fark edilmeyebilir; tekrar işlem davranışı incelenmelidir.**

- **Öz eleştiri Ö58.2 — Başarı ve uyarının birlikteliği çelişki sanılabilir; kapsam ayrımı sınanmalıdır.**

- **Öz eleştiri Ö58.3 — Somut sonuç etiketleri uzun olabilir; dar alanda kesilmeden okunmalıdır.**

## Error

Bölüm kimliği: V59.
Kapsam: Mevcut işlem ve hizmet sorunlarının görsel dili.
Referans: 10 B28/B29; 11 E24/E26 ve §41.
Hata, bilgi eksikliği ve bilinen yer engeli aynı değildir.
Bu bölüm yeni kurtarma akışı veya doğrulama adımı üretmez.

### İlke V59.1 — Sorun etkilenen işe bağlanır.

Karar: Hata mesajı hangi bilginin veya işlemin etkilendiğini söyler.
Gerekçe: Genel arıza görünümü sağlam içeriği değersizleştirir.
Bedel: Tek genel hata şablonu bütün durumları karşılamaz.
İyi örnek: Harita yüklenemedi, mevcut liste okunur.
Kötü örnek: Harita hatasında bütün keşif kırmızılaşır.

### İlke V59.2 — Kırmızı bilgi boşluğu anlamına gelmez.

Karar: Bilinmeyen koşul nötr belirsizlik sözleşmesini izler.
Gerekçe: Bilgi yokluğu bozuk sistem veya kötü yer değildir.
Bedel: Durum sınıfları dikkatle ayrılmalıdır.
İyi örnek: Akşam ses bilgisi bilinmiyor.
Kötü örnek: Ses verisi olmayan yer hata kartıdır.

### İlke V59.3 — Kullanıcının emeği görünür kalır.

Karar: Mevcut sorgu, taslak ve seçim hata yanında korunur.
Gerekçe: Hata görseli yapılan işi kapatmamalıdır.
Bedel: Tam ekran dramatik hata kullanımı sınırlanır.
İyi örnek: Kaydetme sorununun yanında taslak okunur.
Kötü örnek: Kayıt hatası bütün rota içeriğini siler.

### İlke V59.4 — Belirsiz sonuç başarısız diye kesinleşmez.

Karar: İşlemin durumu bilinmiyorsa bu açıkça gösterilir.
Gerekçe: Yanlış tekrar çift kayıt veya dış işlem doğurabilir.
Bedel: Kullanıcıya daha nüanslı sonuç açıklaması gerekir.
İyi örnek: Kayıt sonucunu doğrulayamadık.
Kötü örnek: Teyit kaybolunca kesinlikle kaydedilmedi.

### İlke V59.5 — Hata dili suçlamaz.

Karar: Somut sorun ve mevcut devam yolu nötr anlatılır.
Gerekçe: Kırmızı vurgu kişiye hata yaptığı hükmü vermez.
Bedel: Dikkat çekici mizah ve sert dil kullanılmaz.
İyi örnek: Bu alanın tarihini doğrulayamıyoruz.
Kötü örnek: Yanlış seçim yaptın, baştan başla.

### Hata durum matrisi:

| Durum | Görünüm | Anlam |
| --- | --- | --- |
| Alan doğrulaması | Alana bağlı açıklama | Belirli düzeltme |
| Hizmet kesintisi | Göreve bağlı sorun | Veri yokluğu değil |
| Kayıt başarısız | Taslak yanında hata | Çalışma korunur |
| Sonuç belirsiz | Açık belirsizlik | Tekrar otomatik değil |
| Harita arızası | Yerel harita durumu | Liste sürdürülebilir |
| Kimlik bulunamadı | Mevcut E24 anlamı | Başka yere atlama yok |
| Offline | Ayrı bağlantı kapsamı | Her bilgi hatalı değil |
| Kritik iddia geri çekildi | İlgili sınır | Eski güvence kaldırılır |

### Hata görsel rolleri:

| Parça | Karar | Gerekçe |
| --- | --- | --- |
| Açık tema tonu | #A52E34 | Mevcut hata rolü |
| Koyu tema tonu | #FFADB0 | Tema eşdeğerliği |
| Başlık | Kısa somut sorun | İlk anlayış |
| Açıklama | 16/24 gövde | Düzeltme okunabilirliği |
| Alan sınırı | Metne destek | Yalnız renk olmama |
| İkon | Anlamı destekleyen simge | Hızlı tanıma |
| Eylem | Mevcut kurtarma yolu | Yeni akış üretmeme |
| Yüzey | İlgili görev | Bütün ekranı cezalandırmama |

### İyi ve kötü örnekler:

| Konu | İyi | Kötü |
| --- | --- | --- |
| Mesaj | Geçiş süresi alınamadı | Bir şeyler ters gitti |
| Bağlam | Aynı sorgu korunur | Boş arama alanı |
| Tekrar | Yetkili mevcut yol | Sonuç bilinmeden tekrar |
| Görsel | Sakin belirgin sorun | Büyük korkutucu illüstrasyon |
| Bilinmeyen | Nötr bilgi sınırı | Kırmızı kötü yer |
| Ücret | Somut mevcut durum | Premium alarak düzelt |
| Konum izni | Ayrı tercih | Kırmızı hata |
| Ret | Nötr kullanıcı seçimi | Sistem arızası gibi |

Hata simgesi sonucun anlamını tek başına taşımaz.
Yardımcı teknolojiyle açıklama etkilenen alana bağlanır.
Odak göstergesi hata sınırından ayrı görünür.
Bir alan kırmızı diye bütün metin kırmızı yapılmaz.
Uzun hata cümlesi küçük caption boyutuna düşürülmez.
Hata cümlesi kullanıcının özel sorgusunu gereksiz tekrar etmez.
Teknik kimlik ve altyapı terimi tüketici metnini kaplamaz.
Yeni bağlantı geldi diye hata sessizce başarı sayılmaz.
Önceki içerik tarihliyse bu sınır korunur.
Harita yokken hayalî konum resmi gösterilmez.
Fotoğraf hatası yer kimliği hatası değildir.
AI hatası bilinen somut bilgiyi silmez.
Rota zaman çelişkisi mutlaka sistem arızası değildir.
Kullanıcı çelişkili taslağı saklayabilir.
Kırmızı kart tüm yerin güvensiz olduğu anlamına gelmez.
Hata azaltma adına kritik bilgi saklanamaz.
Neden-sonuç: Yerel ve somut hata dili toparlanma yükünü azaltır.
Bedel değerlendirmesi: Durum ayrımları daha fazla içerik disiplini ister.
Kabul: Kullanıcı neyin olmadığını ve neyin korunduğunu anlar.

- **Öz eleştiri Ö59.1 — Yerel hata küçük kalıp görülmeyebilir; fark edilme ve devam başarısı incelenmelidir.**

- **Öz eleştiri Ö59.2 — Sonuç belirsizliği kullanıcıyı bekletebilir; kesin olmayan dili anlama sınanmalıdır.**

- **Öz eleştiri Ö59.3 — Çok nötr hata dili ciddiyeti azaltabilir; kritik etki açıklığı korunmalıdır.**

## Warning

Bölüm kimliği: V60.
Kapsam: Mevcut kararı etkileyen koşul ve dikkat bilgisi.
Referans: 02 §6; 10 §15; 11 E04/E07.
Uyarı yerin genel kötülük veya güvensizlik rozeti değildir.
Bilinmeyen zorunlu koşul uyarıyla olumlu eşleşmeye dönüşmez.

### İlke V60.1 — Uyarı somut koşulu açıklar.

Karar: Etki ve geçerlilik kapsamı aynı okumada yer alır.
Gerekçe: Dikkat simgesi tek başına neyi değiştireceğini söylemez.
Bedel: Bazı uyarılar tek satırı aşabilir.
İyi örnek: Son giriş saati bu sırayı etkiliyor.
Kötü örnek: Açıklamasız sarı ünlem.

### İlke V60.2 — Ödün ile engel karıştırılmaz.

Karar: Görsel hiyerarşi mevcut karar sonucunu doğru taşır.
Gerekçe: Zorunlu erişim ihlali küçük dezavantaj değildir.
Bedel: Bütün olumsuz koşullar aynı hafif not olmaz.
İyi örnek: Merdiven zorunlu erişimle ilişkili açıklanır.
Kötü örnek: Zorunlu engel ufak sarı tavsiye gibi görünür.

### İlke V60.3 — Kritik uyarı olumlu anlatıma eşlik eder.

Karar: Kararı bozan koşul gerekçenin yakınında görünür.
Gerekçe: Kullanıcı olumlu başlıktan sonra yanıltılmamalıdır.
Bedel: Kart daha az pürüzsüz ve kısa görünebilir.
İyi örnek: Sohbet avantajının yanında süre sınırı vardır.
Kötü örnek: Koşul yalnız yöntem sayfasında bulunur.

### İlke V60.4 — Uyarı rengi sınırlı kullanılır.

Karar: Uyarı tonu yalnız dikkat gerektiren koşulu vurgular.
Gerekçe: Her metadata sarı olursa önem sırası çöker.
Bedel: Bazı eksikler nötr metin olarak kalır.
İyi örnek: Kararı etkileyen yeni koşul ayırt edilir.
Kötü örnek: Tarih, fiyat ve tür hep sarı rozetlidir.

### İlke V60.5 — Uyarıyı kapatmak koşulu kaldırmaz.

Karar: Görsel kapanma mevcut karar bilgisini değiştirmez.
Gerekçe: Bildirimi gizlemek zorunlu sınırdan vazgeçmek değildir.
Bedel: İlgili temel açıklama içerikte kalabilir.
İyi örnek: Geçici bildirim kapanır, engel Yer'de kalır.
Kötü örnek: Uyarı kapanınca rota yeşil onay alır.

### Uyarı durum matrisi:

| Durum | Görünüm | Sınır |
| --- | --- | --- |
| Bilinen kullanım koşulu | Yakın açık metin | Bilinmeyen değil |
| Önemli ödün | Gerekçeyle aynı öncelik | Genel kötü yer değil |
| Zorunlu engel | Erken belirgin açıklama | Telafi edilmiş sayılmaz |
| Kritik bilinmeyen | Somut eksiklik | Koşullu uygunluk diye aklanmaz |
| Zaman değişikliği | Tarih kapsamıyla | Genel sürekli alarm değil |
| Eski bilgi | Geçerlilik sınırı | Bugünkü onay değil |
| Çelişki | Açık kapsamlı belirsizlik | Ortalama alınmaz |
| Kapatılmış bildirim | Temel koşul korunur | Kullanıcı vazgeçmiş sayılmaz |

### Uyarı görsel rolleri:

| Parça | Karar | Gerekçe |
| --- | --- | --- |
| Açık tema tonu | #805400 | Okunur uyarı rolü |
| Koyu tema tonu | #EDC879 | Gece eşdeğerliği |
| Metin | Koşul ve etkisi | Anlam açıklığı |
| Başlık | Gerektiğinde kısa | Tarama yardımı |
| İkon | Metne destek | Tek taşıyıcı değil |
| Yüzey | Mevcut ana/üst yüzey | Yeni sarı dolgu gerekmez |
| Yerleşim ilişkisi | Ait olduğu iddiaya yakın | Bilgiyi bağlama |
| Eylem | Mevcut devam yolu | Yeni onay akışı yok |

### İyi ve kötü örnekler:

| Konu | İyi | Kötü |
| --- | --- | --- |
| Kalabalık | İlgili saat örüntüsü | Genel tehlike |
| Erişim | Belirli yolun sınırı | Her durumda sarı geçiş |
| Fiyat | Güncellik kapsamı | Bütçeyi yükselt baskısı |
| Rezervasyon | Gerçek kullanım koşulu | Yer ayrıldı iması |
| Son giriş | Varışa etkisi | Küçük dekoratif saat |
| AI | Bilinen sınır | Model güven yüzdesi |
| Premium | Aynı kritik bilgi | Ücretli uyarı görünürlüğü |
| Kullanıcı ret | Nötr tercih | Yanlış karar alarmı |

Uyarı dili kullanıcıyı korkutarak eyleme zorlamaz.
Sarı renk meşru alternatifleri değersizleştirmez.
Bir yerdeki engel bütün ilçenin niteliğine yayılmaz.
Uyarı işareti haritada okunur metin karşılığı taşır.
Paylaşım özeti kritik koşulu küçük yazıya saklamaz.
Sabit görselde güncel koşul garantisi verilmez.
Fotoğraf captionı kritik engelin tek yeri değildir.
Ana gövde okunurluğu büyük metinde korunur.
Renkli çerçeve metin hiyerarşisinin yerine geçmez.
Yeni bilgi aynı uyarıyı gereksiz tekrar ettirmez.
Uyarı sayısı kullanıcıya risk puanı olarak sunulmaz.
Daha fazla uyarı daha kötü yer demek değildir.
Az uyarı eksiksiz doğrulama anlamına gelmez.
Uyarının geçerlilik süresi gerçek bilgiye bağlıdır.
Geçici katman kapanınca odak mantığı korunur.
Mevcut akış dışında yeni onay penceresi oluşturulmaz.
Neden-sonuç: Koşula bağlı vurgu kullanıcıya gerçek ödünü gösterir.
Bedel değerlendirmesi: Pürüzsüz olumlu anlatım daha sık bölünür.
Kabul: Uyarı eksik zorunlu koşulu hiçbir zaman uygunlaştırmaz.

- **Öz eleştiri Ö60.1 — Sık uyarı dikkat yorgunluğu yaratabilir; yalnız karar etkisi olanlar vurgulanmalıdır.**

- **Öz eleştiri Ö60.2 — Sarı ton ciddiyeti hafifletebilir; engelin metinsel anlamı sınanmalıdır.**

- **Öz eleştiri Ö60.3 — Uyarı kapandıktan sonra koşul unutulabilir; ilgili iddia bağının yeterliliği incelenmelidir.**

## Info

Bölüm kimliği: V61.
Kapsam: Mevcut görevdeki nötr açıklama ve kapsam bilgisi.
Referans: 10 §14–15; 02 §8; 11 §41.
Bilgilendirme yeni ipucu sistemi veya bildirim kanalı açmaz.
Nötr bilgi daha düşük okunabilirlik anlamına gelmez.

### İlke V61.1 — Bilgi açıklığı sakin görünür.

Karar: Nötr açıklama bağlamıyla anlaşılır metin taşır.
Gerekçe: Her bilgi alarm görünümü gerektirmez.
Bedel: Bazı açıklamalar daha az dikkat çekicidir.
İyi örnek: Arama yalnız cihazdaki kayıtları kapsıyor.
Kötü örnek: Nötr kapsam büyük kırmızı uyarıdır.

### İlke V61.2 — Mavi AI üstünlüğü değildir.

Karar: Bilgi rengi bütün bilgi kaynaklarında aynı anlamdadır.
Gerekçe: Üretim yöntemi doğruluk ayrıcalığı vermez.
Bedel: AI için ayrı dekoratif mavi alan açılmaz.
İyi örnek: Yöntem açıklaması nötr bilgi rolündedir.
Kötü örnek: Mavi kart daha akıllı öneri demektir.

### İlke V61.3 — Kritik sınır info kutusuna saklanmaz.

Karar: Kararı etkileyen eksiklik ilgili iddiada görünür.
Gerekçe: Genel bilgi alanı somut zorunlu koşulu devralamaz.
Bedel: Aynı kavramın bağlama bağlı vurgusu değişebilir.
İyi örnek: Erişim eksikliği gerekçenin yakınında açıklanır.
Kötü örnek: Bilinmeyen erişim küçük bilgi ikonundadır.

### İlke V61.4 — Bilgi ve eylem farklı görünür.

Karar: Açıklama satırı buton gibi davranıyor izlenimi vermez.
Gerekçe: Kullanıcı dokunulabilir alanı tahmin etmek zorunda kalmamalıdır.
Bedel: Bütün metinler renkli chip halinde gösterilemez.
İyi örnek: Gerçek bağlantı hedefi açık adlandırılır.
Kötü örnek: Dekoratif bilgi kapsülü eylem gibi kabartılır.

### İlke V61.5 — Bilgi zamanı ilgili iddiaya bağlanır.

Karar: Tarih ve kapsam genel güncellik mührü yapılmaz.
Gerekçe: Bir kaydın güncellenmesi bütün alanların kontrolü değildir.
Bedel: Kısa tek son güncelleme ifadesi her yerde yetmez.
İyi örnek: Fiyatın kontrol tarihi kendi yanında okunur.
Kötü örnek: Sayfa tarihi bütün özellikleri doğrular.

### Bilgi durum matrisi:

| Durum | Görünüm | Anlam |
| --- | --- | --- |
| Nötr açıklama | Sakin okunur gövde | Bağlam desteği |
| Yöntem erişimi | Açık hedef metni | Yeni bilgi otoritesi değil |
| Kapsam açıklaması | Mevcut görevle bağlı | Sınır görünür |
| Tarihli bilgi | İddiaya bağlı tarih | Genel mühür değil |
| Bilinmeyen ikincil alan | Nötr somut ifade | Yok demek değil |
| Kritik bilinmeyen | Ana karar önceliği | İpucuna saklanmaz |
| Offline kapsam | Cihaz/yerel açıklama | Canlı arama değil |
| Bilgi yenileniyor | Bağlamlı durum | Yeni sonuç henüz yok |

### Bilgilendirme görsel rolleri:

| Parça | Karar | Gerekçe |
| --- | --- | --- |
| Açık tema tonu | #245B83 | Mevcut bilgi rolü |
| Koyu tema tonu | #9ACFF2 | Tema eşdeğerliği |
| Ana açıklama | 16/24 gövde | Okunabilir anlam |
| İkincil ayrıntı | 14/20 uygun bağlamda | Hiyerarşi |
| Caption | 13/20 uygun metadata | Görsel kapsam |
| İkon | 16/20/24 ailesi | Tutarlı destek |
| Bağlantı | Açık hedef adı | Eylem tanınması |
| Yüzey | Ana/üst yüzey eşleşmesi | Kontrast kararlılığı |

### İyi ve kötü örnekler:

| Konu | İyi | Kötü |
| --- | --- | --- |
| Yerel arama | Kapsam açık | İnternet sonucu iması |
| Tarih | İddiaya bağlı | Genel güven damgası |
| Yöntem | Ne açıklanacağı belli | Buraya tıkla |
| Bilinmeyen | Somut sınır | Alan boş bırakıldı |
| Kritik koşul | Görünür gövde | Hover içinde saklı |
| AI | Ortak bilgi dili | Mavi premium zeka |
| İkon | Metni destekler | Açıklamasız i simgesi |
| Renk | Semantik rol | Rastgele kategori tonu |

Bilgi açıklaması gereksiz öğretici metin duvarı oluşturmaz.
Mevcut görevde zaten açık olan şey tekrar anlatılmaz.
Okumak zorunda bırakılmayan ayrıntı kritik sınırı kapsamaz.
Hover bilgisi temel anlamın tek erişim yolu değildir.
Mobilde dokunulabilirlik görsel sınırla anlaşılır kalır.
Klavye odağı gerçek bilgi bağlantısında görünürdür.
Bağlantı çevresi etkileşim hedefi sözleşmesini korur.
Tüketici metninde iç skor ve teknik ağırlık bulunmaz.
Bilgi türü kullanıcıya gerekli düzeyde açıklanır.
Doğrulanmış olgu zaman ve alan sınırını korur.
Çıkarım nötr renk altında kesin olguya dönüşmez.
Tahmin birim ve aralığıyla okunur kalır.
Eksik bilgiler için otomatik boş tablo üretilmez.
Uygulanamaz alan bilgi eksikliği gibi gösterilmez.
Premium ile ücretsiz aynı bilgi sınırlarını görür.
Nötrlik önemli gerçeği silik yapma gerekçesi değildir.
Neden-sonuç: Açık kapsam dili bilginin yanlış genellenmesini azaltır.
Bedel değerlendirmesi: Sadelik için gerekli açıklamayı seçmek bakım ister.
Kabul: Kullanıcı bilginin neyi kapsadığını ve neyi kapsamadığını anlar.

- **Öz eleştiri Ö61.1 — Nötr açıklamalar gözden kaçabilir; bağlamı anlama başarısı araştırılmalıdır.**

- **Öz eleştiri Ö61.2 — Çok tarih göstermek bilgi yükünü artırabilir; yalnız ilgili güncellik vurgulanmalıdır.**

- **Öz eleştiri Ö61.3 — Bilgi ve uyarı ayrımı belirsizleşebilir; karar etkisine göre tutarlılık sınanmalıdır.**

## Animasyon Felsefesi

Bölüm kimliği: V62.
Animasyon, kabul edilmiş durumlar arasındaki ilişkinin görsel açıklamasıdır.
Görevin sırası, sonucu veya kullanılabilirliği animasyonla yeniden tanımlanmaz.
Dayanak: 10 Design System §46–47 ve 07 UX Karar Akışları §25–28.

### Görsel amaç

Kullanıcı hangi öğenin değiştiğini anlayabilmelidir.
Hareket seyretmek görevin zorunlu parçası olmamalıdır.
Sakinlik, geri bildirimin eksiltilmesi anlamına gelmez.
Mevcut sistemin dört süre rolü aynen korunur.

| Süre rolü | Süre | Görsel kullanım | Değişmeyen sınır |
| --- | --- | --- | --- |
| Anlık | 0 ms | Statik durum güncellemesi | Kritik düzeltme bekletilmez |
| Kısa | 120 ms | Küçük seçili durum karşılığı | Yeni bekleme eklenmez |
| Geçiş | 180 ms | Aynı görevde düzen ilişkisi | Kullanıcı girdisi engellenmez |
| Katman | 240 ms | Mevcut sheet veya drawer ilişkisi | Yeni katman oluşturulmaz |
| Azaltılmış hareket | 0 ms | Doğrudan son görünüm | Metin ve odak bilgisi korunur |
| Doğrudan sürükleme | Sabit süreye bağlanmaz | Girdiyi gecikmesiz izleme | Serbest bırakma yeni akış değildir |

### İlke V62.1 — Hareket bir soruya cevap verir.

Karar: Her hareketin konum, durum veya katman ilişkisi şeklinde açıklanabilir amacı bulunur.
Gerekçe: Amaçsız hareket harita ve karar metniyle dikkat için yarışır.
Bedel: Ürün ilk bakışta daha az gösterişli algılanabilir.
Uygulama: Seçili yerin işareti netleşir; kart çevresinde dekoratif nesne dolaşmaz.
Kontrol: Hareket durdurulduğunda hangi bilginin kaybolduğu ayrıca değerlendirilir.

### İlke V62.2 — En kısa yeterli süre seçilir.

Karar: Varlığı gerekli hareket için mevcut dört rolden en küçük yeterli olanı kullanılır.
Gerekçe: Kullanıcıyı fiziksel dünya kararından koparan sunum süresi azalır.
Bedel: Çok kısa geçişte ilişki fark edilmezse statik işaretin güçlenmesi gerekir.
Uygulama: Küçük seçim karşılığı katman açılışı kadar uzun sürmez.
Kontrol: Sürelerin toplamı görevde zorunlu bekleme üretmemelidir.

### İlke V62.3 — Gerçek bilgi hareketten önce gelir.

Karar: Kritik iddia düzeltmesi 0 ms rolüyle doğrudan görünür olur.
Gerekçe: Eski olumlu hükmü zarifçe soldurmak bile yanlış anlamın sürmesine neden olabilir.
Bedel: Önemli düzeltme sıradan geçişlerden daha keskin görünebilir.
Uygulama: Uygunluk sınırı, eski olumlu durumun kapanış gösterisini beklemez.
Kontrol: Görsel düzgünlük gerekçesiyle geçersiz bilgi korunup korunmadığı incelenir.

### İlke V62.4 — Statik eşdeğer tamdır.

Karar: Azaltılmış harekette son durum, ilişkili başlık ve görünür seçim birlikte kalır.
Gerekçe: Hareketi azaltma tercihi kullanıcıdan anlam veya kontrol hakkı alamaz.
Bedel: Hareketle anlatılabilen bazı ilişkiler kısa metin gerektirir.
Uygulama: Taşınmış durak yeni numarası ve mevcut değişiklik açıklamasıyla anlaşılır.
Kontrol: Aynı görev yalnız son görünüm üzerinden yorumlanabilir olmalıdır.

### İlke V62.5 — Hareket kesilebilir.

Karar: Yeni kullanıcı girdisi, önceki görsel geçişin tamamlanmasına bağlı kalmaz.
Gerekçe: Gezi sırasında kullanıcı ekrana aralıklı bakar ve fikrini hızlı değiştirebilir.
Bedel: Ara görüntüler kusursuz sahne geçişi hissi vermeyebilir.
Uygulama: Yeni seçili durum önceki süslemenin bitmesini beklemez.
Kontrol: Hızlı ardışık seçimlerde son kullanıcı niyetinin görünürlüğü değerlendirilir.

### Neden ve sonuç karşılaştırması

| Tercih | Beklenen sonuç | Yanlış yorum riski | Görsel düzeltme |
| --- | --- | --- | --- |
| Kısa durum karşılığı | Girdinin alındığı anlaşılır | Uzak işlem bitti sanılır | Bekleme metni ayrı kalır |
| Statik sıra numarası | Yeni yer kolay bulunur | Eski sıra unutulabilir | Mevcut değişiklik özeti korunur |
| Katman ilişkisi | Bağlam sürekliliği okunur | Arka görev etkin sanılır | Etkin katman sınırı belirgindir |
| Anlık kritik değişim | Yanlış olumlu anlam durur | Hata algısı yaratabilir | Değişimin nedeni metinle açıklanır |
| Dekorun kaldırılması | Okuma alanı sakinleşir | Ürün donmuş sanılır | İşlem durumu görünür kalır |
| Kesilebilir geçiş | Kullanıcı kontrolü sürer | Ara biçim düzensizleşebilir | Son durum kararlı ve nettir |

### İyi ve kötü örnekler

İyi: Rota sırası değişince numara ve kapsamlı değerlendirme durumu birlikte anlaşılır.
Kötü: Yeni sıra görünürken eski toplam, geçiş tamamlanana kadar geçerli gibi tutulur.
İyi: Hareket azaltıldığında sabit seçili işaret korunur.
Kötü: Animasyon kaldırıldığı için hangi yerin seçildiği de belirsizleşir.
İyi: Kayıt beklemesi nötr durum metniyle görünür.
Kötü: İşlem sürerken marka animasyonu başarı hissi üretir.
Bu örnekler yeni akış önermeyen görsel karar karşılaştırmalarıdır.

### Bölüm öz eleştirisi

- **Öz eleştiri Ö62.1 — Dört süre rolü farklı cihazlarda aynı rahatlığı üretmeyebilir.**
  Risk: Sabit süreye bağlılık algılanan gecikmeyi görünmez kılabilir.
  Kontrol: Temsilî düşük ve orta cihazlarda görevin bekleme algısı değerlendirilmelidir.
  Kabul sınırı: Ölçüm yapılmadan akıcı veya hızlı deneyim iddiası kurulmaz.

- **Öz eleştiri Ö62.2 — Sakinlik için hareketi azaltmak konum ilişkisini zayıflatabilir.**
  Risk: Kullanıcı değişen öğeyi tekrar aramak zorunda kalabilir.
  Kontrol: Statik sıra, başlık ve seçili durumla öğeyi bulma görevi incelenmelidir.
  Kabul sınırı: Kayıp anlam dekoratif hareket ekleyerek örtülemez.

- **Öz eleştiri Ö62.3 — Kesilebilirlik ara görünümde küçük tutarsızlıklar yaratabilir.**
  Risk: Hızlı seçim yapan kişi yanlış son durum algılayabilir.
  Kontrol: Ardışık seçim ve geri dönüşte son durumun anlaşılması sınanmalıdır.
  Kabul sınırı: Son seçim açık değilse hareket sadeleştirilir.

## Hareket Prensipleri

Bölüm kimliği: V63.
Bu bölüm hareketin yönünü, mesafesini ve görsel ağırlığını belirler.
Sayfa geçişleri ve geri dönüş davranışı 11 Ekran Mimarisi tarafından belirlenmeye devam eder.
Yeni hareket türü, yeni ekran veya yeni gezinme ilişkisi tanımlanmaz.

### Yön ve süreklilik çerçevesi

Yön, var olan içerik ilişkisine hizmet eder.
Coğrafya ile arayüz yönü aynı şey değildir.
Harita bir dil yönü değişti diye aynalanmaz.
Kısa mesafe, büyük ekran taramasına tercih edilir.

| Görsel ilişki | Kabul edilen anlatım | Kaçınılan anlatım | Gerekçe |
| --- | --- | --- | --- |
| Seçili durum | Yerinde görünür değişim | Ekran boyunca yolculuk | Öğe yeniden aranmaz |
| Katman açılması | Kontrollü, ölçülü ayrışma | Sıçrayıp geri sekme | Görev ciddiyeti korunur |
| Katman kapanması | Kısa, nötr ayrılma | Uzun dramatik çıkış | Geri dönüş bekletilmez |
| Durak yer değiştirmesi | Yakın ilişki ve yeni sıra | Dönen veya takla atan kart | Mekânsal bilgi okunur |
| Odak görünürlüğü | En az gerekli yer değişimi | Ekran başına sıçrama | Okuma bağlamı korunur |
| Harita seçimi | En az gerekli konum açıklaması | Otomatik uçuş gösterisi | Hareket hassasiyeti gözetilir |

### İlke V63.1 — Mesafe gereksiz büyütülmez.

Karar: Görsel geçiş, ilişkiyi anlatan en küçük mesafeyi kullanır.
Gerekçe: Büyük mesafe bakışın metin ve harita arasında yeniden kurulmasını gerektirir.
Bedel: Büyük ekranlarda hareket daha az fark edilebilir.
Uygulama: Fark edilirlik mesafe büyütmek yerine son durum işaretiyle sağlanır.
Kontrol: Kullanıcının öğeyi yeniden arama ihtiyacı gözlenmelidir.

### İlke V63.2 — Giriş ve çıkış sakin kalır.

Karar: Mevcut kontrollü yavaşlama ve kısa nötr çıkış ilkesi korunur.
Gerekçe: Yaylanma ve geri sekme, basit görev ilişkisini gereksiz fizik gösterisine dönüştürür.
Bedel: Sistem bazı eğlence ürünlerinden daha ciddi algılanır.
Uygulama: Sheet bitişi görünür şekilde yerleşir; tekrar zıplamaz.
Kontrol: Son görünümün hangi anda sabit olduğu belirsiz olmamalıdır.

### İlke V63.3 — Aynı neden aynı hareket anlamını taşır.

Karar: Seçim, kapanış ve düzen değişimi kanal içinde tutarlı görsel karşılık alır.
Gerekçe: Kullanıcı her yeni bileşende hareket dilini yeniden çözmek zorunda kalmaz.
Bedel: Bileşene özgü yaratıcı hareket alanı daralır.
Uygulama: Benzer yer kartları seçildikleri kategoriye göre farklı gösteri yapmaz.
Kontrol: Görsel varyantların bir durumun anlamını değiştirmediği kontrol edilir.

### İlke V63.4 — Harita mekânı temsil eder.

Karar: Harita hareketi marka anlatısı veya ödül olarak kullanılmaz.
Gerekçe: Harita hareketinden kullanıcı gerçek coğrafi değişim sonucu çıkarabilir.
Bedel: Destinasyonlar arasında sinematik geçiş fırsatı kullanılmaz.
Uygulama: Seçilmiş yer gerektiği kadar görünür kılınır; pan arama kapsamını değiştirmez.
Kontrol: Görsel hareketin etkin arama kapsamıyla karıştırılmadığı değerlendirilir.

### İlke V63.5 — Okuma ve hareket birbirini engellemez.

Karar: Karar cümlesi, sürekli hareket eden yüzey üzerinde taşınmaz.
Gerekçe: Sabit bir okuma zemini açık havada ve bölünmüş dikkatte daha öngörülebilirdir.
Bedel: Fotoğraf ve harita üzerinde hareketli tipografi kullanılmaz.
Uygulama: Kritik sınırın zemini, arka plan hareketinden bağımsızdır.
Kontrol: Metin aynı anlam ve okunurlukla durağan görüntüde değerlendirilebilir.

### Neden ve sonuç karşılaştırması

| Hareket tercihi | Kullanıcıya verdiği ipucu | Taşıyamayacağı anlam | Görsel koruma |
| --- | --- | --- | --- |
| Yerinde durum değişimi | Bu kontrol değişti | Sonuç doğrulandı | Durum metni |
| Katman ayrışması | Alt görev açıldı | Yeni ürün alanı var | Aynı görev başlığı |
| Sıra ilişkisi | Bu durak taşındı | Rota yapılabilir | Değerlendirme sınırı |
| Kontrollü kapanış | Alt görev bitti | Uzak işlem iptal oldu | Gerçek işlem durumu |
| Harita konum gösterimi | Seçili yer burada | Kullanıcı orada | Konum kapsamı |
| Doğrudan son görünüm | Hareket azaltıldı | İşlem atlandı | Aynı geri bildirim |

### İyi ve kötü örnekler

İyi: Kapanış görseli tamamlanmadan kullanıcı mevcut geri dönüşünü anlayabilir.
Kötü: Kapanış hızı geri eyleminin yeni bir anlamı olduğunu düşündürür.
İyi: Arama kapsamı sabitken haritanın görünür bölgesi ayrı anlaşılır.
Kötü: Kamera hareketi yeni sonuçlar getirildiği izlenimi verir.
İyi: Hareketsiz düzende yeni durak sırası açık kalır.
Kötü: Duraklar yalnız uçuş güzergâhı izlenerek ayırt edilir.
Buradaki sınırlar, mevcut gezinme davranışının görsel ifadesini daraltır.

### Bölüm öz eleştirisi

- **Öz eleştiri Ö63.1 — Küçük mesafe ve düşük vurgu bir araya gelince değişim kaybolabilir.**
  Risk: Kullanıcı dokunuşunun algılanmadığını düşünebilir.
  Kontrol: Düşük parlaklıkta son durumun fark edilirliği değerlendirilmelidir.
  Kabul sınırı: Görünmeyen karşılık büyüyen hareketle değil açık durumla düzeltilir.

- **Öz eleştiri Ö63.2 — Tutarlı yön bazı platformlarda farklı alışkanlıklarla karşılaşabilir.**
  Risk: Marka tutarlılığı adına sistem geri beklentisi zedelenebilir.
  Kontrol: Platform geri eylemiyle görev dönüşünün okunması ayrı incelenmelidir.
  Kabul sınırı: Yerel gezinme geleneği yeni bir marka jestiyle değiştirilmez.

- **Öz eleştiri Ö63.3 — Haritayı sakin tutmak yerler arasındaki uzaklığı az hissettirebilir.**
  Risk: Kullanıcı kısa görsel geçişi kısa fiziksel yol sanabilir.
  Kontrol: Süre ve mesafe metninin bağımsız anlaşılması sınanmalıdır.
  Kabul sınırı: Hareket uzunluğu fiziksel yolculuk ölçüsü olarak sunulmaz.

## Micro Interaction

Bölüm kimliği: V64.
Mikro etkileşim, mevcut işlemin algılandığını ve gerçek durumunu görünür kılar.
İşlem sonucu, teyit ve geri alma sözleşmeleri bu bölüm tarafından değiştirilmez.
Dayanak: 10 Design System §46 ve 11 Ekran Mimarisi §41.

### Geri bildirim çerçevesi

Basılma karşılığı ile tamamlanma aynı işaret değildir.
Seçilme ile uygunluk aynı vurgu değildir.
Kaydetme ile ziyaret beyanı aynı sonuç değildir.
Bir İz alındı durumu yayınlanmış bilgi anlamına gelmez.

| Mevcut olay | Görsel karşılık | Metnin rolü | Kaçınılan anlam |
| --- | --- | --- | --- |
| Butona basıldı | Basılı durum | İşlemi tanımlar | Başarı peşin ilanı |
| Uzak işlem bekliyor | Nötr bekleme | Neyin beklendiğini söyler | Tamamlandı işareti |
| Chip seçildi | Seçili işaret | Koşulu açık tutar | Doğrulanmış eşleşme |
| Rota taşındı | Yeni numara | Mevcut değişimi açıklar | Yeni toplam garantisi |
| Yer kaydedildi | Gerçek kayıt durumu | Hedefi ve kapsamı söyler | Ziyaret veya beğeni |
| Bir İz alındı | Sade alındı karşılığı | İncelemeden ayırır | Doğrulama rozeti |

### İlke V64.1 — Basma karşılığı yerel kalır.

Karar: Basılı durum eylemin algılandığını gösterir; uzak sonucun işareti olmaz.
Gerekçe: Dokunma yanıtı hızlı olabilirken işlemin gerçek tamamlanması belirsiz kalabilir.
Bedel: Tek bir göz alıcı onay hareketiyle bütün süreci özetlemek mümkün olmaz.
Uygulama: Basılı butonun ardından gerçek işlem durumuna uygun görünüm gelir.
Kontrol: Kullanıcı basma karşılığını başarı olarak anlatmamalıdır.

### İlke V64.2 — Seçili durum kalıcı ipucu taşır.

Karar: Kontrolün seçili görünümü geçici parlamaya bağlı değildir.
Gerekçe: Kullanıcı seçimden sonra başka yere bakıp dönebilir.
Bedel: Kalıcı işaret yüzeyde küçük bir görsel yoğunluk yaratır.
Uygulama: Mevcut işaret, metin ve renk rolleri birlikte çalışır.
Kontrol: İlk hareket görülmeden seçim durumu anlaşılmalıdır.

### İlke V64.3 — Geri alma görsel olarak erişilebilir kalır.

Karar: Mevcut geri alma hakkı kısa animasyona veya kısa ömürlü mesaja bağlanmaz.
Gerekçe: Hareketi kaçırmak kullanıcının yaptığı değişikliği düzeltme hakkını azaltamaz.
Bedel: İlgili kaydın eylem alanında ek görsel açıklık gerekir.
Uygulama: Snackbar kaybolsa da kabul edilmiş kalıcı erişim yolu görünür dilini korur.
Kontrol: Mesajı okumamış kişi düzeltme yolunu bulabilmelidir.

### İlke V64.4 — Hata düzeltmesi bütün yüzeyi oynatmaz.

Karar: Düzeltilen alanın hata görünümü ilgili bağlamda çözülür.
Gerekçe: Bütün formun yeniden görsel kurulması diğer alanların da değiştiği hissini verir.
Bedel: Küçük yerel değişim dikkatli durum tasarımı gerektirir.
Uygulama: Hata rengi kalkarken etiket ve kullanıcı metni kararlı kalır.
Kontrol: Düzeltme sonrası yeniden alan arama ihtiyacı incelenmelidir.

### İlke V64.5 — Kutlama gerçek sonucu aşmaz.

Karar: Mevcut başarının görsel karşılığı sade, kısa ve bağlama uygundur.
Gerekçe: Kaydetme veya katkı, kullanıcıya statü kazandıran bir başarı yarışması değildir.
Bedel: Ürün ödül temelli bağlılık araçlarını kullanmaz.
Uygulama: Kayıt teyidi için konfeti, seri veya rozet üretilmez.
Kontrol: Katkısız veya erken bitirilmiş gün görsel olarak eksik gösterilmemelidir.

### İşlem durumu karşılaştırması

| Görünüm | Doğru kullanım | Yanlış kullanım | Neden |
| --- | --- | --- | --- |
| Basılı yüzey | Girdi karşılığı | Kalıcılık teyidi | Yerel temas uzak kayıt değildir |
| Seçili işaret | Kullanıcı koşulu | Yer niteliği | Seçim kanıt üretmez |
| Nötr bekleme | Sonucu bekleme | Gizli başarı | Belirsizlik görünür kalır |
| Başarı işareti | Gerçek teyit | Tahmini tamamlanma | Yanlış güven önlenir |
| Alan hatası | Belirli sorun | Kullanıcı suçlama | Onarım kolaylaşır |
| Geri alma bağlantısı | Mevcut kontrol | Kısa süreli ödül | Hak zaman baskısına dönüşmez |

### İyi ve kötü örnekler

İyi: Cihazda kaydedilen yer, cihaz kapsamını taşıyan sade teyit alır.
Kötü: Cihaz kaydı bulutta güvence altındaymış gibi parlak kalkanla sunulur.
İyi: Bir İz alındı mesajı yayına ilişkin hüküm vermez.
Kötü: Katkı gelir gelmez yere doğrulanmış rozet görünümü eklenir.
İyi: Düzelen hatanın yanındaki metin kararlı kalır.
Kötü: Başarılı alan doğrulaması formu otomatik başka görsel duruma sıçratır.
Mikro karşılıklar işlem yetkisi veya yayın otoritesi oluşturamaz.

### Bölüm öz eleştirisi

- **Öz eleştiri Ö64.1 — Çok benzer nötr durumlar bekleme ile sonuç belirsizliğini karıştırabilir.**
  Risk: Kullanıcı yeniden basarak çifte işlem yaratmaya çalışabilir.
  Kontrol: Bekleyen ve teyidi kaybolmuş işlem metinleri ayrı okunmalıdır.
  Kabul sınırı: Renk farkı tek başına yeterli kabul edilmez.

- **Öz eleştiri Ö64.2 — Kutlamayı azaltmak önemli tamamlanmayı sönük kılabilir.**
  Risk: Kullanıcı işlemin bittiğini fark etmeyebilir.
  Kontrol: İşlem sonucunun metin ve kalıcı durumla anlaşılması değerlendirilmelidir.
  Kabul sınırı: Tamamlanma fark edilmezse gösteriş değil bilgi belirginliği artırılır.

- **Öz eleştiri Ö64.3 — Yerel hata çözümü görünür bağlamdan uzakta kalabilir.**
  Risk: Kullanıcı düzelttiği alanın kabul edildiğini anlayamayabilir.
  Kontrol: Büyütülmüş metin ve klavye odağıyla alan düzeltme gözlenmelidir.
  Kabul sınırı: Düzeltme bilgisi odak veya görsel konum kaybı yaratmamalıdır.

## Gesture Davranışları

Bölüm kimliği: V65.
Gesture bu belgede mevcut görünür eylemlerin görsel yardımcı anlatımıdır.
Yeni gizli komut, yeni sürükleme işi veya yeni gezinme kısa yolu eklenmez.
Dayanak: 10 Design System §48–50 ve 11 Ekran Mimarisi §37–38.

### Görsel okunurluk çerçevesi

Hareket yapılabilirlik ipucu açık ama ölçülüdür.
Bir tutamaç tek başına görevin tamamını öğretmek zorunda değildir.
Sistem kenar hareketi için ayrılmış alan görev kontrolü gibi gösterilmez.
Harita ile sayfanın farklı hareket bağlamı algılanabilir kalır.

| Mevcut jest | Görsel yardımcı | Mevcut alternatif | Kaçınılan risk |
| --- | --- | --- | --- |
| Rota durağı taşıma | Tutarlı taşıma ipucu | Taşıma kontrolü ve klavye | Tek sürükleme yolu |
| Satır kaldırma | Açık eylem ilişkisi | Görünür satır eylemi | Yanlış kaydırmada kayıp |
| Sheet kapatma | Katman ve kapatma ilişkisi | Görünür kapatma | Çıkışın gizlenmesi |
| Harita yakınlaştırma | Kontrol grubu | Yakınlaştırma düğmeleri | Çok parmak zorunluluğu |
| Harita pan | Harita sınırı | Liste görünümü | Sayfanın ele geçirilmesi |
| Sistem geri | Yerel gezinme işareti | Mevcut geri kontrolü | Marka hareketiyle çatışma |

### İlke V65.1 — Görünür alternatif eşit ağırlık taşır.

Karar: Jest alternatifi, düşük kontrastlı ikincil bir yardım gibi saklanmaz.
Gerekçe: Kullanıcının motor kapasitesi ve giriş yöntemi temel görev hakkını değiştirmez.
Bedel: Kontrol alanı yalnız jest kullanan kişi için daha dolu görünür.
Uygulama: Durak taşıma eylemi metinle bulunabilir kalır.
Kontrol: Jest kullanmadan aynı görev kapsamı anlaşılmalıdır.

### İlke V65.2 — Tutamaç taşıma anlamını aşmaz.

Karar: Taşıma ipucu yalnız zaten taşınabilir öğelerde görünür.
Gerekçe: Dekoratif tutamaçlar kullanıcıya olmayan eylem vaadi verir.
Bedel: Kartlar arasında bazı küçük optik farklar oluşur.
Uygulama: Salt okunur paylaşılan içerik düzenlenebilir gibi görünmez.
Kontrol: Görsel ipucunun yetki sınırıyla uyumu incelenmelidir.

### İlke V65.3 — Yıkıcı anlam önceden anlaşılır.

Karar: Mevcut kaldırma eyleminin metni ve semantik vurgusu açıktır.
Gerekçe: Bir satırın yana hareketi, silme ile arşivlemeyi kendi başına açıklamaz.
Bedel: Sadece ikona dayalı daha kompakt görünüm tercih edilmez.
Uygulama: Görsel dil mevcut geri alma ve kayıp açıklamasıyla tutarlı kalır.
Kontrol: Kullanıcı eylemin hangi kaydı etkilediğini söyleyebilmelidir.

### İlke V65.4 — Kenarlar platforma saygı gösterir.

Karar: Sistem geri alanı bağımsız ürün sürüklemesinin görsel hedefi yapılmaz.
Gerekçe: Aynı fiziksel hareketin iki anlamı yanlış görevden çıkışa yol açabilir.
Bedel: Kullanılabilir görsel kontrol alanı bazı cihazlarda daralır.
Uygulama: Kenara yerleştirilen kontrolün dokunma ve odak açıklığı korunur.
Kontrol: Kenar geri kullanımı sırasında komşu görev eylemiyle çatışma sınanmalıdır.

### İlke V65.5 — Doğrudan manipülasyon dürüst görünür.

Karar: Sürüklenen öğe girdiyle ilişkisini gecikmesiz ve sınırlı görsel vurgu ile gösterir.
Gerekçe: Geciken veya büyüyen nesne tutuş hassasiyetini belirsizleştirir.
Bedel: Dramatik yükselme veya büyüme etkisi kullanılmaz.
Uygulama: Yeni sıra son durumda numara ve mevcut açıklamayla görünür kalır.
Kontrol: Bırakma noktası, yeni sıra ve değerlendirme durumu karıştırılmamalıdır.

### Alternatif giriş karşılaştırması

| Kullanım biçimi | Görsel ihtiyaç | Yetersiz yaklaşım | Korunan değer |
| --- | --- | --- | --- |
| Tek elle dokunma | Ayrışan hedef | Bitişik küçük ikon | Yanlış eylemden korunma |
| Klavye | Görünür odak | Yalnız hover | Bağımsız görev tamamlama |
| Anahtar denetimi | Anlaşılır eylem | Uzun basma tek yolu | Giriş eşitliği |
| Sesle kontrol | Görünür ad | Adsız ikon | Komutun bulunması |
| Büyütülmüş görünüm | Kapanış erişimi | Kesilmiş tutamaç | Görevden çıkabilme |
| Hareket azaltma | Statik son durum | Yalnız sürükleme izi | Durumu okuyabilme |

### İyi ve kötü örnekler

İyi: Taşıma kontrolü, sürükleme ipucuyla aynı durağı ve aynı anlamı taşır.
Kötü: Görünür taşıma yolu yalnız yardım metninde anlatılır.
İyi: Harita kontrolleri kendi opak ve belirgin alanında algılanır.
Kötü: Pan alanı sayfanın bütün dikey kaydırmasını ele geçirir.
İyi: Kapatma kontrolü ve katmanın sınırı birlikte okunur.
Kötü: Kapatılabilirlik sadece görünmeyen aşağı kaydırma alışkanlığına bırakılır.
Görsel ipuçları mevcut davranış sözleşmesinin yerine geçmez.

### Bölüm öz eleştirisi

- **Öz eleştiri Ö65.1 — Alternatif eylemler görsel yoğunluğu artırabilir.**
  Risk: Tek elle kullanımda doğru hedefi seçme süresi uzayabilir.
  Kontrol: Taşıma, kaldırma ve ayrıntı hedeflerinin birlikte ayırt edilmesi incelenmelidir.
  Kabul sınırı: Yoğunluk azaltılırken erişilebilir alternatif kaldırılmaz.

- **Öz eleştiri Ö65.2 — Tutamaçlar bütün kullanıcılar için açık bir sembol olmayabilir.**
  Risk: Salt biçim üzerinden düzenlenebilirlik beklentisi hatalı oluşabilir.
  Kontrol: İlk kez gören kişinin eylem anlamı kendi sözüyle sorulmalıdır.
  Kabul sınırı: Görünür eylem adı tutamacın tanınırlığına feda edilmez.

- **Öz eleştiri Ö65.3 — Harita ve sayfa sınırı zayıf kontrastta kaybolabilir.**
  Risk: Kullanıcı hangi yüzeyi hareket ettirdiğini anlayamayabilir.
  Kontrol: Farklı harita yoğunluklarında kontrol ve yüzey sınırı değerlendirilmelidir.
  Kabul sınırı: Harita kullanımı listeye erişimi görsel olarak kilitlememelidir.

## Haptic Feedback

Bölüm kimliği: V66.
Dokunsal geri bildirim mevcut görsel ve metinsel durumun isteğe bağlı yardımcısıdır.
Bu bölüm yeni titreşim komutu, bildirim türü veya zorunlu cihaz yeteneği tanımlamaz.
Dayanak: 10 Design System §46; platform ve kullanıcı tercihi belirleyicidir.

### Duyusal karşılık çerçevesi

Dokunma hissi bir işlemin kanıtı değildir.
Görsel karşılık dokunsal desteğin bulunmadığı cihazlarda da tamamdır.
Günlük geziyi oyunlaştıran titreşim serileri kullanılmaz.
Ses ve haptik olmadan aynı durum anlaşılabilir kalır.

| Durum | Dokunsal rolün sınırı | Zorunlu görsel karşılık | Yanlış çağrışım |
| --- | --- | --- | --- |
| Yerel seçim | İsteğe bağlı kısa yardımcı | Seçili işaret ve metin | Yer uygunluğu doğrulandı |
| Gerçek tamamlanma | Teyitten sonra yardımcı | Doğru sonuç durumu | Her basış başarıdır |
| Hata | Anlamlıysa yardımcı | İlgili hata ve onarım | Kullanıcı cezalandırılıyor |
| Bekleme | Tekrarlı dürtü yok | Nötr durum metni | Daha çok dikkat zorunlu |
| Harita gezinme | Sürekli titreşim yok | Konum ve kontrol açıklığı | Pin yoğunluğu kalite demek |
| Bir İz | Statü hissi yok | Alındı ile yayın ayrımı | Katkı rozeti kazanıldı |

### İlke V66.1 — Dokunsal kanal tamamlayıcıdır.

Karar: Hiçbir başarı, hata veya seçim yalnız titreşimle ifade edilmez.
Gerekçe: Cihaz, kullanıcı tercihi ve algı farklılıkları dokunsal kanalı devre dışı bırakabilir.
Bedel: Görsel tasarım dokunsal desteğe yaslanarak sadeleştirilemez.
Uygulama: Haptik kapalıyken metin ve işaret aynı anlamı taşır.
Kontrol: Sessiz ve dokunsuz kullanım ayrı değerlendirilmelidir.

### İlke V66.2 — Teyit görsel ve dokunsal olarak aynı gerçeğe bağlıdır.

Karar: Tamamlanma hissi yetkili işlem sonucundan önce sunulmaz.
Gerekçe: Dokunsal bir onay, gözden kaçan bekleme metninden daha kesin algılanabilir.
Bedel: Ağ gecikmesinde güçlü tamamlanma hissi ertelenir.
Uygulama: Basma karşılığı ile gerçek kayıt teyidi farklı durumlar olarak korunur.
Kontrol: Kullanıcının yalnız dokunsal karşılıktan çıkardığı anlam sınanmalıdır.

### İlke V66.3 — Tekrar dikkat baskısına dönüşmez.

Karar: Rutin bekleme ve harita gezintisi tekrar eden dokunsal uyaran üretmez.
Gerekçe: Cepte, yürürken veya toplu taşımada gereksiz uyarı dikkat yükünü artırır.
Bedel: Bazı küçük değişiklikler kullanıcı tarafından hemen fark edilmeyebilir.
Uygulama: Mevcut kalıcı durum metni fark edilmenin ana dayanağıdır.
Kontrol: Uzun kullanımda rahatsızlık ve yanlış bildirim algısı araştırılmalıdır.

### İlke V66.4 — Dokunsal gösteri premium işareti değildir.

Karar: Premium kapsamı daha güçlü titreşim veya özel kutlama dizisiyle ayrılmaz.
Gerekçe: Üyelik temel kontrolün duyusal kalitesini değiştirmemelidir.
Bedel: Ücretli alana duyusal statü farkı eklenmez.
Uygulama: Aynı kayıt işlemi hesap hakkından bağımsız aynı dürüst sonucu taşır.
Kontrol: Ücretsiz ve ücretli deneyim arasında temel geri bildirim eşitliği incelenir.

### İlke V66.5 — Platform farkı anlam farkı değildir.

Karar: Desteklenen yerel dokunsal olanaklar kullanılsa da ürün durumunun anlamı ortak kalır.
Gerekçe: Farklı cihazların aynı fiziksel hissi üretmesi varsayılamaz.
Bedel: Cihazlar arasında bire bir duyusal eşitlik vaat edilmez.
Uygulama: Görsel teyit ve eylem adı her kanalda durumun asıl açıklaması olarak korunur.
Kontrol: Cihaz değişiminde kullanıcı farklı bir işlem sonucu varsaymamalıdır.

### Duyusal denge karşılaştırması

| Tercih | Yarar | Bedel | Koruyucu görsel karar |
| --- | --- | --- | --- |
| İsteğe bağlı haptik | Kullanıcı tercihine uyum | Daha az duyusal ipucu | Açık durum işareti |
| Sade tamamlanma | Gerçek sonuç okunur | Kutlama hissi azalır | Kapsamlı teyit metni |
| Beklemede sessizlik | Dikkat yükü azalır | Bekleme unutulabilir | Kalıcı nötr durum |
| Platform uyumu | Tanıdık his | Cihaz farkı sürer | Ortak işlem dili |
| Hata metni önceliği | Onarım anlaşılır | Metin alanı gerekir | Yerel hata ilişkisi |
| Üyelikten bağımsızlık | Temel hak eşitliği | Statü ayrımı yok | Aynı görünür sonuç |

### İyi ve kötü örnekler

İyi: Haptik bulunmayan cihazda kaydın hedefi ve sonucu açıkça okunur.
Kötü: Titreşim alınmadığı için kullanıcının yeniden basması beklenir.
İyi: İşlem teyidi görünür durumla aynı anda aynı anlamı taşır.
Kötü: Bağlantı yokken dokunsal onay işlemi tamamlanmış hissettirir.
İyi: Hata somut onarım metniyle açıklanır.
Kötü: Uzun titreşim dizisi hata nedenini açıklamanın yerine geçer.
Dokunsal sistem, görsel durumların doğruluğunu güçlendirebilir; doğruluk üretemez.

### Bölüm öz eleştirisi

- **Öz eleştiri Ö66.1 — Dokunsal desteği sınırlamak bazı kullanıcıların yararlı ipucunu azaltabilir.**
  Risk: Görsel dikkat sınırlıyken tamamlanma daha zor fark edilebilir.
  Kontrol: İsteğe bağlı haptikle ve haptiksiz aynı görev karşılaştırılmalıdır.
  Kabul sınırı: Destek kaldırılmasa da temel anlam tek kanala bağlanamaz.

- **Öz eleştiri Ö66.2 — Aynı adla anılan yerel haptikler cihazlarda farklı hissedilebilir.**
  Risk: Bir cihazın nötr karşılığı başka cihazda hata uyarısı sanılabilir.
  Kontrol: Temsilî cihazlarda kullanıcı anlamlandırması değerlendirilmelidir.
  Kabul sınırı: Duyusal benzerlik ölçülmeden ortak kalite iddiası kurulmaz.

- **Öz eleştiri Ö66.3 — Dokunsal sonuç çok güçlü algılanırsa metin okunmayabilir.**
  Risk: Kullanıcı cihaz kaydını hesap kaydı gibi genelleyebilir.
  Kontrol: Haptik açıkken kayıt kapsamı anlama görevi yürütülmelidir.
  Kabul sınırı: Kapsam yanlış anlaşılıyorsa yardımcı haptik sadeleştirilir.

## Premium Detaylar

Bölüm kimliği: V67.
Premium hissi bu bölümde bütün ürünün görsel özen düzeyini ifade eder.
Ücretli Premium hizmet hakkının kapsamı kabul edilmiş ticari ve ekran belgelerinde kalır.
Görsel kalite, bilgi doğruluğu veya erişilebilirlik ücretli ayrıcalık olarak sunulmaz.

### Özen çerçevesi

Küçük ayrıntılar anlamı temizlediğinde değerlidir.
Yüzeyin pahalı görünmesi yerin pahalı veya iyi olduğunu ima etmez.
Sistem sans ailesi ve mevcut renk rolleri korunur.
Premium kimlik, altın renkli yeni bir doğruluk katmanı değildir.

| Ayrıntı | Görsel karar | Değer | Yanlış araç |
| --- | --- | --- | --- |
| Optik hizalama | İkon ve metin dengesi | Sakin okuma | Her öğeyi mekanik ortalama |
| Sayı ritmi | Süre ve maliyetin okunması | Hızlı kıyas | Büyük süslü rakam |
| Fotoğraf sınırı | Gerçek içeriğe temiz çerçeve | Yer kimliği | Parlak kalite rozeti |
| Yüzey ayrımı | Sınır, boşluk ve ton | Katman açıklığı | Her karta ağır gölge |
| Durum dili | Gerçek işlemle tutarlı görünüm | Güven | Teyitsiz başarı animasyonu |
| Çıkış kontrolü | Açık ve okunur | Baskısız kullanım | Silik vazgeçme eylemi |

### İlke V67.1 — Özen eşit dağılır.

Karar: Boş, hata, offline ve ücretsiz durumlar ana içerikle aynı görsel titizliği taşır.
Gerekçe: Güven en çok işin aksadığı veya içeriğin eksik olduğu anda sınanır.
Bedel: Nadir görülen durumlara da tasarım değerlendirme emeği ayrılır.
Uygulama: Offline sınırı düşük kalite gri bir geçici ekran gibi sunulmaz.
Kontrol: Sadece ideal içerikle yapılan inceleme yeterli kabul edilmez.

### İlke V67.2 — Optik düzeltme anlamı korur.

Karar: Görsel hizalama, mevcut grid ve ölçü rollerinin içinde optik denge sağlar.
Gerekçe: İkonun matematiksel kutusu ile algılanan ağırlığı aynı olmayabilir.
Bedel: Aynı kutu ölçüsü tüm öğelerde otomatik olarak iyi sonuç vermez.
Uygulama: Metin başlangıcı, ikon ağırlığı ve hedef sınırı birlikte değerlendirilir.
Kontrol: Optik düzeltme dokunma hedefini daraltmamalıdır.

### İlke V67.3 — Az dekor yüksek içerik açıklığı gerektirir.

Karar: Sade yüzeyler güçlü hiyerarşi ve doğru metin aralığıyla tamamlanır.
Gerekçe: Dekor azaldığında küçük hizalama ve kontrast sorunları daha görünür olur.
Bedel: Minimal görünüm son düzeltme aşamasında daha fazla dikkat gerektirir.
Uygulama: Boşluk miktarı görev ilişkisini açıklayacak kadar kesin kullanılır.
Kontrol: Sadeleşme sonucunda ilişkili bilgi parçalarının ayrılmadığı incelenir.

### İlke V67.4 — Premium görünüm kesinlik satmaz.

Karar: Cilalı kart, parlak sınır veya büyük fotoğraf bir iddianın güvenini artırmış gibi sunulmaz.
Gerekçe: Estetik etki kanıt yeterliliğiyle kolay karıştırılabilir.
Bedel: İkna gücü yüksek bazı görsel araçlar kapsamlı bilgiyle sınırlandırılır.
Uygulama: Önemli bilinmeyen, en özenli yer kartında da aynı okuma birimindedir.
Kontrol: Görsel kalite ile bilginin kesinliğinin ayrı anlatılabildiği sınanmalıdır.

### İlke V67.5 — Gerçek hizmet kapsamı sakin görünür.

Karar: Açılmış Premium kolaylığı varsa kapsamı mevcut metin ve semantik düzenle açıklanır.
Gerekçe: Ücretli hizmet, gezi kararını kesen bir statü gösterisi olmamalıdır.
Bedel: Satış vurgusu karar metninin önüne geçemez.
Uygulama: Premium açıklaması temel kayıt veya hata görünümünü gölgeleyen bir katman yaratmaz.
Kontrol: Üyelik göstergesi yer uygunluğu veya ayrıcalıklı doğruluk gibi okunmamalıdır.

### Özen ve gösteriş karşılaştırması

| Alan | Özenli tercih | Gösterişe kayan tercih | Neden reddedilir |
| --- | --- | --- | --- |
| Tipografi | Dengeli satır ve ağırlık | Dekoratif ince başlık | Okunma kırılganlaşır |
| Renk | Anlamlı sınırlı vurgu | Her alanda doygun renk | Öncelik kaybolur |
| Gölge | Gerekli katman ayrımı | Her nesnede yükselme | Sahte önem oluşur |
| Hareket | Kısa durum ilişkisi | Sürekli marka döngüsü | Dikkat parçalanır |
| Fotoğraf | Gerçek mekân kapsamı | Atmosferi abartan düzenleme | Beklenti çarpılır |
| Üyelik | Somut hizmet açıklaması | Parıltılı güven kalkanı | Hak ve bilgi karışır |

### İyi ve kötü örnekler

İyi: Aynı görsel ritim hem dolu listeyi hem bilgi açığını okunur kılar.
Kötü: Az verili yer düşük kalite bir tasarım varyantıyla cezalandırılır.
İyi: Ücretli kolaylığın açıklaması mevcut kapsamı sakin biçimde anlatır.
Kötü: Premium kullanıcı için aynı yer daha güvenilir renk ve rozetle gösterilir.
İyi: Metin büyüdüğünde kart da içerik kadar büyür.
Kötü: Premium görünümü korumak için kritik sınır üç noktaya kesilir.
Kalite hissi gerçek kullanıcı araştırması yapılmadan ulaşılmış sonuç sayılmaz.

### Bölüm öz eleştirisi

- **Öz eleştiri Ö67.1 — Sade özen bazı kullanıcılarca fazla kurumsal bulunabilir.**
  Risk: Turistik merak ve yer karakteri zayıflayabilir.
  Kontrol: Gerçek fotoğraf ve yer anlatımının merak uyandırması incelenmelidir.
  Kabul sınırı: Sıcaklık, kanıtsız olumlu sıfat veya dekoratif baskıyla kurulmaz.

- **Öz eleştiri Ö67.2 — Her duruma eşit özen verme bakım maliyetini yükseltir.**
  Risk: Ana görev iyileştirmeleri nadir görsel varyantlarla gecikebilir.
  Kontrol: Ortak rollerin yeniden kullanımı ve gerçek varyant ihtiyacı değerlendirilmelidir.
  Kabul sınırı: Bakım baskısı kritik bilgi görünürlüğünü azaltma gerekçesi değildir.

- **Öz eleştiri Ö67.3 — Cilalı görünüm istemeden fazla güven üretebilir.**
  Risk: Kullanıcı belirsizlik metnini görse bile genel güvence algılayabilir.
  Kontrol: Estetik değerlendirme ile bilgi kesinliği değerlendirmesi ayrı yürütülmelidir.
  Kabul sınırı: Fazla güven gözlenirse belirsizliğin göreli görünürlüğü güçlendirilir.

## UX Kalite Standartları

Bölüm kimliği: V68.
Görsel kalite, mevcut görevin anlaşılabilir ve bağımsız tamamlanabilir görünmesidir.
Bu bölüm araştırma sonucu, uygulama testi veya uygunluk sertifikası ilan etmez.
Dayanak: 10 Design System §55–57 ve sistem kabul senaryoları.

### Değerlendirme çerçevesi

Ekranın güzel bulunması kararın doğru anlaşılmasıyla aynı ölçü değildir.
Karar sınırı, sonraki eylem ve geri dönüş birlikte değerlendirilir.
Farklı giriş yöntemleri aynı temel anlamı taşır.
Görsel inceleme gerçek kullanıcı ve yardımcı teknoloji sınamalarının yerini tutmaz.

| Değerlendirme alanı | Mevcut ürün hedefi | İncelenecek görsel kanıt | Yanlış tamamlanma iddiası |
| --- | --- | --- | --- |
| Metin okunması | Büyütmede bilgi kaybı yok | Tam kritik cümle | Küçük metinde okunuyordu |
| Kontrol erişimi | 48 birim varsayılan hedef | Ayrışan hedef alanı | İkon görünüyor |
| Küçük kontrol | 44 birim ürün alt sınırı | Çakışmayan etkileşim alanı | Sıkışınca küçültebiliriz |
| Odak | 2 tb halka ve 2 tb ayrım başlangıcı | Kırpılmayan görünür kontrol | Klavye çalışıyor |
| Durum anlamı | Renk dışında metin ve işaret | Seçim, hata ve bekleme ayrımı | Palet semantik |
| Kanal eşitliği | Aynı karar hakkı | Aynı önemli sınır | Mobilde yer yok |

### İlke V68.1 — Kalite görev bağlamında değerlendirilir.

Karar: Bileşenin tek görünümü yerine mevcut görevin ilgili durumları birlikte incelenir.
Gerekçe: Güzel bir buton yanlış sonuç veya okunamayan sınırla birleşince görev kalitesi sağlamaz.
Bedel: İnceleme yalnız ideal bileşen kataloğundan daha fazla zaman alır.
Uygulama: Yer kartı, hata ve geri dönüşte aynı iddia kapsamıyla değerlendirilir.
Kontrol: İnceleme kaydı hangi görev ve durumun ele alındığını belirtmelidir.

### İlke V68.2 — Kritik bilgi görsel kabul sınırıdır.

Karar: Olumlu gerekçe ile karar değiştiren sınır aynı okuma biriminde anlaşılır kalır.
Gerekçe: Görsel öncelik kullanıcıya metnin söylemediği bir güvence verebilir.
Bedel: Bazı kartlar daha uzun ve daha az simetrik olur.
Uygulama: Uzun bilinmeyen metni kısaltmak yerine içerik alanı büyür.
Kontrol: İlk bakış değerlendirmesinde önemli engelin kaçırılması araştırılmalıdır.

### İlke V68.3 — Test kapsamı iddiayı sınırlar.

Karar: Okunabilirlik ve erişilebilirlik yalnız gerçekten incelenmiş koşullar için raporlanır.
Gerekçe: Tasarım kuralının belgede bulunması çalışan deneyimin doğrulandığı anlamına gelmez.
Bedel: Kısa ve iddialı tamamlanma etiketleri kullanılamaz.
Uygulama: Bu belgedeki tüm görev sınamaları gelecek değerlendirme koşullarıdır.
Kontrol: Cihaz, tema, dil, giriş yöntemi ve tarih olmadan kapsamlı başarı iddiası kurulmaz.

### İlke V68.4 — Görsel sadelik bilgi kaybıyla ölçülmez.

Karar: Sadeleşme, kritik metni veya görünür çıkışı kaldırarak yapılmaz.
Gerekçe: Az öğe daha az anlama yükü anlamına gelmeyebilir.
Bedel: En minimal görünen varyant kabul edilmeyebilir.
Uygulama: Önce dekor, gereksiz tekrar ve yardımcı görsel yoğunluk azaltılır.
Kontrol: Kullanıcının hangi kararı vereceği ve nasıl vazgeçeceği görünür kalmalıdır.

### İlke V68.5 — Kusur önceliği estetik puan değildir.

Karar: Yanlış anlam, erişim kaybı ve kontrol kaybı küçük optik sapmadan önce ele alınır.
Gerekçe: Karar kalitesi ile piksel düzenliliği aynı zarar düzeyini taşımaz.
Bedel: Bazı küçük hizalama işleri daha geç tamamlanabilir.
Uygulama: Kesilen engel metni, fotoğraf köşesi farkından daha önceliklidir.
Kontrol: İnceleme listesinde riskin kullanıcıya somut sonucu yazılmalıdır.

### Kalite karşılaştırması

| Yetersiz ölçüt | Neden yetmez | Daha anlamlı soru | Görsel karşılık |
| --- | --- | --- | --- |
| Temiz görünüyor | Eksik bilgi de temiz görünür | Sınır anlaşılıyor mu | İddia ve sınır birlikteliği |
| Hızlı hissettiriyor | Sahte ilerleme yanıltabilir | Gerçek durum biliniyor mu | Dürüst bekleme |
| Her şey hizalı | Hiyerarşi yanlış olabilir | Önce gerekli bilgi okunuyor mu | İçerik önceliği |
| Renkler uyumlu | Kontrast yetersiz olabilir | Metin okunuyor mu | Rol eşleşmesi |
| Harita zengin | Karar bilgisi kaybolabilir | Listeyle aynı anlam var mı | Yardımcı harita |
| Premium görünüyor | Fazla güven oluşabilir | Belirsizlik ayırt ediliyor mu | Kapsamlı durum dili |

### İyi ve kötü örnekler

İyi: Uzun Türkçe yer adıyla ve büyütülmüş metinle kritik bilgi incelenir.
Kötü: Kısa İngilizce örnekler bütün diller için doğrulama sayılır.
İyi: Offline durumun tarihi ve sınırı normal içerik kadar okunur kalır.
Kötü: Ağ yokken bütün yüzey düşük kontrastla okunamazlaştırılır.
İyi: Odak halkası fotoğraf ve harita üzerinde de ayrı değerlendirilir.
Kötü: Düz beyaz zemindeki kontrol sonucu bütün yüzeylere genellenir.
Bu kalite kuralları mevcut WCAG hedefini veya ürün hedeflerini yeniden tanımlamaz.

### Bölüm öz eleştirisi

- **Öz eleştiri Ö68.1 — Geniş değerlendirme kapsamı küçük ekibi yavaşlatabilir.**
  Risk: İnceleme tamamlanamadığı için bütün gelişim durabilir.
  Kontrol: Kritik görev ve durum önceliği açıkça kaydedilmelidir.
  Kabul sınırı: Kapsam daraltılabilir; yapılmamış sınama yapılmış sayılamaz.

- **Öz eleştiri Ö68.2 — Görsel karar testleri davranış sorunlarını üstlenebilir.**
  Risk: Akış problemi yalnız renk veya aralık değişimiyle kapatılmaya çalışılabilir.
  Kontrol: Her bulgunun görsel kapsamda çözülebilirliği ayrıca değerlendirilmelidir.
  Kabul sınırı: Bu belge kabul edilmiş akışları sessizce değiştiremez.

- **Öz eleştiri Ö68.3 — İlk bakış ölçümü yavaş ve dikkatli okumayı değersizleştirebilir.**
  Risk: Hız hedefi ayrıntılı karar hakkını daraltabilir.
  Kontrol: Kısa tarama ile ayrıntılı okuma ayrı görevler olarak incelenmelidir.
  Kabul sınırı: Daha hızlı görünen varyant önemli açıklamayı saklıyorsa kabul edilmez.

## Görsel Tutarlılık Kuralları

Bölüm kimliği: V69.
Tutarlılık, aynı anlamın farklı yerlerde tanınabilir görsel karşılık bulmasıdır.
Bütün bileşenlerin aynı görünmesi veya aynı miktarda bilgi taşıması değildir.
Dayanak: 10 Design System token, alan bileşeni ve kanal uyarlaması sözleşmeleri.

### Ortak dil çerçevesi

Renk rolü bilgi türünden ve durumundan gelir.
Radius rolü görev ilişkisini ve yüzey ailesini izler.
Tipografi önem ve okuma işini taşır.
Platform uyarlaması ortak karar anlamını korur.

| Ortak karar | Korunan şey | Değişebilen sunum | Değişemeyen anlam |
| --- | --- | --- | --- |
| Metin hiyerarşisi | İddia ve sınır ilişkisi | Satır sayısı | Kritik bilinmeyen |
| Seçili durum | Kullanıcı seçiminin açıklığı | Yerel kontrol biçimi | Uygunluk hükmü değildir |
| Hata görünümü | Sorun ve onarım bağlantısı | Kullanılabilir alan | Kullanıcı verisi kaybolmaz |
| Yüzey ayrımı | Etkin görev ilişkisi | Kanalın panel biçimi | Tek etkin modal |
| Renk anlamı | Rol tutarlılığı | Açık ve koyu tonlar | Başarı ile seçim ayrımı |
| Hareket | Durumun açıklanması | Platformun yerel karşılığı | Statik eşdeğer |

### İlke V69.1 — Rol adları görsel hafızayı korur.

Karar: Aynı durum aynı anlamsal rolü kullanır; yeni renk her yeni kategori için üretilmez.
Gerekçe: Kullanıcı renk sözlüğünü her içerik türünde yeniden öğrenmemelidir.
Bedel: Kategori bazında sınırsız görsel çeşitlilik oluşmaz.
Uygulama: Restoran ve etkinlikte bekleme aynı nötr işlem ailesinden gelir.
Kontrol: Rol benzerliği gerçek anlam benzerliğiyle doğrulanmalıdır.

### İlke V69.2 — İçerik farkı korunur.

Karar: Ortak kart ailesi restoran, etkinlik ve otelin karar açısından farklı bilgilerini silmez.
Gerekçe: Görsel birlik adına önemli zaman veya kapsam bilgisi kaybolabilir.
Bedel: Kartlar her koşulda aynı yükseklikte durmaz.
Uygulama: Aynı hiyerarşi içinde ilgili somut bilgi farklı uzunlukta yer alabilir.
Kontrol: Kategori farkı yalnız fotoğrafa bırakılmamalıdır.

### İlke V69.3 — Tema yalnız görünürlük eksenidir.

Karar: Light ve dark modda anlam, sıra, izin ve temel eylemler değişmez.
Gerekçe: Tema tercihi yeni bir ürün durumu veya güven seviyesi değildir.
Bedel: Her temada ayrı kontrast ve yüzey değerlendirmesi gerekir.
Uygulama: Aynı bilinmeyen koyu temada daha silik hale getirilmez.
Kontrol: Her iki temada önem sıralaması aynı kalmalıdır.

### İlke V69.4 — İstisna bir görev gerekçesi taşır.

Karar: Yeni görsel varyant ancak kabul edilmiş görevin somut içerik ihtiyacını karşılıyorsa kullanılır.
Gerekçe: Gerekçesiz varyantlar sistemin bakımını ve öğrenilebilirliğini zayıflatır.
Bedel: Tekil estetik tercihler ortak sisteme kolayca eklenmez.
Uygulama: İç admin yoğunluğu yetkili inceleme işiyle sınırlı kalır.
Kontrol: İstisnanın nedeni, sahibi ve kapsamı mevcut sistem yönetişimiyle kaydedilmelidir.

### İlke V69.5 — Kanallar anlamda eşit kalır.

Karar: Mobil, web ve tablet aynı karar sınırını farklı alan kapasitesinde taşır.
Gerekçe: Ekran küçülmesi kullanıcının bilgi hakkını azaltamaz.
Bedel: Bazı alanlar daha fazla dikey uzunluk gerektirir.
Uygulama: Önce kolon ve dekor azalır; kritik bilgi sığdırmak için kesilmez.
Kontrol: Aynı yerin farklı kanallardaki anlamı karşılaştırılmalıdır.

### Tutarlılık ve aynılık karşılaştırması

| Konu | Tutarlı yaklaşım | Aşırı aynılık | Sonuç |
| --- | --- | --- | --- |
| Kart yüksekliği | İçeriğe göre esnek | Her kartı sabitlemek | Kritik bilgi kesilebilir |
| Platform geri | Tanıdık yerel karşılık | Her yerde özel ikon | Beklenti zedelenebilir |
| Tema | Eşdeğer rol kontrastı | Aynı renk kodu | Okunurluk kaybolabilir |
| Admin | Ortak temel, görev yoğunluğu | Tüketici kartını çoğaltmak | İnceleme zorlaşabilir |
| Harita | Aynı sonuç, coğrafi görünüm | Liste satırını haritaya yığmak | Konum okunmaz |
| Tipografi | Sistem sans ve rol | Her başlığı aynı boyut | Hiyerarşi kaybolur |

### İyi ve kötü örnekler

İyi: Üç içerik türünde aynı bilgi sınırı rolü aynı önemi taşır.
Kötü: Otel kartındaki belirsizlik, fotoğraf daha büyük olsun diye küçültülür.
İyi: Koyu temada katmanlar yüzey ve sınırla ayrılır.
Kötü: Açık temanın gölgesi karartılıp tek ayrım aracı yapılır.
İyi: Platform geri biçimi değişse de aynı önceki göreve dönüş anlatılır.
Kötü: Marka tutarlılığı adına bütün sistem gezinme işaretleri yeniden icat edilir.
Tutarlılık kayıtlı ürün kararlarını görsel olarak sürdürülebilir kılmalıdır.

### Bölüm öz eleştirisi

- **Öz eleştiri Ö69.1 — Güçlü ortak roller yerel içerik karakterini bastırabilir.**
  Risk: Şehirler ve yer türleri birbirinden ayırt edilmez hissedilebilir.
  Kontrol: Gerçek fotoğraf, ad ve somut özelliklerle karakterin anlaşılması incelenmelidir.
  Kabul sınırı: Karakter için yeni kalite renkleri veya puanlar eklenmez.

- **Öz eleştiri Ö69.2 — Esnek kart boyları karşılaştırma ritmini bozabilir.**
  Risk: Kullanıcı farklı bilgilerin eşlerini bulmakta zorlanabilir.
  Kontrol: Ortak etiket ve başlık konumunun taramaya etkisi değerlendirilmelidir.
  Kabul sınırı: Simetri kazanmak için kritik içerik kesilmez.

- **Öz eleştiri Ö69.3 — Çok sayıda istisna belgesi sistemin anlaşılmasını zorlaştırabilir.**
  Risk: Ortak rol yerine yerel kural yığını oluşabilir.
  Kontrol: Bir istisnanın gerçek tekrar ihtiyacını karşılayıp karşılamadığı izlenmelidir.
  Kabul sınırı: Gerekçesi kalmayan varyant yeni varsayılan sayılmaz.

## Yapılmaması Gerekenler

Bölüm kimliği: V70.
Bu bölüm kabul edilmiş ürün sınırlarını ihlal eden görsel tercihleri açıklaştırır.
Yasaklar dekor beğenisine değil somut yanlış anlam ve kontrol kaybına dayanır.
Yeni ürün politikası veya yeni engelleme akışı tanımlanmaz.

### Korunan sınırlar

Estetik bir yüzey ikinci karar motoru olamaz.
Olumlu görünüm bilinmeyen bilgiyi tamamlayamaz.
Ticari görünürlük organik sıra ve uygunluk anlamı üretemez.
Kullanıcının açık tercihi görsel hileyle zayıflatılamaz.

| Kaçınılacak tercih | Ürettiği yanlış anlam | Kabul edilmiş sınır | Görsel karşılık |
| --- | --- | --- | --- |
| Yıldız ve genel puan | Yer üstünlüğü | Puansız karar dili | Somut özellik ve kapsam |
| Güven yüzdesi | Sayısal kesinlik | İç skor kamusal değil | İddia düzeyinde sınır |
| Parlak AI kalkanı | AI doğruladı | AI yayın otoritesi değil | Sade açıklama |
| Premium kalite halesi | Ücret daha doğru bilgi sağlar | Ortak doğruluk çekirdeği | Somut hizmet kapsamı |
| Silik bilinmeyen | Önemsiz ayrıntı | Kritik sınır aynı birimde | Okunur bilgi sınırı |
| Sahte ilerleme | Ölçülen tamamlanma | Gerçek durum zorunlu | Dürüst bekleme |

### İlke V70.1 — Puanın görsel ikamesi kurulmaz.

Karar: Yıldız yerine doluluk çubuğu, halka veya renk seviyesiyle genel kalite puanı üretilmez.
Gerekçe: Biçim değişse de kullanıcı aynı genel üstünlük sonucu çıkarabilir.
Bedel: Hızlı sayısal tarama hissi veren araçlar kullanılmaz.
Uygulama: Yer gerekçesi somut özellik, amaç ve önemli ödünle anlatılır.
Kontrol: Bir görselin yerleri tek boyutta derecelendirdiği algısı araştırılmalıdır.

### İlke V70.2 — Kritik sınır dekor altında kalmaz.

Karar: Fotoğraf, gradient veya cam etkisi önemli uyarı metninin okunmasını azaltamaz.
Gerekçe: Görsel atmosfer, kullanıcının gerçek dünya kararındaki engeli perdeleyebilir.
Bedel: Bazı fotoğraf üstü metin kompozisyonları kullanılmaz.
Uygulama: Mevcut opak ve kontrastlı okuma zemini korunur.
Kontrol: Yoğun ve parlak fotoğraf örneklerinde kritik metin ayrıca incelenmelidir.

### İlke V70.3 — Aciliyet süs olarak kullanılmaz.

Karar: Yanıp sönen renk, geri sayım veya kıtlık rozeti yalnız dikkat çekmek için eklenmez.
Gerekçe: Gerçek kapsam taşımayan aciliyet bağımsız karar süresini baskılar.
Bedel: Kısa vadeli tıklama çekiciliği tasarım ölçütü olmaz.
Uygulama: Zamanlı bilgi varsa mevcut somut zaman kapsamıyla okunur.
Kontrol: Uyarının gerçek karar etkisi görsel biçimden bağımsız açıklanabilmelidir.

### İlke V70.4 — Çıkış görsel olarak cezalandırılmaz.

Karar: Kapatma, vazgeçme ve erken bitiş düşük kontrast veya suçluluk görseliyle zayıflatılmaz.
Gerekçe: Kullanıcının ayrılması kabul edilmiş geçerli sonuçlardan biridir.
Bedel: Devam eylemi tek algılanabilir seçenek haline getirilemez.
Uygulama: Mevcut ret ve çıkış kontrolleri okunur hedef ve etiket taşır.
Kontrol: Devam etmek istemeyen kişinin çıkışı ilk denemede bulması incelenmelidir.

### İlke V70.5 — Görsel kalite test sonucu yerine geçmez.

Karar: Şık görünüm nedeniyle erişilebilir, doğru veya saha koşullarında güvenilir etiketi verilmez.
Gerekçe: Estetik değerlendirme bu farklı kanıt türlerini doğrulayamaz.
Bedel: Tasarım sunumunda bazı pazarlama sıfatları kullanılamaz.
Uygulama: Gerçek sınama yapılmadan yalnız hedef ve karar ifade edilir.
Kontrol: Belge ve sunumların kanıt sınırı aynı titizlikle korunmalıdır.

### İyi ve kötü karşılaştırması

| İyi örnek | Kötü örnek | Neden-sonuç | İncelenecek risk |
| --- | --- | --- | --- |
| Somut erişim sınırı | Evrensel erişilebilir rozeti | Kapsam kaybolursa yanlış güven olur | Yere genelleme |
| Tarihli temel bilgi | Offline canlı yeşil işaret | Eski kayıt güncel sanılır | Anlık durum beklentisi |
| Nötr erken bitiş | Üzgün maskot | Çıkış suçluluk üretir | Devam baskısı |
| Açık kayıt hedefi | Bulut kalkanı | Kalıcılık kapsamı büyür | Yanlış güvence |
| Durağan AI açıklaması | Düşünme tiyatrosu | İşlem yöntemi uydurulur | İç muhakeme algısı |
| Görünür geri alma | Hızla kaybolan tek bağlantı | Yavaş okuma kontrol kaybıdır | Düzeltme hakkı |

### Sınır uygulaması

İyi: Metin alanı büyüdüğünde dekor azalır ve kritik sınır korunur.
Kötü: Aynı yükseklikte kalmak için uyarı yalnız tooltip içine taşınır.
İyi: Ücretli kolaylık varsa gerçek ek iş azalması anlatılır.
Kötü: Ücretsiz kullanıcıya daha az güven veren kart malzemesi uygulanır.
İyi: Harita işareti seçimi gösterir.
Kötü: Daha parlak harita işareti işletmenin daha iyi olduğunu ima eder.
Yasak görsel tercihin yerine yeni ekran açmak bu belgenin çözüm yöntemi değildir.

### Bölüm öz eleştirisi

- **Öz eleştiri Ö70.1 — Yasak listesi tasarım ekibinde gereksiz çekingenlik yaratabilir.**
  Risk: Anlamı destekleyen yararlı görsel çözümler de otomatik elenebilir.
  Kontrol: Reddedilen tercihin somut yanlış anlamı açıkça yazılmalıdır.
  Kabul sınırı: Beğeni farklılığı ürün yasağı gibi sunulmaz.

- **Öz eleştiri Ö70.2 — Genel puansız dil daha fazla okuma isteyebilir.**
  Risk: Kullanıcı seçenek farkını hızlı bulamayabilir.
  Kontrol: Ortak ölçütlerin taranabilirliği ve kısa somut gerekçe değerlendirilmelidir.
  Kabul sınırı: Okuma maliyeti yeni gizli puan sistemiyle çözülmez.

- **Öz eleştiri Ö70.3 — Baskısız çıkış devam eylemini yeterince belirgin bırakmayabilir.**
  Risk: Kullanıcı ne yapabileceğini anlamadan ayrılabilir.
  Kontrol: Ana eylem ve çıkışın birlikte bulunabilirliği incelenmelidir.
  Kabul sınırı: Ana eylem güçlendirilirken ret yolu görünmezleştirilmez.

## Apple vs Google Yaklaşımı

Bölüm kimliği: V71.
Karşılaştırma bütün Apple ve Google ürünlerinin güncel özellik envanteri değildir.
Resmî rehberlerde doğrulanan sınırlı ilkeler ile Şamandıra yorumu açıkça ayrılır.
Kaynaklar 14 Eylül 2026 tarihinde kontrol edilmiştir; rakip iç mimarisi hakkında iddia kurulmaz.

### Belgelenmiş referanslar

Apple, geri bildirimin önemine uygun verilmesini ve durum bilgisinin bağlam içinde sunulmasını önerir. [Apple Feedback](https://developer.apple.com/design/human-interface-guidelines/feedback).
Apple, jestlerin tanıdık işlemesini ve farklı giriş yollarını desteklemeyi önerir. [Apple Gestures](https://developer.apple.com/design/human-interface-guidelines/gestures).
Google'ın Android renk rehberi tutarlı semantik rolleri, kontrastı ve renk dışı ipuçlarını vurgular. [Android renk rehberi](https://developer.android.com/design/ui/mobile/guides/styles/color?hl=en).
Bu üç cümle kaynak özetidir; aşağıdaki tasarım sonuçları Şamandıra'nın kendi değerlendirmesidir.

| Karşılaştırma ekseni | Apple kaynak vurgusu | Google kaynak vurgusu | Şamandıra yorumu |
| --- | --- | --- | --- |
| Geri bildirim | Önemle uyumlu karşılık | Anlamlı semantik ifade | Rutin durum sakin, kritik sınır açık |
| Etkileşim | Tanıdık jest ve alternatif giriş | Renk dışı eylem ipucu | Görünür eylem tek başına anlaşılır |
| Görsel tutarlılık | Bağlamla ilişkili durum | Rolün tutarlı kullanımı | Ortak durum sözlüğü |
| Okunabilirlik | Çok kanallı erişim | Kontrast ve ton ayrımı | Opak, okunur temel yüzey |
| Platform farkı | Yerel beklenti | Android rol ve yüzey yaklaşımı | Aynı anlam, uygun yerel biçim |
| Özgünlük sınırı | Rehber öğrenilir | Rehber öğrenilir | Tescilli görünüm kopyalanmaz |

### İlke V71.1 — Kaynaktan yöntem alınır.

Karar: Referans ürünlerden ekran şablonu yerine ilkenin hangi problemi çözdüğü öğrenilir.
Gerekçe: Şamandıra'nın karar ve kanıt yükümlülüğü başka ürünlerin amacıyla aynı değildir.
Bedel: Tanınmış bir görünümü hızla kopyalayarak benzer kalite algısı üretme yolu kullanılmaz.
Uygulama: Geri bildirim önemi mevcut durum rollerine çevrilir.
Kontrol: Her alınan dersin Şamandıra'daki somut işi açıklanmalıdır.

### İlke V71.2 — Tanıdık etkileşim korunur.

Karar: Marka farkı yaratmak için geri, dokunma veya kaydırma beklentisi yeniden tanımlanmaz.
Gerekçe: Kullanıcı becerisinin tekrar kullanılması öğrenme yükünü azaltır.
Bedel: Bazı kontroller Şamandıra'ya özgü görünmeyebilir.
Uygulama: Özgünlük iddia, sınır ve baskısız kontrolün birlikte okunmasından gelir.
Kontrol: Platform bilgisi olan kullanıcı temel kontrolün anlamını yanlış tahmin etmemelidir.

### İlke V71.3 — Renk rolü marka rengine indirgenmez.

Karar: Semantik durumlar mevcut renk rollerini korur; tek accent bütün anlamlara yayılmaz.
Gerekçe: Aynı renk seçim, başarı ve belirsizlik için kullanıldığında anlamlar karışabilir.
Bedel: Marka rengi her bileşenin baskın rengi olmaz.
Uygulama: Harita seçimi ile hata farklı semantik ipuçlarıyla anlaşılır.
Kontrol: Renkler kaldırıldığında durum metin ve işaretle yine ayırt edilmelidir.

### İlke V71.4 — Geri bildirim önemle orantılıdır.

Karar: Rutin kaydetme karşılığı ile kritik karar sınırı aynı dikkat düzeyinde gösterilmez.
Gerekçe: Her durum yüksek vurgu taşırsa gerçekten önemli değişim kaybolur.
Bedel: Bazı küçük sonuçlar görsel olarak daha sakin kalır.
Uygulama: Mevcut kritik sınır kalıcı okuma biriminde; rutin teyit uygun durum rolündedir.
Kontrol: Kullanıcının hangi değişimin kararı etkilediğini ayırt etmesi değerlendirilmelidir.

### İlke V71.5 — Kalite iddiası referans adından gelmez.

Karar: Apple veya Google ilkesine yakınlık, erişilebilirlik veya kullanılabilirlik sonucu sayılmaz.
Gerekçe: Rehberden öğrenmek uygulanmış tasarımın gerçek görevde başarılı olduğunu kanıtlamaz.
Bedel: Karşılaştırma marka otoritesiyle tasarımı haklı çıkaramaz.
Uygulama: Her uyarlama mevcut kullanıcı senaryolarıyla ayrıca değerlendirilir.
Kontrol: Kaynak adı gerekçenin yerini aldığında karar açıklaması yeniden yazılmalıdır.

### Yaklaşım ve tercih karşılaştırması

| Şamandıra tercihi | Öğrenilen yöntem | Kullanılmayan çıkarım | Neden |
| --- | --- | --- | --- |
| Sade durum metni | Bağlam içinde geri bildirim | Her Apple ekranı sadedir | Kaynak kapsamı sınırlıdır |
| Rol bazlı renk | Semantik tutarlılık | Her Google ürünü aynı palettedir | Ürün genellemesi yapılmaz |
| Görünür jest alternatifi | Çoklu giriş | Yerel jestler tek yoldur | Temel hak korunur |
| Opak okuma zemini | Erişilebilir karşılık | Cam etki kalite şartıdır | Okuma önceliklidir |
| Kısa hareket | Durum ilişkisi | Rakip süreleri kopyalanır | Mevcut süreler bağlayıcıdır |
| Yerel geri beklentisi | Tanıdıklık | Yeni navigasyon gerekir | Akış değişmez |

### İyi ve kötü örnekler

İyi: Apple geri bildirim ilkesinden rutin teyidin bağlama yakın olması öğrenilir.
Kötü: Apple adı kullanılarak her yüzeye saydamlık eklenmesi savunulur.
İyi: Google renk yaklaşımından rol ve kontrast denetimi öğrenilir.
Kötü: Varsayılan bir paletin Şamandıra'nın kanıt anlamını otomatik çözeceği varsayılır.
İyi: Referans ilke, kaynak sınırı ve yerel yorum birlikte yazılır.
Kötü: İncelenmeyen güncel uygulama ekranları hakkında kesin kalite genellemesi yapılır.
Bu karşılaştırma iki şirketi sıralamaz; görsel kararın dayanağını görünür kılar.

### Bölüm öz eleştirisi

- **Öz eleştiri Ö71.1 — Rehberlerden seçilen az sayıda ilke karşılaştırmayı daraltır.**
  Risk: Okur bunu bütün ürün stratejisinin karşılaştırması sanabilir.
  Kontrol: Kaynak kapsamı ve Şamandıra yorumu ayrımı görünür tutulmalıdır.
  Kabul sınırı: Dar kaynaklar genel rakip üstünlüğü iddiasına dönüştürülmez.

- **Öz eleştiri Ö71.2 — Tanıdık kontroller marka ayrışmasını zayıflatabilir.**
  Risk: Görsel dil genel bir platform kabuğu gibi algılanabilir.
  Kontrol: Logo gizliyken iddia ve sınır hiyerarşisinin tanınması araştırılmalıdır.
  Kabul sınırı: Ayrışma temel etkileşim alışkanlığını bozarak sağlanmaz.

- **Öz eleştiri Ö71.3 — Kaynaklar zaman içinde değişebilir.**
  Risk: Gelecekte eski bir rehber cümlesi güncel zorunluluk gibi okunabilir.
  Kontrol: Yeni sürüm incelemesinde bağlantı ve kapsam yeniden kontrol edilmelidir.
  Kabul sınırı: Kaynak güncellemesi kabul edilmiş Şamandıra kararını sessizce değiştirmez.

## Airbnb vs Booking Yaklaşımı

Bölüm kimliği: V72.
Bu karşılaştırma iki ürünün bütün ekranlarını veya dönüşüm performansını değerlendirmez.
Belgelenmiş fiyat açıklığı örnekleri, görsel bilgi hiyerarşisi açısından sınırlı olarak ele alınır.
Şamandıra için rezervasyon, fiyat motoru veya ticari akış açılmaz.

### Belgelenmiş referanslar

Airbnb'nin 21 Nisan 2025 duyurusu, arama sonuçlarında ücretleri içeren toplamın vergi öncesi kapsamla gösterilmesini açıklar; bazı ülke ve bölgelerde gösterilen toplamın vergileri de içerdiğini belirtir. [Airbnb toplam fiyat duyurusu](https://news.airbnb.com/total-price-display-is-now-standard-globally).
Booking.com Demand belgeleri, sipariş önizlemesinde koşullu veya hesaplanamayan ek tutarların açık anlatılmasını ve ilgili tutarın toplam olmadığının belirtilmesini ister. [Booking fiyat gösterimi](https://developers.booking.com/demand/docs/accommodations/display-prices).
Bu örnekler aynı ülke, kullanıcı veya fiyat nesnesini tanımlamaz; hukuki karşılaştırma yapılmaz.
Şamandıra yorumu: Büyük görünen sayı kadar o sayının kapsamı da okunabilir olmalıdır.

| Karşılaştırma ekseni | Airbnb belgeli örneği | Booking belgeli örneği | Şamandıra yorumu |
| --- | --- | --- | --- |
| Tutarın görünürlüğü | Aramada toplam yaklaşımı | Fiyat türüne uygun sunum | Bilinen tutarın kapsamı açık |
| Kapsam sınırı | Vergi öncesi kapsam ve ülke/bölge istisnası | Sipariş önizlemesinde koşullu ücret açıklığı | Bilinmeyen toplam sayılmaz |
| Karşılaştırma | Erken fiyat görünürlüğü | Ayrıntının doğru nitelenmesi | Aynı ölçütte kıyas |
| Görsel hiyerarşi | Toplam bilgisi öne çıkabilir | Ek kapsam görünür kalmalı | Sayı sınırını gölgeleyemez |
| Ürün kapsamı | Konaklama duyurusu | Demand fiyat belgesi | Yeni rezervasyon akışı yok |
| Kanıt sınırı | Şirket duyurusu | Geliştirici sunum kuralı | Güncel ekran genellemesi yok |

### İlke V72.1 — Sayı ile kapsam birlikte okunur.

Karar: Mevcut maliyet ve süre bilgisinin kapsamı sayıyla aynı karar birimindedir.
Gerekçe: Büyük sayı ve küçük dipnot farklı zihinsel öncelik yaratabilir.
Bedel: Kapsamı uzun tutarlarda görsel alan gereksinimi artar.
Uygulama: Bilinen maliyet toplamın bütün parçaları bilinmiş gibi görünmez.
Kontrol: Kullanıcı hangi parçanın dahil olduğunu kendi sözüyle açıklayabilmelidir.

### İlke V72.2 — Görsel çekicilik kıyas temelini bozmaz.

Karar: Bir kartın daha büyük fotoğrafı veya daha parlak fiyatı onu daha uygunmuş gibi ayrıcalıklı kılmaz.
Gerekçe: Görsel baskınlık ortak ölçütte karar vermeyi zorlaştırabilir.
Bedel: Pazarlama etkisi yüksek asimetriler sınırlanır.
Uygulama: Mevcut kart ailesinde ortak bilgi rolleri karşılaştırılabilir kalır.
Kontrol: Fotoğraf kaldırıldığında somut seçenek farkı anlaşılmalıdır.

### İlke V72.3 — Detay yoğunluğu bağlamla sınırlıdır.

Karar: Görsel dil gerekli kapsamı taşır; kullanılmayan işlem alanlarını çoğaltmaz.
Gerekçe: Rezervasyon ürününün yoğunluğu karar destek ürününe otomatik aktarılmaz.
Bedel: Daha fazla ticari alan gösterme kapasitesi kullanılmaz.
Uygulama: Otel içerikleri kabul edilmiş yer kararının bilgi sınırında kalır.
Kontrol: Her görünür ayrıntının mevcut kullanıcının karar sorusuna etkisi açıklanmalıdır.

### İlke V72.4 — Belirsizlik karşılaştırmayı dürüstçe sınırlar.

Karar: Bilinmeyen fiyat veya süre boşluğu uygun renk, metin ve kapsamla görünürdür.
Gerekçe: Boş alanı nötrleştirip gizlemek kullanıcının bilinmeyeni sıfır sanmasına yol açabilir.
Bedel: Bazı seçeneklerin görsel karşılaştırması daha az pürüzsüz olur.
Uygulama: Sayı yoksa mevcut bilgi açığı metni korunur; tahmini sayı uydurulmaz.
Kontrol: Bilinmeyen ile ücretsiz veya uygulanamaz durum ayrımı incelenmelidir.

### İlke V72.5 — Kaynak örneği marka stereotipine dönüşmez.

Karar: Airbnb yalnız sıcak, Booking yalnız yoğun gibi doğrulanmamış evrensel etiketler kullanılmaz.
Gerekçe: Ürün varyantları ve zaman içindeki değişiklikler bu genellemeleri geçersiz kılabilir.
Bedel: Basit ama yüzeysel bir rakip hikâyesi kurulamaz.
Uygulama: Karşılaştırma belgelenmiş örnekle sınırlı tutulur; yerel yorum açıkça adlandırılır.
Kontrol: Kaynağın desteklemediği her rakip iddiası metinden çıkarılmalıdır.

### Yerel tasarım seçeneklerinin karşılaştırması

| Şamandıra seçeneği | İyi kullanım | Kötü kullanım | Neden |
| --- | --- | --- | --- |
| Fotoğraf ağırlığı | Yer kimliğini açıklar | Somut sınırı gölgeler | Atmosfer kanıt değildir |
| Sayı ağırlığı | Bilinen süreyi okunur kılar | Kapsamı dipnota iter | Eksik toplam sanılır |
| Bilgi yoğunluğu | Karar farklarını taşır | İşlem alanlarını çoğaltır | Akış kapsamı aşılır |
| Boşluk | Grupları ayırır | Sınırı uzakta bırakır | İlişki kaybolur |
| Renk | Eylem ve durumu ayırır | Fiyatı kaliteye dönüştürür | İkinci karar motoru olur |
| Belirsizlik | Somut eksiği söyler | Soluk tire gösterir | Yokluk yanlış okunur |

### İyi ve kötü örnekler

İyi: Süre yanında yürüyüş, bekleme ve kalış kapsamı kabul edilmiş metinle anlaşılır.
Kötü: Sadece en küçük süre büyük yazılarak gün yükü hafif gösterilir.
İyi: Bilinen maliyet, bilinmeyen ek parçayı gizlemeden sunulur.
Kötü: Bilinmeyen ücret boş bırakılıp toplam eksiksizmiş gibi görünür.
İyi: Gerçek yer fotoğrafı karar metnini destekler.
Kötü: Fotoğrafın cazibesi bütün yer türleri için uygunluk kanıtı yapılır.
Bu bölüm fiyat, rezervasyon hakkı veya güncel müsaitlik bilgisi üretmez.

### Bölüm öz eleştirisi

- **Öz eleştiri Ö72.1 — Fiyat açıklığı örnekleri genel görsel kaliteyi dar temsil eder.**
  Risk: Okur iki ürünün bütün tasarım dili karşılaştırılmış sanabilir.
  Kontrol: Başlangıç kapsamı ve tablodaki kaynak türleri birlikte okunmalıdır.
  Kabul sınırı: Belgesiz ekran düzeni veya performans iddiası eklenmez.

- **Öz eleştiri Ö72.2 — Sayı ve kapsamı birlikte tutmak küçük ekranda yoğunluk yaratabilir.**
  Risk: Toplam bilgi taraması yavaşlayabilir.
  Kontrol: Sayı, birim ve kapsamın birlikte okunması büyütülmüş metinle değerlendirilmelidir.
  Kabul sınırı: Alan açmak için kritik kapsam dipnota sürülmez.

- **Öz eleştiri Ö72.3 — Fotoğraf baskınlığını sınırlamak turistik çekiciliği azaltabilir.**
  Risk: Yerler soyut bilgi kartları gibi algılanabilir.
  Kontrol: Gerçek fotoğrafın kimlik ve atmosfer katkısı ayrı incelenmelidir.
  Kabul sınırı: Çekicilik, kanıtsız özellik veya yüksek kalite imasıyla artırılmaz.

## Material vs Cupertino Karşılaştırması

Bölüm kimliği: V73.
Cupertino burada Apple platformlarının tanıdık görsel ve etkileşim geleneği için kullanılan kısa addır.
Bir framework, bileşen kütüphanesi veya uygulama teknolojisi seçimi yapılmaz.
Karşılaştırmanın sonucu Şamandıra'nın kabul edilmiş ortak anlam çekirdeğini korumaktır.

### Belgelenmiş referanslar

Google'ın renk rehberi yüzey ve içerik rollerinin eşleşmesini, açık ve koyu temanın ayrı tonlarını açıklar. [Android renk rehberi](https://developer.android.com/design/ui/mobile/guides/styles/color?hl=en).
Android geri rehberi sistem kenar alanlarıyla çatışan sürükleme hedeflerinden kaçınmayı söyler. [Android predictive back rehberi](https://developer.android.com/design/ui/mobile/guides/patterns/predictive-back?hl=en).
Apple jest rehberi tanıdık hareketlere karşılığı korumayı ve alternatif giriş sağlamayı önerir. [Apple Gestures](https://developer.apple.com/design/human-interface-guidelines/gestures).
Şamandıra yorumu: Yerel tanıdıklık ile ortak karar anlamı birlikte korunabilir.

| Eksen | Material tarafında öğrenilen | Cupertino tarafında öğrenilen | Şamandıra görsel kararı |
| --- | --- | --- | --- |
| Renk | Anlamsal rol eşleşmesi | Platformda tanınan durum ifadesi | Mevcut rol paleti korunur |
| Yüzey | Tonla ilişki açıklama | Bağlam ve katman okunması | Opak temel, gerekli sınır |
| Geri | Sistem kenarına saygı | Tanıdık hareket beklentisi | Mevcut geri ilişkisi korunur |
| Giriş | Görünür durum ipuçları | Alternatif girişler | Jest tek yol olmaz |
| Tema | Ayrı ton değerleri | Yerel tercihe uyum yorumu | Aynı bilgi, farklı görünürlük |
| Kimlik | Sistemden yöntem alma | Sistemden yöntem alma | Tescilli görünüm kopyalanmaz |

### İlke V73.1 — Ortak anlam platform görünümünden önce gelir.

Karar: Aynı iddia, bilinmeyen ve işlem sonucu her kanalda aynı kapsamı taşır.
Gerekçe: Platform görseli kullanıcıya farklı doğruluk veya hak düzeyi sunamaz.
Bedel: Hazır yerel örnekler ürün metnine bire bir uygulanamayabilir.
Uygulama: Aynı kayıt hedefi hem Android hem iOS görünümünde açık kalır.
Kontrol: Kanallar arası kıyasta anlam kaybı ayrıca değerlendirilmelidir.

### İlke V73.2 — Yerel davranış marka uğruna değiştirilmez.

Karar: Sistem geri, klavye ve erişilebilir giriş beklentileri kabul edilmiş davranışla korunur.
Gerekçe: Kullanıcıların mevcut becerileri temel kullanım maliyetini azaltır.
Bedel: Kontrol biçimleri platformlar arasında bire bir aynı olmayabilir.
Uygulama: Mevcut geri kontrolü platformun tanıdık ifadesini taşıyabilir.
Kontrol: Görsel birlik için davranışın sessizce değişmediği incelenmelidir.

### İlke V73.3 — Malzeme rolü moda seçimi değildir.

Karar: Yüzey, blur ve gölge yalnız okunur görev ilişkisi sağladığında kullanılır.
Gerekçe: Bir platform trendini bütün karta taşımak harita üstü okunurluğu zayıflatabilir.
Bedel: Dönemin en belirgin efektleri ürünün her alanında görünmez.
Uygulama: Mevcut opak temel korunur; cam etki zorunlu marka sembolü olmaz.
Kontrol: Efekt kaldırıldığında katman ve kontrol sınırı hâlâ anlaşılmalıdır.

### İlke V73.4 — Boyutlar adlardan bağımsız doğrulanır.

Karar: Bir kontrolün platform adı, dokunma hedefi ve odak görünürlüğü incelemesini kaldırmaz.
Gerekçe: Yerel görünüme benzeyen özel uygulama gerekli erişim sonuçlarını sağlamayabilir.
Bedel: Tanıdık bileşenlerde de görsel denetim gerekir.
Uygulama: Mevcut 48 ve 44 mantıksal birim ürün hedefleri korunur.
Kontrol: Görsel ikon boyu ile etkileşim alanı ayrı değerlendirilmelidir.

### İlke V73.5 — Uyarlama yeni varyant enflasyonu yaratmaz.

Karar: Platform farkı gerçek kullanım ihtiyacıyla sınırlanır; her parça iki bağımsız sistem olmaz.
Gerekçe: Gereksiz ayrışma aynı durumun farklı yorumlanması riskini artırır.
Bedel: Bazı platforma özgü dekoratif seçenekler kullanılmaz.
Uygulama: Alan bileşeninin iddia, sınır ve durum sözleşmesi ortaktır.
Kontrol: Yeni varyantın hangi somut platform ihtiyacını karşıladığı yazılmalıdır.

### Karar karşılaştırması

| Seçenek | Olası yarar | Olası bedel | Bu belgede sınır |
| --- | --- | --- | --- |
| Her yerde aynı biçim | Kolay görsel bakım | Yerel beklenti kaybı | Zorunlu değil |
| Her yerde bütünüyle yerel biçim | Tanıdık kontrol | Ortak anlam dağılması | Alan sözleşmesi ortak |
| Yoğun platform efekti | Döneme yakın görünüm | Okunurluk ve maliyet | Koşulsuz kullanılmaz |
| Ortak semantik roller | Tutarlı durum | Rol eşleme emeği | Kabul edilmiş temel |
| Sistem sans | Yerel okuma uyumu | Font ayrışması | Mevcut tercih korunur |
| Statik hareket eşdeğeri | Erişim eşitliği | Ek durum açıklığı | Temel zorunluluk |

### İyi ve kötü örnekler

İyi: Yerel geri işareti kullanılırken aynı durak ve sorgu bağlamına dönüş korunur.
Kötü: Her platformda aynı görünüm için geri eylemi ana sayfaya gönderilir.
İyi: Koyu tema mevcut semantik rolün okunur tonuyla çalışır.
Kötü: Bir platformun örnek rengi bütün yüzeylerde kontrast kontrolsüz uygulanır.
İyi: Tanıdık sheet, mevcut tek etkin modal kuralına uyar.
Kötü: Yerel örneklerde görüldüğü gerekçesiyle iç içe yeni modal görevler açılır.
Karşılaştırma, hangi kütüphanenin kullanılacağına veya ekranın nasıl kurulacağına karar vermez.

### Bölüm öz eleştirisi

- **Öz eleştiri Ö73.1 — Ortak çekirdek ve yerel biçim arasındaki sınır yoruma açıktır.**
  Risk: Ekipler aynı gerekçeyle farklı görsel durum sözlükleri kurabilir.
  Kontrol: Her uyarlamada korunan anlam ve değişen biçim açık kaydedilmelidir.
  Kabul sınırı: Platform farkı bilgi kapsamı farkına dönüşemez.

- **Öz eleştiri Ö73.2 — Platform trendlerinden uzak durmak eski görünme riski taşır.**
  Risk: Kullanıcı görsel sakinliği bakım eksikliği sanabilir.
  Kontrol: Güncellik algısı ile görev başarısı ayrı değerlendirilmelidir.
  Kabul sınırı: Yeni görünme uğruna kontrast ve statik eşdeğer terk edilmez.

- **Öz eleştiri Ö73.3 — Sistem sans ailesi kanallar arasında farklı satır kırılımları üretir.**
  Risk: Aynı içerikte görsel hiyerarşi ve kart ritmi değişebilir.
  Kontrol: Uzun adlar ve kapsam cümleleri desteklenen platformlarda incelenmelidir.
  Kabul sınırı: Satır farkı kritik bilginin kesilmesiyle giderilmez.

## Belge İlişkileri ve Görsel Doğrulama Kaydı

Bu bölüm, görsel kararların kaynak ve kontrol sınırını birlikte kaydeder.
Mevcut uygulama için yeni tasarım veya uygulama kabulü verilmez.
Kaynaklardaki eski performans raporları bu yeni dilin test sonucu olarak kullanılamaz.
Metinsel inceleme, gerçek cihazda okunabilirlik ve yardımcı teknoloji doğrulamasının yerini tutmaz.

### Sayısal görsel değerlerin kontrolü

Aşağıdaki oranlar 10 Design System'in aynen korunan opak sRGB renklerinden yeniden hesaplanmıştır.
Hesaplama, W3C'nin bağıl parlaklık ve kontrast yaklaşımını kullanır.
Üç ondalıklı gösterim okunabilirlik içindir; eşik kabulü yuvarlanmış değere göre yapılmaz.
Bu tablo yeni renk önermez ve kontrastı yetmeyen eşleşmeyi kabul edilebilir ilan etmez.
Renkli metnin tabloda bulunmayan bir zeminde kullanılabileceği varsayılmaz.
Alfa, fotoğraf, gradient veya harita arka planı bu opak çift hesaplarına dahil değildir.
Güçlü sınır oranı kontrolün gerekli algı sınırı içindir; küçük metin rengi olarak kullanma izni vermez.
Gerçek harf çizimi, cihaz parlaklığı ve dış ortam yansıması ayrıca incelenmelidir.

| Tema | Rol çifti | Ön plan / arka plan | Hesaplanan oran |
| --- | --- | --- | --- |
| Açık | Birincil metin/sayfa | #202B28 / #F6F7F4 | 13,585:1 |
| Açık | İkincil metin/iç yüzey | #4C5B54 / #EEF1ED | 6,290:1 |
| Açık | Caption/iç yüzey | #5C6962 / #EEF1ED | 5,049:1 |
| Açık | Caption/üst yüzey | #5C6962 / #FFFFFF | 5,750:1 |
| Açık | Eylem metni/eylem zemini | #FFFFFF / #185A48 | 8,093:1 |
| Açık | Güçlü sınır/iç yüzey | #718078 / #EEF1ED | 3,644:1 |
| Açık | Güçlü sınır/üst yüzey | #718078 / #FFFFFF | 4,149:1 |
| Açık | Hata/üst yüzey | #A52E34 / #FFFFFF | 6,907:1 |
| Açık | Uyarı/üst yüzey | #805400 / #FFFFFF | 6,591:1 |
| Açık | Bilgi/üst yüzey | #245B83 / #FFFFFF | 7,243:1 |
| Koyu | Birincil metin/sayfa | #F0F5EF / #111916 | 16,188:1 |
| Koyu | İkincil metin/iç yüzey | #C0CEC2 / #15201B | 10,244:1 |
| Koyu | Caption/iç yüzey | #A6B6A9 / #15201B | 7,881:1 |
| Koyu | Caption/üst yüzey | #A6B6A9 / #25342B | 6,160:1 |
| Koyu | Eylem metni/eylem zemini | #102B20 / #8DD9B5 | 9,165:1 |
| Koyu | Güçlü sınır/iç yüzey | #829688 / #15201B | 5,315:1 |
| Koyu | Güçlü sınır/üst yüzey | #829688 / #25342B | 4,155:1 |
| Koyu | Hata/üst yüzey | #FFADB0 / #25342B | 7,388:1 |
| Koyu | Uyarı/üst yüzey | #EDC879 / #25342B | 8,187:1 |
| Koyu | Bilgi/üst yüzey | #9ACFF2 / #25342B | 7,840:1 |

Renkler belge boyunca aynı rolü korur.
Renk dışında gerekli metin, işaret ve odak karşılığı bulunur.
Bu hesaplar doğruysa bile bütün ürünün WCAG AA uyumlu olduğu sonucu çıkmaz.
Görsel dilin diğer ölçüleri 10 belgesindeki başlangıç değerlerinin aynen kullanımıdır.

### Mevcut bileşen ailelerine izlenebilirlik

| Görsel konu | Kabul edilmiş dayanak | Korunan karar | Görsel inceleme sorusu |
| --- | --- | --- | --- |
| Kart | 10 B02–B04 | Yer ve günlük rota anatomisi | Gerekçe ile sınır birlikte okunuyor mu? |
| Arama | 10 B07; 11 E03 | Keşfet ile ortak sonuç otoritesi | Ad sonucu öneri sanılıyor mu? |
| Buton ve CTA | 10 B11–B12 | Mevcut eylem ve geri dönüş | Etiket ve kapsam aynı anda anlaşılır mı? |
| Filtre ve chip | 10 B06,B08 | Taslak ve uygulanan koşul ayrımı | Seçim yalnız renge mi bağlı? |
| Etiket ve durum işareti | 10 B09–B10 | Kanıtsız güven rozeti yok | Durum sınıfı yer kalitesi sanılıyor mu? |
| Bottom Sheet | 10 B19; 11 ilgili görev | Mevcut katman ve kapanış | Eylem klavye veya kenar altında mı? |
| Modal ve dialog | 10 B20 | Tek etkin modal görevi | Arka görev yanlış etkin görünüyor mu? |
| Toast | 10 B22 | Geçici, kritik olmayan teyit | Sonuç kapsamı okunuyor mu? |
| Snackbar | 10 B23 | Geçici eylem; kalıcı hak ayrı | Geri alma yalnız süreye mi bağlı? |
| Bildirim | 10 B24; 11 E14 | Gerçek olay, okundu/çözüldü ayrımı | Görsel durum yanlış çözüm ima ediyor mu? |
| Loading ve skeleton | 10 B25–B26 | Gerçek bekleme ve statik iskelet | Sahte yer veya yüzde üretildi mi? |
| Boş, hata ve offline | 10 B27–B29; 11 E24–E26 | Ayrı neden ve durumlar | Birbirinin görünümüyle karışıyor mu? |
| Başarı | 10 B30 | Teyitli işlem ve hedef kapsamı | Genel güven hükmü çıkarılıyor mu? |
| Harita | 10 B31; 11 §31,40 | Aynı kümenin yardımcı görünümü | Marker, liste ve filtre aynı mı? |
| Fotoğraf | 10 B32 | Gerçek yer ve doğru kapsam | Kırpma fiziksel sınırı gizliyor mu? |
| İkon | 10 B33 | Tek aile, açık eylem, metinsel eşdeğer | Görsel kutu ile hedef karışıyor mu? |
| Navigation ve Tab Bar | 10 B35–B36; 11 §31 | Kabul edilmiş navigasyon | Yeni portal ima ediliyor mu? |
| İddia ve AI | 10 B39,B44; 05 | Bilgi/kanıt/karar yetkisi ayrı | Yardımcı açıklama onay gibi mi? |
| Rota düzenleme | 10 B40; 06; 11 E08 | Taslak ve değerlendirme ayrı | Yeni sıraya eski olumlu özet bağlı mı? |
| Kayıt ve Bir İz | 10 B41–B42; 09 | Niyet, ziyaret, katkı ayrı | Kalp veya statü ile anlam kayıyor mu? |
| Paylaşım | 10 B43; 11 §46 | Özel taslak ve yayın kapsamı ayrı | Özel içerik görünümle sızıyor mu? |
| Premium | 10 B45; 09 | Temel hak ve doğruluk ortak | Görsel özen üyeliğe göre değişiyor mu? |
| Admin | 10 B46; 11 E27–E30 | İç yetki ve inceleme ayrı | Ticari vurgu kanıt sırasını bozuyor mu? |

### Diğer referans dosyalarının rolü

Tarihsel uygulama ve veri belgeleri ürünün bağlamını açıklar.
Bu belgelerdeki komut, teknoloji veya görev paketleri bu iş için yürütme talimatı olarak devralınmaz.
Eski görsel inceleme raporları kendi tarih ve kapsamlarında korunur.
Üretim logları ve veri sayıları görsel kalite rozetine çevrilmez.

| Referans grubu | İnceleme amacı | Görsel dile aktarılan sınır |
| --- | --- | --- |
| plan/00_brief_eki.md ve plan/04_marka_ve_tema.md | Marka varlığı ve tarihsel yön | Kilitli logo, doğru marka yazımı, ağır tema yasağı |
| plan/tasarim/yon.md, yon-v2.md, yon-v3.md | Görsel karar geçmişi | Ekranlar yeniden tasarlanmaz; güncel docs ile çelişmeyen kilitler korunur |
| plan/tasarim/gorsel-kunye.md | Fotoğraf ve atmosfer ayrımı | Hero atmosferi gerçek yer kanıtı sayılmaz |
| plan/logo/arastirma.md | Logo araştırması ve iptal edilmiş yönler | Eski konseptler yeniden seçilmez |
| plan/tasarim/p4-rev-dogrulama/rapor.md | Önceki hero test kapsamı | Tarihsel başarı yeni dilin testi değildir |
| plan/tasarim/p5-g-dogrulama/rapor.md | Önceki harita ve performans sınırları | Belgelenmiş başarısız kapılar saklanmaz; yeni doğrulama sayılmaz |
| dokumanlar/kategori_taksonomisi.md | Yer türleri ve fiziksel özellik sözlüğü | Görsel kategori yeni uygunluk ölçütü yaratmaz |
| dokumanlar/veri_sozlugu.md | Veri alanlarının anlamı | Boş veri olumlu özellik gibi çizilmez |
| dokumanlar/bilgi_mimarisi.md | Eski belge yolu taşıma kaydı | İkinci bilgi mimarisi otoritesi değildir |
| plan/01_urun_analizi_ve_strateji.md | Tarihsel ürün ve iş hedefleri | Ticari hedef güncel karar görünümünü değiştirmez |
| plan/02_seo_mimarisi.md | Tarihsel adres ve içerik kapsamı | Görsel metin SEO gerekçesiyle puan otoritesi kurmaz |
| plan/03_cursor_araclari_kurulumu.md | Tarihsel araç ve doğrulama bağlamı | Araç veya hazır kütüphane görsel kararın yerine geçmez |
| plan/05_deployment_oracle.md | Operasyon kapsamı | Bu belge dağıtım veya yayın talimatı değildir |
| plan/06_mobil_ve_harita.md | Mobil ve marker geçmişi | Halka + nokta kilidi ve harita atfı korunur |
| plan/07_cursor_talimatlari.md, BASLA.md, BRIF.md | Tarihsel iş ve başlangıç kayıtları | Eski görev paketleri bu çalışma sırasında uygulanmaz |
| veri/README.md ve veri/cikti/raporlar altındaki Markdown raporlar | Eksik alan ve kimlik eşleştirme bağlamı | Fotoğrafsız/eksik içerik gerçek ve eşit bir durumdur |
| sunucu/README.md, sunucu/api/README.md, sunucu/rota_motoru/README.md | Uygulama ve veri sorumluluğu | Görsel sunum ikinci rota veya karar motoru olmaz |
| site/README.md ve altyapi/README.md | Mevcut uygulama durumu | Hedef görsel dil uygulanmış özellik gibi anlatılmaz |

### Bağlı belgeler

[00 Ürün Felsefesi](../00-product/00-urun-felsefesi.md), [01 Bilgi Mimarisi](../00-product/01-bilgi-mimarisi.md) ve [02 Product Language](../00-product/02-product-language.md) amaç ve ortak anlamı belirler.
[03 Karar Motoru](../00-product/03-karar-motoru.md), [04 Sistem Mimarisi](../00-product/04-sistem-mimarisi.md) ve [05 AI Bilgi Motoru](../04-ai/05-ai-bilgi-motoru.md) bilgi, karar ve sunum yetkisini ayırır.
[06 Akıllı Rota Motoru](../00-product/06-akilli-rota-motoru.md) ile [07 UX Karar Akışları](../02-ux/07-ux-karar-akislari.md) mevcut kullanıcı işini ve geri dönüşü korur.
[08 Tasarım İlkeleri](./08-tasarim-ilkeleri.md) ve [09 Ürün Ekosistemi](../09-business/09-urun-ekosistemi.md) kullanıcı iradesi, eşitlik ve ticari sınırı belirler.
[10 Design System](./10-design-system.md) bütün sayısal temellerin ve bileşen sözleşmelerinin otoritesidir.
[11 Ekran Mimarisi](./11-ekran-mimarisi.md) ekranların görev, bilgi sırası ve ilişkisini korur.
[Proje README](../../README.md) ve [dokümantasyon dizini](../README.md) depo bağlamıdır.

### Etkilediği belgeler

Görsel rol ve durum kataloğu planlanandır; bu görevde oluşturulmuş ayrı katalog yoktur.
UX ve erişilebilirlik doğrulama planı planlanandır; bu metin o çalışmanın sonucu değildir.
Web, mobil ve tablet kanal kabul çalışmaları planlanandır; mevcut ekranlar bu görevde değiştirilmemiştir.
İç operasyon görsel inceleme kaydı planlanandır; admin yetki veya veri modeli burada genişletilmez.
Bu etkiler bağlı kaynakları geriye dönük değiştirme izni değildir.

### Bundan sonra okunması gereken belge

Uygulama düşünüldüğünde önce ilgili görev için 11 Ekran Mimarisi ve 10 Design System birlikte okunmalıdır.
Rota için 06, AI ve kanıt için 05, kayıt/Premium için 09 ilgili otorite olarak ayrıca okunmalıdır.
Sonraki yeni çalışma mevcut planlanan UX ve erişilebilirlik doğrulama planıdır.
Bu okuma ilişkisi kod, ekran üretimi, commit, push veya yayın talimatı değildir.
Aşağıdaki Visual Language Review tamamlanan metnin eleştirel inceleme çerçevesidir.

### Bölüm sonu öz eleştiri

- **Öz eleştiri Ö74.1 — Sayısal doğrulama gerçek okunurluğu eksik temsil eder.**
  Opak çiftin kontrastı doğru olsa da metnin büyütülmesi, dış ışık ve hareketli kullanım sorun yaratabilir.

- **Öz eleştiri Ö74.2 — Çok sayıda kaynak uygulayıcıyı yorabilir.**
  İlgili görev ve rolün otoritesi seçilmeden yalnız son dosyadan çalışmak mevcut anlamı kaybettirebilir.

- **Öz eleştiri Ö74.3 — İzlenebilirlik tablosu kapsamı tamamlanmış sanılabilir.**
  Bir bileşen adının listede olması bütün gerçek durumlarının test edildiği anlamına gelmez.

## Visual Language Review

1. **VLR-001 — Sakin marka ifadesi ilk kullanımda fazla soyut kalıyor mu?**
   Risk: Kullanıcı ürünün hangi gezi kararına yardım ettiğini görsel hiyerarşiden anlayamayabilir.
   Kontrol: İlk bakışta görülen metin ve eylemin anlamı kullanıcıdan kendi sözüyle alınmalıdır.
   Kabul sınırı: Soyutluğu gidermek için yeni onboarding veya zorunlu açıklama akışı eklenmez.

2. **VLR-002 — Deniz metaforu içerik anlamını gereksiz yere kaplıyor mu?**
   Risk: Dalga ve şamandıra çağrışımları gerçek yer bilgisinden daha baskın olabilir.
   Kontrol: Metafor içeren görsel kararların görevde hangi anlamı taşıdığı incelenmelidir.
   Kabul sınırı: Yalnız marka süsü olan hareket veya ikon temel kontrolleri gölgeleyemez.

3. **VLR-003 — Minimal yüzey az bilgi izlenimi veriyor mu?**
   Risk: Kullanıcı gerekli sınırın bulunmadığını veya ürünün yetersiz olduğunu düşünebilir.
   Kontrol: Boşluk ile bilgi eksikliği algısı ayrı sorularla değerlendirilmelidir.
   Kabul sınırı: Görünümü doldurmak için kanıtsız özellik veya öneri eklenmez.

4. **VLR-004 — Premium hissi pahalı yer uygunluğu çağrıştırıyor mu?**
   Risk: Yüzeyin özeni, önerilen yerlerin yalnız yüksek bütçeye uygun olduğu izlenimini verebilir.
   Kontrol: Farklı bütçe bağlamlarında aynı görsel dilin algısı incelenmelidir.
   Kabul sınırı: Bütçe farklılığı kullanıcı veya yer kalitesi ayrımına dönüşemez.

5. **VLR-005 — Güven veren görünüm belirsizliği bastırıyor mu?**
   Risk: Kullanıcı sakin ve düzenli kartı bütün bilgileri doğrulanmış sanabilir.
   Kontrol: Estetik güven ile iddia kesinliğinin ayrı anlaşılması değerlendirilmelidir.
   Kabul sınırı: Önemli bilinmeyen olumlu gerekçeden daha zor bulunur hale getirilemez.

6. **VLR-006 — Zamansızlık hedefi donuk veya eski algısı oluşturuyor mu?**
   Risk: Kullanıcı görsel sakinliği ürünün güncel olmadığına yorabilir.
   Kontrol: Güncellik algısı ile okunabilirlik ve görev başarısı ayrı incelenmelidir.
   Kabul sınırı: Güncel görünmek için mevcut hareket ve kontrast sınırları aşılmaz.

7. **VLR-007 — Turistik karakter yalnız fotoğrafa bağımlı mı?**
   Risk: Fotoğraf yokken yerin kimliği ve gezi bağlamı tamamen kaybolabilir.
   Kontrol: Medyasız yer kartlarında ad, konum ve somut özelliklerin katkısı sınanmalıdır.
   Kabul sınırı: Eksik gerçek fotoğraf yapay yer görseliyle tamamlanmaz.

8. **VLR-008 — Marka accent'i bütün durumları birbirine benzetiyor mu?**
   Risk: Seçim, başarı ve AI açıklaması tek bir olumlu anlam gibi okunabilir.
   Kontrol: Accent kullanılan bütün anlam aileleri birlikte karşılaştırılmalıdır.
   Kabul sınırı: Accent yeni bir uygunluk veya güven derecesi üretemez.

9. **VLR-009 — Görsel kararların gerekçeleri gerçek görev yerine zevke dayanıyor mu?**
   Risk: Tasarım tercihleri tartışılamayan kişisel doğrulara dönüşebilir.
   Kontrol: Her tercihin kullanıcıya etkisi ve bedeli somut olarak okunmalıdır.
   Kabul sınırı: Beğeni ifadesi test sonucu veya ürün gereği gibi sunulmaz.

10. **VLR-010 — Ürün kimliği referans markaların toplamı gibi mi görünüyor?**
    Risk: Şamandıra'nın iddia ve sınır disiplini görsel benzerlik arayışında kaybolabilir.
    Kontrol: Logo olmadan karar hiyerarşisinin hangi ürüne ait hissettirdiği araştırılmalıdır.
    Kabul sınırı: Tanınmak için tescilli görünüm veya ekran düzeni kopyalanmaz.

11. **VLR-011 — Beyaz alan ilişkili bilgiyi birbirinden koparıyor mu?**
    Risk: Olumlu gerekçe ile önemli ödün farklı içerik kümeleri sanılabilir.
    Kontrol: Kullanıcının aynı iddiaya bağlı parçaları eşleştirmesi incelenmelidir.
    Kabul sınırı: Ferahlık adına karar değiştiren sınır okuma biriminden uzaklaştırılmaz.

12. **VLR-012 — Grid disiplini uzun Türkçe metni cezalandırıyor mu?**
    Risk: Düzenli sütunları korumak için başlık veya kapsam metni kesilebilir.
    Kontrol: Uzun yer adları ve bileşik koşullar büyütülmüş metinle değerlendirilmelidir.
    Kabul sınırı: Grid içerik anlamından önce gelmez.

13. **VLR-013 — 8pt düzen bütün optik kararları mekanikleştiriyor mu?**
    Risk: İkon ve metin matematiksel hizalı görünse de algısal olarak dengesiz kalabilir.
    Kontrol: Görsel ağırlık ile hedef sınırlarının birlikte dengesi incelenmelidir.
    Kabul sınırı: Optik düzeltme dokunma hedefini veya mevcut ölçeği bozmaz.

14. **VLR-014 — Yatay alan kullanımı tek elle taramayı zorlaştırıyor mu?**
    Risk: Kullanıcı önemli bilgiyi görmek için telefonu yeniden kavramak zorunda kalabilir.
    Kontrol: Mevcut görevde kontrol erişimi farklı el ve cihaz boyutlarıyla değerlendirilmelidir.
    Kabul sınırı: Tek elle kullanım yeni gizli jestler ekleme gerekçesi olmaz.

15. **VLR-015 — Dikey uzama karar parçalarını aşırı dağıtıyor mu?**
    Risk: İçeriği kesmeme tercihi olumlu gerekçe ile sonucu zihinde bağlamayı zorlaştırabilir.
    Kontrol: Uzun kartta temel karar cümlesinin ve sınırının birlikte bulunması incelenmelidir.
    Kabul sınırı: Sorun kritik metni gizleyerek çözülmez.

16. **VLR-016 — Sabit eylem alanı büyütülmüş içerik üstüne biniyor mu?**
    Risk: Klavye odağı veya önemli satır görünür alanın dışında kalabilir.
    Kontrol: Kısa yatay ekran ve büyütülmüş metinde mevcut sabit alan değerlendirilmelidir.
    Kabul sınırı: Odaklı kontrolün görünmesi estetik sabitlikten önce gelir.

17. **VLR-017 — Kart içi boşluk farklı içerik türlerinde farklı anlam mı taşıyor?**
    Risk: Aynı mesafe bir yerde grup, başka yerde ayrı bölüm izlenimi verebilir.
    Kontrol: Yer, rota ve AI kartlarında grup ilişkileri karşılaştırılmalıdır.
    Kabul sınırı: Gerekçesiz aralık varyantı yeni varsayılan haline gelmez.

18. **VLR-018 — Geniş ekran boşluğu gereksiz içerikle dolduruluyor mu?**
    Risk: Daha fazla alan daha fazla öneri veya bağımsız görev baskısı yaratabilir.
    Kontrol: Geniş ekran varyantının mevcut görev sorusuna ek yükü incelenmelidir.
    Kabul sınırı: Görsel kapasite yeni portal veya akış açma yetkisi değildir.

19. **VLR-019 — Dar ekran hiyerarşisi gerçek önceliği koruyor mu?**
    Risk: Sığdırma sırasında fotoğraf korunup bilgi sınırı aşağı itilebilir.
    Kontrol: Aynı içeriğin dar ve geniş sunumunda ilk okunan bilgiler karşılaştırılmalıdır.
    Kabul sınırı: Alan daralınca önce dekor ve yardımcı düzen azalır.

20. **VLR-020 — Düzensiz kart yükseklikleri ortak ölçütte kıyası zorlaştırıyor mu?**
    Risk: Kullanıcı süre, kapsam ve önemli engelin karşılıklarını bulamayabilir.
    Kontrol: Ortak etiketlerle farklı uzunlukta kartların taranması incelenmelidir.
    Kabul sınırı: Simetri için kritik bilgi kısaltılmaz.

21. **VLR-021 — Radius sıcaklığı kontrolün ciddiyetini azaltıyor mu?**
    Risk: Fazla yumuşak biçimler kritik işlem veya uyarıyı oyuncak gibi gösterebilir.
    Kontrol: Mevcut radius rollerinin farklı önem düzeylerindeki algısı değerlendirilmelidir.
    Kabul sınırı: Şekil tercihi yeni önem hiyerarşisi üretmez.

22. **VLR-022 — Aynı radius bütün yüzeyleri etkileşimli gibi mi gösteriyor?**
    Risk: Bilgi kartı, kontrol ve dekoratif alanın işlevleri karışabilir.
    Kontrol: Tıklanabilirlik beklentisi görünür eylem ve yüzey ailesiyle incelenmelidir.
    Kabul sınırı: Etkileşim sadece köşe biçiminden çıkarılmak zorunda bırakılmaz.

23. **VLR-023 — Gölgesiz kartlar harita üzerinde sınırını kaybediyor mu?**
    Risk: Değişken harita yoğunluğu bilgi yüzeyi ile zemin ayrımını zayıflatabilir.
    Kontrol: Farklı harita ayrıntı yoğunluklarında sınır ve yüzey tonu değerlendirilmelidir.
    Kabul sınırı: Her karta ağır gölge eklemek otomatik çözüm sayılmaz.

24. **VLR-024 — Elevation önem veya kalite sıralaması sanılıyor mu?**
    Risk: Yükselmiş yer kartı daha iyi öneri veya ücretli ayrıcalık gibi okunabilir.
    Kontrol: Katman ayrımı ile yer değerlendirmesinin bağımsız anlaşılması incelenmelidir.
    Kabul sınırı: Elevation yalnız mevcut görev ve yüzey ilişkisini taşır.

25. **VLR-025 — Cam etkisi içerik okunmasını arka plana bağımlı kılıyor mu?**
    Risk: Aynı metin haritanın bir bölgesinde okunurken başka bölgede kaybolabilir.
    Kontrol: Efektin gerçek zemin birleşimleri üzerinde kontrastı değerlendirilmelidir.
    Kabul sınırı: Opak eşdeğer olmadan cam etki temel okuma yüzeyi olamaz.

26. **VLR-026 — Blur kullanımı okunabilirlik sorununu saklıyor mu?**
    Risk: Yetersiz ton ayrımı bulanıklık sayesinde geçici olarak iyi görünebilir.
    Kontrol: Blur kapalıyken kontrol ve katmanın anlaşılması incelenmelidir.
    Kabul sınırı: Bulanıklık tek sınır veya odak kanalı değildir.

27. **VLR-027 — Koyu temada gölge görünmez kaldığında katmanlar birleşiyor mu?**
    Risk: Etkin alt görev ile arka içerik aynı yüzey gibi algılanabilir.
    Kontrol: Gölgesiz görüntüde yüzey ve kenar ayrımı değerlendirilmelidir.
    Kabul sınırı: Katman açıklığı gölgenin algılanmasına bağlı kalmaz.

28. **VLR-028 — Açık tema fazla parlak yüzeylerle göz yorgunluğu yaratıyor mu?**
    Risk: Uzun karar okumasında yüksek ışıklılık rahatsızlık oluşturabilir.
    Kontrol: Açık yüzeylerin uzun okuma ve dış ortam algısı araştırılmalıdır.
    Kabul sınırı: Rahatlık için metin kontrastı düşürülmez.

29. **VLR-029 — Dark mode siyahları bilgi gruplarını birbirine yapıştırıyor mu?**
    Risk: Kart ve sayfa ayrımı kaybolduğunda sıra veya grup anlamı belirsizleşebilir.
    Kontrol: Yakın koyu tonların gerçek cihazda ayrışması incelenmelidir.
    Kabul sınırı: Koyu görünüm, daha az bilgi görünürlüğü anlamına gelemez.

30. **VLR-030 — Efekt maliyeti düşük cihazlarda geri bildirimi geciktiriyor mu?**
    Risk: Premium görünüm için kullanılan yüzey işlemleri doğrudan kontrol hissini zayıflatabilir.
    Kontrol: Temsilî cihazlarda mevcut işlemin görsel karşılık süresi değerlendirilmelidir.
    Kabul sınırı: Etki azaltılabilir; gerçek durum veya kullanıcı kontrolü geciktirilemez.

31. **VLR-031 — Sistem sans ailesi Türkçe karakterleri eşit ağırlıkta gösteriyor mu?**
    Risk: İ, ı, Ş ve Ğ karakterleri başlık ritminde dengesiz algılanabilir.
    Kontrol: Türkçe yer adları farklı desteklenen platformlarda okunmalıdır.
    Kabul sınırı: Karakter sorunu metni değiştirerek veya işaretleri kaldırarak çözülmez.

32. **VLR-032 — Font farkı kanallar arasında yanlış önem sırası üretiyor mu?**
    Risk: Aynı ağırlık adı farklı sistem fontlarında farklı baskınlık gösterebilir.
    Kontrol: Başlık, gövde ve bilgi sınırı beraber karşılaştırılmalıdır.
    Kabul sınırı: Ortak rol yalnız sayısal ağırlık adına bakılarak doğrulanmış sayılmaz.

33. **VLR-033 — İnce başlıklar premium uğruna okunurluğu azaltıyor mu?**
    Risk: Düşük parlaklık ve hareket halinde önemli adlar zor okunabilir.
    Kontrol: Gerçek uzun yer başlıkları farklı ışık koşullarında değerlendirilmelidir.
    Kabul sınırı: Zarafet gerekçesi kritik metni zayıflatmaz.

34. **VLR-034 — Satır yüksekliği uzun sınır cümlelerini parçalı hissettiriyor mu?**
    Risk: Gereğinden fazla boşluk tek iddiaya bağlı açıklamaları ayrı paragraflar gibi gösterebilir.
    Kontrol: Birden çok satırlı kapsam cümlelerinin bütün olarak anlaşılması incelenmelidir.
    Kabul sınırı: Görsel ferahlık anlamsal birlikten önce gelmez.

35. **VLR-035 — Dar satır aralığı büyütülmüş metinde yığılma yaratıyor mu?**
    Risk: Uzun adlar ve önemli koşullar birbirinin görsel alanına girebilir.
    Kontrol: Kullanıcı metin ve aralık ayarlarıyla görünüm değerlendirilmelidir.
    Kabul sınırı: Kullanıcı ölçeği sabit yüksekliğe sığdırmak için bastırılmaz.

36. **VLR-036 — Harf aralığı Türkçe kelime biçimini bozuyor mu?**
    Risk: Aşırı açılmış kısa etiketler okunmayı hızlandırmak yerine yavaşlatabilir.
    Kontrol: Başlık ve kontrol etiketlerinin kelime olarak taranması incelenmelidir.
    Kabul sınırı: Marka ifadesi etiketin doğal okunmasını zedeleyemez.

37. **VLR-037 — Tamamı büyük harfli etiketler karar dilini sertleştiriyor mu?**
    Risk: Nötr bilgi veya vazgeçme eylemi emir gibi hissedilebilir.
    Kontrol: Etiket tonunun görev duygusuna etkisi değerlendirilmelidir.
    Kabul sınırı: Görsel vurgu için bütün metin bağırtılmaz.

38. **VLR-038 — Caption önemli bir bilgi mezarlığına dönüşüyor mu?**
    Risk: Bilinmeyen, zaman kapsamı veya ek maliyet küçük yazıya itilebilir.
    Kontrol: Caption rolündeki bütün metinler karar etkisine göre taranmalıdır.
    Kabul sınırı: Kararı değiştiren bilgi küçük ayrıntı rolüne bırakılamaz.

39. **VLR-039 — Sayıların büyüklüğü kapsam metnini psikolojik olarak eziyor mu?**
    Risk: Kullanıcı toplamın neyi içerdiğini okumadan sayıyla karar verebilir.
    Kontrol: Süre ve maliyet anlamı, kapsama ilişkin sorularla incelenmelidir.
    Kabul sınırı: Sayı, kapsamından bağımsız kesinlik izlenimi yaratamaz.

40. **VLR-040 — Başlık sayısı mevcut görevin yapısını olduğundan karmaşık gösteriyor mu?**
    Risk: Küçük bilgi grupları bağımsız karar aşamaları sanılabilir.
    Kontrol: Başlıkların kullanıcıya hangi görev yapısını anlattığı değerlendirilmelidir.
    Kabul sınırı: Görsel belge düzeni yeni ekran veya adım üretmez.

41. **VLR-041 — Ana CTA ret yolunu görünmez kılıyor mu?**
    Risk: Kullanıcı mevcut öneriyi kabul etmek zorunda olduğunu düşünebilir.
    Kontrol: İlerleme ve vazgeçme yollarının birlikte bulunması incelenmelidir.
    Kabul sınırı: Ana eylem baskın olabilir; ret yolu okunamaz olamaz.

42. **VLR-042 — İkincil butonlar bağlantıdan ayırt edilebiliyor mu?**
    Risk: Kullanıcı işlem başlatacağını mı yoksa başka bağlama gideceğini mi anlayamayabilir.
    Kontrol: Kontrol görünümüyle eylem beklentisi eşleşmesi değerlendirilmelidir.
    Kabul sınırı: Anlam yalnız rengin doygunluğuna bırakılamaz.

43. **VLR-043 — Devre dışı kontrolün nedeni yeterince okunur mu?**
    Risk: Düşük kontrastlı görünüm gerekli açıklamayı da görünmez hale getirebilir.
    Kontrol: Kontrol kullanılamadığında neden ve mevcut devam yolunun okunması incelenmelidir.
    Kabul sınırı: Kontrol istisnası açıklama metnini okunamaz yapma izni değildir.

44. **VLR-044 — Basılı durum tamamlanma gibi mi görünüyor?**
    Risk: Kullanıcı ağ teyidi gelmeden işlemin kaydedildiğini sanabilir.
    Kontrol: Basma, bekleme ve gerçek sonuç görünümleri ayrı anlamlandırılmalıdır.
    Kabul sınırı: Yerel temas uzak işlemin başarısını temsil etmez.

45. **VLR-045 — Buton metni uzadığında hedef bozuluyor mu?**
    Risk: Çeviri veya büyütme, etiketin kesilmesine ya da hedefin küçülmesine neden olabilir.
    Kontrol: En uzun gerçek eylem adlarıyla hedef ve satır davranışı incelenmelidir.
    Kabul sınırı: Alan kazanmak için anlamı belirsiz ikon zorunlu hale getirilmez.

46. **VLR-046 — Yıkıcı eylem rengi bağlamdan bağımsız korku üretiyor mu?**
    Risk: Geri alınabilir basit kaldırma, telafisiz kayıp gibi hissedilebilir.
    Kontrol: Görsel ciddiyet ile mevcut işlemin gerçek sonucu karşılaştırılmalıdır.
    Kabul sınırı: Bu değerlendirme kabul edilmiş onay ve geri alma davranışını değiştirmez.

47. **VLR-047 — İkon ailesi optik ağırlık bakımından tutarlı mı?**
    Risk: Aynı boyuttaki farklı ikonlar eşit olmayan önem algısı yaratabilir.
    Kontrol: Kontrol grupları gerçek metinleri ve hedef sınırlarıyla değerlendirilmelidir.
    Kabul sınırı: Optik fark kalite veya ticari öncelik işareti haline gelemez.

48. **VLR-048 — Dolu ikon her zaman seçili durum mu anlatıyor?**
    Risk: Dekoratif dolu ikonlar kullanıcının seçim sözlüğünü bozabilir.
    Kontrol: Dolu ve çizgi varyantların kullanıldığı bütün durumlar karşılaştırılmalıdır.
    Kabul sınırı: Aynı görsel işaret çelişkili anlamlara verilmez.

49. **VLR-049 — Az tanınan ikonlar metin olmadan yanlış okunuyor mu?**
    Risk: Bir İz, kayıt türü veya bilgi sınırı kontrolü bulunamayabilir.
    Kontrol: İkon anlamı ilk kullanımda açıklamasız tahmin ettirilerek incelenmelidir.
    Kabul sınırı: Kritik veya az tanınan eylem görünür metnini korur.

50. **VLR-050 — Küçük ikon büyük hedef içinde yanlış merkezlenmiş mi?**
    Risk: Kullanıcı komşu eyleme bastığını sanabilir veya hedef alanlarını karıştırabilir.
    Kontrol: Optik merkez ile dokunma sınırının ilişkisi incelenmelidir.
    Kabul sınırı: Büyük hedeflerin görünmeyen alanları birbirine çakışamaz.

51. **VLR-051 — Boş durum kullanıcıyı başarısız hissettiriyor mu?**
    Risk: Boş liste, tamamlanmamış görev veya eksik kişisel geçmiş gibi algılanabilir.
    Kontrol: İllüstrasyon ve metnin duygusal çağrışımı araştırılmalıdır.
    Kabul sınırı: Boş taslak ve erken bitiş geçerli sonuç olarak nötr kalır.

52. **VLR-052 — Boş sonuç ile hizmet hatası aynı görünüyor mu?**
    Risk: Teknik kesinti dünyada uygun yer olmadığı şeklinde yorumlanabilir.
    Kontrol: İki durumun nedeni ve mevcut eylemi ayrı anlamlandırılmalıdır.
    Kabul sınırı: Aynı dekor altında farklı anlamlar tek mesaja indirgenmez.

53. **VLR-053 — Loading göstergesi ölçülmüş ilerleme hissi mi veriyor?**
    Risk: Döngü veya dolan biçim gerçek süreç oranı sanılabilir.
    Kontrol: Kullanıcıdan ne kadar işin tamamlandığını bildiğini açıklaması istenmelidir.
    Kabul sınırı: Ölçülemeyen işte yüzde veya sahte aşama üretilmez.

54. **VLR-054 — Skeleton gerçek sonuç sayısı beklentisi oluşturuyor mu?**
    Risk: Kullanıcı boş gövdelerin kesin gelecek yerler olduğunu düşünebilir.
    Kontrol: Az sonuç ve hiç sonuç olmayan durumlarda beklenti farkı incelenmelidir.
    Kabul sınırı: Görsel iskelet sayı doldurmak için içerik üretme baskısına dönüşmez.

55. **VLR-055 — Skeleton metin ve fotoğrafla uyuşmayıp sıçrama yaratıyor mu?**
    Risk: Kullanıcının baktığı veya basmak üzere olduğu alan yer değiştirebilir.
    Kontrol: Uzun içerik ve farklı fotoğraf oranlarıyla yükleme geçişi değerlendirilmelidir.
    Kabul sınırı: Görsel kararlılık için kritik bilgi geciktirilmez.

56. **VLR-056 — Durağan loading donmuş ürün gibi algılanıyor mu?**
    Risk: Hareket azaltan kullanıcı işlemin sürdüğünü anlayamayabilir.
    Kontrol: Statik metin ve durum işaretinden bekleme anlamı çıkarılması incelenmelidir.
    Kabul sınırı: Statik eşdeğer yalnız animasyonun silinmiş hali değildir.

57. **VLR-057 — Progress görünümü bitince gerçek teyit bekleniyor mu?**
    Risk: Görsel çubuğun dolması ağ sonucundan önce başarı algısı yaratabilir.
    Kontrol: İlerleme sonu ile işlem teyidinin ayrı görünmesi değerlendirilmelidir.
    Kabul sınırı: Görsel doluluk yetkili teyidin yerine geçmez.

58. **VLR-058 — Hata görünümü kullanıcının emeğini örtüyor mu?**
    Risk: Tam yüzey hata boyası mevcut metnin kaybolduğu izlenimini verebilir.
    Kontrol: Korunmuş girdinin ve onarım yolunun bulunması incelenmelidir.
    Kabul sınırı: Hata açıklığı mevcut taslağın görünür değerini silmez.

59. **VLR-059 — Offline işareti her bilgiye aynı geçersizlik damgası vuruyor mu?**
    Risk: Tarihli temel bilgi ile yeni uygunluk güvencesi arasındaki fark kaybolabilir.
    Kontrol: Kullanıcının hangi bilgiye hangi kapsamda eriştiğini anlaması sınanmalıdır.
    Kabul sınırı: Offline görünüm eski bilgiyi canlı yapamaz veya bütün bilgiyi yok sayamaz.

60. **VLR-060 — Sonucu belirsiz işlem hata gibi mi renklendiriliyor?**
    Risk: Kullanıcı tamamlanmış olabilecek işlemi tekrar başlatmaya çalışabilir.
    Kontrol: Başarısızlık ile teyidi bilinmeyen sonuç ayrı örneklerle incelenmelidir.
    Kabul sınırı: Görsel durum gerçek işlem sınıfını değiştirerek basitleştiremez.

61. **VLR-061 — Toast kritik bilginin tek görünür taşıyıcısı mı olmuş?**
    Risk: Kısa mesajı kaçıran kullanıcı karar değiştiren sınırı öğrenemeyebilir.
    Kontrol: Mesaj kaybolduktan sonra aynı önemli bilgiye erişim incelenmelidir.
    Kabul sınırı: Kritik bilgi yalnız geçici katmana bırakılamaz.

62. **VLR-062 — Snackbar geri alma eylemi yeterince ayırt ediliyor mu?**
    Risk: Kısa mesaj içinde kontrol ile açıklama aynı biçimde okunabilir.
    Kontrol: Eylemin bulunabilirliği farklı okuma hızlarında değerlendirilmelidir.
    Kabul sınırı: Mevcut kalıcı geri alma erişimi görsel olarak korunur.

63. **VLR-063 — Bildirim görseli canlı takip garantisi gibi mi algılanıyor?**
    Risk: Kullanıcı uyarı gelmemesini koşulların iyi olduğu şeklinde yorumlayabilir.
    Kontrol: Bildirim kapsamı ve teslim sınırı metinle birlikte değerlendirilmelidir.
    Kabul sınırı: Sakin bildirim dili desteklenmeyen izleme güvencesi veremez.

64. **VLR-064 — Bildirim önemleri yalnız renkle ayrılıyor mu?**
    Risk: Renk görme farklılıklarında kritik değişim rutin bilgiyle karışabilir.
    Kontrol: Renksiz görünümde başlık, simge ve eylem anlamı incelenmelidir.
    Kabul sınırı: Semantik rengin yanında anlamlı metin ve işaret gerekir.

65. **VLR-065 — Bottom sheet ana görevi fazla örtüyor mu?**
    Risk: Kullanıcı hangi bağlamdaki kısa alt işi yaptığını unutabilir.
    Kontrol: Mevcut sheet başlığı ile arka görev ilişkisinin anlaşılması incelenmelidir.
    Kabul sınırı: Görsel rahatlık gerekçesiyle yeni bağımsız modal eklenmez.

66. **VLR-066 — Sheet kapatma işareti büyütmede erişilebilir kalıyor mu?**
    Risk: Tutamaç görünse bile gerçek kapatma kontrolü görünür alan dışında kalabilir.
    Kontrol: Büyük metin, klavye ve kısa ekranla çıkış bulunabilirliği değerlendirilmelidir.
    Kabul sınırı: Sürükleyerek kapatma tek yol olamaz.

67. **VLR-067 — Modal vurgusu rutin durumu gereksiz ciddileştiriyor mu?**
    Risk: Basit geri alınabilir işlem beklenmedik kayıp gibi hissedilebilir.
    Kontrol: Görsel kesinti ile mevcut görevin gerçek öneminin uyumu incelenmelidir.
    Kabul sınırı: Bu belge yeni onay adımı açmaz.

68. **VLR-068 — Dialog seçenekleri kararı tek tarafa itiyor mu?**
    Risk: Kullanıcı açıkça korunması gereken vazgeçme hakkını göremeyebilir.
    Kontrol: Her seçenek anlamı, görünürlüğü ve hedef alanıyla değerlendirilmelidir.
    Kabul sınırı: Düğme vurgusu kullanıcı iradesini görsel olarak geçersiz kılamaz.

69. **VLR-069 — FAB mevcut görevin tek baskın eylemiyle yarışıyor mu?**
    Risk: Kullanıcı hangi kontrolün şu anki işi ilerlettiğini anlayamayabilir.
    Kontrol: Mevcut FAB kullanımında birincil görev algısı ayrıca incelenmelidir.
    Kabul sınırı: Yeni FAB, yeni eylem veya yeni akış bu görsel belgeyle oluşturulmaz.

70. **VLR-070 — Navigation ve tab görünümleri görev ile görünüm seçimini karıştırıyor mu?**
    Risk: Liste–harita değişimi farklı ürün alanına geçiş gibi okunabilir.
    Kontrol: Mevcut sekmelerin kullanıcıya anlattığı ilişki sorulmalıdır.
    Kabul sınırı: Görsel vurgu kabul edilmiş bilgi mimarisini değiştiremez.

71. **VLR-071 — Search görseli doğal ifade yerine komut beklentisi mi oluşturuyor?**
    Risk: Kullanıcı doğru anahtar kelimeyi bulmak zorunda olduğunu düşünebilir.
    Kontrol: Alan etiketi ve yardımcı metinle başlama davranışı incelenmelidir.
    Kabul sınırı: Yeni zorunlu soru veya arama akışı eklenmez.

72. **VLR-072 — Arama önerileri sonucu kesinleştirmiş gibi görünüyor mu?**
    Risk: Benzer adlı yerler arasında yanlış şube seçilebilir.
    Kontrol: Ad ve konum ayrımı öneri durumunda birlikte değerlendirilmelidir.
    Kabul sınırı: Yazım benzerliği yer kimliği güvencesi gibi sunulmaz.

73. **VLR-073 — Harita kontrolleri yoğun coğrafi zeminde kayboluyor mu?**
    Risk: Kullanıcı konum ve liste kontrolünü bulamayabilir.
    Kontrol: Farklı yol, etiket ve fotoğraf yoğunluklarında kontrol sınırı incelenmelidir.
    Kabul sınırı: Kontrol zemini mevcut opak ve kontrastlı rolü korur.

74. **VLR-074 — Marker büyüklüğü yer kalitesi sıralaması gibi mi okunuyor?**
    Risk: Seçili veya kümelenmiş işaretler daha iyi yer algısı yaratabilir.
    Kontrol: Marker boyunun ne anlama geldiği kullanıcıdan açıklaması istenmelidir.
    Kabul sınırı: Görsel işaret organik uygunluk kararı üretemez.

75. **VLR-075 — Marker rengi seçimi ve erişim durumunu karıştırıyor mu?**
    Risk: Yeşil veya accent işaret zorunlu koşul sağlandı güvencesi sanılabilir.
    Kontrol: Seçili yer ve bilgi sınırı farklı örneklerde karşılaştırılmalıdır.
    Kabul sınırı: Seçim rengi olumlu erişim kanıtı değildir.

76. **VLR-076 — Cluster sayısı popülerlik göstergesi gibi algılanıyor mu?**
    Risk: Kullanıcı bir alanın çok yer içermesini daha iyi destinasyon sayabilir.
    Kontrol: Sayının kapsadığı nesnenin anlaşılması incelenmelidir.
    Kabul sınırı: Küme yoğunluğu sosyal kanıt veya kalite puanına çevrilmez.

77. **VLR-077 — Route çizgisinin kesintisizliği erişim garantisi veriyor mu?**
    Risk: Kullanıcı çizgiyi bütün yolun uygunluğu doğrulanmış sanabilir.
    Kontrol: Rota çizimi ile mevcut ulaşım ve erişim sınırı birlikte değerlendirilmelidir.
    Kabul sınırı: Görsel bağlantı desteklenmeyen fiziksel erişim iddiası üretmez.

78. **VLR-078 — Alternatif rota çizgileri okunamaz bir ağ yaratıyor mu?**
    Risk: Kullanıcı seçili günlük planın hangisi olduğunu kaybedebilir.
    Kontrol: Kabul edilmiş alternatif sayısıyla çizgi ve durak kimliği incelenmelidir.
    Kabul sınırı: Görsel zenginlik için yeni alternatif rota eklenmez.

79. **VLR-079 — Yaklaşık konum işareti kesin adres gibi görünüyor mu?**
    Risk: Kullanıcı gerçek giriş veya bulunma noktası hakkında fazla kesinlik çıkarabilir.
    Kontrol: Konum kapsamının metinsel ve görsel eşdeğeri değerlendirilmelidir.
    Kabul sınırı: Nokta temizliği uğruna belirsizlik çemberi veya kapsam metni kaybolmaz.

80. **VLR-080 — Harita atıf ve ölçek bilgileri kontroller altında kalıyor mu?**
    Risk: Haritanın gerekli kaynak ve mesafe anlamı eksilebilir.
    Kontrol: Küçük ekran ve açık katmanda atıf ile ölçek görünürlüğü incelenmelidir.
    Kabul sınırı: Marka temizliği gerekli atıf veya ölçek bilgisini örtemez.

81. **VLR-081 — AI kartı bağımsız uzman otoritesi gibi mi görünüyor?**
    Risk: Kullanıcı açıklamayı motorun kanıt sınırlarından bağımsız kesin hüküm sayabilir.
    Kontrol: AI adı ve görsel vurgusunun güven algısına etkisi araştırılmalıdır.
    Kabul sınırı: AI simgesi veya renk alanı yeni doğrulama rozeti olamaz.

82. **VLR-082 — AI açıklaması önemli ödünü görünüm içinde geriye itiyor mu?**
    Risk: Akıcı metin olumlu gerekçeyi baskınlaştırırken sınır unutulabilir.
    Kontrol: Gerekçe, ödün ve bilinmeyenin aynı anda hatırlanması incelenmelidir.
    Kabul sınırı: Anlatım kalitesi kapsam kaybını telafi etmez.

83. **VLR-083 — Seyahat kartı günlük planı tamamlanması gereken programa çeviriyor mu?**
    Risk: Durak göstergeleri kontrol yerine performans baskısı yaratabilir.
    Kontrol: Tek durak, mola ve erken bitiş örneklerinin algısı değerlendirilmelidir.
    Kabul sınırı: Günün boş bölümü veya atlanan durak görsel başarısızlık sayılmaz.

84. **VLR-084 — Restoran fotoğrafı menü ve kullanım koşulunu gölgeliyor mu?**
    Risk: Estetik yemek görüntüsü çalışma, kalış veya bütçe uygunluğu sanılabilir.
    Kontrol: Somut kullanım kapsamının fotoğraftan bağımsız anlaşılması incelenmelidir.
    Kabul sınırı: Atmosfer fotoğrafı görünmeyen özellikleri doğrulayamaz.

85. **VLR-085 — Etkinlik kartı saat ve son giriş farkını düzleştiriyor mu?**
    Risk: Büyük tarih alanı kullanıcının gerekli zaman penceresini yanlış okumasına yol açabilir.
    Kontrol: Başlangıç ve ilgili giriş sınırının mevcut içerikte ayırt edilmesi incelenmelidir.
    Kabul sınırı: Görsel takvim sadeliği kritik zaman kapsamını silemez.

86. **VLR-086 — Otel kartı rezervasyon yapılabilirliği ima ediyor mu?**
    Risk: Büyük fiyat ve CTA biçimi mevcut olmayan rezervasyon hakkı beklentisi oluşturabilir.
    Kontrol: Kullanıcının karttan hangi eylemleri beklediği değerlendirilmelidir.
    Kabul sınırı: Görsel dil yeni rezervasyon ekranı, envanter veya satın alma akışı açmaz.

87. **VLR-087 — Fotoğraf yokluğu yerin kalitesizliği gibi okunuyor mu?**
    Risk: Az medyalı yerler görsel olarak haksız biçimde zayıf aday sanılabilir.
    Kontrol: Aynı yeterlilikte medyalı ve medyasız içeriğin algısı karşılaştırılmalıdır.
    Kabul sınırı: Medya zenginliği uygunluk veya sıra bonusu değildir.

88. **VLR-088 — Fotoğraf kırpması gerçek alanı çarpıtıyor mu?**
    Risk: Dar bir bölüm bütün mekânın genişliği, sessizliği veya erişimi gibi algılanabilir.
    Kontrol: Kırpmanın yer kimliği ve gösterilen kapsamla ilişkisi incelenmelidir.
    Kabul sınırı: Estetik kırpma görünmeyen alan hakkında olumlu iddia üretemez.

89. **VLR-089 — Gradient metin okunmasını yalnız bazı fotoğraflarda mı sağlıyor?**
    Risk: Parlak veya detaylı görüntülerde aynı metin görünmez olabilir.
    Kontrol: Gerçek görüntü çeşitliliğinde ön ve arka plan birleşimi değerlendirilmelidir.
    Kabul sınırı: Gradient tek okunurluk güvencesi sayılmaz.

90. **VLR-090 — Renk psikolojisi evrensel kullanıcı tepkisi gibi mi anlatılıyor?**
    Risk: Kültür ve kişisel deneyim farkları tasarım gerekçesinde yok sayılabilir.
    Kontrol: Renk çağrışımı iddiaları hedef bağlamda araştırma hipotezi olarak ele alınmalıdır.
    Kabul sınırı: Bir renk kendiliğinden güven, başarı veya sakinlik kanıtı değildir.

91. **VLR-091 — Success görünümü kaydın kapsamını olduğundan geniş gösteriyor mu?**
    Risk: Cihaz kaydı kalıcı hesap güvencesi veya ziyaret beyanı sanılabilir.
    Kontrol: Kullanıcıya neyin nerede tamamlandığı açıklattırılmalıdır.
    Kabul sınırı: Teyit yalnız gerçekten gerçekleşmiş işlemi anlatır.

92. **VLR-092 — Error dili bilgi bilinmeyenini başarısızlığa çeviriyor mu?**
    Risk: Kullanıcı eksik bilgiyi teknik arıza veya kendi hatası sanabilir.
    Kontrol: Bilgi açığı, boş sonuç ve işlem hatası görünümü karşılaştırılmalıdır.
    Kabul sınırı: Farklı durumlar sırf aynı kırmızı aileye sığsın diye birleştirilmez.

93. **VLR-093 — Warning sürekli kullanıldığı için etkisini kaybediyor mu?**
    Risk: Kullanıcı gerçekten karar değiştiren engeli rutin etiket gibi görmezden gelebilir.
    Kontrol: Uyarı yoğunluğu ile önemli sınırın hatırlanması incelenmelidir.
    Kabul sınırı: Yoğunluk azaltılırken gerekli uyarı kaldırılmaz; gereksiz vurgu sadeleşir.

94. **VLR-094 — Info nötr kaldığı için önemli bilinmeyen görünmüyor mu?**
    Risk: Bilinmeyen zorunlu koşul sıradan yardımcı bilgi sanılabilir.
    Kontrol: Bilginin karar etkisi ile görsel öncelik eşleşmesi değerlendirilmelidir.
    Kabul sınırı: Nötr ton, önemli sınırı önemsiz gösterme gerekçesi olamaz.

95. **VLR-095 — Hareket süreleri toplam görevde hissedilir bekleme yaratıyor mu?**
    Risk: Ayrı ayrı kısa geçişler art arda kullanıldığında kullanıcıyı geciktirebilir.
    Kontrol: Mevcut 0, 120, 180 ve 240 ms rollerinin görev içindeki birikimi incelenmelidir.
    Kabul sınırı: Animasyon hazır bilgiye veya hazır eyleme erişimi bekletemez.

96. **VLR-096 — Anlık kritik düzeltme görsel hata sanılıyor mu?**
    Risk: Kullanıcı bilginin neden değiştiğini anlayamayıp güven kaybedebilir.
    Kontrol: Mevcut değişiklik açıklamasıyla yeni sınırın anlamlandırılması değerlendirilmelidir.
    Kabul sınırı: Yumuşak görünüm için geçersiz olumlu bilgi tutulmaz.

97. **VLR-097 — Azaltılmış hareket tercihinde mekânsal ilişki tamamen kayboluyor mu?**
    Risk: Taşınan durak veya kapanan alt görev son durumda bulunamayabilir.
    Kontrol: Başlık, sıra ve görünür seçimle aynı görev tamamlanmalıdır.
    Kabul sınırı: Statik eşdeğer aynı bilgi ve kontrolü taşır.

98. **VLR-098 — Görev ortasında hareket tercihi değişince görünüm sıfırlanıyor mu?**
    Risk: Kullanıcının taslağı, odağı veya anlamlı okuma konumu kaybolabilir.
    Kontrol: Mevcut tercih değişimi senaryosu görsel durum sürekliliğiyle incelenmelidir.
    Kabul sınırı: Tercih uyarlaması yeni başlangıç sayfası yaratamaz.

99. **VLR-099 — Mikro etkileşimler art arda dikkat gürültüsü yaratıyor mu?**
    Risk: Her küçük seçim aynı görsel güçte karşılık alarak asıl değişimi gölgeleyebilir.
    Kontrol: Birkaç düzenlemenin ardışık yapıldığı görevde dikkat dağılımı incelenmelidir.
    Kabul sınırı: Geri bildirim korunur; gereksiz tekrar ve gösteri azaltılır.

100. **VLR-100 — Haptik başarı hissi metindeki bekleme durumunu bastırıyor mu?**
     Risk: Kullanıcı dokunsal karşılıktan uzak işlemin tamamlandığını çıkarabilir.
     Kontrol: Haptik açık ve kapalı durumlarda kayıt kapsamı anlama karşılaştırılmalıdır.
     Kabul sınırı: Dokunsal destek gerçek teyitten önce tamamlanma kanalı olamaz.

101. **VLR-101 — Jest tutamaçları görünür alternatifi gereksiz gibi mi gösteriyor?**
     Risk: Kullanıcı temel görevin ancak sürükleyerek yapılabileceğini düşünebilir.
     Kontrol: İlk kez kullanan kişinin taşıma kontrolünü bulması incelenmelidir.
     Kabul sınırı: Görünür alternatif ikincil yardım metnine saklanmaz.

102. **VLR-102 — Sistem geri alanı ürün kontrolüyle görsel olarak çakışıyor mu?**
     Risk: Kenar hareketi ile görev eylemi birbirini yanlış tetikleyebilir.
     Kontrol: Desteklenen platformların mevcut kenar davranışıyla hedef yerleşimi incelenmelidir.
     Kabul sınırı: Marka farkı sistem gezinme beklentisini yeniden yazmaz.

103. **VLR-103 — Sürüklenen kartın görsel yükselmesi kalite farkı sanılıyor mu?**
     Risk: Hareket bitince kullanıcı taşınan durağın daha önemli hale geldiğini düşünebilir.
     Kontrol: Geçici taşıma görünümü ile kalıcı sıra anlamı ayrı sorulmalıdır.
     Kabul sınırı: Taşıma vurgusu görev dışı uygunluk veya öncelik puanı oluşturmaz.

104. **VLR-104 — Tek elle hedefler farklı cihazlarda hâlâ ayrışıyor mu?**
     Risk: Görsel ikonlar temiz olsa da gerçek dokunma alanları birbirine yaklaşabilir.
     Kontrol: 48 birim varsayılan ve 44 birim alt sınır gerçek görev düzeninde incelenmelidir.
     Kabul sınırı: Hedef ölçüleri WCAG minimumuyla karıştırılarak küçültülmez.

105. **VLR-105 — Odak halkası fotoğraf kenarında kırpılıyor mu?**
     Risk: Klavyeyle kullanan kişi aktif kontrolü kaybedebilir.
     Kontrol: Mevcut 2 tb halka ve 2 tb ayrımın değişken zeminde görünmesi değerlendirilmelidir.
     Kabul sınırı: Radius ve taşma temizliği odağın görünürlüğünü kesemez.

106. **VLR-106 — Yüksek kontrastta renk ve gölgeler kaybolunca anlam sürüyor mu?**
     Risk: Kontrol sınırı, seçili durum veya katman yalnız dekorla taşınıyor olabilir.
     Kontrol: Mevcut yüksek kontrast davranışında metin ve işaret ilişkisi incelenmelidir.
     Kabul sınırı: Anlam zorlanmış renklerde kayboluyorsa görsel karar tamamlanmış sayılmaz.

107. **VLR-107 — Ekran okuyucu karşılığı görsel mahremiyet sınırını aşıyor mu?**
     Risk: Görselde bulunmayan ham kanıt veya özel not erişilebilir açıklamaya sızabilir.
     Kontrol: Görünür metin ile erişilebilir adın izinli kapsamı birlikte değerlendirilmelidir.
     Kabul sınırı: Alternatif sunum kamusal bilgi paketinin sınırlarını genişletemez.

108. **VLR-108 — Sağdan sola dilde coğrafya yanlış aynalanıyor mu?**
     Risk: Arayüz yönü uyarlaması harita, rota numarası veya fotoğraf anlamını bozabilir.
     Kontrol: Mantıksal başlangıç ve bitişle coğrafi yön ayrı incelenmelidir.
     Kabul sınırı: Dil yönü fiziksel dünyayı aynalama gerekçesi değildir.

109. **VLR-109 — Uzun yer adları benzer şubeleri ayırt etmeyi zorlaştırıyor mu?**
     Risk: Kesilen ad veya konum satırı yanlış yer kararına yol açabilir.
     Kontrol: Aynı adın farklı şubeleri gerçekçi uzunlukta metinle karşılaştırılmalıdır.
     Kabul sınırı: Kimlik ayrımı görsel simetri uğruna kısaltılmaz.

110. **VLR-110 — Tarih ve para biçimi görsel olarak belirsiz mi?**
     Risk: Kullanıcı birim veya ziyaret zamanını yanlış okuyabilir.
     Kontrol: Desteklenen yerel biçimlerde sayı, birim ve kapsam birlikte incelenmelidir.
     Kabul sınırı: Büyük sayı tek başına bağlamın yerine geçmez.

111. **VLR-111 — Ücretsiz ve Premium durumlar aynı temel görsel kaliteyi taşıyor mu?**
     Risk: Ücretsiz kullanıcıya daha düşük güven veya daha zor erişim görünümü uygulanabilir.
     Kontrol: Aynı temel görev iki hak bağlamında karşılaştırılmalıdır.
     Kabul sınırı: Doğruluk, erişilebilirlik ve temel kontrol görsel olarak ücretlendirilemez.

112. **VLR-112 — Misafir kayıt görünümü kullanıcıyı hesap açmaya baskılıyor mu?**
     Risk: Cihaz kapsamı açıklaması korku yaratan bir satış aracına dönüşebilir.
     Kontrol: Kayıt sınırının doğru anlaşılması ve baskı algısı ayrı incelenmelidir.
     Kabul sınırı: Gerçek sınır dürüstçe anlatılır; zorunlu login görünümü üretilmez.

113. **VLR-113 — Bir İz görseli katkıyı sosyal başarıya çeviriyor mu?**
     Risk: Kullanıcı daha çok katkıyla statü kazanacağını düşünebilir.
     Kontrol: Alındı ve geri çekme görünümünün çağrışımları araştırılmalıdır.
     Kabul sınırı: Katkı sayacı, yıldız veya kazanılmış güven rozeti oluşturulmaz.

114. **VLR-114 — Paylaşım görünümü özel taslağın canlı aynası sanılıyor mu?**
     Risk: Kullanıcı özel düzenlemenin otomatik yayımlandığını veya alıcının düzenleyebildiğini varsayabilir.
     Kontrol: Mevcut özel, paylaşılan ve bağımsız kopya ayrımı görsel olarak incelenmelidir.
     Kabul sınırı: Yüzey benzerliği hak ve yayın kapsamını eşitleyemez.

115. **VLR-115 — Paylaşım kapatma beklemesi kapalı gibi görünüyor mu?**
     Risk: Bağlantı yokken kullanıcı erişimin gerçekten sona erdiğini düşünebilir.
     Kontrol: Bekleyen kapatma ile teyit edilmiş kapalı durumun anlaşılması değerlendirilmelidir.
     Kabul sınırı: Görsel başarı yetkili erişim teyidinden önce kullanılamaz.

116. **VLR-116 — Admin yoğunluğu tüketici yüzeylerine taşınıyor mu?**
     Risk: İç değerlendirme sayıları veya operasyon ayrıntıları kamusal karar dilini ağırlaştırabilir.
     Kontrol: Ortak temel ile yetkili alan bilgisinin sınırı ayrı incelenmelidir.
     Kabul sınırı: Ortak tasarım sistemi ortak veri görünürlüğü anlamına gelmez.

117. **VLR-117 — Rakip karşılaştırmaları kaynakların desteklediğinden fazlasını söylüyor mu?**
     Risk: Dar rehber örnekleri bütün şirketin güncel ürün davranışı sanılabilir.
     Kontrol: Her kaynak cümlesiyle yerel yorum ayrı etiketlenerek değerlendirilmelidir.
     Kabul sınırı: İncelenmemiş ekran, performans veya iç strateji hakkında kesin iddia kurulmaz.

118. **VLR-118 — Tasarım kararları mevcut ekran mimarisini sessizce değiştiriyor mu?**
     Risk: Yeni görsel varyant bir ek adım, portal veya zorunlu alt görev haline gelebilir.
     Kontrol: Her kararın yalnız görsel ifade mi yoksa yeni davranış mı olduğu incelenmelidir.
     Kabul sınırı: Bu belge kabul edilmiş ekranı ve akışı yeniden tasarlayamaz.

119. **VLR-119 — Belgenin uzunluğu gerçek kararların bulunmasını zorlaştırıyor mu?**
     Risk: Çok sayıda ilke arasından bir bileşenin bağlayıcı sınırı kaçırılabilir.
     Kontrol: İlke kimlikleri ve bölüm başlıklarıyla belirli karar bulma görevi değerlendirilmelidir.
     Kabul sınırı: Satır sayısı gereksiz tekrar veya çelişkili kural üretme gerekçesi değildir.

120. **VLR-120 — Öz eleştiri listesi yapılmış testlerin yerine mi geçiyor?**
     Risk: Kontrol sorularının varlığı tasarımın bütün risklerinin giderildiği şeklinde okunabilir.
     Kontrol: Sonraki değerlendirmelerde gerçek bulgu, kapsam ve tarih bu sorulardan ayrı kaydedilmelidir.
     Kabul sınırı: Bu maddeler sınama gündemidir; doğrulanmış kalite veya uygunluk sonucu değildir.

## Revision Report

İnceleme kapsamı: proje README'si, dokümantasyon dizini ve docs altındaki 00–11 numaralı kabul edilmiş referansların tamamı ile mevcut V1–V73 bölümleri, belge ilişkileri ve Visual Language Review. Tarihsel marka ve hero kararları yalnız çelişmeyen varlık sınırları için değerlendirilmiştir. İnceleme tarihi: 14 Eylül 2026.

### Düzeltilen maddeler

Aşağıdaki sekiz revizyon maddesi aynı sürümde uygulanmıştır; tekrar eden boşluk ve başlık düzeltmeleri ayrı revizyon sayılmamıştır.

1. **R01 — Başlık hiyerarşisi:** Tek belge H1'i eklendi; mevcut ana bölümler H2, alt bölümler kendi ilişkilerini koruyan H3/H4 düzeyine alındı. Bölüm sayım açıklaması buna uyarlandı.
2. **R02 — İçindekiler:** Mevcut ana bölümlere ve bu rapora bağlantılı içindekiler eklendi; bölüm sırası değiştirilmedi.
3. **R03 — Yazım ve boşluklar:** Sözcüklerle bitişen sayılar, ölçü ve katman adları, renk kodları ve sayı dizilerindeki eksik boşluklar düzeltildi. Sayısal değerler korunmuştur.
4. **R04 — Editoryal açıklık:** Yeni belge üretimi izlenimi veren kapsam cümleleri mevcut belge incelemesine uyarlandı; eski İngilizce referans adlarının kökeni belirtildi. “Sayısız kıyas”, “sonucu belirsizliği”, “Haklı gerçek medya” ve uyarının anlatıma eşlik etmesi ifadeleri düzeltildi. WCAG işaretçi hedefi ifadesi netleştirildi.
5. **R05 — Geri çekilen iddia:** V59 durum matrisindeki “Eski güvence durur” ifadesi, güvencenin korunacağı şeklinde okunmasını önlemek için “Eski güvence kaldırılır” olarak düzeltildi. Mevcut yayın ve geri çekme kararı değiştirilmedi.
6. **R06 — Kaynak kapsamı:** V72'de Airbnb'nin vergi dahil gösterim istisnası ve Booking kuralının sipariş önizlemesi kapsamı, mevcut resmî kaynaklarla uyumlu biçimde açıklaştırıldı.
7. **R07 — Sürüm kaydı:** Frontmatter sürümü 1.1 oldu; tarih korundu. Öneri ve kullanıcı incelemesi statüsü, yeni kabul verilmiş gibi değiştirilmedi.
8. **R08 — İnceleme kaydı:** Bu Revision Report eklendi; uyumluluk sonucu, korunan kararlar ve açık doğrulama işleri kaydedildi.

### Düzeltilmeyen maddeler

Aşağıdaki alanlar ayrı ayrı karşılaştırıldı. R05 ile giderilen ifade belirsizliği dışında kabul edilmiş ürün kararını değiştirmeyi gerektiren çelişki bulunmadı.

| Denetim | Referans | Sonuç |
| --- | --- | --- |
| Ürün Felsefesi | 00 | Kişinin bağlamsal kararı, düşük toplam yük ve baskısız çıkış korunuyor. |
| Bilgi Mimarisi | 01 | Keşfet ortak sonuç alanı; harita yardımcı görünüm. Yeni portal veya gezinme ailesi eklenmiyor. |
| Product Language | 02 | Amaç, tercih, zorunlu koşul ve bilgi sınırı ayrılıyor; seçim, başarı ve uygunluk eşitlenmiyor. |
| Karar Motoru | 03 | Görsel vurgu ikinci sıralama veya uygunluk otoritesi oluşturmuyor; kritik bilinmeyen olumlu hükme dönüşmüyor. |
| AI Bilgi Motoru | 05 | AI açıklaması kanıt ve yayın otoritesi değil; iç puan, ham yorum ve muhakeme kamusal görsele taşınmıyor. |
| Sistem Mimarisi | 04 | Sunum bilgi ve karar yetkisini devralmıyor; eski olumlu durum yeni değerlendirmeye taşınmıyor. Geri çekme ifadesi R05 ile açıklaştırıldı. |
| UX Akışları | 07; rota için 06 | Günlük taslak, düzenleme, kayıt, paylaşım, kesinti ve geri dönüş anlamları korunuyor; yeni onay adımı üretilmiyor. |
| Tasarım İlkeleri | 08 | Kritik bilgi, kullanıcı kontrolü, erişilebilirlik ve statik eşdeğer görsel sadelik uğruna eksiltilmiyor. |
| Design System | 10 | Renkler, tipografi, grid, aralık, radius, elevation, hedef boyutu ve hareket süreleri kaynak değerlerle uyumlu. |
| Ekran Mimarisi | 11 | Ekran sorumlulukları ve bilgi sırası korunuyor; FAB, etkinlik ve otel başlıkları yeni ekran veya özellik kabulü sayılmıyor. |

09 Ürün Ekosistemi ayrıca karşılaştırıldı: niyet, ziyaret ve Bir İz ayrımı; özel taslak, paylaşılan seçim ve bağımsız kopya sınırı; ücretsiz temel haklar ve ticari bağımsızlık korunuyor.

Teknik kontrolde tablo sütunları, başlık ilişkileri, ilke kimlikleri, iç bağlantılar, dosya adı ve frontmatter alanları incelendi. Belge içinde Mermaid veya kod bloğu yoktur; kapanmamış blok sorunu bulunmadı. Aynı üst bölüm altında yinelenen başlık veya kaldırılması gereken birebir yinelenmiş uzun paragraf bulunmadı. Farklı konulardaki ortak alt başlıklar ve bağlama göre tekrarlanan yükümlülükler korunmuştur.

Belgedeki 14 farklı yerel dosya bağlantısı mevcut dosyalara ulaşıyor. Proje README'si ve docs/README.md içindeki hedef belge bağlantıları doğru olduğundan bu dosyalar değiştirilmedi. On farklı dış kaynak adresi ve ilgili açıklamalar kontrol edildi; R06 dışındaki kaynak ifadeleri korundu. Belgedeki 20 opak renk çiftinin kontrast oranı yeniden hesaplandı ve gösterilen üç ondalıklı değerlerle eşleşti.

### Bilerek değiştirilmeyen kararlar

- V1–V73 konu sırası, 365 tasarım ilkesi ve 120 maddelik Visual Language Review korundu. Bölümler yeniden yazılmadı veya taşınmadı.
- Kilitli logo ve halka + nokta marker biçimi; kabul edilmiş sistem sans, palet, ölçüler ve süreler korundu.
- Puansız ve kanıt sınırını görünür tutan karar dili; AI'ın yardımcı rolü; harita–liste eşdeğerliği ve günlük rota kapsamı korundu.
- Ücretsiz/Premium temel kalite eşitliği, gerçek fotoğraf koşulu ve erişilebilir kontrol hakları korundu.
- İngilizce tasarım konu adları teknik başlık olarak bırakıldı; kullanıcı arayüzü etiketi veya yeni ürün kavramı olarak kabul edilmedi.
- Tarihsel kaynakların içeriği ve kabul edilmiş diğer belgeler değiştirilmedi.

### Açık bırakılan tasarım kararları

Mevcut öz eleştirilerdeki doğrulama işleri açık kalır: gerçek cihaz ve dış ışıkta okunabilirlik; büyütülmüş metin, odak, yüksek kontrast ve azaltılmış hareket; seçili/başarılı/uygun durumlarının anlaşılması; uzun adlarda kart ritmi; harita yoğunluğunda işaret ve kontrol ayrımı; platformlar arası sistem fontu ve dokunsal karşılık. Bunlar yeni tasarım önerileri veya tamamlanmış testler değildir.

Koşullu FAB, otel ve etkinlik varyantlarının uygulanabilirliği mevcut veri ve kabul edilmiş görev kapsamına bağlı kalır. Bu inceleme yeni özellik, platform kütüphanesi veya görsel varlık seçmemiştir.

### Yayınlanmaya hazır olma durumu

**Evet — belge, mevcut öneri statüsü korunarak dokümantasyon olarak yayınlanmaya hazırdır.** Açık maddeler uygulama ve kullanıcı doğrulaması kapsamındadır; metinsel yayın için çözülmemiş bir editoryal veya mimari engel saptanmamıştır. Bu sonuç ürünün uygulandığı, kullanıcılarca doğrulandığı veya WCAG uygunluğunun kanıtlandığı anlamına gelmez.
