export type JournalPost = {
  slug: string;
  title: string;
  dek: string;
  date: string;
  readingTime: string;
  category: string;
  body: string[];
};

export const posts: JournalPost[] = [
  {
    slug: "why-we-stopped-calling-ourselves-an-agency",
    title: "Why we stopped calling ourselves an agency.",
    dek: "We named the company before we knew what it was. Here is what it actually is.",
    date: "May 2026",
    readingTime: "5 min read",
    category: "Notes from the studio",
    body: [
      "When we filed the LLC, we called it Curious & Creative Agency because the word 'agency' felt like a permission slip. It said: you can charge for this, you can put it on a business card, you can let strangers take you seriously.",
      "Two years in, the word has started to lie. We don't take client work. We don't pitch. We don't have a service offering or a deck. What we have is a podcast we record on the kitchen table, a card game we are quietly manufacturing, a journal full of half-finished essays, and a long list of things we want to make next.",
      "That isn't an agency. That's a studio. So we dropped the word.",
      "It is a small change and an important one. 'Agency' implies you work in service of someone else's brief. 'Studio' implies the work is the brief. The work is what we are accountable to, not a client. We like the second one better.",
    ],
  },
  {
    slug: "the-case-for-cooperative-scoring",
    title: "The case for cooperative scoring.",
    dek: "Why the most interesting card game we could build is one where nobody really wins.",
    date: "April 2026",
    readingTime: "7 min read",
    category: "Kindling",
    body: [
      "Most party games are competitive by reflex. Someone scores more points, someone else scores fewer, and the design problem is how to keep the loser engaged long enough to play another round.",
      "When we started prototyping Kindling, we kept hitting the same wall: a competitive scoring system in an intimacy game produces the wrong outcomes. The most 'winning' move becomes the most performative move. The card you most need to draw is the one your point total tells you to skip.",
      "So we flipped it. The 'winner' of a Kindling session doesn't get the pot. They get to give a gift, from a list of gifts their partner already wanted. The reward goes to the relationship, not the player.",
      "It is, in card-game terms, a small adjustment. In terms of how a couple plays for an hour on a Tuesday night, it changes the entire feel of the room.",
    ],
  },
];
