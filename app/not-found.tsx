import Image from "next/image";
import Link from "next/link";

export default function NotFound() {
  return (
    <div className="mx-auto flex w-full max-w-3xl flex-col items-center gap-8 text-center">
      <div className="relative h-48 w-48 overflow-hidden rounded-full border border-cyber-pink/60">
        <Image src="/broken-crt-pigeon.svg" alt="Broken CRT pigeon" fill className="object-contain p-4" sizes="192px" />
        <div className="scanlines absolute inset-0" />
      </div>
      <h1 className="font-orbitron text-3xl uppercase tracking-[0.4em] text-cyber-pink">Signal Lost</h1>
      <p className="text-sm text-cyber-teal/70">
        The Broken CRT pigeon fluttered through a corrupted timeline and the page you&apos;re looking for fractured into static.
        Follow the humming wires back to safety.
      </p>
      <Link
        href="/"
        className="glitch-border inline-flex items-center justify-center rounded-2xl px-6 py-3 font-orbitron text-xs uppercase tracking-[0.3em] text-cyber-teal"
      >
        Return Home
      </Link>
    </div>
  );
}
