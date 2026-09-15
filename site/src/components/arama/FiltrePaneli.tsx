"use client";

import type { AramaFiltreEylemi, AramaFiltreState } from "@/lib/arama-state";
import type { AramaFiltreDurumu, AramaFiltreKatalogu } from "@/lib/types";

type Props = {
  katalog: AramaFiltreKatalogu;
  state: AramaFiltreState;
  onEylem: (eylem: AramaFiltreEylemi) => void;
};

function degistir(
  mevcut: AramaFiltreDurumu,
  alan: Partial<AramaFiltreDurumu>,
): AramaFiltreDurumu {
  return { ...mevcut, ...alan };
}

function toggle(liste: string[], kod: string): string[] {
  return liste.includes(kod) ? liste.filter((oge) => oge !== kod) : [...liste, kod];
}

export function FiltrePaneli({ katalog, state, onEylem }: Props) {
  const taslak = state.taslak;
  return (
    <section
      aria-labelledby="arama-filtre-baslik"
      className="border-deniz/10 space-y-5 rounded-3xl border bg-white p-5"
    >
      <h2 id="arama-filtre-baslik" className="text-lg font-semibold">
        Filtreler
      </h2>

      <div className="grid gap-4 sm:grid-cols-2">
        <label className="grid gap-1 text-sm font-medium">
          İlçe
          <select
            value={taslak.ilce ?? ""}
            onChange={(olay) =>
              onEylem({
                type: "taslak",
                deger: degistir(taslak, { ilce: olay.target.value || null }),
              })
            }
            className="border-deniz/20 min-h-11 rounded-xl border px-3"
          >
            <option value="">Tüm ilçeler</option>
            {katalog.ilceler.map((ilce) => (
              <option key={ilce.id} value={ilce.id}>
                {ilce.isim}
              </option>
            ))}
          </select>
        </label>
        <label className="grid gap-1 text-sm font-medium">
          Mekân türü
          <select
            value={taslak.tur ?? ""}
            onChange={(olay) =>
              onEylem({
                type: "taslak",
                deger: degistir(taslak, { tur: olay.target.value || null }),
              })
            }
            className="border-deniz/20 min-h-11 rounded-xl border px-3"
          >
            <option value="">Tüm türler</option>
            {katalog.turler.map((tur) => (
              <option key={tur.kod} value={tur.kod}>
                {tur.etiket}
              </option>
            ))}
          </select>
        </label>
      </div>

      {katalog.somut_kosullar.length > 0 ? (
        <div className="grid gap-5 md:grid-cols-2">
          <fieldset className="space-y-2">
            <legend className="font-semibold">Zorunlu koşullar</legend>
            <p className="text-deniz/70 text-sm">Bilinmiyorsa yer eşleşmiş sayılmaz.</p>
            {katalog.somut_kosullar.map((kosul) => (
              <label key={kosul.kod} className="flex min-h-11 items-center gap-3">
                <input
                  type="checkbox"
                  checked={taslak.zorunluKosullar.includes(kosul.kod)}
                  onChange={() =>
                    onEylem({
                      type: "taslak",
                      deger: degistir(taslak, {
                        zorunluKosullar: toggle(taslak.zorunluKosullar, kosul.kod),
                        tercihler: taslak.tercihler.filter((kod) => kod !== kosul.kod),
                      }),
                    })
                  }
                />
                {kosul.etiket}
              </label>
            ))}
          </fieldset>
          <fieldset className="space-y-2">
            <legend className="font-semibold">Tercihler</legend>
            <p className="text-deniz/70 text-sm">
              Sıralamaya yardımcı olur; zorunlu engel değildir.
            </p>
            {katalog.somut_kosullar.map((kosul) => (
              <label key={kosul.kod} className="flex min-h-11 items-center gap-3">
                <input
                  type="checkbox"
                  checked={taslak.tercihler.includes(kosul.kod)}
                  onChange={() =>
                    onEylem({
                      type: "taslak",
                      deger: degistir(taslak, {
                        tercihler: toggle(taslak.tercihler, kosul.kod),
                        zorunluKosullar: taslak.zorunluKosullar.filter(
                          (kod) => kod !== kosul.kod,
                        ),
                      }),
                    })
                  }
                />
                {kosul.etiket}
              </label>
            ))}
          </fieldset>
        </div>
      ) : (
        <p className="text-deniz/70 text-sm">
          Şu anda kanıtı yayımlanmış somut koşul filtresi yok.
        </p>
      )}

      <div className="flex flex-wrap justify-end gap-2">
        <button
          type="button"
          onClick={() => onEylem({ type: "temizle" })}
          className="min-h-11 rounded-full px-4 text-sm underline"
        >
          Temizle
        </button>
        <button
          type="button"
          onClick={() => onEylem({ type: "vazgec" })}
          className="border-deniz/20 min-h-11 rounded-full border px-4 text-sm"
        >
          Vazgeç
        </button>
        <button
          type="button"
          onClick={() => onEylem({ type: "uygula" })}
          className="bg-deniz min-h-11 rounded-full px-5 text-sm font-semibold text-white"
        >
          Uygula
        </button>
      </div>
    </section>
  );
}
