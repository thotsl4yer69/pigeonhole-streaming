"use client";

import { motion } from "framer-motion";
import Link from "next/link";
import { products, type Product } from "@/lib/products";
import { CompatibilityBadges } from "@/components/CompatibilityBadges";

export function ProductGrid() {
  return (
    <section className="flex w-full flex-col gap-10">
      <div className="flex flex-col gap-2 text-left">
        <h2 className="font-orbitron text-3xl uppercase tracking-[0.3em] text-cyber-pink">Device Lineup</h2>
        <p className="max-w-2xl text-cyber-teal/70">
          Precision-calibrated streamers engineered for glitch-art lovers, colorists, and home theater renegades. Tap into the
          collection for curated movie nights via TMDB playlists.
        </p>
      </div>
      <div className="grid gap-8 md:grid-cols-3">
        {products.map((product, index) => (
          <ProductCard key={product.id} product={product} index={index} />
        ))}
      </div>
    </section>
  );
}

interface ProductCardProps {
  product: Product;
  index: number;
}

export function ProductCard({ product, index }: ProductCardProps) {
  return (
    <motion.article
      className="glitch-border flex flex-col gap-6 rounded-3xl bg-crt-glass/70 p-6"
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ delay: index * 0.08 }}
    >
      <div className="relative overflow-hidden rounded-2xl border border-cyber-teal/40">
        <motion.img
          src={product.image}
          alt={product.name}
          className="h-40 w-full object-cover"
          initial={{ scale: 1.1 }}
          whileHover={{ scale: 1.2 }}
          transition={{ type: "spring", stiffness: 120 }}
        />
        <div className="scanlines absolute inset-0" />
      </div>
      <div className="flex flex-col gap-3">
        <h3 className="font-orbitron text-xl uppercase tracking-[0.2em] text-cyber-lime">{product.name}</h3>
        <p className="text-sm text-cyber-teal/70">{product.tagline}</p>
        <p className="text-sm text-white/80">{product.description}</p>
      </div>
      <CompatibilityBadges items={product.compatibility} />
      <ul className="grid grid-cols-2 gap-2 text-xs text-cyber-teal/80">
        {product.specs.map((spec) => (
          <li key={spec} className="rounded border border-cyber-teal/30 px-3 py-2">
            {spec}
          </li>
        ))}
      </ul>
      <div className="mt-auto flex items-center justify-between text-sm text-cyber-pink">
        <span className="font-orbitron text-lg">{product.price}</span>
        <Link
          href={`/products/${product.slug}`}
          className="font-orbitron text-xs uppercase tracking-[0.3em] text-cyber-teal hover:text-cyber-pink"
        >
          View Specs
        </Link>
      </div>
    </motion.article>
  );
}
