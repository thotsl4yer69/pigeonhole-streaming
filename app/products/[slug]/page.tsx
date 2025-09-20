import { notFound } from "next/navigation";
import Image from "next/image";
import { getProductBySlug } from "@/lib/products";
import { CompatibilityBadges } from "@/components/CompatibilityBadges";
import { TMDBPreview } from "@/components/TMDBPreview";
import { Button } from "@/components/ui/button";

interface ProductPageProps {
  params: { slug: string };
}

export default function ProductPage({ params }: ProductPageProps) {
  const product = getProductBySlug(params.slug);

  if (!product) {
    notFound();
  }

  return (
    <div className="mx-auto flex w-full max-w-5xl flex-col gap-12">
      <header className="flex flex-col gap-6 md:flex-row md:items-center md:justify-between">
        <div className="space-y-4">
          <h1 className="font-orbitron text-4xl uppercase tracking-[0.4em] text-cyber-pink">{product.name}</h1>
          <p className="max-w-xl text-cyber-teal/70">{product.description}</p>
          <CompatibilityBadges items={product.compatibility} />
        </div>
        <div className="relative h-72 w-full overflow-hidden rounded-3xl border border-cyber-teal/40 md:w-80">
          <Image src={product.image} alt={product.name} fill className="object-cover" sizes="(max-width: 768px) 100vw, 320px" />
          <div className="scanlines absolute inset-0" />
        </div>
      </header>
      <section className="grid gap-6 md:grid-cols-[2fr_1fr]">
        <div className="glitch-border rounded-3xl bg-crt-glass/70 p-6">
          <h2 className="font-orbitron text-xl uppercase tracking-[0.3em] text-cyber-lime">Core Specs</h2>
          <ul className="mt-4 grid gap-3 text-sm text-white/70">
            {product.specs.map((spec) => (
              <li key={spec} className="rounded border border-cyber-teal/30 px-4 py-3">
                {spec}
              </li>
            ))}
          </ul>
        </div>
        <aside className="flex flex-col gap-4">
          <TMDBPreview collectionId={product.tmdbCollectionId} />
          <div className="glitch-border rounded-3xl bg-black/50 p-6 text-sm text-white/80">
            <p>Price</p>
            <p className="font-orbitron text-2xl text-cyber-pink">{product.price}</p>
            <form action={`/api/checkout/${product.id}`} method="post" className="mt-4">
              <Button type="submit" className="w-full">
                Initiate Checkout
              </Button>
            </form>
          </div>
        </aside>
      </section>
    </div>
  );
}
