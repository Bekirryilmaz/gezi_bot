import type { DistrictDetail } from "@/types/discovery";
import { SAMSUN_ILCELERI } from "@/data/districts";

export { SAMSUN_ILCELERI };
export const SAMSUN_MERKEZ: [number, number] = [41.2867, 36.33];
export const VARSAYILAN_ILCE_ID = "ilkadim";

export function ilceSlug(ad: string): string {
  return ad
    .toLocaleLowerCase("tr-TR")
    .replaceAll("ı", "i")
    .replaceAll("ğ", "g")
    .replaceAll("ü", "u")
    .replaceAll("ş", "s")
    .replaceAll("ö", "o")
    .replaceAll("ç", "c")
    .replaceAll(" ", "-");
}

export function ilceleriProfillerleBirleştir(): DistrictDetail[] {
  return SAMSUN_ILCELERI;
}

export function ilceBul(idVeyaSlug: string): DistrictDetail | undefined {
  return SAMSUN_ILCELERI.find((i) => i.id === idVeyaSlug || i.slug === idVeyaSlug);
}
