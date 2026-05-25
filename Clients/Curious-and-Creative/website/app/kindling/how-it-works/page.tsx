import { modes, categoryMultiplier } from "@/lib/kindling-scoring";

export const metadata = { title: "How it works — Kindling" };

const steps = [
  {
    n: "01",
    title: "Pick your decks.",
    body: "Start with Embers. Shuffle in any add-on packs you want — Challenges, Activities, Kink. You can keep them separate or mix them; both work.",
  },
  {
    n: "02",
    title: "Read the Consent & Care card.",
    body: "Out loud, together, every time. Yes, even if you've played before. Agree on a safeword and confirm anyone can pass on any card without explanation.",
  },
  {
    n: "03",
    title: "Choose a stake mode.",
    body: "No Stakes is the default. Stoke Pot adds an optional money ante that funds a shared reward. Trade Mode lets players cash Sparks in for favors.",
  },
  {
    n: "04",
    title: "Write your Reward Cards.",
    body: "Each player writes 3 things you'd genuinely love to receive — a date, a meal, an experience. Set them aside. These are the prize the game points toward.",
  },
  {
    n: "05",
    title: "Play.",
    body: "On your turn, draw a card. Read it aloud. Accept or pass. If you accept and complete the prompt, you earn Sparks. Pass play.",
  },
  {
    n: "06",
    title: "End the session.",
    body: "Three ways to end: by pre-agreed card count, by timer, or anyone calls 'ember out.' The highest Sparks chooses a reward — to receive, to give, or to fund.",
  },
];

export default function HowItWorks() {
  return (
    <div className="max-w-5xl mx-auto px-6 py-20">
      <p className="eyebrow text-glow/70">How it works</p>
      <h1 className="font-serif text-5xl md:text-6xl leading-tight mt-4">
        Six steps. Two minutes to learn.
      </h1>
      <p className="mt-6 text-lg text-[#f4e6d3]/80 max-w-2xl">
        Kindling's rules are short enough to read aloud before you start.
        Here is the whole game.
      </p>

      <div className="mt-20 grid md:grid-cols-2 gap-x-12 gap-y-14">
        {steps.map((s) => (
          <div key={s.n}>
            <p className="font-serif text-glow text-4xl">{s.n}</p>
            <h2 className="font-serif text-2xl mt-3">{s.title}</h2>
            <p className="mt-3 text-[#f4e6d3]/80 leading-relaxed">{s.body}</p>
          </div>
        ))}
      </div>

      <hr className="border-glow/20 my-20" />

      <section>
        <p className="eyebrow text-glow/70">The Stoke Pot — scoring</p>
        <h2 className="font-serif text-3xl md:text-4xl mt-3 max-w-2xl">
          Sparks earned = intensity × category multiplier.
        </h2>
        <div className="mt-10 grid sm:grid-cols-2 md:grid-cols-3 gap-4 max-w-3xl">
          {Object.entries(categoryMultiplier).map(([cat, mult]) => (
            <div key={cat} className="border-t border-glow/30 pt-3 flex justify-between">
              <span>{cat}</span>
              <span className="text-glow">× {mult}</span>
            </div>
          ))}
        </div>
        <p className="mt-8 text-[#f4e6d3]/75 max-w-2xl leading-relaxed">
          A Match card doubles the Sparks for any player who accepted.
          Kink-pack cards earn an additional +5 Sparks for the player who
          performs the printed aftercare prompt.
        </p>
      </section>

      <hr className="border-glow/20 my-20" />

      <section>
        <p className="eyebrow text-glow/70">Three ways to play</p>
        <div className="mt-8 grid md:grid-cols-3 gap-8">
          {modes.map((m) => (
            <div key={m.name} className="border-t border-glow/30 pt-5">
              <h3 className="font-serif text-2xl text-glow">{m.name}</h3>
              <p className="mt-3 text-[#f4e6d3]/80 leading-relaxed">{m.blurb}</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
