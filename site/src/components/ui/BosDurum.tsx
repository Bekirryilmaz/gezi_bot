"use client";

import { cn } from "cn";
import {
  BOS_FILTRE_BASLIK,
  BOS_HAZIRLANIYOR,
  BOS_LISTE,
  BOS_VERI,
  CTA_SAMSUN,
  CTA_YENILE,
  HATA_PUSULA,
  SAYFA_404_BASLIK,
  SAYFA_404_METIN,
} from "@/lib/marka";
import { Dugme } from "./Dugme";
import { UfukCizgisiBos } from "./UfukCizgisiBos";

export type BosTip =
  | "filtre"
  | "veri"
  | "hata"
  | "404"
  | "hazirlaniyor"
  | "loading"
  | "empty"
  | "insufficient"
  | "unavailable"
  | "error";

type Cta = {
  href?: string;
  onClick?: () => void;
  etiket: string;
  varyant?: "birincil" | "ikincil";
};

const METIN: Record<BosTip, { baslik: string; metin: string; cta: Cta[] }> = {
  filtre: {
    baslik: BOS_FILTRE_BASLIK,
    metin: BOS_LISTE,
    cta: [],
  },
  veri: {
    baslik: BOS_VERI,
    metin: "Bu şehir henüz işaretlenmedi; Samsun açık ve gezilecek yerleri hazır.",
    cta: [{ href: "/sehir/samsun", etiket: CTA_SAMSUN, varyant: "ikincil" }],
  },
  hata: {
    baslik: "Pusula şaştı",
    metin: HATA_PUSULA,
    cta: [{ etiket: CTA_YENILE, varyant: "ikincil" }],
  },
  "404": {
    baslik: SAYFA_404_BASLIK,
    metin: SAYFA_404_METIN,
    cta: [
      { href: "/", etiket: "Ana sayfa", varyant: "ikincil" },
      { href: "/sehir/samsun", etiket: "Keşfe başla", varyant: "birincil" },
    ],
  },
  hazirlaniyor: {
    baslik: BOS_HAZIRLANIYOR,
    metin: "Yayına girince bu yüzey dolacak; şimdilik açık sayfalara bakabilirsin.",
    cta: [{ href: "/sehir/samsun", etiket: CTA_SAMSUN, varyant: "ikincil" }],
  },
  loading: {
    baslik: "Hazırlanıyor",
    metin: "İşaretler yükleniyor; mevcut seçimin korunuyor.",
    cta: [],
  },
  empty: {
    baslik: "Henüz sonuç yok",
    metin: BOS_LISTE,
    cta: [],
  },
  insufficient: {
    baslik: "Plan için bilgi yetersiz",
    metin:
      "Bu seçimlerle güvenli bir sonuç üretilemedi. Tercihlerini değiştirip yeniden deneyebilirsin.",
    cta: [],
  },
  unavailable: {
    baslik: "Şu anda ulaşılamıyor",
    metin:
      "Hizmet geçici olarak kullanılamıyor. Seçimin korunuyor; biraz sonra yeniden deneyebilirsin.",
    cta: [{ etiket: CTA_YENILE, varyant: "ikincil" }],
  },
  error: {
    baslik: "Bir hata oluştu",
    metin: HATA_PUSULA,
    cta: [{ etiket: CTA_YENILE, varyant: "ikincil" }],
  },
};

export function BosDurum({
  tip = "filtre",
  baslik,
  metin,
  cta,
  ctalar,
  className,
}: {
  tip?: BosTip;
  baslik?: string;
  metin?: string;
  cta?: Cta;
  ctalar?: Cta[];
  className?: string;
}) {
  const varsayilan = METIN[tip];
  const eylemler = ctalar ?? (cta ? [cta] : varsayilan.cta);

  return (
    <div
      className={cn(
        "bg-tuz border-bordo/12 rounded-[12px] border px-6 py-16 text-center",
        className,
      )}
    >
      <UfukCizgisiBos />
      <p className="yazi-alt text-bordo">{baslik ?? varsayilan.baslik}</p>
      <p className="yazi-govde text-ink/70 mx-auto mt-3 max-w-md">
        {metin ?? varsayilan.metin}
      </p>
      {eylemler.length > 0 ? (
        <div className="mt-8 flex flex-wrap justify-center gap-3">
          {eylemler.map((e) =>
            e.href ? (
              <Dugme key={e.etiket} href={e.href} varyant={e.varyant ?? "ikincil"}>
                {e.etiket}
              </Dugme>
            ) : (
              <Dugme
                key={e.etiket}
                varyant={e.varyant ?? "ikincil"}
                onClick={e.onClick ?? (() => window.location.reload())}
              >
                {e.etiket}
              </Dugme>
            ),
          )}
        </div>
      ) : null}
    </div>
  );
}
