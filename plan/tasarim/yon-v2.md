# Şamandıra — Görsel Yön v2 (P4-REV)

> **Not (2026-09-08):** Hero **hareket kaynağı** için `yon-v3.md` bu dosyanın üzerine okunur — çelişkide hero hareketi söz konusu olduğunda **yon-v3 kazanır**. Bu dosyanın kanvas sözleşmesi (§2.3) video bağlanana kadar uygulanır; video gelince kanvas kapanır, scrub `video.currentTime`'a geçer. §2.2'deki mp4/webm yasağı **yalnız hero plakası için** yon-v3 ile kalkar; diğer tüm yüzeylerde mp4/gif karusel ve otomatik fotoğraf geçişi hâlâ yasaktır. Palet, split, trikler, kart sözleşmesi, anti-slayt kuralları değişmez.

**Tarih:** 2026-09-06 · **Oturum:** tek tur (doküman + uygulama + kanıt).
**Karar:** P4 hero'su slayt gösterisi gibi bulundu ve **reddedildi**. Hazır şablon avı kapandı; kimlik özgün kalır.
**Dayanak:** K5 (çıta "oha") · K8 (logo final, ağır tema yasak) · K10 (yon yeterliyse Opus'a dönülmez) · kullanıcı kararı 2026-09-06.
**Bu dosya `yon.md`'nin üzerine okunur.** Çelişkide **bu dosya kazanır** — özellikle `yon.md` §2 (fotoğraf sekansı / K9 mekanizması). Palet, tipografi, asimetrik split, 11 ufak trik, fotoğrafsız kart sözleşmesi **korunur**.

K9'un *niyeti* (LCP ≤ 2,5 sn, reduced-motion statik, bölge-nötr ufuk) durur; **video yasağı 2026-09-08'de kalkmıştır** — güncel niyet `yon-v3.md` (kaydırma-scrub, pin yok). K9'un *mekanizması* (flipbook / plaka kurgusu / otomatik fotoğraf geçişi) **iptaldir** ve iptal durur.

---

## 1. Teşhis — slayt hissinin kök nedenleri

P4 Yol B, `yon.md` §2.4'ün kendi uyarısını gerçekleştirdi: *"Farklı fotoğraflar flipbook yapmaz — dürüst adı sinema kurgusu; tutmazsa slayt gösterisi gibi durur."* Tutmadı. Kök nedenler:

1. **Çapraz geçiş plaka sekansı.** 9 ayrı Unsplash sahnesi (şafak ufku, sisli plaj, kayalık, kıyı) 320 ms erime + 1,1 sn duruşla birbirinin üstüne biniyor. Göz "aynı kameranın akışı" değil, **"sonraki slayt"** okuyor. Ara kare üretilmediği için geçiş bir film karesi değil bir sunum kesmesidir.
2. **Sahne süreksizliği.** Ufuk yüksekliği ±%8 kuralı kâğıtta vardı, karelerde tutulmadı: sis/kaya/kum ufuk çizgisi zıplıyor. Flipbook ancak *aynı sahnenin* zaman diliminde çalışır; P4 farklı mekânları aynı kutuya koydu.
3. **Ken Burns itişi slayt grameridir.** Ölçek 1,000→1,055 + yatay kayma %4,5 her plakada "bu kare bitti, yenisi geliyor" der. Bu, PowerPoint / Apple Keynote'un varsayılan fotoğraf geçişidir; atlas/defter değil.
4. **Faz A zaman tetikli otomatik ilerleme.** Sayfa yükünde 18 kare / 1,5 sn kullanıcıdan bağımsız akar. WCAG 2.2.2 eşiğinin altında olsa da *algı* otomatik karuseldir. Kullanıcı "ben kaydırmadım, o değişti" der.
5. **Faz B scrub'ı da fotoğraf indeksi.** Kaydırma bir dalgayı veya ışığı değil, *hangi stok fotoğrafın* gösterileceğini seçiyor. Scrub, slayt kumandasına bağlanınca hareket hâlâ fotoğraftan gelir.
6. **En yakın yüklü kare fallback.** İkili altbölme yüklemede boşluk görünmesin diye atlanan kareler "en yakın yüklü"ye zıplıyor — bu da kesmeli, basamaklı bir slayt titremesi.
7. **Bütçe görünürlüğü.** 66/36 kare, 830+330 KB, LCP'den sonra onlarca AVIF isteği. Ağ sekmesi bile "galeri yükleniyor" der. Hareket prosedürel olsaydı istek 0–1 kapak olurdu.
8. **Sayfa ritmi slaytı çoğaltıyor.** Kağıt zemin %60 monoton + her kartta aynı bordo başlık + kategori plakalarının da "başka bir fotoğraf" olması, hero'daki kesmeleri aşağıya taşıyor. Palet değişmedi; **ritim** (doku, koyu bant, mürekkep dozu) yeterince konuşmadı — "renkler basit" vetosunun asıl kaynağı budur, hex'ler değil.

**Sonuç:** Sorun Unsplash kalitesi veya asimetrik split değil. Sorun **hareketin fotoğraf dizisinden üretilmesi**. Çözüm hazır şablon (karusel, Ken Burns, full-bleed video, aurora mesh) değil; hareketi prosedüre almak.

---

## 2. Yeni hero sözleşmesi

### 2.1 Kompozisyon (korunur)

Asimetrik split aynı: 1280'de metin sol **5/12**, plaka sağ **7/12** ve sağ kenara taşar; 375'te plaka üstte (4:5), metin altta. **Metin hiçbir zaman fotoğrafın üstünde değil.**

Metin sırası değişmez: etiket → h1 (slogan) → GEO tanım cümlesi → çift CTA → mikro kanıt.

### 2.2 Yasak — otomatik fotoğraf geçişi her yerde

Aşağıdakiler **ana sayfa, keşif, yer, bölgeler, rota, tasarım sistemi** dâhil her yüzeyde yasaktır:

- Çapraz geçiş, dissolve, fade-between-images, flipbook, kare sekansı
- Zamanla veya kaydırmayla *fotoğraf indeksini* ilerletmek
- Karusel / slider / marquee (zaten `yon.md` §4.4 RED)
- Ken Burns (otomatik ölçek/pan) — hover nefesi hariç (§2.4)
- mp4 / webm / gif hero (K9 niyeti durur)
- `HeroSekans`, `HeroSekansGecikmeli`, `k-NNN.avif/webp` üretim hattı

Fotoğraf varsa **tek kare** durur. Değişmez.

### 2.3 Hareket kaynağı: prosedür

Hareket **fotoğraftan değil prosedürden** gelir. İki sürücü, tek rAF:

| Sürücü | Ne yapar | Ne yapmaz |
|---|---|---|
| **Zaman** | Dalga fazı, ışık süpürme konumu, şamandıra nabzı | Fotoğraf değiştirmez |
| **Scroll-scrub** | Ufuk kayması (≤ %4 plaka boyu), dalga genliği, rota düğümü görünürlüğü | Kaydırmayı pinlemez, jack yok |

Plaka katmanları (sabit sayı — **5 kanvas + 1 CSS grain = 6**):

| # | Katman | Tür | Davranış |
|---|---|---|---|
| 0 | Statik kapak fotoğrafı | `next/image` (tek kare) | Hiçbir zaman değişmez. Duotone mürekkep tint. |
| 1 | Gök yıkaması | kanvas gradyan | Scrub ile çok yavaş koyulaşır |
| 2 | Uzak dalga | kanvas dolgu | Yavaş faz, düşük genlik, paralaks |
| 3 | Orta dalga | kanvas dolgu | Orta faz |
| 4 | Yakın dalga | kanvas dolgu | Daha hızlı faz; hâlâ mesafe küçük |
| 5 | Ufuk + kızıl şamandıra ışığı + rota düğümleri | kanvas çizgi/nokta | Hairline ufuk; ufukta `samandira`/`signal` nabız (yalnız bu nokta); 5 düğümlü deniz-rengi hat |
| 6 | Grain | CSS overlay | Statik SVG gürültü, animasyon yok |

Dalga **logo dilidir**: mürekkep dolgusu + hairline, süs deniz bandı değil. Ağır tema yasağı (çıpa, dümen, halat, sonar, süzülen şamandıra figürü) durur. Şamandıra **yalnız ufuktaki kızıl ışık noktası** olarak vardır — logodaki fenerin plaka karşılığı; adı sayfada geçmez.

### 2.4 Sağ plaka fotoğraf kuralı

Kapak karesi **kalır** (künye: `gorsel-kunye.md` sıra 1 / `plaka-09` türevli kapak). Tek kare, AVIF+WebP.

- Hover / focus-within: **nefes** — `scale(1 → ≤ 1,03)`, süre ≥ 2,4 sn, `--ease-cikis`. Yalnız kullanıcı tetikler.
- Otomatik Ken Burns yok.
- `prefers-reduced-motion`: nefes yok, ölçek 1.

### 2.5 Sayılar (bütçe kilidi)

| Kalem | Değer |
|---|---|
| Kanvas katmanı | **5** (gök, 3 dalga, ufuk+ışık+düğüm) |
| CSS katmanı | **1** grain |
| rAF | **1** döngü. Bütçe **≤ 8 ms** / kare (hedef). `dt` tavanı 48 ms. |
| DPR tavanı | 2. Kanvas gösterim kutusuna eşitlenir. |
| Dalga genliği | Ekranda **≤ 16 px** (yakın katman); uzak ≤ 8 px |
| Ufuk scrub kayması | Plaka boyunun **≤ %4** |
| Işık süpürme turu | ≈ 8 sn, opaklık ≤ %8 |
| Şamandıra nabzı | 1,8 sn sinüs; yarıçap ≤ plaka boyunun %8'i |
| **Toplam ek KB** | **≤ 150 KB** (kanvas JS gzip + grain SVG data-URI). Kapak karesi LCP'dir, ek sayılmaz. Kare sekansı **0 KB**. |
| Hedef ek JS | ≤ 12 KB gzip (sert tavan 150) |
| Kaydırma payı (scrub) | masaüstü 900 px / mobil 520 px — pin yok |

### 2.6 Fallback

| Koşul | Davranış |
|---|---|
| `prefers-reduced-motion: reduce` | **Tamamen statik kapak.** Kanvas rAF başlamaz, grain animasyonu yok, nefes yok. **0 ek istek** (kare yok, kanvas varlık indirmez). |
| JS yok / hata | Statik kapak, hero tam işlevli |
| `saveData` / 2g/3g | Kanvas çalışmaz, statik kapak (isteğe bağlı; reduced-motion ile aynı görünüm) |
| Hero ekran dışı / sekme gizli | rAF iptal, `will-change` yok |
| Hidrasyon | Tercih **render dallanmasında okunmaz**; effect içinde bağlanır |

Kanvas `aria-hidden`. Kapak `alt=""`. Tek `h1` metindedir. Otomatik dönen *içerik* yoktur (fotoğraf değişmez) → duraklat düğmesi gerekmez. Dalga/ışık dekoratiftir.

### 2.7 Performans hedefi

- LCP elemanı kapak karesi veya h1. **Kare decode yok.** Gözlenen LCP **≤ 2,5 sn**.
- CLS **0**.
- Lighthouse mobil Perf **≥ 80**.
- Uzun görev yok: tek `clearRect` + 5 katman path. `setState` animasyon döngüsünde **yasak** (DOM'a değil kanvasa yaz).

---

## 3. Anti-slayt işçilik — 5 kural

Sayfanın geri kalanı hero'daki kesme gramerini tekrarlamasın diye. Palet **aynı**, işçilik değişir.

1. **Fotoğraflar statik + duotone mürekkep tint.** Hero kapağı ve kategori plakaları (`kesif` / `bolge` / `rota`) tek kare durur. Üzerlerinde bordo+kağıt duotone (CSS filter + multiply overlay). İçerik/yer fotoğrafı geldiğinde duotone **yok** (`yon.md` §1.5 — yerin gerçek rengi).
2. **Geçişler kesikli ayraç / su hattı ile.** Bölümler dissolve veya paralaks perdesiyle değil; `KesilenAyrac` (ortası boş hairline) ve kartın `su-hatti` (1 px `samandira`) ile ayrılır. "Yeni sahne" yok, "sayfa kıvrımı" var.
3. **Kart hover'da gölge yok, su hattı.** `box-shadow` kartta yasak kalır. Hover = hairline `bordo` %12→%40 + alt su hattı + başlık altı çizgisi, 180 ms `--ease-giris`. Yükselme yok.
4. **Bölüm ritmi ışık / koyu mürekkep bandı dönüşümlü.** Ana sayfa 6 bölüm: (1) kapak kağıt → (2) kanıt **koyu mürekkep** → (3) üç yol kağıt → (4) şehir vitrini **koyu mürekkep** → (5) duygu kağıt → (6) doruk **bordo**. İki kağıt bandı yan yana gelmez. Koyu bant oranı hedef: görünür yüzeyin **%35–45**'i (önceki P4'te ~%20, "basit" hissin nedeni).
5. **Hareket eğrileri tek aileden.** Yalnız `--ease-cikis` (giriş/ortaya çıkış) ve `--ease-giris` (durum/kapanış). Reveal 550 ms / 18 px, sayaç 900 ms, hover 180 ms. Yeni cubic-bezier eklenmez. Hero kanvası da aynı hissi taşır (ease-out faz, lineer scrub).

---

## 4. Palet ritmi — "renkler basit" vetosu

**Paleti değiştirme. Ritmi değiştir.** Token tablosu `yon.md` §1.2 kilitli: `bordo #6C0000`, `kagit #F4EFE7`, `samandira #D6402C`, `ink`, `deniz` aynı.

| Ritim vidası | P4 (reddedilen) | v2 |
|---|---|---|
| Kağıt dokusu | %3,5 opaklık, gövdede kayboluyor | **%5–5,5** kağıtta, **%8** koyu bantta. Doku *görünür* — sıcak kâğıt okunur. `background-attachment: fixed` hâlâ yok. |
| Koyu bant oranı | Kanıt + doruk (~2/6, zayıf) | Kanıt + **şehir vitrini** + doruk = 3/6. Vitrin kartı koyu bandın üstünde **tuz adası** olarak kalır (kart yeniden tasarlanmaz). |
| Bordo mürekkep başlık dozu | Her h2/h3 bordo → tek notalı | Kağıt bantta h2 **bordo**, kart h3 **ink** (soru hiyerarşisi boyutla kurulur). Koyu bantta h2 **kagit** — bordo orada *zemin*dir, mürekkep değil. Hero h1 kâğıtta bordo kalır (dozun harcandığı yer). |
| `samandira` %10 | CTA + su hattı + nabız | Aynı + **yalnız** ufuktaki şamandıra ışığı. Yeni kırmızı yüzey yok. |

60-30-10 korunur: %60 kağıt/tuz · %25 bordo ailesi (artık gerçekten koyu bantlarda görünür) · %10 samandira · %5 deniz (rota hattı).

---

## 5. P4-REV iş listesi (FAZ 2)

Kod bu maddelerin dışına taşmaz.

1. **`yon-v2.md` kilit** — bu dosya. `00_brief_eki.md` K9'a "mekanizma iptal, niyet durur" notu.
2. **Sekans kodunu sil.** `HeroSekans.tsx`, `HeroSekansGecikmeli.tsx`, `hero-sekans.ts` kare tablosu, `hero_kare_uretim.mjs` üretim hattı. Kalıntı isim (`Sekans`, `k-002`, `fazA`, `fazB` kare indeksi) kalmaz.
3. **Kare assetlerini sil.** `site/public/hero/masaustu/k-*`, `site/public/hero/mobil/k-*`. **Kapak kalır:** `kapak-masaustu.avif/webp`, `kapak-mobil.avif/webp`.
4. **`HeroUfuk` kur.** Tek client kanvas; rAF'ta `setState` yok; ref yalnız effect/olayda; reduced-motion erken çıkış. `HeroKapak` RSC kalır, kapağı `getImageProps` + `<picture>` (next/image) ile sunar.
5. **Hover nefesi** CSS: plaka `:hover/:focus-within` scale ≤ 1,03; reduced-motion'da 0.
6. **Ana sayfa 6 bölüm** kural 3–5: koyu vitrin bandı, kart h3 ink, doku opaklığı, kesikli ayraçlar, istatistik sayaçları (mevcut DOM yazımı — 60 setState yok).
7. **Kategori plakaları** statik + duotone sınıfı; `Plaka` ham `<img>` değil `next/image` / `getImageProps`.
8. **Sunucu tekilleştir.** 3001 kalıntısı kapatılır; güncel sürüm **3000** (devtunnel 3000'i dinliyor).
9. **Lint anayasası:** `next/link`; render'da `ref.current` yok; effect'te senkron `setState` yok; JSX `escape`; görseller `next/image`.
10. **FAZ 3 kanıt:** Playwright 375+1280 üst/orta/alt + hero t0/t1/t2 (1,5 sn); Chrome DevTools izi (en ağır 3 kalem); Lighthouse mobil Perf ≥ 80, CLS 0, LCP gözlenen ≤ 2,5 sn; reduced-motion statik kapak + 0 ek hero isteği.

**Yapılmaz:** yeni palet tokenı, üçüncü font, şablon hero, video, otomatik fotoğraf, git commit.

---

## 6. `yon.md` geçersiz kılma tablosu

| Geçersiz | Yerine |
|---|---|
| §2 tamamı (flipbook Faz A/B, 66/36 kare, Yol A/B üretim) | bu dosya §2 |
| §0 madde 4–5 (sekans mekanizması, Unsplash plaka kurgusu) | tek statik kapak + prosedürel ufuk |
| §4.2 ana sayfa "(1) Kapak — sekans Faz A → Faz B" | kapak statik; ufuk zaman+scrub |
| §8 kapı 2 (sekans bayt ≤ 900/380 KB) | ek ≤ 150 KB; kare 0 |
| P4 paket tanımı (`yon.md` § uygulama paketleri) | **P4-REV** (bu dosya §5) |

Korunan: §1 palet/tipografi/boşluk/köşe, §3 bileşen davranışı, §4.1 tokenlar, §4.4 marquee RED + pin yasağı, §5 on bir trik, §6 yerleşim eşikleri.
