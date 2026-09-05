# Şamandıra — Cursor Talimat Paketi (T-00 … T-16 + Backlog)
**Tarih:** 2026-09-05 · Güncelleme: 2026-09-05 (T-16 = `yon.md` P1–P6) · Format: brif §14'teki şablon (Amaç / Katman / Dosyalar / Yapılmayacaklar / Doğrulama)

**Karar kaynağı (tek metin):** `plan/00_brief_eki.md` §3. Çelişkide o madde + `plan/tasarim/yon.md` kazanır.

## Kullanım ritüeli (her görevde)
1. **Hazırlık (bir kez, manuel):** Bu `samandira/` klasörünün tamamını repoya **`plan/`** adıyla kopyalayın (00-07 + `logo/` + `tasarim/`). Cursor ajanı böylece şartnameleri kendisi okuyabilir; talimatlar kısa kalır.
2. Yeni Cursor sohbeti aç → şunu yapıştır: *"Önce `plan/BRIF.md` ve `plan/00_brief_eki.md` dosyalarını oku (proje brifi + güncel kararlar)."* (Brif artık repo içinde — elle yapıştırma gerekmez.)
3. Sonra ilgili görev metnini (aşağıdan kopyala) yapıştır. **Tek sohbette tek görev** — bağlam şişmesin.
4. Görev bittiğinde ajana commit YAPTIRMAYIN; diff'i inceleyin, testi siz koşun, commit'i siz atın (brif kuralı).

## Bağımlılık sırası
```
T-00 → T-01 → T-02 → T-03 (K8 üretim = T-16 P1)
                 → T-16 P2–P6 (yon.md; P1 kapandı)
                 → T-04 → T-12(deploy, robots kapalı) → T-05 → T-06 → (robots aç + GSC)
                                                        → T-07, T-08, T-09, T-10, T-11 (paralel yürür)
                                                        → T-13, T-14 → T-15 → Backlog
```
Not: T-12 erken yapılır ki dev tunnel'dan kurtulun; **GSC gönderimi T-06 bitmeden YAPILMAZ** (yarım site indekslenmesin) — T-12 sonrası robots.txt geçici olarak `Disallow: /` kalır, T-06'da açılır. T-16 görsel makyajı SEO görevleriyle paralel yürüyebilir; P4 (hero sekansı) Unsplash/çekim künyesi ister.

---

## T-00 — Cursor araç kurulumu
**Amaç:** Ajanın proje kurallarını, güncel dokümanı ve tarayıcıyı kullanabilmesi; kalite kapılarının kurulması.
**Katman:** repo konfig + site.
**Ön şart:** Skills (`ui-ux-pro-max`, `react-best-practices`, `seo-audit`) ve `.cursor/mcp.json` `plan/BASLA.md` adımlarıyla **elle** kurulmuş olmalı — ajan bunları kurmaz, yalnız varlığını doğrular.
**Yapılacaklar:** `plan/03_cursor_araclari_kurulumu.md` dosyasını oku ve sırayla uygula: (1) `.cursor/rules/` altına §1'deki 4 `.mdc` dosyasını **birebir** oluştur + §3b'nin sonundaki iki rules entegrasyon satırını ekle, (2) kök `AGENTS.md`'yi §2 maddeleriyle güncelle (mevcut `site/AGENTS.md` kalsın), (3) `.cursor/mcp.json`'ı kontrol et — yoksa §3'teki gibi oluştur (postgres bloğu read-only rol açılana kadar kapalı kalsın), (4) `site/` içinde shadcn/ui init + §4'teki bileşenleri ekle, (5) §5 kalite yığınını kur (ESLint 9 flat + Prettier + husky + lint-staged + commitlint; TypeScript strict), (6) §6: Vitest + Playwright (e2e iskeleti, test yazma), (7) §7'deki `.cursor/commands/` dosyalarını oluştur.
**Yapılmayacaklar:** uygulama koduna dokunma; bağımlılık ekleme dışında davranış değiştirme; commit atma.
**Doğrulama:** `npm run lint` ve `npx tsc --noEmit` temiz; skill klasörleri yerinde (`.cursor/skills/` veya `.agents/skills/` altında: `ui-ux-pro-max`, `vercel-react-best-practices`, `web-design-guidelines`, `seo-audit`); shadcn `Button` render eden geçici sayfayı göster sonra sil; MCP listesini bana raporla (yeşil/kırmızı).

