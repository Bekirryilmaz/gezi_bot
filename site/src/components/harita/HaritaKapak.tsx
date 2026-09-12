import type { HaritaIsareti } from "@/lib/harita";
import { haritaKutusu, haritaProje } from "@/lib/harita";

export function HaritaKapak({
  isaretler,
  merkez,
  sehirIsim,
  secilenId,
}: {
  isaretler: HaritaIsareti[];
  merkez: { enlem: number; boylam: number };
  sehirIsim: string;
  secilenId?: string | null;
}) {
  const kutu = haritaKutusu(isaretler, merkez);

  return (
    <svg
      viewBox="0 0 100 62"
      preserveAspectRatio="xMidYMid slice"
      className="harita-kapak-svg absolute inset-0 size-full"
      role="img"
      aria-label={`${sehirIsim} ilçe atlası`}
    >
      <rect width="100" height="62" fill="var(--kagit)" />
      <rect width="100" height="62" fill="var(--tuz)" opacity="0.55" />
      <path
        d="M4 18 C 18 8, 32 22, 48 16 S 78 8, 96 20 L 96 58 L 4 58 Z"
        fill="var(--kagit-koyu)"
        opacity="0.55"
      />
      <path
        d="M0 22 C 22 14, 40 28, 58 20 S 84 12, 100 26"
        fill="none"
        stroke="var(--deniz)"
        strokeWidth="0.35"
        opacity="0.35"
      />
      {isaretler.map((i) => {
        const p = haritaProje(kutu, i.enlem, i.boylam);
        const secili = secilenId === i.id;
        return (
          <g key={i.id}>
            <circle
              cx={p.x}
              cy={(p.y * 62) / 100}
              r={secili ? 1.8 : 1.35}
              fill="none"
              stroke="var(--samandira)"
              strokeWidth="0.35"
              opacity={secili ? 1 : 0.7}
            />
            <circle cx={p.x} cy={(p.y * 62) / 100} r="0.55" fill="var(--samandira)" />
          </g>
        );
      })}
    </svg>
  );
}

export function HaritaKapakDugmeleri({
  isaretler,
  merkez,
  onSec,
  secilenId,
}: {
  isaretler: HaritaIsareti[];
  merkez: { enlem: number; boylam: number };
  onSec: (id: string) => void;
  secilenId: string | null;
}) {
  const kutu = haritaKutusu(isaretler, merkez);
  return (
    <ul className="absolute inset-0 z-10 m-0 list-none p-0">
      {isaretler.map((i) => {
        const p = haritaProje(kutu, i.enlem, i.boylam);
        return (
          <li
            key={i.id}
            className="absolute"
            style={{
              left: `${p.x}%`,
              top: `${p.y}%`,
              transform: "translate(-50%, -50%)",
            }}
          >
            <button
              type="button"
              className={`harita-isik ${secilenId === i.id ? "harita-isik-secili" : ""}`}
              aria-label={i.ad}
              aria-pressed={secilenId === i.id}
              onClick={() => onSec(i.id)}
            />
          </li>
        );
      })}
    </ul>
  );
}
