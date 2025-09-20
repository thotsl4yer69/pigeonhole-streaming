import Link from "next/link";

export function SiteFooter() {
  return (
    <footer className="w-full max-w-6xl rounded-3xl border border-cyber-teal/30 bg-black/60 p-8 text-sm text-cyber-teal/70">
      <div className="flex flex-col gap-6 md:flex-row md:items-center md:justify-between">
        <div className="space-y-2">
          <p className="font-orbitron text-xs uppercase tracking-[0.4em] text-cyber-pink">Pigeonhole Streaming</p>
          <p className="max-w-md text-xs text-white/60">
            Retro-futuristic streaming fleet engineered for perfect signal integrity and neon-lit living rooms. Built by firmware
            artists who obsess over latency, color science, and cinematic sound.
          </p>
        </div>
        <div className="flex flex-col gap-2 text-xs uppercase tracking-[0.35em] text-cyber-teal">
          <Link className="transition hover:text-cyber-pink" href="mailto:hello@pigeonhole.dev">
            hello@pigeonhole.dev
          </Link>
          <Link className="transition hover:text-cyber-pink" href="https://t.me/pigeonhole-support" target="_blank" rel="noreferrer">
            Telegram Support
          </Link>
          <Link className="transition hover:text-cyber-pink" href="/about">
            Company Manifesto
          </Link>
        </div>
      </div>
      <div className="mt-6 flex flex-wrap items-center justify-between gap-4 text-[10px] uppercase tracking-[0.35em] text-white/40">
        <span>© {new Date().getFullYear()} Pigeonhole Collective</span>
        <span>Optimized for 4K HDR · Zero Buffer Pledge</span>
      </div>
    </footer>
  );
}
