import { describe, expect, it } from "vitest";
import { ApiHatasi, veriDurumuBelirle } from "./api";

describe("frontend veri durumlari", () => {
  it("teknik API hatasini bos sonuc olarak siniflandirmaz", () => {
    const hata = new ApiHatasi("Servis yok", 503, "unavailable", "req-1");
    expect(veriDurumuBelirle({ yukleniyor: false, hata, ogeSayisi: 0 })).toBe(
      "unavailable",
    );
  });

  it("loading, empty ve insufficient durumlarini ayri tutar", () => {
    expect(veriDurumuBelirle({ yukleniyor: true })).toBe("loading");
    expect(veriDurumuBelirle({ yukleniyor: false, ogeSayisi: 0 })).toBe("empty");
    expect(veriDurumuBelirle({ yukleniyor: false, yetersiz: true })).toBe("insufficient");
  });
});
