---
title: "Şamandıra — Uygulama Fark Analizi ve MVP Uygulama Planı"
version: "1.0"
status: "uygulamaya_hazir"
phase: "FAZ-15"
last_update: "2026-09-14"
depends:
  - "docs/00-product/03-karar-motoru.md"
  - "docs/00-product/04-sistem-mimarisi.md"
  - "docs/04-ai/05-ai-bilgi-motoru.md"
  - "docs/00-product/06-akilli-rota-motoru.md"
  - "docs/02-ux/07-ux-karar-akislari.md"
  - "docs/09-business/09-urun-ekosistemi.md"
  - "docs/03-design/10-design-system.md"
  - "docs/03-design/11-ekran-mimarisi.md"
  - "docs/03-design/12-gorsel-tasarim-dili.md"
  - "docs/03-design/13-bilesen-ve-etkilesim-sozlesmeleri.md"
  - "docs/09-business/14-urun-ozellik-haritasi.md"
affects:
  - "sunucu/"
  - "site/"
  - "veri/"
  - "altyapi/"
  - "gelecek Alembic migrasyonlari"
author: "Codex"
---

# Şamandıra — Uygulama Fark Analizi ve MVP Uygulama Planı

## 0. Karar özeti

Kod tabanı çalışan bir Samsun prototipidir; fakat kabul edilmiş ürünün MVP'si değildir. Toplama, eşleme, duygu/profil üretimi, PostGIS kataloğu, FastAPI, Next.js ve deterministik rota iskeleti vardır. Buna karşılık yayımlanabilir kanıt modeli, merkezi Karar Motoru, günlük rota sözleşmesi, arama, Gezeceğim Yerler, kontrollü paylaşım, offline kayıt, admin düzeltme/yayın, kimlik-güncellik kapıları ve ürün ölçümü yoktur.

Mevcut prototipin üzerine doğrudan ekran eklemek güvenli değildir. Önce kamusal veri sızıntıları ve ticari skor etkisi kapatılmalı; yer kimliği, iddia/kanıt/güncellik ve yayın uygunluğu kurulmalı; bütün aday üretimi tek karar sözleşmesine bağlanmalıdır. Bu belge, bu bağımlılığa göre **12 P0**, **20 P1–P2 çekirdek/tamamlayıcı** ve **6 P3** iş tanımlar. MVP backlog'u P0+P1+P2 toplam **32 iş**tir.

### İnceleme yöntemi ve sınırı

- Repo genelinde dosya envanteri çıkarıldı; `AGENTS.md`, README'ler, `docs/`, `sunucu/`, `site/`, `veri/`, `ortak/`, `altyapi/`, migration'lar ve testler kaynak kod üzerinden incelendi. README beyanı tek başına uygulama kanıtı sayılmadı.
- Kabul referansı olarak FAZ 14 ve kullanıcının belirttiği 03–14 belgeleri kullanıldı. Tarihsel `plan/` ve README açıklamaları yalnız mevcut prototipi anlamak için okundu.
- Kod, paket, migration ve veritabanı değiştirilmedi. PostgreSQL servisi inceleme anında çalışmadığı için canlı şema sürümü, satır sayıları ve gerçek endpoint davranışı veritabanına karşı doğrulanamadı. Alembic dosya zincirinin başı `0004_tanitim_metni`dir.
- Statik incelemeye ek olarak backend testleri **30/30 geçti**. Frontend tip kontrolü geçti; lint **0 hata/2 `<img>` optimizasyon uyarısı** verdi. Vitest başarı koduyla bitti fakat **hiç test dosyası bulmadı**; e2e test dosyası da yoktur.
- Çalışma ağacında inceleme öncesinden `README.md`, `docs/README.md` değişiklikleri ve izlenmeyen FAZ 14 belgesi vardı; bu dosyalara dokunulmadı.

## 1. Mevcut sistem envanteri

Durum sözlüğü: **VAR** kullanılabilir gerçek kod; **KISMEN VAR** iskelet veya dar davranış; **YOK** uygulanmamış; **TARİHSEL / TERK EDİLMELİ** yalnız prototip mirası; **ÜRÜN KARARIYLA ÇELİŞİYOR** kabul edilmiş davranışa aykırı aktif kod.

### 1.1. Üst seviye envanter

| Alan | Durum | Koddan doğrulanan mevcut davranış | Uygulama kararı |
|---|---|---|---|
| Backend modülleri | VAR | `sunucu/api`, `sunucu/veritabani`, `sunucu/rota_motoru`; FastAPI + SQLAlchemy 2 | Modüler monolit olarak korunabilir; yeni mantıksal sınırlar aynı deploy içinde başlayabilir. |
| Frontend/site | KISMEN VAR | Next.js 16; ana sayfa, Keşfet, Bölgeler, yer detayı, rota sihirbazı, tasarım sistemi | Kabul edilmiş ekranların az bir bölümü var; mevcut tasarım bileşenleri yeniden kullanılabilir. |
| API | KISMEN VAR | Şehir/yer/bölge okuma ve rota üretme uçları; sürümsüz, auth'suz | `/v1` kamusal sözleşmesi ve admin kapsamı ayrılmalı. |
| SQLAlchemy modelleri | KISMEN VAR | Şehir, yer, kaynak, yorum, konaklama, bölge profili, sabit rota, kullanıcı rotası | Katalog var; kanıt/iddia/yayın/sürüm/audit ve doğru kişisel kayıt modeli yok. |
| Alembic | KISMEN VAR | Doğrusal `0001`–`0004`; dosya başı `0004` | Canlı DB revizyonu bilinmiyor; ilk uygulama işi migration baseline denetimi olmalı. |
| PostgreSQL/PostGIS | VAR | `Geography(POINT,4326)`, GiST indeks ve PostGIS extension migration'da | Coğrafi aday bulma temeli uygun; canlı servis bu incelemede kapalıydı. |
| Veri kaynakları | KISMEN VAR | OSM, Google Maps, Ekşi kodu ve çıktı; TripAdvisor/Booking kodu var ama fiilî çıktı yok | Kullanım hakkı ve çıktı izni kaynak bazında modellenmeden yayın girdisi sayılamaz. |
| Veri işleme hattı | KISMEN VAR | JSONL → eşleme → duygu → profil/bölge/tanıtım → DB; manuel CLI | Çalışma koşusu, lineage, kalite kapısı, geri çekme ve idempotent batch manifest yok. |
| Yer eşleme | ÜRÜN KARARIYLA ÇELİŞİYOR | 150 m + isim 80 + kategori, union-find zinciri; otomatik kalıcı birleşim | Şube kimliği ve insan düzeltmesi olmayan zincirleme birleşim durdurulmalı. |
| Karar/puanlama | TARİHSEL / TERK EDİLMELİ | Kategori varsayımları, ilgi ağırlıkları, duygu/kaynak puanı, sponsor bonusu | Yerine zorunlu kapılar + kanıt yeterliği + bağlamsal gerekçe kullanan Karar Motoru gelmeli. |
| Günlük rota | ÜRÜN KARARIYLA ÇELİŞİYOR | 1–14 gün; Haversine, 30 km/s, 8 saat, sabit öğün slotları; otomatik kayıt | MVP tek günlük, düzenlenebilir ve gerçek geçiş/zaman kapsamını dürüstçe taşıyan nesne olmalı. |
| Arama | YOK | Ad/metin arama endpoint'i veya UI yok | Türkçe normalizasyonlu ad/tür/coğrafya araması Karar Motoru aday kaynağı olmalı. |
| Filtre | KISMEN VAR | Backend kategori/alt kategori; UI yalnız kategori chip'i | İlçe, somut koşul, zorunlu/tercih ayrımı ve filtre durum koruması yok. |
| Yorum/duygu işleme | ÜRÜN KARARIYLA ÇELİŞİYOR | BERT genel duygu + kural tabanlı konu/profil; ham metin/yazar saklanıyor ve API'ye çıkıyor | İç gözlem adayı olarak daraltılmalı; kamusal yorum/puan/duygu çıktısı kaldırılmalı. |
| Kullanıcı hesabı | YOK | Kullanıcı/oturum modeli ve auth route'u yok | Tüketici hesabı MVP dışı; temel işler hesapsız kalmalı. |
| İç auth/RBAC | YOK | Admin veya servis rolü yok | Admin P0 için ayrı kimlik, rol, nesne ve eylem yetkisi gerekli. |
| Gezeceğim Yerler | YOK | Yer niyeti deposu/eylemi yok | MVP'de cihazda sürümlü, idempotent kayıt kurulmalı. |
| Favoriler | YOK | Kalp/favori modeli veya UI yok | Ayrı Favoriler eklenmemeli; Gezeceğim ile tek niyet sözleşmesi korunmalı. |
| Rota kaydı | ÜRÜN KARARIYLA ÇELİŞİYOR | Her üretilen rota ve her alternatif anonim olarak DB'ye yazılıyor | Taslak yerelde; kalıcı kayıt açık kullanıcı eylemiyle ve hedefi belirtilerek yapılmalı. |
| Paylaşım | KISMEN VAR | `GET /rotalar/{uuid}` fiilen bilenin okuyabildiği kayıt | Önizleme, ayrı okuma/yönetim token'ı, snapshot, kapatma ve süre sonu yok. |
| Offline | YOK | Manifest var; service worker/IndexedDB/cache politikası yok | Yalnız kayıtlı temel içerik ve taslak, tarih/kapsam sınırıyla açılmalı. |
| Admin/operasyon | YOK | Admin UI, inceleme kuyruğu, yayın/geri çekme, audit yok | Kimlik, iddia, güncellik ve düzeltme için MVP P0'dır. |
| Şehir içerik sistemi | KISMEN VAR | `Sehir`, şehir ayarı, liste ve istatistik; yalnız Samsun veri koşusu | Desteklenen kapsam manifesti ve yayın durumları yok. |
| İlçe içerik sistemi | KISMEN VAR | `Yer.ilce`, bölge profili API/UI | İlçe filtresi/URL'si yok; yorum duygu profili kabul edilen kanıt modeli değil. |
| Mekân detayı | KISMEN VAR | Kimlik, fotoğraf, metin, puan/profil, harita linki | Karar bilgisi, kapsam, bilinmeyen, düzeltme yolu ve doğru şehir bağlamı eksik. |
| Test altyapısı | KISMEN VAR | 30 backend unit/sorgu testi; Vitest/Playwright konfigürasyonu | API, frontend, veri, migration, auth/admin, offline/share/e2e testleri yok. |
| Logging/gözlemlenebilirlik | KISMEN VAR | `print` ve yerel log dosyaları; framework varsayımları | Yapılandırılmış event, request/job ID, metrik, alarm ve karar izi yok. |
| Cache | KISMEN VAR | Next SSR `revalidate: 60`; tarayıcı `no-store`; model `lru_cache` | Yetkili sürüm ve geri çekmeyle invalidation yok; kişisel/ortak cache ayrımı tanımsız. |
| Güvenlik | KISMEN VAR | CORS origin env; UUID rota kimliği | Auth/rate limit/security header yok; varsayılan DB parolası, kamusal ham kişisel metin ve sınırsız yazma riski var. |

### 1.2. Backend, API ve gerçek route envanteri

