# Şamandıra — Harita (Web) ve Mobil Yol Haritası
**Tarih:** 2026-09-05 · Sıra: önce web haritası → PWA → (mezuniyet sonrası) native app

> **Karar kaynağı:** `plan/00_brief_eki.md` §3; markır: `plan/tasarim/yon.md` §5.7.

> İlke: kullanıcı planı "web → Android → App Store" doğru; ama app'in değeri **önce web'de kanıtlanmış mobil trafiğe** bağlı. Bu doküman sırayı ve karar kapılarını tanımlar.

---

## 1. Web haritası (mobil uygulamadan ÖNCE — büyüme fazında)

Harita şu an en büyük ürün eksiği (brifte de işaretli: "yer detayında sadece Google Maps linki"). Etkisi: oturum süresi, keşif dönüşümü, rota sonucunun anlaşılırlığı — hepsi büyüme metriklerini doğrudan besler.

**Teknoloji seçimi: MapLibre GL JS** (açık kaynak, ücretsiz) — Google Maps JS API **değil**:
- Maliyet: Google Maps faturası büyür; MapLibre + ücretsiz tile (OpenFreeMap / Carto basemap) $0 başlar.
- Hukuk: K2 kararıyla uyumlu — Google ekosistemine yeni bağımlılık eklemeyiz.
- Marka: kendi şamandıra markırlarımız (`yon.md` §5.7: halka + nokta, damla pin yasak); Google pinleri jenerik.
- "Google Maps'te aç" linki **kalır** (kullanıcı alışkanlığı; ücretsiz).

