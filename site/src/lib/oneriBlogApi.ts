import { fastapiHata, fastapiJson } from "@/lib/mekanOneriApi";
import type { CommunityPost, PostComment } from "@/types/suggestion";

export async function yayinlariGetir(): Promise<CommunityPost[]> {
  const { ok, govde } = await fastapiJson("/mekan-onerileri/yayinlar", {
    cache: "no-store",
  });
  if (!ok || !Array.isArray(govde)) {
    throw new Error(fastapiHata(govde, "Yazılar alınamadı."));
  }
  return govde as CommunityPost[];
}

export async function yayinGetir(slug: string): Promise<CommunityPost | null> {
  const { ok, status, govde } = await fastapiJson(
    `/mekan-onerileri/yayinlar/${encodeURIComponent(slug)}`,
    { cache: "no-store" },
  );
  if (status === 404) return null;
  if (!ok) throw new Error(fastapiHata(govde, "Yazı alınamadı."));
  return govde as CommunityPost;
}

export async function yorumlariGetir(slug: string): Promise<PostComment[]> {
  const { ok, govde } = await fastapiJson(
    `/mekan-onerileri/yayinlar/${encodeURIComponent(slug)}/yorumlar`,
    { cache: "no-store" },
  );
  if (!ok || !Array.isArray(govde)) return [];
  return govde as PostComment[];
}
