import "../styles/globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "LEDO War Room",
  description: "Latency-aware dual-path decision router",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
