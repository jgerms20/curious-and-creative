export const metadata = { title: "Pre-order — Kindling" };

export default function Order() {
  return (
    <div className="max-w-3xl mx-auto px-6 py-20">
      <p className="eyebrow text-glow/70">Pre-order</p>
      <h1 className="font-serif text-5xl md:text-6xl leading-tight mt-4">
        First run is small.
      </h1>
      <p className="mt-8 text-lg text-[#f4e6d3]/85 leading-relaxed max-w-2xl">
        Kindling's first manufacturing run is 1,000 base decks and 500 of
        each add-on. Join the waitlist and you'll be first to know when
        pre-orders open — plus you'll get a hand-numbered consent &amp;
        care card in your box.
      </p>

      <form
        action="https://formspree.io/f/placeholder"
        method="POST"
        className="mt-12 border-t border-glow/30 pt-10 max-w-lg"
      >
        <label htmlFor="email" className="block text-sm text-[#f4e6d3]/80">
          Email address
        </label>
        <input
          id="email"
          name="email"
          type="email"
          required
          placeholder="you@somewhere.com"
          className="mt-2 w-full bg-transparent border border-glow/40 rounded-sm px-4 py-3 text-[#f4e6d3] placeholder:text-[#f4e6d3]/40 focus:outline-none focus:border-glow"
        />

        <fieldset className="mt-8">
          <legend className="text-sm text-[#f4e6d3]/80">
            Which packs are you most curious about?
          </legend>
          <div className="mt-4 grid grid-cols-2 gap-3 text-sm">
            {["Embers (base)", "Challenges", "Activities", "Kink"].map((p) => (
              <label key={p} className="flex items-center gap-2">
                <input type="checkbox" name="packs" value={p} className="accent-glow" />
                {p}
              </label>
            ))}
          </div>
        </fieldset>

        <label htmlFor="pairing" className="block text-sm text-[#f4e6d3]/80 mt-8">
          How would you describe your pairing? (Optional — helps us write better cards.)
        </label>
        <input
          id="pairing"
          name="pairing"
          type="text"
          placeholder="e.g. queer couple, throuple, friends exploring"
          className="mt-2 w-full bg-transparent border border-glow/40 rounded-sm px-4 py-3 text-[#f4e6d3] placeholder:text-[#f4e6d3]/40 focus:outline-none focus:border-glow"
        />

        <button
          type="submit"
          className="mt-10 bg-glow text-[#1b1110] px-6 py-3 font-medium hover:bg-glow/90 transition-colors w-full md:w-auto"
        >
          Add me to the waitlist
        </button>
        <p className="mt-4 text-xs text-[#f4e6d3]/60">
          We will never sell your email. We send roughly one note a month.
        </p>
      </form>
    </div>
  );
}