| Metot ve yol | Kod | Gerçek davranış | Durum |
|---|---|---|---|
| `GET /` | `sunucu/api/uygulama.py` | Basit kök yanıt | VAR |
| `GET /sehirler` | `sunucu/api/yerler_router.py` | Aktif şehirleri döndürür | VAR |
| `GET /sehirler/{sehir}/yerler` | aynı | Kategori/offset/limit ve kamusal `sadece_kesif`; alfabetik sonuç | KISMEN VAR |
| `GET /sehirler/{sehir}/bolgeler` | aynı | Şehir/ilçe duygu profilleri | ÜRÜN KARARIYLA ÇELİŞİYOR |
| `GET /sehirler/{sehir}/istatistikler` | aynı | Yer/kategori sayıları | VAR |
| `GET /yerler/{id}` | aynı | Detay, ham örnek yorumlar ve bütün `yer_profili` | ÜRÜN KARARIYLA ÇELİŞİYOR |
| `GET /sehirler-tanimli` | aynı | OpenAPI'dan gizli tanımlı şehirler | TARİHSEL / TERK EDİLMELİ |
| `POST /rotalar/olustur` | `sunucu/api/rotalar_router.py` | 1–14 günlük plan üretir ve DB'ye kaydeder | ÜRÜN KARARIYLA ÇELİŞİYOR |
| `POST /rotalar/olustur-alternatifler` | aynı | Varyant ağırlık/koordinat kaydırmayla 2–3 plan üretir, hepsini kaydeder | ÜRÜN KARARIYLA ÇELİŞİYOR |
| `POST /rotalar/{id}/konaklama-bolgesi-oner` | aynı | Çok günlük/konaklama devamı | TARİHSEL / TERK EDİLMELİ |
| `GET /rotalar/{id}` | aynı | Sahiplik olmadan kayıtlı rotayı döndürür | ÜRÜN KARARIYLA ÇELİŞİYOR |
| `GET /sabit-rotalar` | aynı | JSONB çok günlük küratör rotaları | TARİHSEL / TERK EDİLMELİ |

Eksik uç aileleri: arama, Karar Motoru değerlendirmesi, günlük taslak CRUD/düzenleme, Gezeceğim, paylaşım önizleme/oluşturma/kapatma, admin auth, iddia/kanıt/yer kimliği inceleme, yayın/geri çekme, düzeltme bildirimi, health/readiness, metrik ve olay kabulü.

### 1.3. Veri modeli ve migration envanteri

| Model/tablo | Mevcut alanların değeri | Kritik eksik/yanlış |
|---|---|---|
| `Sehir` | Kimlik, ad/plaka/bölge, merkez, aktif | Desteklenen ürün kapsamı, yayın sürümü ve içerik durumu yok. |
| `Yer` | Şehir, ad/kategori/ilçe, konum, iletişim, JSON özellik/aktivite/fotoğraf/profil | Kalıcı canonical kimlik/şube, yayın durumu, iddia düzeyi güncellik ve kanıt bağlantısı yok. |
| `YerKaynak` | Kaynak adı/kimliği/URL; unique çift | Gerçek çekim zamanı kaybolabiliyor; kullanım hakkı, köken ailesi, kapsam, kaynak durumu yok. |
| `Yorum` | Yazar takma adı, ham metin, puan, tarih, duygu, konu ifadeleri | Kişisel/veri hakkı/saklama sınıfı yok; kamusal API'ye sızıyor; yayın kanıtı sanılıyor. |
| `BolgeProfili` | Duygu, konu, özet, yorum sayısı | Claim/evidence yerine bölge hakkında genelleyici yorum çıktısı. |
| `KonaklamaDetay` | Kaynak özellikleri | MVP günlük rota için çekirdek değil; yayımlanabilirlik kapılarına bağlı değil. |
| `SabitRota` | JSONB `duraklar` içinde günler | Günlük nesneyi çok günlük yapıya gömer; tarihsel tutulup kamusal kullanımdan çıkarılmalı. |
| `KullaniciRotasi` | JSONB tercihler/günler, konaklama önerisi | Kullanıcı/sahiplik, revision, status, explicit save, share snapshot yok; yer FK'leri JSONB'de kırılabilir. |

Migration zinciri `0001_ilk_sema` → `0002_yer_profili` → `0003_bolge_profili` → `0004_tanitim_metni` doğrusal görünür. PostGIS extension, geometry ve indeks ilk migration'dadır. Canlı DB kapalı olduğu için `alembic current`, extension sürümü, drift ve gerçek indeksler doğrulanmamıştır. Yeni şema işi tek dev migration'ına yığılmamalı; IP-01 baseline audit'inden sonra kimlik, kanıt/yayın, günlük plan, paylaşım ve admin/audit küçük geri alınabilir migration'lara bölünmelidir.

### 1.4. Veri hattı, karar ve rota ayrıntısı

- `veri/ortak/veri_yukleyiciler.py` tarih desenine uyan **bütün** ham dosyaları birlikte okur. Böylece bağımsız batch manifesti olmadan eski/yeni koşular karışır.
- İncelenen son ham/işlenmiş dosyalar 3–4 Ağustos 2026 tarihlidir: OSM 854, Google yer 1.145, Google yorum 20.162, iki Ekşi dosyası toplam 1.967; son birleşik katalog 1.719, işlenmiş yorum 22.129, yer profili 1.719, bölge profili 18 kayıttır. TripAdvisor/Booking fiilî çıktısı yoktur. Bu sayılar canlı DB kapsamını kanıtlamaz.
- `veri/esleme/eslestirici.py` aynı ana kategori + 150 m + WRatio 80 ile eşleştirir, union-find ile zincirler, koordinatları ortalar ve Google öncelikli ilk dolu alanı seçer. Son eşleme raporunda yalnız 122 çok kaynaklı küme vardır; aynı adlı farklı şubeleri birleştiren belirgin örnekler bulunur. Onay/red kararı, branch kimliği ve manuel override yoktur.
- Birleşik yer kimliği ad + yuvarlanmış ortalama koordinattan türediği için ad/koordinat değişiminde kararsızdır. Profil/tanıtım bağları kayabilir.
- `sunucu/veritabani/aktarim/yer_aktar.py` yeni birleşimde yorum ve konaklama FK'sini taşır, fakat `KullaniciRotasi.gunler` JSONB içindeki yer kimliklerini taşımaz. Yeni koşuda bulunmayan yerleri kapatma/geri çekme yoktur.
- `YerKaynak.cekilme_zamani` import anında `now()` olabilir; özgün kaynak zamanı DB'ye taşınmadığı için eski kanıt yeni görünür.
- `veri/duygu_analizi/model.py` ücretsiz yerel Türkçe BERT; konu ve profil çıkarımı kural tabanlıdır. Bunlar iyi birer **aday gözlem** aracı olabilir, ancak mevcut kod ortalama duygu ve ham örnek ifadeyi kamusal gerçek/puan gibi kullanır.
- Rota skoru ilgi, aktivite, fiyat/sakinlik, kaynak puanı, duygu ve sponsor bonusundan oluşur. Zorunlu durak `+1000` ile skor içine gömülür; ilk durak zaman bütçesine sığmasa da seçilebilir. Bilinmeyen kritik alanlara yayın/uygunluk kapısı yoktur.
- Üretim yolu `siralama.py` içindeki nearest-neighbor/2-opt'u kullanmaz; slot şablonu sıralamayı belirler. Haversine mesafesi, sabit 30 km/s ve 8 saat kullanılır; açılış, bekleme, gerçek yol, ulaşım modu, başlangıç/bitiş/dönüş ve maliyet kapsamı yoktur. Buna rağmen anlatım yürüyüş/toplu taşıma/araç rahatlığı iddiası kurar.

### 1.5. Frontend, cache, test ve operasyon ayrıntısı

- Gerçek sayfalar: `/`, `/sehir/[anahtar]`, `/sehir/[anahtar]/bolgeler`, `/sehir/[anahtar]/rota`, `/yer/[id]`, `/tasarim-sistemi`.
- Keşfet yalnız kategori chip'i ve ilk 60 sonucu taşır; arama, ilçe filtresi, somut koşul, 3–5 hedefli karar, ret/geri alma, kontrollü daha fazla ve state restore yoktur. Backend alfabetik sıralarken ekran metni deneyim sırası izlenimi verir.
- `site/src/components/ui/YerKarti.tsx`, kaynak puanı yoksa `duygu_skoru_ortalama * 5` ile kullanıcı puanı üretir; nötr duygu 0, negatif duygu negatif puan olabilir.
- `site/src/app/yer/[id]/page.tsx` “ham yorum metni yok” derken API ham metni taşır; şehir linklerini Samsun'a sabitler ve her tür yeri “konaklama üssü” yapabilir.
- `RotaSihirbazi.tsx` 1–5 gün ve ağırlık slider'ları ister; günlük niyet, tarih/saat, ulaşım, başlangıç/bitiş, zorunlu koşullar ve düzenleme yoktur.
- `site/src/lib/api.ts` sunucuda 60 saniye revalidate, tarayıcıda `no-store` kullanır. Hataları sayfalarda boş veriye çeviren akış servis hatasını “sonuç yok” gibi gösterebilir. Geri çekme için cache purge/version anahtarı yoktur.
- PWA manifesti vardır; service worker, offline veri deposu ve sync yoktur. Auth/admin/paylaşım yönetimi yoktur.
- Backend testleri skor, kümeleme, slot, kullanılmayan sıralama yardımcıları ve iki DB sorgu/slug davranışına odaklıdır. Sponsor bonusu testte açıkça beklenir. API/DB entegrasyonu README'de Swagger üzerinden manuel kabul edilir; otomatik kanıt değildir.
- CI tanımı bulunmadı. Yapılandırılmış log, karar izi, job/batch metriği, tracing, alarm, SLO ve health/readiness ucu yoktur.

## 2. Kritik ürün çelişkileri

Aşağıdaki **19** madde kaynak kodda etkin veya veri çıktısıyla doğrulanan çelişkilerdir. “Favoriler” ve Premium doğruluk katmanı kodda bulunmadığı için çelişki değil eksik/ertelenen kapsam olarak ayrıca kaydedildi.

