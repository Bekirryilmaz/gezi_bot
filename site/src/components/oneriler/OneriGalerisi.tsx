"use client";

import { useState } from "react";

export function OneriGalerisi({ gorseller, baslik }: { gorseller: string[]; baslik: string }) {
  const [secili, setSecili] = useState(0);
  const [acik, setAcik] = useState(false);
  if (gorseller.length === 0) return null;
  const aktif = gorseller[secili] ?? gorseller[0];

  return (
    <div className="space-y-3">
      <button
        type="button"
        onClick={() => setAcik(true)}
        className="relative block w-full overflow-hidden rounded-2xl border border-teal-100"
      >
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img src={aktif} alt={baslik} className="h-[220px] w-full object-cover sm:h-[320px] md:h-[460px]" />
      </button>
      {gorseller.length > 1 ? (
        <div className="flex gap-2 overflow-x-auto">
          {gorseller.map((src, i) => (
            <button
              key={src}
              type="button"
              onClick={() => setSecili(i)}
              className={`h-16 w-24 shrink-0 overflow-hidden rounded-lg border ${
                i === secili ? "border-teal-700 ring-2 ring-teal-700/30" : "border-teal-100"
              }`}
            >
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img src={src} alt="" className="h-full w-full object-cover" />
            </button>
          ))}
        </div>
      ) : null}
      {acik ? (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center bg-deniz-derin/85 p-6"
          onClick={() => setAcik(false)}
          role="dialog"
          aria-modal
        >
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img
            src={aktif}
            alt={baslik}
            className="max-h-[90vh] max-w-full rounded-xl object-contain"
          />
        </div>
      ) : null}
    </div>
  );
}
