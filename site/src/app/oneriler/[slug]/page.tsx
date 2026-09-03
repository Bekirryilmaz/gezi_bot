import { notFound } from "next/navigation";
import { SiteHeader } from "@/components/SiteHeader";
import { CommentSection } from "@/components/oneriler/CommentSection";
import { MiniKonumHaritasiYukle } from "@/components/oneriler/MiniKonumHaritasiYukle";
import { OneriGalerisi } from "@/components/oneriler/OneriGalerisi";
import { OneriSekmeler } from "@/components/oneriler/OneriSekmeler";
import { yayinGetir, yorumlariGetir } from "@/lib/oneriBlogApi";
import { ONERI_KATEGORILERI } from "@/types/placeSuggestion";
import { kategoriGosterimId } from "@/types/suggestion";
import { ARABA_ERISIM_SECENEKLERI } from "@/types/suggestion";

type Props = { params: Promise<{ slug: string }> };

export async function generateMetadata({ params }: Props) {
  const { slug } = await params;
  const yazi = await yayinGetir(slug).catch(() => null);
  if (!yazi) return { title: "Keşif" };
  return {
    title: yazi.title,
    description: yazi.userStory.slice(0, 160),
  };
}

export default async function OneriDetaySayfasi({ params }: Props) {
  const { slug } = await params;
  const yazi = await yayinGetir(slug);
  if (!yazi) notFound();
  const yorumlar = await yorumlariGetir(slug).catch(() => []);
  const kat = ONERI_KATEGORILERI.find((k) => k.id === kategoriGosterimId(yazi.category));
  const araba = ARABA_ERISIM_SECENEKLERI.find((s) => s.id === yazi.transportation.carAccess);
  const alan = yazi.visibleFields;
  const editoryal = yazi.adminEditorial;
  const tarihMetni = editoryal?.historicalContext?.trim() || editoryal?.adminNotes?.trim();

  return (
    <main className="atmosfer min-h-screen">
      <div className="relative bg-deniz-derin pb-14 pt-24 text-white">
        <SiteHeader />
        <div className="mx-auto max-w-6xl px-4 md:px-8">
          <p className="text-sm uppercase tracking-[0.2em] text-white/55">
            {kat ? `${kat.ikon} ${kat.etiket}` : "Keşif"} · {yazi.city} / {yazi.district}
          </p>
          <h1 className="mt-3 font-display text-2xl font-bold tracking-tight sm:text-3xl md:text-5xl">
            {yazi.title}
          </h1>
          <OneriSekmeler aktif="blog" />
        </div>
      </div>
      <article className="mx-auto max-w-5xl space-y-10 px-4 py-12 md:px-8">
        <OneriGalerisi gorseller={yazi.approvedImages} baslik={yazi.title} />

        <section className="prose prose-slate max-w-none">
          <h2 className="font-display text-2xl text-deniz">Ziyaretçinin hikâyesi</h2>
          <blockquote className="mt-4 border-l-4 border-teal-700 bg-white/70 py-4 pl-5 pr-4 font-display text-lg leading-relaxed text-slate-700">
            {yazi.userStory}
          </blockquote>
        </section>

        {tarihMetni ? (
          <aside className="rounded-2xl border border-teal-200 bg-teal-50/90 p-6 text-teal-950 shadow-sm">
            <p className="text-xs font-semibold uppercase tracking-[0.18em] text-teal-700">
              ŞAMANDIRA Editör Notu & Tarihi Arka Plan
            </p>
            {editoryal?.historicalContext ? (
              <p className="mt-3 text-base leading-relaxed">{editoryal.historicalContext}</p>
            ) : null}
            {editoryal?.adminNotes ? (
              <p className="mt-3 text-sm leading-relaxed text-teal-900/80">{editoryal.adminNotes}</p>
            ) : null}
          </aside>
        ) : null}

        {alan.showSpecialTip && yazi.specialTip ? (
          <p className="rounded-2xl bg-kopuk px-5 py-4 text-sm text-deniz">
            <span className="font-semibold">Ziyaretçi tüyosu: </span>
            {yazi.specialTip}
          </p>
        ) : null}

        {alan.showTransportation ? (
          <div className="grid gap-4 rounded-2xl border border-teal-100 bg-white p-5 md:grid-cols-3">
            <div>
              <p className="text-xs uppercase tracking-wide text-teal-700">Araç</p>
              <p className="mt-1 text-sm font-medium text-ink">
                {araba?.etiket ?? yazi.transportation.carAccess}
              </p>
            </div>
            <div>
              <p className="text-xs uppercase tracking-wide text-teal-700">Yol</p>
              <p className="mt-1 text-sm font-medium text-ink">{yazi.transportation.roadCondition}</p>
            </div>
            <div>
              <p className="text-xs uppercase tracking-wide text-teal-700">Yürüme</p>
              <p className="mt-1 text-sm font-medium text-ink">{yazi.transportation.walkingDistance}</p>
            </div>
          </div>
        ) : null}

        {alan.showDirections && yazi.directions ? (
          <section className="rounded-2xl border border-teal-100 bg-white/80 p-5">
            <h2 className="font-display text-xl text-deniz">Adres tarifi</h2>
            <p className="mt-2 whitespace-pre-line text-sm leading-relaxed text-ink/80">
              {yazi.directions}
            </p>
          </section>
        ) : null}

        {alan.showExactCoordinates ? (
          <section className="space-y-3">
            <h2 className="font-display text-xl text-deniz">Konum</h2>
            <div className="h-[280px] w-full overflow-hidden rounded-2xl border border-teal-100">
              <MiniKonumHaritasiYukle lat={yazi.coordinates.lat} lng={yazi.coordinates.lng} />
            </div>
          </section>
        ) : null}

        <CommentSection postId={yazi.id} ilkYorumlar={yorumlar} />
      </article>
    </main>
  );
}
