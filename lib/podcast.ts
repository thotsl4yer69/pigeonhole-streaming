export type Episode = {
  id: string;
  title: string;
  description: string;
  duration: string;
  audioUrl: string;
  publishedAt: string;
};

export const episodes: Episode[] = [
  {
    id: "001",
    title: "Signal Boost: The CRT Renaissance",
    description:
      "We dissect the return of CRT aesthetics in modern home theaters and talk about why pigeons keep appearing in Net tech art.",
    duration: "38:21",
    audioUrl: "https://cdn.example.com/audio/signal-boost-001.mp3",
    publishedAt: "2024-04-01"
  },
  {
    id: "002",
    title: "Firmware Glitches & Neon Switches",
    description:
      "A behind-the-scenes chat with the engineers who tuned the Cyber Finch Prime to glide between apps at lightning speed.",
    duration: "42:09",
    audioUrl: "https://cdn.example.com/audio/signal-boost-002.mp3",
    publishedAt: "2024-04-15"
  },
  {
    id: "003",
    title: "Projector Shadows and Prism Doves",
    description:
      "Cinematic color science gets the retro-futuristic treatment as we tour the Prism Dove Studio lab.",
    duration: "47:55",
    audioUrl: "https://cdn.example.com/audio/signal-boost-003.mp3",
    publishedAt: "2024-05-02"
  }
];

export function getEpisodeById(id: string) {
  return episodes.find((episode) => episode.id === id);
}
