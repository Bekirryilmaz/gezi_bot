# Şamandıra — SEO Mimarisi ve Uygulama Planı
**Tarih:** 2026-09-05 · Durum: Canlı denetim yapıldı (dev tunnel), bulgular güncel

> **Karar kaynağı:** `plan/00_brief_eki.md` §3 (K7 SEO+GEO kilit). Çelişkide o madde kazanır.

> İlke: **"Sitenin daha baştayken güzel kurgulanması"** = URL'ler, şema (JSON-LD), metadata ve içerik mimarisi ilk 6 haftada doğru kurulur; sonra değiştirmek 301 yükü ve otorite kaybı demek. Bu doküman o temelin şartnamesidir.

---

## 1. Denetim özeti (ne yok?)

| Katman | Durum (2026-09-05) |
|---|---|
| robots.txt | ❌ 404 |
| sitemap.xml | ❌ 404 |
| JSON-LD (yapılandırılmış veri) | ❌ 0 adet |
| canonical | ❌ yok |
| Open Graph / Twitter Card | ❌ yok |
| Meta description | ⚠️ her sayfada aynı metin |
| URL'ler | ❌ `/yer/{uuid}` |
| Görseller | ❌ keşif sayfasında 0 `<img>` |
| Yayın modu | ❌ `npm run dev` (HMR/devtools dışarı açık) |
| SSR | ✅ çalışıyor (içerik HTML'de) |
| lang=tr, next/font | ✅ var |

---

## 2. Alan adı ve host kuralları

- **Canonical host:** `https://şamandıra.com` (punycode: `xn--amandra-vfb22b.com`)
- `www.şamandıra.com`, `http://*`, punycode varyantları → **301** ile canonical'a.
- Sertifikada her iki form: `xn--amandra-vfb22b.com` + `www.xn--amandra-vfb22b.com` (Let's Encrypt/Caddy otomatik halleder; Caddyfile'da site adresini punycode yazın).
- Kod/env'de her zaman **punycode** saklanır; kullanıcıya gösterimde Unicode (IDN kuralı: DB'de ASCII, ekranda Unicode).
- `NEXT_PUBLIC_SITE_URL=https://şamandıra.com` (veya punycode — canonical üretiminde tek biçim kullanın; öneri: canonical'ları punycode üret, Google ikisini de aynı host sayar).
- GSC/Bing'e alan adını eklerken punycode görünür — normal, endişe yok.

---

## 3. Bilgi mimarisi ve URL tasarımı (en kritik karar)

### 3.1 Hedef ağaç

```
/                                   → Ana sayfa (marka + şehir seçimi + değer önerisi)
/sehir/samsun                       → Şehir hub: öne çıkanlar, kategoriler, ilçe kısayolları, rota CTA
/sehir/samsun/gezilecek-yerler      → Kategori listesi (statik yol, ?kategori= yerine)
/sehir/samsun/yeme-icme             → Kategori listesi
/sehir/samsun/bolgeler              → İlçe/bölge indeks
/sehir/samsun/bolgeler/atakum       → İlçe sayfası (profil + duygu özeti + ilçe yerleri + SSS)
/sehir/samsun/rota                  → Rota sihirbazı (noindex,follow — araç sayfası)
/rota/{rota_id}                     → Paylaşılan rota (indexlenebilir, OG image ile viral)
/yer/samsun/{slug}                  → Yer detayı (slug!)
/rehber/{yazi-slug}                 → Editoryal rehber yazıları (hub içerik)
/hakkimizda  /kullanim-kosullari  /gizlilik  /iletisim  /sponsorluk
```

**Karar notları:**
- `/sehir/[anahtar]` yolu **korunur** (Türkçe, mevcut yapı, değişim maliyeti yok). Kategori filtreleri için `?kategori=x` yerine **statik alt yollar** eklenir; query'li sürümler canonical olarak statik yola bakar.
- `/yer/{uuid}` → `/yer/{sehir_anahtari}/{slug}`. UUID'li eski URL'ler **301** ile yenisine.
- **Slug kuralları:** Türkçe karakter → ASCII (`bandırma → bandirma`, `ı→i, ş→s, ğ→g, ü→u, ö→o, ç→c`); kelimeler `-`; max ~60 karakter; benzersizlik şehir kapsamında (`slug` alanı DB'de `(sehir_id, slug)` unique); çakışırsa sonuna kısa sayı (`-2`). Örnekler: `bandirma-vapuru-muzesi`, `amisos-tepesi`, `kizilirmak-deltasi-kus-cenneti`, `sahinkaya-kanyonu`.
- **Slug üretim kaynağı:** yer adı + (gerekirse) alt kategori kelimesi; aktarım sırasında deterministik üretilir, DB'de saklanır (migration `0005_slug`), **asla runtime'da tahmin edilmez**. Ad değişirse slug değişmez (stabilite > tazelik); zorunlu değişimde 301 tablosu.

### 3.2 Veri katmanı değişiklikleri (API + DB)

1. Migration `0005_yer_slug`: `yerler.slug TEXT` + `UNIQUE (sehir_id, slug)` + index.
2. Aktarım (`sunucu/veritabani/aktarim/calistir.py`): slug üretimi (ortak yardımcı `ortak/metin_araclari.py::slug_uret(ad)` — Türkçe transliterasyon burada, veri+sunucu ortak kullanır).
3. API şemaları: `YerOzet/YerDetay` şemalarına `slug` ve `seo_baslik?` alanları; `/sehirler/{anahtar}/yerler` yanıtına slug eklenir (geriye uyumlu: ekleme, çıkarma yok).
4. Yeni endpoint önerileri (SEO sayfaları için):
   - `GET /sehirler/{anahtar}/bolgeler/{ilce_slug}` (tek ilçe detayı — şu an liste var)
   - `GET /yerler/{slug_or_id}/benzer` (PostGIS ile yakındaki yerler → iç link + oturum derinliği)
   - `GET /sehirler/{anahtar}/istatistik` (yer sayısı, kategori dağılımı, ortalama duygu → hub sayfası metnini veriyle besler)
5. Site: `site/src/lib/api.ts` sarmalayıcıları + `types.ts` hizalanır; linkler slug ile.

---

## 4. Metadata şablonları (sayfa türü bazında)

| Sayfa | title (≤60 kr) | description (≤155 kr) |
|---|---|---|
| Ana | `Şamandıra — Gezilecek Yerler ve Rota Planlayıcı` | `Şamandıra, bir şehirdeki gezilecek yerleri deneyim eksenlerine göre puanlayan ve gün gün rota kuran bir gezi rehberidir.` |
| Şehir hub | `Samsun Gezi Rehberi 2026: Gezilecek Yerler, Rotalar` | `Samsun'da gezilecek {n} yer, {ilçe} ilçe rehberi, yorum bazlı değerlendirmeler ve gün gün rota planı. Şamandıra ile Samsun'u keşfet.` |
| Kategori | `Samsun {Kategori} — En İyi {n} Mekan (2026)` | veri güdümlü: kategori + öne çıkan 2-3 yer adı + CTA |
| Yer detay | `{Yer Adı} — {İlçe}, Samsun | Ziyaret Rehberi` | duygu özeti + kategori + pratik bilgi (süre/fiyat) şablondan; yer bazlı **benzersiz** |
| İlçe | `{İlçe} Gezilecek Yerler — {İlçe}/Samsun Rehberi` | bölge profili duygu özeti + yer sayısı |
| Rota paylaşım | `{n} Günlük Samsun Rotası — Şamandıra` | rota duraklarından otomatik özet |
| Rehber yazısı | `{Konu}: {Kanca} (2026)` | elle yazılır, 150 kr |
| Sihirbaz | — | `noindex, follow` |

Kurallar: her sayfa **benzersiz** description (şablon + veri); title'da marka sonda yalnız ana sayfada; `{n}` gibi sayılar API'den (dinamik, güncel); `generateMetadata` ile server-side; `metadataBase` tanımlı (OG URL'lerinin mutlak olması için).

---

## 5. JSON-LD (schema.org) — sayfa türü haritası

| Sayfa | Tipler |
|---|---|
| Tüm sayfalarda | `Organization` (Şamandıra/Alegre Group, logo, sameAs) + `BreadcrumbList` |
| Ana sayfa | `WebSite` (+ ileride `SearchAction`) |
| Şehir hub | `TouristDestination` (`containsPlace` ile öne çıkan yerler) |
| Yer detay | taksonomiden tip eşlemesi: müze→`Museum`, plaj→`Beach`, park→`Park`, cami→`PlaceOfWorship`, restoran→`Restaurant`, kafe→`CafeOrCoffeeShop`, genel→`TouristAttraction`; ortak alanlar: `name, description(=tanitim_metni), geo, address, image, openingHoursSpecification?, isAccessibleForFree?` |
| İlçe | `City`/`AdministrativeArea` + `containsPlace` |
| Rota paylaşım | `ItemList` (duraklar sıralı) + `Trip`? (`ItemList` yeterli ve güvenli) |
| Rehber yazısı | `Article` (author=Person: Hiranur/Bekir, publisher=Organization, dateModified) |

**Yasaklar/kurallar:**
- ❌ `AggregateRating` **koymayın**: Google politikası yalnız site üzerinde toplanan gerçek kullanıcı değerlendirmelerine izin verir; sizin skorunuz yorum-özetinden türetilmiş iç metrik → manuel işlem (rich result spam) riski. Yıldız göstermek isterseniz ileride gerçek kullanıcı puanlama özelliğiyle birlikte.
- ❌ `FAQPage` yalnız sayfada gerçekten görünen SSS metni varsa (ilçe sayfalarına planlanıyor).
- `schema-dts` paketiyle tip güvenliği; bileşen: `site/src/components/seo/JsonLd.tsx`.
- Doğrulama: Google Rich Results Test + Schema.org validator — her sayfa türü için 1 kez manuel, sonra CI'da JSON-LD varlık testi (Playwright).

---

## 6. sitemap + robots + indeks yönetimi

- `site/src/app/sitemap.ts` (Next native; paket gerekmez): şehir, kategori, ilçe, yer, rehber sayfaları; `lastModified` DB güncelleme zamanından; 5.000 URL altı tek dosya yeterli.
- `site/src/app/robots.ts`: tümüne allow; `/api/*`, `/backend/*`, sihirbaz parametreli akışlar disallow; sitemap referansı.
- **GSC:** alan adı mülkü (DNS doğrulama) + sitemap gönderimi; **Bing Webmaster** (GSC'den içe aktarır) + **IndexNow** (Next için hazır paket var; yer/ilçe sayfaları yayına girince ping).
- 301 planı: UUID→slug kalıcı; eski `/sehir/samsun?kategori=...` → statik yol.
- `GET /rotalar/{id}` paylaşım sayfaları: index açık (UGC değil, kendi üretimimiz; OG image ile sosyal trafik → backlink etkisi).

---

## 7. İçerik stratejisi (thin content'ten kurtulma)

### 7.1 Programatik sayfalar (mevcut veriden)
- **Yer sayfası kalite eşiği:** bir yer sayfası index'e açılmadan önce şunlara sahip olmalı: ≥1 fotoğraf, tanitim_metni ≥ ~60 kelime **veya** duygu_ozeti + profil alanları dolu, koordinat, ilçe. Eşiği geçmeyen yer `noindex,follow` (listedeki linki kalır, zamanla eşik geçilince açılır). Bu kural Google'ın "scaled content abuse" sinyallerine karşı sigortadır.
- Yer sayfası bölümleri: hero (foto+ad+kategori+ilçe), tanıtım (nesnel), duygu özeti (öznel — ayrım UI'da net), pratik bilgi kutusu (fiyat algısı, ortalama süre, kalabalık zamanlar, ulaşım), "Google Maps'te aç" + ileride gömülü harita, **yakındaki yerler** (PostGIS → iç link), "Bu yeri içeren örnek rota" CTA, ilçe breadcrumb.
- **İlçe sayfaları:** 17 ilçe × (profil + duygu özeti + o ilçenin yer listesi + SSS + "ilçede rota kur" CTA). Şu an bolgeler verisi var; sayfa derinliği artırılacak.

### 7.2 Editoryal hub (ilk 10 yazı — arama talebi yüksek, veri elimizde)
1. Samsun'da Gezilecek Yerler — 2026 Güncel Liste (ana keyword; hub sayfası, tüm yerlere link)
2. Samsun 2 Günlük Rota: Adım Adım Plan (rota motoru çıktısından gerçek rota + kırılım)
3. Atakum'da Gezilecek Yerler ve Sahil Rehberi
4. Samsun'da Nerede, Ne Yenir? (Bafra pidesi, Çakallı menemen, kaz tiridi...)
5. Kızılırmak Deltası Kuş Cenneti Rehberi (nasıl gidilir, ne zaman)
6. Şahinkaya Kanyonu Gezi Rehberi
7. Bandırma Vapuru ve Milli Mücadele Rotası (19 Mayıs temalı — milli günlerde trafik pikleri)
8. Samsun Müzeleri: Kent Müzesi'nden Panorama'ya
9. Samsun Plajları: Atakum'dan Yakakent'e
10. Samsun'a Hafta Sonu Kaçamağı: İstanbul/Ankara'dan Ulaşım + Plan

Kurallar: her yazı ≥1.200 kelime, özgün fotoğraf (Samsun'da yaşıyorsunuz — en büyük koz), iç linkler yer sayfalarına, `Article` JSON-LD, yazar profili (E-E-A-T: OMÜ + Alegre Group), güncelleme tarihi görünür. Ayda 2-4 yazı ritmi sürdürülebilir.

### 7.3 Fotoğraf kampanyası (SEO + dönüşüm için şart)
- Kaynak sırası: (1) kendi çekimleriniz (telif sizde, en özgün), (2) Google Places API fotoğrafları (resmî kullanım, attribution kurallarına uy), (3) belediye/kültür müdürlüğü basın materyali (izinle), (4) Wikimedia Commons (lisans kontrolü + atıf). **Scraping görsel kullanmayın.**
- Teknik: `next/image`, AVIF/WebP, `alt="{yer adı} — {ilçe}, Samsun"`, lazy, hero için `priority`, blur placeholder. Fotoğraflar DB'de `fotograflar` şemasına (şema zaten var) aktarım hattıyla.

---

## 8. Teknik SEO şartnamesi

- **Prod build:** `next build && next start` (doküman #05'te Docker/Caddy ile). Dev modda yayın = otomatik diskalifiye.
- **ISR/caching:** yer ve ilçe sayfaları `revalidate: 86400` (24s), şehir hub `21600` (6s), ana sayfa `3600`; rota paylaşım sayfası `on-demand revalidate` veya kısa.
- **Core Web Vitals bütçesi:** LCP < 2.5s (hero görsel + font), CLS < 0.1, INP < 200ms; Lighthouse CI: Performance ≥ 85, SEO ≥ 95, A11y ≥ 95, Best Practices ≥ 95 — PR'da bütçe aşımı kırmızı.
- **İç link:** breadcrumb (görünür + JSON-LD), "yakındaki yerler", ilçe ↔ yer çift yönlü, footer'da popüler sayfalar; yetim sayfa bırakma (her yer en az 2 iç link alsın).
- **Sayfalama:** keşif listesi "daha fazla yükle" + `rel=next` yerine her sayfa kendi canonical'ı (`/sehir/samsun/gezilecek-yerler?sayfa=2` → canonical kendine; 60 kayıt büyüyünce gerekli).
- **Analytics:** self-host **Umami** (Oracle'da konteyner; KVKK dostu, çerezsiz, cookie banner yükü minimal) + GSC. Olaylar: `rota_olustur_tamamla`, `yer_detay_goruntule`, `sponsor_link_tikla`, `haric_link_tikla`.
- **Gizlilik/çerez:** Umami çerezsiz olsa da `/gizlilik` sayfası + ölçüm açıklaması şart (KVKK aydınlatma).
- **Güvenlik başlıkları:** Caddy'de HSTS, X-Content-Type-Options, Referrer-Policy; CSP kademeli.
- **404/500:** markalı Türkçe not-found sayfası + "Samsun'u keşfet" CTA (şu an İngilizce Next default 404 dönüyor — incelemede görüldü).
- **Mobil:** viewport mevcut; dokunma hedefleri ve liste kartları 360px'te test (Playwright device emulation).

---

## 9. Anahtar kelime haritası (başlangıç seti)

| Küme | Örnek sorgular | Hedef sayfa | Zorluk |
|---|---|---|---|
| Ana | samsun gezilecek yerler, samsun gezi rehberi | `/sehir/samsun` + hub yazı #1 | Yüksek (bloglar tutuyor; uzun vade) |
| İlçe | atakum gezilecek yerler, ilkadım samsun, vezirköprü şahinkaya | ilçe sayfaları + yazı #3,6 | Orta — **kazanılabilir** |
| Yer | bandırma vapuru müzesi, amisos tepesi, samsun kent müzesi | yer detay sayfaları (60 → 500+) | Düşük — **hızlı kazanım** |
| Rota | samsun 2 günlük rota, samsun gezi planı, karadeniz turu rota | yazı #2 + `/rota/{id}` paylaşım | Düşük — rakip az, **fark yaratır** |
| Yeme | samsun'da ne yenir, bafra pidesi nerede | yazı #4 + yeme-içme kategori | Orta |
| Pratik | samsun plajları, samsun müzeleri, samsun'da kahvaltı | kategori + yazı #7-9 | Orta |

Ölçüm: GSC sorgu raporu haftalık; ilk 8 hafta "yer detay" ve "rota" kümelerinde ilk 20'ye girmek gerçekçi hedef.

---

## 10. 6 haftalık uygulama sırası (Cursor görevlerine bölünmüş hâli doküman #07'de)

1. **Hafta 1:** prod build + robots/sitemap + metadata temel (marka "Şamandıra" ile) + 404 sayfası
2. **Hafta 2:** slug migration + API + site link dönüşümü + 301'ler
3. **Hafta 3:** JSON-LD seti + canonical/OG + OG image şablonu (next/og)
4. **Hafta 4:** kategori statik yolları + ilçe detay sayfası + breadcrumb
5. **Hafta 5:** kürasyon (sıralama/eşik) + fotoğraf hattı ilk parti + yer sayfası derinleştirme
6. **Hafta 6:** GSC/Bing/IndexNow + Umami + Lighthouse CI bütçesi + ilk editoryal yazı

---

## 11. GEO — Üretken Motor Optimizasyonu (yapay zekâ asistanlarınca alıntılanma)
**İlke (K7):** ChatGPT, Perplexity, Gemini gibi asistanlar; **kesin, kısa, yapısal ve tutarlı** sayfaları alıntılar. Amaç: "Samsun'da gezilecek yerler / Şamandıra nedir" tarzı sorularda yanıtın içinde biz olmak.

1. **Tek tanım cümlesi (kilit, 2026-09-05):** "Şamandıra, bir şehirdeki gezilecek yerleri deneyim eksenlerine göre puanlayan ve gün gün rota kuran bir gezi rehberidir." Bu cümle ana sayfa, `/hakkimizda`, Organization JSON-LD, `llms.txt` ve sosyal profillerde **kelimesi kelimesine aynı** yer alır. Slogan katı ayrıdır: "Gezilecek yerleri işaretler."
2. **Önce cevap paragrafı:** her sayfa türünde ilk 40-60 kelime, sayfanın arama sorusunu doğrudan yanıtlar (tanım/liste/karşılaştırma); detay sonra gelir.
3. **`llms.txt`:** kökte; site tanımı + ana sayfalar listesi (şehirler, kategori indeksleri, rehber indeksi).
4. **SSS blokları:** en sorulu 3 sayfa türünde görünür S/S + FAQPage JSON-LD ("X'te gezilecek yerler neler?", "Rota nasıl kurulur?", "Skorlar güvenilir mi?").
5. **Alıntılanabilir veri:** sayı + tarih içeren cümleler ("Eylül 2026 itibarıyla Samsun'da 1.719 yer işaretli; skorlar ziyaretçi duygusu + erişilebilirlik kırılımıyla üretilir") — tarih API istatistik ucundan canlı gelir.
6. **Tutarlılık:** marka adı, tanım, iletişim bilgisi tüm sayfalarda ve dış profillerde (GitHub, sosyal) birebir aynı; çelişkili ifade GEO güvenini kırar.
7. **Yasak:** AggregateRating (Google politikası + AI güveni), kanıtsız "en iyi / 1 numara" iddiaları.
