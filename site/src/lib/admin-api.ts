export type AdminKimlik = {
  id: string;
  eposta: string;
  gorunen_ad: string;
  roller: string[];
  yetkiler: string[];
  csrf_token?: string | null;
};

export type IncelemeDosyasi = {
  id: string;
  dosya_turu: string;
  nesne_turu: string;
  nesne_id: string;
  durum: string;
  risk_sinifi: string;
  onerilen_eylem?: string | null;
  karar_gerekcesi?: string | null;
  surum: number;
  olusturulma_zamani: string;
};

export type EslemeAdayi = {
  id: string;
  sol_sube_id: string;
  sag_sube_id: string;
  confidence: number;
  belirsizlik: Record<string, unknown>;
  durum: string;
};

export type Birlestirme = {
  id: string;
  kaynak_sube_id: string;
  hedef_sube_id: string;
  birlestirme_zamani: string;
};

export type ClaimOzet = {
  id: string;
  sube_id: string;
  yer_id: string | null;
  mekan_adi: string;
  aile: string;
  aktif_surum_no: number | null;
  durum: string;
  risk_sinifi: string;
  kaynak: string | null;
  kaynak_kayit_id: string | null;
  kaynak_alani: string | null;
  candidate_deger: unknown;
};

export type ClaimSayfasi = {
  kayitlar: ClaimOzet[];
  toplam: number;
  sayfa: number;
  sayfa_boyutu: number;
};

export type ClaimInceleme = {
  id: string;
  sube_id: string;
  yer_id: string | null;
  mekan_adi: string;
  aile: string;
  kapsam: Record<string, unknown>;
  aktif_surum_no: number | null;
  surum: Record<string, unknown> | null;
  supporting_evidence: Array<Record<string, unknown>>;
  counter_evidence: Array<Record<string, unknown>>;
  kanit_ozeti: {
    observation_sayisi: number;
    supporting_sayisi: number;
    counter_sayisi: number;
    ilk_tarih: string | null;
    son_tarih: string | null;
  };
  kaynak_haklari: Array<Record<string, unknown>>;
  yayin_onizleme: {
    durum: string;
    neden_kodlari: string[];
    etkilenen_public_alanlar: string[];
  };
  public_preview: Record<string, unknown>;
};

export type AuditOlayi = {
  id: string;
  aktor_id: string;
  eylem: string;
  nesne_turu: string;
  nesne_id: string;
  gerekce: string;
  istek_id: string;
  olusturulma_zamani: string;
};

export type DahiliSinyalOzet = {
  id: string;
  sube_id: string;
  yer_id: string | null;
  mekan_adi: string;
  aile: string;
  guven_sinifi: string;
  durum: string;
  preference_eligible: boolean;
  unique_review_count: number | null;
  conflict_level: string | null;
};

export type DahiliSinyalSayfasi = {
  kayitlar: DahiliSinyalOzet[];
  toplam: number;
};

export class AdminApiHatasi extends Error {
  constructor(
    public durum: number,
    mesaj: string,
  ) {
    super(mesaj);
  }
}

function csrfToken(): string | undefined {
  if (typeof document === "undefined") return undefined;
  return document.cookie
    .split("; ")
    .find((satir) => satir.startsWith("samandira_admin_csrf="))
    ?.split("=")
    .slice(1)
    .join("=");
}

export async function adminIstek<T>(
  yol: string,
  secenekler: RequestInit = {},
): Promise<T> {
  const headers = new Headers(secenekler.headers);
  if (secenekler.body) headers.set("Content-Type", "application/json");
  const csrf = csrfToken();
  if (csrf && secenekler.method && !["GET", "HEAD"].includes(secenekler.method)) {
    headers.set("X-CSRF-Token", decodeURIComponent(csrf));
  }
  const yanit = await fetch(`/backend/v1/admin${yol}`, {
    ...secenekler,
    credentials: "include",
    headers,
  });
  if (!yanit.ok) {
    const govde = (await yanit.json().catch(() => null)) as {
      detail?: string | { mesaj?: string };
    } | null;
    const detay = govde?.detail;
    const mesaj =
      typeof detay === "string" ? detay : detay?.mesaj || "Admin işlemi tamamlanamadı.";
    throw new AdminApiHatasi(yanit.status, mesaj);
  }
  if (yanit.status === 204) return undefined as T;
  return (await yanit.json()) as T;
}

export function kritikEylemMi(eylem: string): boolean {
  return [
    "canonical_merge",
    "split",
    "kritik_claim_yayini",
    "withdraw",
    "hak_degisikligi",
  ].includes(eylem);
}

export function eylemHazirMi(eylem: string, gerekce: string, onay: boolean): boolean {
  return gerekce.trim().length >= 8 && (!kritikEylemMi(eylem) || onay);
}

export type AdminGorunumDurumu = "yukleniyor" | "yetkisiz" | "hazir" | "hata";

export function adminGorunumu(
  durum: AdminGorunumDurumu,
  kuyruk: IncelemeDosyasi[],
): "loading" | "login_redirect" | "empty" | "queue" | "error" {
  if (durum === "yetkisiz") return "login_redirect";
  if (durum === "hata") return "error";
  if (durum === "yukleniyor") return "loading";
  return kuyruk.length ? "queue" : "empty";
}
