#!/usr/bin/env node
/* Render Kindling print files from site/kindling/deck.html (print mode).
 *
 *   node scripts/kindling_print.mjs            # PDFs + overflow check
 *   node scripts/kindling_print.mjs --check    # overflow check only
 *   node scripts/kindling_print.mjs --png      # also export 300 dpi PNGs per card (for MakePlayingCards etc.)
 *
 * Needs Playwright + Chromium (npx playwright install chromium, or set PLAYWRIGHT_PATH).
 * Writes to Production/Kindling/print/. Run scripts/build_kindling.py first if cards changed. */
import http from "node:http";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
const pw = require(process.env.PLAYWRIGHT_PATH || (fs.existsSync("/opt/node22/lib/node_modules/playwright") ? "/opt/node22/lib/node_modules/playwright" : "playwright"));
const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const SITE = path.join(ROOT, "site");
const OUT = path.join(ROOT, "Production", "Kindling", "print");
const args = new Set(process.argv.slice(2));
const DECKS = ["embers", "wildfire", "slowburn", "afterdark"];

const TYPES = { ".html": "text/html", ".js": "text/javascript", ".css": "text/css", ".json": "application/json", ".svg": "image/svg+xml", ".woff2": "font/woff2", ".jpg": "image/jpeg", ".png": "image/png" };
const server = http.createServer((req, res) => {
  const p = path.join(SITE, decodeURIComponent(new URL(req.url, "http://x").pathname));
  if (!p.startsWith(SITE) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { "Content-Type": TYPES[path.extname(p)] || "application/octet-stream" });
  fs.createReadStream(p).pipe(res);
});
await new Promise((r) => server.listen(0, r));
const BASE = `http://localhost:${server.address().port}/kindling/deck.html`;

const browser = await pw.chromium.launch();
const ctx = await browser.newContext({ reducedMotion: "reduce" });
// block remote fonts/assets: print files use the self-hosted fonts in site/assets/fonts
await ctx.route(/^https?:\/\/(?!localhost)/, (r) => r.abort());
const page = await ctx.newPage();
const open = async (q) => {
  await page.goto(`${BASE}?${q}`, { waitUntil: "load" });
  await page.waitForSelector("html[data-ready='1']", { timeout: 30000 });
};

// 1. overflow check on press-size cards
await open("layout=press&deck=all&side=front&rules=1");
const bad = await page.$$eval(".kcard", (cards) => cards.filter((c) => c.scrollHeight > c.clientHeight + 1 || [...c.children].some((k) => k.getBoundingClientRect().bottom > c.getBoundingClientRect().bottom - 2)).map((c) => c.dataset.id));
console.log(bad.length ? `⚠ ${bad.length} card(s) overflow: ${bad.join(", ")}` : "✓ every card fits");
if (args.has("--check")) { await browser.close(); server.close(); process.exit(bad.length ? 1 : 0); }

fs.mkdirSync(OUT, { recursive: true });
const pdf = async (q, file, size) => {
  await open(q);
  await page.pdf({ path: path.join(OUT, file), printBackground: true, preferCSSPageSize: false, ...size });
  console.log("→", path.relative(ROOT, path.join(OUT, file)));
};
const LETTER = { width: "8.5in", height: "11in" };
const PRESS = { width: "69mm", height: "94mm" };

// 2. home prototype sheets (US Letter, duplex)
await pdf("layout=letter&deck=embers", "kindling-prototype-embers-letter.pdf", LETTER);
await pdf("layout=letter&deck=wildfire,slowburn&rules=0", "kindling-prototype-wildfire-slowburn-letter.pdf", LETTER);
await pdf("layout=letter&deck=afterdark&rules=0", "kindling-prototype-afterdark-letter.pdf", LETTER);

// 3. press files: one 69×94 mm page per card (63×88 trim + 3 mm bleed)
for (const d of DECKS) await pdf(`layout=press&deck=${d}&side=front&rules=${d === "embers" ? 1 : 0}`, `kindling-press-${d}-fronts.pdf`, PRESS);
await pdf("layout=press&deck=all&side=back", "kindling-press-backs.pdf", PRESS);

// 4. optional PNGs at 300 dpi (69 mm = 815 px)
if (args.has("--png")) {
  const dir = path.join(OUT, "png");
  fs.mkdirSync(dir, { recursive: true });
  const png = await browser.newPage({ viewport: { width: 815, height: 1110 }, deviceScaleFactor: 1 });
  await png.route(/^https?:\/\/(?!localhost)/, (r) => r.abort());
  for (const side of ["front", "back"]) {
    await png.goto(`${BASE}?layout=press&deck=all&side=${side}&rules=1`, { waitUntil: "load" });
    await png.waitForSelector("html[data-ready='1']");
    await png.addStyleTag({ content: ".kpr-press{zoom:3.1496}" }); // 69mm @96dpi → 815px
    const els = await png.$$(".kpr-press");
    for (let i = 0; i < els.length; i++) {
      const id = await els[i].$eval(".kcard", (c) => c.dataset.id || c.dataset.deck);
      await els[i].screenshot({ path: path.join(dir, `${side === "back" ? "back-" : ""}${id}.png`) });
    }
  }
  console.log("→", path.relative(ROOT, dir), "(PNGs)");
}

await browser.close();
server.close();
