"use client";

import { type ReactNode } from "react";
import { motion } from "motion/react";

const EASE: [number, number, number, number] = [0.22, 1, 0.36, 1];

type Ozellik = {
  children: ReactNode;
  delay?: number;
  className?: string;
};

/**
 * Kaydirma ile bir kez gorunen reveal.
 * MotionConfig reducedMotion="user" transform'u kisar; opacity kalir.
 */
export function Reveal({ children, delay = 0, className }: Ozellik) {
  return (
    <motion.div
      className={className}
      initial={{ opacity: 0, y: 18 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, amount: 0.18 }}
      transition={{ duration: 0.55, delay, ease: EASE }}
    >
      {children}
    </motion.div>
  );
}

export function RevealListe({
  children,
  className,
}: {
  children: ReactNode;
  className?: string;
}) {
  return (
    <motion.div
      className={className}
      initial="gizli"
      whileInView="gorunur"
      viewport={{ once: true, amount: 0.12 }}
      variants={{
        gizli: {},
        gorunur: {
          transition: { staggerChildren: 0.08, delayChildren: 0.06 },
        },
      }}
    >
      {children}
    </motion.div>
  );
}

export function RevealOge({
  children,
  className,
}: {
  children: ReactNode;
  className?: string;
}) {
  return (
    <motion.div
      className={className}
      variants={{
        gizli: { opacity: 0, y: 16 },
        gorunur: {
          opacity: 1,
          y: 0,
          transition: { duration: 0.5, ease: EASE },
        },
      }}
    >
      {children}
    </motion.div>
  );
}
