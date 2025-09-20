import { HeroSection } from "@/components/HeroSection";
import { ProductGrid } from "@/components/ProductCard";
import { TelegramSupport } from "@/components/TelegramSupport";
import { BitcoinPayment } from "@/components/BitcoinPayment";
import { PerformanceHighlights } from "@/components/PerformanceHighlights";

export default function HomePage() {
  return (
    <div className="flex w-full max-w-6xl flex-col gap-16">
      <HeroSection />
      <PerformanceHighlights />
      <ProductGrid />
      <div className="grid gap-8 md:grid-cols-2">
        <TelegramSupport />
        <BitcoinPayment />
      </div>
    </div>
  );
}
