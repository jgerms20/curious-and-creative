import Link from "next/link";

const subNav = [
  { href: "/kindling", label: "Overview" },
  { href: "/kindling/decks", label: "Decks" },
  { href: "/kindling/how-it-works", label: "How it works" },
  { href: "/kindling/manifesto", label: "Manifesto" },
  { href: "/kindling/order", label: "Pre-order" },
];

export default function KindlingLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="bg-[#1b1110] text-[#f4e6d3] min-h-screen">
      <div className="border-b border-glow/20">
        <div className="max-w-6xl mx-auto px-6 py-5 flex items-center justify-between gap-8">
          <Link href="/kindling" className="font-serif text-2xl tracking-tight text-glow">
            Kindling
          </Link>
          <nav className="hidden md:flex items-center gap-7 text-sm">
            {subNav.map((l) => (
              <Link key={l.href} href={l.href} className="hover:text-glow transition-colors">
                {l.label}
              </Link>
            ))}
          </nav>
          <Link href="/" className="text-xs text-glow/70 hover:text-glow">
            ← Curious &amp; Creative
          </Link>
        </div>
      </div>
      {children}
    </div>
  );
}
