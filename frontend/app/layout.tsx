import type { Metadata } from "next";
import "./globals.css";
import Sidebar from "./components/Sidebar";

export const metadata: Metadata = {
  title: "StadiumOS AI — FIFA World Cup 2026",
  description:
    "AI Operating System for FIFA World Cup 2026 stadium operations. Real-time crowd management, navigation, and accessibility powered by multi-agent AI.",
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
        <main className="flex-1">{children}</main>
      </body>
    </html>
  );
}
