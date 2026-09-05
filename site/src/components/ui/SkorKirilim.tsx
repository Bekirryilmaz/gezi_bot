import { DENEYIM_EKSENLERI } from "@/lib/sabitler";

export function SkorKirilim({ kirilim }: { kirilim: Record<string, number> }) {
  const ogeler = DENEYIM_EKSENLERI.map((e) => ({
    etiket: e.etiket,
    deger: kirilim[e.deger] ?? kirilim[e.etiket] ?? 0,
  })).filter((o) => o.deger > 0);

  const yedek =
    ogeler.length > 0
      ? ogeler
      : Object.entries(kirilim)
          .filter(([, v]) => typeof v === "number" && v > 0)
          .map(([k, v]) => ({ etiket: k.replaceAll("_", " "), deger: v }));

  if (yedek.length === 0) return null;

  const tavan = Math.max(...yedek.map((o) => o.deger), 1);
  let enYuksek = 0;
  for (let i = 1; i < yedek.length; i++) {
    if ((yedek[i]?.deger ?? 0) > (yedek[enYuksek]?.deger ?? 0)) enYuksek = i;
  }

  return (
    <ul className="space-y-3">
      {yedek.map((o, i) => {
        const yuzde = Math.min(100, (o.deger / tavan) * 100);
        return (
          <li key={o.etiket}>
            <div className="text-ink/60 flex justify-between text-xs">
              <span>{o.etiket}</span>
              <span className="tabular-nums">{o.deger.toFixed(1)}</span>
            </div>
            <div className="bg-bordo/10 mt-1.5 h-1.5 rounded-full">
              <div className="relative h-1.5" style={{ width: `${yuzde}%` }}>
                <div className="skor-cubuk bg-deniz h-full w-full rounded-full" />
                {i === enYuksek ? (
                  <span
                    className="border-samandira bg-tuz pointer-events-none absolute top-1/2 right-0 size-1.5 translate-x-1/2 -translate-y-1/2 rounded-full border"
                    aria-hidden="true"
                  />
                ) : null}
              </div>
            </div>
          </li>
        );
      })}
    </ul>
  );
}