| ID | Dosya / ilgili kod | Sorun ve çeliştiği kabul | Önem | Önerilen düzeltme |
|---|---|---|---|---|
| C-01 | `sunucu/api/semalar.py::OrnekYorum`, `sunucu/api/yerler_router.py::_ornek_yorumlari_getir` | Yazar ve ham yorum kamusal detay yanıtına giriyor. 03 §13, 04 §18, 05 §5 ve 14 M02 bunu API sınırında yasaklar. | Kritik | Public/admin DTO'larını ayır; public şemadan alanları ve sorguyu kaldır; sözleşme sızıntı testi ekle. |
| C-02 | `YerDetay.yer_profili`, `veri/duygu_analizi/yer_profili_cikarici.py` | `ornek_ifadeler` içeren tüm profil JSON'u public API'ye çıkar; ham pasaj dolaylı sızar. 04 §18 ve 05 §5 ile çelişir. | Kritik | Yalnız yayımlanmış yapılandırılmış iddialardan explicit allow-list sunum DTO'su üret. |
| C-03 | `semalar.py`, `bolgeler`, `YerKarti.tsx`, yer detay | Kaynak puanı, duygu skoru/etiketi ve yorum sayısı kullanıcıya taşınır; kart duyguya `*5` uygulayıp sahte puan üretir. 03 §13, 05 §5, 10 B03, 12 V70.1 ile çelişir. | Kritik | Kamusal puan/duygu alanlarını kaldır; gerekçe–ödün–bilinmeyen sözleşmesine geç. |
| C-04 | `sorgular.py::_KESIF_OZEL_ETIKETLERI`, `skorlama.py::_ticari_katki_hesapla` | `sponsorlu_mekan` keşif kabulüne ve skora +30 etki eder. 03 §14, 04 §0/§18, 09 ticari bağımsızlıkla çelişir. | Kritik | Ticari ilişkiyi ayrı disclosure/enventory alanına taşı; adaylık/sıra/skor etkisini sıfırla ve invariant testle kilitle. |
| C-05 | `skorlama.py::yeri_skorla`, `kumeleme.py` | Zorunlu durak +1000 puandır; yine de budanabilir, ilk durak sığmasa da seçilir. 03 §3/§5/§19 ve 06 zorunlu kapı kuralıyla çelişir. | Kritik | Hard constraint evaluator'ı skordan önce çalıştır; `uygun/uygun_degil/bilinmiyor` ve eleme nedeni üret. |
| C-06 | `skorlama.py`, `sorgular.py`, `rota_olusturucu.py` | Saat, erişim, maliyet gibi kritik bilinmeyenler olumlu aday havuzunda kalır. 03 §5, 05 §14–17, 10 B06 ile çelişir. | Kritik | İddia ailesi ve bağlama göre bilinmeyen politikası; kritik bilinmeyeni doğrulanmış eşleşmeye katmama. |
| C-07 | `Yer` modeli ve `_yer_listesi_sorgusu` | Yayın durumu, geçerlilik, kanıt yeterliği olmadan her DB yeri detay/öneri/rota adayıdır. 04 §1/§13/§17 ve 05 §16–18 ile çelişir. | Kritik | `publication_eligibility` görünümü/servisi; tüm public/query/route yollarını buraya zorunlu bağla. |
| C-08 | `RotaTalebi.gun_sayisi 1..14`, `RotaSihirbazi`, `SabitRota`, `KullaniciRotasi.gunler` | Üretim sözleşmesi çok günlüdür. 06 günlük Akıllı Rota ve 14 MVP kapsamıyla çelişir. | Kritik | Yeni günlük API/nesne kur; çok günlük uçları kamusal akıştan çıkar/deprecate et; yeni çok günlük iş yapma. |
| C-09 | `rota_olusturucu.py`, `rota_anlatim.py` | Kuş uçuşu mesafe ve sabit hızdan yürünebilir/toplu taşımalı/rahat tamamlama iddiaları çıkar; saat/dönüş/bekleme yok. 06 §5–13 ve 10 B04 ile çelişir. | Kritik | Geçiş sağlayıcı adaptörü, süre aralığı ve veri kapsamı; veri yoksa rota değil sınırlı taslak sonucu. |
| C-10 | `sorgular.py::order_by(Yer.isim)`, şehir sayfası metni, `YerKarti.tsx` | Backend alfabetik liste verirken frontend karar sırası izlenimi ve kendi puanını üretir. 03 §20 ve 04 §4 ile çelişir. | Yüksek | Sıra/gerekçe backend karar cevabından gelsin; frontend yalnız açık kullanıcı sıralamasını iletsin. |
| C-11 | `yer_aktar.py::_varsayilan_deneyim_puanlarini_uygula`, duygu ortalaması, `skorlama.py` | Kategori varsayımları ve NLP ortalaması yer-özel kanıt gibi karar/rota skoruna girer. 05 §3/§17 ve 03 kanıt/uygunluk ayrımıyla çelişir. | Kritik | Bunları aday/sinyal olarak etiketle; yayımlanmış iddia olmadan olumlu uygunlukta kullanma. |
| C-12 | `veri/esleme/eslestirici.py`; `esleme_samsun_2026-08-04.md` | Union-find zinciri aynı adlı şubeleri otomatik birleştiriyor; raporda çoklu `NOK Cafe` ve benzeri kümeler var. 03 yanlış şube kapısı, 04 §13, 05 §13/§20 ile çelişir. | Kritik | Kalıcı canonical/branch modeli, aday karar kaydı, confidence reason, manuel split/merge ve regression corpus. |
| C-13 | `veri_yukleyiciler.py`, `YerKaynak.cekilme_zamani`, aktarım | Bütün tarihli ham dosyalar karışır; import zamanı kaynak çekim zamanı olabilir. Eski kanıt yeni görünür. 05 §16 ve 04 güncellik sözleşmesiyle çelişir. | Kritik | Batch manifest + özgün event/fetch/verify/import zamanları; current snapshot seçimi ve lineage. |
| C-14 | `yer_aktar.py` | Yeni koşuda bulunmayan/kapanan kayıt emekliye ayrılmaz; türev ve rotalarda yaşamaya devam eder. 03 §7/§16, 04 düzeltme akışı, 05 §18 ile çelişir. | Kritik | Tombstone/withdrawal, impact graph, public/cache/search/route invalidation ve yeniden değerlendirme kuyruğu. |
| C-15 | `yer_aktar.py::_yerleri_birlestir`, `KullaniciRotasi.gunler` | Merge ilişkisel FK'leri taşırken JSONB rota durak kimliklerini taşımaz; GET sessizce durağı atlayabilir. 03 §16 ve 06 kayıt bütünlüğüyle çelişir. | Kritik | Durakları normalize FK tablosuna taşı; alias/redirect tablosu ve migration doğrulaması ekle. |
| C-16 | `rotalar_router.py`, `_rotayi_kaydet`, alternatif üretimi | Kimliksiz kullanıcı isteği her rota/alternatifi otomatik kalıcı yazar; UUID GET paylaşım gibi kullanılır, revoke/snapshot/sahiplik yok. 07 §12, 13 §29 ve 14 M15 ile çelişir. | Kritik | Üretim yan etkisiz taslak; açık cihaz kaydı; ayrı share snapshot/read/manage token/expiry/revoke. |
| C-17 | `GET .../yerler?sadece_kesif=false` | İstemci public boolean ile vitrin kapısını atlayıp kısıtsız katalog alabilir. 04 yayın sınırı ve 14 M02/M04 ile çelişir. | Yüksek | Public parametreyi kaldır; scope'u sunucu içi repository metodu yap; contract/auth test ekle. |
| C-18 | `site/src/lib/api.ts` ve sayfa `catch` akışları | Servis/parse hataları boş diziye dönüşebilir. 04 §3, 10 B27–B29, 13 §5–7 ile çelişir. | Yüksek | Tipli `ok/empty/insufficient/unavailable/error` sonuçları ve korunmuş retry/state UI. |
| C-19 | `site/src/app/yer/[id]/page.tsx` | Dönüş ve rota linki Samsun'a sabit; her yer “konaklama üssü” olabilir; tarihsel rota senaryosunu üretimde taşır. 11 E04/E07 ve 14 günlük rota sınırıyla çelişir. | Yüksek | Şehir bağını API kimliğinden kur; CTA'yı yer türü/karar bağlamına göre göster; konaklama senaryosunu kaldır. |

### Aranan fakat etkin çelişki bulunmayan konular

- Ayrı Favoriler uygulanmamış; bu iyi bir boşluktur. Yeni depo/kalp eklenmeden doğrudan Gezeceğim Yerler yapılmalıdır.
- Premium/ödeme uygulanmamış; ücretsiz kullanıcının daha düşük doğruluk aldığı bir kod yolu yoktur. Böyle bir ayrım eklenmemelidir.
- Kullanıcı hesabı yoktur; MVP temel akışlarının hesapsız olmasıyla uyumludur. Yalnız iç admin auth P0'dır.
- Frontend skor kırılımını şu anda rota sonucunda render etmiyor; ancak public API bunu gönderdiği için C-01/C-03 ile aynı sözleşme sızıntısı sınıfında temizlenmelidir.

## 3. FAZ 14 MVP fark matrisi

| MVP yeteneği | Mevcut | Hedef fark | Bağlı işler |
|---|---|---|---|
| Bilgi / kanıt / güncellik | Ham kaynak, yorum, profil var; claim ve yayın yok | Kaynak hakkı, observation/evidence/claim, kapsam, zaman, confidence sınıfı, yayın ve geri çekme | IP-02, 03, 04, 27, 28 |
| Karar Motoru | Ağırlıklı prototip skoru | Hard constraint → yayın uygunluğu → bağlamsal değerlendirme → gerekçe/ödün/bilinmeyen/alternatif | IP-05, 15 |
| Mekân detay | Temel içerik + yanlış puan/profil | Kimlik, amaç gerekçesi, somut bilgi, kritik sınır/bilinmeyen, düzeltme, Gezeceğim/rota eylemi | IP-01, 18 |
| Şehir | Şehir listesi ve statik sayfa | Desteklenen kapsam, yayınlı seçki ve kapsama dürüst şehir görünümü | IP-25 |
| İlçe filtresi | İlçe alanı/bölge ekranı var | Canonical ilçe, filtre, URL/state; yalnız kanıtlı içerik | IP-14, 26 |
| Arama | Yok | Türkçe ad/tür/coğrafya araması; kimlik bulma ile uygun öneriyi ayırma | IP-13 |
| Filtre | Yalnız kategori | Somut koşullar, zorunlu/tercih ayrımı, bilinmeyen ve state restore | IP-14 |
| Keşfet | Alfabetik 60'lı katalog | Aynı Karar Motorundan 3–5 hedefli seçenek, gerçek fark, sınır ve ret/undo | IP-16 |
| Bugün Ne Yapalım? | Yok | Günlük niyeti Keşfet bağlamına çeviren kısa giriş; ayrı öneri motoru değil | IP-17 |
| Günlük Akıllı Rota | Çok günlük kaba plan | Tek gün, gerçek geçiş/zaman kapsamı, düzenleme, re-evaluation, bir ana + en çok iki anlamlı alternatif | IP-07, 19, 20 |
| Gezeceğim Yerler | Yok | Hesapsız cihaz kaydı; beğeni/ziyaret/skor değil | IP-21 |
| Rota kaydı | Otomatik DB yazımı | Açık eylem, yerel taslak/kayıt, ad/aç/düzenle/kopyala/sil/undo | IP-22 |
| Offline temel | Manifest dışında yok | Kayıtlı temel içerik ve taslak; tarih/kapsam; canlı iddia yok | IP-23 |
| Salt okunur paylaşım | UUID GET | Asgari önizleme, snapshot, ayrı okuma/yönetim erişimi, revoke/expiry | IP-24 |
| Admin / düzeltme | Yok | İç auth, kimlik/iddia/güncellik kuyruğu, publish/withdraw, impact/audit | IP-08, 09 |
| Ölçüm / log | Print/framework log | Request/job/decision ID, yapılandırılmış olay, ürün/kalite metriği ve alarm | IP-10, 30 |
| Hata durumları | Hata boş veriye dönüşebiliyor | Empty/insufficient/offline/unavailable/error ayrımı, state korunumu ve güvenli retry | IP-10, 31 |

## 4. Gerçek geliştirme backlog'u

Dosya yolları beklenen dokunma alanıdır; uygulama sırasında kesin dosya adları repo kurallarına göre ayrıştırılabilir. Her iş bağımsız kabul edilebilir bir dikey veya altyapı dilimidir.

### P0 — Başlamadan düzeltilmesi gereken kritik konular

#### IP-01 — Kamusal API veri sızıntısını kapat

- **Amaç:** Ham yorum, yorumcu, duygu/puan, ham profil ifadesi ve iç skor kırılımının tarayıcıya hiç gitmemesi.
- **Beklenen dosyalar:** `sunucu/api/semalar.py`, `yerler_router.py`, `rotalar_router.py`, `site/src/lib/types.ts`, yer/bölge ekranları; yeni public-contract testleri.
- **Backend işi:** Public/admin DTO ayır; explicit allow-list response mapper; örnek yorum sorgusunu public yoldan çıkar. **Frontend işi:** Puan/duygu görünümünü ve sahte fallback skoru kaldır; gerekçe/sınır placeholder'ına geç.
- **Veri modeli / migration:** Hayır; iç ham verinin saklama hakkı IP-02'de ele alınır. **API değişikliği:** Evet, kırıcı; `/v1` ile yeni sözleşme.
- **Testler:** OpenAPI snapshot; yasak alan recursive response testi; yer/bölge/rota contract ve browser network assertion.
- **Bağımlılıklar / risk:** Bağımlılık yok. Eski UI kırılır; backend+frontend aynı PR/dalga içinde geçmelidir.
- **Kabul kriteri:** Public JSON, HTML, accessibility metni ve paylaşım önizlemesinde yasak alanlar yok; admin dışı role ham veri verilmez.

#### IP-02 — Kaynak, kanıt, iddia ve güncellik çekirdeğini kur

