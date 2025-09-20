"use client";

import { motion } from "framer-motion";

interface CompatibilityBadgesProps {
  items: string[];
}

export function CompatibilityBadges({ items }: CompatibilityBadgesProps) {
  return (
    <div className="flex flex-wrap gap-3">
      {items.map((item, index) => (
        <motion.span
          key={item}
          className="glitch-border px-3 py-1 text-[10px] uppercase tracking-[0.35em] text-cyber-teal"
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: index * 0.05 }}
        >
          {item}
        </motion.span>
      ))}
    </div>
  );
}
