"use client";

import { useEffect, useId, useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Menu, X } from "lucide-react";

type Props = {
  sehirAnahtari?: string;
};

const NAV = [
  { href: "/hakkimizda", etiket: "Hakkımızda" },
  { href: "/bolgeler", etiket: "Bölgeler" },
  { href: "/kesfet", etiket: "Keşfet" },
  { href: "/oneriler", etiket: "Önerim Var" },
] as const;

export function SiteHeader({ sehirAnahtari = "samsun" }: Props) {
  const [acik, setAcik] = useState(false);
  const pathname = usePathname();
  const panelId = useId();
  const rotaHref = `/sehir/${sehirAnahtari}/rota`;

  useEffect(() => {
    setAcik(false);
  }, [pathname]);

  useEffect(() => {
    if (!acik) return;
    const onceki = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    function kac(e: KeyboardEvent) {
      if (e.key === "Escape") setAcik(false);
    }
    document.addEventListener("keydown", kac);
    return () => {
      document.body.style.overflow = onceki;
      document.removeEventListener("keydown", kac);
    };
  }, [acik]);

  return (
    <header className="absolute inset-x-0 top-0 z-50 max-w-full">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-4 md:px-8 md:py-5">
        <Link
          href="/"
          className="font-display text-2xl tracking-tight text-white drop-shadow-sm md:text-3xl"
        >
          ŞAMANDIRA
        </Link>

        <nav className="hidden items-center gap-7 text-base text-white/90 md:flex">
          {NAV.map((oge) => (
            <Link
              key={oge.href}
              href={oge.href}
              className="min-h-[44px] inline-flex items-center transition hover:text-white"
            >
              {oge.etiket}
            </Link>
          ))}
          <Link
            href={rotaHref}
            className="inline-flex min-h-[44px] items-center rounded-full bg-white/15 px-3.5 py-1.5 backdrop-blur-sm transition hover:bg-white/25"
          >
            Rota Kur
          </Link>
        </nav>

        <button
          type="button"
          className="inline-flex min-h-[44px] min-w-[44px] items-center justify-center rounded-xl text-white md:hidden"
          aria-expanded={acik}
          aria-controls={panelId}
          aria-label={acik ? "Menüyü kapat" : "Menüyü aç"}
          onClick={() => setAcik((v) => !v)}
        >
          {acik ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
        </button>
      </div>

      {acik ? (
        <div className="fixed inset-0 z-[60] md:hidden">
          <button
            type="button"
            className="absolute inset-0 bg-deniz-derin/55"
            aria-label="Menüyü kapat"
            onClick={() => setAcik(false)}
          />
          <nav
            id={panelId}
            className="absolute inset-y-0 right-0 flex w-[min(100%,20rem)] flex-col bg-deniz-derin px-6 pb-10 pt-20 text-white shadow-[-12px_0_40px_rgba(6,54,66,0.35)]"
          >
            <button
              type="button"
              className="absolute right-4 top-4 inline-flex min-h-[44px] min-w-[44px] items-center justify-center rounded-xl"
              aria-label="Menüyü kapat"
              onClick={() => setAcik(false)}
            >
              <X className="h-6 w-6" />
            </button>
            {NAV.map((oge) => (
              <Link
                key={oge.href}
                href={oge.href}
                className="flex min-h-[48px] items-center border-b border-white/10 text-lg"
                onClick={() => setAcik(false)}
              >
                {oge.etiket}
              </Link>
            ))}
            <Link
              href={rotaHref}
              className="mt-6 inline-flex min-h-[44px] items-center justify-center rounded-full bg-white/15 px-4 py-2.5 text-center font-semibold backdrop-blur-sm"
              onClick={() => setAcik(false)}
            >
              Rota Kur
            </Link>
          </nav>
        </div>
      ) : null}
    </header>
  );
}
