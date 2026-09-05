import { cn } from "cn";
import { Dugme } from "./Dugme";

export function BolumBasligi({
  etiket,
  baslik,
  ozet,
  aksiyon,
  id,
  className,
}: {
  etiket?: string;
  baslik: string;
  ozet?: string;
  aksiyon?: { href: string; etiket: string };
  id?: string;
  className?: string;
}) {
  const cipa = id ?? baslik.toLocaleLowerCase("tr-TR").replaceAll(" ", "-");

  return (
    <header className={cn("xl:grid xl:grid-cols-12 xl:gap-6", className)}>
      {etiket ? (
        <p className="etiket text-ink/55 mb-3 xl:col-span-1 xl:mb-0 xl:pt-3">{etiket}</p>
      ) : (
        <span className="hidden xl:col-span-1 xl:block" />
      )}
      <div className="min-w-0 xl:col-span-10">
        <div className="flex flex-wrap items-end justify-between gap-4">
          <h2 id={cipa} className="yazi-bolum text-bordo min-w-0">
            {baslik}
          </h2>
          {aksiyon ? (
            <Dugme href={aksiyon.href} varyant="bolum" className="shrink-0">
              {aksiyon.etiket}
            </Dugme>
          ) : null}
        </div>
        {ozet ? (
          <p className="yazi-govde text-ink/70 mt-4 max-w-[42rem]">{ozet}</p>
        ) : null}
      </div>
    </header>
  );
}