Uygulama adımları (backlog B-02, doküman #07):
1. `npm i maplibre-gl` — bileşen: `site/src/components/harita/Harita.tsx` (client, dynamic import + SSR kapalı: `ssr: false`).
2. Yer detayında mini harita (yer markırı + "yakındaki yerler" noktaları) — T-10'daki `/benzer` endpoint'iyle birleşir.
3. Rota sonuç sayfasında **gün gün polyline** + numaralı şamandıra markırları; gün seçince o günün hattı vurgulanır.
4. Keşif listesinde opsiyonel "harita görünümü" (cluster) — faz 2, önce liste kalitesi.
5. Tile kaynağı: başlangıçta OpenFreeMap (key gerektirmez, adil kullanım) veya Carto (atıf zorunlu: `© OpenStreetMap contributors © CARTO` — K2 kırmızı çizgisiyle uyumlu, OSM atfı zaten footer'da). Trafik büyürse (~>100K tile isteği/gün) kendi tile sunucunuz (Oracle'da 24GB RAM var) veya ücretli sağlayıcı.
6. Performans: harita bileşeni yalnız görünen viewport'ta init; `prefers-reduced-motion` → animasyonsuz uçuş.

## 2. PWA (Faz 4 — app'ten önceki basamak)

- `manifest.json` (isim: Şamandıra, kısa ad: Şamandıra, tema renkleri, ikon seti — T-03'te üretiliyor), `apple-touch-icon`, install prompt (Android Chrome'da doğal; iOS'ta "Ana ekrana ekle" yönlendirmesi).
- Service worker: statik kabuk + son gezilen yerlerin offline önbelleği (Next 16'da `@serwist/next` veya elde minimal SW — ajan talimatı B-06'da).
- Web Share Target: paylaşılan rota linkleri uygulamadan açılsın.
- PWA, app kararının **veri toplama aracıdır**: install sayısı + geri dönüş oranı → madde 3'teki karar kapısı.

## 3. Native app karar kapısı (mezuniyet civarı, ~9. ay)

Umami verisiyle ölç:
- Mobil oturum payı **%60+** ise ve
- Mobilde rota oluşturma + paylaşım anlamlı hacme ulaştıysa ve
- PWA install/geri dönüş oranı zayıfsa (yani tarayıcı yetmiyor) → **app yatırımı meşru.**
Aksi hâlde: PWA + web'de kal, app'i ertele (öğrenci bütçesi ve zaman en kıt kaynak).

## 4. İki yol: Capacitor vs Expo/React Native

| Kriter | A) Capacitor (Next.js'i sar) | B) Expo/React Native (yeni UI) |
|---|---|---|
| Kod tabanı | Tek (mevcut site) | API katmanı ortak, UI yeniden |
| Süre (ilk sürüm) | 2-4 hafta | 8-12 hafta |
| Performans/his | WebView — iyi optimizasyonla kabul edilebilir | Native |
| Offline | SW + yerel depolama (sınırlı) | Gerçek offline (SQLite, MBTiles harita) |
| Apple riski | **Guideline 4.2** (minimum işlevsellik) — salt web sarması reddedilir; native değer ŞART | Düşük |
| Play riski | Düşük (yine de native özellik ekleyin) | Düşük |
| Öneri | **Başlangıç:** hızlı mağaza varlığı | Trafik kanıtlarsa geçiş (2. sürüm) |

**Capacitor sürümünde Apple 4.2'yi aşacak native değerler (şart):**
1. Offline rota: oluşturulan rota JSON/PDF cihazda saklanır, internetsiz açılır ("seyahatte çekmiyor" problemi — gerçek değer).
2. "Rotada" modu: konum takibiyle sıradaki durak, mesafe/süre, durak geçince otomatik ilerleme.
3. Bildirimler: rota günü sabahı hatırlatma (yerel bildirim yeterli, push altyapısı gerekmez).
4. Paylaşım: native share sheet + rota widget'ı (iOS 17+ widget, basit sürüm).
5. Harita: MapLibre native (`maplibre-react-native` Capacitor plugin'i yoksa web haritası WebView'da kalır — kabul).

## 5. Mağaza süreçleri ve maliyetler

**Google Play (önce bu — Android ağırlıklı TR pazarı):**
- Hesap: **$25 tek seferlik** (kişisel hesap yeterli; "Alegre Group" örgüt hesabı için D-U-N-S gerekir — başta kişisel, sonra örgüte taşınır).
- Gerekenler: hedef API seviyesi (güncel Android SDK), veri güvenliği formu (KVKK ile hizala — kişisel veri toplamıyorsanız beyan basit), gizlilik politikası URL (`/gizlilik` hazır olacak), mağaza görselleri (phone screenshots ×4, feature graphic 1024×500, ikon 512).
- Süreç: internal testing (20 tester e-postası) → closed → production. Yeni kişisel hesaplar production için **14 gün kapalı test** şartı var — takvime ekleyin.

**Apple App Store (ikinci — MacBook Air M2 yeterli):**
- Hesap: **$99/yıl** (Apple Developer Program, kişi veya örgüt; örgüt için D-U-N-S).
- Donanım: M2 Air 16GB **yeterli** — Xcode + iOS Simulator rahat çalışır. ⚠️ 256GB SSD dar: Xcode ~15GB + simulator runtime'ları ~8GB/adet; öneri: tek simulator runtime tutun, `DerivedData` temizleme alışkanlığı, gerekirse ~2-3 bin TL'ye harici NVMe (Xcode projeleri harici diskte sorunsuz).
- Süreç: TestFlight (iç: 100 kişi) → App Review. Red yememek için: 4.2 native değerler (yukarıda), privacy nutrition labels, ATT gerekmiyor (reklam yoksa), `UIRequiresFullScreen` yerine adaptive layout.
- Zaman gerçekçiliği: ilk review 24-48 saat; red-düzeltme döngüsüyle 2-4 hafta planlayın.

**Ortak:** mağaza ekran görüntüleri için şamandıra temalı çerçeve şablonu (Figma/Canva), tanıtım metinleri ASO'lu ("Samsun gezi rehberi", "Karadeniz rota planlayıcı" anahtar kelimeleri başlıkta/alt başlıkta).

## 6. Zaman çizelgesi (öneri)

| Dönem | İş |
|---|---|
| Ay 3-4 (web fazında) | MapLibre harita (B-02) — yer detay + rota sonucu |
| Ay 5-6 | PWA (B-06): manifest, offline kabuk, install ölçümü |
| Ay 9 (mezuniyet) | Karar kapısı: Umami mobil payı + PWA verisi → app evet/hayır |
| Ay 10-12 | Capacitor + native değerler (offline rota, rotada modu, bildirim) → **Google Play** |
| Ay 12-15 | iOS port (aynı Capacitor projesi + Mac'te build) → **App Store** |
| App sonrası | Metrikler güçlüyse Expo/React Native yeniden yazım değerlendirmesi (v2) |

## 7. Mobil için bugünden alınacak kararlar (web'i bozmadan hazırlık)

1. Rota sonuçları **paylaşılabilir link** olarak zaten var (`GET /rotalar/{id}`) — app'te de aynı API kullanılır; rota JSON şemasını dondur (versiyonla: `sema_surumu` alanı ekle).
2. API'ye `?alanlar=` benzeri dar yanıt desteği düşünülmesin — bunun yerine mobil için ayrı hafif endpoint gerekirse `/mobil/*` altında (katman kuralı bozulmadan).
3. Tasarım: mevcut Tailwind mobile-first mi doğrula (360px testleri T-14'te Playwright ile) — app WebView'ı aynı CSS'i kullanacak.
4. Durum yönetimi: app offline senaryosu için rota verisinin tam JSON'u istemciye dönüyor mu (şu an dönüyor olmalı) — offline paket buna dayanır.
