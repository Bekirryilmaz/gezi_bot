"use client";

import { useEffect, useId, useMemo, useRef, useState } from "react";
import { Check, ChevronDown } from "lucide-react";

export type SeciciSecenek = {
  id: string;
  etiket: string;
  ikon?: string;
};

type Props = {
  etiket: string;
  yerTutucu: string;
  deger: string;
  secenekler: SeciciSecenek[];
  onSec: (id: string, etiket: string) => void;
  aranabilir?: boolean;
  gerekli?: boolean;
  hata?: string;
};

const LISTE_SINIFI =
  "absolute left-0 top-full z-50 mt-1.5 w-full max-h-40 overflow-y-auto bg-white shadow-2xl rounded-xl border border-teal-100 overscroll-contain";

const SATIR_SINIFI =
  "flex cursor-pointer items-center justify-between px-4 py-2.5 text-sm text-slate-700 transition-colors hover:bg-teal-50 hover:text-teal-900";

export function SeciciMenu({
  etiket,
  yerTutucu,
  deger,
  secenekler,
  onSec,
  aranabilir = false,
  gerekli = false,
  hata,
}: Props) {
  const kutuRef = useRef<HTMLDivElement>(null);
  const listeId = useId();
  const [acik, setAcik] = useState(false);
  const [arama, setArama] = useState("");

  const secili = secenekler.find((s) => s.id === deger);

  const filtrelenmis = useMemo(() => {
    if (!aranabilir) return secenekler;
    const q = arama.trim().toLocaleLowerCase("tr");
    if (!q) return secenekler;
    return secenekler.filter((s) => s.etiket.toLocaleLowerCase("tr").includes(q));
  }, [aranabilir, arama, secenekler]);

  useEffect(() => {
    if (!acik) return;
    function disari(e: MouseEvent) {
      if (!kutuRef.current?.contains(e.target as Node)) {
        setAcik(false);
      }
    }
    function kac(e: KeyboardEvent) {
      if (e.key === "Escape") setAcik(false);
    }
    document.addEventListener("mousedown", disari);
    document.addEventListener("keydown", kac);
    return () => {
      document.removeEventListener("mousedown", disari);
      document.removeEventListener("keydown", kac);
    };
  }, [acik]);

  function sec(secenek: SeciciSecenek) {
    onSec(secenek.id, secenek.etiket);
    setArama("");
    setAcik(false);
  }

  return (
    <label className={`block ${etiket ? "space-y-2" : ""} ${acik ? "relative z-40" : "relative z-30"}`}>
      {etiket ? (
        <span className="text-sm font-medium text-deniz">
          {etiket}
          {gerekli ? (
            <>
              {" "}
              <span className="text-red-500">*</span>
            </>
          ) : null}
        </span>
      ) : null}
      <div ref={kutuRef} className="relative">
        {aranabilir ? (
          <div className="relative">
            <input
              required={gerekli}
              value={acik ? arama : (secili?.etiket ?? deger)}
              onChange={(e) => {
                const metin = e.target.value;
                setArama(metin);
                onSec(metin, metin);
                setAcik(true);
              }}
              onFocus={() => {
                setArama(deger);
                setAcik(true);
              }}
              placeholder={yerTutucu}
              autoComplete="off"
              role="combobox"
              aria-expanded={acik}
              aria-controls={listeId}
              className="w-full rounded-xl border border-[var(--cizgi)] bg-white px-3 py-2.5 pr-10 text-ink outline-none focus:border-deniz"
            />
            <ChevronDown
              className={`pointer-events-none absolute right-3 top-1/2 h-4 w-4 -translate-y-1/2 text-ink/40 transition ${
                acik ? "rotate-180" : ""
              }`}
              aria-hidden
            />
          </div>
        ) : (
          <button
            type="button"
            onClick={() => setAcik((v) => !v)}
            aria-expanded={acik}
            aria-controls={listeId}
            aria-haspopup="listbox"
            className={`flex min-h-[44px] w-full items-center justify-between px-3 py-2.5 text-left text-ink outline-none ${
              etiket
                ? "rounded-xl border border-[var(--cizgi)] bg-white focus:border-deniz"
                : "bg-transparent text-base font-medium"
            }`}
          >
            <span className={secili ? "flex items-center gap-2" : "text-ink/40"}>
              {secili ? (
                <>
                  {secili.ikon ? <span aria-hidden>{secili.ikon}</span> : null}
                  {secili.etiket}
                </>
              ) : (
                yerTutucu
              )}
            </span>
            <ChevronDown
              className={`h-4 w-4 shrink-0 text-ink/40 transition ${acik ? "rotate-180" : ""}`}
              aria-hidden
            />
          </button>
        )}
        {gerekli && !aranabilir ? (
          <input type="hidden" value={deger} required readOnly tabIndex={-1} />
        ) : null}

        {acik ? (
          <ul
            id={listeId}
            role="listbox"
            className={LISTE_SINIFI}
            style={{ colorScheme: "light" }}
          >
            {filtrelenmis.length === 0 ? (
              <li className="px-4 py-2.5 text-sm text-slate-400">Eşleşme yok</li>
            ) : (
              filtrelenmis.map((secenek) => {
                const buSecili = secenek.id === deger;
                return (
                  <li key={secenek.id} role="option" aria-selected={buSecili}>
                    <button
                      type="button"
                      onClick={() => sec(secenek)}
                      className={`${SATIR_SINIFI} w-full text-left ${
                        buSecili ? "bg-teal-100/60 font-semibold text-teal-950" : ""
                      }`}
                    >
                      <span className="flex min-w-0 items-center gap-2">
                        {secenek.ikon ? <span aria-hidden>{secenek.ikon}</span> : null}
                        <span>{secenek.etiket}</span>
                      </span>
                      {buSecili ? (
                        <Check className="h-4 w-4 shrink-0 text-teal-800" aria-hidden />
                      ) : null}
                    </button>
                  </li>
                );
              })
            )}
          </ul>
        ) : null}
      </div>
      {hata ? <p className="text-sm text-red-500">{hata}</p> : null}
    </label>
  );
}
