"use client";

import dynamic from "next/dynamic";

export const MiniKonumHaritasiYukle = dynamic(
  () => import("./MiniKonumHaritasi").then((m) => m.MiniKonumHaritasi),
  {
    ssr: false,
    loading: () => (
      <div className="flex h-full min-h-[280px] w-full items-center justify-center rounded-2xl bg-deniz-derin text-sm text-kopuk/70">
        Harita yükleniyor…
      </div>
    ),
  },
);
