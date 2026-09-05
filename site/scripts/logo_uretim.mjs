/**
 * K8: secili logo.png'den uretim varliklari.
 * Cizgi / kompozisyon / renk degismez; yalniz olcek, kenar alfa, zemin ve ico.
 */
import { mkdirSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import sharp from "sharp";

const KOK = join(dirname(fileURLToPath(import.meta.url)), "..", "..");
const KAYNAK = join(KOK, "plan", "logo", "secili", "logo.png");
const PUBLIC = join(KOK, "site", "public");
const LOGO = join(PUBLIC, "logo");
const BORDO = { r: 108, g: 0, b: 0, alpha: 1 };
const KAGIT = { r: 244, g: 239, b: 231, alpha: 1 };

function bordoMu(r, g, b) {
  return r > 60 && r < 160 && g < 80 && b < 80;
}

async function seffafKaro() {
  const { data, info } = await sharp(KAYNAK)
    .ensureAlpha()
    .raw()
    .toBuffer({ resolveWithObject: true });
  const { width: w, height: h, channels: c } = info;
  const ziyaret = new Uint8Array(w * h);
  const kuyruk = [0, w - 1, (h - 1) * w, h * w - 1];
  for (const bas of kuyruk) ziyaret[bas] = 1;

  while (kuyruk.length > 0) {
    const i = kuyruk.pop();
    const x = i % w;
    const y = (i - x) / w;
    const o = i * c;
    if (bordoMu(data[o], data[o + 1], data[o + 2])) continue;
    data[o + 3] = 0;
    const komsu = [];
    if (x > 0) komsu.push(i - 1);
    if (x + 1 < w) komsu.push(i + 1);
    if (y > 0) komsu.push(i - w);
    if (y + 1 < h) komsu.push(i + w);
    for (const n of komsu) {
      if (ziyaret[n]) continue;
      ziyaret[n] = 1;
      kuyruk.push(n);
    }
  }

  return sharp(data, { raw: { width: w, height: h, channels: c } }).png();
}

function icoYaz(pngler) {
  const n = pngler.length;
  let ofset = 6 + 16 * n;
  const baslik = Buffer.alloc(ofset);
  baslik.writeUInt16LE(0, 0);
  baslik.writeUInt16LE(1, 2);
  baslik.writeUInt16LE(n, 4);
  const parcalar = [baslik];
  pngler.forEach((png, i) => {
    const meta = png.subarray(16, 24);
    const pw = meta.readUInt32BE(0);
    const ph = meta.readUInt32BE(4);
    const girdi = Buffer.alloc(16);
    girdi.writeUInt8(pw < 256 ? pw : 0, 0);
    girdi.writeUInt8(ph < 256 ? ph : 0, 1);
    girdi.writeUInt16LE(0, 2);
    girdi.writeUInt16LE(1, 4);
    girdi.writeUInt16LE(32, 6);
    girdi.writeUInt32LE(png.length, 8);
    girdi.writeUInt32LE(ofset, 12);
    girdi.copy(baslik, 6 + i * 16);
    parcalar.push(png);
    ofset += png.length;
  });
  return Buffer.concat(parcalar);
}

async function olcek(giris, boyut, { padOran = 0, zemin = null } = {}) {
  const pad = Math.round(boyut * padOran);
  const ic = Math.max(1, boyut - pad * 2);
  const isaret = await giris
    .clone()
    .resize(ic, ic, { fit: "contain", background: { r: 0, g: 0, b: 0, alpha: 0 } })
    .png()
    .toBuffer();
  return sharp({
    create: {
      width: boyut,
      height: boyut,
      channels: 4,
      background: zemin ?? { r: 0, g: 0, b: 0, alpha: 0 },
    },
  })
    .composite([{ input: isaret, left: pad, top: pad }])
    .png()
    .toBuffer();
}

async function main() {
  mkdirSync(LOGO, { recursive: true });
  const seffaf = await seffafKaro();
  const seffafBuf = await seffaf.png().toBuffer();
  writeFileSync(join(LOGO, "karo-seffaf.png"), seffafBuf);

  const acik = await sharp({
    create: {
      width: 1024,
      height: 1024,
      channels: 4,
      background: KAGIT,
    },
  })
    .composite([{ input: seffafBuf }])
    .png()
    .toBuffer();
  writeFileSync(join(LOGO, "karo-acik.png"), acik);
  writeFileSync(join(LOGO, "karo.png"), seffafBuf);

  const icoPng = [];
  for (const b of [16, 32, 48]) {
    const buf = await olcek(sharp(seffafBuf), b, { zemin: BORDO });
    writeFileSync(join(LOGO, `icon-${b}.png`), buf);
    icoPng.push(buf);
  }
  writeFileSync(join(PUBLIC, "favicon.ico"), icoYaz(icoPng));

  const apple = await olcek(sharp(seffafBuf), 180, { zemin: BORDO });
  writeFileSync(join(LOGO, "icon-180.png"), apple);
  writeFileSync(join(PUBLIC, "apple-touch-icon.png"), apple);

  writeFileSync(
    join(LOGO, "icon-192.png"),
    await olcek(sharp(seffafBuf), 192, { zemin: BORDO }),
  );
  writeFileSync(
    join(LOGO, "icon-512.png"),
    await olcek(sharp(seffafBuf), 512, { zemin: BORDO }),
  );
  writeFileSync(
    join(LOGO, "icon-512-maskable.png"),
    await olcek(sharp(seffafBuf), 512, { padOran: 0.18, zemin: BORDO }),
  );

  console.log("logo varliklari yazildi");
}

main().catch((hata) => {
  console.error(hata);
  process.exit(1);
});
