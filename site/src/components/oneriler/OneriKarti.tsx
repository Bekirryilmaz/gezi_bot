import Link from "next/link";
import { Heart, MessageCircle } from "lucide-react";
import { ONERI_KATEGORILERI } from "@/types/placeSuggestion";
import { kategoriGosterimId, type CommunityPost } from "@/types/suggestion";

function kapak(yazi: CommunityPost): string | null {
  return yazi.approvedImages[0] ?? null;
}

function ozet(metin: string): string {
  const tek = metin.replace(/\s+/g, " ").trim();
  if (tek.length <= 140) return tek;
  return `${tek.slice(0, 137)}…`;
}

export function OneriKarti({ yazi }: { yazi: CommunityPost }) {
  const gorsel = kapak(yazi);
  const kat = ONERI_KATEGORILERI.find((k) => k.id === kategoriGosterimId(yazi.category));
  return (
    <article className="group overflow-hidden rounded-2xl border border-teal-100/80 bg-white shadow-[0_8px_28px_rgba(6,54,66,0.06)] transition duration-300 hover:-translate-y-1">
      <Link href={`/oneriler/${yazi.slug}`} className="block">
        <div className="relative h-48 overflow-hidden bg-deniz-derin">
          {gorsel ? (
            // eslint-disable-next-line @next/next/no-img-element
            <img
              src={gorsel}
              alt={yazi.title}
              className="h-full w-full object-cover transition duration-300 group-hover:scale-105"
            />
          ) : (
            <div className="flex h-full items-center justify-center text-4xl text-kopuk/50">
              {kat?.ikon ?? "📍"}
            </div>
          )}
          <span className="absolute left-3 top-3 rounded-full bg-yosun/95 px-2.5 py-1 text-xs font-semibold text-white">
            {kat ? `${kat.ikon} ${kat.etiket}` : yazi.category}
          </span>
        </div>
        <div className="space-y-3 p-5">
          <p className="text-xs font-medium uppercase tracking-wide text-teal-700">
            {yazi.city} / {yazi.district}
          </p>
          <h2 className="font-display text-2xl leading-tight text-deniz">{yazi.title}</h2>
          <p className="line-clamp-2 text-sm leading-relaxed text-slate-600">{ozet(yazi.userStory)}</p>
          <div className="flex items-center justify-between pt-1 text-xs text-ink/50">
            <span className="inline-flex items-center gap-3">
              <span className="inline-flex items-center gap-1">
                <Heart className="h-3.5 w-3.5" aria-hidden />
                {yazi.likesCount}
              </span>
              <span className="inline-flex items-center gap-1">
                <MessageCircle className="h-3.5 w-3.5" aria-hidden />
                {yazi.commentsCount}
              </span>
            </span>
            <span className="font-semibold text-teal-700">Hikayeyi ve Detayları Oku →</span>
          </div>
        </div>
      </Link>
    </article>
  );
}
