# T-16 Faz 1 — Keşif ve Araştırma Dosyası (tarihçe)

**Tarih:** 2026-09-05 · **Görev (o gün):** T-16 Faz 1 keşif · **Durum:** tarihçe.

> **K8 bu dosyayı geçersiz kılar (logo).** Kullanıcı illüstrasyonu `plan/logo/secili/logo.png` FİNAL'dir; §6–§7'deki Ufuk / Sonar / Rota / Demir seçimi uygulanmaz. **Slogan + GEO tanım cümlesi (§5 / §7) geçerlidir.** Güncel karar: `plan/00_brief_eki.md` §3. Güncel yön: `plan/tasarim/yon.md`. Sergi `/tasarim-secim` kapatıldı.

Bu dosya T-16 Faz 1'in araştırma çıktısıdır: kaynak havuzu taraması, çıkarılan desenler, `ui-ux-pro-max` notları, reddedilen logo gerekçeleri ve SEO+GEO slogan stratejisi. Ekran görüntüleri `plan/logo/arastirma/` klasöründedir.

**Bağlam / kısıt (o gün):** K5, K6, K7. Palet o sırada `deniz/kopuk/kumsal/gunes` + `samandira #D6402C` idi; **güncel palet `yon.md` §1.2** (bordo mürekkep). Fontlar Fraunces + Sora kilit kaldı.

---

## 1. Kaynak havuzu (10/11 kaynak tarandı)

| # | Kaynak | URL | Ne için bakıldı | Ekran görüntüsü |
|---|---|---|---|---|
| 1 | Design Prompts | https://designprompts.dev/ | Stil taksonomisi: aynı veri 31 farklı estetikle | `designprompts.png`, `ref-designprompts-stil*.png` |
| 2 | Awwwards — Travel | https://www.awwwards.com/websites/travel/ | Ödüllü seyahat sitelerinde kart/rozet anatomisi | `awwwards-travel.png` |
| 3 | Lapa Ninja | https://www.lapa.ninja/ | 7.300+ landing; bölüm sıralaması | `lapa-ninja.png` |
| 4 | Lapa Ninja — Motion | https://www.lapa.ninja/motion/ | Hareketin ayrı bir tür olarak kürasyonu | `ref-lapa-motion*.png` |
| 5 | 21st.dev | https://21st.dev/ | Hero/arka plan bileşen dili, display tipografi ölçüsü | `21st-dev.png`, `ref-21st-hero*.png` |
| 6 | animations.dev | https://animations.dev/ | Soru-önderli hero, bölüm (chapter) isimlendirmesi | `animations-dev.png` |
| 7 | Godly | https://godly.website/ | Yoğun kürasyon arayüzü, etiket filtreleri | `godly-website.png`, `ref-godly-branding*.png` |
| 8 | Typewolf | https://www.typewolf.com/site-of-the-day · /lookbooks | Editoryal tipografi, sıcak kırık-beyaz zemin | `typewolf.png`, `ref-typewolf-lookbook*.png` |
| 9 | Behance | https://www.behance.net/search/projects/travel%20brand%20identity | Seyahat marka kimliği işleri (10.000+ sonuç) | `behance-travel.png` |
| 10 | Figma Community | https://www.figma.com/community/tag/travel/files | Seyahat şablonlarının klişe kalıpları (ne YAPMAMALI) | `figma-community.png` |
| 11 | Mobbin | https://mobbin.com/browse/web/apps | İstatistik bandı ve akış (flow) kürasyonu | `mobbin.png` |
| — | Land-book | https://land-book.com/ | **Erişilemedi** (Cloudflare bot doğrulaması) | `land-book.png` |

Ek referans (Awwwards listesinden isim tespiti, ilham için not edildi): Niarra Travel (Superhero Cheesecake), Hedwig: Curated Travel (catarisso), "How to Time Travel" (Platform81, SOTD), Ota City Official Travel Guide, GetYourGuide Trend Tracker.

---

## 2. Çıkarılan desenler (16 madde)

