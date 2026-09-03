import { NextResponse } from "next/server";
import { fastapiHata, fastapiJson } from "@/lib/mekanOneriApi";

type Baglam = { params: Promise<{ slug: string }> };

export async function POST(istek: Request, { params }: Baglam) {
  const { slug } = await params;
  let govde: unknown;
  try {
    govde = await istek.json();
  } catch {
    return NextResponse.json({ mesaj: "Geçersiz JSON." }, { status: 400 });
  }
  try {
    const { ok, status, govde: cevap } = await fastapiJson(
      `/mekan-onerileri/yayinlar/${encodeURIComponent(slug)}/yorumlar`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(govde),
      },
    );
    if (!ok) {
      return NextResponse.json({ mesaj: fastapiHata(cevap, "Yorum kaydedilemedi.") }, { status });
    }
    return NextResponse.json(cevap, { status: 201 });
  } catch {
    return NextResponse.json({ mesaj: "API’ye bağlanılamadı." }, { status: 503 });
  }
}
