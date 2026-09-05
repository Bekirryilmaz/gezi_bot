# Şamandıra — Ürün Analizi ve Strateji
**Tarih:** 2026-09-05 · **Hazırlayan:** Ürün/planlama asistanı (Arena) · **Ekip:** Alegre Group — Bekir Yılmaz & Hiranur Doğan (OMÜ Bilgisayar Müh. 4. sınıf)

> Bu doküman objektif bir durum tespitidir. Övgü yok, makyaj yok. Amaç: mezuniyete (~Haziran 2027) kadar hem **ticari** hem **akademik** olarak güçlü bir ürün çıkarmak.

---

## 0. TL;DR — Üç cümlelik hüküm

1. **Mühendislik tarafı güçlü ve nadir:** veri toplama → eşleme → duygu → DB → API → deterministik rota motoru → SSR site zincirinin tamamı çalışıyor. Öğrenci projesi seviyesinin belirgin üstünde bir "sistem" var.
2. **Ürün/vitrin tarafı zayıf:** site hâlâ "Rotam" markasında, UUID URL'ler, sıfır fotoğraf, 0 JSON-LD, robots/sitemap yok, aynı meta description her sayfada, alfabetik ve gürültülü yer listesi (onlarca cami/park), üstelik **dev modda** yayın yapılıyor. Yani Google'ın ve kullanıcının gördüğü katman, arka plandaki emeği şu an hiç yansıtmıyor.
3. **Para kısa vadede kullanıcıdan değil, kurumdan ve yerel işletmeden gelir:** Samsun tek şehirli bir rehberin tüketici geliri (affiliate/reklam) ilk 6-12 ayda sembolik kalır; gerçekçi yollar (a) yerel işletme sponsorluğu, (b) belediye/kalkınma ajansı/hibe projeleri, (c) çok şehre ölçeklenince affiliate'tir. En büyük risk ise **veri kaynaklarının hukuki durumu** (Google/Ekşi scraping) — ticarileşmeden önce çözülmeli.

---

## 1. Canlı inceleme bulguları (2026-09-05, dev tünelleri üzerinden)

### 1.1 Site (`qk4cmqnw-3000.euw.devtunnels.ms`)

| Kontrol | Bulgu | Önem |
|---|---|---|
| Marka | `<title>Rotam — Karadeniz'de senin rotan</title>`; ana sayfada 8 yerde "Rotam" | 🔴 Rebrand şart |
| Yayın modu | HTML'de `"b":"development"`, Turbopack HMR client, Next devtools scriptleri → **`npm run dev` ile yayın yapılıyor** | 🔴 Performans + güvenlik + SEO; prod build şart |
| robots.txt | **404** | 🔴 |
| sitemap.xml | **404** | 🔴 |
| JSON-LD | Ana sayfa ve şehir sayfasında **0 adet** | 🔴 |
| canonical | Yok | 🔴 |
| Open Graph | Yok (og:title/og:image yok → WhatsApp/X paylaşımları çirkin) | 🟠 |
| Meta description | Ana sayfa ile `/sehir/samsun` **birebir aynı** metin | 🟠 |
| URL yapısı | `/yer/02fcc326-b543-4eda-...` → UUID. Google ve kullanıcı için anlamsız, telaffuz edilemez, paylaşılamaz | 🔴 Slug şart |
| Keşif listesi | Tam **60 yer**, **0 (sıfır) `<img>`** — hiçbir kartta görsel yok | 🔴 |
| Liste sıralaması | Alfabetik görünüyor ("15 Temmuz Şehitler Parkı", "19 Mayıs Parkı", "30 Ağustos Cami"...) — skor bazlı değil | 🟠 |
| İçerik gürültüsü | İlk 60'ta çok sayıda mahalle camii (Ada Camii, Adalet Cami, Abdullah Paşa Site Cami...), küçük parklar, "ASTORYA", "AYVACIK TEKNE TURU ORGANİZASYON VE SU SPORLARI" gibi kayıt gürültüleri | 🔴 Kürasyon şart |
| SSR | ✅ İçerik HTML'de geliyor (linkler, başlıklar server-side render) — iyi temel | ✅ |
| Tema | `bg-deniz-derin`, `text-kopuk`, `text-gunes` sınıfları çalışıyor; Sora + Fraunces fontları yüklü | ✅ |

