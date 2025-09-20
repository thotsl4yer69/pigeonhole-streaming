"use client";

import { motion } from "framer-motion";
import { Cpu, Gauge, Waves } from "lucide-react";

const features = [
  {
    title: "Adaptive Throughput",
    description: "Latency-reactive firmware auto-tunes bitrates in 12ms cycles for pristine playback during peak congestion.",
    icon: Gauge
  },
  {
    title: "Cinematic Pipeline",
    description: "12-bit color management with TMDB playlist syncing so every session opens on the perfect curated reel.",
    icon: Cpu
  },
  {
    title: "Immersive Audio",
    description: "Spatial audio chambers with phase-aligned subsonics engineered for nocturnal binge rituals.",
    icon: Waves
  }
];

export function FeatureShowcase() {
  return (
    <section className="glitch-border w-full rounded-3xl bg-black/40 p-8" aria-labelledby="feature-showcase-heading">
      <div className="flex flex-col gap-4 text-left">
        <h2
          id="feature-showcase-heading"
          className="font-orbitron text-2xl uppercase tracking-[0.3em] text-cyber-lime"
        >
          Why the Fleet Wins
        </h2>
        <p className="max-w-2xl text-sm text-cyber-teal/70">
          Every device harmonizes bespoke hardware with neon-soaked firmware. These pillars ensure our pigeons glide
          effortlessly through any home theater ecosystem.
        </p>
      </div>
      <div className="mt-8 grid gap-6 md:grid-cols-3">
        {features.map((feature, index) => {
          const Icon = feature.icon;
          return (
            <motion.article
              key={feature.title}
              className="rounded-2xl border border-cyber-teal/30 bg-crt-glass/50 p-6"
              initial={{ opacity: 0, y: 24 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.1 }}
            >
              <div className="flex h-12 w-12 items-center justify-center rounded-full border border-cyber-teal/40 bg-black/40">
                <Icon className="h-6 w-6 text-cyber-pink" aria-hidden />
              </div>
              <h3 className="mt-4 font-orbitron text-lg uppercase tracking-[0.2em] text-white">{feature.title}</h3>
              <p className="mt-2 text-sm text-cyber-teal/70">{feature.description}</p>
            </motion.article>
          );
        })}
      </div>
    </section>
  );
}
