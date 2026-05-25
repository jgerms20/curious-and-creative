import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{ts,tsx,mdx}",
    "./components/**/*.{ts,tsx}",
    "./content/**/*.{ts,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        ivory: "#F7F3EC",
        ink: "#161513",
        terracotta: "#C25A3C",
        sage: "#7E8B7A",
        mustard: "#C8A04A",
        ember: "#7A1F1F",
        glow: "#E2A857",
        cream: "#FAF6EE",
      },
      fontFamily: {
        serif: ['"Fraunces"', "Georgia", "serif"],
        sans: ['"Inter"', "ui-sans-serif", "system-ui", "sans-serif"],
      },
      maxWidth: {
        prose: "68ch",
        column: "42rem",
      },
      letterSpacing: {
        editorial: "0.18em",
      },
    },
  },
  plugins: [],
};

export default config;
