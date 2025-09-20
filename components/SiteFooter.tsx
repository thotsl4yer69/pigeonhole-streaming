import Link from "next/link";
import { Mail, Radio, Shield } from "lucide-react";

const quickLinks = [
  { label: "Device Fleet", href: "/#devices" },
  { label: "About", href: "/about" },
  { label: "Podcast", href: "/podcast/001" }
];

const supportLinks = [
  { label: "Telegram Support", href: "https://t.me/pigeonhole-support" },
  { label: "Status Page", href: "https://status.pigeonhole.dev" },
  { label: "Firmware Notes", href: "https://updates.pigeonhole.dev" }
];

export function SiteFooter() {
  return (
    <footer className="w-full border-t border-cyber-teal/20 bg-black/40">
      <div className="mx-auto flex w-full max-w-6xl flex-col gap-10 px-6 py-10 sm:px-12">
        <div className="grid gap-10 md:grid-cols-3">
          <div className="space-y-3">
            <p className="font-orbitron text-xs uppercase tracking-[0.4em] text-cyber-pink">Pigeonhole Streaming</p>
            <p className="text-sm text-cyber-teal/70">
              Retro-futuristic entertainment gear engineered for enthusiasts chasing the perfect neon glow and frame-perfect
              latency.
            </p>
            <div className="flex items-center gap-3 text-xs text-cyber-teal/60">
              <Radio className="h-4 w-4" aria-hidden />
              <span>Broadcasting from the Broken CRT lab · Since 2021</span>
            </div>
          </div>
          <div>
            <h2 className="font-orbitron text-sm uppercase tracking-[0.3em] text-white">Quick Links</h2>
            <ul className="mt-4 space-y-2 text-sm text-cyber-teal/70">
              {quickLinks.map((item) => (
                <li key={item.href}>
                  <Link className="hover:text-white" href={item.href}>
                    {item.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
          <div>
            <h2 className="font-orbitron text-sm uppercase tracking-[0.3em] text-white">Support</h2>
            <ul className="mt-4 space-y-2 text-sm text-cyber-teal/70">
              {supportLinks.map((item) => (
                <li key={item.href}>
                  <Link className="hover:text-white" href={item.href}>
                    {item.label}
                  </Link>
                </li>
              ))}
            </ul>
            <div className="mt-4 flex flex-col gap-2 text-xs text-cyber-teal/60">
              <div className="flex items-center gap-2">
                <Shield className="h-4 w-4" aria-hidden />
                <span>Encrypted logistics & zero telemetry promise</span>
              </div>
              <div className="flex items-center gap-2">
                <Mail className="h-4 w-4" aria-hidden />
                <a className="hover:text-white" href="mailto:signal@pigeonhole.dev">
                  signal@pigeonhole.dev
                </a>
              </div>
            </div>
          </div>
        </div>
        <p className="text-center text-[11px] uppercase tracking-[0.3em] text-cyber-teal/50">
          © {new Date().getFullYear()} Pigeonhole Streaming. All rights reverberate in the neon ether.
        </p>
      </div>
    </footer>
  );
}
