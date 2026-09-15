import type { KesfetCevabi, KesfetSecenegi } from "./types";

export type KesfetEkranDurumu =
  "initial" | "loading" | "success" | "empty" | "insufficient" | "unavailable" | "error";

export function kesfetCevapDurumu(cevap: KesfetCevabi): KesfetEkranDurumu {
  return cevap.durum;
}

export function secenegiReddet(
  secenekler: KesfetSecenegi[],
  reddedilenler: string[],
  secenek: KesfetSecenegi,
): { secenekler: KesfetSecenegi[]; reddedilenler: string[] } {
  return {
    secenekler: secenekler.filter((oge) => oge.yer.place_id !== secenek.yer.place_id),
    reddedilenler: [
      ...new Set([...reddedilenler, secenek.yer.place_id, secenek.yer.canonical_id]),
    ],
  };
}

export function reddiGeriAl(
  secenekler: KesfetSecenegi[],
  reddedilenler: string[],
  secenek: KesfetSecenegi,
  sira: number,
): { secenekler: KesfetSecenegi[]; reddedilenler: string[] } {
  const yeni = [...secenekler];
  if (!yeni.some((oge) => oge.yer.place_id === secenek.yer.place_id)) {
    yeni.splice(Math.min(sira, yeni.length), 0, secenek);
  }
  return {
    secenekler: yeni,
    reddedilenler: reddedilenler.filter(
      (id) => ![secenek.yer.place_id, secenek.yer.canonical_id].includes(id),
    ),
  };
}
