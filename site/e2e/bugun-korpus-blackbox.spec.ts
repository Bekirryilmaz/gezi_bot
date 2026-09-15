import { expect, test } from "@playwright/test";

// Gercek development API/DB gerekir. Normal suite'i uzun ve veriye bagimli
// hale getirmemek icin opt-in; devtunnel icin PLAYWRIGHT_BASE_URL kullanilir.
test("30 doğal ifade gerçek API ile desktop ve mobil UI state üretir", async ({
  page,
}, testInfo) => {
  test.skip(process.env.FAZ25_BLACKBOX !== "1", "FAZ25_BLACKBOX=1 ile çalıştırılır");
  test.setTimeout(240_000);
  const ifadeler = [
    "sevgilimle kahve içicem ve sohbet edicez",
    "ailemi yemeğe götürcem",
    "sevgilimle takılıcaz",
    "arkadaşlarla eğlenmek istiyoruz",
    "laptop açıp çalışacağım",
    "çocuklarla çıkacağız",
    "manzaralı sakin yer",
    "wifi kesin olsun",
    "otopark şart",
    "bu akşam bir yere gidelim",
    "sevgilimle kahve içip oturacağız",
    "ailecek yemek yiyebileceğimiz bir yer",
    "arkadaşlarla kahve içip sohbet edeceğiz",
    "Atakum'da kahve içelim",
    "atakumda arkadaslarla kahve icek yer",
    "çalışmalık sakin bir kafe",
    "çocuklarla gidebileceğimiz yer",
    "manzaralı bir yerde oturalım",
    "çok pahalı olmasın",
    "arabamız yok uzak olmasın",
    "şimdi açık bir yer",
    "tatlı yiyelim",
    "kahvaltıya gidelim",
    "müze gezmek istiyorum",
    "tarihi yer gezip sonra kahve içelim",
    "biraz dolaşıp sonra yemek yiyelim",
    "eşimle yemek yiyelim",
    "yalnız kahve içmek istiyorum",
    "kahve içelim wifi şart",
    "asdasd 123 !!!",
  ];
  const izler: object[] = [];
  await page.goto("/");
  const alan = page.locator("#bugun-ne-yapalim");
  for (const [sira, ifade] of ifadeler.entries()) {
    await page.setViewportSize({ width: sira < 15 ? 1280 : 390, height: 844 });
    // 20/dakika korumasini degistirmeden gerçek kullanici yolunu test et.
    await page.waitForTimeout(3300);
    await alan.getByLabel("Bugün için ihtiyacın").fill(ifade);
    const cevapBekle = page.waitForResponse(
      (response) =>
        response.url().includes("/backend/v1/bugun-ne-yapalim") &&
        response.request().method() === "POST",
    );
    await alan.getByRole("button", { name: "Bugün için seçenek bul" }).click();
    const cevap = await cevapBekle;
    expect(cevap.status(), ifade).toBe(200);
    const veri = await cevap.json();
    await expect(alan.getByText("Şunu anladım:", { exact: true })).toBeVisible();
    await expect(
      alan.getByRole("button", { name: "Bugün için seçenek bul" }),
    ).toBeEnabled();
    if (veri.durum === "clarification") {
      await expect(alan.getByText(veri.netlestirme.soru, { exact: true })).toBeVisible();
    } else if (veri.kesfet?.secenekler?.length) {
      await expect(
        alan.getByRole("list", { name: "Bugün için seçenekler" }).getByRole("listitem"),
      ).toHaveCount(veri.kesfet.secenekler.length);
    } else {
      await expect(alan.getByText(veri.durum_aciklamasi, { exact: true })).toBeVisible();
    }
    expect(
      await page.evaluate(
        () =>
          document.documentElement.scrollWidth <= document.documentElement.clientWidth,
      ),
      ifade,
    ).toBe(true);
    const metin = await alan.innerText();
    expect(metin, ifade).not.toMatch(
      /claim sözleşmesi|fiyat claim'i|çalışma saati claim'i/,
    );
    izler.push({
      ifade,
      viewport: sira < 15 ? "desktop" : "390px",
      durum: veri.durum,
      metin,
    });
    if (sira === 0 || sira === 16) {
      await testInfo.attach(sira === 0 ? "desktop" : "mobile", {
        body: await alan.screenshot(),
        contentType: "image/png",
      });
    }
  }
  await testInfo.attach("30-ifade-ui-trace", {
    body: JSON.stringify(izler, null, 2),
    contentType: "application/json",
  });
});
