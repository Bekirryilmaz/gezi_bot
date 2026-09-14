import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Admin | Şamandıra",
  robots: { index: false, follow: false },
};

export default function AdminLayout({ children }: { children: React.ReactNode }) {
  return <div data-admin-alani="true">{children}</div>;
}