## T-01 — Doküman gerçeği
**Amaç:** README'lerin yalan söylemesinin bitmesi ("Faz 3 boş / site yok" iddiaları).
**Katman:** dokümanlar.
**Yapılacaklar:** Kök `README.md`, `sunucu/README.md`, `sunucu/api/README.md` ve `site/README.md`'yi gerçek durumla yeniden yaz: üç katmanlı mimari özeti, çalışan site + API (endpoint tablosu `plan/00_brief_eki.md` §4-5'ten), kurulum/çalıştırma (`calis.txt` ile hizalı: port 8125/3000, `.venv_test`, `C:\PostgreSQL`), komut listeleri (toplayıcı → eşleme → duygu → aktarım → API → site), doküman haritası (`dokumanlar/` + `plan/`), marka: **Şamandıra** (Alegre Group). `calis.txt`'i de gözden geçir, çelişki varsa düzelt.
**Yapılmayacaklar:** kod değişmez; eski README içeriklerini "tarihçe" diye taşıma — temiz yeniden yaz.
**Doğrulama:** README'deki her komutu kuru çalıştırılabilirlik açısından kontrol et (yol/port doğruluğu); bana eski-yeni fark özetini ver.

## T-02 — Marka metinleri: Rotam → Şamandıra
**Amaç:** Kullanıcının gördüğü her yerde Şamandıra markası.
**Katman:** site + sunucu (yalnız marka stringleri).
**Yapılacaklar:** Site genelinde "Rotam" geçen tüm kullanıcı metinlerini değiştir: `site/src/app/layout.tsx` (metadata title/description şablonu: `Şamandıra — Karadeniz'in kişisel gezi rehberi`), `page.tsx` hero/footer, tüm bileşenler, `manifest`/`site.webmanifest` adı. API: `sunucu/api/uygulama.py` FastAPI `title="Şamandıra API"`, description'ı ürün tanımıyla güncelle. Footer tagline: "Karadeniz'den başlayan kişisel gezi rotaları. Önce Samsun, sonra tüm kıyı." → korunabilir ama marka Şamandıra. Konumlanma cümlesi: `plan/04_marka_ve_tema.md` §1.
**Yapılmayacaklar:** kod tanımlayıcıları, dosya yolları, DB içerikleri, git geçmişi, `plan/` dokümanlarındaki tarihsel atıflar değişmez.
**Doğrulama:** `grep -ri "rotam" site/src sunucu --include="*.tsx" --include="*.ts" --include="*.py"` → kullanıcıya görünen dosyalarda 0 sonuç; tarayıcıda `/` ve `/docs` başlıklarını göster.

## T-03A — İPTAL
Logo + slogan keşfi kapandı. Final logo K8 (`plan/logo/secili/logo.png`). Diğer görevlerdeki "T-03A" / "T-16 Faz 1 logo" atıfları K8 olarak okunur.

## T-03 — Logo üretim varlıkları, 404, bölge-nötr metin
**Amaç:** K8 karosunun sitede durması; İngilizce 404 ve bölge kilitli cümlelerin bitmesi.
**Katman:** site (+ public varlıklar).
**Şartname:** `plan/00_brief_eki.md` §3.8 (K8), `plan/04_marka_ve_tema.md` §4, `plan/tasarim/yon.md` §1.6.
**Yapılacaklar:** (1) `plan/logo/secili/logo.png` **sabit** — çizgi/kompozisyon/renk değiştirme. Yalnız üretim: şeffaf + açık zemin PNG, favicon 16/32/48 + `.ico`, apple-touch 180, PWA 192/512 + maskable, header kilidi (karo + `şamandıra`), `og-default.png`. Script: `site/scripts/logo_uretim.mjs`. (2) Header/footer `KelimeKilidi` + `LogoKaro` (`next/image`). Ufuk SVG/bileşen yok. (3) Türkçe `not-found.tsx`. (4) `/tasarim-secim` yok. (5) **K6:** "Karadeniz'in kişisel gezi rehberi" yüzeylerden temiz.
**Yapılmayacaklar:** logoyu yeniden çizmek; vektör "yorumu"; rota motoru.
**Doğrulama:** sekme faviconu; `/` header kilidi 375+1280; 404 Türkçe.

