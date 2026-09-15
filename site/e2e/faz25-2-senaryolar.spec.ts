import { expect, test } from "@playwright/test";

const senaryolar = [
  "sevgilimle kahve içicem ve sohbet edicez",
  "ailemi yemeğe götürcem",
  "çalışmalık sakin bir kafe",
  "çocuklarla gidebileceğimiz yer",
  "sakin kahveci",
  "manzaralı bir yerde oturalım",
  "kahvaltıya gidelim",
  "tatlı yiyelim",
] as const;

type Cevap = {
  durum: string;
  kesfet?: { secenekler?: Array<{ yer: { isim: string } }> };
  netlestirme?: { soru: string };
};

async function bugunYanitiAl(
  page: import("@playwright/test").Page,
  alan: import("@playwright/test").Locator,
  ifade: string,
) {
  for (let deneme = 0; deneme < 6; deneme += 1) {
    const yanitSozu = page.waitForResponse(
      (yanit) =>
        yanit.url().includes("/backend/v1/bugun-ne-yapalim") &&
        yanit.request().method() === "POST" &&
        yanit.request().postDataJSON()?.serbest_metin === ifade,
      { timeout: 30_000 },
    );
    await alan.getByRole("button", { name: "Bugün için seçenek bul" }).click();
    const yanit = await yanitSozu;
    if (yanit.ok()) return yanit;
    if (yanit.status() !== 429) {
      throw new Error(`${ifade} HTTP ${yanit.status()}`);
    }
    await page.waitForTimeout(61_000);
  }
  throw new Error(`${ifade} yazma limiti asildi`);
}

async function senaryoyuDogrula(page: import("@playwright/test").Page, ifade: string) {
  const alan = page.locator("#bugun-ne-yapalim");
  await expect(alan.getByLabel("Bugün için ihtiyacın")).toBeVisible();
  await alan.getByLabel("Bugün için ihtiyacın").fill(ifade);
  const yanit = await bugunYanitiAl(page, alan, ifade);
  const govde = (await yanit.json()) as Cevap;
  await expect(alan.getByText("Şunu anladım:", { exact: true })).toBeVisible();
  await expect(alan).not.toContainText("Rotam");
  await expect(alan).not.toContainText(/yorum sayısı|sentiment/i);

  if (govde.durum === "clarification") {
    await expect(
      alan.getByText(govde.netlestirme?.soru ?? "", { exact: true }),
    ).toBeVisible();
    return govde;
  }

  const kartlar = alan
    .getByRole("list", { name: "Bugün için seçenekler" })
    .getByRole("link");
  const adet = govde.kesfet?.secenekler?.length ?? 0;
  if (adet > 0) {
    await expect(kartlar).toHaveCount(adet);
    const aday = (govde.kesfet?.secenekler ?? []).find(
      (secenek) => secenek.yer.isim.trim().length > 1,
    );
    const tiklanan = aday
      ? alan.getByRole("link", { name: aday.yer.isim }).first()
      : kartlar.first();
    const yerAdi = aday?.yer.isim ?? (await tiklanan.textContent());
    await tiklanan.click();
    await expect(page.getByRole("heading", { name: yerAdi!, exact: true })).toBeVisible();
    await expect(page.getByRole("heading", { name: "Doğruladığımız" })).toBeVisible();
    await expect(page.getByRole("heading", { name: "Deneyim sinyali" })).toBeVisible();
    await expect(
      page.getByRole("heading", { name: "Henüz doğrulayamadığımız" }),
    ).toBeVisible();
    await page.getByRole("link", { name: "Bugün Ne Yapalım bağlamına dön" }).click();
    await expect(alan.getByLabel("Bugün için ihtiyacın")).toHaveValue(ifade);
  } else {
    await expect(
      alan.getByText(/doğrulanmış bilgi henüz yeterli değil|Yalnız \d+ destekli seçenek/),
    ).toBeVisible();
  }
  return govde;
}

test.describe.configure({ mode: "serial" });

test.describe("FAZ 25.2 bağlı senaryolar", () => {
  test("masaüstü 1280px ve 390px bağlı akışlar", async ({ page }) => {
    test.setTimeout(720_000);
    for (const [sira, genislik] of ([1280, 390] as const).entries()) {
      if (sira > 0) await page.waitForTimeout(61_000);
      await page.setViewportSize({ width: genislik, height: 844 });
      for (const ifade of senaryolar) {
        await page.goto("/");
        await senaryoyuDogrula(page, ifade);
      }
    }
  });
});
