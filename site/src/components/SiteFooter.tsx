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
  { href: "/", ad: "Ana sayfa" },
  { href: "/sehir/samsun", ad: "Keşfet" },
  { href: "/sehir/samsun/bolgeler", ad: "Bölgeler" },
  { href: "/sehir/samsun/rota", ad: "Rota planlayıcı" },
] as const;

const BAG_SINIF =
  "text-ink/75 hover:text-bordo focus-visible:ring-samandira decoration-bordo/0 hover:decoration-bordo/45 cursor-pointer underline underline-offset-4 transition-[color,text-decoration-color] duration-[var(--sure-hizli)] focus-visible:ring-2 focus-visible:outline-none";

/**
 * V1: alt bant koyu bordo blok DEGIL — kagit (tuz) zemin + murekkep metin.
 * Bordo yalnizca marka karosunda, baslik etiketlerinde ve bag hover'inda.
 */
export function SiteFooter() {
  return (
    <footer className="doku-kagit bg-tuz border-bordo/12 border-t">
      <div className="kabuk grid gap-10 py-16 md:grid-cols-4">
        <div>
          <KelimeKilidi boyut={40} yaziSinif="text-[22px] text-bordo" />
          <p className="text-ink/80 mt-4 text-sm">{SLOGAN}</p>
          <p className="yazi-indeks text-ink/65 mt-3 max-w-sm">{TANIM_CUMLESI}</p>
        </div>

        <div>
          <p className="etiket text-bordo/70">Sayfalar</p>
          <ul className="mt-4 space-y-2 text-sm">
            {SAYFALAR.map((s) => (
              <li key={s.href}>
                <Link href={s.href} className={BAG_SINIF}>
                  {s.ad}
                </Link>
              </li>
            ))}
          </ul>
        </div>

        <div>
          <p className="etiket text-bordo/70">Yasal</p>
          <p className="text-ink/80 mt-4 text-sm">{STUDYO}</p>
          <p className="yazi-indeks text-ink/60 mt-3">
            Gizlilik, kullanım koşulları ve iletişim sayfaları yayınlanınca burada yer
            alır.
          </p>
        </div>

        <div>
          <p className="etiket text-bordo/70">Güven</p>
          <p className="yazi-govde text-ink/85 mt-4 text-[15px]">{GUVEN_CUMLESI}</p>
          <p className="text-ink/55 mt-6 text-[11px] leading-relaxed">{OSM_ATFI}</p>
        </div>
      </div>
      <div className="border-bordo/12 border-t">
        <p className="kabuk text-ink/55 py-4 text-[11px]">
          {MARKA_WORDMARK} · {STUDYO}
        </p>
      </div>
    </footer>
  );
}