### 1.2 API (`qk4cmqnw-8125.euw.devtunnels.ms`)

- `openapi.json` ayakta: **"Gezi Platformu API" v0.1.0**, 9 endpoint doğrulandı (sehirler, yerler, bolgeler, yer detay, rotalar/olustur, olustur-alternatifler, konaklama-bolgesi-oner, rota getir, sabit-rotalar).
- ⚠️ Veri tabanına dokunan endpoint'ler (`/sehirler` vb.) dışarıdan isteklerde **25-90 sn'de yanıt vermedi** (timeout). Site SSR'ı aynı veriyi çekebildiğine göre sorun büyük olasılıkla tünel/cold-start tarafında; ama bu **prod'a dev tunnel ile çıkılamayacağının** canlı kanıtı. Oracle'a geçiş (doküman #05) bu sorunu kökten çözer.
- API başlığı bile hâlâ jenerik: "Gezi Platformu API" → "Şamandıra API" olmalı.

### 1.3 Alan adı ve marka (DNS/HTTP incelemesi)

| Alan adı | Durum |
|---|---|
| `şamandıra.com` (IDN) | ✅ **Sizde.** DNS GoDaddy park IP'lerine (13.248.243.5 / 76.223.105.230) bakıyor → kayıtlı, park halinde. Punycode: `xn--amandra.com-3zb60d` |
| `samandira.com` (ASCII) | ❌ Başkasında — **HugeDomains'ta satılık** (aftermarket, genelde 4 haneli USD). Alınamayacak varsayın. |
| `samandira.com.tr` | ❌ Başka bir sunucuya çözülüyor (85.159.66.62) — dolu. |
| `şamandıra.com.tr` | Boş görünüyor (DNS çözülmüyor) — ileride savunma amaçlı düşünülebilir. |

**IDN değerlendirmesi (objectif):** Google, IDN alan adlarını ASCII ile **eşit** değerlendirir; bilinen bir SEO cezası yok. Gerçek riskler: (1) bazı araçlar/ekranlarda `xn--amandra.com-3zb60d` görünür, (2) **e-posta** tarafında IDN sorunludur (`info@şamandıra.com` deliverability riski), (3) sözlü iletişimde "ş mı, s mi, ı mı i mi" sürtünmesi. Karar önerisi: **canonical = `https://şamandıra.com`**; tüm altyapı (DNS, sertifika, env.) punycode `xn--amandra.com-3zb60d` ile yönetilir; e-posta için ASCII bir alias kullanılır (örn. Gmail/Workspace `alegregroup@gmail.com` veya ileride ASCII bir `.app/.co` alan adı).

**Marka çakışması notu:** "Şamandıra" Türkiye'de (a) İstanbul/Sancaktepe'de bir semt, (b) Fenerbahçe Can Bartu Tesisleri'nin bulunduğu yer olarak güçlü bir futbol çağrışımına sahip. Jenerik "şamandıra" aramalarında bu içeriklerle karışma riski var. Azaltma: "şamandıra gezi", "şamandıra rota", "şamandıra samsun" gibi birleşik marka aramalarını beslemek + TÜRKPATENT'te marka ön araştırması (sınıf 39 "seyahat düzenleme", 42 "yazılım/SaaS", 41 "yayıncılık") yapmak. İsim yine de iyi: denizcilik/yön bulma metaforu Karadeniz + rota ürünüyle birebir örtüşüyor, Türkçe, akılda kalıcı ve `.com`'u sizde.

---

## 2. Ürün nedir, ne olmalı? (Pozisyonlama)

### 2.1 Bugünkü ürün
Samsun için: (1) keşif listesi, (2) bölge/ilçe rehberi + duygu özeti, (3) ilgi ağırlıklarına göre gün gün rota. Konaklama vitrinde gizli; otel dayatmayan alternatifli rota akışı (Senaryo 2) gerçekten iyi bir ürün fikri.

### 2.2 Önerilen pozisyonlama
> **"Şamandıra — Karadeniz'in kişisel gezi rehberi. Keşfet, oku, gün gün rotanı kur."**

