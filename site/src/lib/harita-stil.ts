/**
 * OpenFreeMap Positron JSON'unu marka paletine boyar.
 * MapLibre CSS degiskeni okumaz — yon.md 1.2 kilit hex'leri.
 */
export const HARITA_PALET = {
  kagit: "#F4EFE7",
  tuz: "#FBF8F3",
  kagitKoyu: "#EBE3D6",
  ink: "#142126",
  bordo: "#6C0000",
  samandira: "#D6402C",
  deniz: "#0A4D5C",
  su: "#D4DCDB",
  halo: "#FBF8F3",
} as const;

type StilKatmani = {
  id?: string;
  type?: string;
  source?: string;
  paint?: Record<string, unknown>;
  layout?: Record<string, unknown>;
};

type Stil = {
  layers?: StilKatmani[];
  sources?: Record<string, unknown>;
  [k: string]: unknown;
};

function renkMi(deger: unknown): deger is string {
  if (typeof deger !== "string") return false;
  return (
    deger.startsWith("#") ||
    deger.startsWith("rgb") ||
    deger.startsWith("hsl") ||
    deger === "white" ||
    deger === "black"
  );
}

function katmanRengi(id: string, anahtar: string): string {
  if (anahtar.includes("halo")) return HARITA_PALET.halo;
  if (id === "background") return HARITA_PALET.kagit;
  if (id.startsWith("water") || id.includes("waterway")) {
    if (anahtar.startsWith("text")) return HARITA_PALET.deniz;
    return HARITA_PALET.su;
  }
  if (id.startsWith("boundary")) return "rgba(108, 0, 0, 0.28)";
  if (
    id.includes("label") ||
    id.startsWith("label_") ||
    anahtar.startsWith("text-color")
  ) {
    return HARITA_PALET.ink;
  }
  if (
    id.includes("park") ||
    id.includes("wood") ||
    id.includes("landcover") ||
    id.includes("landuse")
  ) {
    return HARITA_PALET.kagitKoyu;
  }
  if (id.includes("building")) return HARITA_PALET.tuz;
  if (id.includes("casing") || id.includes("outline")) return HARITA_PALET.kagitKoyu;
  if (
    id.includes("highway") ||
    id.includes("road") ||
    id.includes("railway") ||
    id.includes("aeroway") ||
    id.includes("pier")
  ) {
    return HARITA_PALET.tuz;
  }
  if (anahtar.includes("outline")) return HARITA_PALET.kagitKoyu;
  return HARITA_PALET.kagit;
}

function boyaIfade(id: string, anahtar: string, deger: unknown): unknown {
  if (renkMi(deger)) return katmanRengi(id, anahtar);
  if (Array.isArray(deger)) {
    return deger.map((parca) => boyaIfade(id, anahtar, parca));
  }
  return deger;
}

export function boyaHaritaStili(girdi: unknown): Stil {
  const stil = (girdi ?? {}) as Stil;
  const kaynaklar = { ...(stil.sources ?? {}) };
  delete kaynaklar.ne2_shaded;
  stil.sources = kaynaklar;

  const katmanlar = Array.isArray(stil.layers) ? stil.layers : [];
  stil.layers = katmanlar.flatMap((katman) => {
    if (katman.source === "ne2_shaded") return [];
    const id = String(katman.id ?? "");
    const paint = katman.paint ? { ...katman.paint } : {};
    for (const anahtar of Object.keys(paint)) {
      if (
        anahtar.includes("color") ||
        anahtar.includes("halo") ||
        anahtar.includes("outline")
      ) {
        paint[anahtar] = boyaIfade(id, anahtar, paint[anahtar]);
      }
    }
    if (id === "background") paint["background-color"] = HARITA_PALET.kagit;
    return [{ ...katman, paint }];
  });
  return stil;
}
