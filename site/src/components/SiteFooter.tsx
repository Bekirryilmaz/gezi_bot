import Link from "next/link";
import {
  GUVEN_CUMLESI,
  MARKA_WORDMARK,
  OSM_ATFI,
  SLOGAN,
  STUDYO,
  TANIM_CUMLESI,
} from "@/lib/marka";
import { KelimeKilidi } from "@/components/marka/KelimeKilidi";

const SAYFALAR = [
  { href: "/sehir/samsun", ad: "Keşfet" },
  { href: "/sehir/samsun/bolgeler", ad: "Bölgeler" },
  { href: "/sehir/samsun/rota", ad: "Rota planlayıcı" },
] as const;

export function SiteFooter() {
  return (
    <footer className="bg-deniz-derin text-kopuk">
      <div className="mx-auto grid max-w-6xl gap-10 px-5 py-14 md:grid-cols-4 md:px-8">
        <div className="md:col-span-1">
          <KelimeKilidi yaziSinif="text-[22px] text-kopuk" className="text-kopuk" />
          <p className="text-kopuk/70 mt-3 text-sm">{SLOGAN}</p>
          <p className="text-kopuk/80 mt-3 text-xs leading-relaxed">{TANIM_CUMLESI}</p>
        </div>

        <div>
          <p className="text-kumsal text-[11px] tracking-[0.24em] uppercase">Sayfalar</p>
          <ul className="mt-3 space-y-2 text-sm">
            {SAYFALAR.map((s) => (
              <li key={s.href}>
                <Link
                  href={s.href}
                  className="text-kopuk/80 hover:text-kopuk focus-visible:ring-samandira cursor-pointer focus-visible:ring-2 focus-visible:outline-none"
                >
                  {s.ad}
                </Link>
              </li>
            ))}
          </ul>
        </div>

        <div>
          <p className="text-kumsal text-[11px] tracking-[0.24em] uppercase">Stüdyo</p>
          <p className="text-kopuk/80 mt-3 text-sm">{STUDYO}</p>
          <p className="text-kopuk/80 mt-2 text-xs leading-relaxed">
            Yasal sayfalar (gizlilik, iletişim) yayın öncesi eklenecek — ölü bağlantı yok.
          </p>
        </div>

        <div>
          <p className="text-kumsal text-[11px] tracking-[0.24em] uppercase">Güven</p>
          <p className="text-kopuk/80 mt-3 text-sm leading-relaxed">{GUVEN_CUMLESI}</p>
          <p className="text-kopuk/75 mt-4 text-[11px] leading-relaxed">{OSM_ATFI}</p>
        </div>
      </div>
      <div className="border-t border-white/10">
        <p className="text-kopuk/70 mx-auto max-w-6xl px-5 py-4 text-[11px] md:px-8">
          {MARKA_WORDMARK} · {STUDYO}
        </p>
      </div>
    </footer>
  );
}
