/**
 * P4-REV dogrulama: prosedurel ufuk + anti-slayt ana sayfa.
 *
 * Olcer:
 *  - 375 / 1280 ust-orta-alt
 *  - hero t0 / t1 / t2 (1,5 sn ara) — ayni kapak, hareketli katman
 *  - LCP + CLS
 *  - /hero/k-* istegi 0
 *  - reduced-motion: kanvas rAF yok, 0 ek hero istegi
 *
 * Kullanim: node scripts/p4-rev-dogrulama.mjs [taban-url]
 */
import { chromium } from "playwright";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const KOK = path.resolve(__dirname, "..");
const CIKTI = path.resolve(KOK, "..", "plan", "tasarim", "p4-rev-dogrulama");
const TABAN = process.argv[2] ?? "http://127.0.0.1:3000";

const OLCUM_ENJEKSIYON = `
  window.__lcp = null;
  window.__cls = 0;
  new PerformanceObserver((liste) => {
    const son = liste.getEntries().at(-1);
    if (son) {
      window.__lcp = {
        sure: Math.round(son.startTime),
        boyut: son.size,
        etiket: son.element ? son.element.tagName.toLowerCase() : null,
        sinif: son.element ? String(son.element.className) : null,
        url: son.url || null,
      };
    }
  }).observe({ type: "largest-contentful-paint", buffered: true });
  new PerformanceObserver((liste) => {
    for (const g of liste.getEntries()) {
      if (!g.hadRecentInput) window.__cls += g.value;
    }
  }).observe({ type: "layout-shift", buffered: true });
`;

function kb(bayt) {
  return Math.round((bayt / 1024) * 10) / 10;
}

function heroIstekMi(yol) {
  return yol.startsWith("/hero/");
}

function kareIstekMi(yol) {
  return /\/hero\/(masaustu|mobil)\//.test(yol) || /\/hero\/k-/.test(yol);
}

async function ufukOrnek(sayfa) {
  return sayfa.evaluate(() => {
    const kanvas = document.querySelector("[data-hero-ufuk]");
    if (!(kanvas instanceof HTMLCanvasElement) || kanvas.width < 8) {
      return { genislik: 0, satirToplam: 0 };
    }
    const ctx = kanvas.getContext("2d");
    if (!ctx) return { genislik: kanvas.width, satirToplam: 0 };
    const y = Math.floor(kanvas.height * 0.55);
    const veri = ctx.getImageData(0, y, kanvas.width, 1).data;
    let toplam = 0;
    for (let i = 0; i < veri.length; i++) toplam += veri[i];
    return { genislik: kanvas.width, satirToplam: toplam };
  });
}

async function heroKareleri(sayfa, ad) {
  await sayfa.evaluate(() => window.scrollTo(0, 0));
  await sayfa.waitForTimeout(1000);
  await sayfa.locator(".hero-plaka").screenshot({
    path: path.join(CIKTI, `${ad}-hero-t0.png`),
  });
  const t0 = await ufukOrnek(sayfa);
  await sayfa.waitForTimeout(1500);
  await sayfa.locator(".hero-plaka").screenshot({
    path: path.join(CIKTI, `${ad}-hero-t1.png`),
  });
  const t1 = await ufukOrnek(sayfa);
  await sayfa.waitForTimeout(1500);
  await sayfa.locator(".hero-plaka").screenshot({
    path: path.join(CIKTI, `${ad}-hero-t2.png`),
  });
  const t2 = await ufukOrnek(sayfa);
  return { t0, t1, t2 };
}

