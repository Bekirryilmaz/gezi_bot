import { NextResponse } from "next/server";
import { fastapiHata, fastapiJson, yoneticiBasliklari } from "@/lib/mekanOneriApi";

export async function GET(istek: Request) {
  const url = new URL(istek.url);
  const durum = url.searchParams.get("durum") ?? "beklemede";
  try {
    const { ok, status, govde } = await fastapiJson(
      `/mekan-onerileri?durum=${encodeURIComponent(durum)}`,
      { headers: yoneticiBasliklari(istek), cache: "no-store" },
    );
    if (!ok) {
      return NextResponse.json({ mesaj: fastapiHata(govde, "Liste alınamadı.") }, { status });
    }
    return NextResponse.json(govde);
  } catch {
    return NextResponse.json({ mesaj: "API’ye bağlanılamadı." }, { status: 503 });
  }
}
