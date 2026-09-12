import { BolumBasligi } from "@/components/ui/BolumBasligi";
import { KesilenAyrac } from "@/components/ui/KesilenAyrac";
import { Reveal } from "@/components/hareket/Reveal";
import { HaritaKapi } from "./HaritaKapi";
import { HaritaKapak } from "./HaritaKapak";
import { HaritaPlakaPaneli } from "./HaritaPlakaPaneli";
import type { HaritaIsareti } from "@/lib/harita";

export function HaritaBolum({
  sehirAnahtari,
  sehirIsim,
  isaretler,
  merkez,
}: {
  sehirAnahtari: string;
  sehirIsim: string;
  isaretler: HaritaIsareti[];
  merkez: { enlem: number; boylam: number };
}) {
  return (
    <section className="bg-kagit bolum-harita" data-harita-bolum>
      <div className="kabuk">
        <KesilenAyrac className="mb-16" />
        <Reveal>
          <BolumBasligi
            etiket="Atlas"
            baslik={`${sehirIsim} işaretli`}
            ozet="İlçeler birer ışık. Kaydırınca kamera uçar; tıklayınca plaka açılır. Yeni şehir aynı katmandan eklenir."
            aksiyon={{ href: `/sehir/${sehirAnahtari}/bolgeler`, etiket: "Bölgeyi tanı" }}
          />
        </Reveal>
        <div className="mt-12">
          {isaretler.length === 0 ? (
            <p className="yazi-govde text-ink/65">
              Bu şehir için henüz işaretlenecek ilçe koordinatı yok.
            </p>
          ) : (
            <>
              <script
                type="application/json"
                id="harita-veri"
                dangerouslySetInnerHTML={{
                  __html: JSON.stringify({ isaretler, merkez, sehirIsim }).replaceAll(
                    "<",
                    "\\u003c",
                  ),
                }}
              />
              <HaritaKapi>
                <div className="grid gap-5 lg:grid-cols-12 lg:items-stretch">
                  <div
                    data-harita-sahne
                    data-harita-yuklu="0"
                    className="harita-sahne border-bordo/12 relative overflow-hidden rounded-[12px] border lg:col-span-7"
                  >
                    <HaritaKapak
                      isaretler={isaretler}
                      merkez={merkez}
                      sehirIsim={sehirIsim}
                    />
                  </div>
                  <div className="lg:col-span-5">
                    <HaritaPlakaPaneli isaret={null} sehirIsim={sehirIsim} />
                  </div>
                </div>
              </HaritaKapi>
            </>
          )}
        </div>
      </div>
    </section>
  );
}
