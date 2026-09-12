# P4-REV kanıt raporu

**Tarih:** 2026-09-06 · **Commit yok** · Sözleşme: `plan/tasarim/yon-v2.md`  
**Sunucu:** `next start` port **3000** (3001 kapalı). Devtunnel 3000'i dinliyor.

---

## yon-v2 özeti — 6 madde

1. **Teşhis.** Slayt hissi Unsplash kalitesinden değil: çapraz geçiş plaka sekansı, sahne süreksizliği, Ken Burns, zaman tetikli kare indeksi ve sayfa ritminin aynı kesme gramerini tekrarlaması.
2. **Yasak.** Otomatik fotoğraf geçişi her yüzeyde kapalı. `HeroSekans` / `k-*` hattı silindi. Fotoğraf varsa tek statik kare durur.
3. **Hareket kaynağı.** Zaman + scroll-scrub; 5 kanvas katmanı (gök, 3 dalga, ufuk+şamandıra+düğüm) + CSS grain. Hover nefesi `scale ≤ 1,03`. Reduced-motion = statik kapak, rAF yok, 0 ek kare isteği.
4. **Anti-slayt 5 kural.** Statik duotone plaka; kesikli ayraç / su hattı; kartta gölge yok; ışık/koyu mürekkep bant dönüşü; tek ease ailesi.
5. **Palet ritmi.** Hex değişmedi. Kağıt dokusu %5,2 / koyu %8; vitrin koyu banda alındı; kart h3 ink, hero h1 bordo.
6. **Bütçe.** Kare sekansı 0 KB. Kapak LCP (masaüstü 66,7 KB / mobil 40,2 KB). Ek hareket JS+grain hedef ≤ 150 KB.

---

## Ölçüm tablosu

| Kapı | Hedef | Sonuç | Not |
|---|---|---|---|
| Gözlenen LCP 1280 | ≤ 2,5 sn | **696 ms** | `kapak-masaustu.avif` |
| Gözlenen LCP 375 | ≤ 2,5 sn | **256 ms** | `kapak-mobil.avif` |
| CLS 1280 / 375 | 0 | **0 / 0** | Playwright |
| Chrome DevTools LCP | — | **463 ms** | CLS 0,00; indirme 9 ms |
| Lighthouse mobil Perf | ≥ 80 | **86** | Üç koşu: 85 / 68 / 86 (medyan 85). Lab Slow 4G LCP 3,8 sn; gözlenen LCP ayrı kapı. |
| Lighthouse CLS | 0 | **0** | |
| Kare isteği (`/hero/k-*`) | 0 | **0** | |
| Reduced-motion ek istek | 0 | **0** | Kanvas DOM'da, `display:none`, rAF yok |
| Ufuk hareket (t0≠t1≠t2) | sürekli | **true** | Aynı kapak; orta satır toplamı değişiyor |
| Yatay taşma | 0 | **0** | |

Ham JSON: `p4-rev-olcum.json`, `lh-anasayfa.json`.

---

## Chrome DevTools — en ağır 3 kalem

Hero açık, üretim `http://127.0.0.1:3000/`, CPU 1×, ağ kısıtsız.

1. **LCP render delay 369 ms (%80).** Kapak 9 ms'de inmiş; boya font/CSS/React hidrasyonunu bekliyor. Çözüm notu: preload + `decoding="sync"` duruyor. Kare decode yok. İleride Fraunces/Sora yüz sayısını kesmek bu dilimi düşürür; P4-REV'de palet/tipografi kilidi yüzünden yapılmadı.
2. **DOM layout 77 ms (311 düğüm, derinlik 13).** En geniş ebeveyn ilçe `<ol>` (17 çocuk). Hero kareleri değil vitrin. Çözüm notu: 17 satır için sanallaştırma yok; kabul.
3. **Legacy JS ~14,4 KB.** Next polyfill/transpile. Çözüm notu: uygulama kodu değil; kare bütçesine dönülmez.

Kanvas: idle başlar, ~30 fps, path adımı `w/72`. rAF içinde `setState` yok.

---

## Ekran görüntüleri

Hepsi `plan/tasarim/p4-rev-dogrulama/`.

### Hero t0 / t1 / t2 — aynı fotoğraf, sürekli katman

![1280 t0](anasayfa-1280-hero-t0.png)
![1280 t1](anasayfa-1280-hero-t1.png)
![1280 t2](anasayfa-1280-hero-t2.png)

Mobil: `anasayfa-375-hero-t0.png` … `t2.png`.

### Ana sayfa 1280 üst / orta / alt

![1280 üst](anasayfa-1280-ust.png)
![1280 orta](anasayfa-1280-orta.png)
![1280 alt](anasayfa-1280-alt.png)

375: `anasayfa-375-ust.png` / `orta.png` / `alt.png`.

### Reduced-motion

![reduced-motion](reduced-motion-1280.png)

Dalga/düğüm yok; tek kapak duruyor.
