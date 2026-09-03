"use client";

import { useState } from "react";
import type { PostComment } from "@/types/suggestion";

type Props = {
  postId: string;
  ilkYorumlar: PostComment[];
};

export function CommentSection({ postId, ilkYorumlar }: Props) {
  const [yorumlar, setYorumlar] = useState(ilkYorumlar);
  const [ad, setAd] = useState("");
  const [icerik, setIcerik] = useState("");
  const [mesaj, setMesaj] = useState<string | null>(null);
  const [gonderiliyor, setGonderiliyor] = useState(false);

  async function gonder(e: React.FormEvent) {
    e.preventDefault();
    setMesaj(null);
    setGonderiliyor(true);
    try {
      const yanit = await fetch(`/api/oneriler/${postId}/yorumlar`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ authorName: ad.trim(), content: icerik.trim() }),
      });
      const json = (await yanit.json()) as PostComment | { mesaj?: string };
      if (!yanit.ok) {
        setMesaj((json as { mesaj?: string }).mesaj ?? "Yorum gönderilemedi.");
        return;
      }
      setYorumlar((onceki) => [json as PostComment, ...onceki]);
      setAd("");
      setIcerik("");
    } catch {
      setMesaj("Bağlantı kurulamadı.");
    } finally {
      setGonderiliyor(false);
    }
  }

  return (
    <section className="space-y-6 border-t border-teal-100 pt-10">
      <h2 className="font-display text-3xl text-deniz">Yorumlar</h2>
      <form onSubmit={gonder} className="space-y-3 rounded-2xl border border-teal-100 bg-white/80 p-5">
        <label className="block space-y-1.5">
          <span className="text-sm font-medium text-deniz">Adın</span>
          <input
            required
            minLength={2}
            maxLength={80}
            value={ad}
            onChange={(e) => setAd(e.target.value)}
            className="w-full rounded-xl border border-[var(--cizgi)] bg-white px-3 py-2.5 outline-none focus:border-deniz"
            placeholder="Adın"
          />
        </label>
        <label className="block space-y-1.5">
          <span className="text-sm font-medium text-deniz">Yorumun</span>
          <textarea
            required
            minLength={4}
            maxLength={1200}
            rows={4}
            value={icerik}
            onChange={(e) => setIcerik(e.target.value)}
            className="w-full rounded-xl border border-[var(--cizgi)] bg-white px-3 py-2.5 outline-none focus:border-deniz"
            placeholder="Bu noktayı sen nasıl yaşadın?"
          />
        </label>
        {mesaj ? <p className="text-sm text-bordo">{mesaj}</p> : null}
        <button
          type="submit"
          disabled={gonderiliyor}
          className="rounded-full bg-teal-700 px-5 py-2 text-sm font-semibold text-white hover:bg-deniz disabled:opacity-60"
        >
          {gonderiliyor ? "Gönderiliyor…" : "Yorumu gönder"}
        </button>
      </form>
      {yorumlar.length === 0 ? (
        <p className="text-sm text-ink/50">İlk yorumu sen bırak.</p>
      ) : (
        <ul className="space-y-4">
          {yorumlar.map((y) => (
            <li key={y.id} className="rounded-2xl bg-kopuk/80 px-4 py-3">
              <p className="text-sm font-semibold text-deniz">{y.authorName}</p>
              <p className="mt-1 text-sm leading-relaxed text-ink/80">{y.content}</p>
              {y.createdAt ? (
                <p className="mt-2 text-xs text-ink/40">
                  {new Date(y.createdAt).toLocaleDateString("tr-TR")}
                </p>
              ) : null}
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
