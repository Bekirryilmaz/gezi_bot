"use client";

import dynamic from "next/dynamic";

export const TurkeyMapYukle = dynamic(
  () => import("./TurkeyMap").then((m) => m.TurkeyMap),
  {
    ssr: false,
    loading: () => (
      <div
        className="flex h-full min-h-[420px] w-full items-center justify-center bg-deniz-derin text-sm text-kopuk/70"
        aria-busy="true"
      >
        Harita yükleniyor…
      </div>
    ),
  },
);
