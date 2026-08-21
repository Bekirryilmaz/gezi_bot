import Link from "next/link";
import { SiteHeader } from "@/components/SiteHeader";
import { bolgeleriGetir, sehirleriGetir } from "@/lib/api";
import { duyguEtiketi } from "@/lib/sabitler";

type Props = {
  params: Promise<{ anahtar: string }>;
};

export async function generateMetadata({ params }: Props) {
  const { anahtar } = await params;
  const sehirler = await sehirleriGetir().catch(() => []);
  const sehir = sehirler.find((s) => s.anahtar === anahtar);
  return { title: sehir ? `${sehir.isim} bölgeleri` : "Bölgeler" };
}

export default async function BolgelerSayfasi({ params }: Props) {
  const { anahtar } = await params;
  const [sehirler, bolgeler] = await Promise.all([
    sehirleriGetir().catch(() => []),
    bolgeleriGetir(anahtar).catch(() => []),
  ]);
  const sehir = sehirler.find((s) => s.anahtar === anahtar);

  return (
    <main className="atmosfer min-h-screen">
      <div className="relative bg-deniz-derin pb-14 pt-24 text-white">
        <SiteHeader sehirAnahtari={anahtar} />
        <div className="mx-auto max-w-6xl px-5 md:px-8">
          <p className="text-sm uppercase tracking-[0.2em] text-white/55">Bölgeler</p>
          <h1 className="mt-3 font-display text-4xl md:text-6xl">
            {sehir?.isim ?? anahtar} ve ilçeleri
          </h1>
          <p className="mt-4 max-w-xl text-white/75">
            Önce tanıtım, sonra orada yaşayanların ve gidenlerin ortak izlenimi.
          </p>
        </div>
      </div>

      <div className="mx-auto max-w-6xl space-y-14 px-5 py-12 md:px-8">
        {bolgeler.length === 0 ? (
          <p className="text-ink/60">Bölge profili bulunamadı.</p>
        ) : (
          bolgeler.map((bolge) => (
            <article
              key={bolge.bolge_adi}
              className="border-b border-[var(--cizgi)] pb-12"
            >
              <div className="flex flex-wrap items-baseline justify-between gap-3">
                <h2 className="font-display text-3xl text-deniz capitalize">
                  {bolge.bolge_adi}
                  <span className="ml-3 text-base font-sans font-normal text-ink/45">
                    {bolge.ilce_mi ? "ilçe" : "şehir geneli"}
                  </span>
                </h2>
                <Link
                  href={`/sehir/${anahtar}/rota?konaklama_bolge=${encodeURIComponent(bolge.bolge_adi)}`}
                  className="text-sm font-medium text-yosun hover:underline"
                >
                  Bu bölgeden rota kur →
                </Link>
              </div>

              <section className="mt-8">
                <h3 className="text-sm font-semibold uppercase tracking-wide text-ink/45">
                  Tanıtım
                </h3>
                {bolge.tanitim_metni ? (
                  <p className="mt-2 max-w-3xl text-lg leading-relaxed text-ink/85">
                    {bolge.tanitim_metni}
                  </p>
                ) : (
                  <p className="mt-2 text-ink/55">
                    Bu bölge için henüz derlenmiş bir tanıtım metni yok.
                  </p>
                )}
              </section>

              <section className="mt-8">
                <h3 className="text-sm font-semibold uppercase tracking-wide text-ink/45">
                  Kullanıcı deneyimleri
                </h3>
                {bolge.duygu_ozeti ? (
                  <p className="mt-2 max-w-3xl text-lg leading-relaxed text-ink/85">
                    {bolge.duygu_ozeti}
                  </p>
                ) : (
                  <p className="mt-2 text-ink/55">
                    Bu bölge için henüz kullanıcı deneyimi özeti yok.
                  </p>
                )}
                <p className="mt-3 text-sm text-ink/45">
                  {duyguEtiketi(bolge.genel_duygu_etiketi)}
                  {" · "}
                  {bolge.kullanilan_yorum_sayisi} yoruma dayalı
                </p>
              </section>
            </article>
          ))
        )}

        <Link href={`/sehir/${anahtar}`} className="inline-block text-yosun hover:underline">
          ← Keşfe dön
        </Link>
      </div>
    </main>
  );
}
