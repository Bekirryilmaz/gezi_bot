import type { CityDetail } from "@/types/city";
import { TURKIYE_SEHIRLERI } from "@/data/cities";
import { sehirSlug } from "@/lib/slug";

export { TURKIYE_SEHIRLERI, sehirSlug };
export const TURKIYE_MERKEZ: [number, number] = [39.0, 35.0];
export const VARSAYILAN_IL_ID = "samsun";

export function sehirBul(idVeyaSlug: string): CityDetail | undefined {
  return TURKIYE_SEHIRLERI.find((s) => s.id === idVeyaSlug || s.slug === idVeyaSlug);
}
