/**
 * G1-G4 dogrulama: doruk token, harita lazy, logo, mikro etkilesim.
 *
 * Olcer:
 *  - 375 / 1280 ust-orta-alt (harita bolumu dahil)
 *  - harita scroll t0 / t1 / t2
 *  - katlanmadan once 0 karo (openfreemap planet)
 *  - LCP + CLS
 *  - reduced-motion: statik harita kapagi, 0 karo
 *
 * Kullanim: node scripts/p5-g-dogrulama.mjs [taban-url]
 */
import { chromium } from "playwright";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const KOK = path.resolve(__dirname, "..");
const CIKTI = path.resolve(KOK, "..", "plan", "tasarim", "p5-g-dogrulama");
const TABAN = process.argv[2] ?? "http://127.0.0.1:3000";

const OLCUM_ENJEKSIYON = `
  window.__lcp = null;
  window.__cls = 0;
  try { document.documentElement.style.scrollBehavior = "auto"; } catch (e) {}
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

function karoIstekMi(url) {
  if (!url.includes("tiles.openfreemap.org")) return false;
  if (url.includes("/fonts/") || url.includes("/styles/") || url.includes("/sprites/")) {
    return false;
  }
  return /\/\d+\/\d+\/\d+/.test(url);
}

async function sahneKaresi(sayfa, yol) {
  const sahne = sayfa.locator("[data-harita-sahne]");
  await sahne.scrollIntoViewIfNeeded();
  await sayfa.waitForTimeout(400);
  const kutu = await sahne.boundingBox();
  if (!kutu || kutu.width < 8 || kutu.height < 8) {
    throw new Error("harita sahnesi kutu vermedi");
  }
  await sayfa.screenshot({
    path: yol,
    clip: kutu,
    animations: "allow",
  });
}

async function haritaKareleri(sayfa, ad) {
  await sayfa.locator("[data-harita-sahne]").scrollIntoViewIfNeeded();
  await sayfa
    .locator('[data-harita-yuklu="1"]')
    .waitFor({ state: "attached", timeout: 20000 })
    .catch(() => {});
  await sayfa.waitForTimeout(800);
  await sahneKaresi(sayfa, path.join(CIKTI, `${ad}-harita-t0.png`));
  await sayfa.evaluate(() => window.scrollBy(0, 360));
  await sayfa.waitForTimeout(900);
  await sahneKaresi(sayfa, path.join(CIKTI, `${ad}-harita-t1.png`));
  await sayfa.evaluate(() => window.scrollBy(0, 360));
  await sayfa.waitForTimeout(900);
  await sahneKaresi(sayfa, path.join(CIKTI, `${ad}-harita-t2.png`));
}

async function sayfaOlc(tarayici, genislik, yukseklik, ad) {
  const baglam = await tarayici.newContext({
    viewport: { width: genislik, height: yukseklik },
    deviceScaleFactor: 2,
  });
  const istekler = { onceKaro: 0, sonraKaro: 0, maplibre: 0, ofmStil: 0 };
  let katlandi = false;
  baglam.on("request", (r) => {
    const url = r.url();
    if (url.includes("maplibre")) istekler.maplibre += 1;
    if (url.includes("tiles.openfreemap.org/styles/")) istekler.ofmStil += 1;
    if (!karoIstekMi(url)) return;
    if (katlandi) istekler.sonraKaro += 1;
    else istekler.onceKaro += 1;
  });

  const sayfa = await baglam.newPage();
  await sayfa.addInitScript({ content: OLCUM_ENJEKSIYON });
  await sayfa.goto(`${TABAN}/`, { waitUntil: "load", timeout: 90000 });
  await sayfa.waitForTimeout(800);

  const katlamaOncesi = await sayfa.evaluate(() => {
    const bolum = document.querySelector("[data-harita-bolum]");
    const sahne = document.querySelector("[data-harita-sahne]");
    const bolumDikey = bolum?.getBoundingClientRect();
    const sahneDikey = sahne?.getBoundingClientRect();
    return {
      haritaVar: Boolean(bolum),
      haritaKatlamada: bolumDikey ? bolumDikey.top < window.innerHeight : false,
      sahneKatlamada: sahneDikey
        ? sahneDikey.top < window.innerHeight && sahneDikey.bottom > 0
        : false,
      yuklu: document
        .querySelector("[data-harita-yuklu]")
        ?.getAttribute("data-harita-yuklu"),
      dorukSinif: document.querySelector(".bolum-doruk")?.className ?? "",
      dorukMurekkep: Boolean(
        document.querySelector(".bolum-doruk.doku-koyu.bg-murekkep"),
      ),
      logoKilit: Boolean(document.querySelector('.site-header img[src*="karo-seffaf"]')),
    };
  });

  const lcp = await sayfa.evaluate(() => window.__lcp);
  await sayfa.screenshot({ path: path.join(CIKTI, `${ad}-ust.png`) });

  katlandi = true;
  await haritaKareleri(sayfa, ad);

  await sayfa.evaluate(() =>
    window.scrollTo(0, Math.max(0, (document.body.scrollHeight - innerHeight) / 2)),
  );
  await sayfa.waitForTimeout(600);
  await sayfa.screenshot({ path: path.join(CIKTI, `${ad}-orta.png`) });

  await sayfa.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
  await sayfa.waitForTimeout(600);
  await sayfa.screenshot({ path: path.join(CIKTI, `${ad}-alt.png`) });

  const cls = await sayfa.evaluate(() => Math.round(window.__cls * 10000) / 10000);
  const yatay = await sayfa.evaluate(
    () => document.documentElement.scrollWidth - document.documentElement.clientWidth,
  );
  const harita = await sayfa.evaluate(() => {
    const kanvas = document.querySelector("[data-harita-kanvas]");
    const kapak = document.querySelector(".harita-kapak-svg");
    const isik = document.querySelectorAll(".harita-isik").length;
    return {
      kanvasVar: Boolean(kanvas),
      kapakVar: Boolean(kapak),
      isikSayisi: isik,
      yuklu: document
        .querySelector("[data-harita-yuklu]")
        ?.getAttribute("data-harita-yuklu"),
    };
  });

  let plaka = null;
  if (genislik >= 1024) {
    await sayfa.locator("[data-harita-sahne]").scrollIntoViewIfNeeded();
    await sayfa.waitForTimeout(400);
    const secilenAd = await sayfa.evaluate(() => {
      const sahne = document.querySelector("[data-harita-sahne]");
      if (!sahne) return null;
      const kutu = sahne.getBoundingClientRect();
      const dugmeler = [...document.querySelectorAll(".harita-isik")];
      const icerde =
        dugmeler.find((d) => {
          const r = d.getBoundingClientRect();
          return (
            r.width > 2 &&
            r.left >= kutu.left &&
            r.right <= kutu.right &&
            r.top >= kutu.top &&
            r.bottom <= kutu.bottom
          );
        }) ?? dugmeler[Math.floor(dugmeler.length / 2)];
      if (!(icerde instanceof HTMLElement)) return null;
      icerde.click();
      return icerde.getAttribute("aria-label");
    });
    await sayfa.waitForTimeout(700);
    const yanMetin = await sayfa.evaluate(() => {
      const yan = document.querySelector("[data-harita-sahne]")?.nextElementSibling;
      return yan?.textContent?.replace(/\s+/g, " ").trim().slice(0, 180) ?? "";
    });
    plaka = {
      secilenAd,
      metin: yanMetin,
      dugme: yanMetin.includes("Bölgeyi tanı"),
    };
    await sayfa.screenshot({
      path: path.join(CIKTI, `${ad}-plaka-panel.png`),
      animations: "allow",
    });
    const bolgeCta = sayfa.locator("a", { hasText: "Bölgeyi tanı" }).last();
    await bolgeCta.click();
    await sayfa.waitForURL(/\/bolgeler/, { timeout: 15000 });
    plaka = { ...plaka, bolgeUrl: sayfa.url() };
  }

  await baglam.close();
  return {
    genislik,
    lcp,
    cls,
    yatayTasma: yatay,
    katlamaOncesi,
    harita,
    istekler,
    plaka,
  };
}

async function azaltilmisHareket(tarayici) {
  const baglam = await tarayici.newContext({
    viewport: { width: 1280, height: 800 },
    deviceScaleFactor: 2,
    reducedMotion: "reduce",
  });
  let karo = 0;
  baglam.on("request", (r) => {
    if (karoIstekMi(r.url())) karo += 1;
  });
  const sayfa = await baglam.newPage();
  await sayfa.addInitScript({ content: OLCUM_ENJEKSIYON });
  await sayfa.goto(`${TABAN}/`, { waitUntil: "load", timeout: 90000 });
  await sayfa.waitForTimeout(800);
  await sayfa.locator("[data-harita-bolum]").scrollIntoViewIfNeeded();
  await sayfa.waitForTimeout(1600);
  const durum = await sayfa.evaluate(() => {
    const kanvas = document.querySelector("[data-harita-kanvas]");
    const kapak = document.querySelector(".harita-kapak-svg");
    const heroUfuk = document.querySelector("[data-hero-ufuk]");
    return {
      tercih: matchMedia("(prefers-reduced-motion: reduce)").matches,
      haritaKanvas: Boolean(kanvas),
      kapakVar: Boolean(kapak),
      heroUfukGorunur: heroUfuk ? getComputedStyle(heroUfuk).display !== "none" : false,
      yuklu: document
        .querySelector("[data-harita-yuklu]")
        ?.getAttribute("data-harita-yuklu"),
    };
  });
  await sayfa.screenshot({ path: path.join(CIKTI, "reduced-motion-1280.png") });
  await baglam.close();
  return { ...durum, karo };
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
  fs.writeFileSync(path.join(CIKTI, "p5-g-olcum.json"), JSON.stringify(rapor, null, 2));
  console.log(JSON.stringify(rapor, null, 2));
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
