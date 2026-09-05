"use client";

import { useRef, type KeyboardEvent, type ReactNode } from "react";
import { cn } from "cn";

export function FiltreSatiri({
  children,
  className,
}: {
  children: ReactNode;
  className?: string;
}) {
  const ref = useRef<HTMLDivElement>(null);

  const klavye = (e: KeyboardEvent<HTMLDivElement>) => {
    if (e.key !== "ArrowRight" && e.key !== "ArrowLeft") return;
    const kok = ref.current;
    if (!kok) return;
    const baglar = [...kok.querySelectorAll<HTMLElement>("a, button")];
    if (baglar.length === 0) return;
    const i = baglar.indexOf(document.activeElement as HTMLElement);
    const sonraki =
      e.key === "ArrowRight"
        ? baglar[(i + 1 + baglar.length) % baglar.length]
        : baglar[(i - 1 + baglar.length) % baglar.length];
    sonraki?.focus();
    e.preventDefault();
  };

  return (
    <div
      ref={ref}
      role="navigation"
      aria-label="Filtreler"
      onKeyDown={klavye}
      className={cn(
        "filtre-satiri flex [scrollbar-width:none] gap-2 overflow-x-auto pb-1 [-ms-overflow-style:none] [&::-webkit-scrollbar]:hidden",
        className,
      )}
    >
      {children}
    </div>
  );
}
