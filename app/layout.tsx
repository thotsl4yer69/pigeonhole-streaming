import type { Metadata } from "next";
import "./globals.css";
import { Orbitron, Inter } from "next/font/google";

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
        <div className="absolute inset-0 -z-10 bg-grid bg-[length:40px_40px] opacity-40" />
        <main className="relative flex min-h-screen flex-col items-center justify-start gap-16 px-6 py-10 sm:px-12">
          {children}
        </main>
      </body>
    </html>
  );
}
