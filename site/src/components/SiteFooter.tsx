import Link from "next/link";

export function SiteFooter() {
  return (
    <footer className="bg-deniz-derin text-kopuk border-t border-[var(--cizgi)]">
      <div className="mx-auto flex max-w-6xl flex-col gap-3 px-5 py-10 md:flex-row md:items-end md:justify-between md:px-8">
        <div>
          <p className="font-display text-2xl">Şamandıra</p>
          <p className="text-kopuk/75 mt-2 max-w-md text-sm">
            Karadeniz’den başlayan kişisel gezi rotaları. Önce Samsun, sonra tüm kıyı.
          </p>
        </div>
        <Link href="/sehir/samsun/rota" className="text-gunes text-sm hover:underline">
          Kendi rotanı oluştur →
        </Link>
      </div>
    </footer>
  );
}
