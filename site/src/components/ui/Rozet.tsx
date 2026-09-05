import { cn } from "cn";

type Ton = "deniz" | "samandira" | "signal" | "yosun" | "sis";

const TON: Record<Ton, string> = {
  deniz: "bg-deniz/12 text-deniz",
  samandira: "bg-samandira/12 text-samandira-koyu",
  signal: "bg-signal text-deniz-derin",
  yosun: "bg-yosun/12 text-yosun",
  sis: "bg-kagit-koyu text-ink/70",
};

export function Rozet({
  children,
  ton = "deniz",
  className,
}: {
  children: React.ReactNode;
  ton?: Ton;
  className?: string;
}) {
  return (
    <span
      className={cn(
        "inline-flex min-h-7 items-center rounded-full px-2.5 text-[11px] font-medium tracking-wide",
        TON[ton],
        className,
      )}
    >
      {children}
    </span>
  );
}
