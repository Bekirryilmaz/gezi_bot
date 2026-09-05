import { cn } from "cn";

export function BolumBasligi({
  etiket,
  baslik,
  ozet,
  className,
}: {
  etiket?: string;
  baslik: string;
  ozet?: string;
  className?: string;
}) {
  return (
    <header className={cn("max-w-2xl", className)}>
      {etiket ? (
        <p className="text-kumsal text-[11px] font-medium tracking-[0.24em] uppercase">
          {etiket}
        </p>
      ) : null}
      <h2 className="font-display text-deniz-derin mt-2 text-4xl leading-[1.08] tracking-[-0.02em] md:text-5xl">
        {baslik}
      </h2>
      {ozet ? (
        <p className="text-ink/70 mt-4 text-[15px] leading-relaxed">{ozet}</p>
      ) : null}
    </header>
  );
}
