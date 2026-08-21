import Link from "next/link";

export function SiteFooter() {
  return (
    <footer className="border-t border-[var(--cizgi)] bg-deniz-derin text-kopuk">
      <div className="mx-auto flex max-w-6xl flex-col gap-3 px-5 py-10 md:flex-row md:items-end md:justify-between md:px-8">
        <div>
          <p className="font-display text-2xl">Rotam</p>
          <p className="mt-2 max-w-md text-sm text-kopuk/75">
            Karadeniz’den başlayan kişisel gezi rotaları. Önce Samsun, sonra tüm kıyı.
          </p>
        </div>
        <Link href="/sehir/samsun/rota" className="text-sm text-gunes hover:underline">
          Kendi rotanı oluştur →
        </Link>
      </div>
    </footer>
  );
}
