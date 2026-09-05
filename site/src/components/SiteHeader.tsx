"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Menu } from "lucide-react";
import { CTA_BIRINCIL } from "@/lib/marka";
import { KelimeKilidi } from "@/components/marka/KelimeKilidi";
import { Dugme } from "@/components/ui/Dugme";
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

  return (
    <header
      data-ana={anaSayfa ? "1" : undefined}
      className="site-header text-ink fixed inset-x-0 top-0 z-50"
    >
      <div className="mx-auto flex h-16 max-w-6xl items-center justify-between gap-4 px-5 md:px-8">
        <KelimeKilidi
          oncelik
          yaziSinif="text-[22px] md:text-[24px]"
          className="text-ink min-h-11"
          mobilGizleYazi
        />
        <nav className="hidden items-center gap-1 md:flex">
          {NAV.map((n) => {
            const href = n.href(sehirAnahtari);
            const aktif = yol === href || yol.startsWith(`${href}/`);
            return (
              <Link
                key={n.ad}
                href={href}
                className={`focus-visible:ring-samandira inline-flex min-h-11 cursor-pointer items-center px-3 text-sm transition-colors duration-200 hover:opacity-100 focus-visible:ring-2 focus-visible:outline-none ${
                  aktif ? "font-semibold" : "opacity-80"
                }`}
              >
                <span className="relative">
                  {n.ad}
                  {aktif ? (
                    <span
                      className="bg-samandira absolute inset-x-0 -bottom-1 mx-auto size-1 rounded-full"
                      aria-hidden="true"
                    />
                  ) : null}
                </span>
              </Link>
            );
          })}
          <Dugme
            href={`/sehir/${sehirAnahtari}/rota`}
            varyant="birincil"
            className="ml-2"
          >
            {CTA_BIRINCIL}
          </Dugme>
        </nav>

        <Sheet open={menu} onOpenChange={setMenu}>
          <SheetTrigger
            className="focus-visible:ring-samandira hover:bg-kagit-koyu inline-flex size-11 cursor-pointer items-center justify-center rounded-lg focus-visible:ring-2 focus-visible:outline-none md:hidden"
            aria-label="Menüyü aç"
          >
            <Menu className="size-5" aria-hidden="true" />
          </SheetTrigger>
          <SheetContent
            side="right"
            className="bg-kagit text-ink w-72 border-l md:hidden"
          >
            <SheetHeader>
              <SheetTitle>Menü</SheetTitle>
            </SheetHeader>
            <nav className="flex flex-col gap-1 px-4">
              {NAV.map((n) => (
                <Link
                  key={n.ad}
                  href={n.href(sehirAnahtari)}
                  className="hover:bg-kagit-koyu inline-flex min-h-11 cursor-pointer items-center rounded-lg px-3 text-base"
                  onClick={() => setMenu(false)}
                >
                  {n.ad}
                </Link>
              ))}
              <Dugme
                href={`/sehir/${sehirAnahtari}/rota`}
                varyant="birincil"
                className="mt-3"
              >
                {CTA_BIRINCIL}
              </Dugme>
            </nav>
          </SheetContent>
        </Sheet>
      </div>
    </header>
  );
}
