import Link from "next/link";
import { cn } from "cn";
import { Rozet } from "./Rozet";

export function RehberKarti({
  baslik,
  ozet,
  href,
  etiket = "Rehber",
  className,
}: {
  baslik: string;
  ozet: string;
  href: string;
  etiket?: string;
  className?: string;
}) {
  return (
    <Link
      href={href}
      className={cn(
        "kart-isik group border-deniz/10 focus-visible:ring-samandira flex cursor-pointer flex-col rounded-2xl border bg-white p-6 transition-[transform] duration-200 hover:-translate-y-0.5 focus-visible:ring-2 focus-visible:outline-none",
        className,
      )}
    >
      <Rozet ton="sis">{etiket}</Rozet>
      <h3 className="font-display text-deniz-derin group-hover:text-deniz mt-3 text-2xl tracking-[-0.01em]">
        {baslik}
      </h3>
      <p className="text-ink/70 mt-2 text-sm leading-relaxed">{ozet}</p>
    </Link>
  );
}