- **Amaç:** Ham girdiyi yayımlanmış bilgiden ayırmak; her iddianın kapsamını, kökenini, zamanını ve durumunu izlemek.
- **Beklenen dosyalar:** `sunucu/veritabani/modeller.py`, yeni `sunucu/bilgi/`, `sunucu/veritabani/migrasyonlar/versions/`, `veri/ortak/*`, aktarım mapper'ları.
- **Backend işi:** `KaynakPolitikasi`, `VeriBatch`, `Gozlem`, `KanitBaglantisi`, `Iddia`, `IddiaSurumu`, `YayinDurumu` servislerini ekle. **Frontend işi:** Yok; yalnız tiplenen kamusal sınır IP-15/18'de.
- **Veri modeli / migration:** Evet; additive tablolar, event/fetch/verify/import zamanları, scope, claim family, knowledge state, confidence class, valid interval, rights/use policy.
- **API değişikliği:** İç admin/bilgi API'si eklenir; public henüz yalnız IP-01 allow-list. **Testler:** State transition, provenance, temporal scope, rights gate ve geri çekme unit/integration testleri.
- **Bağımlılıklar / risk:** IP-11. Aşırı genel EAV modeli kaçınılmalı; ilk claim aileleri MVP koşullarıyla sınırlı tutulmalı.
- **Kabul kriteri:** Kamusal her somut iddia aktif sürüm ve izinli kanıta izlenir; `bilinmiyor/çelişkili/eskimiş` ayrı; tek “güncellendi” tarihi doğruluk yerine geçmez.

#### IP-03 — Canonical yer ve şube kimliğini düzelt

- **Amaç:** Aynı adlı farklı şubeyi ayırmak, yanlış birleşimi geri alınabilir yapmak ve kimliği kaynak/ad/koordinat değişiminden bağımsızlaştırmak.
- **Beklenen dosyalar:** `modeller.py`, `veri/esleme/eslestirici.py`, `veri/ortak/yer_modeli.py`, `yer_aktar.py`, yeni kimlik servisi/admin ekranı.
- **Backend işi:** Kalıcı `YerKimligi`, `Sube`, `YerAlias`, `EslemeKarari` ve merge/split servisi; geçiş alias'ı. **Frontend işi:** Aynı ad şube ayırıcı kimlik satırı; kaldırılmış/taşınmış kayıt durumu.
- **Veri modeli / migration:** Evet; stable UUID, alias, candidate pair, decision/audit ve normalized referanslar. **API değişikliği:** Evet; canonical id ve redirect/replaced durumu.
- **Testler:** Bilinen doğru/yanlış çift regression corpus; transitive-chain, split, merge, idempotency ve route/share reference testleri.
- **Bağımlılıklar / risk:** IP-11; IP-09 insan incelemesi. Hatalı otomatik migration veri kaybı yaratabilir; dry-run + örneklem gate zorunlu.
- **Kabul kriteri:** Belirsiz çift otomatik kalıcı birleşmez; örnek yanlış şubeler ayrılır; eski kimlik doğru canonical kayda yönlenir; hiçbir kayıtlı nesne sessiz durak kaybetmez.

#### IP-04 — Yayın uygunluğu, geri çekme ve etki yayılımını tek kapı yap

- **Amaç:** Eski, hak dışı, yanlış kimlikli veya geri çekilmiş bilginin arama, detay, karar, rota, paylaşım ve cache'de yaşamamasını sağlamak.
- **Beklenen dosyalar:** yeni `sunucu/yayin/`, `sorgular.py`, bütün router'lar, `site/src/lib/api.ts`, pipeline/aktarim kodu.
- **Backend işi:** Merkezi `yayinlanabilir_mi`/query scope; tombstone; impact graph ve re-evaluation queue. **Frontend işi:** Withdrawn/limited durumları ve mevcut seçimi koruyan uyarı.
- **Veri modeli / migration:** Evet; publication/withdrawal reason, affected object, invalidation event. **API değişikliği:** Evet; durum/sürüm/ETag ve kontrollü `410/limited` cevapları.
- **Testler:** Bir iddia/yer geri çekildiğinde tüm tüketicilerde invariant; cache invalidation; saved/share snapshot correction tests.
- **Bağımlılıklar / risk:** IP-02, IP-03. Fan-out ve yarış koşulu; outbox/idempotent consumer kullanılmalı.
- **Kabul kriteri:** Public/route sorgularında kapıyı atlayan kod yolu yok; kritik düzeltme ölçülen süre içinde tüm online çıktılarda olumlu iddiayı durdurur.

#### IP-05 — Karar bağlamı ve hard-constraint çekirdeğini kur

- **Amaç:** Zorunlu koşulları skordan ayırmak ve bilinmeyeni doğru üç durumlu mantıkla değerlendirmek.
- **Beklenen dosyalar:** yeni `sunucu/karar_motoru/`; `sunucu/api/semalar.py`; tarihsel `rota_motoru/skorlama.py` adaptörü/testleri.
- **Backend işi:** `KararBaglami`, amaç, tercih, zorunlu koşul, ret, geografi ve zaman; `uygun/uygun_degil/degerlendirilemiyor`; reason codes. **Frontend işi:** Anlaşılan koşul özeti ve zorunlu/tercih düzenleme modeli.
- **Veri modeli / migration:** Karar izleri için evet; ham hassas bağlamı asgari tut. **API değişikliği:** Evet; versioned context ve evaluation contract.
- **Testler:** Property/invariant: hiçbir yumuşak avantaj hard fail'i telafi etmez; unknown true/false değildir; sponsor sonucu değiştirmez.
- **Bağımlılıklar / risk:** IP-02, IP-04. MVP'de koşul ailesini sınırlamazsa kapsam büyür.
- **Kabul kriteri:** Her aday için kapı sonucu ve eleme nedeni var; bilinmeyen kritik koşul doğrulanmış eşleşmede yok; aynı bağlam aynı politika sürümünde deterministik.

#### IP-06 — Sponsor ve ticari sinyali organik karardan ayır

- **Amaç:** Ücretli ilişkiyi şeffaf fakat organik uygunluk ve güven dışında tutmak.
- **Beklenen dosyalar:** `sorgular.py`, `rota_motoru/skorlama.py`, `ortak/sabitler.py`, ilgili testler; gelecekte ticari presentation DTO.
- **Backend işi:** Sponsor filtre/bonusunu kaldır; ticari metadata'yı ayrı açıklama alanı olarak taşı. **Frontend işi:** Yalnız gerçekten etkin ticari içerikte açık etiket; organik karta görsel üstünlük yok.
- **Veri modeli / migration:** Mevcut etiketi karardan ayırmak için zorunlu değil; ileride kampanya modeli P3. **API değişikliği:** İç skor alanı kaldırılır, disclosure ayrı alan olabilir.
- **Testler:** Sponsor bayrağı açık/kapalı aynı organik adaylık ve sırayı verir; snapshot ve regression.
- **Bağımlılıklar / risk:** IP-01. Eski test/fixture beklentileri değişir.
- **Kabul kriteri:** Kod aramasında sponsorun filtre/skor/rank etkisi yok; ticari ekip güven/yayın/uygunluğu değiştiremez.

#### IP-07 — Çok günlük prototipi günlük MVP sınırına al

- **Amaç:** Aktif ürün sözleşmesini tek günlük Akıllı Rota yapmak; çok günlük Akıllı Gezi'yi uygulamamak.
- **Beklenen dosyalar:** `semalar.py`, `rotalar_router.py`, `rota_olusturucu.py`, `RotaSihirbazi.tsx`, route README ve deprecation notları.
- **Backend işi:** Yeni günlük draft/evaluate uçları; `gun_sayisi` ve konaklama bölgesi akışını public v1'den çıkar. **Frontend işi:** Gün seçiciyi/konaklama senaryosunu kaldır; günlük niyet girişi.
- **Veri modeli / migration:** IP-19/22 ile evet; eski tablolar hemen silinmez, salt tarihsel okunur. **API değişikliği:** Evet, kırıcı `/v1/gunluk-planlar`.
- **Testler:** Public OpenAPI'da çok günlük create yok; günlük input/output contract; legacy route çağrısına kontrollü deprecation/kapama.
- **Bağımlılıklar / risk:** IP-01. Var olan demo davranışı kaybolur; feature flag yerine net public sınır tercih edilmeli.
- **Kabul kriteri:** MVP ekranı/API'si birden çok gün üretemez; eski veriler korunur ama yeni ürün sonucu sayılmaz.

#### IP-08 — İç admin kimliği, RBAC ve audit sınırını kur

- **Amaç:** Ham kanıt, kimlik düzeltme ve yayın eylemlerini public kullanıcıdan ayırmak.
- **Beklenen dosyalar:** yeni `sunucu/auth/`, `sunucu/admin/`, admin route'ları ve ayrı `site/src/app/admin/` kabuğu; secret/config.
- **Backend işi:** Admin session/OIDC veya güvenli küçük ekip auth, roller, object/action authorization, CSRF/rate limit, immutable audit. **Frontend işi:** Giriş ve yetkisiz/hata durumları; public bundle'dan ayrık admin alanı.
- **Veri modeli / migration:** Evet; admin user/role/grant/audit event. **API değişikliği:** Evet; `/v1/admin/*`, public OpenAPI/security sınırı ayrı.
- **Testler:** AuthN/AuthZ matrix, IDOR, session expiry, audit immutability, admin DTO leak tests.
- **Bağımlılıklar / risk:** IP-11; teknoloji seçimi deploy ortamıyla doğrulanmalı. Tüketici hesabıyla birleştirilmemeli.
- **Kabul kriteri:** Public kimlik ham kanıta/yayına erişemez; her kritik işlem aktör-zaman-gerekçe-etki taşır; varsayılan deny.

#### IP-09 — Minimum admin düzeltme ve yayın iş akışını kur

- **Amaç:** Yanlış şube, çelişki, güncellik ve geri çekmeyi kod/SQL müdahalesi olmadan yönetmek.
- **Beklenen dosyalar:** `sunucu/admin/`, `sunucu/bilgi/`, `site/src/app/admin/*`, yeni admin bileşenleri.
- **Backend işi:** İnceleme kuyruğu, claim/identity case, evidence side-by-side, preview, approve/narrow/withdraw/split/merge, impact. **Frontend işi:** E27–E29'un MVP alt kümesi.
- **Veri modeli / migration:** IP-02/03/08 tablolarına case, assignment, decision ve optimistic version ekleri. **API değişikliği:** Evet; idempotent admin commands.
- **Testler:** State machine, concurrent edit, second-review-required, rollback/withdraw propagation, accessibility smoke.
- **Bağımlılıklar / risk:** IP-02, 03, 04, 08. Büyük CMS yapılmamalı; yalnız MVP yayın/düzeltme görevleri.
- **Kabul kriteri:** Operatör yanlış şubeyi ayırabilir, iddiayı daraltıp geri çekebilir, etkiyi önizleyebilir; ticari bonus veremez.

#### IP-10 — Güvenlik, hata ve gözlemlenebilirlik tabanını kur

- **Amaç:** Sessiz hata, sınırsız anonim yazma ve izlenemeyen karar/iş koşusunu engellemek.
- **Beklenen dosyalar:** `uygulama.py`, router'lar, config, logging middleware, `site/src/lib/api.ts`, error UI; deployment config.
- **Backend işi:** Request/correlation ID, structured log, typed errors, health/readiness, body/timeout/rate limits, güvenli CORS/header, secret fail-fast. **Frontend işi:** empty/insufficient/offline/unavailable/error ayrımı ve state-preserving retry.
- **Veri modeli / migration:** Audit/outbox dışında hayır. **API değişikliği:** Evet; error envelope, idempotency key ve health uçları.
- **Testler:** Rate-limit, CORS, secret config, duplicate command, error mapping, no-sensitive-log, outage browser tests.
- **Bağımlılıklar / risk:** IP-01/08 ile paralel. PII'nin loga sızması ve yüksek cardinality engellenmeli.
- **Kabul kriteri:** Teknik hata boş liste olmaz; write endpoint idempotent/sınırlı; request-job-decision zinciri aranabilir; varsayılan DB parolası prod'da çalışmaz.

