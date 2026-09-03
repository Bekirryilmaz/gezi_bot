import type { Feature, FeatureCollection } from "geojson";
import type { CityDetail } from "@/types/city";
import type { DistrictDetail } from "@/types/discovery";
import { SAMSUN_ILCELERI } from "@/data/districts";

export function ilceGeoYolu(sehirSlug: string): string {
  return `/data/geo/districts/${sehirSlug}.geojson`;
}

function halkaMerkezi(halka: number[][]): [number, number] | null {
  if (!halka?.length) return null;
  let sx = 0;
  let sy = 0;
  const n = Math.max(halka.length - 1, 1);
  for (let i = 0; i < n; i++) {
    sx += halka[i][0];
    sy += halka[i][1];
  }
  return [sy / n, sx / n];
}

export function geometriMerkezi(feature: Feature): [number, number] {
  const geom = feature.geometry;
  if (geom?.type === "Polygon") {
    return halkaMerkezi(geom.coordinates[0] as number[][]) ?? [39, 35];
  }
  if (geom?.type === "MultiPolygon") {
    return halkaMerkezi(geom.coordinates[0][0] as number[][]) ?? [39, 35];
  }
  return [39, 35];
}

function jenerikIlce(
  id: string,
  name: string,
  slug: string,
  coordinates: [number, number],
  sehir: CityDetail,
): DistrictDetail {
  return {
    id,
    name,
    slug,
    coordinates,
    vibe: `${sehir.name} keşif durağı`,
    highlights: {
      attractions: [
        {
          name: `${name} merkez`,
          category: "kultur",
          desc: `${sehir.name}’nin ${name} ilçesi. Haritada sınırı seçerek keşfe başlayın.`,
          image: sehir.coverImage,
        },
      ],
      gastronomy: [],
      travelTips: {
        tip: `${name} için yerel durakları yerinde sorun; merkezden ilçe dolmuşları en pratik bağ.`,
        bestTimeToVisit: "İlkbahar ve sonbahar.",
        atmosphere: sehir.region,
        transport: "İlçe dolmuşu veya özel araç.",
      },
    },
  };
}

export function ilceleriGeojsonDan(
  geo: FeatureCollection,
  sehir: CityDetail,
): DistrictDetail[] {
  const samsunHarita =
    sehir.slug === "samsun"
      ? new Map(SAMSUN_ILCELERI.map((i) => [i.id, i]))
      : null;

  const liste = geo.features.flatMap((feature) => {
    const p = feature.properties;
    if (!p || typeof p !== "object") return [];
    const id = typeof p.id === "string" ? p.id : "";
    const name = typeof p.name === "string" ? p.name : "";
    const slug = typeof p.slug === "string" ? p.slug : id;
    if (!id || !name) return [];
    const hazir = samsunHarita?.get(id);
    if (hazir) return [hazir];
    return [jenerikIlce(id, name, slug, geometriMerkezi(feature), sehir)];
  });

  return liste.sort((a, b) => a.name.localeCompare(b.name, "tr"));
}

export function varsayilanIlce(
  ilceler: DistrictDetail[],
  sehirSlug: string,
): DistrictDetail | undefined {
  if (!ilceler.length) return undefined;
  if (sehirSlug === "samsun") {
    return ilceler.find((i) => i.id === "ilkadim") ?? ilceler[0];
  }
  return (
    ilceler.find((i) => /merkez/i.test(i.name) || i.slug === sehirSlug) ??
    ilceler[0]
  );
}
