import Image from "next/image";
import { Timeline } from "@/components/Timeline";

const pillars = [
  {
    title: "Signal Craft",
    body: "Firmware built in-house with nightly regression sweeps across latency, color accuracy, and glitch stability benchmarks."
  },
  {
    title: "Analog Reverence",
    body: "We study cathode ray artifacts, magnetic interference, and VHS flutter to reimagine them as modern interface poetry."
  },
  {
    title: "Community First",
    body: "The flock co-designs features inside our Telegram lab. Feature flags and roadmap votes are transparent to every member."
  }
];

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
      <section className="grid gap-6 md:grid-cols-3" aria-labelledby="pillar-heading">
        <h2
          id="pillar-heading"
          className="md:col-span-3 font-orbitron text-2xl uppercase tracking-[0.3em] text-cyber-lime"
        >
          What Guides the Flock
        </h2>
        {pillars.map((pillar) => (
          <div key={pillar.title} className="glitch-border rounded-3xl bg-black/40 p-6 text-sm text-cyber-teal/70">
            <h3 className="font-orbitron text-base uppercase tracking-[0.3em] text-white">{pillar.title}</h3>
            <p className="mt-3 leading-relaxed">{pillar.body}</p>
          </div>
        ))}
      </section>
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
