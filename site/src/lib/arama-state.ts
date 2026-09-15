import type { AramaFiltreDurumu } from "./types";

export type AramaFiltreState = {
  uygulanan: AramaFiltreDurumu;
  taslak: AramaFiltreDurumu;
};

export type AramaFiltreEylemi =
  | { type: "taslak"; deger: AramaFiltreDurumu }
  | { type: "uygula" }
  | { type: "vazgec" }
  | { type: "temizle" };

export function bosAramaFiltreleri(sehir = "samsun"): AramaFiltreDurumu {
  return { sehir, ilce: null, tur: null, zorunluKosullar: [], tercihler: [] };
}

function kopyala(deger: AramaFiltreDurumu): AramaFiltreDurumu {
  return {
    ...deger,
    zorunluKosullar: [...deger.zorunluKosullar],
    tercihler: [...deger.tercihler],
  };
}

export function aramaFiltreReducer(
  state: AramaFiltreState,
  eylem: AramaFiltreEylemi,
): AramaFiltreState {
  if (eylem.type === "taslak") return { ...state, taslak: kopyala(eylem.deger) };
  if (eylem.type === "uygula") {
    const uygulanan = kopyala(state.taslak);
    return { uygulanan, taslak: kopyala(uygulanan) };
  }
  if (eylem.type === "vazgec") return { ...state, taslak: kopyala(state.uygulanan) };
  const temiz = bosAramaFiltreleri(state.uygulanan.sehir);
  return { uygulanan: temiz, taslak: kopyala(temiz) };
}

export function filtreleriUrlYaz(filtreler: AramaFiltreDurumu, q = ""): string {
  const params = new URLSearchParams();
  if (q) params.set("q", q);
  params.set("sehir", filtreler.sehir);
  if (filtreler.ilce) params.set("ilce", filtreler.ilce);
  if (filtreler.tur) params.set("tur", filtreler.tur);
  for (const kod of [...filtreler.zorunluKosullar].sort()) params.append("zorunlu", kod);
  for (const kod of [...filtreler.tercihler].sort()) params.append("tercih", kod);
  return params.toString();
}

export function filtreleriUrlOku(params: URLSearchParams): {
  q: string;
  filtreler: AramaFiltreDurumu;
} {
  return {
    q: params.get("q") ?? "",
    filtreler: {
      sehir: params.get("sehir") ?? "samsun",
      ilce: params.get("ilce"),
      tur: params.get("tur"),
      zorunluKosullar: [...new Set(params.getAll("zorunlu"))],
      tercihler: [...new Set(params.getAll("tercih"))],
    },
  };
}
