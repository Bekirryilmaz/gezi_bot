"use client";

import { useEffect, useRef, useState } from "react";
import Image from "next/image";
import { Quote } from "lucide-react";
import { ilberOrtayliQuotes } from "@/data/quotes";

const GECIKME_MS = 5000;

export function IlberQuotesSlider() {
  const [sira, setSira] = useState(0);
  const duraklat = useRef(false);
  const soz = ilberOrtayliQuotes[sira];

  useEffect(() => {
    const zaman = window.setInterval(() => {
      if (duraklat.current) return;
      setSira((onceki) => (onceki + 1) % ilberOrtayliQuotes.length);
    }, GECIKME_MS);
    return () => window.clearInterval(zaman);
  }, []);

  return (
    <section
      className="overflow-hidden rounded-2xl bg-deniz-derin text-kopuk shadow-[0_16px_40px_rgba(6,54,66,0.22)]"
      onMouseEnter={() => {
        duraklat.current = true;
      }}
      onMouseLeave={() => {
        duraklat.current = false;
      }}
      onFocusCapture={() => {
        duraklat.current = true;
      }}
      onBlurCapture={() => {
        duraklat.current = false;
      }}
    >
      <div className="grid gap-8 p-6 md:grid-cols-[minmax(140px,220px)_1fr] md:items-center md:p-10">
        <div className="mx-auto w-40 md:w-full">
          <div className="relative aspect-square overflow-hidden rounded-full border-4 border-kopuk/25 shadow-[0_8px_24px_rgba(0,0,0,0.28)]">
            <Image
              src="/hakkimizda/ilber-ortayli.jpg"
              alt="İlber Ortaylı"
              fill
              className="object-cover object-[center_18%]"
              sizes="220px"
              priority={false}
            />
          </div>
          <p className="mt-3 text-center font-display text-lg text-white">
            İlber Ortaylı
          </p>
          <p className="text-center text-xs text-kopuk/55">Tarihçi</p>
        </div>

        <div className="min-w-0">
          <p className="text-xs font-semibold uppercase tracking-[0.18em] text-kopuk/50">
            İlham köşesi
          </p>
          <div key={soz.id} className="alinti-kayma mt-4">
            <Quote
              className="h-7 w-7 text-yosun"
              aria-hidden
            />
            <blockquote
              className="mt-3 font-display text-xl leading-relaxed text-white md:text-2xl"
              aria-live="polite"
            >
              {soz.quote}
            </blockquote>
            <div className="mt-3 flex justify-end">
              <Quote className="h-6 w-6 rotate-180 text-yosun" aria-hidden />
            </div>
            <p className="mt-2 text-sm text-kopuk/60">— {soz.source}</p>
          </div>

          <div className="mt-6 flex gap-2" role="tablist" aria-label="Alıntılar">
            {ilberOrtayliQuotes.map((madde, i) => {
              const aktif = i === sira;
              return (
                <button
                  key={madde.id}
                  type="button"
                  role="tab"
                  aria-selected={aktif}
                  aria-label={`Alıntı ${i + 1}`}
                  onClick={() => setSira(i)}
                  className={`h-2.5 rounded-full transition ${
                    aktif ? "w-7 bg-yosun" : "w-2.5 bg-kopuk/30 hover:bg-kopuk/50"
                  }`}
                />
              );
            })}
          </div>
        </div>
      </div>
    </section>
  );
}
