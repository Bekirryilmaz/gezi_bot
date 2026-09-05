import Image from "next/image";
import { cn } from "cn";

export type PlakaOran = "kart" | "hero" | "genis" | "dikey";

const ORAN: Record<PlakaOran, string> = {
  kart: "aspect-[16/10]",
  hero: "aspect-[4/5] md:h-[min(78vh,640px)] md:aspect-auto",
  genis: "aspect-[16/10] md:aspect-[2/1]",
  dikey: "aspect-[4/5]",
};

function KategoriIsareti({ kategori }: { kategori?: string }) {
  if (kategori === "yeme_icme") {
    return <circle cx="12" cy="12" r="6" />;
  }
  if (kategori === "konaklama") {
    return <rect x="6" y="6" width="12" height="12" rx="2" />;
  }
  return <rect x="6" y="6" width="12" height="12" />;
}

export function Plaka({
  kaynak,
  alt = "",
  oran = "kart",
  etiket,
  rozet,
  kategori,
  oncelik = false,
  kenarli = true,
  className,
}: {
  kaynak?: string | null;
  alt?: string;
  oran?: PlakaOran;
  etiket?: React.ReactNode;
  rozet?: React.ReactNode;
  kategori?: string;
  oncelik?: boolean;
  kenarli?: boolean;
  className?: string;
}) {
  const fotograf = Boolean(kaynak?.startsWith("/"));
  const scrim = Boolean(fotograf && (etiket || rozet));

  return (
    <div
      className={cn(
        "relative w-full overflow-hidden",
        kenarli ? "rounded-[4px]" : "rounded-none",
        ORAN[oran],
        className,
      )}
    >
      {fotograf && kaynak ? (
        <Image
          src={kaynak}
          alt={alt}
          fill
          sizes="(max-width: 768px) 100vw, (max-width: 1280px) 50vw, 400px"
          className="object-cover"
          priority={oncelik}
        />
      ) : (
        <div className="plaka-izgara absolute inset-0" aria-hidden="true">
          <svg
            width="24"
            height="24"
            viewBox="0 0 24 24"
            className="text-bordo/35 absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2"
            fill="none"
            stroke="currentColor"
            strokeWidth="1"
          >
            <KategoriIsareti kategori={kategori} />
          </svg>
        </div>
      )}
      {scrim ? (
        <div
          className="from-bordo-950/70 pointer-events-none absolute inset-x-0 bottom-0 h-[70%] bg-gradient-to-t to-transparent"
          aria-hidden="true"
        />
      ) : null}
      {rozet ? <div className="absolute top-3 right-3 z-10">{rozet}</div> : null}
      {etiket ? (
        <div
          className={cn(
            "absolute bottom-3 left-3 z-10 min-w-0",
            fotograf ? "text-white" : "text-ink/70",
          )}
        >
          {etiket}
        </div>
      ) : null}
    </div>
  );
}
