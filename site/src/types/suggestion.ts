import { z } from "zod";
import { ONERI_KATEGORILERI } from "@/types/placeSuggestion";

export type ArabaErisimi =
  | "kolay"
  | "zor"
  | "4x4_gerekli"
  | "aracsiz_ulasilamaz";

export interface PlaceSuggestionFormValues {
  title: string;
  category: string;
  city: string;
  district: string;
  coordinates: {
    lat: number;
    lng: number;
  };
  directions: string; // Adres tarifi (Zorunlu)
  transportation: {
    carAccess: ArabaErisimi;
    walkingDistance: string;
    roadCondition: string;
    publicTransit: string;
  };
  description: string;
  images: File[] | string[];
  submitterEmail: string; // İletişim / Doğrulama için zorunlu
  specialTip?: string; // Yalnızca bu alan opsiyonel (?)
}

export const ARABA_ERISIM_SECENEKLERI: { id: ArabaErisimi; etiket: string }[] = [
  { id: "kolay", etiket: "Kolay (otomobille ulaşılır)" },
  { id: "zor", etiket: "Zor (dikkatli sürüş gerekir)" },
  { id: "4x4_gerekli", etiket: "4x4 gerekli" },
  { id: "aracsiz_ulasilamaz", etiket: "Araçla ulaşılamaz" },
];

export const YOL_DURUMU_SECENEKLERI = [
  { id: "Asfalt", etiket: "Asfalt" },
  { id: "Stabilize", etiket: "Stabilize" },
  { id: "Toprak patika", etiket: "Toprak patika" },
  { id: "Taşlık", etiket: "Taşlık" },
  { id: "Karışık", etiket: "Karışık" },
] as const;

const EPOSTA_DESENI = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const KATEGORI_IDLER = new Set(ONERI_KATEGORILERI.map((k) => k.id));

const koordinatSema = z.custom<{ lat: number; lng: number }>(
  (v) =>
    typeof v === "object" &&
    v !== null &&
    Number.isFinite((v as { lat: number }).lat) &&
    Number.isFinite((v as { lng: number }).lng),
  { message: "Haritadan konum seç." },
);

export const oneriFormSema = z.object({
  title: z
    .string()
    .trim()
    .min(3, "Mekan adı en az 3 karakter olmalı.")
    .max(200, "Mekan adı en fazla 200 karakter olabilir."),
  category: z
    .string()
    .min(1, "Kategori seç.")
    .refine((v) => KATEGORI_IDLER.has(v as never), "Geçerli bir kategori seç."),
  city: z.string().trim().min(2, "Şehir seç."),
  district: z.string().trim().min(2, "İlçe gir."),
  coordinates: koordinatSema,
  directions: z
    .string()
    .trim()
    .min(10, "Adres tarifi en az 10 karakter olmalı.")
    .max(1500, "Adres tarifi en fazla 1500 karakter olabilir."),
  transportation: z.object({
    carAccess: z.enum(["kolay", "zor", "4x4_gerekli", "aracsiz_ulasilamaz"]),
    walkingDistance: z.string().trim().min(2, "Yürüme mesafesi veya süresini yaz."),
    roadCondition: z.string().trim().min(2, "Yol tipini seç."),
    publicTransit: z.string().trim().min(2, "Toplu taşıma durumunu yaz."),
  }),
  description: z
    .string()
    .trim()
    .min(20, "Açıklama en az 20 karakter olmalı.")
    .max(2500, "Açıklama en fazla 2500 karakter olabilir."),
  images: z
    .array(z.custom<File>((v) => typeof File !== "undefined" && v instanceof File))
    .min(1, "En az bir fotoğraf yükle."),
  submitterEmail: z.string().trim().regex(EPOSTA_DESENI, "Geçerli bir e-posta gir."),
  specialTip: z.string().trim().max(500, "Ziyaretçi tüyosu en fazla 500 karakter olabilir.").optional(),
});

export type OneriFormSema = z.infer<typeof oneriFormSema>;

export type CommunityCategory =
  | "gizli_koy"
  | "selale_doga"
  | "butik_kafe"
  | "manzara_tepe"
  | "tarihi_kalinti"
  | "kamp_alani"
  | "diger";

export interface CommunityVisibleFields {
  showDirections: boolean;
  showTransportation: boolean;
  showExactCoordinates: boolean;
  showSpecialTip: boolean;
}

export interface CommunityEditorial {
  historicalContext?: string;
  adminNotes?: string;
  publishedAt: string;
}

export interface CommunityPost {
  id: string;
  slug: string;
  title: string;
  category: CommunityCategory;
  city: string;
  district: string;
  coordinates: {
    lat: number;
    lng: number;
  };
  directions: string;
  transportation: {
    carAccess: string;
    walkingDistance: string;
    roadCondition: string;
  };
  userStory: string;
  specialTip?: string;
  approvedImages: string[];
  submitterEmail: string;
  adminEditorial?: CommunityEditorial;
  visibleFields: CommunityVisibleFields;
  likesCount: number;
  commentsCount: number;
  status: "beklemede" | "onaylandi" | "reddedildi";
}

export interface PostComment {
  id: string;
  postId: string;
  authorName: string;
  content: string;
  createdAt: string;
  status: "yayinda" | "beklemede";
}

export function toggleFieldVisibility(
  current: CommunityVisibleFields,
  field: keyof CommunityVisibleFields,
): CommunityVisibleFields {
  return { ...current, [field]: !current[field] };
}

export function updateAdminContext(
  current: CommunityEditorial | undefined,
  patch: { historicalContext?: string; adminNotes?: string },
): CommunityEditorial {
  return {
    historicalContext: patch.historicalContext ?? current?.historicalContext,
    adminNotes: patch.adminNotes ?? current?.adminNotes,
    publishedAt: current?.publishedAt ?? new Date().toISOString(),
  };
}

export function kategoriGosterimId(kategori: string): string {
  return kategori === "kamp_alani" ? "kamp_karavan" : kategori;
}

