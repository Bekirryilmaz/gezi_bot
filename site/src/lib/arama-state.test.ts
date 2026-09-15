import { describe, expect, it } from "vitest";

import {
  aramaFiltreReducer,
  bosAramaFiltreleri,
  filtreleriUrlOku,
  filtreleriUrlYaz,
} from "./arama-state";

describe("arama filtre state", () => {
  it("taslagi uygular, vazgecince uygulanana doner ve temizler", () => {
    const bos = bosAramaFiltreleri();
    let state = { uygulanan: bos, taslak: { ...bos } };
    state = aramaFiltreReducer(state, {
      type: "taslak",
      deger: { ...bos, ilce: "ilce-1", zorunluKosullar: ["otopark"] },
    });
    expect(state.uygulanan.ilce).toBeNull();
    state = aramaFiltreReducer(state, { type: "vazgec" });
    expect(state.taslak.ilce).toBeNull();
    state = aramaFiltreReducer(state, {
      type: "taslak",
      deger: { ...bos, ilce: "ilce-1", tercihler: ["otopark"] },
    });
    state = aramaFiltreReducer(state, { type: "uygula" });
    expect(state.uygulanan).toEqual(state.taslak);
    state = aramaFiltreReducer(state, { type: "temizle" });
    expect(state.uygulanan).toEqual(bos);
  });

  it("URL state round-trip yapar", () => {
    const filtreler = {
      sehir: "samsun",
      ilce: "canonical-atakum",
      tur: "kafe",
      zorunluKosullar: ["otopark"],
      tercihler: ["sessiz_ortam"],
    };
    const yazilan = filtreleriUrlYaz(filtreler, "Mado Atakum");
    expect(filtreleriUrlOku(new URLSearchParams(yazilan))).toEqual({
      q: "Mado Atakum",
      filtreler,
    });
  });
});
