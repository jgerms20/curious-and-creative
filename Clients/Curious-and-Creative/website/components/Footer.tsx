import Link from "next/link";

export default function Footer() {
  return (
    <footer className="mt-32 border-t border-ink/15">
      <div className="max-w-6xl mx-auto px-6 py-12 grid grid-cols-1 md:grid-cols-3 gap-10 text-sm">
        <div>
          <p className="font-serif text-xl">Curious &amp; Creative</p>
          <p className="text-ink/70 mt-2 max-w-xs">
            A small studio for our curious creative life. Made in our
            apartment, by Jay and Janelle.
          </p>
        </div>
        <div>
          <p className="eyebrow text-ink/60">Projects</p>
          <ul className="mt-3 space-y-1">
            <li><Link href="/podcast">The Podcast</Link></li>
            <li><Link href="/kindling">Kindling</Link></li>
            <li><Link href="/journal">Journal</Link></li>
          </ul>
        </div>
        <div>
          <p className="eyebrow text-ink/60">Studio</p>
          <ul className="mt-3 space-y-1">
            <li><Link href="/about">About</Link></li>
            <li><Link href="/contact">Contact</Link></li>
          </ul>
          <p className="text-ink/60 mt-6 text-xs">
            © {new Date().getFullYear()} Curious &amp; Creative LLC.
          </p>
        </div>
      </div>
    </footer>
  );
}
