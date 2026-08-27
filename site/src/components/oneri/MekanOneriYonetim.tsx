"use client";

import { useCallback, useState } from "react";
import type { PlaceSuggestion } from "@/types/placeSuggestion";
import { ONERI_KATEGORILERI } from "@/types/placeSuggestion";

const DEPO_ANAHTAR = "samandira-yonetici";

function kategoriEtiket(id: string): string {
  const k = ONERI_KATEGORILERI.find((x) => x.id === id);
  if (!k) return id;
  return `${k.ikon} ${k.etiket}`;
}

function anahtarOku(): string {
  if (typeof window === "undefined") return "";
  return sessionStorage.getItem(DEPO_ANAHTAR) ?? "";
}

export function OneriYonetim() {
  const [giris, setGiris] = useState("");
  const [oneriler, setOneriler] = useState<PlaceSuggestion[]>([]);
  const [durumFiltre, setDurumFiltre] = useState("beklemede");
  const [mesaj, setMesaj] = useState<string | null>(null);
  const [yukleniyor, setYukleniyor] = useState(false);

  const basliklar = useCallback(() => {
    const anahtar = giris || anahtarOku();
    return { "X-Yonetici-Anahtar": anahtar };
  }, [giris]);

  async function yukle(filtre = durumFiltre) {
    setYukleniyor(true);
    setMesaj(null);
    try {
      const yanit = await fetch(`/api/onerim-var?durum=${encodeURIComponent(filtre)}`, {
        headers: basliklar(),
        cache: "no-store",
      });
      const json = (await yanit.json()) as PlaceSuggestion[] | { mesaj?: string };
      if (!yanit.ok) {
        setMesaj((json as { mesaj?: string }).mesaj ?? "Liste alınamadı.");
        setOneriler([]);
        return;
      }
      setOneriler(json as PlaceSuggestion[]);
    } catch {
      setMesaj("Bağlantı hatası.");
    } finally {
      setYukleniyor(false);
    }
  }

  async function onayla(id: string) {
    const yanit = await fetch(`/api/onerim-var/onayla/${id}`, {
      method: "POST",
      headers: basliklar(),
    });
    const json = (await yanit.json()) as { mesaj?: string; yerId?: string };
    setMesaj(json.mesaj ?? (yanit.ok ? "Onaylandı." : "Onaylanamadı."));
    if (yanit.ok) await yukle();
  }

  async function reddet(id: string) {
    const yanit = await fetch(`/api/onerim-var/reddet/${id}`, {
      method: "POST",
      headers: basliklar(),
    });
    const json = (await yanit.json()) as { mesaj?: string };
    setMesaj(json.mesaj ?? (yanit.ok ? "Reddedildi." : "Reddedilemedi."));
    if (yanit.ok) await yukle();
  }

  return (
    <div className="space-y-6">
      <form
        className="flex flex-wrap items-end gap-3"
        onSubmit={(e) => {
          e.preventDefault();
          sessionStorage.setItem(DEPO_ANAHTAR, giris);
          void yukle();
        }}
      >
        <label className="space-y-1 text-sm">
          <span className="text-ink/60">Yönetici anahtarı</span>
          <input
            type="password"
            value={giris}
            onChange={(e) => setGiris(e.target.value)}
            className="block rounded-xl border border-[var(--cizgi)] bg-white px-3 py-2"
            placeholder="YONETICI_ANAHTAR"
          />
        </label>
        <select
          value={durumFiltre}
          onChange={(e) => setDurumFiltre(e.target.value)}
          className="rounded-xl border border-[var(--cizgi)] bg-white px-3 py-2 text-sm"
        >
          <option value="beklemede">Beklemede</option>
          <option value="onaylandi">Onaylandı</option>
          <option value="reddedildi">Reddedildi</option>
        </select>
        <button
          type="submit"
          className="rounded-full bg-deniz px-4 py-2 text-sm font-semibold text-white"
        >
          {yukleniyor ? "Yükleniyor…" : "Listele"}
        </button>
      </form>

      {mesaj ? <p className="text-sm text-deniz">{mesaj}</p> : null}

      <ul className="space-y-4">
        {oneriler.map((oneri) => (
          <li
            key={oneri.id}
            className="rounded-2xl bg-white p-4 shadow-[0_8px_24px_rgba(6,54,66,0.08)]"
          >
            <div className="flex flex-wrap items-start justify-between gap-3">
              <div>
                <p className="text-xs uppercase tracking-wide text-ink/45">
                  {kategoriEtiket(oneri.category)} · {oneri.city} / {oneri.district}
                </p>
                <h2 className="font-display text-2xl text-deniz">{oneri.title}</h2>
                <p className="mt-2 text-sm text-ink/75">{oneri.description}</p>
                {oneri.specialTip ? (
                  <p className="mt-2 text-sm text-yosun">Tüyo: {oneri.specialTip}</p>
                ) : null}
                <p className="mt-2 text-xs tabular-nums text-ink/50">
                  {oneri.coordinates.lat.toFixed(5)}, {oneri.coordinates.lng.toFixed(5)}
                  {" · "}
                  {oneri.submitter.email}
                </p>
              </div>
              {oneri.status === "beklemede" ? (
                <div className="flex gap-2">
                  <button
                    type="button"
                    onClick={() => void onayla(oneri.id)}
                    className="rounded-full bg-yosun px-3 py-1.5 text-xs font-semibold text-white"
                  >
                    Onayla
                  </button>
                  <button
                    type="button"
                    onClick={() => void reddet(oneri.id)}
                    className="rounded-full bg-bordo px-3 py-1.5 text-xs font-semibold text-white"
                  >
                    Reddet
                  </button>
                </div>
              ) : (
                <span className="rounded-full bg-kopuk px-3 py-1 text-xs">{oneri.status}</span>
              )}
            </div>
            {oneri.images.length > 0 ? (
              <div className="mt-3 flex gap-2 overflow-x-auto">
                {oneri.images.map((src) => (
                  // eslint-disable-next-line @next/next/no-img-element
                  <img
                    key={src}
                    src={src}
                    alt=""
                    className="h-24 w-32 rounded-lg object-cover"
                  />
                ))}
              </div>
            ) : null}
          </li>
        ))}
      </ul>
      {!yukleniyor && oneriler.length === 0 ? (
        <p className="text-sm text-ink/50">Kayıt yok veya henüz listelenmedi.</p>
      ) : null}
    </div>
  );
}