Ölçülen değerler `getComputedStyle` ile canlı sayfalardan alınmıştır — tahmin değildir.

### Tipografi ölçeği

1. **Display tipografi negatif harf aralığı ister.** Ölçüm: 21st.dev h1 = 64px / ağırlık 500 / satır 67.84px (1.06) / harf aralığı −1.408px (**−0.022em**). designprompts.dev h1 = 28px / harf aralığı −0.56px (**−0.02em**). Kural: 40px üstü her başlıkta `letter-spacing: -0.02em`, satır yüksekliği 1.0–1.1. Bizde Fraunces zaten yüksek kontrastlı; sıkı tracking olmadan hero'da dağınık duruyor.
2. **Editoryal hiyerarşi ağırlıkla değil, boyut ve stille kurulur.** Typewolf lookbook h1 = 58px serif 700 / satır 1.2; gövde aynı serif ailesinden 16px. Ağırlık zıplaması yok, **boyut zıplaması** var (58 → 16 = 3.6×). Bizde Fraunces display / Sora gövde ayrımı bu işi zaten yapıyor; ölçek sıçraması yeterince agresif değil.
3. **Kürasyon/indeks arayüzleri küçük taban puntoyla yoğunlaşır.** Godly gövde = **13px** Inter. Pazarlama sayfası büyük, liste sayfası küçük ve yoğun. Şamandıra'da aynı ayrım: ana sayfa hero büyük (Fraunces 56–72px), keşif listesi sıkı (Sora 13–14px etiket, 15–16px gövde).
4. **Etiket/tarih/rozet için ayrı bir tipografik kat gerekir.** `ui-ux-pro-max` "Minimalist Monochrome Editorial" kaydı: mono 400–500, `uppercase`, `tracking-widest`. Mevcut sergide bu kat zaten kullanılmış (`text-[10px] tracking-[0.24em] uppercase`) ve işliyor — sistemleştirilmeli.

### Renk kullanımı

5. **Saf beyaz zemin editoryal işlerde kullanılmıyor.** Typewolf zemini `rgb(230, 221, 222)` = **#E6DDDE** (sıcak kırık-beyaz). Şamandıra'nın `--sis: #f3f7f6` zemini soğuk tarafta; kumsal tonuna hafif kayan bir kağıt zemin (ör. `#F4EFE7`) hem sıcaklık hem ayrışma verir.
6. **Vurgu rengi %10'u geçmiyor.** Ödüllü seyahat sitelerinde baskın renk fotoğraf/zemin; marka kırmızısı yalnız CTA ve işarette. `plan/04` §3'teki 60-30-10 kuralı sahada doğrulandı — `samandira #D6402C` metin rengi olarak asla kullanılmayacak.
7. **Bölüm bazlı renk ilerlemesi anlatıyı taşıyor.** `ui-ux-pro-max` "Scroll-Triggered Storytelling": *"Progressive reveal. Each chapter has distinct color. Building intensity."* Bizim karşılığı: gün döngüsü (şafak kumsalı → gündüz denizi → alacakaranlık → derin gece) — mevcut `Gun` sahnesi bunu zaten deniyor.

### Hero kurgusu

8. **Hero tek cümle, ≤8 kelime, iddia veya soru.** animations.dev: *"How do you craft animations that feel right?"* — soru-önderli. 21st.dev: *"The living library of interfaces"* — iddia-önderli. İkisi de alt satırda tek açıklama cümlesi + tek birincil CTA. Şamandıra hero'su şu an bunu yapmıyor; slogan + tanım cümlesi ayrımı gerekiyor (bkz. §5 GEO).
9. **Hero'da hareket dekoratif katmanda, metin sabit.** `ui-ux-pro-max` gsap "Parallax Scroll / Subtle": *"Apply parallax to background/decorative layers only, never to text or interactive controls"*, `yPercent` deltası 5–15 arası. Metni paralaks yapmak okuma konforunu bozuyor.
10. **İstatistik bandı sosyal kanıt yerine geçiyor.** Mobbin: *"1,428 apps / 621,500+ screens / 323,900 flows"*. Lapa: *"7,300+ landing pages / 15,000+ screenshots"*. Şamandıra'nın elinde gerçek sayı var: **1.719 yer kaydı** (`00_brief_eki.md` §4), ilçe sayısı, deneyim ekseni sayısı. Yorum sayısı **verilmeyecek** (K2 kaynak ifşası kırmızı çizgisi).

