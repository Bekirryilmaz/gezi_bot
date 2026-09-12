"use client";

import { type ReactNode, useEffect, useRef } from "react";
import { cn } from "cn";

/**
 * G4 — CTA manyetik hover. Yalniz transform; 1-2 odak (hero + doruk).
 * ui-ux-pro-max gsap: clamp *0.28, reduced-motion notr.
 */
export function Manyetik({
  children,
  className,
}: {
  children: ReactNode;
  className?: string;
}) {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const azalt = window.matchMedia("(prefers-reduced-motion: reduce)");
    const ince = window.matchMedia("(hover: hover) and (pointer: fine)");
    if (azalt.matches || !ince.matches) return;

    const hareket = (e: PointerEvent) => {
      const r = el.getBoundingClientRect();
      const x = (e.clientX - r.left - r.width / 2) * 0.28;
      const y = (e.clientY - r.top - r.height / 2) * 0.28;
      el.style.transform = `translate3d(${x.toFixed(1)}px, ${y.toFixed(1)}px, 0)`;
    };
    const gir = () => {
      el.style.willChange = "transform";
    };
    const cik = () => {
      el.style.transform = "translate3d(0,0,0)";
      el.style.willChange = "auto";
    };

    el.addEventListener("pointerenter", gir);
    el.addEventListener("pointermove", hareket);
    el.addEventListener("pointerleave", cik);
    return () => {
      el.removeEventListener("pointerenter", gir);
      el.removeEventListener("pointermove", hareket);
      el.removeEventListener("pointerleave", cik);
    };
  }, []);

  return (
    <div ref={ref} className={cn("manyetik inline-flex", className)}>
      {children}
    </div>
  );
}
