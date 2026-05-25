export const metadata = { title: "About — Curious & Creative" };

export default function About() {
  return (
    <article className="max-w-2xl mx-auto px-6 py-20">
      <p className="eyebrow text-ink/60">About</p>
      <h1 className="font-serif text-5xl md:text-6xl leading-tight mt-4">
        Two people, one studio.
      </h1>
      <div className="mt-10 space-y-6 text-lg text-ink/80 leading-relaxed">
        <p>
          Curious &amp; Creative is the holding company for the projects
          Jay and Janelle make together. It's not an agency. It's not a
          service business. It's a small studio for our curious creative
          life — and a place to put the things we build into the world.
        </p>
        <p>
          <strong>Curiosity is a practice, not a personality trait.</strong>{" "}
          It can be trained, and it gets sharper when shared with someone
          you love. Creativity belongs to everyone — we don't want to
          gatekeep it behind industries or job titles. Intimacy is the
          same skill as creativity: paying close attention, taking small
          risks, making room for surprise.
        </p>
        <p>
          Play is serious work. The best things we make are the ones that
          felt like games while we were making them.
        </p>
      </div>

      <h2 className="font-serif text-3xl mt-16">What lives here</h2>
      <ul className="mt-6 space-y-3 text-ink/80">
        <li><strong>Kindling.</strong> A modular card game for pairings.</li>
        <li><strong>The Podcast.</strong> Long-form conversations on living a curious life.</li>
        <li><strong>The Journal.</strong> Short essays and notes from the studio.</li>
        <li>Future projects — books, more games, events, whatever we get curious about next.</li>
      </ul>

      <h2 className="font-serif text-3xl mt-16">What we're not</h2>
      <p className="mt-6 text-ink/80 leading-relaxed">
        We're not building an agency, we're not taking client work, and
        we're not trying to scale into a media company. We are two people
        making things we believe in, together, with the door open for
        collaborators we love.
      </p>
    </article>
  );
}
