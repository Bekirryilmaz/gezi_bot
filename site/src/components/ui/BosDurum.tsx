import { cn } from "cn";
import { BOS_LISTE } from "@/lib/marka";
import { Dugme } from "./Dugme";

export function BosDurum({
  baslik = "Burada henüz bir şey yok",
  metin = BOS_LISTE,
  cta,
  className,
}: {
  baslik?: string;
  metin?: string;
  cta?: { href: string; etiket: string };
  className?: string;
}) {
  return (
    <div
      className={cn(
        "border-deniz/20 bg-kagit rounded-2xl border border-dashed px-6 py-14 text-center",
        className,
      )}
    >
      <p className="font-display text-deniz-derin text-2xl">{baslik}</p>
      <p className="text-ink/65 mx-auto mt-3 max-w-md text-sm leading-relaxed">{metin}</p>
      {cta ? (
        <div className="mt-6">
          <Dugme href={cta.href} varyant="ikincil">
            {cta.etiket}
          </Dugme>
        </div>
      ) : null}
    </div>
  );
}
