"use client";

import { useId } from "react";

type Props = {
  deger: string;
  onDegerDegis: (deger: string) => void;
  onAra?: () => void;
  yukleniyor?: boolean;
};

export function AramaKutusu({ deger, onDegerDegis, onAra, yukleniyor = false }: Props) {
  const id = useId();
  return (
    <form
      role="search"
      className="flex w-full gap-2"
      onSubmit={(olay) => {
        olay.preventDefault();
        onAra?.();
      }}
    >
      <label htmlFor={id} className="sr-only">
        Yer, tür, şehir veya ilçe ara
      </label>
      <input
        id={id}
        type="search"
        value={deger}
        onChange={(olay) => onDegerDegis(olay.target.value)}
        placeholder="Örn. Mado Atakum veya kahve"
        autoComplete="off"
        className="border-deniz/20 focus-visible:ring-deniz min-h-11 min-w-0 flex-1 rounded-full border bg-white px-4 text-base outline-none focus-visible:ring-2"
      />
      <button
        type="submit"
        disabled={yukleniyor || deger.trim().length === 0}
        className="bg-deniz min-h-11 rounded-full px-5 text-sm font-semibold text-white disabled:opacity-50"
      >
        {yukleniyor ? "Aranıyor…" : "Ara"}
      </button>
    </form>
  );
}
