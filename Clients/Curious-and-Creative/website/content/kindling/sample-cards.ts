import type { Category } from "@/lib/kindling-scoring";

export type SampleCard = {
  category: Category;
  intensity: 1 | 2 | 3 | 4 | 5;
  prompt: string;
  time: string;
  deck: "Embers" | "Challenges" | "Activities" | "Kink";
};

export const sampleCards: SampleCard[] = [
  { deck: "Embers", category: "Ask", intensity: 1, time: "2 min", prompt: "What was the last thing you did just because you were curious?" },
  { deck: "Embers", category: "Notice", intensity: 2, time: "2 min", prompt: "Stare into each other's eyes for two full minutes. No talking, no laughing." },
  { deck: "Embers", category: "Touch", intensity: 3, time: "2 min", prompt: "Trace the inside of their forearm with one finger for two minutes." },
  { deck: "Embers", category: "Tend", intensity: 1, time: "1 min", prompt: "Pour them a glass of water and hand it to them without speaking." },
  { deck: "Embers", category: "Ask", intensity: 5, time: "10 min", prompt: "If we had a year left together, what would you want to do differently starting tomorrow?" },
  { deck: "Embers", category: "Play", intensity: 2, time: "5 min", prompt: "Make up a 30-second song about how you met. Sing it." },
  { deck: "Challenges", category: "Challenge", intensity: 5, time: "This month", prompt: "Take a pole or stripper-style class together this month. Perform what you learned for each other." },
  { deck: "Challenges", category: "Challenge", intensity: 4, time: "One day", prompt: "Reverse roles for a full day. Chores, errands, tone, all of it." },
  { deck: "Activities", category: "Activity", intensity: 3, time: "1 hour", prompt: "Read aloud to them while they take a bath. Their pick of book." },
  { deck: "Activities", category: "Activity", intensity: 4, time: "1 hour", prompt: "Bathe them. Wash their hair. No phones in the room." },
  { deck: "Kink", category: "Kink", intensity: 4, time: "30 min", prompt: "Blindfold them, then offer three tastes (food, drink, scent). They guess each. Aftercare: hold them and tell them what surprised you about their reactions." },
  { deck: "Kink", category: "Kink", intensity: 5, time: "1 hour", prompt: "Trade a 'service' hour — one of you takes care of the other completely, the other only receives. Aftercare prompt on the card back." },
];
