import Link from "next/link";
import { ArrowRight } from "lucide-react";
import { cn } from "cn";
import { ODAK } from "@/lib/kart-sinif";
import { Spinner } from "./Spinner";

const VARYANT = {
  birincil:
    "dugme-birincil bg-samandira text-base font-semibold text-white hover:bg-samandira-koyu",
  ikincil:
    "border-bordo text-bordo hover:bg-kagit-koyu border bg-transparent text-base font-semibold",
  hayalet: "text-bordo hover:bg-kagit-koyu bg-transparent text-base font-semibold",
  metin:
    "text-bordo decoration-deniz hover:decoration-2 bg-transparent text-base font-medium underline decoration-1 underline-offset-4",
  bolum: "etiket text-bordo hover:bg-kagit-koyu gap-2 bg-transparent",
} as const;

type Varyant = keyof typeof VARYANT;

type Ortak = {
  children: React.ReactNode;
  varyant?: Varyant;
  className?: string;
  yukleniyor?: boolean;
  "aria-label"?: string;
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

const TABAN = cn(
  "inline-flex min-h-11 cursor-pointer items-center justify-center gap-2 rounded-[8px] px-5",
  "transition-[background-color,color,border-color,box-shadow,text-decoration-thickness] duration-[var(--sure-hizli)]",
  "disabled:pointer-events-none disabled:opacity-50",
  ODAK,
);

export function Dugme(ozellik: LinkOzellik | DugmeOzellik) {
  const varyant = ozellik.varyant ?? "birincil";
  const icerik = (
    <>
      {ozellik.yukleniyor ? <Spinner className="mr-2" /> : null}
      {ozellik.children}
      {varyant === "bolum" && !ozellik.yukleniyor ? (
        <ArrowRight className="size-3.5" aria-hidden="true" />
      ) : null}
    </>
  );
  const sinif = cn(TABAN, VARYANT[varyant], ozellik.className);

  if ("href" in ozellik && ozellik.href) {
    if (ozellik.dis) {
      return (
        <a
          href={ozellik.href}
          className={sinif}
          target="_blank"
          rel="noreferrer"
          aria-label={ozellik["aria-label"]}
        >
          {icerik}
        </a>
      );
    }
    return (
      <Link href={ozellik.href} className={sinif} aria-label={ozellik["aria-label"]}>
        {icerik}
      </Link>
    );
  }

  const dugme = ozellik as DugmeOzellik;
  return (
    <button
      type={dugme.type ?? "button"}
      className={sinif}
      onClick={dugme.onClick}
      disabled={dugme.disabled || dugme.yukleniyor}
      aria-label={dugme["aria-label"]}
    >
      {icerik}
    </button>
  );
}
