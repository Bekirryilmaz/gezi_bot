export type PlaceSuggestionCategory =
  | "gizli_koy"
  | "selale_doga"
  | "butik_kafe"
  | "manzara_tepe"
  | "tarihi_kalinti"
  | "kamp_karavan"
  | "diger";

export type PlaceSuggestionStatus = "beklemede" | "onaylandi" | "reddedildi";

export interface PlaceSuggestion {
  id: string;
  title: string;
  category: PlaceSuggestionCategory;
  city: string;
  district: string;
  description: string;
  specialTip?: string;
  coordinates: {
    lat: number;
    lng: number;
  };
  images: string[];
  submitter: {
    name?: string;
    email: string;
  };
  status: PlaceSuggestionStatus;
  createdAt: string;
}

export type Oneri = PlaceSuggestion;

export const ONERI_KATEGORILERI: {
  id: PlaceSuggestionCategory;
  etiket: string;
  ikon: string;
}[] = [
  { id: "gizli_koy", ikon: "🌊", etiket: "Gizli Koy / Plaj" },
  { id: "selale_doga", ikon: "🌲", etiket: "Şelale & Doğa Alanı" },
  { id: "butik_kafe", ikon: "☕", etiket: "Butik Kafe & Lezzet Durağı" },
  { id: "manzara_tepe", ikon: "🌄", etiket: "Manzara Tepesi & Seyir Noktası" },
  { id: "tarihi_kalinti", ikon: "🏛️", etiket: "Tarihi Kalıntı / Antik Mekan" },
  { id: "kamp_karavan", ikon: "⛺", etiket: "Kamp & Karavan Noktası" },
  { id: "diger", ikon: "📍", etiket: "Diğer Keşif Noktası" },
];

export const MEKAN_ONERI_KATEGORILERI = ONERI_KATEGORILERI;
