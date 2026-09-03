import Link from "next/link";
import { SiteHeader } from "@/components/SiteHeader";
import { YerSatiri } from "@/components/YerSatiri";
import { KesfetPaneli } from "@/components/discovery/KesfetPaneli";
import { sehirleriGetir, yerleriGetir } from "@/lib/api";
import { IL_SECICI_ACIK } from "@/lib/kesfetOzellik";
import { ANA_KATEGORILER } from "@/lib/sabitler";

type Props = {
  params: Promise<{ anahtar: string }>;
  searchParams: Promise<{ kategori?: string }>;
};

export async function generateMetadata({ params }: Props) {
  const { anahtar } = await params;
  const sehirler = await sehirleriGetir().catch(() => []);
  const sehir = sehirler.find((s) => s.anahtar === anahtar);
  return {
    title: sehir ? `${sehir.isim} Keşif` : "Keşif",
  };
}

export default async function SehirKesifSayfasi({ params, searchParams }: Props) {
  const { anahtar } = await params;
  const { kategori } = await searchParams;

  const [sehirler, liste] = await Promise.all([
    sehirleriGetir().catch(() => []),
    yerleriGetir(anahtar, {
      anaKategori: kategori,
      limit: 60,
    }).catch(() => ({ yerler: [], toplam_sayi: 0 })),
  ]);
  const yerler = liste.yerler;

  const sehir = sehirler.find((s) => s.anahtar === anahtar);
  const baslik = sehir?.isim ?? (anahtar === "samsun" ? "Samsun" : anahtar);

  return (
    <main className="atmosfer min-h-screen">
      <div className="relative bg-deniz-derin pb-16 pt-24 text-white">
        <SiteHeader sehirAnahtari={anahtar} />
        <div className="mx-auto max-w-6xl px-4 md:px-8">
          <p className="text-sm uppercase tracking-[0.2em] text-white/55">Keşfet</p>
          <h1 className="mt-3 font-display text-2xl font-bold tracking-tight sm:text-3xl md:text-5xl">
            {baslik}
          </h1>
          <p className="mt-4 max-w-xl text-white/75">
            İlçeyi haritada seç, sonra kategoriye göre yerleri süz.
          </p>
        </div>
      </div>

      <div className="mx-auto max-w-6xl space-y-14 px-4 py-10 md:px-8">
        {IL_SECICI_ACIK || anahtar === "samsun" ? (
          <section>
            <h2 className="mb-6 font-display text-3xl text-deniz">İlçeler</h2>
            <KesfetPaneli sehirAnahtari={anahtar} />
          </section>
        ) : null}

        <section>
          <h2 className="mb-4 font-display text-3xl text-deniz">Yerler</h2>
          <div className="flex flex-wrap gap-2">
            <Link
              href={`/sehir/${anahtar}`}
              className={`inline-flex min-h-[44px] items-center rounded-full px-4 py-2 text-sm transition ${
                !kategori
                  ? "bg-deniz text-white"
                  : "bg-white/70 text-ink hover:bg-white"
              }`}
            >
              Tümü
            </Link>
            {ANA_KATEGORILER.filter((k) => k.deger !== "konaklama").map((k) => (
              <Link
                key={k.deger}
                href={`/sehir/${anahtar}?kategori=${k.deger}`}
                className={`inline-flex min-h-[44px] items-center rounded-full px-4 py-2 text-sm transition ${
                  kategori === k.deger
                    ? "bg-deniz text-white"
                    : "bg-white/70 text-ink hover:bg-white"
                }`}
              >
                {k.etiket}
              </Link>
            ))}
          </div>

          <div className="mt-8">
            <p className="mb-2 text-sm text-ink/50">{liste.toplam_sayi} yer</p>
            {yerler.length === 0 ? (
              <p className="py-12 text-ink/60">
                Yer bulunamadı. API çalışıyor mu? ({process.env.NEXT_PUBLIC_API_URL})
              </p>
            ) : (
              <div className="rounded-2xl bg-white/60 px-4 md:px-6">
                {yerler.map((yer) => (
                  <YerSatiri key={yer.id} yer={yer} />
                ))}
              </div>
            )}
          </div>

          <div className="mt-12 flex flex-wrap gap-4">
            <Link
              href={`/sehir/${anahtar}/rota`}
              className="rounded-full bg-gunes px-5 py-2.5 text-sm font-semibold text-deniz-derin"
            >
              Bu şehir için rota kur
            </Link>
            <Link
              href={`/sehir/${anahtar}/bolgeler`}
              className="rounded-full border border-deniz/30 px-5 py-2.5 text-sm text-deniz"
            >
              İlçe profilleri
            </Link>
          </div>
        </section>
      </div>
    </main>
  );
}
