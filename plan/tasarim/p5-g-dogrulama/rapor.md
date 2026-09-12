# P5 G1–G4 kanıt raporu

**Tarih:** 2026-09-06 · **Commit yok** · Sözleşme: `plan/tasarim/yon.md`, `plan/tasarim/yon-v2.md`, `plan/00_brief_eki.md`  
**Sunucu:** API `8125` (yeni `enlem`/`boylam`) + `next start` port **3000**

---

## Dört madde

1. **G1 — Doruk rengi.** Doruk CTA `bg-bordo` değil; kanıt bandıyla aynı `doku-koyu bg-murekkep`. Üstte `border-t-2 border-bordo` + 40px `LogoKaro`.
2. **G2 — Atlas.** Hero’nun hemen altında kağıt bant. MapLibre GL JS 6 + OpenFreeMap Positron (anahtarsız). Stil JSON marka paletine boyandı (kağıt zemin, mürekkep etiket, bordo sınır). 17 Samsun ilçesi nokta işaretçisi (poligon yok). Scroll-scrub `jumpTo`; tıklanınca yan plaka. Lazy: katlamadan **0 karo**; worker `public/maplibre/maplibre-gl-worker.mjs`.
3. **G3 — Logo.** Header kilit 40px. Hero ufukta HTML `karo-seffaf.png` (canvas dışında, `loading="lazy"`). Bölüm kenar notunda 16px karo. Işık noktası: harita işaretçisi + ufuk nabız.
4. **G4 — Ayrışma.** Manyetik CTA (hero + doruk, yalnız `transform`), birincil düğmede ışık süpürme, kartta `su-hatti` `scaleX`, `KesilenAyrac` IO. Hepsi `transform`/`opacity`.

Palet hex kilitli.

---

## Ölçüm tablosu

| Kapı | Hedef | Sonuç | Not |
|---|---|---|---|
| Gözlenen LCP 1280 | ≤ 2,5 sn | **336 ms** | `kapak-masaustu.avif` |
| Gözlenen LCP 375 | ≤ 2,5 sn | **324 ms** | `kapak-mobil.avif` |
| CLS 1280 / 375 | 0 | **0 / 0** | Playwright |
| Chrome DevTools LCP | — | **481 ms** | Render delay 402 ms (%84); kapak indirme 26 ms. CLS **0,00** |
| Lighthouse mobil Perf | ≥ 80 | **70** (lab) | Slow 4G + 4× CPU. En iyi sakin koşu **75**; gürültülü **61**. TBT lab **420 ms** (P4-REV **160 ms**). Kapı lab’da kaçtı; gözlenen LCP/CLS ayrı kapı ve geçti. |
| Lighthouse CLS | 0 | **0** | |
| Harita karo katlamadan önce | 0 | **0 / 0** | 1280 ve 375 `onceKaro` |
| Harita karo katladıktan sonra | > 0 | **35 / 26** | OpenFreeMap `planet/…pbf` |
| Reduced-motion karo | 0 | **0** | Kanvas yok; SVG kapak |
| Yatay taşma | 0 | **0** | |
| Doruk mürekkep token | evet | **true** | `doku-koyu bg-murekkep` |
| İşaretçi → plaka → bölgeler | evet | **Atakum / Ayvacık** → `/sehir/samsun/bolgeler` | Playwright + MCP |

Ham JSON: `p5-g-olcum.json`, `lh-anasayfa.json`.

---

## Chrome DevTools — en ağır 3 kalem

Hero açık, üretim `http://127.0.0.1:3000/`, CPU 1×, ağ kısıtsız.

1. **LCP render delay 402 ms (%84).** Kapak 26 ms’de inmiş; boya font/CSS/hidrasyonu bekliyor. Çözüm notu: preload duruyor. Kare decode yok.
2. **DOM layout 113 ms (415 düğüm, derinlik 13).** En geniş ebeveyn harita kapak SVG (21 çocuk: kıyı + 17 ilçe halkası). Çözüm notu: katlamada `content-visibility`; işaretçi düğmeleri IO’dan önce DOM’da yok.
3. **Legacy JS ~14,4 KB.** Next polyfill (`Array.at` / `flatMap` vb.). Çözüm notu: uygulama kodu değil.

Harita: katlamadan 0 OpenFreeMap isteği. Worker bağlanınca karo gelir. rAF haritada `setState` yok (`jumpTo`). Hero ufuk rAF ilk kaydırmaya (veya 8 sn) ertelendi — Lighthouse TBT için.

---

## Ekran görüntüleri

Hepsi `plan/tasarim/p5-g-dogrulama/`.

### Harita scroll t0 / t1 / t2 — aynı stil, kamera uçar

![1280 t0](anasayfa-1280-harita-t0.png)
![1280 t1](anasayfa-1280-harita-t1.png)
![1280 t2](anasayfa-1280-harita-t2.png)

375: `anasayfa-375-harita-t0.png` … `t2.png`.

### Ana sayfa 1280 üst / orta / alt

![1280 üst](anasayfa-1280-ust.png)
![1280 orta](anasayfa-1280-orta.png)
![1280 alt](anasayfa-1280-alt.png)

375: `anasayfa-375-ust.png` / `orta.png` / `alt.png`.

### Plaka paneli + reduced-motion

![plaka](anasayfa-1280-plaka-panel.png)
![reduced-motion](reduced-motion-1280.png)

Reduced-motion: MapLibre yok; SVG kapak + “Bir ilçe ışığına dokun.”

---

## Lab Lighthouse notu

Hedef ≥ 80 lab’da bu turda **tutmadı** (son koşu **70**, TBT **420 ms**, LCP lab **5,0 sn**). P4-REV lab 86 / TBT 160 ms idi; fark yeni atlas HTML’si + ek istemci adaları + 4× CPU altında uzun görev. Gözlenen LCP (Playwright / DevTools) ve CLS kapıları geçti; harita lazy kanıtı geçti.

---

## Kullanılan skill / MCP

**Skill:** frontend-design, ui-ux-pro-max, animation-on-scroll, 3d-web-experiences, webapp-testing, vercel-react-best-practices.

**MCP:** context7 (`/maplibre/maplibre-gl-js` — Map, Marker, `cooperativeGestures`, `setWorkerUrl` / Turbopack worker kopyası), tavily (OpenFreeMap anahtarsız Positron), chrome-devtools (iz + LCP/DOM/legacy), playwright (375+1280, t0/t1/t2, lazy karo, Atakum → plaka → `/bolgeler`), memory (`G1-G4 tasarim turu`), postgres (önceki tur: 17 ilçe koordinatı).
