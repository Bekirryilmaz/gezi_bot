import { chromium } from "playwright";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const KOK = path.resolve(__dirname, "..");
const CIKTI = path.resolve(KOK, "..", "plan", "logo", "faz2-dogrulama");
const YER = "7e4f304c-8540-467f-a982-80457f3f9d8c";
const SAYFALAR = [
  ["anasayfa", "/"],
  ["kesif", "/sehir/samsun"],
  ["bolgeler", "/sehir/samsun/bolgeler"],
  ["rota", "/sehir/samsun/rota"],
  ["yer", `/yer/${YER}`],
  ["tasarim", "/tasarim-sistemi"],
  ["yok", "/bu-sayfa-yok-404"],
];

async function konumCek(sayfa, ad) {
  await sayfa.evaluate(() => window.scrollTo(0, 0));
  await sayfa.waitForTimeout(900);
  await sayfa.screenshot({ path: path.join(CIKTI, `${ad}-ust.png`) });
  await sayfa.evaluate(() =>
    window.scrollTo(
      0,
      Math.max(0, (document.body.scrollHeight - window.innerHeight) / 2),
    ),
  );
  await sayfa.waitForTimeout(900);
  await sayfa.screenshot({ path: path.join(CIKTI, `${ad}-orta.png`) });
  await sayfa.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
  await sayfa.waitForTimeout(900);
  await sayfa.screenshot({ path: path.join(CIKTI, `${ad}-alt.png`) });
}

async function main() {
  fs.mkdirSync(CIKTI, { recursive: true });
  const tarayici = await chromium.launch({ headless: true });

  const og = await tarayici.newPage({ viewport: { width: 1200, height: 630 } });
  await og.goto("http://127.0.0.1:3000/logo/og-sablon.html", {
    waitUntil: "networkidle",
    timeout: 60000,
  });
  await og.waitForTimeout(800);
  await og.screenshot({
    path: path.join(KOK, "public", "og-default.png"),
    clip: { x: 0, y: 0, width: 1200, height: 630 },
  });
  await og.close();
  console.log("og-default.png yazildi");

  for (const genislik of [1280, 375]) {
    const sayfa = await tarayici.newPage({
      viewport: { width: genislik, height: genislik === 375 ? 812 : 800 },
    });
    for (const [ad, yol] of SAYFALAR) {
      const kod = `${ad}-${genislik}`;
      await sayfa.goto(`http://127.0.0.1:3000${yol}`, {
        waitUntil: "networkidle",
        timeout: 60000,
      });
      await sayfa.waitForTimeout(500);
      await konumCek(sayfa, kod);
      console.log("cekildi", kod);
    }
    await sayfa.close();
  }

  const azalt = await tarayici.newPage({
    viewport: { width: 1280, height: 800 },
    reducedMotion: "reduce",
  });
  await azalt.goto("http://127.0.0.1:3000/", {
    waitUntil: "domcontentloaded",
    timeout: 60000,
  });
  await azalt.waitForTimeout(700);
  const hareket = await azalt.evaluate(() => {
    const dalga = document.querySelector(".dalga-a");
    const stil = dalga ? getComputedStyle(dalga).animationName : "yok";
    return {
      animationName: stil,
      reduced: matchMedia("(prefers-reduced-motion: reduce)").matches,
    };
  });
  await azalt.screenshot({
    path: path.join(CIKTI, "reduced-motion-anasayfa.png"),
  });
  fs.writeFileSync(
    path.join(CIKTI, "reduced-motion.json"),
    JSON.stringify(hareket, null, 2),
  );
  console.log("reduced-motion", hareket);
  await azalt.close();
  await tarayici.close();
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