### Kaydırma koreografisi

11. **Anlatı bölümlere ayrılıp isimlendiriliyor.** animations.dev ders bölümleri: *The Odyssey, Angry Rabbits, Ghost town, Pirates in the jungle, Lost in the mountains*. İsimlendirme, bölümü hatırlanabilir yapıyor. Şamandıra bölümleri denizcilik metaforundan alınacak: *ufuk, sığlık, rota, demir*.
12. **Bölüm sonu mini CTA + finalde doruk CTA.** `ui-ux-pro-max` pattern: *"End of each chapter (mini) + Final climax CTA"*. Tek CTA'yı sayfa sonuna bırakmak dönüşüm kaybı.
13. **Hareket, indirgenmiş harekette tamamen kapanır ve içerik son okunabilir halinde kalır.** Hem `ui-ux-pro-max` (*"render each chapter in its final readable state under reduced motion"*) hem Motion dokümanı bunu şart koşuyor. Ek kural: *"Pause scroll animation when offscreen or hidden."*
14. **Hareket başlı başına bir tür olarak kürate ediliyor.** Lapa'nın ayrı `/motion/` bölümü var ("Websites in Motion", h1 48px/700). Yani hareket dili, statik tasarım kadar marka varlığıdır — Faz 2'de `hareket.css` + Motion tokenları sistemleştirilecek.

### Kart anatomisi ve CTA dili

15. **Kart = görsel-önce + üretici satırı + durum rozeti.** Awwwards kartları: site görseli, altında stüdyo adı (Phenomenon Studio, catarisso, Lime Creative), köşede `HM`/`SOTD` rozeti. Şamandıra yer kartı karşılığı: fotoğraf + yer adı + ilçe + **skor rozeti** (`Şehrin Klasiği` / `Sponsorlu` — `plan/04` §7). Rozet her görünümde zorunlu.
16. **Galeri gezinmesi filtre çipleriyle yapılıyor, menüyle değil.** designprompts: `MODE: All / Light / Dark` + `TYPE: All / Sans / Serif / Mono`. Godly: `All / Web / Interface / Branding / Product / Typography / Motion`. Şamandıra keşif sayfasındaki kategori çipleri doğru yolda; eksik olan **aktif durum görselliği** ve sayı göstergesi.

### Benzemezlik kuralı (uygulanan filtre)

Figma Community "travel" şablonları ve Behance seyahat kimlikleri taranırken tekrar eden klişeler **yasak listesine** alındı: jenerik damla harita pini, uçak/valiz ikonografisi, pasaport damgası dokusu, turkuaz-turuncu gradyan, polaroid çerçeve, el yazısı script font, "Explore the world" tipi bölge-nötr olmayan İngilizce klişe. İlham **desen düzeyinde** alındı (ölçek, ritim, katman, zamanlama); hiçbir görsel/kod kopyalanmadı — T-16 "Yapılmayacaklar" maddesi gereği.

---

## 3. Tasarım sistemi yönü (`ui-ux-pro-max` çıktısı + marka kilidi)

Komut: `search.py "travel discovery guide route planner cinematic editorial" --design-system --variance 7 --motion 7 --density 4 -p "Samandira"`

**Skill'in verdiği ham çıktı ve bizim kararımız:**

