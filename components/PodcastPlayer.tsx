"use client";

import { motion } from "framer-motion";
import { Play, Waves } from "lucide-react";

interface PodcastPlayerProps {
  title: string;
  description: string;
  duration: string;
  audioUrl: string;
}

export function PodcastPlayer({ title, description, duration, audioUrl }: PodcastPlayerProps) {
  return (
    <motion.section
      className="glitch-border flex flex-col gap-4 rounded-3xl bg-crt-glass/60 p-6"
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <div className="flex items-center gap-3">
        <div className="flex h-12 w-12 items-center justify-center rounded-full border border-cyber-teal/40 bg-black/50">
          <Play className="h-6 w-6 text-cyber-pink" />
        </div>
        <div>
          <h2 className="font-orbitron text-lg uppercase tracking-[0.3em] text-cyber-teal">{title}</h2>
          <p className="text-xs text-white/70">Duration: {duration}</p>
        </div>
      </div>
      <p className="text-sm text-cyber-teal/80">{description}</p>
      <div className="flex items-center gap-2 text-xs text-white/50">
        <Waves className="h-4 w-4 text-cyber-lime" />
        <span>Streaming a simulated feed from: {audioUrl}</span>
      </div>
      <button
        type="button"
        className="glitch-border relative overflow-hidden rounded-2xl bg-gradient-to-r from-cyber-pink/40 via-cyber-teal/40 to-cyber-lime/40 px-5 py-3 text-xs uppercase tracking-[0.4em]"
        onClick={() => {
          console.info("Pretend to play", audioUrl);
        }}
      >
        Engage Playback
      </button>
    </motion.section>
  );
}