- **Ne:** Veri destekli şehir rehberi + rota planlayıcı (editoryal blog değil, OTA değil).
- **Kimin için:** Samsun'a gezi planlayanlar (şehir dışı), hafta sonu kaçamağı arayan yerel halk, öğrenciler; genişlemede Karadeniz rotacıları.
- **Fark ne (rakiplerde olmayan):**
  1. **Şeffaf skorlama:** "Neden bu yer önerildi?" sorusunun kırılımla cevabı (sponsor/klasik/duygu ağırlıkları görünür). Bloglar ve TripAdvisor bunu vermez.
  2. **Yorumdan üretilen duygu özeti + bölge profili:** Ekşi/Google yorumlarından şablon anlatım — özgün, kopyalanamaz içerik (SEO için altın).
  3. **Otel dayatmayan rota motoru:** 2-3 alternatif + konaklama bölgesi önerisi; deterministik, açıklanabilir.
  4. **İlçe bazlı rehber:** Atakum/İlkadım/Vezirköprü... düzeyinde yapılandırılmış sayfa (rakipler genelde tek liste blog yazısı).
- **Ne DEĞİL (bilinçli kapsam dışı):** rezervasyon/ödeme, kullanıcı yorumu yazma (şimdilik), sosyal ağ, İngilizce sürüm (şimdilik).

### 2.3 Ürün adı hiyerarşisi
- **Ürün/marka:** Şamandıra (site, API başlığı, sosyal hesaplar)
- **Şemsiye/stüdyo:** Alegre Group (kurumsal kimlik, B2B teklifler, fatura tarafı, "made by" imzası)
- **Repo:** `gezi_bot` → öneri: `samandira` (ASCII; repo adlarında Türkçe karakter kullanmayın)

### 2.4 Kuzey Yıldızı metriği
Öneri: **haftalık tamamlanan rota oluşturma sayısı** (ürünün gerçekten kullanıldığını ölçer) + yardımcı metrik: **organik oturum** (Google'dan gelen). İkisi birlikte: "bulunuyoruz" + "işe yarıyoruz".

---

## 3. Pazar gerçekleri (objektif, sayılarla)

- **Samsun turizmi:** 2025'in ilk 5 ayında 214.507 konaklamalı turist (yalnızca 11.361'i yabancı) → yıllık ~500-600 bin konaklamalı ziyaretçi; ağırlık **yerli ve günübirlik**. Samsun Kent Müzesi tek başına 2026'nın ilk 8 ayında ~800 bin ziyaretçi (ayda ~100 bin) çekiyor → kentte ciddi bir "gezme" hacmi var ama bu hacmin küçük bir kısmı online rehber arıyor.
- **Arama rekabeti:** "Samsun'da gezilecek yerler" SERP'inde Wise blog, nerdenerede.com, kucukoteller.com.tr blogu, GoTürkiye, Kültür Portalı, belediye sayfaları var. Ana anahtar kelimede blog/otorite siteleri güçlü. **Bizim kazanacağımız alan:** (a) yer detayı long-tail'i ("Bandırma Vapuru ziyaret saatleri", "Amisos Tepesi nasıl gidilir" — yüzlerce düşük rekabetli sorgu), (b) ilçe sayfaları ("Atakum'da gezilecek yerler"), (c) **rota sorguları** ("Samsun 2 günlük rota", "Samsun gezi planı" — yapılandırılmış cevap veren site neredeyse yok), (d) "Samsun gezi rehberi 2026" güncellik oyunu.
- **Gelir gerçekçiliği:** Türkiye gezi nişinde organikten gelen gelir düşük (oturum başına ₺0,05-0,30 aralığı tipik). 10.000 aylık oturum ≈ ₺500-3.000/ay potansiyel (affiliate+reklam karışımı). **Tek şehirle geçim geliri hayaldir; doğru beklenti: ilk yıl = portföy + ilk B2B/sponsorluk gelirleri + ölçeklenme kanıtı.**
- **Affiliate oranları (referans):** GetYourGuide ~%8 (31 gün çerez), Viator ~%8-10 (30 gün), Travelpayouts üzerinden %50'ye varan gelir paylaşımı; Booking.com affiliate ~%4 ve tek oturumluk çerez — ayrıca Booking'in Türkiye içi konaklama satışı yargı kararıyla engelli olduğundan TR trafiği için pratikte zayıf. Ulaşım tarafında obilet/Enuygun iş ortaklıkları Türkiye'ye daha uygun. GetYourGuide/Viator envanteri Samsun'da zayıf, Kapadokya/İstanbul'da güçlü → **affiliate geliri çok şehre açılınca anlam kazanır.**

