# Şamandıra — Görsel Yön v3 (hero scroll-video)

**Tarih:** 2026-09-08 · **Karar:** kullanıcı, 2026-09-08.
**Bu dosya `yon.md` ve `yon-v2.md`'nin üzerine okunur.** Çelişkide **hero hareketi** için bu dosya kazanır. Palet, tipografi, asimetrik split, 11 ufak trik, fotoğrafsız kart sözleşmesi, anti-slayt işçilik kuralları `yon.md` + `yon-v2.md`'de **korunur**.

**Kapsam:** yalnız ana sayfa hero plakası. Harita bölümüne (G2) ve başka yüzeye dokunmaz.

---

## 1. Teşhis

### 1.1 Neden Apple pin kopyalanmaz

`yon.md` §4.4 RED listesi durur: scroll-jacking yasak, pin yasak, Lenis/GSAP ScrollTrigger pin yasak, sticky hero hapsetme yasak. Apple product-page hissi **pin'den değil scrub'dan** gelir: sayfa normal akar, kullanıcı kaydırdıkça video ilerler. Kaydırma payı tavanı `yon-v2.md` §2.5 ile aynı fikirdir — masaüstü ~900 px / mobil ~520 px; bir ekrandan uzun hapis yok. Pin, tarayıcının kaydırma fiziğini bozar, mobilde adres çubuğu/ivme ile çatışır ve `yon.md`'nin "sayfa kullanıcının" ilkesini ihlal eder.

### 1.2 Neden P4 slayt geri gelmesin

P4'ün reddi (`yon-v2.md` §1) fotoğraf **dizisinden** hareket üretmeyeydi. Kling klipleri birleştirilirken aynı hataya düşülmez: **tek sürekli kamera, aynı ufuk**. Kesmeli montaj, sahne değişimi, farklı mekânların arka arkaya konması = slayt grameri → kabul değil. Çapraz geçiş, flipbook, kare indeksi, Ken Burns otomatik, karusel yasakları **durur**.

### 1.3 Neden full-bleed video + üstünde yazı yok

Asimetrik split kilitlidir: 1280'de metin sol **5/12**, plaka sağ **7/12** ve sağ kenara taşar; 375'te plaka üstte (4:5), metin altta. **Metin hiçbir zaman görselin üstünde değil.** Full-bleed video + üstüne yazı, hem bu sözleşmeyi hem okunabilirliği hem de LCP disiplinini bozar; jenerik "saas hero" görünümüdür, kimlik değildir.

---

## 2. Mekanizma

| Sürücü | Video varken | Ne yapmaz |
|---|---|---|
| **Kaydırma (scroll-scrub)** | Belge kaydırma ilerlemesi → `video.currentTime` (plaka görünürken) | Kaydırmayı pinlemez, jack yok, otomatik ilerletmez |
| **Zaman (rAF zamanı)** | **YOK** — video varken zaman sürücüsü kapalıdır | Dalga fazı, ışık süpürme, nabız: hepsi KAPALI |

Video bağlanınca `HeroUfuk` kanvasının zaman sürücülü hareketi (dalga/nabız/ufuk kayması) **kapanır**; plaka hareket kaynağı tek başına videodur. Kanvas katmanları sökülür veya devre dışı bırakılır — ikisi aynı anda hareket üretmez.

- Otomatik oynatma **yok**, ses **yok**, loop **yok**, controls **yok**. Hareket yalnız kullanıcı kaydırınca.
- Scrub eşlemesi: plakanın görünür kaydırma aralığı (masaüstü ~900 px / mobil ~520 px) videonun tüm süresine yayılır. Kesin eşleme eğrisi video tesliminde ölçülür.

---

## 3. Varlık sözleşmesi

Konum: `site/public/hero/`.

