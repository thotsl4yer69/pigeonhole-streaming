import Image from "next/image";
import { Timeline } from "@/components/Timeline";

export default function AboutPage() {
  return (
    <div className="mx-auto flex w-full max-w-5xl flex-col gap-12">
      <header className="glitch-border rounded-3xl bg-crt-glass/70 p-8">
        <div className="flex flex-col gap-6 md:flex-row md:items-center">
          <div className="relative h-40 w-40 shrink-0 overflow-hidden rounded-full border border-cyber-pink/70">
            <Image
              src="/broken-crt-pigeon.svg"
              alt="Broken CRT pigeon"
              fill
              className="object-contain p-4"
              sizes="160px"
            />
          </div>
          <div className="space-y-4">
            <h1 className="font-orbitron text-4xl uppercase tracking-[0.4em] text-cyber-pink">About the Flock</h1>
            <p className="text-sm text-cyber-teal/80">
              Pigeonhole Streaming is a collective of glitch-artists, firmware magicians, and radio pirates building retro-future
              entertainment gear. Our mascot, the Broken CRT pigeon, symbolizes the beauty of fractured signals stitched into a
              coherent experience.
            </p>
          </div>
        </div>
      </header>
      <Timeline />
      <section className="glitch-border rounded-3xl bg-black/40 p-8 text-sm text-cyber-teal/70">
        <h2 className="font-orbitron text-xl uppercase tracking-[0.3em] text-cyber-lime">Manifesto</h2>
        <p className="mt-4">
          We believe the best streams embrace imperfection. Our hardware is tuned to celebrate the artifacts—scanlines,
          chromatic aberrations, buffer whispers—because that texture makes every binge feel alive. Follow the pigeon, trust the
          hum, and never mute the neon.
        </p>
      </section>
    </div>
  );
}
