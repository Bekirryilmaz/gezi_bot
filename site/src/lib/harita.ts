import type { BolgeProfili } from "./types";

/** OpenFreeMap Positron — anahtarsiz vektor karo stili. */
export const OFM_STIL_URL = "https://tiles.openfreemap.org/styles/positron";

export type HaritaIsareti = {
  id: string;
  ad: string;
  enlem: number;
  boylam: number;
  ozet: string | null;
  href: string;
};

export type HaritaKutu = {
  minE: number;
  maxE: number;
  minB: number;
  maxB: number;
};

export type HaritaKamera = {
  center: [number, number];
  zoom: number;
  pitch: number;
  bearing: number;
};

export function haritaIsaretleriniKur(
  sehirAnahtari: string,
  bolgeler: BolgeProfili[],
): HaritaIsareti[] {
  const liste: HaritaIsareti[] = [];
  for (const b of bolgeler) {
    if (!b.ilce_mi) continue;
    if (b.enlem == null || b.boylam == null) continue;
    const ozet = b.duygu_ozeti ?? b.tanitim_metni;
    liste.push({
      id: b.bolge_adi,
      ad: b.bolge_adi,
      enlem: b.enlem,
      boylam: b.boylam,
      ozet: ozet ? ozet.slice(0, 180) : null,
      href: `/sehir/${sehirAnahtari}/bolgeler`,
    });
  }
  return liste.toSorted((a, b) => a.boylam - b.boylam || a.enlem - b.enlem);
}

export function haritaMerkeziniBul(
  sehir: { merkez_enlem: number | null; merkez_boylam: number | null } | undefined,
  bolgeler: BolgeProfili[],
  isaretler: HaritaIsareti[],
): { enlem: number; boylam: number } {
  if (sehir?.merkez_enlem != null && sehir.merkez_boylam != null) {
    return { enlem: sehir.merkez_enlem, boylam: sehir.merkez_boylam };
  }
  const sehirBolgesi = bolgeler.find(
    (b) => !b.ilce_mi && b.enlem != null && b.boylam != null,
  );
  if (sehirBolgesi?.enlem != null && sehirBolgesi.boylam != null) {
    return { enlem: sehirBolgesi.enlem, boylam: sehirBolgesi.boylam };
  }
  if (isaretler.length === 0) return { enlem: 0, boylam: 0 };
  let e = 0;
  let b = 0;
  for (const i of isaretler) {
    e += i.enlem;
    b += i.boylam;
  }
  return { enlem: e / isaretler.length, boylam: b / isaretler.length };
}

export function haritaKutusu(
  isaretler: HaritaIsareti[],
  merkez: { enlem: number; boylam: number },
): HaritaKutu {
  let minE = merkez.enlem;
  let maxE = merkez.enlem;
  let minB = merkez.boylam;
  let maxB = merkez.boylam;
  for (const i of isaretler) {
    if (i.enlem < minE) minE = i.enlem;
    if (i.enlem > maxE) maxE = i.enlem;
    if (i.boylam < minB) minB = i.boylam;
    if (i.boylam > maxB) maxB = i.boylam;
  }
  const padE = Math.max((maxE - minE) * 0.14, 0.12);
  const padB = Math.max((maxB - minB) * 0.14, 0.12);
  return {
    minE: minE - padE,
    maxE: maxE + padE,
    minB: minB - padB,
    maxB: maxB + padB,
  };
}

export function haritaProje(
  kutu: HaritaKutu,
  enlem: number,
  boylam: number,
): { x: number; y: number } {
  const genB = kutu.maxB - kutu.minB || 1;
  const genE = kutu.maxE - kutu.minE || 1;
  return {
    x: ((boylam - kutu.minB) / genB) * 100,
    y: (1 - (enlem - kutu.minE) / genE) * 100,
  };
}

function lerp(a: number, b: number, t: number): number {
  return a + (b - a) * t;
}

function yolOrnekle(isaretler: HaritaIsareti[]): HaritaIsareti[] {
  if (isaretler.length <= 6) return isaretler;
  const n = isaretler.length - 1;
  const adimlar = [0, 0.2, 0.4, 0.6, 0.8, 1];
  const secilen: HaritaIsareti[] = [];
  const gorulen = new Set<string>();
  for (const a of adimlar) {
    const i = Math.round(n * a);
    const oge = isaretler[i];
    if (!oge || gorulen.has(oge.id)) continue;
    gorulen.add(oge.id);
    secilen.push(oge);
  }
  return secilen;
}

export function haritaScrubNoktasi(
  isaretler: HaritaIsareti[],
  merkez: { enlem: number; boylam: number },
  t: number,
): HaritaKamera {
  const ornek = yolOrnekle(isaretler);
  const yol: Array<{
    enlem: number;
    boylam: number;
    zoom: number;
    pitch: number;
    bearing: number;
  }> = [
    {
      enlem: merkez.enlem,
      boylam: merkez.boylam,
      zoom: 8.45,
      pitch: 22,
      bearing: -20,
    },
  ];
  for (let i = 0; i < ornek.length; i++) {
    const o = ornek[i];
    if (!o) continue;
    yol.push({
      enlem: o.enlem,
      boylam: o.boylam,
      zoom: 10.15 + (i % 3) * 0.12,
      pitch: 28 + (i % 2) * 6,
      bearing: -16 + i * 4,
    });
  }
  const son = t * Math.max(yol.length - 1, 0);
  const i = Math.min(Math.floor(son), yol.length - 1);
  const j = Math.min(i + 1, yol.length - 1);
  const a = yol[i];
  const b = yol[j];
  if (!a || !b) {
    return {
      center: [merkez.boylam, merkez.enlem],
      zoom: 8.45,
      pitch: 22,
      bearing: -20,
    };
  }
  const f = son - i;
  return {
    center: [lerp(a.boylam, b.boylam, f), lerp(a.enlem, b.enlem, f)],
    zoom: lerp(a.zoom, b.zoom, f),
    pitch: lerp(a.pitch, b.pitch, f),
    bearing: lerp(a.bearing, b.bearing, f),
  };
}
