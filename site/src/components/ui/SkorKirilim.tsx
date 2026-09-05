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

  return (
    <ul className="space-y-2">
      {yedek.map((o) => (
        <li key={o.etiket}>
          <div className="text-ink/55 flex justify-between text-xs">
            <span>{o.etiket}</span>
            <span className="tabular-nums">{o.deger.toFixed(1)}</span>
          </div>
          <div className="bg-deniz/10 mt-1 h-1.5 overflow-hidden rounded-full">
            <div
              className="bg-deniz h-full rounded-full"
              style={{ width: `${Math.min(100, (o.deger / tavan) * 100)}%` }}
            />
          </div>
        </li>
      ))}
    </ul>
  );
}
