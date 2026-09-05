export function SayfaHero({
  etiket,
  baslik,
  ozet,
  children,
}: {
  etiket: string;
  baslik: string;
  ozet?: string;
  children?: React.ReactNode;
}) {
  return (
    <section className="bg-kagit text-ink pt-28 pb-16">
      <div className="mx-auto max-w-6xl px-5 md:px-8">
        <p className="text-ink/55 text-[11px] tracking-[0.24em] uppercase">{etiket}</p>
        <h1 className="font-display mt-3 max-w-3xl text-4xl leading-[1.05] tracking-[-0.02em] text-balance md:text-6xl">
          {baslik}
        </h1>
        {ozet ? (
          <p className="text-ink/75 mt-4 max-w-xl text-[15px] leading-relaxed text-pretty">
            {ozet}
          </p>
        ) : null}
        {children}
      </div>
      <div className="mt-8 flex items-center px-5 md:px-8" aria-hidden="true">
        <span className="bg-ink/15 h-px flex-1" />
        <span className="bg-samandira mx-1.5 size-1.5 rounded-full" />
        <span className="bg-ink/15 h-px flex-1" />
      </div>
    </section>
  );
}
