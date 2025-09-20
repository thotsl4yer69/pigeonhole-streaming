"use client";

import { motion } from "framer-motion";

const milestones = [
  {
    year: "2021",
    headline: "The First Signal",
    body: "Pigeonhole prototypes stream the first 4K feed from a warehouse CRT wall while synthwave pigeons coo in approval."
  },
  {
    year: "2022",
    headline: "Neon Firmware",
    body: "Firmware engineers unveil the neon glitch overlay that powers latency-reactive UI animations across the fleet."
  },
  {
    year: "2023",
    headline: "TMDB Sync",
    body: "Partnership with TMDB allows every device to sync curated collections with a single tap from the companion app."
  },
  {
    year: "2024",
    headline: "Broken CRT Pigeon",
    body: "The iconic mascot is reborn as a fractured hologram guiding fans through the portal between analog and digital."
  }
];

export function Timeline() {
  return (
    <section className="flex w-full flex-col gap-6">
      <h2 className="font-orbitron text-2xl uppercase tracking-[0.3em] text-cyber-teal">Flight Log</h2>
      <div className="relative space-y-8 border-l border-cyber-teal/40 pl-8">
        {milestones.map((milestone, index) => (
          <motion.div
            key={milestone.year}
            className="relative"
            initial={{ opacity: 0, x: -20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ delay: index * 0.1 }}
          >
            <span className="absolute -left-10 flex h-6 w-6 items-center justify-center rounded-full border border-cyber-pink bg-black text-xs font-orbitron text-cyber-pink">
              {milestone.year}
            </span>
            <h3 className="font-orbitron text-lg uppercase tracking-[0.2em] text-cyber-lime">{milestone.headline}</h3>
            <p className="text-sm text-white/70">{milestone.body}</p>
          </motion.div>
        ))}
      </div>
    </section>
  );
}
