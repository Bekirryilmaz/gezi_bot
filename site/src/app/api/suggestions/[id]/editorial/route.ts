import { NextResponse } from "next/server";
import { fastapiHata, fastapiJson, yoneticiBasliklari } from "@/lib/mekanOneriApi";

type Baglam = { params: Promise<{ id: string }> };

export async function PATCH(istek: Request, { params }: Baglam) {
  const { id } = await params;
  let govde: unknown;
  try {
    govde = await istek.json();
  } catch {
    return NextResponse.json({ mesaj: "Geçersiz JSON." }, { status: 400 });
  }
  try {
    const { ok, status, govde: cevap } = await fastapiJson(
      `/mekan-onerileri/${encodeURIComponent(id)}/editorial`,
      {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
          ...yoneticiBasliklari(istek),
        },
        body: JSON.stringify(govde),
      },
    );
    if (!ok) {
      return NextResponse.json({ mesaj: fastapiHata(cevap, "Güncellenemedi.") }, { status });
    }
    return NextResponse.json(cevap);
  } catch {
    return NextResponse.json({ mesaj: "API’ye bağlanılamadı." }, { status: 503 });
  }
}
