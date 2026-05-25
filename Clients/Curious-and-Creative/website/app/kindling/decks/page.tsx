import { sampleCards } from "@/content/kindling/sample-cards";

export const metadata = { title: "Decks — Kindling" };

const decks = [
  {
    name: "Embers",
    sub: "The base deck",
    count: "~150 cards",
    price: "$39",
    blurb:
      "The everyday deck. Conversation, vulnerability, small intimate acts. Safe for almost any pairing — and the only pack you need to start.",
  },
  {
    name: "Challenges Pack",
    sub: "Add-on",
    count: "~60 cards",
    price: "$24",
    blurb:
      "Bigger, one-time experiences — designed to be drawn occasionally. A class to take together. A day to spend without phones. A favor you'll remember years from now.",
  },
  {
    name: "Activities Pack",
    sub: "Add-on",
    count: "~60 cards",
    price: "$24",
    blurb:
      "Slower, more ritual. Date-shaped prompts that turn an evening into a thing you did, not a thing you scrolled through.",
  },
  {
    name: "Kink Pack",
    sub: "Add-on · 18+",
    count: "~60 cards",
    price: "$28",
    blurb:
      "Explore kink and role-play with consent and aftercare built into every card. Designed for couples and for group play, with a one-page Consent & Care insert in the box.",
  },
];

export default function Decks() {
  return (
    <div className="max-w-6xl mx-auto px-6 py-20">
      <p className="eyebrow text-glow/70">The Decks</p>
      <h1 className="font-serif text-5xl md:text-6xl leading-tight mt-4">
        Modular by design.
      </h1>
      <p className="mt-6 text-lg text-[#f4e6d3]/80 max-w-2xl">
        Start with the base deck. Add packs as your pairing wants more
        heat, more ritual, or more risk. Shuffle them together or keep them
        separate — both work.
      </p>

      <div className="mt-20 space-y-16">
        {decks.map((d) => {
          const sample = sampleCards.find((c) => c.deck.toLowerCase() === d.name.split(" ")[0].toLowerCase());
          return (
            <div key={d.name} className="grid md:grid-cols-12 gap-10 border-t border-glow/30 pt-10">
              <div className="md:col-span-7">
                <p className="eyebrow text-glow/70">{d.sub}</p>
                <h2 className="font-serif text-4xl md:text-5xl mt-3 text-glow">
                  {d.name}
                </h2>
                <p className="mt-6 text-lg text-[#f4e6d3]/80 leading-relaxed max-w-xl">
                  {d.blurb}
                </p>
                <p className="mt-6 text-sm text-[#f4e6d3]/60">
                  {d.count} · {d.price}
                </p>
              </div>
              {sample && (
                <div className="md:col-span-5">
                  <div className="bg-[#f4e6d3] text-[#1b1110] rounded-sm p-6 aspect-[3/4] flex flex-col justify-between shadow-lg max-w-xs ml-auto">
                    <div>
                      <div className="flex justify-between items-start">
                        <span className="eyebrow text-ember">{sample.category}</span>
                        <span className="text-ember tracking-widest">
                          {"·".repeat(sample.intensity)}
                        </span>
                      </div>
                      <p className="font-serif text-xl mt-8 leading-snug">
                        "{sample.prompt}"
                      </p>
                    </div>
                    <p className="text-xs text-ink/60 mt-6">Sample card</p>
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