| Boyut | Skill önerisi | Şamandıra kararı | Gerekçe |
|---|---|---|---|
| Desen | Scroll-Triggered Storytelling | **Kabul** | Rota ürünü doğal olarak bir yolculuk anlatısı; bölümler denizcilik metaforuna oturuyor. |
| Stil | Aurora UI (parlak mesh gradyan) | **Kısmi red** | Mesh gradyan jenerik SaaS işareti. Yerine: **prosedürel deniz** — kod ile çizilen ufuk/dalga/ışık katmanları (mevcut `Gun`/`Firtina` sahneleri bu yönü doğruluyor). Gradyan yalnız atmosfer katmanında, marka rengiyle. |
| Palet | `#EA580C` turuncu + `#0891B2` teal | **Red** | Marka paleti `plan/04` §3 ile kilitli. Skill'in "adventure orange + map teal" notu bizim `samandira #D6402C` + `deniz #0A4D5C` ikilisiyle aynı psikolojik işi zaten yapıyor. |
| Tipografi | Playfair Display + Inter | **Red (eşdeğer korunuyor)** | Fraunces + Sora aynı editoryal serif+sans mantığı; Fraunces'ın değişken optik boyutu Playfair'den üstün ve latin-ext (ş, ı, ğ) tam. |
| Hareket kademesi | Standard (400–600ms, `power2.inOut`) | **Kabul, Motion'a çevrildi** | GSAP kurulu değil; `motion@13.2.0` kurulu. Eşleme: `power2.inOut` ≈ `ease: [0.4, 0, 0.2, 1]`. |
| Yoğunluk | Standard (16–64px boşluk) | **Kabul** | Pazarlama sayfası ferah, liste sayfası sıkı (madde 3). |

**Kilitlenen yön cümlesi:** *Editoryal denizcilik — sıcak kağıt zemin üzerinde yüksek kontrastlı Fraunces display, kod ile çizilen prosedürel deniz katmanları, %10 şamandıra kırmızısı vurgu, bölümlenmiş kaydırma anlatısı.*

**Anti-desenler (skill + kendi denetimimiz):** tutarsız stil, düşük kontrast, ikon yerine emoji, tıklanabilir öğede `cursor-pointer` eksikliği, metne uygulanan paralaks, `prefers-reduced-motion` yok sayımı, Lighthouse'u düşüren süsleme.

---

## 4. Hareket dili — teknik temel (Context7 / `motion.dev`)

Kaynak: Context7 `/websites/motion_dev` (1433 snippet, yüksek itibar). Faz 2'de kullanılacak doğrulanmış API'ler:

- **`whileInView` + `initial`** — bölüm açılış reveal'i. Kalıp: `initial={{ opacity: 0, y: 24 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }}`.
- **`useInView(ref, { once: true, amount, margin })`** — `once: true` tek seferlik tetikleme; `amount: "some" | "all" | 0–1` eşik; `margin` ile erken tetikleme.
- **`useScroll({ target, offset, axis })`** → `scrollYProgress` (0–1) + **`useTransform`** — paralaks ve kaydırmaya bağlı sahne ilerlemesi.
- **`useReducedMotion()`** — dokümandaki resmi kalıp, paralaksı sıfırlar:
  ```jsx
  const shouldReduceMotion = useReducedMotion()
  const y = useTransform(scrollY, [0, 1], [0, -0.2], { clamp: false })
  return <motion.div style={{ y: shouldReduceMotion ? 0 : y }} />
  ```

**Performans sözleşmesi (T-16 + `vercel-react-best-practices`):** animasyon yalnız `transform`/`opacity`; `will-change` yalnız aktif paralaks katmanında ve kaydırma durunca kaldırılır; ağır sahneler `next/dynamic` ile; SVG'ler sarmalayıcı `<div>` üzerinden animasyonlanır (donanım hızlandırma); uzun listelerde `content-visibility: auto`.

---

## 5. Slogan stratejisi — SEO + GEO (K7)

K7 gereği slogan bir "reklam cümlesi" değil, **iki ayrı işi** yapan bir çift:

1. **Slogan (marka katı):** ≤5 kelime, bölge kilidi yok, akılda kalıcı, header/OG/footer'da kullanılır.
2. **Tanım cümlesi (GEO katı):** yapay zekâ asistanının (ChatGPT/Perplexity/Gemini) **alıntılayacağı** kesin, öznesi belli, kategori kelimesi içeren cümle. Ana sayfa `<h1>` altında ve meta description'da birebir geçer.