## T-04 — Prod build disiplini
**Amaç:** `npm run dev` ile yayının bitmesi; prod build'in temiz çıkması.
**Katman:** site.
**Yapılacaklar:** `next.config.ts`: `output: 'standalone'`, güvenlik başlıkları (`headers()`: X-Content-Type-Options, Referrer-Policy, X-Frame-Options, Permissions-Policy), `/backend` rewrite hedefini env'e bağla (`BACKEND_INTERNAL_URL`, default `http://127.0.0.1:8125`). `next build` hatalarını gider (tip hataları strict modda çıkabilir — `any` ile değil düzgün çöz). `next start` ile prod modda çalıştırıp tüm sayfaları dolaş. `calis.txt`'e prod çalıştırma komutlarını ekle.
**Yapılmayacaklar:** özellik ekleme; bağımlılık yükseltme (Next 16/React 19 sabit).
**Doğrulama:** `next build && next start` sonrası Lighthouse (mobil): Perf ≥ 80, SEO ≥ 90, A11y ≥ 90, BP ≥ 90 — raporu bana ver; HTML'de HMR/devtools kalıntısı olmadığını grep'le kanıtla.

## T-05 — Slug sistemi (URL'lerin SEO'ya açılması)
**Amaç:** `/yer/{uuid}` → `/yer/samsun/{slug}`; UUID linkler 301.
**Katman:** ortak + sunucu + site (şartname: `plan/02_seo_mimarisi.md` §3 — harfiyen uy).
**Yapılacaklar:** (1) `ortak/metin_araclari.py::slug_uret(ad)` — Türkçe→ASCII transliterasyon (ş→s, ı→i, ğ→g, ü→u, ö→o, ç→c), küçük harf, `-`, max 60 kr, çakışmada `-2` eki; birim testleri (veri tarafı pytest'e ek). (2) Alembic `0005_yer_slug`: `yerler.slug` + `UNIQUE(sehir_id, slug)` + index. (3) `sunucu/veritabani/aktarim/calistir.py`: aktarımda slug üret/doldur (idempotent kalsın; mevcut kayıtlarda UPDATE). (4) `sunucu/api/semalar.py` yer şemalarına `slug`; `GET /yerler/{yer_id}` hem UUID hem slug kabul etsin (aynı endpoint, path çözümleyici). (5) Site: `types.ts` + `api.ts` güncelle; `/yer/[id]` → `/yer/[sehir]/[slug]` route yapısı; eski `/yer/{uuid}` için `redirect()` (301) — slug'ı API'den çöz. (6) Tüm iç linkler (keşif kartları, rota durakları, bölgeler) slug'a döner.
**Yapılmayacaklar:** rota motoru skor/kümeleme mantığı; keşif vitrini filtresi; slug'ı runtime tahminle üretme (DB'den oku).
**Doğrulama:** `pytest sunucu/rota_motoru/testler/ -v` yeşil (rota çıktısı değişmemeli); aktarımı iki kez koş (idempotent); tarayıcıda: kart linki `/yer/samsun/bandirma-vapuru-muzesi` formatında, eski UUID link 301 ile yenisine gidiyor; rota sonucu durak linkleri çalışıyor.

