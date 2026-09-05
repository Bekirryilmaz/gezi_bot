import { cn } from "cn";

export type IstatistikOge = {
  deger: string;
  etiket: string;
};

export function IstatistikBandi({
  ogeler,
  className,
}: {
  ogeler: IstatistikOge[];
  className?: string;
}) {
  return (
    <dl
      className={cn(
        "border-deniz/10 grid gap-6 border-y py-10 sm:grid-cols-3",
        className,
      )}
    >
      {ogeler.map((o) => (
        <div key={o.etiket} className="text-center">
          <dt className="text-kumsal text-[11px] tracking-[0.24em] uppercase">
            {o.etiket}
          </dt>
          <dd className="font-display text-deniz-derin mt-2 text-4xl tracking-[-0.02em] tabular-nums md:text-5xl">
            {o.deger}
          </dd>
        </div>
      ))}
    </dl>
  );
}