GEO filtreleri: aranan kategori kelimesi (`gezi rehberi`, `rota planlayıcı`, `gezilecek yerler`) slogan veya tanım cümlesinde **birebir** geçmeli; tanım cümlesi bağlamdan bağımsız tek başına doğru olmalı ("önce cevap" ilkesi, `02_seo_mimarisi.md` §11); marka adı cümlenin öznesi olmalı ki alıntıda kaybolmasın.

Adaylar, gerekçeleri ve en iyi üçün kullanım örnekleri bu dosyanın §5'indedir (10 aday). `/tasarim-secim` sergisi kapatıldı.

---

## 6. Logo konsept yönü

Reddedilen ilk tur ("yavan/çocuk işi") ve `plan/04` §4'teki A/B/C konseptlerinin ortak zaafı: **şamandıranın resmini çizmek**. Ödüllü kimliklerde işaret, nesnenin illüstrasyonu değil, nesnenin **davranışının** soyutlaması oluyor.

Faz 1'de üretilen 4 konsept bu yüzden dört farklı soyutlama ekseninde kuruldu — hepsi 32×32 kılavuzda, tek çizgi kalınlığı ailesiyle (2.8 / 2.2 / 1.8) ve optik düzeltmeyle:

| Konsept | Soyutlama ekseni | Neden ayrışıyor |
|---|---|---|
| **Sonar** | Şamandıranın *sinyali* — dikey kapsül gövde + iki basık eşmerkezli halka | Harita pini değil, "işaret veriyor" fiili. Halkalar basık olduğu için suya açılı bakış okunur; bu hamle işareti wifi ikonundan ayırır. |
| **Ufuk** | Şamandıranın *ufuk çizgisini kesmesi* — halka + iki parçalı ufuk çizgisi + yansıma | Tek daire + tek yatay çizgi; favicon'da en dayanıklısı. |
| **Rota** | Şamandıranın *dizilimi* — üç düğüm arasında kesikli hat, tepe düğüm vurgulu | Ürünün asıl işini (gün gün rota) doğrudan anlatır. |
| **Demir** | Şamandıranın *zinciri* — 45°'lik ortak eksende iki bakla | "Demir atmak" = kaydedilen rota. Zincir baklası hiçbir seyahat klişesinde yok; en ayırt edici konsept. |

### 6.1 Yineleme kaydı — 5 tur

Her tur tarayıcıda gerçek boyutlarda render edilip (16/24/32/48px + silüet) incelendi; tespit edilen kusur bir sonraki turda düzeltildi. Kanıt: `logo-inceleme-tur1..5.png`, `logo-inceleme-son.png`.

