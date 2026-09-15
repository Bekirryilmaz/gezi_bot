import type {
  AlternatifRotalarCevap,
  ApiHataZarfi,
  BolgeProfili,
  GunlukPlanCevap,
  GunlukPlanTalebi,
  RotaCevap,
  RotaTalebi,
  Sehir,
  SehirIstatistikleri,
  YerDetay,
  YerListeCevabi,
  YerOzet,
  VeriDurumu,
  AramaCevabi,
  AramaFiltreDurumu,
  AramaFiltreKatalogu,
  IlceDetayi,
  KamusalYerDetayi,
  KararBaglami,
  KesfetCevabi,
  SehirKapsami,
} from "./types";

export class ApiHatasi extends Error {
  constructor(
    mesaj: string,
    readonly status: number | null,
    readonly durum: Exclude<VeriDurumu, "loading" | "ready">,
    readonly requestId?: string,
    readonly kod?: string,
  ) {
    super(mesaj);
    this.name = "ApiHatasi";
  }
}

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

function hataDurumu(status: number): ApiHatasi["durum"] {
  if (status === 404) return "empty";
  if (status === 409 || status === 422) return "insufficient";
  if ([429, 502, 503, 504].includes(status)) return "unavailable";
  return "error";
}

async function apiHatasiOlustur(yanit: Response, yol: string): Promise<ApiHatasi> {
  let govde: ApiHataZarfi | null = null;
  try {
    govde = (await yanit.json()) as ApiHataZarfi;
  } catch {
    // Sunucu eski/bozuk bir cevap verdiyse de teknik hata bos sonuca donusmez.
  }
  const hata = govde?.hata;
  return new ApiHatasi(
    hata?.mesaj ?? `API isteği başarısız (${yanit.status}): ${yol}`,
    yanit.status,
    hata?.durum ?? hataDurumu(yanit.status),
    hata?.request_id ?? yanit.headers.get("X-Request-ID") ?? undefined,
    hata?.kod,
  );
}

export function apiDurumu(hata: unknown): Exclude<VeriDurumu, "loading" | "ready"> {
  return hata instanceof ApiHatasi ? hata.durum : "error";
}

export function veriDurumuBelirle({
  yukleniyor,
  hata,
  ogeSayisi,
  yetersiz = false,
}: {
  yukleniyor: boolean;
  hata?: unknown;
  ogeSayisi?: number;
  yetersiz?: boolean;
}): VeriDurumu {
  if (yukleniyor) return "loading";
  if (hata) return apiDurumu(hata);
  if (yetersiz) return "insufficient";
  if (ogeSayisi === 0) return "empty";
  return "ready";
}

async function apiGet<T>(yol: string, signal?: AbortSignal): Promise<T> {
  let yanit: Response;
  try {
    yanit = await fetch(`${apiKoku()}${yol}`, {
      signal,
      ...(typeof window === "undefined"
        ? { next: { revalidate: 60 } }
        : { cache: "no-store" }),
    });
  } catch (hata) {
    if (hata instanceof DOMException && hata.name === "AbortError") throw hata;
    throw new ApiHatasi(agHatasiMesaji(hata), null, "unavailable");
  }
  if (!yanit.ok) {
    throw await apiHatasiOlustur(yanit, yol);
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

/** Ana sayfa kanit bandi: sayilar elle yazilmaz (yon.md 3.8). */
export async function istatistikleriGetir(
  sehirAnahtari: string,
): Promise<SehirIstatistikleri> {
  return apiGet<SehirIstatistikleri>(`/sehirler/${sehirAnahtari}/istatistikler`);
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
      headers: {
        "Content-Type": "application/json",
        "Idempotency-Key": globalThis.crypto.randomUUID(),
      },
      body: JSON.stringify(govde),
    });
  } catch (hata) {
    throw new ApiHatasi(agHatasiMesaji(hata), null, "unavailable");
  }
  if (!yanit.ok) {
    throw await apiHatasiOlustur(yanit, yol);
  }
  return yanit.json() as Promise<T>;
}

