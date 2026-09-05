import { cn } from "cn";

export function Kabuk({
  children,
  className,
  as: Tag = "div",
}: {
  children: React.ReactNode;
  className?: string;
  as?: "div" | "section" | "header" | "article";
}) {
  return <Tag className={cn("kabuk", className)}>{children}</Tag>;
}
