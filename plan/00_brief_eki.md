# Şamandıra — Brief Eki (2026-09-05)
> Bu dosya, orijinal proje brifinin (Rotam brifi) **üzerine** okunur. Çelişki olursa bu ek kazanır. Cursor oturumlarına brifle birlikte yapıştırılır.

## 1. Marka değişikliği
- Ürün adı artık **Şamandıra** (eski: Rotam). Stüdyo/şemsiye: **Alegre Group**.
- Kullanıcıya görünen hiçbir yerde "Rotam" kalmaz: site metinleri, `<title>`, footer, OG, favicon, manifest, API başlığı (`Gezi Platformu API` → `Şamandıra API`), README'ler, dokümanlar.
- **Kod tanımlayıcıları değişmez** (`rota_olustur`, `duygu_skoru` vb. kalır). Repo adı `gezi_bot` → `samandira` (manuel, GitHub'da).
- Ekip: Bekir Yılmaz (veri/sunucu/rota/devops + B2B) — captain.cook.023@gmail.com · Hiranur Doğan (site/SEO/içerik/analitik) — hiranur7791@gmail.com · GitHub: Bekirryilmaz / hira1im.

## 2. Alan adı ve yayın
- Canonical: `https://şamandıra.com` — punycode: `xn--amandra.com-3zb60d` (IDN; DNS GoDaddy, 2 yıllık alındı).
- ASCII `samandira.com` başkasında (HugeDomains satılık) → alınmayacak. Tüm varyantlar canonical'a 301.
- E-postada IDN kullanılmayacak (deliverability); ASCII alias (Gmail) kullanılır.
- Şu an yayın: dev tunnel (`qk4cmqnw-3000/8125.euw.devtunnels.ms`) + **`npm run dev`** → geçici. Hedef: Oracle Cloud Ampere A1 (PAYG, ücretsiz kota: 4 OCPU/24GB/200GB blok/10TB egress) + Docker + Caddy + prod build. Detay: `05_deployment_oracle.md`.
- API dışarıdan yalnız `api.şamandıra.com` alt alan adıyla (CORS: canonical origin); DB asla public değil.

## 3. Kararlar (2026-09-05, kullanıcı onaylı)
1. **Büyüme öncelikli**: ilk 9 ay trafik/ürün/portföy; monetizasyon (sponsorluk, affiliate, hibe satışı) mezuniyet sonrası. Sponsor altyapısı (rozet UI, fiyat sayfası taslağı) hazırlanır ama satış yapılmaz.
2. **Veri kaynağı ifşası yok**: sitede hangi kaynaktan veri geldiği belirtilmez; ham veri/yorum/kullanıcı bilgisi yayınlanmaz — yalnız duygu analizi türevleri (özet, skor, profil).
   **Kırmızı çizgiler:** (a) ham yorum metni + yorumcu adı/takma adı asla görünmez; `ornek_ifade` parçacıkları anonim ve ≤10 kelime, (b) `© OpenStreetMap contributors` atfı footer'da **kalır** (ODbL yasal zorunluluk), (c) scraping fotoğrafları sitede kullanılmaz (kendi çekimimiz / Places API / izinli kaynak), (d) toplayıcılar yalnız geliştirme makinesinde çalışır, canlı sunucuya scraping kurulmaz, (e) repo public açılırken `veri/` ayrı **private** repoya taşınır (`samandira-veri`), public repo: `sunucu/ site/ ortak/ dokumanlar/`, (f) `/gizlilik` (KVKK), `/kullanim-kosullari`, `/iletisim`, `/hakkimizda` sayfaları eklenir.
3. **Bitirme projesi değil**: portföy/girişim projesi. Faz 6 = demo video + case study + public repo + hafif ölçüm.
4. **Rebrand derinliği**: yüzey + repo/dokümanlar (kod içi tanımlayıcılar hariç).

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
| `logo/` | SVG logo konseptleri + önizleme sayfası |

## 7. Ajana ek çalışma kuralları (brifin §4'üne ek)
- Marka: kullanıcıya görünen metinlerde "Şamandıra"; "Rotam" yazma. API başlığı/description'ı Şamandıra olarak güncelle.
- Kaynak ifşası: UI/metin şablonlarında "Google'dan alındı", "Ekşi yorumları" gibi ifadeler kullanma; duygu özeti "ziyaretçi yorumlarından derlenmiştir" düzeyinde jenerik kalır. OSM atfı hariç (footer'da kalır).
- Slug: yeni yer bağlantısı her zaman `/yer/{sehir}/{slug}`; UUID linki üretme.
- Yeni sayfa = benzersiz title/description + canonical + JSON-LD + sitemap kaydı (doküman #02).
- Prod disiplin: `npm run dev` çıktısı canlıya taşınmaz; yayın `next build && next start` (Docker standalone).
- Ham yorum metni/yorumcu adı render eden bileşen yazma; `ornek_ifade` anonim + kısa.
- Deploy dosyalarına (Dockerfile, compose, Caddyfile) sır/parola gömme; `.env` + `.env.example` düzeni.
