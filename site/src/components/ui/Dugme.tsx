import Link from "next/link";
import { cn } from "cn";

const VARYANT = {
  birincil:
    "bg-samandira text-white hover:bg-samandira-koyu focus-visible:ring-samandira",
  ikincil: "bg-deniz text-kopuk hover:bg-deniz-derin focus-visible:ring-deniz",
  hayalet:
    "border border-[color-mix(in_oklab,currentColor_40%,transparent)] bg-transparent hover:bg-white/10 focus-visible:ring-current",
} as const;

type Varyant = keyof typeof VARYANT;

type Ortak = {
  children: React.ReactNode;
  varyant?: Varyant;
  className?: string;
};

type LinkOzellik = Ortak & {
  href: string;
  dis?: boolean;
};

type DugmeOzellik = Ortak & {
  href?: undefined;
  type?: "button" | "submit";
  onClick?: () => void;
  disabled?: boolean;
};

const TABAN =
  "inline-flex min-h-11 cursor-pointer items-center justify-center rounded-full px-5 text-sm font-semibold tracking-tight transition-[background-color,color,box-shadow] duration-200 focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:outline-none disabled:pointer-events-none disabled:opacity-50";

export function Dugme(ozellik: LinkOzellik | DugmeOzellik) {
  const varyant = ozellik.varyant ?? "birincil";
  const sinif = cn(TABAN, VARYANT[varyant], ozellik.className);

  if ("href" in ozellik && ozellik.href) {
    if (ozellik.dis) {
      return (
        <a href={ozellik.href} className={sinif} target="_blank" rel="noreferrer">
          {ozellik.children}
        </a>
      );
    }
    return (
      <Link href={ozellik.href} className={sinif}>
        {ozellik.children}
      </Link>
    );
  }

  const dugme = ozellik as DugmeOzellik;
  return (
    <button
      type={dugme.type ?? "button"}
      className={sinif}
      onClick={dugme.onClick}
      disabled={dugme.disabled}
    >
      {dugme.children}
    </button>
  );
}
