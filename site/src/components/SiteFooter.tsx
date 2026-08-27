import Link from "next/link";

export function SiteFooter() {
  return (
    <footer className="border-t border-bordo/20 bg-deniz-derin text-kopuk">
      <div className="mx-auto flex max-w-6xl flex-col gap-3 px-5 py-10 md:flex-row md:items-end md:justify-between md:px-8">
        <div>
          <p className="font-display text-2xl">ŞAMANDIRA</p>
          <p className="mt-2 max-w-md text-sm text-kopuk/75">
            Karadeniz kıyısında kişisel gezi rotaları. Önce Samsun, sonra tüm kıyı.
          </p>
        </div>
        <div className="flex flex-wrap gap-4 text-sm">
          <Link href="/onerim-var" className="text-kopuk/80 hover:text-gunes">
            Önerim Var
          </Link>
          <Link href="/kesfet" className="text-kopuk/80 hover:text-gunes">
            İlçeleri keşfet
          </Link>
          <Link href="/sehir/samsun/rota" className="text-gunes hover:underline">
            Kendi Rotanı Oluştur →
          </Link>
        </div>
      </div>
    </footer>
  );
}
