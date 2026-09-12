/**
 * Ana sayfa "Sehri uc yoldan oku" kart plakalari (16:10).
 *
 * Kaynak yine plan/tasarim/hero-kaynak (kunye: plan/tasarim/gorsel-kunye.md).
 * Bunlar ATMOSFER plakasidir; belirli bir yerin fotografi gibi sunulmaz,
 * dekoratiftir (alt=""). Duotone YOK — yon.md 1.5: duotone yalniz hero'da.
 */
import { mkdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import sharp from "sharp";

const KOK = join(dirname(fileURLToPath(import.meta.url)), "..", "..");
const KAYNAK = join(KOK, "plan", "tasarim", "hero-kaynak");
const CIKTI = join(KOK, "site", "public", "plaka");

const GENISLIK = 1200;
const YUKSEKLIK = 750;

const PLAKALAR = [
  { ad: "kesif", kaynak: "plaka-05.jpg" },
  { ad: "bolge", kaynak: "plaka-04.jpg" },
  { ad: "rota", kaynak: "plaka-02.jpg" },
];

mkdirSync(CIKTI, { recursive: true });

for (const plaka of PLAKALAR) {
  const taban = sharp(join(KAYNAK, plaka.kaynak)).resize(GENISLIK, YUKSEKLIK, {
    fit: "cover",
    position: "centre",
  });
  const hedef = join(CIKTI, plaka.ad);
  await taban
    .clone()
    .avif({ quality: 46, effort: 6, chromaSubsampling: "4:2:0" })
    .toFile(`${hedef}.avif`);
  await taban
    .clone()
    .webp({ quality: 62, effort: 6, smartSubsample: true })
    .toFile(`${hedef}.webp`);
  console.log(
    `${plaka.ad}: avif ${(statSync(`${hedef}.avif`).size / 1024).toFixed(1)} KB · ` +
      `webp ${(statSync(`${hedef}.webp`).size / 1024).toFixed(1)} KB`,
  );
}
