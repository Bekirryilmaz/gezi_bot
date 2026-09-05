import { cn } from "cn";

export function KesilenAyrac({ className }: { className?: string }) {
  return (
    <div className={cn("flex items-center", className)} aria-hidden="true">
      <span className="bg-bordo/12 h-px flex-1" />
      <span className="w-1.5 shrink-0" />
      <span className="bg-bordo/12 h-px flex-1" />
    </div>
  );
}
