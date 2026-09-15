import { expect, test } from "@playwright/test";

test("canlı Swagger /docs endpoint ve DTO şemasını gösterir", async ({
  page,
}, testInfo) => {
  test.skip(process.env.FAZ25_DOCS !== "1", "FAZ25_DOCS=1 gerekir");
  await page.goto("https://qk4cmqnw-8125.euw.devtunnels.ms/docs");
  const notice = page.getByRole("button", { name: "Continue", exact: true });
  if (await notice.isVisible()) await notice.click();
  await expect(page.getByRole("heading", { name: /Şamandıra API/ })).toBeVisible({
    timeout: 20000,
  });
  const endpoint = page.getByRole("button", { name: /POST.*\/v1\/bugun-ne-yapalim/ });
  await endpoint.click();
  await expect(
    page.getByRole("button", { name: "Try it out", exact: true }),
  ).toBeVisible();
  await testInfo.attach("live-docs", {
    body: await page.screenshot({ fullPage: true }),
    contentType: "image/png",
  });
});