| Konsept | Kapatılan kusurlar | **Kapanmayan sınır** |
|---|---|---|
| **Sonar** | T1: eşmerkezli yaylar birebir wifi ikonu → T2 basık elipse çevrildi. T2: gövde noktası lekeye dönüştü → T3 dikey kapsüle uzatıldı (5.6 → 9.4). | **Silüet.** Çizgiler 3.4'e çıkınca iki halka uçlarda birleşip dolu mercek oluyor; bu kurulumda geometrik olarak çözülemez (açıklık 1.8 < çizgi yarıçapları toplamı 3.4). T5'te elipsler ayrık yaya çevrildi, silüet düzeldi ama işaret birebir **"indir" (download) ikonuna** döndü — gövdeyi lozenge'e genişletmek de kurtarmadı. Klişe çarpışması leke kusurundan ağır kabul edilip T3 geometrisine geri dönüldü. |
| **Ufuk** | T1: su altı kesikli yay dairenin dibinde okunmayan leke yaptı → T2 tamamen kaldırıldı, halka kalınlaştırıldı, ufuk boşlukları halkanın gerçek silüetiyle hizalandı. T2: çizgiler güdük → T3 çerçeve kenarına uzatıldı. | **Yok** — dört testin (16px / tek renk / silüet / benzersizlik) dördünü de geçen tek konsept. |
| **Rota** | T1: yan düğümlerin kalın çizgisi donut etkisi yapıp vurgulu tepe düğümüyle yarıştı → T2 küçültüldü (2.5 → 2.2), inceltildi, kesik ritmi sıkıldı. | 16px'te kesikli hat kaybolur, üç nokta kalır. Silüette kesikler dolup tek kemere döner. |
| **Demir** | T1: iki dikey bakla tek sapa dönüştü, silüet anahtar/lolipop → T2 tek delikli bakla. T3: bakla dikeyden yataya çevrildi ama silüet hâlâ "anahtar deliği" tek lekesi — alt bakla üst halkadan **dar** kaldığı için silüeti genişletmiyor, altını dolduruyordu. T4: oran tersine çevrildi, leke dağıldı ama dikey eksende iki halka kaçınılmaz olarak **"8" rakamı / kardan adam** gibi okundu. T5: sorun eksende çözüldü — gerçek zincir dikey değil **diyagonal** dizilir; iki bakla 45°'lik ortak eksene yatırıldı, eksende 9 birim ayrıldı, uçta 3.6 birimlik gerçek geçişme kaldı. | En dar toleranslı konsept: çizgi kalınlığı değiştirilemez, iki delik 16px'te sınırda açık kalıyor. |

**Seçim için özet:** Ufuk teknik olarak en güvenli, Demir en ayırt edici, Rota ürünü en doğrudan anlatan, Sonar en "davranışsal" ama tek renk baskıda/kabartmada sınırlı.

Her konsept için mockup duvarı (header açık/koyu, uygulama ikonu, kartvizit, harita markırı, favicon 16/32/48px) ve tam renk / tek renk / silüet tonlama testi sergide görünürdür. Duvar ekran görüntüleri: `sergi-{1280,375}-duvar-{sonar,ufuk,rota,demir}.png`.

---

## 6.2 Sergi denetimi (`web-design-guidelines` skill'i) — düzeltilenler

Sergi kurulduktan sonra skill ile denetlendi; bulunan üç kusur düzeltildi ve Playwright ile doğrulandı:

| Bulgu | Düzeltme | Doğrulama |
|---|---|---|
| Koyu zeminli sayfada tarayıcı kaydırma çubuğu ve taşma alanı açık temada kalıyordu. | `hareket.css`'e `html:has([data-sergi]) { color-scheme: dark }` — düzeltme yalnız sergiye kapsamlandı, global tema bozulmadı. | `getComputedStyle(html).colorScheme === "dark"` |
| Sticky üst bant (~57px) çapa atlamalarında hedef bölümün başlığını kapatıyordu. | `[data-sergi] section[id] { scroll-margin-top: 4.5rem }` — dört çapanın tamamını tek kuralla kapsıyor. | Dört çapa tıklandı: bölüm üstü 72px'e oturuyor, başlık 152px'te — bandın altında kalan yok. |
| İşaret her mockup'ta `role="img"` + `aria-label` taşıdığı için ekran okuyucu konsept adını duvar başına ~15 kez okuyordu; yanındaki "şamandıra" kelime işareti zaten aynı bilgiyi veriyor. | Logo bileşenlerine `dekoratif` bayrağı eklendi; mockup bağlamlarında `aria-hidden="true"` uygulanıyor. | Sayfadaki 74 SVG'nin `role="img"` olan sayısı: 0. |
| Sayfada **iki `h1`** vardı: girişteki başlık ve arşivlenmiş hareket çalışmasındaki "Salon". | Arşiv bölümündeki başlık `h2`'ye indirildi. | `document.querySelectorAll('h1').length === 1` (her iki hareket modunda). Başlık sıralamasında atlama yok (71 başlık tarandı). |
| **Hidrasyon uyuşmazlığı** — arşiv bileşenleri `azalt ? sabit : motionDegeri` biçiminde dallanıyordu. `useReducedMotion()` sunucuda medya sorgusunu bilemeyip `null`, tercihi olan istemcide `true` döndüğü için sunucu ve istemcinin ilk render'ı farklı HTML üretiyor; React tüm ağacı yeniden kuruyordu. Yalnız azaltılmış-hareket kullanıcılarını etkiliyordu, bu yüzden ilk denetimde görünmedi. | Kök nedene tek noktadan müdahale: `kaydir.tsx` içinde hidrasyona güvenli `useAzalt()` hook'u — ilk render herkeste hareketli varyant, tercih effect içinde bağlanıyor. 7 doğrudan `useReducedMotion()` çağrısı bu hook'a çevrildi. Metin sayaçları için `KaydirYazi`'ya `duragan` parametresi eklendi (8 çağrı yeri). | `reducedMotion: reduce` **ve** normal modda ayrı ayrı yüklendi: her ikisinde 0 uyuşmazlık, 0 konsol hatası. Davranış korundu: azaltılmışta sayaçlar sabit son değeri (`07:41`, `2.8 m`, `f/8.0`, `120 / 120`), normalde başlangıç değerini gösteriyor. |