## T-06 — SEO çekirdeği (metadata, robots, sitemap, JSON-LD)
**Amaç:** Sitenin indekslenebilir hâle gelmesi. Şartname: `plan/02_seo_mimarisi.md` §4, §5, §6 — şablonlara harfiyen uy.
**Katman:** site (+ küçük API ekleri).
**Yapılacaklar:** (1) `layout.tsx`'e `metadataBase` + Organization/WebSite JSON-LD. (2) Her sayfa türü için `generateMetadata`: §4'teki title/description şablonları (veri güdümlü `{n}` alanları API'den), canonical, OG/Twitter kartları. (3) `app/robots.ts` — **bu görevde geçici `Disallow: /`** (T-12 deploy sonrası, GSC öncesi açılacak; kod içine `SITE_INDEKSE_ACIK` env bayrağı koy). (4) `app/sitemap.ts` — şehir/kategori/ilçe/yer/rehber URL'leri, `lastModified` DB'den. (5) `site/src/components/seo/JsonLd.tsx` + `schema-dts`: sayfa türü → şema eşlemesi (§5 tablosu; taksonomi alt kategorisinden Museum/Restaurant/Beach... türetme). **AggregateRating koyma.** (6) Breadcrumb bileşeni (görünür + JSON-LD). (7) Rota sihirbazı sayfası `robots: noindex, follow`; `/rota/{id}` paylaşım sayfası indexlenebilir (sayfa henüz yoksa route iskeletini oluştur — içerik T-07/rota sonucundan). (8) API: `GET /sehirler/{anahtar}/istatistik` (yer/ilçe sayıları, kategori dağılımı, ort. duygu) — metadata `{n}` alanları için. (9) **GEO paketi (K7, şartname `02` §11):** ana sayfa + `/hakkimizda` üstüne AI-alıntılanabilir tek tanım cümlesi (T-16 Faz 1'de seçilen konumlanma cümlesi, kelimesi kelimesine aynı); kökte `llms.txt`; en sorulu 3 sayfa türünde görünür SSS + FAQPage JSON-LD; her sayfa türünde ilk 40-60 kelime sayfanın sorusunu doğrudan yanıtlayan "önce cevap" paragrafı; sayı+tarih içeren alıntılanabilir istatistik cümlesi (API istatistik ucundan beslenir).
**Yapılmayacaklar:** içerik/metin şablonlarının şişirilmesi; rota motoru; keşif filtresi.
**Doğrulama:** `curl -s http://localhost:3000/sehir/samsun | grep -c 'application/ld+json'` ≥ 2; her sayfa türünde title/description **benzersiz** (5 örnek URL çıktısını bana ver); sitemap.xml geçerli XML; Rich Results Test sonuçlarını raporla; Lighthouse SEO ≥ 95; `llms.txt` 200 dönüyor ve tanım cümlesi ana sayfa + /hakkimizda'da birebir aynı.

## T-07 — Dinamik OG görselleri (next/og)
**Amaç:** Paylaşılan her linkin (WhatsApp/X/Instagram DM) şık kart olması — büyüme kanalının görsel ayağı.
**Katman:** site.
**Yapılacaklar:** `opengraph-image.tsx` (ImageResponse): yer detayı (yer adı + ilçe + kategori + duygu skoru + fotoğraf varsa o, yoksa deniz degrade + logo), şehir hub, `/rota/{id}` (gün sayısı + durak adları + "Şamandıra ile planlandı"). Şablon: `plan/04_marka_ve_tema.md` §3 paleti + §8 og-default. 1200×630, yazı taşmalarını kırpma kurallarıyla çöz. Fotoğraf kaynağı T-09'a bağlı — yoksa degrade fallback.
**Yapılmayacaklar:** harici servis (Vercel OG vb.) — native `next/og` kullan.
**Doğrulama:** `curl -I` ile 3 farklı URL'nin OG görseli 200 + content-type image/png; görselleri bana dosya olarak göster.

