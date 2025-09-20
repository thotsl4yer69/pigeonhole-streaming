import type { Metadata } from "next";
import "./globals.css";
import { Orbitron, Inter } from "next/font/google";
import { SiteHeader } from "@/components/SiteHeader";
import { SiteFooter } from "@/components/SiteFooter";

const orbitron = Orbitron({
  subsets: ["latin"],
  variable: "--font-orbitron",
  display: "swap"
});

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap"
});

export const metadata: Metadata = {
  title: "Pigeonhole Streaming",
  description: "Retro-futuristic streaming hardware marketplace"
};

export default function RootLayout({
  children
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={`${orbitron.variable} ${inter.variable}`} suppressHydrationWarning>
      <body className="min-h-screen bg-crt-screen text-white antialiased">
        <div className="pointer-events-none absolute inset-0 -z-10 bg-grid bg-[length:40px_40px] opacity-40" />
        <a
          href="#main-content"
          className="absolute left-4 top-4 z-50 -translate-y-20 rounded-full border border-cyber-teal/60 bg-black px-4 py-2 text-xs uppercase tracking-[0.3em] text-white transition focus:translate-y-0 focus:outline-none"
        >
          Skip to content
        </a>
        <div className="relative mx-auto flex min-h-screen w-full max-w-7xl flex-col items-center gap-10 px-6 pb-12 pt-8 sm:px-12">
          <SiteHeader />
          <main id="main-content" className="flex w-full max-w-6xl flex-1 flex-col items-center gap-16 pb-12">
            {children}
          </main>
          <SiteFooter />
        </div>
      </body>
    </html>
  );
}