Kalan bilinen kusur (düzeltilmedi, kapsam dışı): arşiv bölümündeki 45 bağlantı 24px'lik dokunma hedefi eşiğinin altında. Bunların tamamı arşivlenmiş hareket çalışmasına ait; Faz 1 bölümlerinde (yön / logo / slogan / karar) eşik altı hedef yok.

---

## 7. SEÇİM — Faz 1 kapısı (kısmen superseded)

**Tarih:** 2026-09-05 · Sergi (`/tasarim-secim`, kapatıldı) üzerinden o gün onaylandı.

| Karar | O günkü seçim | 2026-09-05 sonrası |
|---|---|---|
| **Logo** | Ufuk (`plan/logo/arsiv/ufuk.svg`) | **GEÇERSİZ — K8:** `plan/logo/secili/logo.png` |
| **Slogan** | Aday 01 — "Gezilecek yerleri işaretler." | **Geçerli** (`00_brief_eki.md` §3.5) |
| **GEO tanım cümlesi** | Aday 01 tanımı | **Geçerli** (`04_marka_ve_tema.md` §1) |
| **Tasarım yönü** | Kâğıt zemin + ufuk→sığlık→rota→demir anlatısı | Yön **`yon.md`**: "Mürekkep ve Tuz"; bölüm adları kullanıcı sorusu; denizcilik anlatısı düşer |

Reddedilen üç konsept (Sonar / Rota / Demir) §6.1 ve `plan/logo/arsiv/` tarihçesidir.

### Üretim (K8, Ufuk değil)

Favicon / apple-touch / PWA / maskable / OG / şeffaf+açık karo: `plan/04_marka_ve_tema.md` §4, script `site/scripts/logo_uretim.mjs`. Çizgi/kompozisyon/renk değişmez.

---

## 8. Faz 2'ye taşınacak kararlar (seçim sonrası uygulanacak)

- Sıcak kağıt zemin tokenı (`#F4EFE7` civarı) `@theme`'e eklenir; mevcut `deniz/kopuk/kumsal/gunes` tokenlarına dokunulmaz.
- Tipografi ölçeği: display 40px+ için `letter-spacing: -0.02em`, `line-height: 1.0–1.1`; mono etiket katı (`uppercase`, `tracking-[0.24em]`, 10–11px).
- Bölümlenmiş kaydırma anlatısı: *ufuk → sığlık → rota → demir*, her bölüm sonunda mini CTA, sonda doruk CTA.
- İstatistik bandı: yer sayısı + ilçe sayısı + deneyim ekseni sayısı (yorum sayısı YOK — K2).
- Kart ailesi: görsel-önce + ilçe satırı + zorunlu rozet katı.
- Hareket: `whileInView` reveal + kademeli kart girişi + yalnız dekoratif katmanda paralaks (`yPercent` 5–15); `useReducedMotion` ile tam statik.
- Filtre çiplerine aktif durum + sayı göstergesi.
