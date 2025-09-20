import type { Metadata } from "next";
import "./globals.css";
import { Orbitron, Inter } from "next/font/google";
import { SiteHeader } from "@/components/SiteHeader";
import { SiteFooter } from "@/components/SiteFooter";
import { GlobalStructuredData } from "@/components/StructuredData";

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
  metadataBase: new URL("https://mz1312.xx.kg"),
  title: {
    default: "Pigeonhole Streaming",
    template: "%s | Pigeonhole Streaming"
  },
  description: "Retro-futuristic streaming hardware tuned for cinema obsessives.",
  keywords: [
    "streaming hardware",
    "home theater",
    "4K media player",
    "retro futurism",
    "Pigeonhole streaming"
  ],
  openGraph: {
    type: "website",
    url: "https://mz1312.xx.kg",
    siteName: "Pigeonhole Streaming",
    title: "Pigeonhole Streaming",
    description: "Retro-futuristic streaming hardware tuned for cinema obsessives.",
    images: [
      {
        url: "https://mz1312.xx.kg/og-image.jpg",
        width: 1200,
        height: 630,
        alt: "Pigeonhole Streaming neon devices"
      }
    ]
  },
  twitter: {
    card: "summary_large_image",
    title: "Pigeonhole Streaming",
    description: "Retro-futuristic streaming hardware tuned for cinema obsessives.",
    images: ["https://mz1312.xx.kg/og-image.jpg"],
    creator: "@pigeonhole"
  },
  alternates: {
    canonical: "https://mz1312.xx.kg"
  },
  icons: {
    icon: "/favicon.ico",
    apple: "/apple-touch-icon.png"
  },
  themeColor: "#0ff"
};

export default function RootLayout({
  children
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={`${orbitron.variable} ${inter.variable}`} suppressHydrationWarning>
      <body className="min-h-screen bg-crt-screen text-white antialiased">
        <GlobalStructuredData siteUrl="https://mz1312.xx.kg" />
        <a
          href="#main-content"
          className="absolute left-4 top-4 z-50 -translate-y-full rounded bg-cyber-teal px-3 py-2 text-xs font-semibold text-black focus:translate-y-0"
        >
          Skip to main content
        </a>
        <div className="absolute inset-0 -z-10 bg-grid bg-[length:40px_40px] opacity-40" />
        <div className="relative flex min-h-screen w-full flex-col items-center gap-12 px-6 py-10 sm:px-12">
          <SiteHeader />
          <main id="main-content" className="flex w-full flex-1 flex-col items-center gap-16">
            {children}
          </main>
          <SiteFooter />
        </div>
      </body>
    </html>
  );
}
