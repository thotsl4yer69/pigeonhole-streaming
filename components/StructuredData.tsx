interface GlobalStructuredDataProps {
  siteUrl: string;
}

export function GlobalStructuredData({ siteUrl }: GlobalStructuredDataProps) {
  const data = {
    "@context": "https://schema.org",
    "@type": "Organization",
    name: "Pigeonhole Streaming",
    url: siteUrl,
    sameAs: ["https://t.me/pigeonhole-support"],
    slogan: "Retro-futuristic streaming hardware tuned for perfect neon cinema.",
    contactPoint: [
      {
        "@type": "ContactPoint",
        contactType: "customer support",
        areaServed: "Worldwide",
        availableLanguage: ["English"],
        email: "hello@pigeonhole.dev"
      }
    ]
  };

  return (
    <script type="application/ld+json" suppressHydrationWarning dangerouslySetInnerHTML={{ __html: JSON.stringify(data) }} />
  );
}

interface ProductStructuredDataProps {
  product: {
    name: string;
    description: string;
    price: string;
    image: string;
    compatibility: string[];
    slug: string;
  };
  siteUrl: string;
}

export function ProductStructuredData({ product, siteUrl }: ProductStructuredDataProps) {
  const priceValue = Number(product.price.replace(/[^0-9.]/g, ""));
  const data = {
    "@context": "https://schema.org",
    "@type": "Product",
    name: product.name,
    description: product.description,
    image: `${siteUrl}${product.image}`,
    sku: product.slug,
    brand: {
      "@type": "Brand",
      name: "Pigeonhole Streaming"
    },
    offers: {
      "@type": "Offer",
      priceCurrency: "USD",
      price: priceValue || undefined,
      availability: "https://schema.org/PreOrder",
      url: `${siteUrl}/products/${product.slug}`
    },
    additionalProperty: product.compatibility.map((item) => ({
      "@type": "PropertyValue",
      name: "Compatibility",
      value: item
    }))
  };

  return (
    <script type="application/ld+json" suppressHydrationWarning dangerouslySetInnerHTML={{ __html: JSON.stringify(data) }} />
  );
}

interface PodcastStructuredDataProps {
  episode: {
    id: string;
    title: string;
    description: string;
    audioUrl: string;
    publishedAt: string;
    duration: string;
  };
  siteUrl: string;
}

export function PodcastStructuredData({ episode, siteUrl }: PodcastStructuredDataProps) {
  const [minutes, seconds = 0] = episode.duration.split(":").map(Number);
  const isoDuration = `PT${minutes || 0}M${seconds || 0}S`;

  const data = {
    "@context": "https://schema.org",
    "@type": "PodcastEpisode",
    name: episode.title,
    description: episode.description,
    url: `${siteUrl}/podcast/${episode.id}`,
    datePublished: episode.publishedAt,
    duration: isoDuration,
    episodeNumber: Number(episode.id),
    partOfSeries: {
      "@type": "PodcastSeries",
      name: "Signal Boost Podcast",
      url: `${siteUrl}/podcast/${episode.id}`
    },
    audio: {
      "@type": "AudioObject",
      contentUrl: episode.audioUrl,
      encodingFormat: "audio/mpeg"
    }
  };

  return (
    <script type="application/ld+json" suppressHydrationWarning dangerouslySetInnerHTML={{ __html: JSON.stringify(data) }} />
  );
}
