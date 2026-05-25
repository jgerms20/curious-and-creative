import Link from "next/link";

const projects = [
  {
    href: "/kindling",
    eyebrow: "A card game",
    title: "Kindling",
    blurb:
      "A modular card game for rekindling and deepening connection. Consent-first, queer by default, designed to be played.",
  },
  {
    href: "/podcast",
    eyebrow: "Audio",
    title: "The Podcast",
    blurb:
      "Long-form conversations on living a curious life — with the people we love and the people we love listening to.",
  },
  {
    href: "/journal",
    eyebrow: "Writing",
    title: "The Journal",
    blurb:
      "Essays, notes, and dispatches from the studio. What we're reading, what we're making, what we got wrong this week.",
  },
];

export default function Home() {
  return (
    <div>
      <section className="max-w-6xl mx-auto px-6 pt-20 pb-24 md:pt-32 md:pb-40">
        <p className="eyebrow text-ink/60 mb-6">Curious &amp; Creative LLC</p>
        <h1 className="font-serif text-5xl md:text-7xl leading-[1.02] tracking-tight max-w-4xl">
          A small studio for our curious{" "}
          <span className="italic text-terracotta">creative life</span>.
        </h1>
        <p className="mt-8 text-lg md:text-xl text-ink/75 max-w-2xl leading-relaxed">
          We are Jay and Janelle. This is the home for the things we make
          together — a podcast, a card game, a journal, and whatever we
          get curious about next.
        </p>
        <div className="mt-10 flex gap-6 text-sm">
          <Link
            href="/projects"
            className="underline decoration-terracotta decoration-2 underline-offset-4 hover:text-terracotta"
          >
            See the projects
          </Link>
          <Link href="/about" className="text-ink/70 hover:text-ink">
            About the studio →
          </Link>
        </div>
      </section>

      <section className="border-t border-ink/15 bg-cream/40">
        <div className="max-w-6xl mx-auto px-6 py-20">
          <div className="flex items-baseline justify-between mb-12">
            <h2 className="font-serif text-3xl md:text-4xl">What lives here</h2>
            <Link href="/projects" className="text-sm underline">
              All projects
            </Link>
          </div>
          <div className="grid md:grid-cols-3 gap-10">
            {projects.map((p) => (
              <Link
                href={p.href}
                key={p.href}
                className="group block border-t border-ink/20 pt-6 hover:border-terracotta transition-colors"
              >
                <p className="eyebrow text-ink/60">{p.eyebrow}</p>
                <h3 className="font-serif text-2xl mt-3 group-hover:text-terracotta transition-colors">
                  {p.title}
                </h3>
                <p className="mt-3 text-ink/70 leading-relaxed">{p.blurb}</p>
                <p className="mt-5 text-sm underline decoration-1 underline-offset-4">
                  Read more
                </p>
              </Link>
            ))}
          </div>
        </div>
      </section>

      <section className="max-w-4xl mx-auto px-6 py-24">
        <p className="eyebrow text-ink/60">A note from us</p>
        <p className="mt-6 font-serif text-2xl md:text-3xl leading-snug">
          We don't want to be an agency. We want to be a studio — small,
          stubborn, and devoted to the work we'd make whether or not
          anyone was watching. Curious &amp; Creative is the holding
          company for that work.
        </p>
        <p className="mt-8 text-ink/70 leading-relaxed">
          Everything we publish lives here: the podcast, the card game,
          the essays. We will add more projects as we get curious about
          them, and we will retire the ones that stop being interesting.
          We promise no roadmap and no growth-hacking.
        </p>
        <p className="mt-8 italic font-serif text-ink/70">— Jay &amp; Janelle</p>
      </section>
    </div>
  );
}
