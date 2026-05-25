export type Category =
  | "Ask"
  | "Tell"
  | "Notice"
  | "Tend"
  | "Touch"
  | "Play"
  | "Challenge"
  | "Activity"
  | "Kink";

export const categoryMultiplier: Record<Category, number> = {
  Ask: 1,
  Tell: 1,
  Notice: 1.5,
  Tend: 1.5,
  Touch: 2,
  Play: 2,
  Challenge: 3,
  Activity: 3,
  Kink: 3,
};

export function sparksFor(category: Category, intensity: number, isMatch = false) {
  const base = categoryMultiplier[category] * intensity;
  return isMatch ? base * 2 : base;
}

export const modes = [
  {
    name: "No Stakes",
    blurb:
      "Just play. The player with the most Sparks chooses one of their partner's pre-written Reward Cards to receive — and the partner has the joy of giving it.",
  },
  {
    name: "Stoke Pot",
    blurb:
      "Each player antes the same small amount ($20–$100). At the end, the highest Sparks gets to pick a shared reward to fund from the pot — a date, an experience, a meal.",
  },
  {
    name: "Trade Mode",
    blurb:
      "Mid-session, players can cash in Sparks for favors written by their partner before the game. Prices are set on each Reward Card.",
  },
];
