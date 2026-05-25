export const metadata = { title: "Podcast — Curious & Creative" };

export default function Podcast() {
  return (
    <article className="max-w-2xl mx-auto px-6 py-20">
      <p className="eyebrow text-ink/60">Podcast</p>
      <h1 className="font-serif text-5xl md:text-6xl leading-tight mt-4">
        Long conversations, slow and warm.
      </h1>
      <p className="mt-8 text-lg text-ink/80 leading-relaxed">
        Our podcast is a place to talk to people we admire about how they
        live a curious creative life. Artists, writers, therapists,
        builders, partners. Sometimes it's just the two of us trying to
        figure something out.
      </p>
      <p className="mt-4 text-lg text-ink/80 leading-relaxed">
        New episodes drop monthly. Show notes and full transcripts live
        here when the first season is out.
      </p>

      <div className="mt-12 border-t border-ink/20 pt-8">
        <p className="eyebrow text-ink/60">Coming soon</p>
        <p className="font-serif text-2xl mt-3">
          Season one is in production. Subscribe to the journal to know
          when episode one drops.
        </p>
      </div>
    </article>
  );
}
