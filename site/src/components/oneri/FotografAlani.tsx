"use client";

import { useCallback, useEffect, useRef, useState, useMemo } from "react";

const MAKS_DOSYA = 3;
const MAKS_BOYUT = 5 * 1024 * 1024;
const IZINLI = ["image/jpeg", "image/png", "image/webp"];

type Props = {
  dosyalar: File[];
  onChange: (dosyalar: File[]) => void;
  hata?: string | null;
};

export function FotografAlani({ dosyalar, onChange, hata }: Props) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [surukleniyor, setSurukleniyor] = useState(false);
  const [yerelHata, setYerelHata] = useState<string | null>(null);
  const onizlemeler = useMemo(
    () => dosyalar.map((d) => URL.createObjectURL(d)),
    [dosyalar],
  );

  useEffect(() => {
    return () => {
      onizlemeler.forEach((u) => URL.revokeObjectURL(u));
    };
  }, [onizlemeler]);

  const ekle = useCallback(
    (yeni: FileList | File[]) => {
      const adaylar = Array.from(yeni);
      const biriken = [...dosyalar];
      for (const dosya of adaylar) {
        if (biriken.length >= MAKS_DOSYA) {
          setYerelHata("En fazla 3 görsel yükleyebilirsin.");
          break;
        }
        if (!IZINLI.includes(dosya.type)) {
          setYerelHata("Yalnızca JPEG, PNG veya WebP kabul edilir.");
          continue;
        }
        if (dosya.size > MAKS_BOYUT) {
          setYerelHata("Her görsel en fazla 5 MB olabilir.");
          continue;
        }
        biriken.push(dosya);
        setYerelHata(null);
      }
      onChange(biriken.slice(0, MAKS_DOSYA));
    },
    [dosyalar, onChange],
  );

  return (
    <div className="space-y-3">
      <div
        role="button"
        tabIndex={0}
        onClick={() => inputRef.current?.click()}
        onKeyDown={(e) => {
          if (e.key === "Enter" || e.key === " ") {
            e.preventDefault();
            inputRef.current?.click();
          }
        }}
        onDragOver={(e) => {
          e.preventDefault();
          setSurukleniyor(true);
        }}
        onDragLeave={() => setSurukleniyor(false)}
        onDrop={(e) => {
          e.preventDefault();
          setSurukleniyor(false);
          ekle(e.dataTransfer.files);
        }}
        className={`cursor-pointer rounded-xl border-2 border-dashed px-4 py-8 text-center transition ${
          surukleniyor
            ? "border-yosun bg-yosun/10"
            : "border-[var(--cizgi)] bg-white/70 hover:border-deniz"
        }`}
      >
        <p className="text-sm font-medium text-deniz">Fotoğrafları sürükle veya tıkla</p>
        <p className="mt-1 text-xs text-ink/55">En fazla 3 görsel · JPEG / PNG / WebP · 5 MB</p>
        <input
          ref={inputRef}
          type="file"
          accept="image/jpeg,image/png,image/webp"
          multiple
          className="hidden"
          onChange={(e) => {
            if (e.target.files) ekle(e.target.files);
            e.target.value = "";
          }}
        />
      </div>
      {dosyalar.length > 0 ? (
        <ul className="grid grid-cols-3 gap-2">
          {dosyalar.map((dosya, i) => (
            <li key={`${dosya.name}-${i}`} className="relative overflow-hidden rounded-lg bg-deniz-derin">
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img
                src={onizlemeler[i]}
                alt={dosya.name}
                className="h-24 w-full object-cover"
              />
              <button
                type="button"
                onClick={() => onChange(dosyalar.filter((_, j) => j !== i))}
                className="absolute right-1 top-1 rounded-full bg-bordo px-2 py-0.5 text-[11px] text-white"
              >
                Kaldır
              </button>
            </li>
          ))}
        </ul>
      ) : null}
      {(hata || yerelHata) && (
        <p className="text-sm text-bordo">{hata || yerelHata}</p>
      )}
    </div>
  );
}
