import { cn } from "cn";

export function Spinner({ className }: { className?: string }) {
  return (
    <div className={cn("inline-flex size-4 animate-spin", className)} aria-hidden="true">
      <svg viewBox="0 0 16 16" className="size-full" fill="none">
        <circle
          cx="8"
          cy="8"
          r="6"
          stroke="currentColor"
          strokeOpacity="0.25"
          strokeWidth="2"
        />
        <path
          d="M14 8a6 6 0 0 0-6-6"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
        />
      </svg>
    </div>
  );
}