#### IP-11 — Migration ve canlı şema baseline denetimi

- **Amaç:** Dosyadaki `0004` ile gerçek geliştirme/staging DB'lerini karşılaştırıp güvenli schema evolution başlangıcı oluşturmak.
- **Beklenen dosyalar:** `alembic.ini`, migration env/versions, yeni read-only audit scripti ve runbook; CI kontrolü.
- **Backend işi:** `alembic current/heads/history`, PostGIS/index/constraint/drift raporu; backup/restore ve downgrade stratejisi. **Frontend işi:** Yok.
- **Veri modeli / migration:** Bu iş migration çalıştırmaz; sonraki migration'ların baseline'ını ve sırasını onaylar. **API değişikliği:** Hayır.
- **Testler:** Boş DB upgrade, production-like snapshot upgrade, downgrade where safe, model-vs-schema diff.
- **Bağımlılıklar / risk:** Çalışır DB erişimi gerekli. İnceleme anında servis kapalı olduğu için ilk gerçek uygulama gününün kapısıdır.
- **Kabul kriteri:** Her ortamın revizyonu kayıtlı; drift yok veya düzeltme planı var; PostGIS/indeksler doğrulanmış; migration çalıştırma/geri dönüş runbook'u onaylı.

#### IP-12 — P0 invariant testleri ve CI kalite kapısı

- **Amaç:** Bugünkü çelişkilerin geri gelmesini merge öncesi engellemek.
- **Beklenen dosyalar:** backend test klasörleri, `site/src/**/*.test.tsx`, `site/e2e/`, CI workflow, test fixture/corpus.
- **Backend işi:** Public contract, sponsor, hard constraint, publication gate, branch identity, withdrawal tests. **Frontend işi:** Search/empty/error, forbidden data, route daily boundary smoke tests.
- **Veri modeli / migration:** Test DB fixture gerekir; migration yok. **API değişikliği:** Hayır, sözleşmeleri doğrular.
- **Testler:** İşin kendisi; unit + integration + contract + minimal e2e, deterministic seed.
- **Bağımlılıklar / risk:** IP-01–11 ile kademeli. Gerçek scraper/network CI'da kullanılmamalı; sabit lisanslı fixture.
- **Kabul kriteri:** CI format/lint/type/backend/frontend/migration/contract/e2e kapılarını koşturur; test yokken yeşil sayılmaz; P0 invariant ihlali merge'i durdurur.

### P1 — MVP çekirdeği

#### IP-13 — Türkçe arama ve aday getirme API'si

- **Amaç:** Yer adı, tür ve coğrafyayı hızlı bulmak; adla bulmayı uygun öneriyle karıştırmamak.
- **Beklenen dosyalar:** yeni `sunucu/arama/`, `sorgular.py`, API router/schema, `site/src` arama sayfası/bileşenleri.
- **Backend işi:** Türkçe case/diacritic normalizasyonu, prefix/fuzzy sınırı, il/ilçe/tür, pagination ve scope. **Frontend işi:** E03/B07; debounce, son sorgu kazanır, klavye/a11y, state restore.
- **Veri modeli / migration:** PostgreSQL extension/index kararı için evet olabilir (`pg_trgm`, normalized column/index). **API değişikliği:** Evet, `GET /v1/arama`.
- **Testler:** Türkçe İ/ı/ş/ğ, typo, aynı ad şube, pagination, stale response, scope/publication filter.
- **Bağımlılıklar / risk:** IP-03/04/05. Fuzzy arama yanlış kimliği üst sıraya çıkarabilir.
- **Kabul kriteri:** Kimlik sonuçları ile bağlamsal öneriler tipte ayrıdır; yalnız yayınlanabilir yer döner; p95 hedefi pilotta ölçülür.

#### IP-14 — İlçe ve somut koşul filtre sözleşmesi

- **Amaç:** Kategori, ilçe ve MVP koşullarını görünür, korunur ve zorunlu/tercih ayrımıyla uygulamak.
- **Beklenen dosyalar:** Karar/search API, `site` filter components, URL/state yönetimi.
- **Backend işi:** Canonical filter definitions; unknown/hard condition semantics; facet count yalnız izinli küme. **Frontend işi:** B06/13 §10, apply/cancel/clear, active summary, geri dönüş koruması.
- **Veri modeli / migration:** İlçe canonicalization IP-03 ile gerekebilir. **API değişikliği:** Evet; typed filter/context.
- **Testler:** İlçe/kategori bileşimi, bilinmeyen zorunlu koşul, clear kapsamı, URL roundtrip, a11y keyboard.
- **Bağımlılıklar / risk:** IP-03/05/13. Verisi olmayan filtre UI'da sunulmamalı.
- **Kabul kriteri:** Sonuç bağlamı uygulanan filtreleri aynen taşır; zorunlu koşul sessiz gevşemez; geri dönüşte sorgu/filtre/konum korunur.

#### IP-15 — Kamusal Karar Sonucu sözleşmesi

- **Amaç:** Bütün kanallara aynı gerekçe, ödün, bilinmeyen, kapsam ve alternatif farkını vermek.
- **Beklenen dosyalar:** `sunucu/karar_motoru`, `api/semalar.py`, `site/src/lib/types.ts`, karar kartları.
- **Backend işi:** `KararSonucu`: understood need, eligibility, reasons, blockers/tradeoffs, unknowns, validity/scope, action, trace ref. **Frontend işi:** B03/B39 anlam sırasını değiştirmeden render.
- **Veri modeli / migration:** Karar izi için evet; ham konum/özel metni varsayılan saklama. **API değişikliği:** Evet, değerlendirme/search/discover ortak envelope.
- **Testler:** JSON schema, reason-code localization, no internal score/raw evidence, cross-channel snapshot.
- **Bağımlılıklar / risk:** IP-01/02/04/05. Serbest metin gerekçe yeni gerçek uydurmamalı.
- **Kabul kriteri:** Frontend yeniden sıralama/puan üretmez; aynı decision id her kanalda aynı kapsamı taşır; teknik hata ayrı sonuçtur.

#### IP-16 — Keşfet'i Karar Motoruna bağla

- **Amaç:** 60'lı alfabetik katalog yerine 3–5 hedefli, gerekçeli ve sınırları görünür seçenek sunmak.
- **Beklenen dosyalar:** yeni discover endpoint/orchestrator; şehir page/components; state/analytics.
- **Backend işi:** Context → search candidates → decision evaluate → diversity/alternative difference; ret context. **Frontend işi:** E02; card/list/map eşdeğeri, uymuyor/undo, controlled more.
- **Veri modeli / migration:** Ret/decision trace için minimal event. **API değişikliği:** Evet, `POST /v1/kesfet/degerlendir` veya eşdeğeri.
- **Testler:** 3–5 hedef kuralı, az bilgiyle sayı doldurmama, sponsor invariance, ret/undo, pagination stability.
- **Bağımlılıklar / risk:** IP-13/14/15. Diversity ikinci gizli skor motoru olmamalı.
- **Kabul kriteri:** Her kartın gerçek gerekçe ve kritik sınırı var; yayın dışı/unknown hard koşullu aday yok; istemci kendi önerisini üretmiyor.

#### IP-17 — “Bugün Ne Yapalım?” kısa karar girişi

- **Amaç:** Günlük niyeti az soruyla Keşfet bağlamına dönüştürmek; ayrı öneri motoru yaratmamak.
- **Beklenen dosyalar:** ana sayfa, intent form/components, Karar context API.
- **Backend işi:** Yapılandırılmış hızlı niyet; opsiyonel metin ayrıştırma yalnız aday; netleştirme gereksinimi. **Frontend işi:** Amaç/şehir ve yalnız karar değiştiren koşular; login/konum zorunlu değil.
- **Veri modeli / migration:** Hayır; kısa ömürlü context/trace. **API değişikliği:** IP-15 context create/evaluate.
- **Testler:** Eksik şehir, unknown condition, clarification, manual fallback, late response and privacy.
- **Bağımlılıklar / risk:** IP-05/15/16. Chatbot kapsamına dönüşmemeli.
- **Kabul kriteri:** Sonuç IP-16 ile aynı motor/sözleşmedir; anlaşılmayan koşul düşmez; LLM kapalıyken yapılandırılmış akış çalışır.

#### IP-18 — Mekân detayını karar birimi yap

- **Amaç:** Yeri puansız, kanıtlı pratik bilgi, kritik sınır ve doğru eylemlerle göstermek.
- **Beklenen dosyalar:** `GET /v1/yerler/{id}`, `site/src/app/yer/[id]`, B03/B39/B41 bileşenleri.
- **Backend işi:** Public claim projection, current context evaluation, alternative max 3, correction link. **Frontend işi:** Doğru şehir linki; Gezeceğim, yol tarifi, bağlama uygun günlük rota; conditional lodging behavior yok.
- **Veri modeli / migration:** IP-02/03 kullanır. **API değişikliği:** Evet, yeni detail contract/slug yönlendirme kararı.
- **Testler:** No forbidden fields, wrong city, branch identity, withdrawn/limited/unknown, keyboard/a11y, SEO metadata scope.
- **Bağımlılıklar / risk:** IP-03/04/15/21. SEO slug migration'ı canonical id'yi gölgelememeli.
- **Kabul kriteri:** Sayfa ad/tür/konum/gerekçe/sınır/kapsam taşır; puan/duygu/yorum yok; eylemler mevcut yer türü ve bağlamla doğru.

#### IP-19 — Gerçek geçiş kapsamlı günlük rota üretimi

- **Amaç:** Bir günü zaman, başlangıç/bitiş, ulaşım ve dönüş kapsamıyla savunulabilir taslak/rota olarak değerlendirmek.
- **Beklenen dosyalar:** yeni `sunucu/rota/` veya mevcut motor refactor; transition provider adapter/cache; daily API; route UI.
- **Backend işi:** Tek gün input; opening/visit/wait/transition/return windows; real road provider adapter; infeasible/limited result; one main + max two meaningful alternatives. **Frontend işi:** Günlük rota kartı ve kapsam özeti.
- **Veri modeli / migration:** Evet; `GunlukPlan`, revision, stop, leg, constraint, evaluation. **API değişikliği:** Evet, `/v1/gunluk-planlar/*`.
- **Testler:** Time windows, return included/excluded, unknown transport, provider outage, hard constraint, route invariant and golden scenarios.
- **Bağımlılıklar / risk:** IP-05/07/15. Ücretsiz/düşük maliyet için sağlayıcı adaptörü ve cache; sağlayıcı yoksa kesin rota iddiası yok.
- **Kabul kriteri:** Kuş uçuşu mesafeden yürüyüş/toplu taşıma vaadi üretilmez; toplamın kapsamı görünür; sığmayan seçili yerler kaybolmaz.

#### IP-20 — Günlük rota düzenleme ve yeniden değerlendirme

- **Amaç:** Ekle/kaldır/sırala/sabitle işlemlerini geri alınabilir yapmak ve bütün gün etkisini yeniden hesaplamak.
- **Beklenen dosyalar:** daily plan command API, route editor components, optimistic state/version handling.
- **Backend işi:** Revisioned idempotent commands; stop/time/order locks; async/sync reevaluate; stale response rejection. **Frontend işi:** E08/13 §15; drag + accessible move, undo, pending/limited states.
- **Veri modeli / migration:** IP-19 tablolarına event/revision/lock. **API değişikliği:** Evet; command endpoints with expected revision/idempotency.
- **Testler:** Concurrent edit, stale response, remove last stop, undo, hard constraint conflict, offline local edit handoff.
- **Bağımlılıklar / risk:** IP-19. Otomatik yeniden doldurma kullanıcının iradesini ezmemeli.
- **Kabul kriteri:** Her değişiklik yeni revision; son durak kaldırılınca boş taslak; sabit koşul sessiz değişmez; eski değerlendirme yeni taslağı ezmez.

