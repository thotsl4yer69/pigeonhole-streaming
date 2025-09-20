"use client";

import { motion } from "framer-motion";
import { Quote } from "lucide-react";

const testimonials = [
  {
    quote:
      "The Prism Dove Studio shaved hours off our grading pipeline. The TMDB playlists feel like a concierge for our midnight screenings.",
    author: "Mara I., Neon Archive Curator"
  },
  {
    quote:
      "Cyber Finch Prime keeps our esports lounge streaming at 144Hz with zero packet loss. The pigeons know their networks.",
    author: "Dex H., Signal Basement Operator"
  },
  {
    quote:
      "Nocturne Owl Beacon is the only streamer that respects my nocturnal rituals. The ambient underglow pairs with my vinyl perfectly.",
    author: "Jun K., Analog Futurist"
  }
];

export function Testimonials() {
  return (
    <section className="w-full" aria-labelledby="testimonials-heading">
      <div className="flex flex-col gap-4 text-left">
        <h2 id="testimonials-heading" className="font-orbitron text-2xl uppercase tracking-[0.3em] text-cyber-pink">
          Signal Proof
        </h2>
        <p className="max-w-2xl text-sm text-cyber-teal/70">
          Operators from underground cinemas to rooftop lounges trust our fleet to keep the neon humming. Here is a slice of
          their signal reports.
        </p>
      </div>
      <div className="mt-6 grid gap-6 md:grid-cols-3">
        {testimonials.map((item, index) => (
          <motion.figure
            key={item.author}
            className="glitch-border h-full rounded-3xl bg-black/40 p-6"
            initial={{ opacity: 0, y: 24 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: index * 0.1 }}
          >
            <Quote className="h-6 w-6 text-cyber-lime" aria-hidden />
            <blockquote className="mt-4 text-sm text-white/80">“{item.quote}”</blockquote>
            <figcaption className="mt-6 text-xs uppercase tracking-[0.3em] text-cyber-teal/70">{item.author}</figcaption>
          </motion.figure>
        ))}
      </div>
    </section>
  );
}
