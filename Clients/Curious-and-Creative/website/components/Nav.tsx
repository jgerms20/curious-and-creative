import Link from "next/link";

const links = [
  { href: "/projects", label: "Projects" },
  { href: "/journal", label: "Journal" },
  { href: "/podcast", label: "Podcast" },
  { href: "/kindling", label: "Kindling" },
  { href: "/about", label: "About" },
  { href: "/contact", label: "Contact" },
];

export default function Nav() {
  return (
    <header className="border-b border-ink/15">
      <div className="max-w-6xl mx-auto px-6 py-6 flex items-center justify-between">
        <Link href="/" className="font-serif text-2xl tracking-tight">
          Curious <span className="text-terracotta">&amp;</span> Creative
        </Link>
        <nav className="hidden md:flex items-center gap-7 text-sm">
          {links.map((l) => (
            <Link
              key={l.href}
              href={l.href}
              className="hover:text-terracotta transition-colors"
            >
              {l.label}
            </Link>
          ))}
        </nav>
        <Link
          href="/kindling/order"
          className="md:hidden text-sm underline"
        >
          Kindling
        </Link>
      </div>
    </header>
  );
}