| Varlık | Durum |
|---|---|
| Poster (LCP) | Mevcut kapak (`kapak-masaustu.avif/webp`, `kapak-mobil.avif/webp`) durabilir; ya da videonun ilk karesinden AVIF üretilir. Karar video tesliminde. |
| Video (birincil) | `hero-plaka.webm` |
| Video (yedek) | `hero-plaka.mp4` (eski `yon-v2.md` §2.2'deki mp4 yasağı **yalnız hero plakası için** kalkar; diğer yüzeylerde mp4/gif karusel hâlâ yasak) |

Kilitler:

- **Ses yok** (ses kanalı üretimde sıyrılır).
- **Süre hedefi:** 4–8 sn kaynak; scrub tüm süreye yayılır.
- **Boyut tavanı (KİLİT):** mobil video **≤ 1,2 MB**, masaüstü video **≤ 2,5 MB**. Tek dosya; 4K yok; 720–1080 plaka genişliği yeter. Tavan aşılırsa kare hızı/bitrate düşer — **çözünürlük şişmez**.
- **Sahne (K6/K8):** bölge-nötr ufuk/kıyı/ışık. Tanınabilir şehir silueti, yüz, tabela, belirli Samsun yeri **yok**. Ağır denizcilik teması yok. Bu video **yer fotoğrafı değildir** (K2): vitrinde, yer detayda, OG yer görselinde kullanılmaz.

---

## 4. Yükleme

- **LCP elemanı poster karedir.** `<video>` LCP **olamaz**. Poster `fetchpriority=high` ile `<picture>` (mevcut `HeroKapak` düzeni) üzerinden sunulur.
- Video `preload="none"`; yüklemesi **IntersectionObserver** (hero kesişince) veya `window load` sonrası başlar. Kesin tetik uygulamada seçilir; ikisi de kabul, ikisi dışına çıkılmaz.
- Sekme gizli (`document.hidden`) veya hero ekran dışı → `currentTime` güncellemesi durur; dinleyici/rAF boşa çalışmaz.

---

## 5. Fallback tablosu

| Koşul | Davranış |
|---|---|
| `prefers-reduced-motion: reduce` | **Yalnız poster.** `<video>` etiketi mount bile edilmez — **0 video isteği**. Nefes/scale yok. |
| JS yok / JS hata | Poster; hero tam işlevli (metin, CTA, bağlantılar). |
| `saveData` / 2g | Video yüklenmez; poster. |
| Decode / kaynak hatası | Poster kalır; hata sessizce yutulur, hero işlevsel. |
| **Video henüz yok (BUGÜN)** | `yon-v2.md` kanvas sözleşmesi yürürlükte: `HeroUfuk` prosedürel ufuk + statik kapak. |

---

## 6. Erişilebilirlik

- Video ve plaka `aria-hidden`; poster `alt=""` (dekoratif).
- Tek `h1` metindedir; metin sırası değişmez (etiket → h1 → GEO tanım cümlesi → çift CTA → mikro kanıt).
- Otomatik oynayan içerik yoktur → WCAG 2.2.2 duraklat düğmesi **gerekmez**. Hareket yalnız kullanıcının kaydırmasıyla oluşur.

---

## 7. Performans

- LCP ≤ 2,5 sn (poster). CLS **0**. Lighthouse mobil Perf **≥ 80**.
- rAF içinde `setState` **yasak** (DOM'a değil, yalnız `video.currentTime`'a yaz).
- `currentTime` yazımı layout okumasıyla (`scrollY` / `getBoundingClientRect`) iç içe girmez: **önce oku, sonra yaz** — aynı karede okuma-yazma-okuma zinciri kurulmaz.
- Video decode maliyeti teslimde ölçülür; hedef dışıysa bitrate/kare hızı düşürülür (§3 tavanları).

---

## 8. Kling / AI üretim kuralları

- Kling AI (veya eşdeğer üretim aracı) **yalnız hero plaka atmosferi** için izinlidir.
- **Künye zorunlu:** video tesliminde `plan/tasarim/gorsel-kunye.md`'ye eklenir — araç adı, üretim tarihi, sahne tarifi (prompt özeti), yüz/marka/tabela yok denetimi.
- Birden çok klip kullanılacaksa tek sürekli kamera / aynı ufuk şartı geçerlidir (§1.2); kesmeli birleştirme kabul değil.
- **Yasak yüzeyler:** yer kartı, OG yer görseli, keşif vitrini, rehber görselleri. AI üretimi görsel yalnız hero plakasındadır.

---

## 9. Uygulama notu (kod yok)

- Mevcut `HeroKapak` (RSC, asimetrik split + `<picture>` LCP) **kalır**; sökülmez.
- Video gelince: `HeroUfuk` rAF/zaman sürücüsü kapanır; scrub bağlantısı `video.currentTime`'a taşınır. Bileşen arayüzü ve fallback davranışı §5 tablosuna göre kurulur.
- Harita bölümüne (G2) dokunulmaz.
- Bugün yapılacak iş **yoktur**: kanvas `yon-v2.md` ile çalışmaya devam eder.

---

## 10. Yapılmayacaklar

- Pin, scroll-jack, sticky hero hapsetme, Lenis/GSAP ScrollTrigger pin.
- Scrub için kütüphane şartı yok — vanilla (IO + rAF + scroll dinleyici) yeter.
- `canvas-design` skill ile poster üretme — poster mevcut kapaktan veya video ilk karesinden gelir.
- Unsplash kare sekansını / flipbook'u geri getirme.
- Full-bleed video, video üstü metin, otomatik oynatma, ses, loop, controls.
- Videoyu yer kartı / OG / vitrin / rehber görseli olarak kullanma.
