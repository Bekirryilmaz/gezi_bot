import { NextResponse } from "next/server";
import { fastapiHata, fastapiJson, istemciIp } from "@/lib/mekanOneriApi";

const pencereMs = 60 * 60 * 1000;
const limit = 5;
const ipKayit = new Map<string, number[]>();

function hizSiniri(ip: string): boolean {
  const simdi = Date.now();
  const liste = (ipKayit.get(ip) ?? []).filter((t) => simdi - t < pencereMs);
  if (liste.length >= limit) {
    ipKayit.set(ip, liste);
    return false;
  }
  liste.push(simdi);
  ipKayit.set(ip, liste);
  return true;
}

export async function POST(istek: Request) {
  const ip = istemciIp(istek);
  if (!hizSiniri(ip)) {
    return NextResponse.json(
      { mesaj: "Çok fazla öneri gönderildi. Biraz sonra tekrar dene." },
      { status: 429 },
    );
  }

  let govde: FormData;
  try {
    govde = await istek.formData();
  } catch {
    return NextResponse.json({ mesaj: "Geçersiz form." }, { status: 400 });
  }

  try {
    const { ok, status, govde: cevap } = await fastapiJson("/mekan-onerileri", {
      method: "POST",
      body: govde,
      headers: { "X-Forwarded-For": ip },
    });
    if (!ok) {
      return NextResponse.json(
        { mesaj: fastapiHata(cevap, "Öneri kaydedilemedi."), detail: fastapiHata(cevap, "") },
        { status },
      );
    }
    return NextResponse.json(cevap, { status });
  } catch {
    return NextResponse.json(
      {
        mesaj:
          "API’ye bağlanılamadı. FastAPI’nin çalıştığından emin ol (calis.txt).",
      },
      { status: 503 },
    );
  }
}
