import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";

import { BugunNeYapalimAlani } from "./BugunNeYapalimAlani";

describe("Bugün Ne Yapalım giriş sözleşmesi", () => {
  it("serbest metin ve yapılandırılmış fallback'i semantik kontrollerle sunar", () => {
    const html = renderToStaticMarkup(
      <BugunNeYapalimAlani
        sehir="Samsun"
        sehirAnahtari="samsun"
        filtreKatalogu={{
          sehir_id: "samsun-id",
          sehir_anahtari: "samsun",
          ilceler: [{ id: "atakum-id", isim: "Atakum", sehir_id: "samsun-id" }],
          turler: [],
          somut_kosullar: [{ kod: "wifi", etiket: "Wi-Fi", iddia_ailesi: "wifi" }],
        }}
      />,
    );
    expect(html).toContain("Bugün için ihtiyacın");
    expect(html).toContain("Yazarak ilerlemek istemiyorum");
    expect(html).toContain("Atakum");
    expect(html).toContain("Wi-Fi kesin olsun");
    expect(html).toContain('type="submit"');
    expect(html).not.toContain("en iyi");
    expect(html).not.toContain("puan");
  });
});
