/**
 * geoBoundaries TUR ADM2 (simplified) dosyasını mevcut il poligonlarıyla
 * eşleştirip public/data/geo/districts/[il-slug].geojson üretir.
 * Samsun için eldeki yüksek çözünürlüklü samsun-ilceler.geojson korunur.
 */
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const KOK = path.join(__dirname, "..");
const ADM2 = path.join(__dirname, "tur-adm2-simplified.geojson");
const ILLER = path.join(KOK, "public", "data", "turkey-provinces.geojson");
const CIKTI = path.join(KOK, "public", "data", "geo", "districts");
const SAMSUN_KAYNAK = path.join(KOK, "public", "data", "samsun-ilceler.geojson");

function slug(ad) {
  return String(ad)
    .toLocaleLowerCase("tr-TR")
    .replaceAll("ı", "i")
    .replaceAll("ğ", "g")
    .replaceAll("ü", "u")
    .replaceAll("ş", "s")
    .replaceAll("ö", "o")
    .replaceAll("ç", "c")
    .replaceAll("â", "a")
    .replaceAll("î", "i")
    .replaceAll("û", "u")
    .replaceAll(" ", "-")
    .replaceAll("'", "")
    .replaceAll(".", "");
}

function noktaHalkada(x, y, halka) {
  let icerde = false;
  for (let i = 0, j = halka.length - 1; i < halka.length; j = i++) {
    const xi = halka[i][0];
    const yi = halka[i][1];
    const xj = halka[j][0];
    const yj = halka[j][1];
    const keser =
      yi > y !== yj > y && x < ((xj - xi) * (y - yi)) / (yj - yi + 1e-12) + xi;
    if (keser) icerde = !icerde;
  }
  return icerde;
}

function noktaPoligonda(x, y, halkalar) {
  if (!halkalar?.length) return false;
  if (!noktaHalkada(x, y, halkalar[0])) return false;
  for (let i = 1; i < halkalar.length; i++) {
    if (noktaHalkada(x, y, halkalar[i])) return false;
  }
  return true;
}

function noktaGeometride(x, y, geom) {
  if (!geom) return false;
  if (geom.type === "Polygon") return noktaPoligonda(x, y, geom.coordinates);
  if (geom.type === "MultiPolygon") {
    return geom.coordinates.some((poly) => noktaPoligonda(x, y, poly));
  }
  return false;
}

function temsilNoktasi(geom) {
  if (!geom) return null;
  if (geom.type === "Polygon") {
    const halka = geom.coordinates[0];
    return halka[Math.floor(halka.length / 2)];
  }
  if (geom.type === "MultiPolygon") {
    const halka = geom.coordinates[0][0];
    return halka[Math.floor(halka.length / 2)];
  }
  return null;
}

function merkezNokta(geom) {
  let halka = null;
  if (geom?.type === "Polygon") halka = geom.coordinates[0];
  if (geom?.type === "MultiPolygon") halka = geom.coordinates[0][0];
  if (!halka?.length) return null;
  let sx = 0;
  let sy = 0;
  const n = halka.length - 1;
  for (let i = 0; i < n; i++) {
    sx += halka[i][0];
    sy += halka[i][1];
  }
  return [sx / n, sy / n];
}

function ilMerkezi(feature) {
  return merkezNokta(feature.geometry);
}

function main() {
  const adm2 = JSON.parse(fs.readFileSync(ADM2, "utf8"));
  const iller = JSON.parse(fs.readFileSync(ILLER, "utf8"));
  const ilMerkezleri = iller.features.map((f) => ({
    f,
    c: ilMerkezi(f),
  }));

  const kova = new Map();
  let eslesmeyen = 0;

  for (const feat of adm2.features) {
    const ad = feat.properties?.shapeName;
    if (!ad) continue;
    const adaylar = [merkezNokta(feat.geometry), temsilNoktasi(feat.geometry)].filter(
      Boolean,
    );
    let il = null;
    for (const [x, y] of adaylar) {
      il = iller.features.find((p) => noktaGeometride(x, y, p.geometry));
      if (il) break;
    }
    if (!il) {
      const c = adaylar[0];
      if (c) {
        let enYakin = null;
        let en = Infinity;
        for (const { f, c: mc } of ilMerkezleri) {
          if (!mc) continue;
          const d = (c[0] - mc[0]) ** 2 + (c[1] - mc[1]) ** 2;
          if (d < en) {
            en = d;
            enYakin = f;
          }
        }
        il = enYakin;
      }
    }
    if (!il) {
      eslesmeyen += 1;
      continue;
    }
    const ilSlug = il.properties.slug || slug(il.properties.name);
    if (!kova.has(ilSlug)) kova.set(ilSlug, []);
    const ilceSlug = slug(ad);
    kova.get(ilSlug).push({
      type: "Feature",
      properties: { id: ilceSlug, name: ad, slug: ilceSlug },
      geometry: feat.geometry,
    });
  }

  fs.mkdirSync(CIKTI, { recursive: true });
  for (const [ilSlug, features] of kova) {
    if (ilSlug === "samsun") continue;
    const gorulen = new Map();
    const tekil = features.map((f) => {
      let id = f.properties.id;
      if (gorulen.has(id)) {
        const n = gorulen.get(id) + 1;
        gorulen.set(id, n);
        id = `${id}-${n}`;
        f.properties.id = id;
        f.properties.slug = id;
      } else {
        gorulen.set(id, 1);
      }
      return f;
    });
    fs.writeFileSync(
      path.join(CIKTI, `${ilSlug}.geojson`),
      JSON.stringify({ type: "FeatureCollection", features: tekil }),
    );
  }

  fs.copyFileSync(SAMSUN_KAYNAK, path.join(CIKTI, "samsun.geojson"));

  const ozet = [...kova.entries()]
    .map(([k, v]) => `${k}:${v.length}`)
    .sort()
    .join(" ");
  console.log(`iller=${kova.size} eslesmeyen=${eslesmeyen}`);
  console.log(ozet);
}

main();
