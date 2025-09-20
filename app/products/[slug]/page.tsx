import type { Metadata } from "next";
import { notFound } from "next/navigation";
import Image from "next/image";
import { getProductBySlug, products } from "@/lib/products";
import { CompatibilityBadges } from "@/components/CompatibilityBadges";
import { TMDBPreview } from "@/components/TMDBPreview";
import { CheckoutButton } from "@/components/CheckoutButton";
import { ProductStructuredData } from "@/components/StructuredData";

const siteUrl = "https://mz1312.xx.kg";

interface ProductPageProps {
  params: { slug: string };
}

export function generateStaticParams() {
  return products.map((product) => ({ slug: product.slug }));
}

export function generateMetadata({ params }: ProductPageProps): Metadata {
  const product = getProductBySlug(params.slug);

  if (!product) {
    return {
      title: "Product not found"
    };
  }

  const canonical = `${siteUrl}/products/${product.slug}`;

  return {
    title: product.name,
    description: product.description,
    alternates: { canonical },
    openGraph: {
      type: "product",
      url: canonical,
      title: product.name,
      description: product.description,
      images: [{ url: `${siteUrl}${product.image}`, width: 1200, height: 675, alt: product.name }]
    },
    twitter: {
      card: "summary_large_image",
      title: product.name,
      description: product.description,
      images: [`${siteUrl}${product.image}`]
    }
  };
}

export default function ProductPage({ params }: ProductPageProps) {
  const product = getProductBySlug(params.slug);

  if (!product) {
    notFound();
  }

  return (
    <div className="mx-auto flex w-full max-w-5xl flex-col gap-12">
      <ProductStructuredData product={product} siteUrl={siteUrl} />
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
            <CheckoutButton productId={product.id} productName={product.name} />
          </div>
        </aside>
      </section>
    </div>
  );
}
