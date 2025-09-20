"use client";

import { motion } from "framer-motion";
import { MessageCircle } from "lucide-react";
import { Button } from "@/components/ui/button";

export function TelegramSupport() {
  return (
    <motion.section
      className="glitch-border flex flex-col gap-4 rounded-3xl bg-crt-glass/60 p-6"
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
    >
      <div className="flex items-center gap-3">
        <MessageCircle className="h-6 w-6 text-cyber-teal" />
        <h3 className="font-orbitron text-lg uppercase tracking-[0.3em] text-cyber-teal">Telegram Concierge</h3>
      </div>
      <p className="text-sm text-white/70">
        Join the encrypted flock for 24/7 firmware drops, neon calibration tips, and to DM the engineers who birthed the Broken
        CRT pigeon.
      </p>
      <Button asChild>
        <a href="https://t.me/pigeonhole-support" target="_blank" rel="noreferrer">
          Open Secure Channel
        </a>
      </Button>
    </motion.section>
  );
}
