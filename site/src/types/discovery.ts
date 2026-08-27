export type KesifKategorisi = "doga" | "tarih" | "sahil" | "kultur";

export interface DistrictDetail {
  id: string;
  name: string;
  slug: string;
  coordinates: [number, number]; // [lat, lng]
  vibe: string; // kısa rozet
  highlights: {
    attractions: Array<{
      name: string;
      category: KesifKategorisi;
      desc: string;
      image: string;
    }>;
    gastronomy: Array<{ name: string; desc: string; image: string }>;
    travelTips: {
      tip: string;
      bestTimeToVisit: string;
      atmosphere: string;
      transport: string;
    };
  };
}
