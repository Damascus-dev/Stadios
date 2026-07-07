import type { Metadata, Viewport } from "next";
import "./globals.css";
import Sidebar from "./components/Sidebar";

export const metadata: Metadata = {
  title: "StadiumOS AI — FIFA World Cup 2026",
  description:
    "AI Operating System for FIFA World Cup 2026 stadium operations. Real-time crowd management, navigation, and accessibility powered by multi-agent AI.",
  manifest: "/manifest.json",
  appleWebApp: {
    capable: true,
    statusBarStyle: "black-translucent",
    title: "StadiumOS AI",
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
      <body className="min-h-full flex bg-[#0a0e1a] text-white font-[Inter,system-ui,sans-serif]">
        <Sidebar />
        <main className="flex-1 pb-[70px] md:pb-0 md:ml-[68px]">{children}</main>
      </body>
    </html>
  );
}
