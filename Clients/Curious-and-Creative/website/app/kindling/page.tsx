import Link from "next/link";
import { sampleCards } from "@/content/kindling/sample-cards";

export const metadata = { title: "Kindling — a card game for pairings" };

export default function KindlingHome() {
  const featured = sampleCards.slice(0, 6);
  return (
    <div>
      <section className="max-w-6xl mx-auto px-6 pt-24 pb-32">
        <p className="eyebrow text-glow/80">A card game · launching this year</p>
        <h1 className="font-serif text-5xl md:text-7xl leading-[1.02] tracking-tight mt-6 max-w-4xl">
          A card game for{" "}
          <span className="italic text-glow">pairings</span> who want to know
          each other more closely.
        </h1>
        <p className="mt-8 text-lg md:text-xl text-[#f4e6d3]/80 max-w-2xl leading-relaxed">
          Kindling is conversation, vulnerability, shared experience, and
          consent-forward intimacy in one modular deck system. Built for
          couples, throuples, and anyone exploring connection — queer by
          default, designed to be played, not displayed.
        </p>
        <div className="mt-10 flex flex-wrap gap-6 text-sm">
          <Link
            href="/kindling/order"
            className="bg-glow text-[#1b1110] px-6 py-3 font-medium hover:bg-glow/90 transition-colors"
          >
            Join the waitlist
          </Link>
          <Link href="/kindling/how-it-works" className="underline underline-offset-4 hover:text-glow">
            How the game works →
          </Link>
        </div>
      </section>

      <section className="border-y border-glow/15 bg-[#231614]">
        <div className="max-w-6xl mx-auto px-6 py-20">
          <p className="eyebrow text-glow/70">A few cards from the deck</p>
          <h2 className="font-serif text-3xl md:text-4xl mt-3">
            Some are quiet. Some are not.
          </h2>
          <div className="grid md:grid-cols-3 gap-6 mt-12">
            {featured.map((c, i) => (
              <div
                key={i}
                className="bg-[#f4e6d3] text-[#1b1110] rounded-sm p-6 aspect-[3/4] flex flex-col justify-between shadow-lg"
              >
                <div>
                  <div className="flex justify-between items-start">
                    <span className="eyebrow text-ember">{c.category}</span>
                    <span className="text-ember tracking-widest">
                      {"·".repeat(c.intensity)}
                    </span>
                  </div>
                  <p className="font-serif text-xl mt-8 leading-snug">
                    "{c.prompt}"
                  </p>
                </div>
                <div className="flex justify-between text-xs text-ink/60 mt-6">
                  <span>{c.time}</span>
                  <span>{c.deck} deck</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="max-w-4xl mx-auto px-6 py-24">
        <p className="eyebrow text-glow/70">Why we made it</p>
        <p className="mt-6 font-serif text-2xl md:text-3xl leading-snug">
          The intimacy-deck shelf is mostly talk. The other shelf is mostly
          gimmick. We wanted a deck that lives between — vulnerable enough
          for a long Sunday on the couch, daring enough for a Saturday
          you'll remember in five years.
        </p>
        <p className="mt-6 text-[#f4e6d3]/75 leading-relaxed">
          Kindling is built consent-first and queer by default. Every card
          can be declined for free, no penalty, no eyebrow. The scoring
          system is cooperative — the "winner" doesn't take from their
          partner, they give a gift the partner already wanted.
        </p>
        <div className="mt-10">
          <Link href="/kindling/manifesto" className="underline underline-offset-4 hover:text-glow">
            Read the manifesto →
          </Link>
        </div>
      </section>

      <section className="border-t border-glow/15 bg-[#231614]">
        <div className="max-w-6xl mx-auto px-6 py-20 grid md:grid-cols-3 gap-10">
          {[
            {
              title: "Base deck — Embers",
              blurb:
                "~150 cards. Conversation, vulnerability, and small intimate acts. Safe for almost any pairing.",
              price: "$39",
            },
            {
              title: "Challenges Pack",
              blurb:
                "~60 cards. Bigger one-time experiences. Naked Twister, role-reversal day, a class to take together.",
              price: "$24",
            },
            {
              title: "Activities Pack",
              blurb:
                "~60 cards. Slow, ritual prompts. Bathe them. Read to them. Cook in your underwear.",
              price: "$24",
            },
            {
              title: "Kink Pack (18+)",
              blurb:
                "~60 cards. Explore kink and role-play with consent and aftercare built into every card.",
              price: "$28",
            },
            {
              title: "Future packs",
              blurb:
                "Queer & Found · Long Distance · Brand New · Long Haul · Platonic. Coming after launch.",
              price: "",
            },
            {
              title: "The Pairing Bundle",
              blurb:
                "All four launch packs, plus a hand-numbered consent & care card. Free shipping.",
              price: "$99",
            },
          ].map((d) => (
            <div key={d.title} className="border-t border-glow/30 pt-5">
              <div className="flex items-baseline justify-between">
                <h3 className="font-serif text-2xl">{d.title}</h3>
                <span className="text-glow text-sm">{d.price}</span>
              </div>
              <p className="mt-3 text-[#f4e6d3]/75">{d.blurb}</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
