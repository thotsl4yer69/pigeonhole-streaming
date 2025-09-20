"use client";

import { motion } from "framer-motion";
import { Film } from "lucide-react";

interface TMDBPreviewProps {
  collectionId?: number;
}

export function TMDBPreview({ collectionId }: TMDBPreviewProps) {
  if (!collectionId) {
    return null;
  }

  return (
    <motion.div
      className="glitch-border flex items-center gap-3 rounded-2xl bg-black/40 px-4 py-3 text-xs text-cyber-teal"
      initial={{ opacity: 0, y: 10 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
    >
      <Film className="h-4 w-4 text-cyber-pink" />
      <div>
        <p className="font-orbitron uppercase tracking-[0.3em]">TMDB Sync</p>
        <p className="text-[11px] text-white/70">Auto-curated collection #{collectionId}</p>
      </div>
    </motion.div>
  );
}
