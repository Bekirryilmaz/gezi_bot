export type EventCategory =
  | "gastronomi"
  | "kultur_sanat"
  | "muzik"
  | "doga_yayla"
  | "geleneksel";

export type TicketOrAccess = "Ucretsiz" | "Biletli" | "Katılıma Açık";

export interface RegionalEvent {
  id: string;
  title: string;
  citySlug: string;
  cityName: string;
  district?: string;
  category: EventCategory;
  startDate: string;
  endDate: string;
  summary: string;
  badge: string;
  imageUrl?: string;
  ticketOrAccess: TicketOrAccess;
}

export const KATEGORI_ETIKET: Record<EventCategory, string> = {
  gastronomi: "Gastronomi & Hasat",
  kultur_sanat: "Kültür & Sanat",
  muzik: "Müzik & Sahne",
  doga_yayla: "Doğa & Yayla",
  geleneksel: "Geleneksel Şenlikler",
};
