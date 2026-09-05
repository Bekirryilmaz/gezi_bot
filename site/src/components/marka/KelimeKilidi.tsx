import Link from "next/link";
import { cn } from "cn";
import { MARKA_WORDMARK } from "@/lib/marka";
import { LogoKaro } from "./LogoKaro";

type Ozellik = {
  href?: string;
  boyut?: number;
  yaziSinif?: string;
  className?: string;
  yalnizIsaret?: boolean;
  mobilGizleYazi?: boolean;
  oncelik?: boolean;
};

/**
 * Kelime kilidi: karo + "şamandıra".
 * Bosluk = isaret kenarinin ~0.35 em'i. Minimum isaret 24px.
 */
export function KelimeKilidi({
  href = "/",
  boyut = 32,
  yaziSinif,
  className,
  yalnizIsaret = false,
  mobilGizleYazi = false,
  oncelik = false,
}: Ozellik) {
  const isaret = Math.max(boyut, 24);
  const icerik = (
    <>
      <LogoKaro boyut={isaret} dekoratif oncelik={oncelik} />
      {yalnizIsaret ? (
        <span className="sr-only">{MARKA_WORDMARK}</span>
      ) : (
        <span
          className={cn(
            "font-display leading-none tracking-[-0.02em]",
            mobilGizleYazi && "max-md:hidden",
            yaziSinif,
          )}
        >
          {MARKA_WORDMARK}
        </span>
      )}
    </>
  );

  const sinif = cn(
    "inline-flex cursor-pointer items-center gap-[0.35em] focus-visible:ring-2 focus-visible:ring-samandira focus-visible:outline-none",
    className,
  );

  if (href) {
    return (
      <Link href={href} className={sinif} aria-label="Şamandıra ana sayfa">
        {icerik}
      </Link>
    );
  }

  return <span className={sinif}>{icerik}</span>;
}
