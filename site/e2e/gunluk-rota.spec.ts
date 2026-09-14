import { expect, test } from "@playwright/test";

test("public rota akisi yalniz tek gunluk MVP kontrollerini gosterir", async ({
  page,
}) => {
  await page.goto("/sehir/samsun/rota");

  await expect(page.getByText("Tek günlük Akıllı Rota", { exact: true })).toBeVisible();
  await expect(
    page.getByRole("button", { name: "Bugünün rotasını oluştur" }),
  ).toBeVisible();
  await expect(page.getByText("Kaç gün", { exact: false })).toHaveCount(0);
  await expect(page.getByText("Konaklama bölgem", { exact: false })).toHaveCount(0);
  await expect(page.getByText("Alternatif rotaları", { exact: false })).toHaveCount(0);
});
