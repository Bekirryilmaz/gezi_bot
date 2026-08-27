import Link from "next/link";

type Props = {
  sehirAnahtari?: string;
};

export function SiteHeader({ sehirAnahtari = "samsun" }: Props) {
  return (
    <header className="absolute inset-x-0 top-0 z-20">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-5 py-5 md:px-8">
        <Link
          href="/"
          className="font-display text-2xl tracking-tight text-white drop-shadow-sm md:text-3xl"
        >
          ŞAMANDIRA
        </Link>
        <nav className="flex items-center gap-5 text-sm text-white/90 md:gap-7 md:text-base">
          <Link href="/hakkimizda" className="transition hover:text-white">
            Hakkımızda
          </Link>
          <Link href="/bolgeler" className="transition hover:text-white">
            Bölgeler
          </Link>
          <Link href="/kesfet" className="transition hover:text-white">
            Keşfet
          </Link>
          <Link href="/onerim-var" className="transition hover:text-white">
            Önerim Var
          </Link>
          <Link
            href={`/sehir/${sehirAnahtari}/rota`}
            className="rounded-full bg-white/15 px-3.5 py-1.5 backdrop-blur-sm transition hover:bg-white/25"
          >
            Rota Kur
          </Link>
        </nav>
      </div>
    </header>
  );
}
