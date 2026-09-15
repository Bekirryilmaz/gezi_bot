"use client";

import { useEffect, useRef } from "react";
import Link from "next/link";

const FRAME_COUNT = 216;
const FOCUS_X = 0.42;
const FOCUS_Y = 0.28;
const frameSrc = (i: number) => `/hero/sequence/frame_${String(i).padStart(4, "0")}.webp`;

// [başlangıç, bitiş] scroll aralıkları + senaryo perdeleri
const CAPTIONS = [
  {
    from: 0.03,
    to: 0.25,
    title: "Bilmediğin şehirde kaybolma.",
    sub: "Şamandıra seni yönlendirir.",
  },
  {
    from: 0.28,
    to: 0.5,
    title: "Çantanı al, gerisini bize bırak.",
    sub: "Deneyimine göre rota kurulur.",
  },
  { from: 0.53, to: 0.75, title: "1.719 yer işaretli.", sub: "15 ilçe, gün gün plan." },
  { from: 0.78, to: 1.0, title: "Rotanı kur.", sub: "" },
];

export default function ScrollHero() {
  const sectionRef = useRef<HTMLElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const captionRefs = useRef<(HTMLDivElement | null)[]>([]);

  useEffect(() => {
    const canvas = canvasRef.current!;
    const ctx = canvas.getContext("2d")!;
    const section = sectionRef.current!;
    const images: (HTMLImageElement | null)[] = new Array(FRAME_COUNT + 1).fill(null);
    let raf = 0,
      drawn = -1,
      cancelled = false;
    let current = 1,
      target = 1,
      ticking = false;
    const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    const fitCanvas = () => {
      const dpr = Math.min(window.devicePixelRatio || 1, 2);
      canvas.width = Math.floor(canvas.clientWidth * dpr);
      canvas.height = Math.floor(canvas.clientHeight * dpr);
      drawn = -1;
      update();
    };

    const drawCover = (img: HTMLImageElement) => {
      const s = Math.max(
        canvas.width / img.naturalWidth,
        canvas.height / img.naturalHeight,
      );
      const w = img.naturalWidth * s,
        h = img.naturalHeight * s;
      ctx.drawImage(
        img,
        (canvas.width - w) * FOCUS_X,
        (canvas.height - h) * FOCUS_Y,
        w,
        h,
      );
    };

    const tick = () => {
      const diff = target - current;
      if (Math.abs(diff) < 0.05) current = target;
      else current += diff * 0.16;
      const idx = Math.max(1, Math.min(FRAME_COUNT, Math.round(current)));
      const img = images[idx] ?? images.slice(1).find(Boolean);
      if (img && img !== images[drawn]) {
        drawCover(img);
        drawn = images.indexOf(img);
      }
      if (current !== target && !cancelled) requestAnimationFrame(tick);
      else ticking = false;
    };

    const update = () => {
      raf = 0;
      const total = section.offsetHeight - window.innerHeight;
      const p = Math.min(1, Math.max(0, -section.getBoundingClientRect().top / total));

      target = reduced ? FRAME_COUNT : 1 + Math.round(p * (FRAME_COUNT - 1));
      if (!ticking) {
        ticking = true;
        requestAnimationFrame(tick);
      }

      CAPTIONS.forEach((c, i) => {
        const el = captionRefs.current[i];
        if (!el) return;
        const fade = 0.04;
        const vis = Math.min(1, (p - c.from) / fade, (c.to - p) / fade);
        el.style.opacity = String(Math.max(0, Math.min(1, vis)));
        el.style.transform = `translateY(${(1 - Math.max(0, Math.min(1, vis))) * 30}px)`;
      });
    };

    const onScroll = () => {
      if (!raf) raf = requestAnimationFrame(update);
    };
    const loadOne = (i: number) =>
      new Promise<void>((res) => {
        const img = new Image();
        (img as HTMLImageElement).decoding = "async";
        img.onload = () => {
          images[i] = img;
          update();
          res();
        };
        img.onerror = () => res();
        img.src = frameSrc(i);
      });

    (async () => {
      await loadOne(1);
      const CONC = 6;
      for (let s = 2; s <= FRAME_COUNT && !cancelled; s += CONC) {
        await Promise.all(
          Array.from({ length: Math.min(CONC, FRAME_COUNT - s + 1) }, (_, k) =>
            loadOne(s + k),
          ),
        );
      }
    })();

    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", fitCanvas);
    fitCanvas();
    return () => {
      cancelled = true;
      cancelAnimationFrame(raf);
      window.removeEventListener("scroll", onScroll);
      window.removeEventListener("resize", fitCanvas);
    };
  }, []);

  return (
    <section ref={sectionRef} className="relative h-[350vh] md:h-[450vh]">
      <div className="sticky top-0 h-screen overflow-hidden bg-black">
        <img
          src="/hero/sequence/frame_0001.webp"
          alt=""
          className="absolute inset-0 h-full w-full object-cover"
        />
        <canvas ref={canvasRef} className="absolute inset-0 h-full w-full" />
        <div className="pointer-events-none absolute inset-0 flex items-center justify-center">
          {CAPTIONS.map((c, i) => (
            <div
              key={i}
              ref={(el) => {
                captionRefs.current[i] = el;
              }}
              className="absolute px-6 text-center opacity-0"
            >
              <p className="text-3xl font-bold text-white drop-shadow-lg md:text-5xl">
                {c.title}
              </p>
              {c.sub && <p className="mt-3 text-lg text-white/80 md:text-xl">{c.sub}</p>}
              {i === CAPTIONS.length - 1 && (
                <Link
                  href="/sehir/samsun/rota"
                  className="pointer-events-auto mt-6 inline-block rounded-full bg-white px-8 py-3 font-semibold text-black"
                >
                  Hemen başla
                </Link>
              )}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
