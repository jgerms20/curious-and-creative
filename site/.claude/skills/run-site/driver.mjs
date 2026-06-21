#!/usr/bin/env node
// Smoke driver for the Curious & Creative hub site.
// Boots the running dev server, walks every page, screenshots each one,
// and reports any console errors or broken assets.
//
// Usage:
//   # Make sure the dev server is running first:
//   #   cd <site> && python3 -m http.server 8765 &
//   node .claude/skills/run-site/driver.mjs            # smoke all pages
//   node .claude/skills/run-site/driver.mjs about      # one page only
//   BASE=http://localhost:8765 node ... shows          # custom base URL
//
// Screenshots land in .claude/skills/run-site/screenshots/<page>.png

import pw from '/opt/node22/lib/node_modules/playwright/index.js';
const { chromium } = pw;
import { mkdir } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const BASE = process.env.BASE || 'http://localhost:8765';
const here = dirname(fileURLToPath(import.meta.url));
const shotDir = resolve(here, 'screenshots');
await mkdir(shotDir, { recursive: true });

const PAGES = {
  home:     '/',
  about:    '/pages/about.html',
  shows:    '/pages/shows.html',
  ventures: '/pages/ventures.html',
  contact:  '/pages/contact.html',
};

const pick = process.argv[2];
const todo = pick ? { [pick]: PAGES[pick] } : PAGES;
if (pick && !PAGES[pick]) {
  console.error(`unknown page "${pick}". try one of: ${Object.keys(PAGES).join(', ')}`);
  process.exit(2);
}

const browser = await chromium.launch({ args: ['--no-sandbox'] });
const ctx = await browser.newContext({
  viewport: { width: 1280, height: 900 },
  // Reveal-on-scroll elements use IntersectionObserver and start at opacity 0.
  // A full-page screenshot doesn't scroll, so they'd stay invisible.
  // Reduced-motion mode disables the gate (see css/base.css @media block).
  reducedMotion: 'reduce',
});
let fail = 0;

// Expected, non-fatal noise in this sandbox:
//   - ERR_CERT_AUTHORITY_INVALID on https://fonts.googleapis.com / spotify embeds
//     when the container intercepts TLS.
//   - 404s for /assets/joshua.jpg + /assets/janel.jpg on about.html. These are
//     intentional drop-in slots; the <img onerror="this.remove()"> hides them
//     gracefully until photos are added.
const EXPECTED_404S = new Set(['/assets/joshua.jpg', '/assets/janel.jpg']);

for (const [name, path] of Object.entries(todo)) {
  const page = await ctx.newPage();
  const real = [];
  const noise = [];
  page.on('pageerror', (e) => real.push(`pageerror: ${e.message}`));
  page.on('console', (m) => {
    if (m.type() !== 'error') return;
    const t = m.text();
    if (/ERR_CERT_AUTHORITY_INVALID/.test(t)) { noise.push(`cert: ${t}`); return; }
    if (/status of 404/.test(t)) { noise.push(`404: ${t}`); return; }
    real.push(`console.error: ${t}`);
  });
  page.on('requestfailed', (r) => {
    const u = r.url();
    if (!u.includes('localhost') && !u.startsWith(BASE)) return; // ignore cross-origin
    const path = new URL(u).pathname;
    if (EXPECTED_404S.has(path)) { noise.push(`expected 404: ${path}`); return; }
    real.push(`requestfailed: ${r.method()} ${u} — ${r.failure()?.errorText}`);
  });

  const url = BASE + path;
  const resp = await page.goto(url, { waitUntil: 'load', timeout: 15000 });
  if (!resp || !resp.ok()) {
    console.error(`✗ ${name}  ${url}  HTTP ${resp?.status() ?? 'no-response'}`);
    fail++;
    await page.close();
    continue;
  }

  // Wait for hero / page-head to be reveal-stable
  await page.waitForLoadState('networkidle', { timeout: 8000 }).catch(() => {});

  const title = await page.title();
  const shot = resolve(shotDir, `${name}.png`);
  await page.screenshot({ path: shot, fullPage: true });

  const status = real.length ? '✗' : (noise.length ? '✓ (noise)' : '✓');
  console.log(`${status.padEnd(10)} ${name.padEnd(8)} HTTP 200  "${title}"  → ${shot}`);
  for (const e of real) console.log(`    REAL ${e}`);
  if (process.env.VERBOSE) for (const n of noise) console.log(`    noise: ${n}`);
  if (real.length) fail++;
  await page.close();
}

await browser.close();
process.exit(fail ? 1 : 0);