export async function kesfetDegerlendir(
  talep: {
    sorgu: string;
    baglam: KararBaglami;
    arama?: { ilce_id?: string | null; tur?: string | null };
    hedef_sayi?: number;
    haric_yerler?: string[];
  },
  signal?: AbortSignal,
): Promise<KesfetCevabi> {
  let yanit: Response;
  try {
    yanit = await fetch(`${apiKoku()}/v1/kesfet/degerlendir`, {
      method: "POST",
      signal,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(talep),
      cache: "no-store",
    });
  } catch (hata) {
    if (hata instanceof DOMException && hata.name === "AbortError") throw hata;
    throw new ApiHatasi(agHatasiMesaji(hata), null, "unavailable");
  }
  if (!yanit.ok) throw await apiHatasiOlustur(yanit, "/v1/kesfet/degerlendir");
  return yanit.json() as Promise<KesfetCevabi>;
}

export async function sehirKapsaminiGetir(sehir: string): Promise<SehirKapsami> {
  return apiGet<SehirKapsami>(`/v1/sehirler/${sehir}/kapsam`);
}

export async function ilceDetayiniGetir(
  sehir: string,
  ilce: string,
): Promise<IlceDetayi> {
  return apiGet<IlceDetayi>(`/v1/sehirler/${sehir}/ilceler/${ilce}`);
}

export async function kamusalYerDetayiGetir(yerId: string): Promise<KamusalYerDetayi> {
  return apiGet<KamusalYerDetayi>(`/v1/yerler/${yerId}`);
}

export async function kamusalYerDetayiniDegerlendir(
  yerId: string,
  baglam: KararBaglami,
  signal?: AbortSignal,
): Promise<KamusalYerDetayi> {
  const yanit = await fetch(
    `${apiKoku()}/v1/yerler/${encodeURIComponent(yerId)}/degerlendir`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(baglam),
      signal,
    },
  );
  if (!yanit.ok) throw await apiHatasiOlustur(yanit, `/v1/yerler/${yerId}/degerlendir`);
  return yanit.json() as Promise<KamusalYerDetayi>;
}

export async function gunlukPlanOlustur(
  talep: GunlukPlanTalebi,
): Promise<GunlukPlanCevap> {
  return rotaPost<GunlukPlanCevap>("/v1/gunluk-planlar", talep);
}

/** @deprecated Public UI tek gunluk akisa gecmistir; sunucu bu uclari 410 ile kapatir. */
export async function rotaOlustur(talep: RotaTalebi): Promise<RotaCevap> {
  return rotaPost<RotaCevap>("/rotalar/olustur", talep);
}

/** @deprecated Public UI'da alternatif/konaklama devam adimi yoktur. */
export async function rotaAlternatifleriOlustur(
  talep: RotaTalebi,
): Promise<AlternatifRotalarCevap> {
  return rotaPost<AlternatifRotalarCevap>("/rotalar/olustur-alternatifler", talep);
}

/** @deprecated Tarihsel uyumluluk; public akista cagrilmaz. */
export async function konaklamaBolgesiOner(rotaId: string): Promise<RotaCevap> {
  return rotaPost<RotaCevap>(`/rotalar/${rotaId}/konaklama-bolgesi-oner`, {});
}

export function apiTabanUrl(): string {
  return apiKoku();
}

export async function aramaGetir(
  q: string,
  filtreler: AramaFiltreDurumu,
  secenekler: { limit?: number; cursor?: string; signal?: AbortSignal } = {},
): Promise<AramaCevabi> {
  const params = new URLSearchParams({ q, sehir: filtreler.sehir });
  if (filtreler.ilce) params.set("ilce", filtreler.ilce);
  if (filtreler.tur) params.set("tur", filtreler.tur);
  for (const kod of filtreler.zorunluKosullar) params.append("zorunlu_kosul", kod);
  for (const kod of filtreler.tercihler) params.append("tercih", kod);
  params.set("limit", String(secenekler.limit ?? 20));
  if (secenekler.cursor) params.set("cursor", secenekler.cursor);
  return apiGet<AramaCevabi>(`/v1/arama?${params}`, secenekler.signal);
}

export async function aramaFiltreleriniGetir(
  sehir = "samsun",
  signal?: AbortSignal,
): Promise<AramaFiltreKatalogu> {
  return apiGet<AramaFiltreKatalogu>(
    `/v1/arama/filtreler?${new URLSearchParams({ sehir })}`,
    signal,
  );
}
