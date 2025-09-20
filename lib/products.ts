export type Product = {
  id: string;
  slug: string;
  name: string;
  tagline: string;
  description: string;
  price: string;
  compatibility: string[];
  specs: string[];
  image: string;
  tmdbCollectionId?: number;
};

export const products: Product[] = [
  {
    id: "cyber-finch",
    slug: "cyber-finch",
    name: "Cyber Finch Prime",
    tagline: "Featherweight streamer with heavyweight decoding.",
    description:
      "The Cyber Finch Prime blends low-latency Wi-Fi 6E with a custom neon OS overlay that keeps your stream crisp and responsive.",
    price: "$249",
    compatibility: ["Dolby Vision", "HDR10+", "Matter Ready"],
    specs: ["Amlogic G3 Octa-Core", "32GB UFS Storage", "4GB LPDDR5", "Wi-Fi 6E"],
    image: "/products/cyber-finch.svg",
    tmdbCollectionId: 420818
  },
  {
    id: "prism-dove",
    slug: "prism-dove",
    name: "Prism Dove Studio",
    tagline: "Color graded visuals tuned for cinematographers.",
    description:
      "12-bit pipeline, SDI input, and a pro-grade remote wrapped inside a reflective glass chassis inspired by cathedral windows.",
    price: "$399",
    compatibility: ["ProRes", "DaVinci Sync", "Calibrated"],
    specs: ["Snapdragon X Elite", "64GB NVMe", "8GB LPDDR5X", "Tri-Band Wi-Fi"],
    image: "/products/prism-dove.svg",
    tmdbCollectionId: 9485
  },
  {
    id: "nocturne-owl",
    slug: "nocturne-owl",
    name: "Nocturne Owl Beacon",
    tagline: "The nocturnal powerhouse for midnight binge sessions.",
    description:
      "Anodized obsidian shell with passive cooling fins and a lumen-reactive underglow that adapts to ambient lighting.",
    price: "$329",
    compatibility: ["Dolby Atmos", "VRR", "Cloud DVR"],
    specs: ["Custom Ryzen Edge", "48GB SSD Cache", "6GB LPDDR5", "Bluetooth 5.4"],
    image: "/products/nocturne-owl.svg"
  }
];

export function getProductBySlug(slug: string) {
  return products.find((product) => product.slug === slug);
}
