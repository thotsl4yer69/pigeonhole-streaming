import { HeroSection } from "@/components/HeroSection";
import { FeatureShowcase } from "@/components/FeatureShowcase";
import { ProductGrid } from "@/components/ProductCard";
import { TelegramSupport } from "@/components/TelegramSupport";
import { BitcoinPayment } from "@/components/BitcoinPayment";
import { Testimonials } from "@/components/Testimonials";

export default function HomePage() {
  return (
    <div className="flex w-full max-w-6xl flex-col gap-16">
      <HeroSection />
      <FeatureShowcase />
      <ProductGrid />
      <div className="grid gap-8 md:grid-cols-2">
        <TelegramSupport />
        <BitcoinPayment />
      </div>
      <Testimonials />
    </div>
  );
}
