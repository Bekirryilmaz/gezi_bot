import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";

import { KesfetKararAlani } from "./KesfetKararAlani";

describe("KesfetKararAlani", () => {
  it("ilk akışı form etiketleri ve dürüst claimsiz kapsamla erişilebilir kurar", () => {
    const html = renderToStaticMarkup(
      <KesfetKararAlani
        kapsam={{
          sehir_id: "s",
          sehir_anahtari: "samsun",
          sehir_ismi: "Samsun",
          manifest_surumu: "m",
          kimlik_aramasi_destekleniyor: true,
          karar_kapsami_destekleniyor: false,
          yayinlanmis_yer_sayisi: 1,
          desteklenen_yer_turleri: ["kafe"],
          desteklenen_iddia_aileleri: [],
          ilceler: [],
          kapsam_aciklamasi: "Claim kapsamı yok.",
        }}
        filtreKatalogu={{
          sehir_id: "s",
          sehir_anahtari: "samsun",
          ilceler: [],
          turler: [],
          somut_kosullar: [],
        }}
        ilkSorgu=""
        ilkFiltreler={{
          sehir: "samsun",
          ilce: null,
          tur: null,
          zorunluKosullar: [],
          tercihler: [],
        }}
      />,
    );
    expect(html).toContain("Bu ziyarette ne yapmak istiyorsun?");
    expect(html).toContain("Bu koşulu henüz doğrulayamıyoruz");
    expect(html).toContain('role="search"');
    expect(html).not.toMatch(/duygu|yorum|skor|%93/i);
  });
});
