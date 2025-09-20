"use client";

import { motion } from "framer-motion";
import Image from "next/image";
import { Button } from "@/components/ui/button";
import Link from "next/link";

export function HeroSection() {
  return (
    <section
      id="hero"
      className="relative flex w-full flex-col gap-12 overflow-hidden rounded-3xl border border-cyber-pink/50 bg-crt-glass/60 p-10 text-center shadow-glitch"
    >
      <motion.div
        className="absolute inset-0 -z-10 opacity-30"
        initial={{ scale: 1.08, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ duration: 1.4, ease: "easeOut" }}
      >
        <Image src="/crt-pigeon.svg" alt="CRT pigeon silhouette" fill priority className="object-cover" sizes="100vw" />
      </motion.div>
      <motion.h1
        className="font-orbitron text-4xl uppercase tracking-[0.4em] sm:text-5xl"
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
      >
        Pigeonhole Streaming Fleet
      </motion.h1>
      <motion.p
        className="mx-auto max-w-2xl text-balance text-lg text-cyber-teal/80"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2, duration: 0.8 }}
      >
        Neon-infused streaming devices tuned for cinematic obsessives, studio archivists, and audio futurists. Pick a bird, tune
        the glitches, and let the retro CRT hum guide you home.
      </motion.p>
      <motion.div
        className="flex flex-wrap items-center justify-center gap-6"
        initial="hidden"
        animate="show"
        variants={{
          hidden: {},
          show: {
            transition: {
              staggerChildren: 0.1
            }
          }
        }}
      >
        {["Latency Optimized", "Neon Calibrated", "Immersive Audio"].map((badge) => (
          <motion.span
            key={badge}
            className="glitch-border px-4 py-2 text-xs uppercase tracking-[0.3em]"
            variants={{ hidden: { opacity: 0, y: 10 }, show: { opacity: 1, y: 0 } }}
          >
            {badge}
          </motion.span>
        ))}
      </motion.div>
      <motion.div
        className="flex flex-wrap justify-center gap-4"
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ delay: 0.4, duration: 0.5 }}
      >
        <Button asChild>
          <Link href="/products/cyber-finch">Explore Devices</Link>
        </Button>
        <Button variant="ghost" asChild>
          <Link href="/podcast/001">Listen to the Signal</Link>
        </Button>
        <Button variant="outline" asChild>
          <Link href="/about">Meet the Collective</Link>
        </Button>
      </motion.div>
    </section>
  );
}
