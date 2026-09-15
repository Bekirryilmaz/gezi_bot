import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";

import { AktifFiltreOzeti } from "./AktifFiltreOzeti";
import { AramaKutusu } from "./AramaKutusu";
import { FiltrePaneli } from "./FiltrePaneli";
import { SonucListesi } from "./SonucListesi";

const katalog = {
  sehir_id: "sehir-1",
  sehir_anahtari: "samsun",
  ilceler: [{ id: "ilce-1", isim: "Atakum", sehir_id: "sehir-1" }],
  turler: [{ kod: "kafe", etiket: "Kafe" }],
  somut_kosullar: [{ kod: "otopark", etiket: "Otopark", iddia_ailesi: "otopark" }],
};
const filtre = {
  sehir: "samsun",
  ilce: "ilce-1",
  tur: "kafe",
  zorunluKosullar: ["otopark"],
  tercihler: [],
};

describe("arama bilesenleri", () => {
  it("arama kutusu erisilebilir search ve label tasir", () => {
    const html = renderToStaticMarkup(
      <AramaKutusu deger="atakum" onDegerDegis={() => undefined} />,
    );
    expect(html).toContain('role="search"');
    expect(html).toContain("Yer, tür, şehir veya ilçe ara");
  });

  it("filtre paneli hard ve preference anlamini ayirir", () => {
    const html = renderToStaticMarkup(
      <FiltrePaneli
        katalog={katalog}
        state={{ uygulanan: filtre, taslak: filtre }}
        onEylem={() => undefined}
      />,
    );
    expect(html).toContain("Zorunlu koşullar");
    expect(html).toContain("Tercihler");
    expect(html).toContain("Uygula");
    expect(html).toContain("Vazgeç");
    expect(html).toContain("Temizle");
    expect(
      renderToStaticMarkup(<AktifFiltreOzeti filtreler={filtre} katalog={katalog} />),
    ).toContain("Otopark · zorunlu");
  });

  it("loading error empty ve insufficient durumlarini ayri sunar", () => {
    expect(
      renderToStaticMarkup(<SonucListesi durum="loading" sonuclar={[]} />),
    ).toContain("aranıyor");
    expect(renderToStaticMarkup(<SonucListesi durum="error" sonuclar={[]} />)).toContain(
      'role="alert"',
    );
    expect(renderToStaticMarkup(<SonucListesi durum="empty" sonuclar={[]} />)).toContain(
      "eşleşen",
    );
    expect(
      renderToStaticMarkup(<SonucListesi durum="insufficient" sonuclar={[]} />),
    ).toContain("yeterli bilgi yok");
  });
});