---

## 4. Gelir modelleri — öncelik sırasıyla

> **Karar (2026-09-05): ilk 9 ay büyüme odaklı.** Aşağıdaki modeller mezuniyet sonrası dönem için sıraya kondu; Faz 5 artık "monetizasyon deneyleri" değil "büyüme sprinti" (bkz. §6). Sponsorluk/affiliate altyapıları hazırlanır ama satış başlatılmaz.

### A) Yerel işletme sponsorluğu (en hızlı, en gerçekçi) 🔴 Öncelik 1
- Altyapı **zaten kodda**: `sponsorlu_mekan` etiketi (+30 rota skoru) ve keşif vitrininde öncelik.
- Paketler: (1) **Vitrin** — profil sayfası zenginleştirme + foto + "Sponsorlu" rozeti, (2) **Rota** — kategori eşleşen rotalarda öncelik (+30 zaten var), (3) **Bölge** — ilçe sayfasında öne çıkan kutusu.
- Fiyat önerisi (başlangıç, Samsun): aylık ₺1.500-5.000/işletme; "kurucu üye" ilk 10 işletmeye %50 indirim + ömür boyu rozet.
- **Etik kural (pazarlanabilirlik için şart):** sponsor içerik her yerde "Sponsorlu" etiketi taşır; skor kırılımında `sponsor +30` zaten şeffaf — bu şeffaflığı rakiplere karşı **pazarlama argümanı** yapın ("biz neden önerdiğimizi gösteririz").
- Kanal: Bekir'in freelance müşteri ağı (nakliyat/inşaat sitesi müşterileri bile referans ağzı), Instagram DM, yüz yüze ziyaret. Hedef: 3 ay içinde 5 ücretli işletme = ₺10-20K/ay.

### B) Kurumsal / hibe / white-label 🔴 Öncelik 2
- **TÜBİTAK 2209-A/B** (üniversite öğrencileri araştırma projeleri) — bu proje için biçilmiş kaftan; çağrı dönemlerini takip edin (genelde sonbahar). OMÜ danışman hocayla başvuru.
- **TÜBİTAK 1512 BiGG** — mezuniyet sonrası girişimleşme (450K+ TL hibe dönemleri oluyor); Şamandıra "seyahat teknolojisi" olarak başvurabilir.
- **TEKNOFEST** yarışmaları (Turizm Teknolojileri, Yapay Zekâ) — görünürlük + ödül + jüri ağı.
- **KOSGEB Girişimci Desteği** — şirket kurunca.
- **B2B white-label:** Samsun Büyükşehir/İl Kültür Turizm Müdürlüğü, **OKA (Orta Karadeniz Kalkınma Ajansı)**, TGA (GoTürkiye) ekosistemi → "şehrin dijital rehberi" projesi. Belediyeler bu tip işlere bütçe ayırıyor; referans olarak çalışan canlı site + teknik rapor güçlü koz. Aynı motor ikinci şehre 1 haftada kurulabiliyorsa bu **ürünleşmiş B2B teklifidir**.
- **Kuluçka:** OMÜ Teknopark / Samsun TEKMER ön kuluçka — ofis + mentörlük + ağ.

