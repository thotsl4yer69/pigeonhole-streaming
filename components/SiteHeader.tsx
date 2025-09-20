import Link from "next/link";
import { Button } from "@/components/ui/button";

const navigation = [
  { href: "/#devices", label: "Devices" },
  { href: "/podcast/001", label: "Podcast" },
  { href: "/about", label: "About" }
];

export function SiteHeader() {
  return (
    <header className="sticky top-0 z-40 w-full max-w-6xl rounded-full border border-cyber-teal/40 bg-black/70 backdrop-blur">
      <div className="flex flex-wrap items-center justify-between gap-4 px-6 py-4">
        <Link href="/" className="font-orbitron text-sm uppercase tracking-[0.4em] text-cyber-pink">
          Pigeonhole Streaming
        </Link>
        <nav aria-label="Primary" className="flex flex-1 items-center justify-center gap-6 text-[11px] uppercase tracking-[0.35em]">
          {navigation.map((item) => (
            <Link key={item.href} href={item.href} className="text-cyber-teal/80 transition hover:text-cyber-pink">
              {item.label}
            </Link>
          ))}
        </nav>
        <div className="flex items-center gap-3">
          <Button asChild size="sm">
            <Link href="https://t.me/pigeonhole-support" target="_blank" rel="noreferrer">
              Talk to an Engineer
            </Link>
          </Button>
        </div>
      </div>
    </header>
  );
}
