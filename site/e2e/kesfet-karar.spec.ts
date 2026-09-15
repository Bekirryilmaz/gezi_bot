import { expect, test } from "@playwright/test";

test("Keşfet bağlamı mekân detayından dönüşte korunur", async ({ page, request }) => {
  const listeYaniti = await request.get("/backend/sehirler/samsun/yerler?limit=1");
  expect(listeYaniti.ok()).toBeTruthy();
  const liste = (await listeYaniti.json()) as { yerler: Array<{ isim: string }> };
  const yerAdi = liste.yerler[0]?.isim;
  expect(yerAdi).toBeTruthy();

  await page.goto("/sehir/samsun");
  await page
    .getByRole("searchbox", { name: "Yer, tür, şehir veya ilçe ara" })
    .fill(yerAdi!);
  await page.getByLabel("Bu ziyarette ne yapmak istiyorsun?").fill("sakin bir yürüyüş");
  await page.getByRole("button", { name: "Ara", exact: true }).click();

  await expect(page.getByText("Karar özeti", { exact: true })).toBeVisible();
  await expect(page.getByText("Adla bulunan yerler", { exact: true })).toBeVisible();
  await page.getByRole("link", { name: yerAdi!, exact: true }).click();
  await expect(page.getByRole("heading", { name: yerAdi!, exact: true })).toBeVisible();

  await page.getByRole("link", { name: "Keşfet bağlamına dön" }).click();
  await expect(
    page.getByRole("searchbox", { name: "Yer, tür, şehir veya ilçe ara" }),
  ).toHaveValue(yerAdi!);
  await expect(page.getByLabel("Bu ziyarette ne yapmak istiyorsun?")).toHaveValue(
    "sakin bir yürüyüş",
  );
});
