export const metadata = { title: "Manifesto — Kindling" };

const principles = [
  {
    title: "Consent is the game, not a disclaimer.",
    body: "Every card can be declined for free, no penalty, no explanation needed. The deck itself reminds players to talk about what they're up for. Consent is the whole point.",
  },
  {
    title: "Pairings, not couples.",
    body: "Kindling works for two people, three people, or a group of friends exploring intimacy together. Our language and mechanics don't assume one shape of love.",
  },
  {
    title: "Queer by default.",
    body: "No card assumes gender, anatomy, or relationship structure. Inclusivity isn't a special pack — it's the base layer.",
  },
  {
    title: "Intimacy isn't only sex.",
    body: "Half the base deck is non-physical. A bathtub and a book is a card. A glass of water handed across the room is a card.",
  },
  {
    title: "Cooperative reward, not competition.",
    body: "The 'winner' picks a shared reward both players already wanted. Scoring is in service of the pairing — not in service of beating each other.",
  },
  {
    title: "A beautiful object.",
    body: "Kindling should look like something you leave on the coffee table — not something you hide in a drawer.",
  },
];

export default function Manifesto() {
  return (
    <article className="max-w-2xl mx-auto px-6 py-24">
      <p className="eyebrow text-glow/70">The Manifesto</p>
      <h1 className="font-serif text-5xl md:text-6xl leading-tight mt-4">
        Six things we promise.
      </h1>
      <p className="mt-8 text-lg text-[#f4e6d3]/80 leading-relaxed">
        Kindling is built around six principles. Every card, every pack,
        every word of the rules booklet is checked against them. If a card
        doesn't meet all six, it doesn't ship.
      </p>

      <div className="mt-16 space-y-12">
        {principles.map((p, i) => (
          <div key={p.title} className="border-t border-glow/30 pt-6">
            <p className="eyebrow text-glow/70">No. {i + 1}</p>
            <h2 className="font-serif text-3xl mt-3 text-glow">{p.title}</h2>
            <p className="mt-4 text-lg text-[#f4e6d3]/80 leading-relaxed">{p.body}</p>
          </div>
        ))}
      </div>
    </article>
  );
}
