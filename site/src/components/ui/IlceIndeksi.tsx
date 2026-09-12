/**
 * Ilce indeksi — sehir vitrininde fotograf yokken plaka kutusunu dolduran
 * editoryal blok. Uydurma gorsel yerine gercek veri: yer fotografi olmayan
 * bir sehri baska yerin fotografiyla temsil etmeyiz (yon.md 1.5 / K9).
 */
export function IlceIndeksi({ ilceler }: { ilceler: string[] }) {
  if (ilceler.length === 0) return null;

  return (
    <div className="plaka-izgara border-bordo/12 h-full border-t p-5 md:border-t-0 md:border-l md:p-6">
      <p className="etiket text-ink/45">İlçe indeksi</p>
      <ol className="mt-4 grid grid-cols-2 gap-x-6 sm:grid-cols-3">
        {ilceler.map((ilce, i) => (
          <li
            key={ilce}
            className="border-bordo/12 flex items-baseline gap-2 border-b py-1.5"
          >
            <span className="text-bordo/45 text-[11px] tabular-nums">
              {String(i + 1).padStart(2, "0")}
            </span>
            <span className="text-ink/80 min-w-0 truncate text-[13px] capitalize">
              {ilce}
            </span>
          </li>
        ))}
      </ol>
    </div>
  );
}
