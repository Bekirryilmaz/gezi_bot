import { cn } from "cn";
import { IstatistikSayac } from "./IstatistikSayac";

export type IstatistikOge = {
  deger: number;
  etiket: string;
  baglam?: string;
};

export function IstatistikBandi({
  ogeler,
  className,
}: {
  ogeler: IstatistikOge[];
  className?: string;
}) {
  if (ogeler.length < 3) return null;

  return (
    <dl
      className={cn(
        "border-bordo/12 grid gap-8 border-y py-10 sm:grid-cols-3",
        className,
      )}
    >
      {ogeler.map((o) => (
        <div key={o.etiket} className="text-center">
          <dt className="etiket text-ink/55">{o.etiket}</dt>
          <dd className="yazi-sayi text-bordo mt-3">
            <IstatistikSayac deger={o.deger} />
          </dd>
          {o.baglam ? <p className="text-ink/55 mt-2 text-sm">{o.baglam}</p> : null}
        </div>
      ))}
    </dl>
  );
}
