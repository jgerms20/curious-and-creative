import Link from "next/link";

export const metadata = { title: "Projects — Curious & Creative" };

const projects = [
  {
    href: "/kindling",
    eyebrow: "Card game · launching this year",
    title: "Kindling",
    blurb:
      "A modular card game for pairings. Conversation, vulnerability, shared experience, and consent-forward intimacy. Designed to be played, not displayed.",
    status: "In development",
  },
  {
    href: "/podcast",
    eyebrow: "Audio · ongoing",
    title: "The Podcast",
    blurb:
      "Conversations on living a curious creative life. Long-form, slow, warm. New episodes monthly.",
    status: "Recording",
  },
  {
    href: "/journal",
    eyebrow: "Writing · ongoing",
    title: "The Journal",
    blurb:
      "Essays and notes from the studio. What we're reading, what we're making, what we got wrong this week.",
    status: "Publishing weekly",
  },
];

export default function Projects() {
  return (
    <div className="max-w-5xl mx-auto px-6 py-20">
      <p className="eyebrow text-ink/60">Projects</p>
      <h1 className="font-serif text-5xl md:text-6xl leading-tight mt-4">
        Everything we make.
      </h1>
      <p className="mt-6 text-lg text-ink/75 max-w-2xl">
        Each of these lives under the Curious &amp; Creative roof.
        We add projects as we get curious about them, and retire the
        ones that stop being interesting.
      </p>

      <div className="mt-16 space-y-16">
        {projects.map((p) => (
          <Link
            key={p.href}
            href={p.href}
            className="block group border-t border-ink/20 pt-8 hover:border-terracotta transition-colors"
          >
            <div className="flex items-baseline justify-between gap-6">
              <p className="eyebrow text-ink/60">{p.eyebrow}</p>
              <p className="eyebrow text-terracotta">{p.status}</p>
            </div>
            <h2 className="font-serif text-4xl md:text-5xl mt-4 group-hover:text-terracotta transition-colors">
              {p.title}
            </h2>
            <p className="mt-4 text-lg text-ink/75 max-w-2xl">{p.blurb}</p>
            <p className="mt-6 text-sm underline underline-offset-4">
              Read more →
            </p>
          </Link>
        ))}
      </div>
    </div>
  );
}
