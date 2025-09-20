import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { getEpisodeById, episodes } from "@/lib/podcast";
import { PodcastPlayer } from "@/components/PodcastPlayer";
import { PodcastStructuredData } from "@/components/StructuredData";

const siteUrl = "https://mz1312.xx.kg";

interface PodcastPageProps {
  params: { id: string };
}

export function generateStaticParams() {
  return episodes.map((episode) => ({ id: episode.id }));
}

export function generateMetadata({ params }: PodcastPageProps): Metadata {
  const episode = getEpisodeById(params.id);

  if (!episode) {
    return {
      title: "Episode not found"
    };
  }

  const canonical = `${siteUrl}/podcast/${episode.id}`;

  return {
    title: `${episode.title} · Signal Boost Podcast`,
    description: episode.description,
    alternates: { canonical },
    openGraph: {
      type: "article",
      url: canonical,
      title: episode.title,
      description: episode.description
    },
    twitter: {
      card: "summary",
      title: episode.title,
      description: episode.description
    }
  };
}

export default function PodcastPage({ params }: PodcastPageProps) {
  const episode = getEpisodeById(params.id);

  if (!episode) {
    notFound();
  }

  return (
    <div className="mx-auto flex w-full max-w-4xl flex-col gap-8">
      <PodcastStructuredData episode={episode} siteUrl={siteUrl} />
      <header className="glitch-border rounded-3xl bg-crt-glass/70 p-6 text-center">
        <h1 className="font-orbitron text-3xl uppercase tracking-[0.3em] text-cyber-pink">Signal Boost Podcast</h1>
        <p className="mt-2 text-sm text-cyber-teal/70">Episode {episode.id} · Published {episode.publishedAt}</p>
      </header>
      <PodcastPlayer
        title={episode.title}
        description={episode.description}
        duration={episode.duration}
        audioUrl={episode.audioUrl}
      />
    </div>
  );
}
