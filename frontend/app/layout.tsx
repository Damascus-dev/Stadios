import type { Metadata, Viewport } from "next";
import "./globals.css";
import AppShell from "./components/AppShell";

export const metadata: Metadata = {
  title: "StadiumOS Navigator — AI Stadium Navigation",
  description:
    "AI-powered interactive stadium navigation for FIFA World Cup 2026. 3D Digital Twin with explainable routing.",
  manifest: "/manifest.json",
  appleWebApp: {
    capable: true,
    statusBarStyle: "black-translucent",
    title: "StadiumOS Navigator",
  },
  other: {
    "mobile-web-app-capable": "yes",
  },
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  maximumScale: 1,
  viewportFit: "cover",
  themeColor: "#0a0e1a",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="h-full antialiased">
      <body className="min-h-full bg-[#0a0e1a] text-white font-[Inter,system-ui,sans-serif]">
        <AppShell>{children}</AppShell>
      </body>
    </html>
  );
}
