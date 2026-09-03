"use client";

import { useCallback, useState } from "react";
import type { PlaceSuggestion } from "@/types/placeSuggestion";
import { ONERI_KATEGORILERI } from "@/types/placeSuggestion";
import {
  toggleFieldVisibility,
  updateAdminContext,
  type CommunityVisibleFields,
} from "@/types/suggestion";

const DEPO_ANAHTAR = "samandira-yonetici";

const VARSAYILAN_ALAN: CommunityVisibleFields = {
  showDirections: true,
  showTransportation: true,
  showExactCoordinates: false,
  showSpecialTip: true,
};

function kategoriEtiket(id: string): string {
  const k = ONERI_KATEGORILERI.find((x) => x.id === id);
  if (!k) return id;
  return `${k.ikon} ${k.etiket}`;
}

function anahtarOku(): string {
  if (typeof window === "undefined") return "";
  return sessionStorage.getItem(DEPO_ANAHTAR) ?? "";
}

function alanlar(oneri: PlaceSuggestion): CommunityVisibleFields {
  return oneri.visibleFields ?? VARSAYILAN_ALAN;
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

  async function gorunurlukKaydet(oneri: PlaceSuggestion, field: keyof CommunityVisibleFields) {
    const sonraki = toggleFieldVisibility(alanlar(oneri), field);
    const yanit = await fetch(`/api/suggestions/${oneri.id}/gorunurluk`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json", ...basliklar() },
      body: JSON.stringify(sonraki),
    });
    const json = (await yanit.json()) as PlaceSuggestion | { mesaj?: string };
    setMesaj(yanit.ok ? "Görünürlük güncellendi." : ((json as { mesaj?: string }).mesaj ?? "Güncellenemedi."));
    if (yanit.ok) await yukle();
  }

  async function editorialKaydet(oneri: PlaceSuggestion, form: HTMLFormElement) {
    const veri = new FormData(form);
    const guncel = updateAdminContext(oneri.adminEditorial, {
      historicalContext: String(veri.get("historicalContext") ?? ""),
      adminNotes: String(veri.get("adminNotes") ?? ""),
    });
    const yanit = await fetch(`/api/suggestions/${oneri.id}/editorial`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json", ...basliklar() },
      body: JSON.stringify({
        historicalContext: guncel.historicalContext,
        adminNotes: guncel.adminNotes,
      }),
    });
    const json = (await yanit.json()) as { mesaj?: string };
    setMesaj(yanit.ok ? "Editör notu kaydedildi." : (json.mesaj ?? "Kaydedilemedi."));
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
                {oneri.directions ? (
                  <p className="mt-2 text-sm text-ink/70">Tarif: {oneri.directions}</p>
                ) : null}
                {oneri.transportation ? (
                  <p className="mt-1 text-sm text-ink/60">
                    Ulaşım: {oneri.transportation.carAccess} · {oneri.transportation.roadCondition} ·{" "}
                    {oneri.transportation.walkingDistance} · {oneri.transportation.publicTransit}
                  </p>
                ) : null}
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
            {oneri.status === "onaylandi" ? (
              <div className="mt-4 space-y-3 border-t border-teal-100 pt-4">
                <p className="text-xs font-semibold uppercase tracking-wide text-teal-700">
                  Blog görünürlüğü
                </p>
                <div className="flex flex-wrap gap-2">
                  {(
                    [
                      ["showDirections", "Adres tarifi"],
                      ["showTransportation", "Ulaşım"],
                      ["showExactCoordinates", "Tam koordinat"],
                      ["showSpecialTip", "Tüyo"],
                    ] as const
                  ).map(([alan, etiket]) => (
                    <button
                      key={alan}
                      type="button"
                      onClick={() => void gorunurlukKaydet(oneri, alan)}
                      className={`rounded-full px-3 py-1 text-xs font-semibold ${
                        alanlar(oneri)[alan]
                          ? "bg-yosun text-white"
                          : "bg-kopuk text-ink/60"
                      }`}
                    >
                      {etiket}
                    </button>
                  ))}
                </div>
                <form
                  className="grid gap-2 md:grid-cols-2"
                  onSubmit={(e) => {
                    e.preventDefault();
                    void editorialKaydet(oneri, e.currentTarget);
                  }}
                >
                  <textarea
                    name="historicalContext"
                    defaultValue={oneri.adminEditorial?.historicalContext ?? ""}
                    rows={3}
                    placeholder="Tarihi / kültürel arka plan"
                    className="w-full rounded-xl border border-[var(--cizgi)] px-3 py-2 text-sm"
                  />
                  <textarea
                    name="adminNotes"
                    defaultValue={oneri.adminEditorial?.adminNotes ?? ""}
                    rows={3}
                    placeholder="Editör tavsiyesi"
                    className="w-full rounded-xl border border-[var(--cizgi)] px-3 py-2 text-sm"
                  />
                  <button
                    type="submit"
                    className="rounded-full bg-deniz px-3 py-1.5 text-xs font-semibold text-white md:col-span-2"
                  >
                    Editör notunu kaydet
                  </button>
                </form>
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
