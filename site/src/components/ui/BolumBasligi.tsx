import { cn } from "cn";
import { LogoKaro } from "@/components/marka/LogoKaro";
import { Dugme } from "./Dugme";

export function BolumBasligi({
  etiket,
  baslik,
  ozet,
  aksiyon,
  id,
  koyu = false,
  className,
}: {
  etiket?: string;
  baslik: string;
  ozet?: string;
  aksiyon?: { href: string; etiket: string };
  id?: string;
  /** Koyu murekkep bandi: baslik kagit, bordo zemin olarak kalir. */
  koyu?: boolean;
  className?: string;
}) {
  const cipa = id ?? baslik.toLocaleLowerCase("tr-TR").replaceAll(" ", "-");

  return (
    <header className={cn("xl:grid xl:grid-cols-12 xl:gap-6", className)}>
      {etiket ? (
        <div className="mb-3 flex items-center gap-2 xl:col-span-1 xl:mb-0 xl:flex-col xl:items-start xl:gap-3 xl:pt-3">
          <LogoKaro boyut={16} dekoratif className="size-4" />
          <p className={cn("etiket", koyu ? "text-kagit/45" : "text-ink/55")}>{etiket}</p>
        </div>
      ) : (
        <span className="hidden xl:col-span-1 xl:block" />
      )}
      <div className="min-w-0 xl:col-span-10">
        <div className="flex flex-wrap items-end justify-between gap-4">
          <h2
            id={cipa}
            className={cn("yazi-bolum min-w-0", koyu ? "text-kagit" : "text-bordo")}
          >
            {baslik}
          </h2>
          {aksiyon ? (
            <Dugme
              href={aksiyon.href}
              varyant="bolum"
              className={cn("shrink-0", koyu && "text-kagit hover:bg-bordo-700")}
            >
              {aksiyon.etiket}
            </Dugme>
          ) : null}
        </div>
        {ozet ? (
          <p
            className={cn(
              "yazi-govde mt-4 max-w-[42rem]",
              koyu ? "text-kagit/75" : "text-ink/70",
            )}
          >
            {ozet}
          </p>
        ) : null}
      </div>
    </header>
  );
}
