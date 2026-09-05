import { cn } from "cn";
import { DUYGU_KUNYE } from "@/lib/marka";

export function DuyguOzeti({
  metin,
  etiket,
  className,
}: {
  metin: string;
  etiket?: string;
  className?: string;
}) {
  const acilis = metin.trim().split(/\s+/).slice(0, 8).join(" ");

  return (
    <blockquote
      className={cn("bg-bordo-900 text-kagit rounded-[12px] px-6 py-6", className)}
    >
      <p className="etiket text-kagit/55">{DUYGU_KUNYE}</p>
      {etiket ? <p className="etiket text-kagit/80 mt-3">{etiket}</p> : null}
      <p className="font-display mt-4 text-2xl leading-snug font-medium italic md:text-3xl">
        “{acilis}
        {acilis.length < metin.trim().length ? "…" : ""}”
      </p>
      <p className="yazi-govde text-kagit/80 mt-4">{metin}</p>
    </blockquote>
  );
}
