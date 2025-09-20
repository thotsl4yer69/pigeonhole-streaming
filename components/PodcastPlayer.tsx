"use client";

import { motion } from "framer-motion";
import { Waves } from "lucide-react";

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
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h2 className="font-orbitron text-lg uppercase tracking-[0.3em] text-cyber-teal">{title}</h2>
          <p className="text-xs text-white/70">Duration: {duration}</p>
        </div>
        <a
          href={audioUrl}
          className="text-[11px] uppercase tracking-[0.35em] text-cyber-pink underline-offset-4 hover:underline"
        >
          Download Episode
        </a>
      </div>
      <p className="text-sm text-cyber-teal/80">{description}</p>
      <div className="flex items-center gap-2 text-xs text-white/50">
        <Waves className="h-4 w-4 text-cyber-lime" />
        <span>Streaming from: {new URL(audioUrl).hostname}</span>
      </div>
      <audio
        controls
        preload="none"
        src={audioUrl}
        className="w-full rounded-2xl bg-black/60"
        aria-label={`Play ${title}`}
      >
        Your browser does not support the audio element. You can
        <a href={audioUrl}> download the episode instead.</a>
      </audio>
    </motion.section>
  );
}
