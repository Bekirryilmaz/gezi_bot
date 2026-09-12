"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Menu } from "lucide-react";
import { CTA_BIRINCIL } from "@/lib/marka";
import { ODAK } from "@/lib/kart-sinif";
import { KelimeKilidi } from "@/components/marka/KelimeKilidi";
import { Dugme } from "@/components/ui/Dugme";
import { Markir } from "@/components/ui/Markir";
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet";

const NAV = [
  { href: (s: string) => `/sehir/${s}`, ad: "Keşfet" },
  { href: (s: string) => `/sehir/${s}/bolgeler`, ad: "Bölgeler" },
] as const;

export function SiteHeader({ sehirAnahtari = "samsun" }: { sehirAnahtari?: string }) {
  const yol = usePathname();
  const [menu, setMenu] = useState(false);
  const anaSayfa = yol === "/";
  const rotaHref = `/sehir/${sehirAnahtari}/rota`;

  return (
    <header
      data-ana={anaSayfa ? "1" : undefined}
      className="site-header text-ink fixed inset-x-0 top-0 z-50 h-14 md:h-16"
    >
      <div className="kabuk grid h-full grid-cols-[auto_1fr_auto] items-center gap-3">
        <KelimeKilidi
          oncelik
          boyut={40}
          yaziSinif="text-[24px] md:text-[28px]"
          className="text-ink min-h-11 [&_img]:size-9 md:[&_img]:size-10"
          mobilGizleYazi
        />
        <nav
          className="hidden items-center justify-center gap-1 md:flex"
          aria-label="Ana"
        >
          {NAV.map((n) => {
            const href = n.href(sehirAnahtari);
            const aktif = yol === href || yol.startsWith(`${href}/`);
            return (
              <Link
                key={n.ad}
                href={href}
                aria-current={aktif ? "page" : undefined}
                className={`inline-flex min-h-11 cursor-pointer items-center px-3 text-sm ${ODAK} ${
                  aktif ? "text-bordo font-medium" : "text-ink/80 hover:text-ink"
                }`}
              >
                <span className="relative">
                  {n.ad}
                  {aktif ? (
                    <span
                      className="nav-nokta bg-samandira absolute inset-x-0 -bottom-1 mx-auto size-1 rounded-full"
                      aria-hidden="true"
                    />
                  ) : null}
                </span>
              </Link>
            );
          })}
        </nav>
        <div className="flex items-center justify-end gap-1">
          <Dugme href={rotaHref} varyant="birincil" className="max-md:px-3">
            <Markir className="text-white md:hidden" boyut={14} />
            <span>{CTA_BIRINCIL}</span>
          </Dugme>
          <Sheet open={menu} onOpenChange={setMenu}>
            <SheetTrigger
              className={`${ODAK} hover:bg-kagit-koyu inline-flex size-11 cursor-pointer items-center justify-center rounded-[8px] md:hidden`}
              aria-label="Menüyü aç"
            >
              <Menu className="size-5" aria-hidden="true" />
            </SheetTrigger>
            <SheetContent
              side="right"
              className="bg-kagit text-ink border-bordo/12 w-72 border-l md:hidden"
            >
              <SheetHeader>
                <SheetTitle className="font-display text-bordo">Menü</SheetTitle>
              </SheetHeader>
              <nav className="flex flex-col gap-1 px-4" aria-label="Mobil">
                {NAV.map((n) => (
                  <Link
                    key={n.ad}
                    href={n.href(sehirAnahtari)}
                    className={`${ODAK} hover:bg-kagit-koyu inline-flex min-h-11 cursor-pointer items-center rounded-[8px] px-3 text-base`}
                    onClick={() => setMenu(false)}
                  >
                    {n.ad}
                  </Link>
                ))}
              </nav>
            </SheetContent>
          </Sheet>
        </div>
      </div>
    </header>
  );
}
