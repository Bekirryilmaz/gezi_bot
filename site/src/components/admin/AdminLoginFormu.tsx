"use client";

import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";

import { adminIstek, type AdminKimlik } from "@/lib/admin-api";

export function AdminLoginFormu() {
  const router = useRouter();
  const [hata, setHata] = useState("");
  const [bekliyor, setBekliyor] = useState(false);

  async function giris(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setBekliyor(true);
    setHata("");
    const form = new FormData(event.currentTarget);
    try {
      await adminIstek<AdminKimlik>("/login", {
        method: "POST",
        body: JSON.stringify({ eposta: form.get("eposta"), parola: form.get("parola") }),
      });
      router.replace("/admin");
      router.refresh();
    } catch (error) {
      setHata(error instanceof Error ? error.message : "Giriş yapılamadı.");
    } finally {
      setBekliyor(false);
    }
  }

  return (
    <form
      onSubmit={giris}
      className="border-bordo/15 bg-tuz mx-auto grid w-full max-w-md gap-5 rounded-xl border p-6 shadow-sm sm:p-8"
    >
      <div>
        <p className="etiket text-samandira">İç ekip</p>
        <h1 className="yazi-bolum text-bordo mt-2">Admin girişi</h1>
        <p className="text-ink/70 mt-3 text-sm">
          Bu alan yalnız yetkili Şamandıra operasyon ekibi içindir.
        </p>
      </div>
      <label className="grid gap-2 text-sm font-medium" htmlFor="eposta">
        E-posta
        <input
          id="eposta"
          name="eposta"
          type="email"
          autoComplete="username"
          required
          className="border-bordo/20 focus:ring-samandira rounded-md border bg-white px-3 py-3 outline-none focus:ring-2"
        />
      </label>
      <label className="grid gap-2 text-sm font-medium" htmlFor="parola">
        Parola
        <input
          id="parola"
          name="parola"
          type="password"
          autoComplete="current-password"
          required
          className="border-bordo/20 focus:ring-samandira rounded-md border bg-white px-3 py-3 outline-none focus:ring-2"
        />
      </label>
      {hata && (
        <p role="alert" className="rounded-md bg-red-50 p-3 text-sm text-red-800">
          {hata}
        </p>
      )}
      <button
        disabled={bekliyor}
        className="dugme-birincil bg-bordo rounded-md px-5 py-3 font-semibold text-white disabled:opacity-50"
      >
        {bekliyor ? "Doğrulanıyor…" : "Giriş yap"}
      </button>
    </form>
  );
}
