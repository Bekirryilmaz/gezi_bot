import { afterEach, describe, expect, it, vi } from "vitest";

import {
  adminGorunumu,
  adminIstek,
  eylemHazirMi,
  kritikEylemMi,
  type IncelemeDosyasi,
} from "./admin-api";

afterEach(() => vi.unstubAllGlobals());

describe("admin akislari", () => {
  it("login istegini admin namespace altina ve cookie ile gonderir", async () => {
    const fetchMock = vi
      .fn()
      .mockResolvedValue(new Response(JSON.stringify({ id: "1" }), { status: 200 }));
    vi.stubGlobal("fetch", fetchMock);
    await adminIstek("/login", {
      method: "POST",
      body: JSON.stringify({ eposta: "a", parola: "b" }),
    });
    expect(fetchMock).toHaveBeenCalledWith(
      "/backend/v1/admin/login",
      expect.objectContaining({ credentials: "include", method: "POST" }),
    );
  });

  it("401 durumunu unauthorized redirect kararina cevirir", async () => {
    vi.stubGlobal(
      "fetch",
      vi
        .fn()
        .mockResolvedValue(
          new Response(JSON.stringify({ detail: "Admin oturumu gerekli." }), {
            status: 401,
          }),
        ),
    );
    await expect(adminIstek("/me")).rejects.toMatchObject({ durum: 401 });
    expect(adminGorunumu("yetkisiz", [])).toBe("login_redirect");
  });

  it("kuyruk render ve empty durumlarini ayirir", () => {
    const dosya = { id: "1" } as IncelemeDosyasi;
    expect(adminGorunumu("hazir", [dosya])).toBe("queue");
    expect(adminGorunumu("hazir", [])).toBe("empty");
  });

  it("approve normal, withdrawal ve merge kritik onayli akar", () => {
    expect(kritikEylemMi("claim_approve")).toBe(false);
    expect(eylemHazirMi("claim_approve", "Yeterli gerekce", false)).toBe(true);
    expect(eylemHazirMi("withdraw", "Yeterli gerekce", false)).toBe(false);
    expect(eylemHazirMi("withdraw", "Yeterli gerekce", true)).toBe(true);
    expect(eylemHazirMi("canonical_merge", "Yeterli gerekce", true)).toBe(true);
  });

  it("typed error state mesajini korur", async () => {
    vi.stubGlobal(
      "fetch",
      vi
        .fn()
        .mockResolvedValue(
          new Response(JSON.stringify({ detail: "Yayin kapisi reddetti." }), {
            status: 409,
          }),
        ),
    );
    await expect(adminIstek("/incelemeler")).rejects.toThrow("Yayin kapisi reddetti.");
    expect(adminGorunumu("hata", [])).toBe("error");
  });
});
