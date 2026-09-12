import { cn } from "cn";
import { IstatistikSayac } from "./IstatistikSayac";

export type IstatistikOge = {
  deger: number;
  etiket: string;
  baglam?: string;
};

export function IstatistikBandi({
  ogeler,
  koyu = false,
  className,
}: {
  ogeler: IstatistikOge[];
  /** Koyu murekkep bandinda kullanilir: hairline ve metin tonlari tersine doner. */
  koyu?: boolean;
  className?: string;
}) {
  if (ogeler.length < 3) return null;

  return (
    <dl
      className={cn(
        "grid gap-8 border-y py-10 sm:grid-cols-3",
        koyu
          ? "border-kagit/14 divide-kagit/10 sm:divide-x"
          : "border-bordo/12 divide-bordo/10 sm:divide-x",
        className,
      )}
    >
      {ogeler.map((o) => (
        <div key={o.etiket} className="text-center">
          <dt className={cn("etiket", koyu ? "text-kagit/55" : "text-ink/55")}>
            {o.etiket}
          </dt>
          <dd className={cn("yazi-sayi mt-3", koyu ? "text-kagit" : "text-bordo")}>
            <IstatistikSayac deger={o.deger} />
          </dd>
          {o.baglam ? (
            <p className={cn("mt-2 text-sm", koyu ? "text-kagit/60" : "text-ink/55")}>
              {o.baglam}
            </p>
          ) : null}
        </div>
      ))}
    </dl>
  );
}