#### IP-21 — Gezeceğim Yerler cihaz kaydı

- **Amaç:** Kullanıcının “sonra gitmek istiyorum” niyetini hesapsız ve beğeni/ziyaretten ayrı saklamak.
- **Beklenen dosyalar:** `site/src/lib/depolama/*`, Gezeceğim sayfası, yer/kart eylemleri, storage schema/migrations.
- **Backend işi:** MVP'de yok; public place revalidation endpoint kullanılır. **Frontend işi:** Versioned IndexedDB tercihli depo, add/remove/undo/open, storage failure and device scope.
- **Veri modeli / migration:** Sunucu hayır; local schema version evet. **API değişikliği:** Yeni özel write yok; batch place refresh gerekebilir.
- **Testler:** Idempotent add, remove/undo, quota/private mode, withdrawn place, schema upgrade, no ranking side effect.
- **Bağımlılıklar / risk:** IP-04/18. Tarayıcı temizliği ve cihaz kapsamı dürüst anlatılmalı.
- **Kabul kriteri:** İşlem gerçekten diske yazılmadan başarı yok; ayrı Favoriler oluşmaz; kayıt öneri sırasını değiştirmez; hesap gerektirmez.

#### IP-22 — Açık eylemli rota taslak/kayıt yaşam döngüsü

- **Amaç:** Otomatik DB yazımını kaldırıp boş/tarihsiz günlük taslağı cihazda adlandırma, açma, kopyalama ve silme ile saklamak.
- **Beklenen dosyalar:** route editor/storage, legacy save removal, local record list and lifecycle UI.
- **Backend işi:** Route evaluation yan etkisiz; share dışında kullanıcı planını MVP'de zorunlu sunucuya yazma. **Frontend işi:** Draft autosave kapsamı, explicit save, rename/duplicate/delete/undo.
- **Veri modeli / migration:** Local normalized schema; server legacy rows korunur fakat yeni yazılmaz. **API değişikliği:** Create/evaluate ayrılır; GET UUID legacy public olmaz.
- **Testler:** Reload recovery, storage fail, duplicate id, delete/undo, outdated place re-evaluation, no alternative persistence.
- **Bağımlılıklar / risk:** IP-07/19/20. Autosave ile “kaydedildi” anlamı karışmamalı.
- **Kabul kriteri:** Rota üretmek uzak kalıcı kayıt oluşturmaz; kullanıcı kayıt hedefini bilir; boş/tarihsiz/limited draft saklanabilir, değerlendirme durumu silinmez.

#### IP-23 — Offline temel davranış

- **Amaç:** Daha önce cihazda kaydedilmiş yer/rotayı tarihli ve sınırlı olarak açmak; canlı uygunluk uydurmamak.
- **Beklenen dosyalar:** service worker/PWA config, storage/cache policy, offline UI B29/E26, network state adapter.
- **Backend işi:** Cacheable public projection için version/ETag; revalidation. **Frontend işi:** App shell + explicit saved snapshot; local draft edit; pending action semantics.
- **Veri modeli / migration:** Server hayır; local cache schema/version. **API değişikliği:** Conditional GET/ETag ve batch revalidate olabilir.
- **Testler:** Browser offline e2e, cache miss/hit, stale/withdrawn reconnect, pending share close not falsely complete, no live claim.
- **Bağımlılıklar / risk:** IP-04/10/21/22. Service worker eski olumlu bilgiyi uzun süre tutabilir; allow-list cache.
- **Kabul kriteri:** Offline yalnız gerçekten yereldeki kayıt açılır; son alınma zamanı iddia doğrulama zamanı sanılmaz; reconnect güncel geri çekmeyi uygular.

#### IP-24 — Salt okunur paylaşım snapshot'ı

- **Amaç:** Günlük planı asgari içerikle, hesap/app zorunluluğu olmadan, yönetilebilir ve geri çekilebilir paylaşmak.
- **Beklenen dosyalar:** share model/service/router, public share page, owner preview/manage UI, token utilities.
- **Backend işi:** Immutable snapshot revision, unguessable read token, separate hashed manage secret, expiry/revoke, correction overlay, rate limit. **Frontend işi:** Scope preview; copy/link; recipient read-only; close/update.
- **Veri modeli / migration:** Evet; `Paylasim`, `PaylasimSurumu`, token hash, status/expiry. **API değişikliği:** Evet; preview/create/read/update/revoke, idempotency.
- **Testler:** Token separation/entropy, IDOR, private field exclusion, revoke/expiry, route delete, correction propagation, no-login recipient.
- **Bağımlılıklar / risk:** IP-04/08/10/15/22. Ev/otel konumu ve özel koşul sızıntısı yüksek risk.
- **Kabul kriteri:** Read token yönetemez; varsayılan özel alanlar yok; paylaşım açık kullanıcı eylemidir; kapalı link bilgi sızdırmadan kapalı görünür.

### P2 — MVP tamamlayıcı

#### IP-25 — Şehir kapsamı ve yayın manifesti

- **Amaç:** “Samsun var” ile hangi görev/ilçe/iddia ailelerinin gerçekten desteklendiğini ayırmak.
- **Beklenen dosyalar:** `Sehir`/scope modelleri, city API, şehir sayfası ve admin scope control.
- **Backend işi:** City coverage manifest; published claim/decision coverage counters. **Frontend işi:** E05; desteklenen kapsam, az/veri yok durumu ve Keşfet girişi.
- **Veri modeli / migration:** Evet; city capability/scope/version. **API değişikliği:** Evet, city detail/capabilities.
- **Testler:** Kısmi ilçe/özellik kapsamı, disabled city, no false total coverage, cache invalidation.
- **Bağımlılıklar / risk:** IP-02/04/09. Sayıların kalite/uygunluk puanı gibi sunulması engellenmeli.
- **Kabul kriteri:** Şehir ekranı kapsanmayan görevi varmış gibi göstermez; ikinci şehir eklemek kod sabiti gerektirmez.

#### IP-26 — İlçe sayfası ve canonical coğrafya

- **Amaç:** İlçe filtresi ve içerik sayfasını yorum duygu genellemesi yerine yayımlanmış bilgiyle kurmak.
- **Beklenen dosyalar:** location model/query, district API/route, E06 sayfası, URL/state.
- **Backend işi:** Canonical district id/slug, geometry/containment, publication projection. **Frontend işi:** İlçe görünümü ve Keşfet'e korunmuş filtreyle dönüş.
- **Veri modeli / migration:** Evet olabilir; ilçe tablosu/geometry/alias. **API değişikliği:** Evet, `/v1/sehirler/{sehir}/ilceler/{ilce}`.
- **Testler:** Slug/alias, wrong city, location boundary, no sentiment fields, back-state.
- **Bağımlılıklar / risk:** IP-03/14/25. Metin kaynak kapsamını aşmamalı.
- **Kabul kriteri:** İlçe kimliği string serbest metin değildir; sayfa yalnız yayınlı bilgi taşır; filtre aynı canonical id'yi kullanır.

#### IP-27 — Veri batch orkestrasyonu ve kalite kapısı

- **Amaç:** Tarihli dosyaları rastgele karıştırmadan tekrarlanabilir, gözlenebilir ve yayın öncesi kapılı veri koşusu yapmak.
- **Beklenen dosyalar:** `veri/toplayicilar`, `veri/ortak/veri_yukleyiciler.py`, pipeline entrypoints, manifests/reports, ops runbook.
- **Backend işi:** Batch manifest, stage state, checksums, current input selection, retry/dead-letter, import dry-run. **Frontend işi:** Yok; admin job status küçük görünüm olabilir.
- **Veri modeli / migration:** IP-02 `VeriBatch`; ek job/outbox tabloları. **API değişikliği:** Yalnız admin job/status.
- **Testler:** Rerun/idempotency, two-date isolation, partial failure, schema validation, deterministic output, rights gate.
- **Bağımlılıklar / risk:** IP-02/03/09/10. Scraper koşusu CI'da canlı kaynağa bağlanmamalı.
- **Kabul kriteri:** Her yayımlanmış sürüm tek manifest/input setine izlenir; eski batch kendiliğinden yeniye karışmaz; kalite gate geçmeden import/yayın yok.

#### IP-28 — NLP çıktısını gözlem adayı sınırına çek

- **Amaç:** Mevcut düşük maliyetli BERT/kural kodunu koruyup onu gerçek/yayın/uygunluk otoritesi olmaktan çıkarmak.
- **Beklenen dosyalar:** `veri/duygu_analizi/*`, output models, claim candidate mapper, evaluation fixtures.
- **Backend işi:** Sentiment/topic/profile → `AdayGozlem` with span/time/place/source; no average place score; minimum support only queue priority. **Frontend işi:** Public değişiklik yok.
- **Veri modeli / migration:** IP-02 gözlem/kanıt tabloları; raw retention policy. **API değişikliği:** Admin candidate review only.
- **Testler:** Turkish negation/aspect corpus, false branch attachment, time/scope, no automatic publish, model version/reproducibility.
- **Bağımlılıklar / risk:** IP-02/03/09/27. Yorum kaynaklarının kullanım hakkı ve kişisel veri saklama politikası onaylanmadan yeniden işleme yapılmamalı.
- **Kabul kriteri:** Model/kurallar yalnız aday üretir; tek/ortalama duygu public iddiaya veya sıra bonusuna dönüşmez; başarısız model temel ürün akışını kesmez.

#### IP-29 — “Bilgi hatalı mı?” düzeltme girişi

- **Amaç:** Kullanıcının somut hatayı yorum/puan sistemine dönüştürmeden admin kuyruğuna iletmesi.
- **Beklenen dosyalar:** correction intake API, place/route UI form, admin case queue.
- **Backend işi:** Structured issue types, optional note, anti-abuse/rate limit, status/manage receipt without public author. **Frontend işi:** Küçük düzeltme akışı; gönderim sonucu/belirsizlik.
- **Veri modeli / migration:** Evet; correction submission/case link/retention. **API değişikliği:** Evet, anonymous controlled intake.
- **Testler:** Spam/size/PII handling, duplicate submission, network uncertainty, no auto publish, withdrawal dependency.
- **Bağımlılıklar / risk:** IP-08/09/10. Serbest metin hakaret/kişisel veri taşıyabilir; asgari saklama ve erişim.
- **Kabul kriteri:** Gönderim kamusal yorum değildir; otomatik yayın/puan yok; somut yer-zaman-alan admin case'ine izlenir.

#### IP-30 — Ürün, kalite ve operasyon ölçümü

- **Amaç:** MVP karar başarısını ve yanlış olumlu bilgi riskini puan/popülerlik vanity metric'i olmadan ölçmek.
- **Beklenen dosyalar:** event schema/collector, observability config, privacy docs/runbook, dashboards as code.
- **Backend işi:** Decision/correction/publication/job events; data quality and freshness lag. **Frontend işi:** Consent/anonymous event boundary; task completion/undo/error events.
- **Veri modeli / migration:** Event store/warehouse seçimine göre; kişisel bağlam minimize edilir. **API değişikliği:** Event ingest varsa evet.
- **Testler:** Schema validation, duplicate event, PII filter, denominator correctness, outage no-block.
- **Bağımlılıklar / risk:** IP-10/15/27/29. Telemetri karar verisi veya kişisel konum deposuna dönüşmemeli.
- **Kabul kriteri:** En az task completion, empty reason, hard-unknown, route edit, stale correction, publication lag ve error rate ölçülür; event kaybı temel görevi bozmaz.

#### IP-31 — Ekran durumları, erişilebilirlik ve MVP e2e

