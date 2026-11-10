/* Case studies + the Gen Alpha Lab gate.
   CC.renderCases(el, { leg, variant, limit }) renders cases from data/cases.json into el:
     leg     "studio" | "network" | "consultancy" | null (null = every leg)
     variant "rail" (compact cards, e.g. the homepage proof rail) | "full" (the case-study template)
     limit   max number of cases (optional)
   With no matching case it renders nothing and hides el's closest [data-slot] section.
   Returns a promise of the number of cases rendered. Load after js/cc.js. */
(() => {
  const CC = (window.CC = window.CC || {});
  const esc = CC.esc || ((s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c])));
  const root = CC.root || document.body.dataset.root || "./";
  const url = CC.url || ((p) => (!p ? "" : /^(https?:|mailto:|#)/.test(p) ? p : root + p));

  // the rail and the case template are styled in css/legs.css; pull it in on pages that do not link it
  if (!document.querySelector('link[href$="css/legs.css"]')) {
    const l = document.createElement("link");
    l.rel = "stylesheet";
    l.href = url("css/legs.css");
    document.head.appendChild(l);
  }

  const LEGS = {
    studio: { label: "The Studio", page: "pages/studio.html" },
    network: { label: "The Network", page: "pages/shows.html" },
    consultancy: { label: "The Consultancy", page: "pages/consultancy.html" },
  };
  const has = (v) => (Array.isArray(v) ? v.length > 0 : v != null && String(v).trim() !== "");
  const when = (iso) => {
    if (!iso) return "";
    const d = new Date(iso + "T12:00:00");
    return isNaN(d) ? "" : d.toLocaleDateString("en-US", { month: "long", day: "numeric", year: "numeric" });
  };
  const ARROW = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 8h10M9 4l4 4-4 4"/></svg>';

  let cache;
  const load = () => (cache = cache || fetch(url("data/cases.json"), { cache: "no-cache" }).then((r) => (r.ok ? r.json() : null)).catch(() => null));

  const caseHref = (c) => url(`${(LEGS[c.leg] || LEGS.studio).page}#case-${c.id}`);

  const rail = (c) => `<a class="case-card" href="${esc(caseHref(c))}">
      <span class="case-card__leg">${esc((LEGS[c.leg] || {}).label || "")}</span>
      <b class="case-card__client">${esc(c.client)}</b>
      ${has(c.occasion) ? `<span class="case-card__occasion">${esc(c.occasion)}</span>` : ""}
      ${has(c.summary || c.assignment) ? `<span class="case-card__line">${esc(c.summary || c.assignment)}</span>` : ""}
      <span class="case-card__go">Read the case ${ARROW}</span>
    </a>`;

  const list = (items) => `<ul class="case__tags">${items.filter(has).map((x) => `<li>${esc(x)}</li>`).join("")}</ul>`;
  const media = (m) => {
    if (m.embed) return `<figure class="case__media case__media--video"><iframe src="${esc(m.embed)}" title="${esc(m.caption || m.alt || "Video")}" loading="lazy" allow="encrypted-media; picture-in-picture" allowfullscreen></iframe>${m.caption ? `<figcaption>${esc(m.caption)}</figcaption>` : ""}</figure>`;
    if (!m.src) return "";
    if (m.type === "video") return `<figure class="case__media case__media--video"><video controls preload="metadata" playsinline src="${esc(url(m.src))}"${m.poster ? ` poster="${esc(url(m.poster))}"` : ""}></video>${m.caption ? `<figcaption>${esc(m.caption)}</figcaption>` : ""}</figure>`;
    return `<figure class="case__media"><img src="${esc(url(m.src))}" alt="${esc(m.alt || "")}" loading="lazy">${m.caption ? `<figcaption>${esc(m.caption)}</figcaption>` : ""}</figure>`;
  };
  const row = (label, body) => `<div class="case__row"><dt>${label}</dt><dd>${body}</dd></div>`;

  // compact label / value rows, in the template's field order; a field that is missing renders nothing
  const full = (c) => {
    const rows = [];
    if (has(c.assignment)) rows.push(row("Assignment", esc(c.assignment)));
    const crew = (c.crew || []).filter((p) => p && has(p.name));
    if (crew.length) rows.push(row("Crew", `<ul class="case__crew">${crew.map((p) => `<li><b>${esc(p.name)}</b>${has(p.role) ? `<span>${esc(p.role)}</span>` : ""}</li>`).join("")}</ul>`));
    if (has((c.captured || []).filter(has))) rows.push(row("Captured", list(c.captured)));
    if (has((c.deliverables || []).filter(has))) rows.push(row("Deliverables", list(c.deliverables)));
    const shots = (c.media || []).map(media).filter(Boolean);
    if (shots.length) rows.push(row("Stills &amp; video", `<div class="case__gallery">${shots.join("")}</div>`));
    if (has(c.turnaround)) rows.push(row("Turnaround", esc(c.turnaround)));
    const t = c.testimonial;
    const quote = t && t.approved === true && has(t.quote)
      ? `<blockquote class="case__quote"><p>${esc(t.quote)}</p>${has(t.name) ? `<footer>${esc(t.name)}${has(t.role) ? `, ${esc(t.role)}` : ""}</footer>` : ""}</blockquote>` : "";
    const meta = [(LEGS[c.leg] || {}).label, when(c.date)].filter(Boolean).join(" · ");
    return `<article class="case" id="case-${esc(c.id)}">
      <header class="case__head">
        ${meta ? `<span class="eyebrow">${esc(meta)}</span>` : ""}
        <h3 class="case__client">${esc(c.client)}</h3>
        ${has(c.occasion) ? `<p class="case__occasion">${esc(c.occasion)}</p>` : ""}
      </header>
      ${rows.length ? `<dl class="case__body">${rows.join("")}</dl>` : ""}
      ${quote}
    </article>`;
  };

  CC.renderCases = (el, opts = {}) => {
    if (!el) return Promise.resolve(0);
    const { leg = null, variant = "rail", limit } = opts;
    const slot = el.closest("[data-slot]");
    return load().then((d) => {
      let cases = ((d && d.cases) || []).filter((c) => c && c.id && c.client && (!leg || c.leg === leg));
      cases.sort((a, b) => String(b.date || "").localeCompare(String(a.date || "")));
      if (limit) cases = cases.slice(0, limit);
      el.innerHTML = cases.length ? (variant === "full" ? cases.map(full).join("") : `<div class="case-rail">${cases.map(rail).join("")}</div>`) : "";
      if (slot) slot.hidden = !cases.length;
      if (cases.length && location.hash.startsWith("#case-")) {
        const t = document.getElementById(location.hash.slice(1));
        if (t) setTimeout(() => t.scrollIntoView(), 60);
      }
      return cases.length;
    });
  };

  /* ---------- Gen Alpha Lab password gate ----------
     A light gate in front of an invite-only project: keeps casual visitors out. The password's
     sha256 lives in data/projects.json, so it is not real access control.
     Markup: <a href="#" data-lab-gate="genalpha">…</a> */
  const sha256 = async (t) => [...new Uint8Array(await crypto.subtle.digest("SHA-256", new TextEncoder().encode(t)))].map((b) => b.toString(16).padStart(2, "0")).join("");
  let projects;
  const project = (id) => (projects = projects || fetch(url("data/projects.json"), { cache: "no-cache" }).then((r) => (r.ok ? r.json() : null)).catch(() => null))
    .then((d) => ((d && d.projects) || []).find((p) => p.id === id && p.gate && p.url));

  CC.labGate = async (id, opener) => {
    const p = await project(id);
    if (!p) return;
    const key = "cc-gate-" + p.id;
    try { if (sessionStorage.getItem(key) === p.gate) { location.href = p.url; return; } } catch (e) { /* storage blocked */ }
    let dlg = document.getElementById("lab-gate");
    if (!dlg) {
      dlg = document.createElement("dialog");
      dlg.id = "lab-gate";
      dlg.className = "lgate";
      dlg.setAttribute("aria-labelledby", "lab-gate-h");
      document.body.appendChild(dlg);
    }
    dlg.innerHTML = `<form method="dialog" class="lgate__form">
      <span class="lgate__mark" aria-hidden="true">α</span>
      <h2 id="lab-gate-h">${esc(p.name)}</h2>
      <p>The Lab is invite only. Enter the password to go in.</p>
      <label class="sr-only" for="lab-gate-pw">Password</label>
      <input id="lab-gate-pw" type="password" autocomplete="off" placeholder="Password" required>
      <p class="lgate__err" role="alert" hidden>That is not the password. Try again.</p>
      <div class="lgate__actions"><button class="btn" type="submit">Enter</button><button class="btn btn--ghost" type="button" data-lgate-close>Not now</button></div>
    </form>`;
    const form = dlg.querySelector("form"), input = dlg.querySelector("input"), err = dlg.querySelector(".lgate__err");
    dlg.querySelector("[data-lgate-close]").addEventListener("click", () => dlg.close());
    dlg.addEventListener("close", () => { if (opener && opener.focus) opener.focus(); }, { once: true });
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      if ((await sha256(input.value.trim().toLowerCase())) === p.gate) {
        try { sessionStorage.setItem(key, p.gate); } catch (x) { /* storage blocked */ }
        location.href = p.url;
      } else { err.hidden = false; input.select(); }
    });
    dlg.showModal();
    input.focus();
  };
  document.addEventListener("click", (e) => {
    const a = e.target.closest("[data-lab-gate]");
    if (!a) return;
    e.preventDefault();
    CC.labGate(a.dataset.labGate, a);
  });

  // pages that carry a Selected work slot fill it on load: <div data-cases="studio" data-variant="full"></div>
  const boot = () => document.querySelectorAll("[data-cases]").forEach((el) => {
    CC.renderCases(el, { leg: el.dataset.cases || null, variant: el.dataset.variant || "full", limit: Number(el.dataset.limit) || undefined });
  });
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot); else boot();
})();
