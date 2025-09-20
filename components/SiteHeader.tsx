"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import { Menu, X } from "lucide-react";
import { Button } from "@/components/ui/button";

const navItems = [
  { label: "Home", href: "/" },
  { label: "Devices", href: "/#devices" },
  { label: "About", href: "/about" },
  { label: "Podcast", href: "/podcast/001" }
];

export function SiteHeader() {
  const pathname = usePathname();
  const [isMenuOpen, setMenuOpen] = useState(false);

  return (
    <header className="sticky top-4 z-50 w-full max-w-6xl">
      <motion.nav
        className="glitch-border flex items-center justify-between rounded-3xl bg-black/40 px-6 py-4 backdrop-blur"
        initial={{ opacity: 0, y: -16 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
        aria-label="Primary"
      >
        <Link href="/" className="font-orbitron text-sm uppercase tracking-[0.4em] text-cyber-teal">
          Broken CRT Pigeon
        </Link>
        <div className="hidden items-center gap-6 md:flex">
          <ul className="flex items-center gap-6 text-xs uppercase tracking-[0.3em] text-cyber-teal/80">
            {navItems.map((item) => {
              const isActive = pathname === item.href || (item.href !== "/" && pathname?.startsWith(item.href));
              return (
                <li key={item.href}>
                  <Link
                    href={item.href}
                    className={`relative transition-colors hover:text-white ${isActive ? "text-white" : ""}`}
                  >
                    {item.label}
                    {isActive ? (
                      <motion.span
                        layoutId="active-pill"
                        className="absolute -bottom-2 left-0 h-[2px] w-full bg-gradient-to-r from-cyber-pink to-cyber-lime"
                      />
                    ) : null}
                  </Link>
                </li>
              );
            })}
          </ul>
          <Button asChild size="sm">
            <Link href="/products/cyber-finch">Book a Demo</Link>
          </Button>
        </div>
        <button
          type="button"
          className="flex h-10 w-10 items-center justify-center rounded-full border border-cyber-teal/40 text-cyber-teal md:hidden"
          aria-label="Toggle navigation menu"
          onClick={() => setMenuOpen((prev) => !prev)}
        >
          {isMenuOpen ? <X className="h-5 w-5" aria-hidden /> : <Menu className="h-5 w-5" aria-hidden />}
        </button>
      </motion.nav>
      <AnimatePresence>
        {isMenuOpen ? (
          <motion.div
            key="mobile-menu"
            initial={{ opacity: 0, y: -8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -8 }}
            transition={{ duration: 0.2 }}
            className="mt-3 overflow-hidden rounded-3xl border border-cyber-teal/40 bg-black/60 md:hidden"
          >
            <ul className="flex flex-col divide-y divide-cyber-teal/20 text-sm uppercase tracking-[0.3em]">
              {navItems.map((item) => {
                const isActive = pathname === item.href || (item.href !== "/" && pathname?.startsWith(item.href));
                return (
                  <li key={item.href}>
                    <Link
                      href={item.href}
                      className={`block px-6 py-4 transition-colors hover:bg-cyber-teal/10 ${
                        isActive ? "text-cyber-lime" : "text-cyber-teal/80"
                      }`}
                      onClick={() => setMenuOpen(false)}
                    >
                      {item.label}
                    </Link>
                  </li>
                );
              })}
              <li className="px-6 py-4">
                <Button asChild size="sm" className="w-full" onClick={() => setMenuOpen(false)}>
                  <Link href="/products/cyber-finch">Book a Demo</Link>
                </Button>
              </li>
            </ul>
          </motion.div>
        ) : null}
      </AnimatePresence>
    </header>
  );
}