- **Amaç:** Kabul edilen empty/error/offline/loading/success sözleşmelerini gerçek ana akışlarda doğrulamak.
- **Beklenen dosyalar:** shared state components, E02–E09 pages, Playwright/Vitest tests, accessibility tooling.
- **Backend işi:** Deterministic test scenarios/error injection. **Frontend işi:** B25–B30, keyboard/focus/live regions, reduced motion, state restore.
- **Veri modeli / migration:** Hayır. **API değişikliği:** IP-10 typed states kullanılır.
- **Testler:** Keşfet → detay → geri; Bugün → sonuç; route edit/save; Gezeceğim; share read; offline; axe/keyboard/mobile breakpoints.
- **Bağımlılıklar / risk:** IP-13–24. Görsel bitirme işlevsel hata durumunu ertelememeli.
- **Kabul kriteri:** Hiçbir API hatası empty state olmaz; klavye ile ana görevler tamamlanır; kritik bilinmeyen her breakpoint'te görünür; test dosyası olmadan CI yeşil değildir.

#### IP-32 — Yetkili cache ve invalidation politikası

- **Amaç:** Performansı korurken cache'i hakikat sahibi yapmamak ve kritik geri çekmeyi geciktirmemek.
- **Beklenen dosyalar:** `site/src/lib/api.ts`, Next cache config, backend cache adapter, outbox/invalidation, CDN runbook.
- **Backend işi:** Public projection version/ETag, cache key scope, withdrawal purge, stale-if-error sınırı. **Frontend işi:** Server/browser/personal cache ayrımı; correction refresh.
- **Veri modeli / migration:** Invalidation outbox IP-04'te. **API değişikliği:** Version/ETag/Cache-Control.
- **Testler:** Cross-user leakage, withdrawal purge, 304, stale error, offline-vs-online, personalized no-shared-cache.
- **Bağımlılıklar / risk:** IP-04/10/15/23. 60 saniyelik kör revalidate kritik yanlış bilgiyi tutabilir.
- **Kabul kriteri:** Kişisel karar ortak cache'e girmez; kritik geri çekme purge eder; offline snapshot ayrıca tarihli kalır; cache rebuild yetkili kaynaktan yapılır.

### P3 — v1 sonrası

#### IP-33 — İsteğe bağlı tüketici hesabı ve cihazlar arası eşitleme

- **Amaç:** Temel akışları kilitlemeden kullanıcının seçtiği kayıtları hesaba taşımak.
- **Beklenen dosyalar:** consumer auth/account/sync modules, login/settings UI.
- **Backend işi:** Account, ownership, selective sync/conflict copies. **Frontend işi:** Login dönüşü ve “bu cihazda devam”.
- **Veri modeli / migration:** Evet. **API değişikliği:** Evet.
- **Testler:** Account isolation, selective migration, logout, deletion, conflicts. **Bağımlılıklar / risk:** IP-08 sınırlarını tüketici auth ile karıştırmama; IP-21/22.
- **Kabul kriteri:** Keşfet/rota/kayıt/paylaşım okuma hesapsız sürer; cihaz verisi sessiz taşınmaz.

#### IP-34 — Gezdiğim Yerler ve ziyaret olayı

- **Amaç:** Ziyareti niyetten ve öneri sinyalinden ayrı kişisel olay olarak tutmak.
- **Beklenen dosyalar:** visit model/API/UI. **Backend/frontend:** Açık ziyaret beyanı, edit/delete; kamusal puan yok.
- **Veri modeli / migration:** Evet. **API değişikliği:** Evet. **Testler:** Niyet/ziyaret ayrımı, privacy/delete.
- **Bağımlılıklar / risk:** IP-33 veya yerel-first strateji kararı; IP-21. **Kabul kriteri:** Ziyaret organik sırayı etkilemez, Gezeceğim'i sessiz silmez.

#### IP-35 — Bir İz katkısı

- **Amaç:** Yapılandırılmış gözlemi yorum portalı olmadan düzeltilebilir iç katkı yapmak.
- **Beklenen dosyalar:** contribution intake/review/status UI/API. **Backend/frontend:** Yer-zaman-alan gözlemi, withdrawal; no public profile/feed.
- **Veri modeli / migration:** Evet. **API değişikliği:** Evet. **Testler:** Scope, abuse, withdrawal impact.
- **Bağımlılıklar / risk:** IP-02/08/09/29 ve hak/saklama politikası. **Kabul kriteri:** Katkı otomatik kanıt/yayın/puan değildir; yazar kamusal değildir.

#### IP-36 — Site içi harita genişletmesi ve dış bildirimler

- **Amaç:** Aynı karar kümesini yardımcı harita görünümünde göstermek; bildirimleri yalnız gerçek opt-in olaylara bağlamak.
- **Beklenen dosyalar:** map components/provider, notification preference/service. **Veri/API/migration:** İhtiyaca göre evet.
- **Testler:** Liste-harita eşitliği, marker a11y, permission denial, no unsolicited alert.
- **Bağımlılıklar / risk:** IP-15/16/19/33; harita ikinci arama/sıra motoru olmamalı. **Kabul kriteri:** Harita yeni aday/uygunluk üretmez; bildirim ana görevi veya kritik sınırı gölgelemez.

#### IP-37 — Premium ve ödeme araştırması

- **Amaç:** Yalnız doğrulanmış ek kolaylık için iş modeli hazırlamak; doğruluk, güvenlik ve temel kayıtları ücretlendirmemek.
- **Beklenen dosyalar:** Önce araştırma/karar belgesi; kod yok. **Backend/frontend/veri/API/migration:** Bu işte yok.
- **Testler:** Kullanıcı/pilot doğrulaması ve ücretsiz temel hak invariant'ı. **Bağımlılıklar / risk:** MVP kullanım kanıtı ve ayrı onay.
- **Kabul kriteri:** Açılmış gerçek hizmet, fiyat ve yetki kararı olmadan Premium UI/ödeme kodu yazılmaz; ücretsiz kullanıcı aynı doğruluğu alır.

#### IP-38 — Çok günlük Akıllı Gezi keşfi

- **Amaç:** Günlük planları bir gezi altında düzenleme ihtiyacını MVP sonrası araştırmak; bu backlog'da uygulamamak.
- **Beklenen dosyalar:** Gelecek discovery/ADR; üretim kodu yok. **Backend/frontend/veri/API/migration:** Bu işte yok.
- **Testler:** Önce kullanım araştırması ve domain prototipi. **Bağımlılıklar / risk:** Günlük rota MVP ölçümü; erken soyutlama.
- **Kabul kriteri:** Ayrı kabul kararı olmadan `gun_sayisi`, konaklama/şehirler arası plan veya çok günlük API geri dönmez.

## 5. Uygulama sırası ve bağımlılık kapıları

| Dalga | Kapsam | Çıkış kapısı |
|---|---|---|
| **Dalga 0 — Güvenli başlangıç** | IP-11 baseline; IP-01 kamusal sızıntı; IP-06 sponsor; IP-07 günlük sınır; IP-10 güvenlik/hata; IP-12 ilk invariant CI | Public API yasak veri taşımıyor; sponsor etkisiz; yeni çok günlük üretim yok; migration baseline biliniyor; CI ihlali durduruyor. |
| **Dalga 1 — Kimlik, kanıt ve operasyon temeli** | IP-02, IP-03, IP-04, IP-08, IP-09; IP-27'nin batch manifest çekirdeği | Bir yer/iddia kaynak-zaman-kapsam-yayın durumuna izlenir; yanlış şube düzeltilebilir; geri çekme bütün tüketicilere yayılır; admin yetkili/auditlidir. |
| **Dalga 2 — Tek karar otoritesi ve bulma** | IP-05, IP-13, IP-14, IP-15; IP-28 aday gözlem sınırı | Hard constraints skordan önce; unknown ayrı; arama/filtre yalnız yayınlı aday; public karar paketi tek sözleşme. |
| **Dalga 3 — İlk kullanıcı değeri** | IP-16 Keşfet, IP-17 Bugün Ne Yapalım, IP-18 yer detay, IP-25 şehir, IP-26 ilçe | Kullanıcı 3–5 hedefli seçeneği gerekçe/sınırla görür; doğru detay/coğrafya; empty/error ayrımı; frontend ikinci motor değil. |
| **Dalga 4 — Günlük Akıllı Rota** | IP-19, IP-20; route bölümü IP-31 testleri | Tek günlük plan gerçek geçiş ve zaman kapsamını taşır; düzenlenebilir/undo; eski yanıt ezmez; sığmayan seçim görünür. |
| **Dalga 5 — Kişisel süreklilik** | IP-21, IP-22, IP-23, IP-24, IP-32 | Gezeceğim ve rota cihazda gerçek kaydolur; offline tarihli okunur; paylaşım salt okunur ve kapatılabilir; cache geri çekmeyi tutmaz. |
| **Dalga 6 — Pilot ve yayın sertleştirme** | IP-27 tam kalite gate, IP-29, IP-30, IP-31 tam e2e/a11y; SLO/runbook | Düzeltme alınır/işlenir; kalite ve task metrikleri ölçülür; pilot senaryoları otomatik ve operasyonel runbook ile geçer. |

### Kritik yol

`IP-11 → IP-02 → IP-03 → IP-04 → IP-05 → IP-15 → IP-16/IP-18 → IP-19 → IP-20 → IP-22/IP-24`.

IP-01, IP-06, IP-07, IP-10 ve IP-12 bu yolun başında paralel yürüyebilir; ancak Dalga 0 çıkış kapısı geçmeden yeni kullanıcı özelliği yayınlanmaz. IP-08/09, IP-02/03/04'ün insan düzeltme güvenlik ağıdır ve pilot veri yayını öncesinde tamamlanmalıdır.

## 6. Çok günlük Akıllı Gezi için bugünden korunacak sınırlar

Çok günlük özellik bu planda **uygulanmayacaktır**. Yalnız günlük MVP'yi ileride kilitlememek için şu domain kararları bugünden korunur:

1. **Günlük plan bağımsız aggregate'tir.** `GunlukPlan` tek `service_date` (opsiyonel), timezone, şehir/kapsam, başlangıç, istenen bitiş/dönüş, ulaşım, revision ve status taşır. `gun_sayisi` veya `gunler: []` taşımaz.
2. **Durak ve geçiş normalize edilir.** `GunlukPlanDuragi` canonical yer FK/alias çözümü, sıra, rol, ziyaret aralığı, kullanıcı seçimi ve kilitleri; `GecisAyagi` sağlayıcı/sürüm/zaman/mesafe/kapsam taşır. JSONB yer kimliği temel referans olmaz.
3. **Kullanıcı taslağı ile değerlendirme ayrıdır.** Taslak revision değişmeden eski hesap yeni planı ezmez; değerlendirme kullanılan claim/policy/transition sürümlerine bağlanır.
4. **Kayıt ve paylaşım entity-type bağımsızdır.** Gelecek paylaşım bir günlük plan revision'ını veya ileride ayrı gezi revision'ını gösterebilir; token/owner modeli `gunler` JSON biçimine bağlanmaz.
5. **Gelecek gezi ayrı aggregate olur.** Olası `Gezi` ve `GeziGunu`, günlük plan revision'larına referans verir; konaklama, şehirler arası geçiş, günler arası bütçe ve çapraz gün koşulları `GunlukPlan` içine sokulmaz.
6. **API adları tekil ve sürümlüdür.** MVP `/v1/gunluk-planlar`; gelecekte ayrı onayla `/v1/geziler`. Bugün `gun_sayisi` saklamak ileri uyumluluk değildir.
7. **MVP sorgu ve UI'si geleceği ima etmez.** Çok günlük şema, gizli flag, konaklama önerisi veya sahte boş alan eklenmez. Extension point yalnız ADR ve domain boundary'dir.

## 7. AI / LLM uygulama sınırı

