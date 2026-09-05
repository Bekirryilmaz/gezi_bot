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

export function SiteFooter() {
  return (
    <footer className="doku-koyu bg-bordo text-kagit">
      <div className="kabuk grid gap-10 py-16 md:grid-cols-4">
        <div>
          <KelimeKilidi
            boyut={40}
            yaziSinif="text-[22px] text-kagit"
            className="text-kagit"
          />
          <p className="text-kagit/80 mt-4 text-sm">{SLOGAN}</p>
          <p className="yazi-indeks text-kagit/70 mt-3 max-w-sm">{TANIM_CUMLESI}</p>
        </div>

        <div>
          <p className="etiket text-kagit/55">Sayfalar</p>
          <ul className="mt-4 space-y-2 text-sm">
            {SAYFALAR.map((s) => (
              <li key={s.href}>
                <Link
                  href={s.href}
                  className="text-kagit/85 hover:text-kagit focus-visible:ring-samandira decoration-kagit/0 hover:decoration-kagit/50 cursor-pointer underline underline-offset-4 transition-[text-decoration-color] duration-[var(--sure-hizli)] focus-visible:ring-2 focus-visible:outline-none"
                >
                  {s.ad}
                </Link>
              </li>
            ))}
          </ul>
        </div>

        <div>
          <p className="etiket text-kagit/55">Yasal</p>
          <p className="text-kagit/80 mt-4 text-sm">{STUDYO}</p>
          <p className="yazi-indeks text-kagit/65 mt-3">
            Gizlilik, kullanım koşulları ve iletişim sayfaları yayınlanınca burada yer
            alır.
          </p>
        </div>

        <div>
          <p className="etiket text-kagit/55">Güven</p>
          <p className="yazi-govde text-kagit/85 mt-4 text-[15px]">{GUVEN_CUMLESI}</p>
          <p className="text-kagit/65 mt-6 text-[11px] leading-relaxed">{OSM_ATFI}</p>
        </div>
      </div>
      <div className="border-kagit/14 border-t">
        <p className="kabuk text-kagit/60 py-4 text-[11px]">
          {MARKA_WORDMARK} · {STUDYO}
        </p>
      </div>
    </footer>
  );
}
