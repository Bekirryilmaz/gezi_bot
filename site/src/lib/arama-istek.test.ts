import { describe, expect, it } from "vitest";

import { AramaIstekYoneticisi } from "./arama-istek";

describe("stale response guvenligi", () => {
  it("eski yanit daha gec gelse de yeni sorgunun ustune yazmaz", async () => {
    const yonetici = new AramaIstekYoneticisi();
    let eskiyiCoz!: (deger: string) => void;
    let yeniyiCoz!: (deger: string) => void;
    const eski = yonetici.yurut(
      () =>
        new Promise<string>((coz) => {
          eskiyiCoz = coz;
        }),
    );
    const yeni = yonetici.yurut(
      () =>
        new Promise<string>((coz) => {
          yeniyiCoz = coz;
        }),
    );
    yeniyiCoz("atakum");
    eskiyiCoz("at");
    await expect(yeni).resolves.toBe("atakum");
    await expect(eski).resolves.toBeUndefined();
  });
});
