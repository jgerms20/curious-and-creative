export const metadata = { title: "Contact — Curious & Creative" };

export default function Contact() {
  return (
    <article className="max-w-xl mx-auto px-6 py-20">
      <p className="eyebrow text-ink/60">Contact</p>
      <h1 className="font-serif text-5xl leading-tight mt-4">Say hi.</h1>
      <p className="mt-8 text-lg text-ink/80 leading-relaxed">
        We're slow with email but we read everything. If you'd like to
        collaborate on a project, recommend Kindling to your clients, book
        us on a podcast, or just send a kind word — please write.
      </p>
      <ul className="mt-10 space-y-3 text-lg">
        <li>
          <span className="text-ink/60">Studio:</span>{" "}
          <a href="mailto:hello@curiousandcreative.com" className="underline">
            hello@curiousandcreative.com
          </a>
        </li>
        <li>
          <span className="text-ink/60">Press / podcasts:</span>{" "}
          <a href="mailto:press@curiousandcreative.com" className="underline">
            press@curiousandcreative.com
          </a>
        </li>
        <li>
          <span className="text-ink/60">Kindling wholesale:</span>{" "}
          <a href="mailto:wholesale@curiousandcreative.com" className="underline">
            wholesale@curiousandcreative.com
          </a>
        </li>
      </ul>
    </article>
  );
}
