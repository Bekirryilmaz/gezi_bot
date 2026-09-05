import Link from "next/link";
import { cn } from "cn";

export function FiltreCip({
  href,
  aktif,
  children,
  sayi,
}: {
  href: string;
  aktif: boolean;
  children: React.ReactNode;
  sayi?: number;
}) {
  return (
    <Link
      href={href}
      className={cn(
        "focus-visible:ring-samandira inline-flex min-h-11 cursor-pointer items-center gap-2 rounded-full px-4 text-sm transition-colors duration-200 focus-visible:ring-2 focus-visible:outline-none",
        aktif ? "bg-deniz text-kopuk" : "text-ink bg-white/80 hover:bg-white",
      )}
      aria-current={aktif ? "page" : undefined}
    >
      {children}
      {sayi != null ? (
        <span
          className={cn(
            "rounded-full px-1.5 text-[11px] tabular-nums",
            aktif ? "bg-white/20" : "bg-deniz/10 text-deniz",
          )}
        >
          {sayi}
        </span>
      ) : null}
    </Link>
  );
}
