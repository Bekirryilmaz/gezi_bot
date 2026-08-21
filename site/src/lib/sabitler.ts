export const ANA_KATEGORILER = [
  { deger: "gezilecek_yer", etiket: "Gezilecek yerler" },
  { deger: "yeme_icme", etiket: "Yeme & içme" },
  { deger: "konaklama", etiket: "Konaklama" },
] as const;

export const ALT_KATEGORI_ETIKETLERI: Record<string, string> = {
  tarihi_kulturel: "Tarihi & kültürel",
  doga_manzara: "Doğa & manzara",
  plaj_su: "Plaj & su",
  eglence_aktivite: "Eğlence",
  gece_hayati: "Gece hayatı",
  alisveris: "Alışveriş",
  spor_doga_yuruyus: "Spor & yürüyüş",
  dini_manevi: "Dini & manevi",
  fotograf_noktasi: "Fotoğraf noktası",
  otel: "Otel",
  pansiyon_apart: "Pansiyon / apart",
  kamp_karavan: "Kamp & karavan",
  hostel: "Hostel",
  ev_kiralama: "Ev kiralama",
  restoran_lokanta: "Restoran",
  deniz_mahsulleri: "Deniz mahsulleri",
  kebap_izgara: "Kebap & ızgara",
  ev_yemekleri_esnaf: "Ev yemekleri",
  fine_dining_romantik: "Fine dining",
  sokak_lezzeti: "Sokak lezzeti",
  kafe: "Kafe",
  tatli_pastane: "Tatlı & pastane",
  kahve_uzmanlik: "Kahve",
  meyhane_bar: "Meyhane & bar",
  cay_bahcesi: "Çay bahçesi",
};

export const DENEYIM_EKSENLERI = [
  { deger: "tarihi_kulturel_puani", etiket: "Tarih & kültür" },
  { deger: "eglence_puani", etiket: "Eğlence" },
  { deger: "doga_macera_puani", etiket: "Doğa & macera" },
  { deger: "gastronomi_puani", etiket: "Gastronomi" },
  { deger: "gece_hayati_puani", etiket: "Gece hayatı" },
  { deger: "rahatlatici_sakin_puani", etiket: "Sakin & rahat" },
] as const;

export function kategoriEtiketi(ana: string): string {
  return ANA_KATEGORILER.find((k) => k.deger === ana)?.etiket ?? ana;
}

export function altKategoriEtiketi(alt: string): string {
  return ALT_KATEGORI_ETIKETLERI[alt] ?? alt.replaceAll("_", " ");
}

export function duyguEtiketi(etiket: string | null | undefined): string {
  if (etiket === "olumlu") return "Olumlu";
  if (etiket === "olumsuz") return "Olumsuz";
  if (etiket === "notr") return "Nötr";
  return "Belirsiz";
}
