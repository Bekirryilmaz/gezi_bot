import { cn } from "cn";

export type RozetTur = "sponsorlu" | "klasik" | "kategori" | "skor" | "durum";

const TUR: Record<RozetTur, string> = {
  sponsorlu: "bg-signal text-ink",
  klasik: "border-deniz text-deniz border bg-transparent",
  kategori: "bg-kagit-koyu text-ink",
  skor: "border-bordo/20 text-ink border bg-transparent tabular-nums",
  durum: "border-bordo/20 text-ink/70 border bg-transparent font-medium",
};

export function Rozet({
  children,
  tur = "kategori",
  className,
}: {
  children: React.ReactNode;
  tur?: RozetTur;
  className?: string;
}) {
  return (
    <span
      className={cn(
        "etiket inline-flex min-h-7 items-center rounded-full px-2.5",
        TUR[tur],
        className,
      )}
    >
      {children}
    </span>
  );
}

export function RozetKati({
  ogeler,
  limit = 2,
  className,
}: {
  ogeler: React.ReactNode[];
  limit?: number;
  className?: string;
}) {
  const gorunen = ogeler.slice(0, limit);
  const fazla = ogeler.length - gorunen.length;

  return (
    <div
      className={cn(
        "flex h-7 min-h-7 items-center gap-1.5 overflow-hidden whitespace-nowrap",
        className,
      )}
    >
      {gorunen}
      {fazla > 0 ? <Rozet tur="durum">+{fazla}</Rozet> : null}
    </div>
  );
}
