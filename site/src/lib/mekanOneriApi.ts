function apiKoku(): string {
  return process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8125";
}

export function yoneticiBasliklari(istek: Request): HeadersInit {
  const anahtar =
    istek.headers.get("x-yonetici-anahtar") ??
    istek.headers.get("authorization") ??
    "";
  return {
    "X-Yonetici-Anahtar": anahtar.replace(/^Bearer\s+/i, ""),
  };
}

export function istemciIp(istek: Request): string {
  return (
    istek.headers.get("x-forwarded-for")?.split(",")[0]?.trim() ||
    istek.headers.get("x-real-ip") ||
    "bilinmiyor"
  );
}

export function fastapiHata(govde: unknown, yedek: string): string {
  if (govde && typeof govde === "object" && "detail" in govde) {
    const detay = (govde as { detail: unknown }).detail;
    if (typeof detay === "string") return detay;
    if (Array.isArray(detay) && detay[0] && typeof detay[0] === "object") {
      const ilk = detay[0] as { msg?: string };
      if (ilk.msg) return ilk.msg;
    }
  }
  if (govde && typeof govde === "object" && "mesaj" in govde) {
    const mesaj = (govde as { mesaj: unknown }).mesaj;
    if (typeof mesaj === "string") return mesaj;
  }
  return yedek;
}

export async function fastapiJson(
  yol: string,
  init?: RequestInit,
): Promise<{ ok: boolean; status: number; govde: unknown }> {
  const yanit = await fetch(`${apiKoku()}${yol}`, init);
  const metin = await yanit.text();
  let govde: unknown = {};
  if (metin) {
    try {
      govde = JSON.parse(metin) as unknown;
    } catch {
      govde = { detail: metin };
    }
  }
  return { ok: yanit.ok, status: yanit.status, govde };
}
