import { NextResponse } from "next/server";
import { fastapiHata, fastapiJson } from "@/lib/mekanOneriApi";

type Baglam = { params: Promise<{ slug: string }> };

export async function GET(_istek: Request, { params }: Baglam) {
  const { slug } = await params;
  try {
    const { ok, status, govde } = await fastapiJson(
      `/mekan-onerileri/yayinlar/${encodeURIComponent(slug)}`,
      { cache: "no-store" },
    );
    if (!ok) {
      return NextResponse.json({ mesaj: fastapiHata(govde, "Yazı bulunamadı.") }, { status });
    }
    return NextResponse.json(govde);
  } catch {
    return NextResponse.json({ mesaj: "API’ye bağlanılamadı." }, { status: 503 });
  }
}
