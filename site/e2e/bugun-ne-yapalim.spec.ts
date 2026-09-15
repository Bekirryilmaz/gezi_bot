import { expect, test } from "@playwright/test";

test("Bugün Ne Yapalım gerçek sonuçtan detaya ve korunmuş bağlama döner", async ({
  page,
}) => {
  await page.goto("/");
  const alan = page.locator("#bugun-ne-yapalim");
  await alan
    .getByLabel("Bugün için ihtiyacın")
    .fill("Samsun'da bugün kahve içmek istiyorum.");
  await alan.getByRole("button", { name: "Bugün için seçenek bul" }).click();
  await expect(alan.getByText("Şunu anladım:", { exact: true })).toBeVisible();
  await expect(
    alan.getByRole("heading", { name: "Bugün için hedefli seçenekler" }),
  ).toBeVisible();
  const ilkYer = alan
    .getByRole("list", { name: "Bugün için seçenekler" })
    .getByRole("link")
    .first();
  const yerAdi = await ilkYer.textContent();
  await ilkYer.click();
  await expect(page.getByRole("heading", { name: yerAdi!, exact: true })).toBeVisible();
  await page.getByRole("link", { name: "Bugün Ne Yapalım bağlamına dön" }).click();
  await expect(alan.getByLabel("Bugün için ihtiyacın")).toHaveValue(
    "Samsun'da bugün kahve içmek istiyorum.",
  );
  await expect(
    alan.getByRole("heading", { name: "Bugün için hedefli seçenekler" }),
  ).toBeVisible();
});

test("yetersiz doğal dil yalnız bir netleştirme sorar ve klavyeyle tamamlanır", async ({
  page,
}) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto("/");
  const alan = page.locator("#bugun-ne-yapalim");
  await alan.getByLabel("Bugün için ihtiyacın").fill("Atakum'da bir yer arıyorum.");
  const gonder = alan.getByRole("button", { name: "Bugün için seçenek bul" });
  await gonder.focus();
  await page.keyboard.press("Enter");
  await expect(
    alan.getByText("Nasıl bir şey düşünüyorsunuz?", { exact: true }),
  ).toBeVisible();
  await alan.getByRole("button", { name: "Kahve içmek" }).focus();
  await page.keyboard.press("Enter");
  await expect(alan.getByText("Şunu anladım:", { exact: true })).toBeVisible();
  await expect(alan).toHaveCSS("overflow-x", "visible");
});

test("teknik hata boş sonuç gibi gösterilmez", async ({ page }) => {
  await page.route("**/backend/v1/bugun-ne-yapalim", async (route) => {
    await route.fulfill({
      status: 503,
      contentType: "application/json",
      body: JSON.stringify({
        hata: {
          kod: "test",
          mesaj: "Geçici teknik hata",
          durum: "unavailable",
          request_id: "e2e",
        },
      }),
    });
  });
  await page.goto("/");
  const alan = page.locator("#bugun-ne-yapalim");
  await alan.getByLabel("Bugün için ihtiyacın").fill("kahve");
  await alan.getByRole("button", { name: "Bugün için seçenek bul" }).click();
  await expect(alan.getByRole("alert")).toContainText("Geçici teknik hata");
});

test("yemek amacı kategori fact ile hedefli seçenek üretir ve sayıyı uydurmaz", async ({
  page,
}) => {
  await page.goto("/");
  const alan = page.locator("#bugun-ne-yapalim");
  await alan.getByLabel("Bugün için ihtiyacın").fill("Samsun'da yemek yemek istiyorum.");
  await alan.getByRole("button", { name: "Bugün için seçenek bul" }).click();
  await expect(alan.getByText("Şunu anladım:", { exact: true })).toBeVisible();
  const kartlar = alan
    .getByRole("list", { name: "Bugün için seçenekler" })
    .getByRole("listitem");
  const adet = await kartlar.count();
  expect(adet).toBeGreaterThanOrEqual(3);
  expect(adet).toBeLessThanOrEqual(5);
});