### C) Affiliate & komisyon 🟡 Öncelik 3 (çok şehirle birlikte)
- Ulaşım: obilet / Enuygun iş ortaklığı (Samsun'a otobüs/uçak trafiği gerçek).
- Deneyim/tur: GetYourGuide / Viator / Travelpayouts (Samsun zayıf → Trabzon/Amasya/Kapadokya genişlemesiyle güçlenir; "Şahinkaya Kanyonu tekne turu" gibi yerel operatörlerle **doğrudan** anlaşma affiliate'ten daha kârlı olabilir).
- Konaklama: Türkiye'de yasal zemin nedeniyle dikkat; yerel otellerle doğrudan "rezervasyon için arayın/WhatsApp" yönlendirmesi + sabit ücret daha uygulanabilir.

### D) Premium kullanıcı özellikleri 🟢 Uzun vade
- Hesap sistemi gelince: kayıtlı rotalar, çok şehirli seyahat planı, PDF/ offline çıktı, "yolculuk modu". Freemium. Şimdilik kapsam dışı — ama rota paylaşım linki (`GET /rotalar/{id}`) zaten viral tohum; paylaşım sayfasına OG image eklemek bedava büyüme kanalı.

### E) Veri/API lisanslama 🟢 Uzun vade
- Temizlenmiş POI + duygu veri seti ve rota API'si lisanslanabilir. **Dikkat:** OSM verisi ODbL lisanslı (atıf + paylaşım yükümlülüğü), Google verisi ToS'a tabi → ancak kendi özgün katmanınız (duygu özeti, skorlar, profil) lisanslanabilir.

### Yapmayın
- İlk 6 ay AdSense/reklam ağı: trafik düşükken gelir komik, UX'i bozar, "kalitesiz site" sinyali verir.
- İçerik satmak (yerel işletmeden para alıp tanıtım metnini şişirmek): duygu sisteminin nesnelliğini bozar — ürünün ruhuna ihanet.

---

## 5. Riskler ve azaltmalar (önem sırasıyla)

| # | Risk | Etki | Azaltma |
|---|---|---|---|
| 1 | **Veri kaynağı hukuku:** Google Maps scraping ToS ihlali; Ekşi yorumlarının sitede gösterimi telif + KVKK (yorumcu takma adı bile kişisel veri sayılabilir) | Ticarileşme, hibe ve mezuniyet jürisinde en çok sorgulanacak konu; Cease&desist riski | (a) Sitede **ham yorum metni değil** şablon duygu özeti göster (büyük ölçüde zaten böyle — `ornek_ifadeler` alıntılarını kısalt/atıfla), (b) yorumcu adı/takma adı gösterme, (c) vitrin verisini kademeli **resmî kaynaklara** taşı: Google Places API (ücretli, yasal; yorum başına 5 adet döner), OSM (ODbL atıfla serbest), belediye/kültür envanterleri, (d) scraping hattını Ar-Ge/analiz amacıyla sınırla ve dokümante et, (e) siteye Künye/Gizlilik/KVKK aydınlatma sayfaları |
| 2 | **IDN alan adı** (`xn--amandra.com-3zb60d`) | E-posta deliverability, bazı araçlarda punycode görünümü, sözlü iletişim | Canonical tek: `https://şamandıra.com`; tüm varyantlar 301; e-posta ASCII alias; sertifika punycode host için alınır (Let's Encrypt destekler) |
| 3 | **Marka çakışması** (Sancaktepe/Şamandıra semti + Fenerbahçe tesisleri) | Marka aramalarının karışması | Birleşik sorguları besle ("şamandıra gezi rehberi"), footer/meta'da "Şamandıra — gezi rehberi" kalıbı, TÜRKPATENT marka araştırması + başvuru (39/42/41) |
| 4 | **İçerik kalitesi:** 0 fotoğraf, 60 kayıtlık liste, cami/park gürültüsü, alfabetik sıralama | Kullanıcı güveni + Google "thin content" riski — SEO'nun 1 numaralı düşmanı | Kürasyon sprinti (doküman #02 ve #06): skor bazlı sıralama, alt-kategori filtreleri, "turistik değer" eşiği, fotoğraf kaynakları (Places API, belediye basın bültenleri, kendi çekimleriniz — Samsun'da yaşıyorsunuz, en büyük avantajınız) |
| 5 | **Tek makine bağımlılığı:** veri `veri/cikti/` git'te değil, DB yerelde, yayın dev tunnel'da | Veri kaybı = 6 aylık emek gider; yayın her an kopabilir | Oracle'a geçiş + `pg_dump` cron + yedeklerin ikinci kopyası (rclone → Oracle Object Storage / B2); JSONL ham verinin arşivlenmesi |
| 6 | **Dev modda yayın** | Performans, güvenlik başlıkları yok, HMR soketi dışarı açık | `next build && next start` + reverse proxy (doküman #05) |
| 7 | **Kapsam kayması** (mobil, auth, admin, harita hepsi birden) | Hiçbirinin bitmemesi | Bu dokümanın yol haritası sırasına sadakat; mobil **mezuniyetten sonra** |
| 8 | İki kişilik ekipte efor dağılması | Yavaşlama | Bölüm 7'deki rol paylaşımı + haftalık ritim + GitHub Projects |

---

## 6. Yol haritası — Eylül 2026 → Haziran 2027 (9 ay)

**Faz 0 — Masa temizliği (1-2 hafta)**
- Cursor araç/skill kurulumu (doküman #03), repo hijyeni (yanlış README'lerin düzeltilmesi), marka kararlarının netleşmesi (bu dokümanın soruları).
- Çıktı: ajan verimli çalışıyor, repo gerçeği anlatıyor.

**Faz 1 — Şamandıra rebrand + SEO temeli (2-6. haftalar)**
- Marka: isim, logo, favicon, OG şablonu, renk diline "şamandıra" motifinin işlenmesi (doküman #04).
- SEO: slug sistemi (DB migration 0005 + API + site), sayfa bazlı metadata, JSON-LD, sitemap/robots, canonical/OG, prod build (doküman #02).
- Çıktı: `şamandıra.com`'a kurulabilir, indexlenebilir site.

**Faz 2 — Canlıya alma (4-8. haftalar)**
- Oracle Ampere A1 (PAYG'de 4 OCPU/24GB ücretsiz kalıyor — Haziran 2026'daki limit değişikliği yalnızca Free Tier hesapları etkiledi; siz PAYG'ye yükselttiğiniz için doğru yapmışsınız): Docker (ARM64) + PostgreSQL/PostGIS + FastAPI + Next prod + Caddy/nginx + Let's Encrypt + yedekleme + Umami analitik (doküman #05).
- DNS: GoDaddy'den A kaydı → Oracle IP; GSC + Bing Webmaster doğrulama.
- Çıktı: `https://şamandıra.com` canlı, tünel bağımlılığı bitti.

**Faz 3 — İçerik kalitesi ve büyüme (6-16. haftalar)**
- Kürasyon: vitrin sıralama/eşikler, gürültü temizliği, fotoğraf kampanyası (yer başına en az 1 fotoğraf hedefi: Places API + kendi çekimleriniz).
- 17 ilçe sayfasının zenginleştirilmesi + ilk 10 editoryal rehber yazısı (doküman #02 içerik planı).
- Rota paylaşım sayfası + dinamik OG image (viral döngü).
- Çıktı: Google'da ilk 500-1.000 indeksli sayfa, ilk organik oturumlar.

**Faz 4 — İkinci şehir (3-5. ay)**
- Aday: **Trabzon** (turizm hacmi büyük, havalimanı, Uzungöl/Sümela) veya **Amasya/Ordu** (daha az rekabet, Karadeniz turu tamamlar). Öneri: Trabzon (talep) — ama karar veri toplama maliyetine göre.
- Amaç: "şehir bağımsız mimari" iddiasının **kanıtı** — akademik raporun en değerli bölümü bu olur. `sehir_ayarlari.py`'ye tek kayıtla şehir ekleniyorsa bu bir mimari başarı hikâyesidir; ölçün ve raporlayın (kaç satır kod değişti, kaç saat sürdü).

**Faz 5 — Büyüme sprinti (4-7. ay)** *(Karar 2026-09-05: monetizasyon mezuniyet sonrasına ertelendi)*
- İçerik: ayda 2-4 editoryal yazı, ilçe sayfalarının tamamlanması, fotoğraf kampanyası.
- Dağıtım: rota paylaşım OG kartları (viral döngü), Samsun odaklı Instagram/TikTok içeriği ("2 günlük Samsun rotası" dikey videoları), yerel Facebook grupları, üniversite toplulukları.
- Yan kulvar (düşük efor, yüksek getiri): TÜBİTAK 2209 / TEKNOFEST başvuruları, OMÜ Teknopark ön kuluçka görüşmesi.
- Sponsorluk/affiliate: yalnızca **hazırlık** (fiyat sayfası taslağı, `sponsorlu_mekan` rozet UI'ı, link altyapısı) — satış yok.

**Faz 6 — Portföy paketleme (6-9. ay)** *(Karar: bitirme projesi değil — kişisel/girişim projesi)*
- Hafif ölçüm: duygu spot-check (100 yorumda elle doğrulama), Lighthouse/CWV raporu, GSC büyüme ekran görüntüleri, rota motoru kırılım demosu.
- 3 dk demo videosu + case-study yazısı (LinkedIn / dev.to / Medium) + public repo + cilalı README (canlı site + video + mimari diyagram).
- İki GitHub profilinde repo pinleme + düzenli contribution; LinkedIn'de lansman postu.

**Faz 7 — Mobil (mezuniyet sonrası, 9-12. ay)**
- PWA → Capacitor sarmalayıcı (tek kod tabanı) + yerel yetenekler (harita/offline/konum/bildirim) → Google Play → Apple Developer ($99/yıl) → App Store (doküman #06).
- Not: MacBook Air M2 (16GB) Xcode + simulator için **yeterli**; 256GB SSD dar — harici disk/CloudKit yerine dikkatli temizlik gerekir.

---

## 7. Ekip ve iş bölümü (Alegre Group)

| Alan | Sorumlu | Not |
|---|---|---|
| Veri hattı, API, rota motoru, DevOps/deploy | **Bekir** | Flask/Python + sunucu deneyimi zaten var (bekiryilmaz.me) |
| Site UX/UI, SEO uygulama, içerik/editoryal, analitik | **Hiranur** | Çalışma: studytrack (Flutter) + sistem projesi; frontend'e kayması mantıklı |
| Marka, taksonomi, büyük kararlar | **Ortak** | Kararlar bu klasördeki dokümanlara yazılır (decision log) |
| B2B satış / işletme görüşmeleri | **Bekir** (+ Hiranur sunum materyali) | Freelance ağı avantaj |
| Hibe/yarışma başvuruları | **Hiranur** (dosya), Bekir (teknik bölüm) | 2209/TEKNOFEST takvimi takibi |

**Çalışma ritmi önerisi:**
- Haftada 1 planlama (30 dk, hangi Cursor görevleri) + 1 review (30 dk, PR/ekran incelemesi).
- GitHub Projects (ücretsiz) — kolonlar: Buzdolabı / Bu hafta / Cursor'da / İnceleme / Bitti.
- Branch disiplini: `main` korunur; her görev `feat/...` branch + PR; iki göz onayı (birbirinizin PR'ına).
- İletişim kanalı: tek Discord/WhatsApp başlığı + kararlar her zaman repoya (doküman olarak) yazılır.
- Kurumsal e-posta: `info@şamandıra.com` IDN riski nedeniyle **kullanmayın**; `alegregrouptr@gmail.com` gibi ASCII adres + ileride Workspace. (Not: briefte Bekir'in mailto linki yanlışlıkla Hiranur'un adresine bağlanmış — düzeltin.)

---

## 8. KPI panosu (haftalık takip, basit tutun)

| Metrik | Kaynak | 3 ay hedefi | 9 ay hedefi |
|---|---|---|---|
| İndeksli sayfa | GSC | 300 | 2.000+ (2 şehir) |
| Organik oturum/ay | GSC + Umami | 500 | 5.000-15.000 |
| Haftalık rota oluşturma | Umami event | 20 | 300 |
| Fotoğraflı yer oranı | kalite raporu | %40 | %90 |
| Vitrin gürültü oranı (turistik değeri düşük kayıt) | kalite raporu | %20 | <%5 |
| Lighthouse SEO/Perf | CI | 90/85 | 95/90 |
| Sponsor görüşmesi → ücretli | CRM (basit tablo) | 5 görüşme | 5-10 ücretli işletme |
| Hibe başvurusu | takvim | 1 (2209) | 2-3 + sonuç |

---

## 9. Portföy paketleme *(Karar 2026-09-05: bitirme projesi değil; iş görüşmeleri + girişim vitrini)*

**Bu projeyi iş görüşmesinde/investor sohbetinde güçlü yapan anlatı:**
1. **Uçtan uca sistem:** 6 katman (toplayıcı → eşleme → NLP → DB → algoritma → web) — "CRUD sitesi" değil, veri mühendisliği + algoritma + ürün.
2. **NLP:** Türkçe BERT ile duygu analizi + kural tabanlı, **izlenebilir** konu/profil çıkarımı (LLM kara kutusu yerine açıklanabilirlik — 2026'da akademik olarak savunulabilir ve etik açıdan güçlü bir tercih).
3. **Algoritma:** bearing tabanlı açısal kümeleme + slot bazlı günlük dizilim + TSP yedeği; deterministik ve kırılımı açıklanabilir skorlama. Baseline karşılaştırması yapılabilir (greedy vs kümeleme; uzman planı vs motor).
4. **Mimari disiplin:** şehir-bağımsız tasarım (ikinci şehir kanıtı), katman ayrımı, şema/model ayrımı, migration disiplini, taksonomi-önce geliştirme kültürü.
5. **Ürünleşme:** canlı domain, gerçek kullanıcı ölçümü, monetizasyon deneyi — mühendislik fakültesi projelerinde nadir.

**Vitrin için üretilecekler (Faz 6):** demo videosu, mimari diyagram seti, case-study yazısı (problem → mimari → sonuçlar; GSC/Lighthouse metrikleriyle), README'de canlı site + ekran görüntüleri + "neden böyle tasarlandı" notları. Ağır akademik ölçüm (F1, kullanıcı çalışması) gerekmiyor — ama ileride 2209/BiGG başvurusu yaparsanız bu bölümü geri açarız.

**Açık kaynak stratejisi önerisi:** kod **public** (MIT/Apache-2.0) → GitHub profili mezuniyette vitrin olacak (iki profilin de şu an zayıf olduğunu not edelim: bu proje ikisinin de pinned repo'su olmalı); **veri private** (JSONL + DB dump lisans/ToS nedeniyle dağıtılamaz). Repo'ya `docs/` altında bu strateji dokümanları + `README`'de canlı site bağlantısı + demo videosu.

---

## 10. Karar defteri (2026-09-05 — kullanıcı onaylı)

| # | Konu | Karar | Sonuç |
|---|---|---|---|
| K1 | Gelir önceliği | **Önce büyüme**: 9 ay trafik + ürün kalitesi + portföy; monetizasyon mezuniyet sonrası | Faz 5 "büyüme sprinti" oldu; sponsor/affiliate altyapısı hazırlanır, satılmaz |
| K2 | Veri kaynağı duruşu | **Kaynaklar sitede ifşa edilmez.** Ham veri ve kullanıcı bilgileri olduğu gibi yayınlanmaz; yalnız duygu analizi türevleri (özet/skor/profil) görünür | Aşağıdaki **kırmızı çizgiler** geçerli |
| K3 | Rebrand derinliği | **Yüzey + repo/dokümanlar**: site metinleri, logo, favicon, OG, API başlığı, README'ler, dokümanlar Şamandıra; GitHub repo adı `samandira`; kod tanımlayıcıları değişmez | T-02/T-03 talimatları + manuel repo yeniden adlandırma |
| K4 | Akademik çerçeve | **Portföy/girişim** — bitirme projesi değil | Faz 6 hafif ölçüm + demo video + public repo |

**K2 kırmızı çizgileri (kararın güvenli uygulanması):**
1. Ham yorum metni, yorumcu adı/takma adı **hiçbir sayfada** yayınlanmaz; yalnız şablondan üretilmiş duygu özeti + kısa, kaynağa atıfsız `ornek_ifade` parçacıkları (anonim, ≤10 kelime) gösterilir.
2. **OSM atfı kalır** (`© OpenStreetMap contributors`) — bu ODbL lisansının yasal zorunluluğu, "gizleme" kararı bunu kapsamaz; footer'a tek satır yeter.
3. Scraping ile toplanmış **fotoğraflar sitede kullanılmaz** (telif riski en yüksek materyal); fotoğraf kaynakları: kendi çekimleriniz, Places API, izinli belediye materyali, Wikimedia (lisanslı).
4. Toplayıcılar **yalnız geliştirme makinesinde** çalışır; canlı sunucuya `veri/` scraping hattı kurulmaz (sunucuda sadece DB + API + site yaşar).
5. ⚠️ **Repo public olursa yöntem görünür** (`google_maps_toplayici.py` vb. dosya adları bile yeter). Çözüm: public repo `samandira` = `sunucu/ + site/ + ortak/ + dokumanlar/`; **`veri/` ayrı PRIVATE repo** (`samandira-veri`) olarak taşınır. Faz 6'daki public açılışta bu ayrım yapılır.
6. Yasal asgari sayfalar yine eklenir: `/gizlilik` (KVKK aydınlatma), `/kullanim-kosullari`, `/iletisim`, `/hakkimizda` — bunlar kaynak ifşası gerektirmez.
