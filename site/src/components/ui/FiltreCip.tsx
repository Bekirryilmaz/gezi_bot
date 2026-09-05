import Link from "next/link";
import { cn } from "cn";
import { ODAK } from "@/lib/kart-sinif";

export function FiltreCip({
  href,
  aktif,
  children,
  sayi,
  disabled,
}: {
  href: string;
  aktif: boolean;
  children: React.ReactNode;
  sayi?: number;
  disabled?: boolean;
}) {
  const devreDisi = disabled || sayi === 0;
  const sinif = cn(
    "inline-flex min-h-11 cursor-pointer items-center gap-2 rounded-full border px-4 text-sm",
    "transition-[background-color,border-color,color] duration-[var(--sure-hizli)]",
    ODAK,
    aktif
      ? "border-samandira bg-samandira/10 text-ink"
      : "border-bordo/12 text-ink bg-tuz hover:border-bordo/40",
    devreDisi && "cursor-not-allowed opacity-50 hover:border-bordo/12",
  );

  const icerik = (
    <>
      {aktif ? (
        <span className="bg-samandira size-1 shrink-0 rounded-full" aria-hidden="true" />
      ) : null}
      <span className="min-w-0">{children}</span>
      {sayi != null ? (
        <span className="text-ink/55 text-[11px] tabular-nums">{sayi}</span>
      ) : null}
    </>
  );

  if (devreDisi) {
    return (
      <span className={sinif} aria-disabled="true">
        {icerik}
      </span>
    );
  }

  return (
    <Link href={href} className={sinif} aria-current={aktif ? "page" : undefined}>
      {icerik}
    </Link>
  );
}
