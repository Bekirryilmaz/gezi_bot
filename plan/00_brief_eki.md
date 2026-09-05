# Şamandıra — Brief Eki (2026-09-05)
> Bu dosya, orijinal proje brifinin (Rotam brifi) **üzerine** okunur. Çelişki olursa bu ek kazanır. Cursor oturumlarına brifle birlikte yapıştırılır.

## 1. Marka değişikliği
- Ürün adı artık **Şamandıra** (eski: Rotam). Stüdyo/şemsiye: **Alegre Group**.
- Kullanıcıya görünen hiçbir yerde "Rotam" kalmaz: site metinleri, `<title>`, footer, OG, favicon, manifest, API başlığı (`Gezi Platformu API` → `Şamandıra API`), README'ler, dokümanlar.
- **Kod tanımlayıcıları değişmez** (`rota_olustur`, `duygu_skoru` vb. kalır). Repo adı `gezi_bot` → `samandira` (manuel, GitHub'da).
- Ekip: Bekir Yılmaz (veri/sunucu/rota/devops + B2B) — captain.cook.023@gmail.com · Hiranur Doğan (site/SEO/içerik/analitik) — hiranur7791@gmail.com · GitHub: Bekirryilmaz / hira1im.

## 2. Alan adı ve yayın
- Canonical: `https://şamandıra.com` — punycode: `xn--amandra-vfb22b.com` (IDN; DNS GoDaddy, 2 yıllık alındı).
- ASCII `samandira.com` başkasında (HugeDomains satılık) → alınmayacak. Tüm varyantlar canonical'a 301.
- E-postada IDN kullanılmayacak (deliverability); ASCII alias (Gmail) kullanılır.
- Şu an yayın: dev tunnel (`qk4cmqnw-3000/8125.euw.devtunnels.ms`) + **`npm run dev`** → geçici. Hedef: Oracle Cloud Ampere A1 (PAYG, ücretsiz kota: 4 OCPU/24GB/200GB blok/10TB egress) + Docker + Caddy + prod build. Detay: `05_deployment_oracle.md`.
- API dışarıdan yalnız `api.şamandıra.com` alt alan adıyla (CORS: canonical origin); DB asla public değil.

## 3. Kararlar (2026-09-05, kullanıcı onaylı)

> **Tek karar metni.** Arena'nın 2026-09-05 plan taslakları (`01`–`07`, `BASLA`) ve T-16 Faz 1 notları (`logo/arastirma.md`) bu listeyle okunur. Çelişkide **bu madde + `plan/tasarim/yon.md` kazanır.** Logo keşfi (Ufuk/Sonar/Rota/Demir, A-B-C, `/tasarim-secim`) tarihçedir.

1. **Büyüme öncelikli**: ilk 9 ay trafik/ürün/portföy; monetizasyon (sponsorluk, affiliate, hibe satışı) mezuniyet sonrası. Sponsor altyapısı (rozet UI, fiyat sayfası taslağı) hazırlanır ama satış yapılmaz.
2. **Veri kaynağı ifşası yok**: sitede hangi kaynaktan veri geldiği belirtilmez; ham veri/yorum/kullanıcı bilgisi yayınlanmaz — yalnız duygu analizi türevleri (özet, skor, profil).
   **Kırmızı çizgiler:** (a) ham yorum metni + yorumcu adı/takma adı asla görünmez; `ornek_ifade` parçacıkları anonim ve ≤10 kelime, (b) `© OpenStreetMap contributors` atfı footer'da **kalır** (ODbL yasal zorunluluk), (c) scraping fotoğrafları sitede kullanılmaz (kendi çekimimiz / Places API / izinli kaynak), (d) toplayıcılar yalnız geliştirme makinesinde çalışır, canlı sunucuya scraping kurulmaz, (e) repo public açılırken `veri/` ayrı **private** repoya taşınır (`samandira-veri`), public repo: `sunucu/ site/ ortak/ dokumanlar/`, (f) `/gizlilik` (KVKK), `/kullanim-kosullari`, `/iletisim`, `/hakkimizda` sayfaları eklenir.
3. **Bitirme projesi değil**: portföy/girişim projesi. Faz 6 = demo video + case study + public repo + hafif ölçüm.
4. **Rebrand derinliği**: yüzey + repo/dokümanlar (kod içi tanımlayıcılar hariç).
5. **Tasarım çıtası "oha" (K5):** Sitede etkileyici hero, mikro etkileşimler ve **ufak** logo göndermeleri olacak — görev T-16 (`yon.md` P1–P6). Slogan **"Gezilecek yerleri işaretler."** ve GEO tanım cümlesi kilitli (Faz 1'den kalan geçerli seçim). **Tüm tasarım işleri Cursor'dadır;** Arena tasarım ÜRETMEZ. İlk SVG turu ve `/tasarim-secim` sergisi kapatıldı.
6. **Kapsam: tüm Türkiye (2026-09-05):** Ürün Karadeniz'e kilitli DEĞİLDİR; tüm Türkiye'yi kapsar. Samsun ilk çıkış plajıdır (bildiğimiz şehir), markanın sınırı değil. Tüm marka metinleri/başlıklar/slogan/tasarım bölge-nötr olacak ("Karadeniz'in kişisel gezi rehberi" vb. düzeltilecek — T-03 madde 8). Yeni şehir eklemek = yalnız `veri/ortak/sehir_ayarlari.py` kaydı + veri (B-04 playbook); kodda/tasarımda değişiklik gerektirmeyecek şekilde kurulur.
7. **Baş kriter SEO + GEO (2026-09-05):** Tüm içerik/slogan/metadata/tasarım kararlarında birinci öncelik klasik SEO ve **GEO** (yapay zekâ asistanlarınca alıntılanma: ChatGPT/Perplexity/Gemini). Sloganın başka markalara benzerliği kullanıcı talimatıyla önemsizdir; sloganda aranır kelime + AI-alıntılanabilir tanım cümlesi aranır. GEO kuralları: `02_seo_mimarisi.md` §11; uygulama: T-06 madde 9.
8. **K8 — Logo FİNAL (2026-09-05):** Marka işareti **kullanıcının verdiği illüstrasyondur**: `plan/logo/secili/logo.png` — bordo karo üzerine beyaz çizgi şamandıra (kafes kule, fener, rüzgâr gülü/anemometre, bağlama halkaları, dalga hattı). Bu dosya **SABİTTİR**: Cursor çizgiyi, kompozisyonu, oranı, renkleri **değiştirmez**; yalnız **üretim varlıkları** üretir (favicon seti 16/32/48 + `.ico`, apple-touch 180, PWA 192/512 + maskable, OG karosu, şeffaf/açık zemin PNG). **Ufuk ve önceki tüm logo turları (Sonar / Rota / Demir / A-B-C) GEÇERSİZDİR**; `plan/logo/arsiv/` yalnız tarihçedir. Logodan ölçülen kilit değerler: bordo **#6C0000**, çizgi **#FFFFFF**, karo köşe yarıçapı kenarın **%14,6'sı**. **Site tasarımı şamandıra konseptini birebir yansıtmak zorunda DEĞİLDİR:** denizcilik teması sayfa yüzeyine yayılmaz; gönderme yalnız **"ufak trikler"** ile yapılır (kapalı liste: `plan/tasarim/yon.md` §5). Ağır tema **yasak**: her bölümde dalga bandı, çıpa/pusula/dümen ikonografisi, halat-düğüm dokusu, denizci çizgisi, "ahoy/kaptan" dili.
9. **K9 — Hero = fotoğraf sekansı (2026-09-05):** Ana sayfa hero'su **fotoğraf sekansı (flipbook)** ile video hissi verir; **video dosyası (mp4/webm/gif) YOKTUR**. Görsel kaynak listesi **kapalıdır**: **(a) kendi çekimimiz** (birincil, T-09 + manuel iş #7 ile aynı hat) veya **(b) Unsplash lisanslı fotoğraf** (köprü). **Scraping fotoğrafı YASAK** (K2 kırmızı çizgisi c); stok video, AI ile üretilmiş fotoğraf ve hotlink de yok. Unsplash kuralları: elle indirme (**API kullanılmaz** — API Şartları atıf + indirme takibi zorunluluğu getirir), tanınabilir yüz veya marka/tabela içeren kare kullanılmaz (model izni ve marka hakkı lisansa dâhil değil), Unsplash karesi **asla belirli bir yerin fotoğrafı gibi sunulmaz** (yer kartı/yer detay fotoğrafı yalnız kendi çekimimiz), her karenin künyesi `plan/tasarim/gorsel-kaynak.md`'ye yazılır. Mekanizma şartnamesi: `plan/tasarim/yon.md` §2.
10. **K10 — Model bütçesi (2026-09-05):** Yaratıcı yön **Opus** ile tek oturumda kapatılmıştır (çıktı: `plan/tasarim/yon.md`); **tüm uygulama Grok 4.6 extra high** ile yapılır. **Cursor Auto modu kullanılmaz.** Yeni yaratıcı tur açmadan önce `plan/tasarim/yon.md` yeterli mi diye bakılır; doküman cevaplıyorsa Opus'a dönülmez.

## 4. Canlı denetim anlık görüntüsü (2026-09-05) — düzeltilecekler
- `npm run dev` ile yayın (prod build şart) · robots.txt 404 · sitemap.xml 404 · JSON-LD 0 · canonical yok · OG yok · her sayfada aynı description · `/yer/{uuid}` URL'leri (slug şart) · keşif sayfasında 0 görsel · 60 kayıt alfabetik + gürültülü (cami/park ağırlıklı; kürasyon + skor sıralaması şart) · 404 sayfası İngilizce Next default · API başlığı jenerik.
- Sağlam olanlar: SSR çalışıyor, tema tokenları (`deniz/kopuk/kumsal/gunes`) oturmuş, Sora+Fraunces fontları yüklü, API 9 endpoint ayakta.
- **Veri varlığı (2026-09-06 doğrulandı): DB'de 1.719 yer kaydı var** (`SELECT count(*) FROM yerler`); keşif vitrini varsayılan limit nedeniyle ilk 60'ını gösteriyor. T-05 (slug) + T-08 (kürasyon/eşik) sonrası ~1.700 yer sayfası = programatik SEO'nun ana gövdesi. Kalite eşiği (fotoğraf + metin doluluğu) olmadan hepsini index'e AÇMA (doküman #02 §7.1).

## 5. Yeni hedef mimari (özet)
```
GoDaddy DNS (şamandıra.com → Oracle reserved IP)
  → Caddy (HTTPS/IDN cert, www→apex 301, güvenlik başlıkları)
      ├─ site: Next 16 prod (standalone)  — SSR → http://api:8125 (docker içi)
      │        tarayıcı → /backend/* rewrite → api
      ├─ api:  FastAPI 8125 (yalnız iç ağ + opsiyonel api. alt alan adı)
      ├─ db:   PostGIS 5432 (yalnız iç ağ)
      └─ umami: analitik (KVKK dostu, çerezsiz)
Geliştirme makinesi (Windows): toplayıcılar + aktarım + yerel test; veri JSONL burada kalır.
```
- URL tasarımı: `/sehir/samsun`, `/sehir/samsun/gezilecek-yerler`, `/sehir/samsun/bolgeler/atakum`, `/yer/samsun/{slug}`, `/rota/{id}`, `/rehber/{slug}`. Slug: DB'de `yerler.slug` (migration `0005_yer_slug`), üretim `ortak/metin_araclari.py::slug_uret` (Türkçe→ASCII), UUID URL'ler 301.
- JSON-LD: Organization, WebSite, BreadcrumbList, TouristDestination (şehir), TouristAttraction/Museum/Restaurant/... (yer — taksonomiden eşleme), City (ilçe), ItemList (rota), Article (rehber). **AggregateRating YASAK** (skorlar türetilmiş metrik, Google politika ihlali).
- Rota sihirbazı `noindex,follow`; paylaşılan rota `/rota/{id}` indexlenebilir + dinamik OG image.

## 6. Doküman haritası (bu klasör — workspace `samandira/`)
| Dosya | İçerik |
|---|---|
| `BRIF.md` | orijinal proje brifi (Rotam dönemi, tarihî belge — değişmez) |
| `00_brief_eki.md` | bu dosya — kararlar + güncel durum |
| `01_urun_analizi_ve_strateji.md` | derin analiz, pazar, gelir modelleri, riskler, 9 aylık yol haritası, KPI |
| `02_seo_mimarisi.md` | URL/slug şartnamesi, metadata şablonları, JSON-LD, içerik planı, keyword haritası |
| `03_cursor_araclari_kurulumu.md` | Cursor rules/MCP/skill kurulumu + kalite kapıları |
| `04_marka_ve_tema.md` | Şamandıra marka sistemi: logo, palet, tipografi, ses tonu |
| `05_deployment_oracle.md` | Oracle canlıya alma: adım adım komutlar, compose, Caddy, yedek |
| `06_mobil_ve_harita.md` | web haritası (MapLibre) + PWA + Capacitor/Expo + store süreçleri |
| `07_cursor_talimatlari.md` | numaralı, kopyalanabilir Cursor görev paketleri (T-00 … T-17) + manuel işler |
| `logo/` | `secili/logo.png` = **FİNAL (K8)**; `arastirma/` tarama + tarihçe notları; `arsiv/` reddedilen SVG/PNG; `faz2-dogrulama/` ekran kayıtları |
| `tasarim/` | `yon.md` — görsel yön, hero sekans şartnamesi, bileşen + hareket + yerleşim sözleşmesi (K8/K9 üzerine kurulu) |

## 7. Ajana ek çalışma kuralları (brifin §4'üne ek)
- Marka: kullanıcıya görünen metinlerde "Şamandıra"; "Rotam" yazma. API başlığı/description'ı Şamandıra olarak güncelle.
- Kaynak ifşası: UI/metin şablonlarında "Google'dan alındı", "Ekşi yorumları" gibi ifadeler kullanma; duygu özeti "ziyaretçi yorumlarından derlenmiştir" düzeyinde jenerik kalır. OSM atfı hariç (footer'da kalır).
- Slug: yeni yer bağlantısı her zaman `/yer/{sehir}/{slug}`; UUID linki üretme.
- Yeni sayfa = benzersiz title/description + canonical + JSON-LD + sitemap kaydı (doküman #02).
- Prod disiplin: `npm run dev` çıktısı canlıya taşınmaz; yayın `next build && next start` (Docker standalone).
- Ham yorum metni/yorumcu adı render eden bileşen yazma; `ornek_ifade` anonim + kısa.
- Deploy dosyalarına (Dockerfile, compose, Caddyfile) sır/parola gömme; `.env` + `.env.example` düzeni.
