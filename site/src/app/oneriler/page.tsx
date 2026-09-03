import { SiteHeader } from "@/components/SiteHeader";
import { OneriKarti } from "@/components/oneriler/OneriKarti";
import { OneriSekmeler } from "@/components/oneriler/OneriSekmeler";
import { yayinlariGetir } from "@/lib/oneriBlogApi";
import type { CommunityPost } from "@/types/suggestion";

export const metadata = {
  title: "Önerim Var",
  description: "Onaylanan gizli koylar, lezzet durakları ve manzara noktaları. Hikâyeyi oku, yola çık.",
};

export default async function OnerilerSayfasi() {
  let yazilar: CommunityPost[] = [];
  try {
    yazilar = await yayinlariGetir();
  } catch {
    yazilar = [];
  }

  return (
    <main className="atmosfer min-h-screen">
      <div className="relative bg-deniz-derin pb-14 pt-24 text-white">
        <SiteHeader />
        <div className="mx-auto max-w-6xl px-4 md:px-8">
          <p className="text-sm uppercase tracking-[0.2em] text-white/55">TOPLULUK KEŞFİ</p>
          <h1 className="mt-3 font-display text-2xl font-bold tracking-tight sm:text-3xl md:text-5xl">
            Bir Önerim Var!
          </h1>
          <p className="mt-5 max-w-2xl text-base leading-relaxed text-white/80 md:text-lg">
            Ekibin onayladığı saklı noktalar. Hikâyeyi oku, tarifine bak, yola çık.
          </p>
          <OneriSekmeler aktif="blog" />
        </div>
      </div>
      <div className="mx-auto max-w-6xl px-4 py-12 md:px-8">
        {yazilar.length === 0 ? (
          <p className="rounded-2xl bg-white/80 px-6 py-10 text-center text-ink/60">
            Henüz yayında bir keşif yok. İlk saklı noktayı sen öner.
          </p>
        ) : (
          <div className="grid grid-cols-1 gap-4 md:grid-cols-2 md:gap-6 lg:grid-cols-3">
            {yazilar.map((yazi) => (
              <OneriKarti key={yazi.id} yazi={yazi} />
            ))}
          </div>
        )}
      </div>
    </main>
  );
}
