import { describe, expect, it } from "vitest";

import { kesfetCevapDurumu, reddiGeriAl, secenegiReddet } from "./kesfet-state";
import type { KesfetCevabi, KesfetSecenegi } from "./types";

const secenek = {
  yer: {
    place_id: "yer-1",
    canonical_id: "canonical-1",
    branch_id: "sube-1",
    isim: "Yer",
  },
  cografya: {
    sehir_id: "s",
    sehir_anahtari: "samsun",
    sehir_ismi: "Samsun",
    ilce_id: "i",
    ilce_ismi: "Atakum",
  },
  ana_kategori: "yeme_icme",
  alt_kategori: "kafe",
  neden_bu: "Amaç destekleniyor.",
  anlamli_fark: "Daha sakin.",
  karar_sonucu: {
    karar_id: "k",
    yer: null,
    karar_turu: "onerilebilir",
    anlasilan_ihtiyac: {},
    uygunluk: "uygun",
    gerekceler: [],
    kritik_engeller: [],
    onemli_odunler: [],
    bilinmeyenler: [],
    zaman_ve_kapsam: {},
    bilgi_surumu: "b",
    politika_surumu: "p",
    yayin_surumu: 1,
    anlamli_alternatif_farki: null,
    trace_reference: null,
  },
} satisfies KesfetSecenegi;

describe("Keşfet state", () => {
  it("empty, insufficient ve success durumlarını birbirine dönüştürmez", () => {
    for (const durum of ["empty", "insufficient", "success"] as const) {
      const cevap = {
        durum,
        secenekler: [],
        kimlik_eslesmeleri: [],
        kullanilan_baglam: {},
        sinirlama_nedeni: "",
        degerlendirilemeyen_aday_sayisi: 0,
        daha_fazla_var_mi: false,
        trace_reference: null,
      } satisfies KesfetCevabi;
      expect(kesfetCevapDurumu(cevap)).toBe(durum);
    }
  });

  it("reddetme yalnız bağlam kimliklerini ekler ve geri alma sırayı döndürür", () => {
    const reddedildi = secenegiReddet([secenek], [], secenek);
    expect(reddedildi.secenekler).toEqual([]);
    expect(reddedildi.reddedilenler).toEqual(["yer-1", "canonical-1"]);
    const geri = reddiGeriAl([], reddedildi.reddedilenler, secenek, 0);
    expect(geri.secenekler).toEqual([secenek]);
    expect(geri.reddedilenler).toEqual([]);
  });
});
