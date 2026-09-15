import { expect, test } from "@playwright/test";

test("FAZ25 canlı 21 ifade desktop ve 390px", async ({ page }, testInfo) => {
  test.skip(process.env.FAZ25_LIVE_SITE !== "1", "FAZ25_LIVE_SITE=1 gerekir");
  test.setTimeout(1_200_000);
  const expressions =
    process.env.FAZ25_OUTCOME_ONLY === "1"
      ? [
          "otopark şart yemek",
          "en fazla 500 tl yemek",
          "sevgilimle kahve içip oturacağız",
          "çalışmalık sakin bir kafe",
        ]
      : [
          "sevgilimle kahve içicem ve sohbet edicez",
          "sevgilimle takılıcaz",
          "sevgilimle eğlenicez",
          "ailemi yemeğe götürcem",
          "ailecek yemek yiyebileceğimiz bir yer",
          "arkadaşlarla kahve içip sohbet edeceğiz",
          "arkadaşlarla eğlenmek istiyoruz",
          "laptop açıp çalışacağım",
          "çalışmalık sakin bir kafe",
          "çocuklarla gidebileceğimiz yer",
          "manzaralı bir yerde oturalım",
          "çok pahalı olmasın",
          "arabamız yok uzak olmasın",
          "wifi kesin olsun",
          "otopark şart",
          "bu akşam nereye gidelim",
          "şimdi açık bir yer",
          "tatlı yiyelim",
          "kahvaltıya gidelim",
          "müze gezmek istiyorum",
          "tarihi yer gezip sonra kahve içelim",
        ];
  const goals =
    process.env.FAZ25_OUTCOME_ONLY === "1"
      ? ["yemek_yemek", "yemek_yemek", "kahve_icmek", "calisma"]
      : [
          "kahve_icmek",
          "birlikte_vakit",
          "eglence",
          "yemek_yemek",
          "yemek_yemek",
          "kahve_icmek",
          "eglence",
          "calisma",
          "calisma",
          "cocukla_aktivite",
          "birlikte_vakit",
          null,
          null,
          null,
          null,
          null,
          null,
          "tatli_yemek",
          "kahvalti_yapmak",
          "tarihi_kulturel_ziyaret",
          "kahve_icmek",
        ];
  const traces: object[] = [];
  const widths = process.env.FAZ25_WIDTHS?.split(",").map(Number) ?? [1280, 390];
  for (const width of widths) {
    const currentPage = await page.context().newPage();
    currentPage.setDefaultTimeout(30_000);
    await currentPage.setViewportSize({ width, height: 844 });
    for (let navigationAttempt = 0; navigationAttempt < 3; navigationAttempt++) {
      try {
        await currentPage.goto("/", { waitUntil: "domcontentloaded", timeout: 30_000 });
        break;
      } catch (error) {
        if (navigationAttempt === 2) throw error;
      }
    }
    // Devtunnel's ordinary first-visit notice (not a TLS/browser security error).
    const continueButton = currentPage.getByRole("button", {
      name: "Continue",
      exact: true,
    });
    if (await continueButton.isVisible()) await continueButton.click();
    const area = currentPage.locator("#bugun-ne-yapalim");
    await expect(
      area.getByRole("textbox", { name: "Bugün için ihtiyacın" }),
    ).toBeVisible();
    await expect(area.getByRole("textbox", { name: "Bugün için ihtiyacın" })).toBeEnabled(
      { timeout: 30_000 },
    );
    for (const [index, expression] of expressions.entries()) {
      const subset = process.env.FAZ25_QUERY_INDICES?.split(",").map(Number);
      if (subset && !subset.includes(index)) continue;
      await currentPage.waitForTimeout(7000);
      await area.getByRole("textbox", { name: "Bugün için ihtiyacın" }).fill(expression);
      const attempts: object[] = [];
      let responseBody = null;
      for (let attempt = 0; attempt < 3; attempt++) {
        const responsePromise = currentPage.waitForResponse(
          (r) =>
            r.url().includes("/backend/v1/bugun-ne-yapalim") &&
            r.request().method() === "POST" &&
            r.request().postDataJSON()?.serbest_metin === expression,
          { timeout: 20_000 },
        );
        await area
          .getByRole("button", { name: "Bugün için seçenek bul", exact: true })
          .click();
        try {
          const response = await responsePromise;
          attempts.push({ http: response.status() });
          if (response.ok()) {
            responseBody = await response.json();
            break;
          }
        } catch {
          attempts.push({ http: 0, state: "timeout" });
        }
        await expect(
          area.getByRole("button", { name: "Bugün için seçenek bul", exact: true }),
        ).toBeEnabled();
        await currentPage.waitForTimeout(7000);
      }
      await expect(
        area.getByRole("button", { name: "Bugün için seçenek bul", exact: true }),
      ).toBeEnabled();
      await expect(
        area.getByRole("textbox", { name: "Bugün için ihtiyacın" }),
      ).toHaveValue(expression);
      const text = await area.innerText();
      expect.soft(responseBody, expression).not.toBeNull();
      expect
        .soft(text, expression)
        .not.toMatch(
          /hard constraint|preference|publication|claim|karar bağlamı|kritik bilinmeyen|yayımlanmış/i,
        );
      expect
        .soft(
          await currentPage.evaluate(
            () =>
              document.documentElement.scrollWidth <=
              document.documentElement.clientWidth,
          ),
          expression,
        )
        .toBe(true);
      if (responseBody) {
        expect
          .soft(responseBody.anlasilan_ihtiyac.ana_amac, expression)
          .toBe(goals[index]);
        await expect(area.getByText("Şunu anladım:", { exact: true })).toBeVisible();
        if (responseBody.durum === "clarification") {
          await expect(
            area.getByText(responseBody.netlestirme.soru, { exact: true }),
          ).toBeVisible();
        }
        if (responseBody.kesfet?.secenekler?.length) {
          await expect(
            area
              .getByRole("list", { name: "Bugün için seçenekler" })
              .getByRole("listitem"),
          ).toHaveCount(responseBody.kesfet.secenekler.length);
        }
      }
      traces.push({ expression, width, attempts, response: responseBody, text });
      try {
        await testInfo.attach(`live-${width}-${index}`, {
          body: await area.screenshot({ timeout: 15_000 }),
          contentType: "image/png",
        });
      } catch {
        // The devtunnel occasionally leaves a font request pending. Keep the
        // interaction assertion and record a viewport screenshot when possible.
        await testInfo
          .attach(`live-${width}-${index}-font-timeout`, {
            body: await currentPage.screenshot({ timeout: 15_000 }),
            contentType: "image/png",
          })
          .catch(() => undefined);
      }
      // Reload preserves previous result but must not silently override a new natural query.
      if (index === 0) await currentPage.reload();
    }
    await currentPage.close();
  }
  await testInfo.attach("live-42-trace", {
    body: JSON.stringify(traces, null, 2),
    contentType: "application/json",
  });
});
