import { Dugme } from "@/components/ui/Dugme";
import { Plaka } from "@/components/ui/Plaka";
import { UfukCizgisiBos } from "@/components/ui/UfukCizgisiBos";
import type { HaritaIsareti } from "@/lib/harita";

export function HaritaPlakaPaneli({
  isaret,
  sehirIsim,
}: {
  isaret: HaritaIsareti | null;
  sehirIsim: string;
}) {
  if (!isaret) {
    return (
      <aside className="kart-kabuk flex h-full min-h-48 flex-col justify-center p-6">
        <UfukCizgisiBos className="mb-6" />
        <p className="etiket text-ink/45">Plaka</p>
        <p className="yazi-alt text-ink mt-3">Bir ilçe ışığına dokun.</p>
        <p className="yazi-govde text-ink/65 mt-3">
          {sehirIsim} ilçeleri işaretli. Şehir eklendikçe aynı atlas büyür.
        </p>
        <span className="su-hatti" />
      </aside>
    );
  }

  return (
    <aside className="kart-kabuk flex h-full flex-col overflow-hidden" aria-live="polite">
      <Plaka etiket={isaret.ad} oran="kart" />
      <div className="flex flex-1 flex-col p-6">
        <p className="etiket text-ink/45">İlçe</p>
        <h3 className="yazi-alt text-ink mt-2">{isaret.ad}</h3>
        {isaret.ozet ? (
          <p className="yazi-govde text-ink/70 mt-3 line-clamp-4">{isaret.ozet}</p>
        ) : (
          <p className="yazi-govde text-ink/55 mt-3">
            Bu ilçe için özet henüz derlenmedi.
          </p>
        )}
        <div className="relative z-10 mt-6">
          <Dugme href={isaret.href} varyant="bolum">
            Bölgeyi tanı
          </Dugme>
        </div>
      </div>
      <span className="su-hatti" />
    </aside>
  );
}
