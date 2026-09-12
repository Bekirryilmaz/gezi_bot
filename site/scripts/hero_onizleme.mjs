/** Kontrol karesi: hero kapaklarini ve secili kareleri tek PNG'de yan yana koyar. */
import { mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import sharp from "sharp";

const KOK = join(dirname(fileURLToPath(import.meta.url)), "..", "..");
const CIKTI = join(KOK, "plan", "tasarim", "p4-dogrulama");
mkdirSync(CIKTI, { recursive: true });

const HUCRE_G = 320;
const HUCRE_Y = 240;

const KARELER = [
  ["kapak", join(KOK, "site", "public", "hero", "kapak-masaustu.avif")],
  ["k-010", join(KOK, "site", "public", "hero", "masaustu", "k-010.avif")],
  ["k-018", join(KOK, "site", "public", "hero", "masaustu", "k-018.avif")],
  ["k-030", join(KOK, "site", "public", "hero", "masaustu", "k-030.avif")],
  ["k-042", join(KOK, "site", "public", "hero", "masaustu", "k-042.avif")],
  ["k-054", join(KOK, "site", "public", "hero", "masaustu", "k-054.avif")],
  ["k-066", join(KOK, "site", "public", "hero", "masaustu", "k-066.avif")],
  ["mobil-kapak", join(KOK, "site", "public", "hero", "kapak-mobil.avif")],
];

const sutun = 4;
const satir = Math.ceil(KARELER.length / sutun);
const katmanlar = [];
for (const [i, [, yol]] of KARELER.entries()) {
  katmanlar.push({
    input: await sharp(yol).resize(HUCRE_G, HUCRE_Y, { fit: "cover" }).png().toBuffer(),
    left: (i % sutun) * HUCRE_G,
    top: Math.floor(i / sutun) * HUCRE_Y,
  });
}

await sharp({
  create: {
    width: sutun * HUCRE_G,
    height: satir * HUCRE_Y,
    channels: 3,
    background: { r: 244, g: 239, b: 231 },
  },
})
  .composite(katmanlar)
  .png()
  .toFile(join(CIKTI, "hero-kontak.png"));

console.log(
  "yazildi:",
  join(CIKTI, "hero-kontak.png"),
  KARELER.map(([a]) => a).join(" "),
);
