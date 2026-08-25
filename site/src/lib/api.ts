import type {
  AlternatifRotalarCevap,
  BolgeProfili,
  RotaCevap,
  RotaTalebi,
  Sehir,
  YerDetay,
  YerListeCevabi,
  YerOzet,
} from "./types";

function apiKoku(): string {
  // Sunucu tarafinda dogrudan FastAPI'ye git.
  // Tarayicida ayni origin uzerinden /backend vekili kullan — CORS ve
  // "Failed to fetch" (API kapali / farkli host) sorununu azaltir.
  if (typeof window === "undefined") {
    return process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8125";
  }
  return "/backend";
}

function agHatasiMesaji(hata: unknown): string {
  const metin = hata instanceof Error ? hata.message : String(hata);
  if (
    metin === "Failed to fetch" ||
    metin === "Load failed" ||
    metin === "NetworkError when attempting to fetch resource."
  ) {
    return (
      "API'ye bağlanılamadı. PostgreSQL ve FastAPI'nin çalıştığından emin ol " +
      "(repo kökündeki calis.txt). Site açık kalsa bile rota isteği API olmadan gidemez."
    );
  }
  return metin;
}

async function apiGet<T>(yol: string): Promise<T> {
  let yanit: Response;
  try {
    yanit = await fetch(`${apiKoku()}${yol}`, {
      ...(typeof window === "undefined" ? { next: { revalidate: 60 } } : { cache: "no-store" }),
    });
  } catch (hata) {
    throw new Error(agHatasiMesaji(hata));
  }
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
    sadeceKesif?: boolean;
  } = {},
): Promise<YerListeCevabi> {
  const params = new URLSearchParams();
  if (secenekler.anaKategori) params.set("ana_kategori", secenekler.anaKategori);
  if (secenekler.altKategori) params.set("alt_kategori", secenekler.altKategori);
  params.set("limit", String(secenekler.limit ?? 48));
  params.set("offset", String(secenekler.offset ?? 0));
  if (secenekler.sadeceKesif === false) params.set("sadece_kesif", "false");
  const cevap = await apiGet<YerListeCevabi | YerOzet[]>(
    `/sehirler/${sehirAnahtari}/yerler?${params}`,
  );
  if (Array.isArray(cevap)) {
    return { yerler: cevap, toplam_sayi: cevap.length };
  }
  return cevap;
}

export async function yerDetayiGetir(yerId: string): Promise<YerDetay> {
  return apiGet<YerDetay>(`/yerler/${yerId}`);
}

export async function bolgeleriGetir(sehirAnahtari: string): Promise<BolgeProfili[]> {
  return apiGet<BolgeProfili[]>(`/sehirler/${sehirAnahtari}/bolgeler`);
}

async function rotaPost<T>(yol: string, govde: unknown): Promise<T> {
  let yanit: Response;
  try {
    yanit = await fetch(`${apiKoku()}${yol}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(govde),
    });
  } catch (hata) {
    throw new Error(agHatasiMesaji(hata));
  }
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
  return apiKoku();
}
