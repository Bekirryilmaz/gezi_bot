"use client";

import Link from "next/link";

type Aktif = "blog" | "form";

export function OneriSekmeler({ aktif }: { aktif: Aktif }) {
  const tab =
    "flex min-h-[44px] flex-1 items-center justify-center gap-1.5 rounded-full px-4 py-2.5 text-center text-sm font-semibold transition";
  return (
    <div className="mt-8 flex w-full max-w-xl flex-col gap-2 rounded-2xl border border-white/20 bg-white/10 p-1 backdrop-blur-sm sm:flex-row sm:rounded-full sm:gap-0">
      <Link
        href="/oneriler"
        className={`${tab} ${
          aktif === "blog"
            ? "bg-yosun text-white shadow-sm"
            : "text-white/75 hover:text-white"
        }`}
        aria-current={aktif === "blog" ? "page" : undefined}
      >
        📖 Topluluk Önerileri & Blog
      </Link>
      <Link
        href="/onerim-var"
        className={`${tab} ${
          aktif === "form"
            ? "bg-yosun text-white shadow-sm"
            : "text-white/75 hover:text-white"
        }`}
        aria-current={aktif === "form" ? "page" : undefined}
      >
        ✍️ Bir Öneri Bırak
      </Link>
    </div>
  );
}
