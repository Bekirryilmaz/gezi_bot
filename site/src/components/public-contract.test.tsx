import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import { GunlukRotaSihirbazi } from "./GunlukRotaSihirbazi";
import { YerKarti } from "./ui/YerKarti";
import type { YerOzet } from "@/lib/types";

const YER: YerOzet = {
  id: "yer-1",
  isim: "Ornek Yer",
  ana_kategori: "gezilecek_yer",
  alt_kategori: "tarihi_kulturel",
  ilce: "Atakum",
  enlem: 41,
  boylam: 36,
  kapak_fotografi_url: null,
  ticari_bildirim: null,
};

describe("public frontend contract", () => {
  it("yer kartinda legacy duygu skorunu kullanici puani gibi gostermez", () => {
    const legacyYer = {
      ...YER,
      duygu_skoru_ortalama: 0.92,
      kaynakta_puan_ortalamasi: 4.8,
    };
    const html = renderToStaticMarkup(<YerKarti yer={legacyYer} />);
    expect(html).not.toContain("4.6");
    expect(html).not.toContain("4.8");
    expect(html).not.toContain("skor");
  });

  it("public rota akisi gun sayisi veya konaklama secimi gostermez", () => {
    const html = renderToStaticMarkup(
      <GunlukRotaSihirbazi sehirAnahtari="samsun" sehirIsim="Samsun" />,
    );
    expect(html).not.toContain("Kaç gün");
    expect(html).not.toContain("Konaklama bölgem");
    expect(html).not.toContain("Alternatif rotaları");
    expect(html).toContain("Tek günlük Akıllı Rota");
  });
});
