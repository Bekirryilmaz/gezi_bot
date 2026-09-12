/**
 * Kaynak plakalarin tek karede on izlemesi (yuz / marka / tabela denetimi icin).
 */
import { readdirSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import sharp from "sharp";

const KOK = join(dirname(fileURLToPath(import.meta.url)), "..", "..");
const KAYNAK = join(KOK, "plan", "tasarim", "hero-kaynak");
const HUCRE_W = 420;
const HUCRE_H = 315;
const SUTUN = 3;

const dosyalar = readdirSync(KAYNAK)
  .filter((d) => d.endsWith(".jpg"))
  .sort();

const satir = Math.ceil(dosyalar.length / SUTUN);
const parcalar = [];

for (const [i, dosya] of dosyalar.entries()) {
  const buf = await sharp(join(KAYNAK, dosya))
    .resize(HUCRE_W, HUCRE_H, { fit: "cover" })
    .toBuffer();
  parcalar.push({
    input: buf,
    left: (i % SUTUN) * HUCRE_W,
    top: Math.floor(i / SUTUN) * HUCRE_H,
  });
}

const cikti = join(KAYNAK, "_kontak.png");
await sharp({
  create: {
    width: SUTUN * HUCRE_W,
    height: satir * HUCRE_H,
    channels: 3,
    background: { r: 20, g: 33, b: 38 },
  },
})
  .composite(parcalar)
  .png()
  .toBuffer()
  .then((b) => writeFileSync(cikti, b));

console.log("kontak yazildi:", cikti, dosyalar.join(", "));
