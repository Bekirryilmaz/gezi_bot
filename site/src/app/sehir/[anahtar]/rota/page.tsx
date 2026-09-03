import { SiteHeader } from "@/components/SiteHeader";
import { RotaSihirbazi } from "@/components/RotaSihirbazi";
import { WeatherErrorBoundary } from "@/components/rota/WeatherErrorBoundary";
import { WeatherWidget } from "@/components/rota/WeatherWidget";
import { bolgeleriGetir, sehirleriGetir } from "@/lib/api";
import { SAMSUN_MERKEZ } from "@/lib/ilceler";

type Props = {
  params: Promise<{ anahtar: string }>;
  searchParams: Promise<{
    konaklama_yer_id?: string;
    konaklama_bolge?: string;
  }>;
};

export async function generateMetadata({ params }: Props) {
  const { anahtar } = await params;
  const sehirler = await sehirleriGetir().catch(() => []);
  const sehir = sehirler.find((s) => s.anahtar === anahtar);
  return { title: sehir ? `${sehir.isim} Rota` : "Rota" };
}

export default async function RotaSayfasi({ params, searchParams }: Props) {
  const { anahtar } = await params;
  const sorgu = await searchParams;
  const [sehirler, bolgeler] = await Promise.all([
    sehirleriGetir().catch(() => []),
    bolgeleriGetir(anahtar).catch(() => []),
  ]);
  const sehir = sehirler.find((s) => s.anahtar === anahtar);
  const isim = sehir?.isim ?? (anahtar === "samsun" ? "Samsun" : anahtar);

  return (
    <main className="atmosfer min-h-screen">
      <div className="relative bg-deniz-derin pb-14 pt-24 text-white">
        <SiteHeader sehirAnahtari={anahtar} />
        <div className="mx-auto max-w-6xl px-4 md:px-8">
          <p className="text-sm uppercase tracking-[0.2em] text-white/55">Rota</p>
          <h1 className="mt-3 font-display text-2xl font-bold tracking-tight sm:text-3xl md:text-5xl">
            {isim} için rotan
          </h1>
          <p className="mt-4 max-w-xl text-white/75">
            Konaklama bölgen belliyse oradan başla; değilse alternatif rotalardan
            birini seç — ardından bölge önerisi ve kısa tavsiye gelir.
          </p>
        </div>
      </div>

      <div className="mx-auto max-w-6xl space-y-10 px-4 py-12 md:px-8">
        <WeatherErrorBoundary>
          <WeatherWidget
            enlem={sehir?.merkez_enlem ?? SAMSUN_MERKEZ[0]}
            boylam={sehir?.merkez_boylam ?? SAMSUN_MERKEZ[1]}
            konumEtiketi={isim}
          />
        </WeatherErrorBoundary>
        <RotaSihirbazi
          sehirAnahtari={anahtar}
          sehirIsim={isim}
          baslangicKonaklamaYerId={sorgu.konaklama_yer_id ?? null}
          baslangicKonaklamaBolge={sorgu.konaklama_bolge ?? null}
          bolgeler={bolgeler}
        />
      </div>
    </main>
  );
}