async function sayfaOlc(tarayici, genislik, yukseklik, ad) {
  const baglam = await tarayici.newContext({
    viewport: { width: genislik, height: yukseklik },
    deviceScaleFactor: 2,
  });
  const bayt = { kapak: 0, kare: 0, plaka: 0, kareSayisi: 0 };
  baglam.on("response", async (yanit) => {
    const yol = new URL(yanit.url()).pathname;
    if (!heroIstekMi(yol) && !yol.startsWith("/plaka/")) return;
    let boyut = Number(yanit.headers()["content-length"] ?? 0);
    if (!boyut) {
      boyut = await yanit
        .body()
        .then((b) => b.length)
        .catch(() => 0);
    }
    if (yol.startsWith("/plaka/")) bayt.plaka += boyut;
    else if (yol.includes("/kapak-")) bayt.kapak += boyut;
    else if (kareIstekMi(yol)) {
      bayt.kare += boyut;
      bayt.kareSayisi++;
    }
  });

  const sayfa = await baglam.newPage();
  await sayfa.addInitScript(OLCUM_ENJEKSIYON);
  await sayfa.goto(`${TABAN}/`, { waitUntil: "load", timeout: 60000 });
  await sayfa.waitForTimeout(400);

  const ufukOrnekleri = await heroKareleri(sayfa, ad);

  const lcp = await sayfa.evaluate(() => window.__lcp);
  await sayfa.screenshot({ path: path.join(CIKTI, `${ad}-ust.png`) });

  await sayfa.evaluate(() =>
    window.scrollTo(0, Math.max(0, (document.body.scrollHeight - innerHeight) / 2)),
  );
  await sayfa.waitForTimeout(800);
  await sayfa.screenshot({ path: path.join(CIKTI, `${ad}-orta.png`) });

  await sayfa.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
  await sayfa.waitForTimeout(800);
  await sayfa.screenshot({ path: path.join(CIKTI, `${ad}-alt.png`) });

  const cls = await sayfa.evaluate(() => Math.round(window.__cls * 10000) / 10000);
  const yatay = await sayfa.evaluate(
    () => document.documentElement.scrollWidth - document.documentElement.clientWidth,
  );
  const ufuk = await sayfa.evaluate(() => {
    const kanvas = document.querySelector("[data-hero-ufuk]");
    const kapak = document.querySelector(".hero-plaka img");
    return {
      kanvasVar: Boolean(kanvas),
      kapakGorunur: kapak ? kapak.getBoundingClientRect().height > 0 : false,
    };
  });

  await baglam.close();
  return {
    genislik,
    lcp,
    cls,
    yatayTasma: yatay,
    kapakKB: kb(bayt.kapak),
    kareIstek: bayt.kareSayisi,
    kareKB: kb(bayt.kare),
    kategoriPlakaKB: kb(bayt.plaka),
    ufuk,
    ufukOrnekleri,
    ufukHareket:
      ufukOrnekleri.t0.satirToplam !== ufukOrnekleri.t1.satirToplam &&
      ufukOrnekleri.t1.satirToplam !== ufukOrnekleri.t2.satirToplam,
  };
}

async function azaltilmisHareket(tarayici) {
  const baglam = await tarayici.newContext({
    viewport: { width: 1280, height: 800 },
    deviceScaleFactor: 2,
    reducedMotion: "reduce",
  });
  const ekIstek = [];
  baglam.on("request", (r) => {
    const yol = new URL(r.url()).pathname;
    if (kareIstekMi(yol)) ekIstek.push(yol);
  });
  const sayfa = await baglam.newPage();
  await sayfa.goto(`${TABAN}/`, { waitUntil: "load", timeout: 60000 });
  await sayfa.waitForTimeout(2000);
  await sayfa.evaluate(() => window.scrollTo(0, 600));
  await sayfa.waitForTimeout(800);
  const durum = await sayfa.evaluate(() => {
    const kanvas = document.querySelector("[data-hero-ufuk]");
    const kapak = document.querySelector(".hero-plaka img");
    return {
      tercih: matchMedia("(prefers-reduced-motion: reduce)").matches,
      kanvasVar: Boolean(kanvas),
      kanvasGorunur: kanvas ? getComputedStyle(kanvas).display !== "none" : false,
      kapakGorunur: kapak ? kapak.getBoundingClientRect().height > 0 : false,
    };
  });
  await sayfa.evaluate(() => window.scrollTo(0, 0));
  await sayfa.waitForTimeout(300);
  await sayfa.screenshot({ path: path.join(CIKTI, "reduced-motion-1280.png") });
  await baglam.close();
  return { ...durum, istenenKare: ekIstek.length };
}

async function main() {
  fs.mkdirSync(CIKTI, { recursive: true });
  const tarayici = await chromium.launch({ headless: true });

  const rapor = {
    taban: TABAN,
    zaman: new Date().toISOString(),
    masaustu: await sayfaOlc(tarayici, 1280, 800, "anasayfa-1280"),
    mobil: await sayfaOlc(tarayici, 375, 812, "anasayfa-375"),
    azaltilmisHareket: await azaltilmisHareket(tarayici),
  };

  await tarayici.close();
  fs.writeFileSync(path.join(CIKTI, "p4-rev-olcum.json"), JSON.stringify(rapor, null, 2));
  console.log(JSON.stringify(rapor, null, 2));
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
