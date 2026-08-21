import type {
  AlternatifRotalarCevap,
  BolgeProfili,
  RotaCevap,
  RotaTalebi,
  Sehir,
  YerDetay,
  YerOzet,
} from "./types";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";

async function apiGet<T>(yol: string): Promise<T> {
  const yanit = await fetch(`${API_URL}${yol}`, {
    next: { revalidate: 60 },
  });
  if (!yanit.ok) {
    throw new Error(`API hatası (${yanit.status}): ${yol}`);
  }
  return yanit.json() as Promise<T>;
}

export async function sehirleriGetir(): Promise<Sehir[]> {
  return apiGet<Sehir[]>("/sehirler");
}

export async function yerleriGetir(
  sehirAnahtari: string,
  secenekler: {
    anaKategori?: string;
    altKategori?: string;
    limit?: number;
    offset?: number;
  } = {},
): Promise<YerOzet[]> {
  const params = new URLSearchParams();
  if (secenekler.anaKategori) params.set("ana_kategori", secenekler.anaKategori);
  if (secenekler.altKategori) params.set("alt_kategori", secenekler.altKategori);
  params.set("limit", String(secenekler.limit ?? 48));
  params.set("offset", String(secenekler.offset ?? 0));
  return apiGet<YerOzet[]>(`/sehirler/${sehirAnahtari}/yerler?${params}`);
}

export async function yerDetayiGetir(yerId: string): Promise<YerDetay> {
  return apiGet<YerDetay>(`/yerler/${yerId}`);
}

export async function bolgeleriGetir(sehirAnahtari: string): Promise<BolgeProfili[]> {
  return apiGet<BolgeProfili[]>(`/sehirler/${sehirAnahtari}/bolgeler`);
}

async function rotaPost<T>(yol: string, govde: unknown): Promise<T> {
  const yanit = await fetch(`${API_URL}${yol}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(govde),
  });
  if (!yanit.ok) {
    const metin = await yanit.text();
    throw new Error(metin || `İstek başarısız (${yanit.status})`);
  }
  return yanit.json() as Promise<T>;
}

export async function rotaOlustur(talep: RotaTalebi): Promise<RotaCevap> {
  return rotaPost<RotaCevap>("/rotalar/olustur", talep);
}

export async function rotaAlternatifleriOlustur(
  talep: RotaTalebi,
): Promise<AlternatifRotalarCevap> {
  return rotaPost<AlternatifRotalarCevap>("/rotalar/olustur-alternatifler", talep);
}

export async function konaklamaBolgesiOner(rotaId: string): Promise<RotaCevap> {
  return rotaPost<RotaCevap>(`/rotalar/${rotaId}/konaklama-bolgesi-oner`, {});
}

export function apiTabanUrl(): string {
  return API_URL;
}