| İş sınıfı | MVP'de yapılacak | Araç/uygulama | Yetki sınırı |
|---|---|---|---|
| Deterministik kod | Kimlik kapıları, rights/publication/freshness, hard constraints, arama filtresi, route scheduling, version/invalidation, share token, ölçüm | Python/SQL/PostGIS/TypeScript; testli saf kurallar | Gerçeğin ve yayın durumunun tek teknik uygulayıcısı; girdisi yine yetkili claim olmalı. |
| Kural tabanlı | Kaynak/claim family politikası, tri-state, Türkçe alias/synonym, admin escalation, reason code → standart metin | Sürümlü policy/config + regression test | Avantaj hard fail'i telafi etmez; kural değişimi review/rollout ister. |
| Veri hazırlama | Batch manifest, normalize, duplicate adayları, event/fetch/verify zamanları, source rights, quality gate, gold corpus | Mevcut pipeline'ın gözlenebilir/idempotent refactor'u | Ham girdi kendiliğinden kanıt/yayın değildir. |
| Klasik NLP | Duygu/konu/ifade tespiti, claim/observation adayı ve admin önceliği | Mevcut Türkçe BERT + şeffaf sözlük/kurallar; CPU/lokal | Ortalama puan, public yorum özeti veya tek başına uygunluk üretmez. |
| LLM'nin gerçekten faydalı olabileceği | Serbest niyeti yapılandırılmış adaylara ayırma; onaylı yapılandırılmış gerekçeyi sade anlatma; admin case özeti; çelişki/duplicate aday açıklaması | Opsiyonel, düşük maliyetli çağrı; JSON schema, allow-list, timeout/fallback, eval | Kaynak, kanıt, yayın otoritesi veya tek uygunluk kararı değildir; saat/fiyat/erişilebilirlik üretemez. |

Özel model eğitimi MVP önerisi değildir. LLM kapalı, kota dolu veya hatalı olduğunda arama, filtre, Karar Motoru, günlük rota ve admin yayın kapıları deterministik çalışmaya devam eder. LLM çıktısı kaynak id, claim id ve policy tarafından desteklenmeyen olumlu cümle ekleyemez; şema/claim doğrulamasından geçmeyen çıktı kullanılmaz.

## 8. Kalite kapıları ve “implementasyona hazır” tanımı

| Kapı | Geçme koşulu |
|---|---|
| K0 — Baseline | Canlı geliştirme/staging DB revizyonu ve drift raporu bilinir; backup/restore yolu denenmiştir. |
| K1 — Kamusal güvenlik | Yasak yorum/yazar/puan/iç skor public API ve browser payload'ında yoktur. |
| K2 — Ticari bağımsızlık | Sponsor bayrağı organik adaylık, sıra, güven ve rota sonucunu değiştirmez. |
| K3 — Kimlik | Belirsiz şube otomatik birleşmez; merge/split geri alınabilir; kayıt referansları korunur. |
| K4 — Bilgi | Her olumlu claim kaynak, kapsam, zaman, hak ve yayın sürümüne bağlıdır; unknown/stale ayrı. |
| K5 — Tek karar | Hard constraint telafi edilemez; frontend/rota aynı Karar Motoru sonucunu kullanır. |
| K6 — Günlük rota | Tek gün, geçiş/zaman/dönüş kapsamı, edit/revision/undo ve sınırlı sonuç davranışı geçer. |
| K7 — Kayıt/paylaşım/offline | Yerel kayıt gerçek; paylaşım read/manage ayrık ve revoke; offline canlı iddia üretmez. |
| K8 — Operasyon | Admin auth/audit, düzeltme/yayın/geri çekme ve etki yayılımı pilot senaryosunda çalışır. |
| K9 — Yayın | CI, e2e/a11y, structured logs, metrik/alert ve runbook; sıfır test dosyası başarı sayılmaz. |

Bu planla implementasyona **hazırız**, fakat “özellik geliştirmeye hazır” olmanın ilk işi Dalga 0'dır. Canlı DB baseline sonucu IP-11'de beklenmedik drift gösterirse yalnız migration sırası revize edilir; ürün sözleşmesi ve backlog önceliği değişmez.

## 9. Son tablolar

### A) İlk düzeltilecek 10 kritik konu

| Sıra | Kritik konu | Çelişki | İlk iş |
|---:|---|---|---|
| 1 | Public API'den ham yorum, yazar ve profil pasajı sızıntısı | C-01, C-02 | IP-01 |
| 2 | Duygu/puan ve sahte `duygu*5` sunumu | C-03 | IP-01 |
| 3 | Sponsorun organik keşif/rota bonusu | C-04 | IP-06 |
| 4 | Zorunlu koşulun puana gömülmesi ve unknown kabulü | C-05, C-06 | IP-05 |
| 5 | Yayın/güncellik kapısı olmadan bütün kataloğun aday olması | C-07 | IP-02, IP-04 |
| 6 | Aktif çok günlük rota/konaklama sözleşmesi | C-08 | IP-07 |
| 7 | Kuş uçuşu veriden yapılabilirlik/yürüme/ulaşım iddiası | C-09 | IP-19 |
| 8 | Yanlış şube ve geri alınamaz zincirleme duplicate merge | C-12 | IP-03 |
| 9 | Eski batch/timestamp ve geri çekilmeyen mekân/türev | C-13, C-14 | IP-02, IP-04, IP-27 |
| 10 | Merge sonrası rota referansı kaybı ve kontrolsüz anonim kayıt/paylaşım | C-15, C-16 | IP-03, IP-22, IP-24 |

### B) İlk geliştirilecek 20 iş

| Sıra | İş | Öncelik | Dalga | Başlama koşulu |
|---:|---|---|---|---|
| 1 | IP-11 Migration ve canlı şema baseline denetimi | P0 | 0 | DB erişimi |
| 2 | IP-01 Kamusal API veri sızıntısını kapat | P0 | 0 | Yok |
| 3 | IP-06 Sponsor/ticari sinyali ayır | P0 | 0 | IP-01 ile paralel |
| 4 | IP-07 Günlük MVP sınırı | P0 | 0 | IP-01 ile paralel |
| 5 | IP-10 Güvenlik, hata, gözlemlenebilirlik tabanı | P0 | 0 | Yok |
| 6 | IP-12 P0 invariant testleri ve CI | P0 | 0 | İlk 5 işle birlikte büyür |
| 7 | IP-02 Kanıt/iddia/güncellik çekirdeği | P0 | 1 | IP-11 |
| 8 | IP-03 Canonical yer/şube kimliği | P0 | 1 | IP-11 |
| 9 | IP-04 Yayın/geri çekme/etki kapısı | P0 | 1 | IP-02, IP-03 |
| 10 | IP-08 İç admin auth/RBAC/audit | P0 | 1 | IP-11 |
| 11 | IP-09 Minimum admin düzeltme/yayın | P0 | 1 | IP-02, 03, 04, 08 |
| 12 | IP-27 Veri batch orkestrasyonu çekirdeği | P2 | 1 | IP-02, IP-03 |
| 13 | IP-05 Karar bağlamı/hard constraints | P0 | 2 | IP-02, IP-04 |
| 14 | IP-13 Türkçe arama | P1 | 2 | IP-03, IP-04, IP-05 |
| 15 | IP-14 İlçe/somut koşul filtreleri | P1 | 2 | IP-03, IP-05, IP-13 |
| 16 | IP-15 Kamusal Karar Sonucu | P1 | 2 | IP-01, 02, 04, 05 |
| 17 | IP-28 NLP'yi gözlem adayı sınırına çek | P2 | 2 | IP-02, IP-03, IP-09 |
| 18 | IP-16 Keşfet'i Karar Motoruna bağla | P1 | 3 | IP-13, IP-14, IP-15 |
| 19 | IP-17 Bugün Ne Yapalım? | P1 | 3 | IP-05, IP-15, IP-16 |
| 20 | IP-18 Mekân detayını karar birimi yap | P1 | 3 | IP-03, IP-04, IP-15 |

Not: İlk 20'den sonra sıra IP-25 → IP-26 → IP-19 → IP-20 → IP-21 → IP-22 → IP-23 → IP-24 → IP-32 → IP-29 → IP-30 → IP-31'dir. Dalga kapısı geçmeden sonraki dalga production'a açılmaz; güvenli paralel çalışma yapılabilir.

### C) Şu anda dokunulmaması gereken / ertelenen işler

| İş | Karar | Ne açar? |
|---|---|---|
| Çok günlük Akıllı Gezi, konaklama merkezi, şehirler arası plan | Uygulama yok; tarihsel kod public akıştan çıkarılır | Günlük rota pilot kanıtı + ayrı ürün kabulü (IP-38) |
| Tüketici hesabı ve çoklu cihaz sync | P3 | Yerel kayıt MVP'si ve kullanıcı ihtiyacı (IP-33) |
| Gezdiğim Yerler | P3 | Niyet/kayıt modeli doğrulandıktan sonra (IP-34) |
| Bir İz açık katkı sistemi | P3 | Admin/kanıt/düzeltme ve abuse/saklama olgunluğu (IP-35) |
| Ayrı Favoriler | Yapılmayacak | Gezeceğim tek niyet deposudur; yeni karar gerekmedikçe açılmaz |
| Premium, ödeme, abonelik, kota | Araştırma P3; kod yok | Gerçek ek kolaylık ve ayrı ticari kabul (IP-37) |
| Premium kullanıcıya daha doğru öneri | Yasak | Hiçbir koşulda ücretli doğruluk katmanı yok |
| İkinci şehir / ülke ölçeklemesi | Ertele | Samsun kapsam/operasyon/kalite kapıları |
| Geniş site içi harita, dış bildirim | P3 | Liste-karar ve günlük rota stabilitesi (IP-36) |
| İşletme self-service paneli, reklam açık artırması | Ertele | Yetki/kanıt/ticari bağımsızlık için ayrı kabul |
| Özel model eğitimi / fine-tune | Ertele | Ölçülmüş hata seti; önce deterministik/kural/klasik NLP |
| Canlı fiyat/saat/yoğunluk vaadi, rezervasyon | Yapılmayacak/ayrı kapsam | Yetkili güncel kaynak, hak ve hata bütçesi olmadan açılamaz |
| Tarihsel `SabitRota` ve otomatik konaklama akışını genişletme | Dokunma; emekliye ayır | Yalnız veri koruma/deprecation migration'ı; yeni özellik yok |
| SEO slug, rehber ve içerik hacmi büyütme | Çekirdek sonrasına ertele | Canonical kimlik ve publication projection stabilitesi |

## Bağlı belgeler

- [03 Karar Motoru](../00-product/03-karar-motoru.md)
- [04 Sistem Mimarisi](../00-product/04-sistem-mimarisi.md)
- [05 AI Bilgi Motoru](../04-ai/05-ai-bilgi-motoru.md)
- [06 Akıllı Rota Motoru](../00-product/06-akilli-rota-motoru.md)
- [07 UX Karar Akışları](../02-ux/07-ux-karar-akislari.md)
- [09 Ürün Ekosistemi](../09-business/09-urun-ekosistemi.md)
- [10 Design System](../03-design/10-design-system.md)
- [11 Ekran Mimarisi](../03-design/11-ekran-mimarisi.md)
- [12 Görsel Tasarım Dili](../03-design/12-gorsel-tasarim-dili.md)
- [13 Bileşen ve Etkileşim Sözleşmeleri](../03-design/13-bilesen-ve-etkilesim-sozlesmeleri.md)
- [14 Ürün Özellik Haritası](../09-business/14-urun-ozellik-haritasi.md)

## Etkilediği belgeler

Bu belge kabul edilmiş ürün davranışlarını değiştirmez. Uygulama başladığında `sunucu/README.md`, `sunucu/api/README.md`, `sunucu/rota_motoru/README.md`, `veri/README.md` ve `site/README.md` yalnız gerçekten tamamlanan işlerle birlikte güncellenmelidir. Tarihsel plan ve prototip açıklamaları hedef sözleşme olarak kullanılmamalıdır.

## Bundan sonra okunması gereken belge

İlk uygulama dalı için bu belgedeki **Dalga 0**, ardından IP-02/IP-03 migration ADR'ları okunmalıdır. Yeni ürün kapsamı yazılmamalı; her PR ilgili IP kabul kriterini ve K0–K9 kapısını referanslamalıdır.
