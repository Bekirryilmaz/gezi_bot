import { cn } from "cn";

/** Bos durum ufku: tek hairline + tek nokta. */
export function UfukCizgisiBos({ className }: { className?: string }) {
  return (
    <div className={cn("relative mx-auto mb-8 w-28", className)} aria-hidden="true">
      <span className="bg-samandira absolute -top-1 left-1/2 size-1 -translate-x-1/2 rounded-full" />
      <span className="bg-bordo/20 block h-px w-full" />
    </div>
  );
}
