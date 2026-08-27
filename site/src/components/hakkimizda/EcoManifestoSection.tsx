import { Footprints, HeartHandshake, Trash2, TreePine } from "lucide-react";

const KURALLAR = [
  {
    ikon: Trash2,
    baslik: "Sıfır Atık",
    metin: "Çöpünü doğada bırakma, çantana geri koy.",
  },
  {
    ikon: TreePine,
    baslik: "Dokunulmamış Doğallık",
    metin: "Bitki örtüsüne ve yaban hayatına müdahale etme.",
  },
  {
    ikon: HeartHandshake,
    baslik: "Saygılı Keşif",
    metin: "Sessizliği ve yerel yaşamın huzurunu koru.",
  },
] as const;

export function EcoManifestoSection() {
  return (
    <section className="rounded-2xl border border-emerald-500/20 bg-emerald-950/40 px-5 py-10 text-kopuk md:px-10 md:py-12">
      <p className="text-xs font-semibold uppercase tracking-[0.18em] text-emerald-200/80">
        🌿 VAZGEÇİLMEZ İLKEMİZ
      </p>
      <div className="mt-3 flex flex-wrap items-center gap-3">
        <Footprints className="h-7 w-7 text-emerald-300" aria-hidden />
        <h2 className="font-display text-3xl text-white md:text-4xl">
          Ayak İzinden Başka Bir Şey Bırakma
        </h2>
      </div>

      <div className="mt-6 max-w-3xl space-y-4 text-base leading-relaxed text-emerald-50/90 md:text-lg">
        <p>
          Doğa bize cömertçe kollarını açıyor; ancak bu güzelliklerin yarın da
          var olabilmesi tamamen bizim ona göstereceğimiz saygıya bağlı.
          ŞAMANDIRA olarak paylaştığımız hiçbir gizli koyun, şelalenin ya da
          yaylanın tahrip edilmesine, çöp yığınlarına teslim edilmesine seyirci
          kalamayız.
        </p>
        <p>
          Gittiğiniz her yerde doğanın sesini dinleyin, yaban hayatına saygı
          duyun ve yanınızda getirdiğiniz hiçbir şeyi—tek bir izmariti, tek bir
          plastik kapağı dahi—arkada bırakmayın. Gerçek bir gezgin, geçtiği yeri
          bulduğundan daha temiz bırakandır.
        </p>
      </div>

      <ul className="mt-8 grid gap-4 sm:grid-cols-3">
        {KURALLAR.map((kural) => {
          const Ikon = kural.ikon;
          return (
            <li
              key={kural.baslik}
              className="rounded-xl border border-emerald-400/20 bg-emerald-950/50 p-4"
            >
              <Ikon className="h-6 w-6 text-emerald-300" aria-hidden />
              <h3 className="mt-3 font-display text-xl text-white">{kural.baslik}</h3>
              <p className="mt-2 text-sm leading-relaxed text-emerald-100/80">
                {kural.metin}
              </p>
            </li>
          );
        })}
      </ul>
    </section>
  );
}
