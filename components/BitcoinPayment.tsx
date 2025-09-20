"use client";

import { motion } from "framer-motion";
import Image from "next/image";

export function BitcoinPayment() {
  return (
    <motion.section
      className="glitch-border flex flex-col gap-4 rounded-3xl bg-crt-glass/60 p-6"
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
    >
      <h3 className="font-orbitron text-lg uppercase tracking-[0.3em] text-cyber-lime">Bitcoin Checkout</h3>
      <p className="text-sm text-white/70">
        Route your sats through the Broken CRT node. Once the payment hum stabilizes, our flock initiates shipment.
      </p>
      <div className="relative h-36 w-36 self-center overflow-hidden rounded-2xl border border-cyber-teal/40">
        <Image src="/qr-bitcoin.svg" alt="Bitcoin QR" fill className="object-contain p-4" sizes="144px" />
      </div>
      <p className="text-center text-xs text-cyber-teal/60">Lightning invoices refresh every 15 minutes.</p>
    </motion.section>
  );
}
