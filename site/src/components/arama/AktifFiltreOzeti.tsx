import type { AramaFiltreDurumu, AramaFiltreKatalogu } from "@/lib/types";

export function AktifFiltreOzeti({
  filtreler,
  katalog,
}: {
  filtreler: AramaFiltreDurumu;
  katalog: AramaFiltreKatalogu;
}) {
  const etiketler: string[] = [];
  const ilce = katalog.ilceler.find((oge) => oge.id === filtreler.ilce);
  const tur = katalog.turler.find((oge) => oge.kod === filtreler.tur);
  if (ilce) etiketler.push(ilce.isim);
  if (tur) etiketler.push(tur.etiket);
  for (const kod of filtreler.zorunluKosullar) {
    const kosul = katalog.somut_kosullar.find((oge) => oge.kod === kod);
    if (kosul) etiketler.push(`${kosul.etiket} · zorunlu`);
  }
  for (const kod of filtreler.tercihler) {
    const kosul = katalog.somut_kosullar.find((oge) => oge.kod === kod);
    if (kosul) etiketler.push(`${kosul.etiket} · tercih`);
  }
  if (etiketler.length === 0) return null;
  return (
    <ul aria-label="Uygulanan filtreler" className="flex flex-wrap gap-2">
      {etiketler.map((etiket) => (
        <li key={etiket} className="bg-kopuk rounded-full px-3 py-1 text-sm">
          {etiket}
        </li>
      ))}
    </ul>
  );
}
