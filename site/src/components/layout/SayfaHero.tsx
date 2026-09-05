import { KesilenAyrac } from "@/components/ui/KesilenAyrac";

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
    <section className="bg-kagit text-ink pt-28 pb-12 md:pb-16">
      <div className="kabuk">
        <p className="etiket text-ink/55">{etiket}</p>
        <h1 className="yazi-bolum text-bordo mt-3 max-w-3xl">{baslik}</h1>
        {ozet ? (
          <p className="yazi-govde text-ink/75 mt-4 max-w-[42rem]">{ozet}</p>
        ) : null}
        {children}
      </div>
      <KesilenAyrac className="mt-10" />
    </section>
  );
}
