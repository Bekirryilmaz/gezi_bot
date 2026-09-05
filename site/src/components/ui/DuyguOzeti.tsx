import { cn } from "cn";
import { Rozet } from "./Rozet";

export function DuyguOzeti({
  metin,
  etiket,
  className,
}: {
  metin: string;
  etiket?: string;
  className?: string;
}) {
  return (
    <blockquote
      className={cn(
        "border-samandira/70 bg-kagit-koyu/40 border-l-2 py-1 pl-5",
        className,
      )}
    >
      {etiket ? (
        <Rozet ton="yosun" className="mb-3">
          {etiket}
        </Rozet>
      ) : null}
      <p className="font-display text-deniz-derin text-xl leading-relaxed italic md:text-2xl">
        {metin}
      </p>
    </blockquote>
  );
}
