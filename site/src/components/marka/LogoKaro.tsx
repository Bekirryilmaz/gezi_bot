import Image from "next/image";
import { cn } from "cn";
import { LOGO_MIN_ISARET } from "@/lib/marka";

type Ozellik = {
  boyut?: number;
  className?: string;
  /** Yanindaki wordmark ayni bilgiyi tasiyorsa true. */
  dekoratif?: boolean;
  oncelik?: boolean;
};

/**
 * Secili logo karosu — plan/logo/secili/logo.png turevi.
 * Cizgi/kompozisyon/renk degismez.
 */
export function LogoKaro({
  boyut = 32,
  className,
  dekoratif = false,
  oncelik = false,
}: Ozellik) {
  const kenar = Math.max(boyut, LOGO_MIN_ISARET);
  return (
    <Image
      src="/logo/karo-seffaf.png"
      alt={dekoratif ? "" : "Şamandıra"}
      width={kenar}
      height={kenar}
      className={cn("shrink-0", className)}
      priority={oncelik}
    />
  );
}
