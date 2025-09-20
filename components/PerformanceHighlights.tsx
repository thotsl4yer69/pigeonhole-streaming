"use client";

import { motion } from "framer-motion";
import { Gauge, HardDriveDownload, ShieldCheck } from "lucide-react";

const highlights = [
  {
    icon: Gauge,
    title: "Latency Lab Tested",
    description: "Each device ships with firmware tuned to keep response times under 40ms for the most demanding streaming apps."
  },
  {
    icon: HardDriveDownload,
    title: "Instant Library Sync",
    description: "TMDB playlists, Dolby Vision profiles, and calibration LUTs load in seconds with our zero-buffer provisioning pipeline."
  },
  {
    icon: ShieldCheck,
    title: "Fail-Safe Rollbacks",
    description: "Snapshot restores and encrypted diagnostics ensure perfect uptime across the entire pigeonhole fleet."
  }
];

export function PerformanceHighlights() {
  return (
    <section className="flex w-full flex-col gap-8">
      <div className="flex flex-col gap-2 text-left">
        <h2 className="font-orbitron text-2xl uppercase tracking-[0.3em] text-cyber-teal">Why Perfection Matters</h2>
        <p className="max-w-2xl text-sm text-cyber-teal/70">
          Every chassis is battle tested in the Neon Lab to guarantee flawless playback, secure updates, and immersive cinematic
          audio from day one.
        </p>
      </div>
      <div className="grid gap-6 md:grid-cols-3">
        {highlights.map((highlight) => (
          <motion.article
            key={highlight.title}
            className="glitch-border flex flex-col gap-4 rounded-3xl bg-black/40 p-6"
            initial={{ opacity: 0, y: 16 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.4 }}
          >
            <highlight.icon className="h-8 w-8 text-cyber-pink" />
            <h3 className="font-orbitron text-lg uppercase tracking-[0.3em] text-white">{highlight.title}</h3>
            <p className="text-sm text-cyber-teal/80">{highlight.description}</p>
          </motion.article>
        ))}
      </div>
    </section>
  );
}