## T-08 — Kürasyon: sıralama + gürültü eşiği + kategori yolları
**Amaç:** Keşif vitrininin "60 alfabetik kayıt, yarısı cami/park" görüntüsünden çıkması.
**Katman:** sunucu (sorgular) + site + doküman/taksonomi ÖNCE.
**Yapılacaklar:** (1) **Önce** `dokumanlar/kategori_taksonomisi.md`'ye "Vitrin sıralama ve eşik kuralları" bölümü ekle, sonra `ortak/sabitler.py`'ye ilgili sabitler (proje kuralı: taksonomi → sabit → kod). Kural önerisi: keşif listesi **skor bazlı sıralı** (mevcut keşif skoru/duygu/deneyim puanı bileşimi — formülü kırılımla belgele); turistik değeri düşük alt kategoriler (mahalle camii, küçük park, site içi mekan) ancak `sehrin_klasigi`/yüksek duygu/çok kaynaklı ise vitrine girer. (2) `sunucu/veritabani/sorgular.py`: ORDER BY + eşik filtresi (yalnız `sadece_kesif=true` yolu — rota motorunun `sadece_kesif=false` sorgusuna DOKUNMA). (3) Kalite raporuna (`veri/kalite_kontrol/rapor_olustur.py`) "vitrin uygunluğu" metrikleri ekle. (4) Site: statik kategori yolları `/sehir/[anahtar]/gezilecek-yerler` ve `/yeme-icme` (`?kategori=` sürümleri canonical'ı statiğe verir).
**Yapılmayacaklar:** rota skorlama bileşenleri; verinin kendisi (DB'de kayıt silme yok — yalnız vitrin filtresi).
**Doğrulama:** pytest rota testleri **birebir aynı** sonuç (rota değişmedi kanıtı: bir örnek rotanın kırılımını önce/sonra karşılaştır); tarayıcıda ilk sayfa: skor sıralı, cami/park yoğunluğu gözle görülür azalmış; kategori yolları + canonical çalışıyor.

## T-09 — Fotoğraf hattı
**Amaç:** Sıfır görselden fotoğraflı vitrine (SEO + güven + dönüşüm).
**Katman:** veri (aktarım) + sunucu + site.
**Yapılacaklar:** (1) Kendi çektiğimiz fotoğraflar için düzen: `veri/cikti/fotograflar/{slug}.jpg` + `manifest.json` (slug → dosya listesi, telif: "Alegre Group"). (2) Aktarımda fotoğraf kayıtlarının DB'ye yazımı (mevcut fotoğraf şemasını kullan — `plan`'daki brif §7: şema var). (3) API: yer şemalarına `fotograflar: [{url, alt, kaynak}]`; statik servis: fotoğraflar `site/public/yerler/{slug}/` altına kopyalanır (deploy'da volume) VEYA API üzerinden `/medya/{...}` — öneri: site public (basit, hızlı). (4) Site: keşif kartlarında `next/image` (16:9, blur placeholder, alt=`{ad} — {ilçe}, Samsun`), yer detay hero galerisi. (5) Fotoğrafı olmayan yer: degrade + kategori ikonu fallback (asla boş kutu).
**Yapılmayacaklar:** **scraping kaynaklı görsel kullanma** (K2 kırmızı çizgisi); harici hotlink.
**Doğrulama:** 5 örnek yerle uçtan uca: klasöre jpg at → aktarım → kartta görünüyor; CLS < 0.1 (Lighthouse); alt metinleri Türkçe ve benzersiz.

## T-10 — İlçe sayfaları + yakındaki yerler
**Amaç:** 17 ilçe sayfasının derinleşmesi + iç link ağı (SEO'nun çarpanı).
**Katman:** sunucu + site.
**Yapılacaklar:** (1) API: `GET /sehirler/{anahtar}/bolgeler/{bolge_slug}` (tek bölge detayı: profil + duygu özeti + o bölgenin yerleri) ve `GET /yerler/{yer_id}/benzer` (PostGIS `ST_DWithin` ~5 km, aynı/uyumlu kategori, max 6 — mesafe bilgisiyle). (2) Site: `/sehir/[anahtar]/bolgeler/[slug]` sayfası: bölge tanıtımı + duygu özeti + yer listesi (skor sıralı) + "bu bölgede rota kur" CTA (sihirbaza `bolge` parametresi) + SSS bloğu (bölge verisinden şablon — JSON-LD `FAQPage` yalnız gerçek görünen sorularla). (3) Yer detayına "Yakındaki yerler" bölümü (benzer endpoint'i). (4) Breadcrumb her sayfada (T-06 bileşeni).
**Yapılmayacaklar:** bölge profili üretim mantığı (veri katmanı) değişmez; rota motoru.
**Doğrulama:** Atakum + İlkadım + Vezirköprü sayfalarında Playwright turu; benzer yerler mesafe gösteriyor; ilçe sayfaları sitemap'te; City/Breadcrumb JSON-LD validator'dan geçiyor.

## T-11 — Kurumsal + yasal sayfalar
**Amaç:** Güven (E-E-A-T) + KVKK asgarisi + ileriki sponsorluk zemini.
**Katman:** site.
**Yapılacaklar:** `/hakkimizda` (Alegre Group; Bekir + Hiranur kartları — OMÜ Bilgisayar Müh., GitHub/LinkedIn linkleri, Person JSON-LD; "Şamandıra nedir, nasıl çalışır?" — şeffaflık: skor kırılımı anlatımı, **veri kaynağı ifşası YOK**, "ziyaretçi yorumlarından derlenen analizler" düzeyi), `/gizlilik` (KVKK aydınlatma: hangi veri işleniyor — çerez yok, Umami anonim sayaç; iletişim: ASCII e-posta), `/kullanim-kosullari`, `/iletisim` (form değil — mailto + basit form; spam koruması sonra), `/sponsorluk` **taslak** (Büyüme kararı gereği yayında görünür link YOK, `noindex`; içerik: paket iskeleti — Faz 5'te açılacak). Footer'a yasal linkler + `Harita verisi © OpenStreetMap contributors` atfı.
**Yapılmayacaklar:** kaynak adlarını (Google/Ekşi/TripAdvisor) kullanıcıya görünen metinlerde anma; hukuki metinleri uydurma — taslak üret, "avukat/hoca kontrolü" notu düş.
**Doğrulama:** Sayfalar render + footer linkleri; Organization/Person JSON-LD geçerli; `/sponsorluk` noindex.

## T-12 — Deploy paketi (Oracle hazır)
**Amaç:** Sunucuda `docker compose up -d` ile çalışan yayın paketi. Şartname: `plan/05_deployment_oracle.md` — birebir uy.
**Katman:** yeni `deploy/` klasörü (+ next.config küçük ek).
**Yapılacaklar:** `deploy/api/Dockerfile` (python:3.12-slim; requirements yolu `calis.txt`/repo gerçeğinden doğrula; uvicorn + alembic), `deploy/site/Dockerfile` (node:22-alpine multi-stage → standalone; build arg `NEXT_PUBLIC_API_URL=http://api:8125`), `docker-compose.yml` (§4 iskeleti: db/api/site/caddy; healthcheck'ler; restart unless-stopped; db portu dışa kapalı), `caddy/Caddyfile` (punycode host, www 301, güvenlik başlıkları, api alt alan adı), `.env.example` (DB_PASSWORD, umumi değerler — **sır yok**), `scripts/yedekle.sh` + `scripts/saglik.sh`, API'ye `GET /healthz` (DB ping) ekle. `next.config.ts` rewrite hedefi `BACKEND_INTERNAL_URL` env (T-04'te eklendiyse dokunma).
**Yapılmayacaklar:** sırları git'e koyma; lokal geliştirme akışını bozma (`calis.txt` komutları aynen çalışmalı); scraping/veri katmanını imaja dahil etme (api imajı yalnız `sunucu/ + ortak/`).
**Doğrulama:** `docker compose config` geçerli; Dockerfile'lar `docker build --check`/hadolint temiz (bu makinede Docker yok — sentaks + mantık doğrula, gerçek build sunucuda); `/healthz` kodunu pytest'e ekle.

## T-13 — Umami analitik + olaylar
**Amaç:** Ölçmeden büyüme olmaz: trafik + ürün olayları.
**Katman:** deploy + site.
**Yapılacaklar:** compose'a `umami` servisi (aynı db sunucusunda ayrı `umami` veritabanı) + Caddy'de `umami.` alt alan adı (veya path). Site: prod-only script enjeksiyonu (`NEXT_PUBLIC_UMAMI_URL` boşsa hiç yüklenmez — dev'de analytics yok). Olay enstrümantasyonu: `rota_olustur_tamamla` (senaryo, gün sayısı, alternatif seçimi), `yer_detay_goruntule`, `bolge_goruntule`, `dis_link_tikla` (Google Maps vb.), `sponsor_rozet_goruntule`. `/gizlilik` metnindeki analitik paragrafını gerçek kurulumla hizala (çerezsiz, IP anonim).
**Yapılmayacaklar:** çerez tabanlı araç (GA4 şimdilik YOK — KVKK yükü + büyüme odaklı minimal ölçüm); kişisel veri gönderen olay.
**Doğrulama:** prod build'de olaylar Umami panelinde görünüyor; dev modda script yüklenmiyor (ağ sekmesi kanıtı).

## T-14 — Test paketi + CI
**Amaç:** Regresyon korkusu olmadan hız.
**Katman:** site + repo.
**Yapılacaklar:** (1) Playwright e2e (`site/e2e/`): akış-1 ana→keşif→yer detay; akış-2 rota sihirbazı senaryo-2 uçtan uca (alternatifler→seç→bölge önerisi→paylaşım linki); akış-3 SEO sözleşmesi (5 sayfa türünde title/description/canonical/JSON-LD/og:image assert). (2) `lighthouserc.json` (§ bütçeler: Perf≥85 SEO≥95 A11y≥95 BP≥95). (3) GitHub Actions: PR'da lint + typecheck + vitest + pytest(rota) + site build; main'de ek olarak e2e (docker servisleriyle) + Lighthouse CI. (4) `main` branch koruması talimatını bana yaz (manuel uygulayacağım).
**Yapılmayacaklar:** test uğruna üretim kodunu çarpıtma; flaky test bırakma (retry ile maskeleme).
**Doğrulama:** Actions ilk koşuda yeşil; e2e 3 akış geçiyor; Lighthouse raporu PR yorumunda.

## T-15 — Editoryal altyapı (/rehber)
**Amaç:** Hub içeriklerin yayınlanabileceği sistem + ilk yazı.
**Katman:** site.
**Yapılacaklar:** (1) `site/content/rehber/*.mdx` düzeni: frontmatter (baslik, aciklama, kapak, yazar, tarih, hedef anahtar kelime), MDX render (next-mdx-remote veya @next/mdx — Next 16 uyumuna Context7'den bak), `/rehber` indeks + `/rehber/[slug]` sayfası, Article JSON-LD + yazar kartı (Person, T-11 verisi) + "yazıdaki yerler" kutusu (frontmatter'daki yer slug'larından otomatik kartlar → iç link). (2) İlk yazı iskeleti: "Samsun'da Gezilecek Yerler — 2026 Güncel Liste": API'den skor sıralı ilk 20 yer + her biri için 2-3 cümlelik şablon giriş + insan eliyle yazılacak bölümler için `TODO(hiranur)` işaretleri. (3) sitemap + breadcrumb entegrasyonu.
**Yapılmayacaklar:** yazı içeriğini tamamen otomatik üretme (E-E-A-T + scaled content riski — iskelet otomatik, cümleler insan); CMS kurma (MDX yeterli).
**Doğrulama:** `/rehber/...` Article validator'dan geçiyor; yer kutuları doğru slug'lara link veriyor; indeks sayfası sitemap'te.

---

## T-16 — Sinematik makyaj (P1–P6, `yon.md`)
**Amaç:** K5/K6/K7 + K8/K9. Şartname: `plan/tasarim/yon.md`. Model: Grok 4.6 extra high (K10). Auto yasak.
**Katman:** site + `plan/tasarim/` + public varlıklar.
**Lint anayasası (her pakette):** iç gezinme `next/link`; görseller `next/image`; render sırasında ref okuma yok; effect gövdesinde senkron `setState` yok (kaydırma CSS `animation-timeline` veya olay dinleyicisi); diyalog/sheet Escape ile kapanır.

**P1 — Marka varlıkları** (ön koşul: yok; **kapandı**)
K8 logosundan üretim seti (`site/scripts/logo_uretim.mjs`); vektörleştirme yok (kaynak PNG sabittir). Ufuk varlık/bileşen yok; header kilidi karo + wordmark. Doğrulama: favicon + `/` kilidi.

**P2 — Tokenlar** (ön koşul: P1)
`yon.md` §1.2 palet (bordo rampı, `tuz`), §1.3 tipografi ölçeği, §1.4 boşluk, §1.6 köşe (kontrol 8 px, kart 12 px, plaka 0/4), §4.1 zamanlama. `.dalga` / `.serit-kaydir` / `.sonar-halka` / `.samandira-suz` kaldır. `deniz` veri katmanına iner. Doğrulama: tokenlar `@theme`'de; kontrast tablosu §1.2.

**P3 — Bileşen kütüphanesi** (ön koşul: P2)
`yon.md` §3 davranış tanımları: sticky header, footer 4 kolon, `Plaka`, kart/CTA/rozet/bölüm başlığı/istatistik/boş durum/iskelet. `/tasarim-sistemi` vitrini (noindex) bu sözleşmeyi listeler. Ölü link yok. Doğrulama: vitrin 375+1280; boş ve dolu kart yüksekliği aynı.

**P4 — Hero sekansı** (ön koşul: P3)
`yon.md` §2: asimetrik split; Faz A/B; Yol B (Unsplash plaka kurgusu) köprü, künye `plan/tasarim/gorsel-kaynak.md`. Video yok. `prefers-reduced-motion` → statik kapak. Bütçe ≤ 900 KB / ≤ 380 KB. Doğrulama: ağ sekmesi bayt; reduced-motion kare indirmiyor.

**P5 — Sayfa makyajı** (ön koşul: P4)
`yon.md` §4.2 koreografi + §6 yerleşim eşikleri. Ana, keşif, yer, bölgeler, sihirbaz, 404. Bölüm adları kullanıcı sorusu. Mini CTA + doruk CTA. Doğrulama: tarayıcı akışı (tek ekran kanıt değil).

**P6 — Doğrulama** (ön koşul: P5)
`yon.md` §8 on kapı: Lighthouse mobil Perf≥80 SEO≥95 A11y≥90 BP≥90; CLS≤0,02; reduced-motion 0 hidrasyon uyarısı; ölü link taraması; "Rotam" yok.

**Yapılmayacaklar:** yeni bağımlılık (motion kurulu; sharp yalnız üretim script'i); 21st.dev kopyala-yapıştır; rota motoru/veri; logoyu yeniden çizmek; marquee; ağır tema; Auto mod.
**Doğrulama:** paket kapıları yukarıda; görev kullanıcı onayıyla kapanır.

---


## Backlog (sırası gelince talimatlaştırılır)
| # | İş | Not |
|---|---|---|
| B-01 | Keşif listesine "daha fazla yükle" | Brifteki örnek talimat aynen kullanılabilir: `GET /sehirler/{anahtar}/yerler` zaten limit/offset/toplam_sayi dönüyor; rota motoruna/taksonomiye/keşif filtresine dokunma; `/sehir/samsun`'da ikinci sayfayı tarayıcıda doğrula |
| B-02 | Web haritası (MapLibre) | Şartname: `plan/06_mobil_ve_harita.md` §1 — yer detay mini harita + rota polyline |
| B-03 | Sponsorluk hazırlığı | Rozet UI (`signal` rengi, "Sponsorlu"), `/sponsorluk` sayfasının noindex'ten açılması — **yalnız büyüme kararı değişince** |
| B-04 | İkinci şehir: Trabzon | Playbook ölçümlü: `sehir_ayarlari.py`'ye kayıt → toplayıcılar → aktarım → site otomatik. Kaç saat/satır sürdü kaydet (case study malzemesi) |
| B-05 | PWA | manifest + SW offline kabuk + share target (`plan/06` §2) |
| B-06 | Public repo ayrımı | `veri/` → private `samandira-veri`; public `samandira`: sunucu+site+ortak+dokumanlar+plan (K2 kırmızı çizgisi e) |
| B-07 | Rota PDF dışa aktarma | Paylaşılabilirlik + ileride premium adayı |
| B-08 | Rota paylaşım sosyal kartı iyileştirme | T-07 sonrası metrikle karar |

## Manuel işler (Cursor yapamaz — sizin liste)
1. `samandira/` klasörünü repoya `plan/` olarak kopyala (T-00 ön şartı).
2. Postgres read-only rol (`plan/03` §3'teki SQL) — sonra mcp.json yorumunu aç.
3. GitHub: repo rename `gezi_bot` → `samandira`; `main` koruması; iki profilde pin; (B-06 zamanı gelince veri repo ayrımı).
4. GoDaddy DNS kayıtları (`plan/05` §5) + Oracle instance (§1) + SSH anahtarı.
5. GSC + Bing Webmaster (T-06 sonrası), UptimeRobot, Oracle bütçe alarmı.
6. Sosyal hesaplar: Instagram/X/TikTok/YouTube `@samandira...` (handle ASCII) + TÜRKPATENT marka ön araştırması (`plan/04` §9).
7. Fotoğraf çekim planı: ilk 30 yer (kendiniz çekin — en özgün içerik; hafta sonu 2 tur yeter).
8. Logo FİNAL (K8, 2026-09-05): `plan/logo/secili/logo.png`. Slogan + GEO tanım cümlesi kilit. Eski turlar: `plan/logo/arsiv/`. Yön: `plan/tasarim/yon.md`.
