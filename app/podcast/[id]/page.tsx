import { notFound } from "next/navigation";
import { getEpisodeById } from "@/lib/podcast";
import { PodcastPlayer } from "@/components/PodcastPlayer";

interface PodcastPageProps {
  params: { id: string };
}

export default function PodcastPage({ params }: PodcastPageProps) {
  const episode = getEpisodeById(params.id);

  if (!episode) {
    notFound();
  }

  return (
    <div className="mx-auto flex w-full max-w-4xl flex-col gap-8">
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
