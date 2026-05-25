import Link from "next/link";
import { posts } from "@/content/journal/posts";

export const metadata = { title: "Journal — Curious & Creative" };

export default function Journal() {
  const [lead, ...rest] = posts;
  return (
    <div className="max-w-6xl mx-auto px-6 py-20">
      <p className="eyebrow text-ink/60">The Journal</p>
      <h1 className="font-serif text-5xl md:text-6xl leading-tight mt-4 max-w-3xl">
        Essays and dispatches from the studio.
      </h1>

      <Link
        href={`/journal/${lead.slug}`}
        className="group block mt-16 border-t border-ink/20 pt-10 hover:border-terracotta transition-colors"
      >
        <div className="grid md:grid-cols-12 gap-10 items-start">
          <div className="md:col-span-7">
            <p className="eyebrow text-terracotta">{lead.category}</p>
            <h2 className="font-serif text-4xl md:text-5xl leading-tight mt-4 group-hover:text-terracotta transition-colors">
              {lead.title}
            </h2>
            <p className="mt-4 text-lg text-ink/75 max-w-xl">{lead.dek}</p>
            <p className="mt-6 text-sm text-ink/60">
              {lead.date} · {lead.readingTime}
            </p>
          </div>
          <div className="md:col-span-5 hidden md:block">
            <div className="aspect-[4/5] bg-cream border border-ink/15 flex items-center justify-center">
              <span className="font-serif text-terracotta text-7xl italic">
                C&amp;C
              </span>
            </div>
          </div>
        </div>
      </Link>

      <div className="mt-20 grid md:grid-cols-2 gap-12">
        {rest.map((p) => (
          <Link
            key={p.slug}
            href={`/journal/${p.slug}`}
            className="group block border-t border-ink/20 pt-6 hover:border-terracotta transition-colors"
          >
            <p className="eyebrow text-ink/60">{p.category}</p>
            <h3 className="font-serif text-2xl md:text-3xl mt-3 group-hover:text-terracotta transition-colors">
              {p.title}
            </h3>
            <p className="mt-3 text-ink/75">{p.dek}</p>
            <p className="mt-4 text-sm text-ink/60">
              {p.date} · {p.readingTime}
            </p>
          </Link>
        ))}
      </div>
    </div>
  );
}
