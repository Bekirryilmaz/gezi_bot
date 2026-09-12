/**
 * T-16 P4 dogrulama: hero sekansi + ana sayfa.
 *
 * Olcer:
 *  - 375 / 1280'de ust-orta-alt ekran goruntusu
 *  - LCP elemani ve suresi (kaydirmadan once okunur)
 *  - Faz B sonuna kadar inen sekans baytlari (kapak ayri)
 *  - CLS
 *  - reduced-motion: kanvas gizli, statik kapak duruyor mu
 *
 * Kullanim: node scripts/p4-dogrulama.mjs [taban-url]
 */
import { chromium } from "playwright";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const KOK = path.resolve(__dirname, "..");
const CIKTI = path.resolve(KOK, "..", "plan", "tasarim", "p4-dogrulama");
const TABAN = process.argv[2] ?? "http://127.0.0.1:3001";

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
        sinif: son.element ? son.element.className : null,
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

/** Kaydirma "jack"lenmemis mi: istenen konuma gercekten gidiyor mu. */
async function kaydirmaDurustlugu(sayfa) {
  const hedef = 900;
  await sayfa.evaluate((y) => window.scrollTo(0, y), hedef);
  await sayfa.waitForTimeout(700);
  const gercek = await sayfa.evaluate(() => Math.round(window.scrollY));
  return { hedef, gercek, sapma: Math.abs(gercek - hedef) };
}

async function sayfaOlc(tarayici, genislik, yukseklik, ad) {
  const baglam = await tarayici.newContext({
    viewport: { width: genislik, height: yukseklik },
    deviceScaleFactor: 2,
  });
  const bayt = { kapak: 0, sekans: 0, plaka: 0, kareSayisi: 0 };
  baglam.on("response", async (yanit) => {
    const yol = new URL(yanit.url()).pathname;
    if (!yol.startsWith("/hero/") && !yol.startsWith("/plaka/")) return;
    let boyut = Number(yanit.headers()["content-length"] ?? 0);
    if (!boyut) {
      boyut = await yanit
        .body()
        .then((b) => b.length)
        .catch(() => 0);
    }
    if (yol.startsWith("/plaka/")) bayt.plaka += boyut;
    else if (yol.includes("/kapak-")) bayt.kapak += boyut;
    else {
      bayt.sekans += boyut;
      bayt.kareSayisi++;
    }
  });

  const sayfa = await baglam.newPage();
  await sayfa.addInitScript(OLCUM_ENJEKSIYON);
  await sayfa.goto(`${TABAN}/`, { waitUntil: "load", timeout: 60000 });
  await sayfa.waitForTimeout(2600); // Faz A (1,5 sn) bitsin

  const lcp = await sayfa.evaluate(() => window.__lcp);
  await sayfa.screenshot({ path: path.join(CIKTI, `${ad}-ust.png`) });

  const kaydirma = await kaydirmaDurustlugu(sayfa);

  // Faz B payini (900 px masaustu / 520 px mobil) adim adim gec.
  for (let y = 0; y <= 1000; y += 100) {
    await sayfa.evaluate((v) => window.scrollTo(0, v), y);
    await sayfa.waitForTimeout(180);
  }
  await sayfa.waitForTimeout(1800);
  const fazBSonu = { ...bayt };

  await sayfa.evaluate(() =>
    window.scrollTo(0, Math.max(0, (document.body.scrollHeight - innerHeight) / 2)),
  );
  await sayfa.waitForTimeout(1200);
  await sayfa.screenshot({ path: path.join(CIKTI, `${ad}-orta.png`) });

  await sayfa.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
  await sayfa.waitForTimeout(1200);
  await sayfa.screenshot({ path: path.join(CIKTI, `${ad}-alt.png`) });

  const cls = await sayfa.evaluate(() => Math.round(window.__cls * 10000) / 10000);
  const yatay = await sayfa.evaluate(
    () => document.documentElement.scrollWidth - document.documentElement.clientWidth,
  );

  // Sayfa tamamen gezildikten sonraki toplam (Faz B sonrasi tembel kareler dahil).
  await sayfa.waitForTimeout(600);
  const toplam = { ...bayt };
  await baglam.close();

  return {
    genislik,
    lcp,
    cls,
    yatayTasma: yatay,
    kaydirma,
    kapakKB: kb(toplam.kapak),
    sekansFazBSonuKB: kb(fazBSonu.sekans),
    sekansToplamKB: kb(toplam.sekans),
    inenKare: toplam.kareSayisi,
    kategoriPlakaKB: kb(toplam.plaka),
  };
}

async function azaltilmisHareket(tarayici) {
  const baglam = await tarayici.newContext({
    viewport: { width: 1280, height: 800 },
    deviceScaleFactor: 2,
    reducedMotion: "reduce",
  });
  const sekansIstek = [];
  baglam.on("request", (r) => {
    const yol = new URL(r.url()).pathname;
    if (yol.startsWith("/hero/") && !yol.includes("/kapak-")) sekansIstek.push(yol);
  });
  const sayfa = await baglam.newPage();
  await sayfa.goto(`${TABAN}/`, { waitUntil: "load", timeout: 60000 });
  await sayfa.waitForTimeout(2500);
  await sayfa.evaluate(() => window.scrollTo(0, 600));
  await sayfa.waitForTimeout(1500);
  const durum = await sayfa.evaluate(() => {
    const kanvas = document.querySelector(".hero-plaka canvas");
    const kapak = document.querySelector(".hero-plaka img");
    return {
      tercih: matchMedia("(prefers-reduced-motion: reduce)").matches,
      kanvasVar: Boolean(kanvas),
      kanvasGorunur: kanvas ? getComputedStyle(kanvas).display !== "none" : false,
      kapakGorunur: kapak ? kapak.getBoundingClientRect().height > 0 : false,
    };
  });
  await sayfa.evaluate(() => window.scrollTo(0, 0));
  await sayfa.waitForTimeout(400);
  await sayfa.screenshot({ path: path.join(CIKTI, "reduced-motion-1280.png") });
  await baglam.close();
  return { ...durum, istenenSekansKaresi: sekansIstek.length };
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
  fs.writeFileSync(path.join(CIKTI, "p4-olcum.json"), JSON.stringify(rapor, null, 2));
  console.log(JSON.stringify(rapor, null, 2));
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
