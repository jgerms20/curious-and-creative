import Link from "next/link";
import { notFound } from "next/navigation";
import { posts } from "@/content/journal/posts";

export function generateStaticParams() {
  return posts.map((p) => ({ slug: p.slug }));
}

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const post = posts.find((p) => p.slug === slug);
  return { title: post ? `${post.title} — Curious & Creative` : "Journal" };
}

export default async function JournalPost({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const post = posts.find((p) => p.slug === slug);
  if (!post) notFound();

  return (
    <article className="max-w-2xl mx-auto px-6 py-20">
      <Link href="/journal" className="text-sm text-ink/60 hover:text-ink">
        ← Back to journal
      </Link>
      <p className="eyebrow text-terracotta mt-10">{post.category}</p>
      <h1 className="font-serif text-4xl md:text-5xl leading-tight mt-4">
        {post.title}
      </h1>
      <p className="mt-4 text-lg text-ink/70 italic">{post.dek}</p>
      <p className="mt-6 text-sm text-ink/60">
        {post.date} · {post.readingTime}
      </p>
      <hr className="border-ink/15 my-10" />
      <div className="space-y-6 text-lg text-ink/85 leading-relaxed font-serif">
        {post.body.map((para, i) => (
          <p key={i}>{para}</p>
        ))}
      </div>
    </article>
  );
}
