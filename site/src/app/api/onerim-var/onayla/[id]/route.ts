import { NextResponse } from "next/server";
import { fastapiHata, fastapiJson, yoneticiBasliklari } from "@/lib/mekanOneriApi";

type Props = { params: Promise<{ id: string }> };

export async function POST(istek: Request, { params }: Props) {
  const { id } = await params;
  try {
    const { ok, status, govde } = await fastapiJson(
      `/mekan-onerileri/${encodeURIComponent(id)}/onayla`,
      { method: "POST", headers: yoneticiBasliklari(istek) },
    );
    if (!ok) {
      return NextResponse.json({ mesaj: fastapiHata(govde, "Onaylanamadı.") }, { status });
    }
    return NextResponse.json(govde);
  } catch {
    return NextResponse.json({ mesaj: "API’ye bağlanılamadı." }, { status: 503 });
  }
}
