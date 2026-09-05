import { cn } from "cn";

/** Logodan halka + nokta — jenerik damla pin yok. */
export function Markir({
  className,
  boyut = 16,
}: {
  className?: string;
  boyut?: number;
}) {
  return (
    <svg
      width={boyut}
      height={boyut}
      viewBox="0 0 16 16"
      className={cn("shrink-0", className)}
      aria-hidden="true"
    >
      <circle
        cx="8"
        cy="8"
        r="5.25"
        fill="none"
        stroke="currentColor"
        strokeWidth="1.25"
      />
      <circle cx="8" cy="8" r="1.75" fill="currentColor" />
    </svg>
  );
}
