import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";

import { BaglamliKararOzeti } from "./BaglamliKararOzeti";
import type { KamusalYerDetayi } from "@/lib/types";

const DETAY: KamusalYerDetayi = {
  yer: {
    place_id: "yer-1",
    canonical_id: "c-1",
    branch_id: "s-1",
    isim: "Ornek Kafe",
  },
  cografya: {
    sehir_id: "sehir-1",
    sehir_anahtari: "samsun",
    sehir_ismi: "Samsun",
    ilce_id: null,
    ilce_slug: null,
    ilce_ismi: null,
  },
  ana_kategori: "yeme_icme",
  alt_kategori: "kafe",
  adres: null,
  aciklama: null,
  telefon: null,
  web_sitesi: null,
  enlem: 41,
  boylam: 36,
  fotograf_urlleri: [],
  pratik_bilgiler: [],
  karar_sonucu: {
    karar_id: "k-1",
    yer: {
      place_id: "yer-1",
      canonical_id: "c-1",
      branch_id: "s-1",
      isim: "Ornek Kafe",
    },
    karar_turu: "onerilebilir",
    anlasilan_ihtiyac: {},
    uygunluk: "uygun",
    gerekceler: [
      {
        kod: "amac_destekleniyor",
        mesaj: "Yer belirtilen amacı destekliyor.",
        ilgili_kosul: "kahve_icmek",
      },
      {
        kod: "deneyim_sinyali_destekliyor",
        mesaj: "Deneyim sinyali bu tercihi destekliyor.",
        ilgili_kosul: "sessiz_ortam",
      },
    ],
    kritik_engeller: [],
    onemli_odunler: [
      {
        kod: "tercih_bilinmiyor",
        mesaj: "Belirtilen tercih için yeterli bilgi yok.",
        ilgili_kosul: "wifi",
      },
    ],
    bilinmeyenler: [],
    zaman_ve_kapsam: {},
    bilgi_surumu: "b",
    politika_surumu: "p",
    yayin_surumu: 1,
    anlamli_alternatif_farki: null,
    trace_reference: "t",
  },
  kritik_bilinmeyenler: [],
  kapsam_anlami: "kapsam",
  duzeltme_girisi: { etiket: "Düzelt", aciklama: "", href: null },
};

describe("BaglamliKararOzeti", () => {
  it("fact, deneyim ve henuz dogrulanamayan ayrimini gosterir; teknik alani gizler", () => {
    const html = renderToStaticMarkup(
      <BaglamliKararOzeti yerId="yer-1" ilkDetay={DETAY} />,
    );
    expect(html).toContain("Doğruladığımız");
    expect(html).toContain("Deneyim sinyali");
    expect(html).toContain("Henüz doğrulayamadığımız");
    expect(html).toContain("sakinlik deneyimi açısından destekleyici sinyal var.");
    expect(html).not.toMatch(/guven|unique_review|google|%93|skor/i);
  });
});
