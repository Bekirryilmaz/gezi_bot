import { NextResponse } from "next/server";
import { fastapiHata, fastapiJson } from "@/lib/mekanOneriApi";

export async function GET() {
  try {
    const { ok, status, govde } = await fastapiJson("/mekan-onerileri/yayinlar", {
      cache: "no-store",
    });
    if (!ok) {
      return NextResponse.json({ mesaj: fastapiHata(govde, "Liste alınamadı.") }, { status });
    }
    return NextResponse.json(govde);
  } catch {
    return NextResponse.json({ mesaj: "API’ye bağlanılamadı." }, { status: 503 });
  }
}
