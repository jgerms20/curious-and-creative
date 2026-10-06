/* Curious & Creative — shared site runtime.
   Every page: <body data-page="…" data-root="./ or ../">, with
   <div data-cc="header"></div> and <div data-cc="footer"></div>.
   Content comes from data/content.json (refreshed by the GitHub Action). */
(() => {
  const root = document.body.dataset.root || "./";
  const page = document.body.dataset.page || "";
  const CC = (window.CC = { root, page });
  // public (publishable) key: access is enforced by database rules, not by hiding this
  CC.SUPABASE = { url: "https://zsgacmfbqqmbcexomyoo.supabase.co", key: "sb_publishable_2GNNUjTGciy6Wi_wxDuStg_tY1sP28y" };

  /* ---------------- helpers ---------------- */
  const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const url = (p) => (!p ? "" : /^(https?:|mailto:|#)/.test(p) ? p : root + p);
  const ago = (iso) => {
    if (!iso) return "";
    const d = (Date.now() - new Date(iso).getTime()) / 86400000;
    if (d < 1) return "Today";
    if (d < 2) return "Yesterday";
    if (d < 7) return `${Math.floor(d)} days ago`;
    if (d < 30) return `${Math.floor(d / 7)} wk${Math.floor(d / 7) > 1 ? "s" : ""} ago`;
    return new Date(iso).toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" });
  };
  const dur = (s) => {
    if (!s) return "";
    const h = Math.floor(s / 3600), m = Math.round((s % 3600) / 60);
    return h ? `${h} hr ${m} min` : `${m} min`;
  };
  const icon = {
    search: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5"/><path d="M20 20l-4.6-4.6"/></svg>',
    menu: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>',
    close: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>',
    moon: '<svg class="moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5z"/></svg>',
    sun: '<svg class="sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4.2"/><path d="M12 2.5v2.2M12 19.3v2.2M4.3 4.3l1.6 1.6M18.1 18.1l1.6 1.6M2.5 12h2.2M19.3 12h2.2M4.3 19.7l1.6-1.6M18.1 5.9l1.6-1.6"/></svg>',
    arrow: '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 8h10M9 4l4 4-4 4"/></svg>',
    left: '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M10 3L5 8l5 5"/></svg>',
    right: '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 3l5 5-5 5"/></svg>',
    play: '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M8 5.14v13.72a1 1 0 0 0 1.53.85l10.7-6.86a1 1 0 0 0 0-1.7L9.53 4.3A1 1 0 0 0 8 5.14Z"/></svg>',
    ext: '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 3h7v7M13 3L4 12"/></svg>',
  };
  Object.assign(CC, { esc, url, ago, dur, icon });

  /* ---------------- site map (for nav + search) ---------------- */
  const PAGES = [
    { label: "Home", href: "index.html", words: "home front page latest" },
    { label: "About", href: "pages/about.html", words: "about us story who joshua janel founders team duo" },
    { label: "Studio", href: "pages/studio.html", words: "studio services strategy brand building production consulting hire work with us" },
    { label: "Podcasts", href: "pages/shows.html", words: "podcasts shows listen episodes spotify apple youtube" },
    { label: "Videos", href: "index.html#videos", words: "videos youtube watch approachable ai" },
    { label: "Photography", href: "pages/art.html", words: "photography photos art prints gallery portraits fashion events rio landscapes travel" },
    { label: "Archive", href: "pages/archive.html", words: "archive every episode all back catalog history" },
    { label: "Inventions", href: "pages/inventions.html", words: "inventions build products" },
    { label: "Kindling", href: "kindling/", words: "kindling card game couples intimacy deck play" },
    { label: "Shop", href: "pages/shop.html", words: "shop store buy order prints art artwork janel joshua kindling deck" },
    { label: "Network", href: "pages/network.html", words: "network shows web map secondary god is brazilian dominate the decade aspiring abolitionist" },
    { label: "Contact", href: "pages/contact.html", words: "contact email hello pitch guest press" },
  ];
  CC.PAGES = PAGES;

  /* ---------------- theme ---------------- */
  const setTheme = (t) => {
    document.documentElement.dataset.theme = t;
    try { localStorage.setItem("cc-theme", t); } catch (e) { /* storage blocked */ }
    document.querySelectorAll("[data-theme-toggle]").forEach((b) => {
      b.setAttribute("aria-label", t === "dark" ? "Switch to light mode" : "Switch to dark mode");
      b.setAttribute("aria-pressed", String(t === "dark"));
    });
  };
  CC.toggleTheme = () => setTheme(document.documentElement.dataset.theme === "dark" ? "light" : "dark");

  /* ---------------- chrome: header / drawer / search / footer ---------------- */
  const navLink = (href, label) => {
    const here = page && href === `pages/${page}.html`;
    return `<a href="${url(href)}"${here ? ' aria-current="page"' : ""}>${label}</a>`;
  };

  const header = `
    <a class="skip" href="#main">Skip to content</a>
    <header class="hdr" id="hdr">
      <div class="hdr__bar wrap">
        <a class="wordmark" href="${url("index.html")}" aria-label="Curious and Creative — home"><span class="g">Curious</span><span class="a">&amp;</span><span class="p">Creative</span></a>
        <button class="hdr__search" type="button" data-open-search aria-haspopup="dialog">${icon.search}<span>Discover anything</span><kbd>/</kbd></button>
        <nav class="hdr__links" aria-label="Primary">${navLink("pages/about.html", "About")}${navLink("pages/studio.html", "Studio")}${navLink("pages/shows.html", "Podcasts")}${navLink("index.html#videos", "Videos")}${navLink("pages/art.html", "Photography")}${navLink("pages/shop.html", "Shop")}</nav>
        <button class="icon-btn hdr__search-mobile" type="button" data-open-search aria-label="Search">${icon.search}</button>
        <button class="icon-btn theme-btn" type="button" data-theme-toggle aria-label="Switch to dark mode">${icon.moon}${icon.sun}</button>
        <button class="icon-btn" type="button" data-open-drawer aria-label="Open menu" aria-expanded="false" aria-controls="drawer">${icon.menu}</button>
      </div>
    </header>`;

  const footer = `
    <footer class="ftr wrap">
      <div class="ftr__bar">
        <a class="wordmark" href="${url("index.html")}"><span class="g">Curious</span><span class="a">&amp;</span><span class="p">Creative</span></a>
        <nav class="ftr__links" aria-label="Footer">${PAGES.filter((p) => !["Home", "Videos"].includes(p.label)).map((p) => `<a href="${url(p.href)}">${p.label}</a>`).join("")}</nav>
        <p class="ftr__copy">© ${new Date().getFullYear()} Curious &amp; Creative · Joshua German &amp; Janel Moore</p>
      </div>
      <p class="ftr__sign">Built curious. Made creative. · <a href="${url("backstage/")}" style="opacity:.7">Team</a></p>
    </footer>`;

  const drawer = `
    <div class="scrim" data-close-drawer></div>
    <aside class="drawer" id="drawer" role="dialog" aria-modal="true" aria-label="Menu" aria-hidden="true">
      <div class="drawer__top">
        <a class="wordmark" href="${url("index.html")}"><span class="g" style="color:#5BD36B">Curious</span><span class="a">&amp;</span><span class="p" style="color:#FF6FB0">Creative</span></a>
        <button class="icon-btn" type="button" data-close-drawer aria-label="Close menu">${icon.close}</button>
      </div>
      <nav class="drawer__nav" aria-label="Menu">${PAGES.map((p) => `<a href="${url(p.href)}">${p.label}</a>`).join("")}</nav>
      <div><h3>Our shows</h3><div class="drawer__shows" data-drawer-shows></div></div>
      <div><h3>Find us</h3><div class="drawer__social">
        <a href="https://instagram.com/jgerms20" target="_blank" rel="noopener">Instagram</a>
        <a href="https://www.youtube.com/@Approachable.A.I" target="_blank" rel="noopener">YouTube</a>
        <a href="https://jgerms20.substack.com" target="_blank" rel="noopener">Substack</a>
        <a href="https://joshuamgerman.com" target="_blank" rel="noopener">joshuamgerman.com</a>
      </div></div>
    </aside>
    <div class="search" id="search" role="dialog" aria-modal="true" aria-label="Search" aria-hidden="true">
      <div class="search__in">
        <div class="search__top">
          <span class="eyebrow">Search every show, episode, and page</span>
          <button class="icon-btn" type="button" data-close-search aria-label="Close search">${icon.close}</button>
        </div>
        <label class="search__field">${icon.search}<span class="sr-only">Search</span><input id="search-input" type="search" autocomplete="off" spellcheck="false" placeholder="Try “Erykah Badu”"></label>
        <div class="search__hint">Try:
          <button type="button" data-q="Erykah Badu">Erykah Badu</button>
          <button type="button" data-q="Five Percent">Five Percent Nation</button>
          <button type="button" data-q="vibe coding">Vibe coding</button>
          <button type="button" data-q="inauguration">Inauguration</button>
          <button type="button" data-q="photography">Photography</button>
        </div>
        <div id="search-results" aria-live="polite"></div>
      </div>
    </div>`;

  const mount = (sel, html) => { const el = document.querySelector(sel); if (el) el.outerHTML = html; };
  mount('[data-cc="header"]', header);
  mount('[data-cc="footer"]', footer);
  document.body.insertAdjacentHTML("beforeend", drawer);
  setTheme(document.documentElement.dataset.theme || "light");

  const hdr = document.getElementById("hdr");
  const onScroll = () => hdr && hdr.classList.toggle("is-scrolled", window.scrollY > 8);
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* modal plumbing */
  let lastFocus = null;
  const openLayer = (el, focusSel) => {
    lastFocus = document.activeElement;
    el.classList.add("is-open");
    el.setAttribute("aria-hidden", "false");
    document.documentElement.classList.add("is-locked");
    setTimeout(() => { const f = el.querySelector(focusSel); if (f) f.focus(); }, 60);
  };
  const closeLayer = (el) => {
    if (!el || !el.classList.contains("is-open")) return;
    el.classList.remove("is-open");
    el.setAttribute("aria-hidden", "true");
    if (!document.querySelector(".drawer.is-open, .search.is-open, .lightbox.is-open")) document.documentElement.classList.remove("is-locked");
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  };
  CC.openLayer = openLayer;
  CC.closeLayer = closeLayer;

  const drawerEl = document.getElementById("drawer");
  const scrim = document.querySelector(".scrim");
  const searchEl = document.getElementById("search");
  const input = document.getElementById("search-input");

  const openDrawer = () => { scrim.classList.add("is-open"); openLayer(drawerEl, "[data-close-drawer].icon-btn"); document.querySelectorAll("[data-open-drawer]").forEach((b) => b.setAttribute("aria-expanded", "true")); };
  const closeDrawer = () => { scrim.classList.remove("is-open"); closeLayer(drawerEl); document.querySelectorAll("[data-open-drawer]").forEach((b) => b.setAttribute("aria-expanded", "false")); };
  CC.openSearch = (q) => {
    if (drawerEl.classList.contains("is-open")) closeDrawer();
    openLayer(searchEl, "#search-input");
    if (typeof q === "string") { input.value = q; runSearch(); }
  };
  const closeSearch = () => closeLayer(searchEl);

  document.addEventListener("click", (e) => {
    const t = e.target.closest("[data-open-search],[data-close-search],[data-open-drawer],[data-close-drawer],[data-theme-toggle],[data-q],[data-search-topic]");
    if (!t) return;
    if (t.matches("[data-open-search]")) CC.openSearch();
    else if (t.matches("[data-close-search]")) closeSearch();
    else if (t.matches("[data-open-drawer]")) openDrawer();
    else if (t.matches("[data-close-drawer]")) closeDrawer();
    else if (t.matches("[data-theme-toggle]")) CC.toggleTheme();
    else if (t.matches("[data-q]")) { input.value = t.dataset.q; runSearch(); input.focus(); }
    else if (t.matches("[data-search-topic]")) { e.preventDefault(); CC.openSearch(t.dataset.searchTopic); }
  });
  drawerEl.addEventListener("click", (e) => { if (e.target.closest("a")) closeDrawer(); });
  searchEl.addEventListener("click", (e) => { if (e.target.closest("a")) closeSearch(); });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") { closeSearch(); closeDrawer(); }
    const typing = /INPUT|TEXTAREA|SELECT/.test(document.activeElement?.tagName) || document.activeElement?.isContentEditable;
    if (!typing && (e.key === "/" || ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k"))) { e.preventDefault(); CC.openSearch(); }
  });

  /* ---------------- fuzzy search ---------------- */
  const fold = (s) => String(s || "").normalize("NFKD").replace(/[̀-ͯ]/g, "").toLowerCase();
  const words = (s) => fold(s).split(/[^a-z0-9]+/).filter(Boolean);
  // rough phonetic key so "Erica" ≈ "Erykah", "Kristina" ≈ "Christina"
  const phon = (w) => w
    .replace(/^kn/, "n").replace(/^wr/, "r").replace(/ph/g, "f").replace(/ck/g, "k").replace(/ch/g, "k")
    .replace(/c(?=[eiy])/g, "s").replace(/[cq]/g, "k").replace(/x/g, "ks").replace(/z/g, "s").replace(/y/g, "i")
    .replace(/(?!^)h/g, "").replace(/(.)\1+/g, "$1");
  const lev = (a, b) => {
    if (Math.abs(a.length - b.length) > 2) return 9;
    const row = Array.from({ length: b.length + 1 }, (_, i) => i);
    for (let i = 1; i <= a.length; i++) {
      let prev = row[0]; row[0] = i;
      for (let j = 1; j <= b.length; j++) {
        const cur = row[j];
        row[j] = Math.min(row[j] + 1, row[j - 1] + 1, prev + (a[i - 1] === b[j - 1] ? 0 : 1));
        prev = cur;
      }
    }
    return row[b.length];
  };
  const tokenScore = (q, w) => {
    if (w === q) return 4;
    if (w.startsWith(q) && q.length >= 2) return 3;
    const pq = phon(q), pw = phon(w);
    if (pq.length >= 3 && (pw === pq || pw.startsWith(pq))) return 2.5;
    if (q.length >= 4 && pq[0] === pw[0] && lev(pq, pw) <= (q.length >= 9 ? 2 : 1)) return 1.6;
    return 0;
  };

  let INDEX = [];
  const addDoc = (doc) => {
    const fields = [[doc.title, 3], [doc.sub, 1.6], [doc.text, 1]];
    doc._t = fields.map(([s, w]) => ({ w, toks: [...new Set(words(s))] }));
    INDEX.push(doc);
  };
  const score = (doc, qt) => {
    let total = 0, hits = 0;
    for (const q of qt) {
      let best = 0;
      for (const f of doc._t) for (const w of f.toks) { const s = tokenScore(q, w) * f.w; if (s > best) best = s; }
      if (best > 0) hits++;
      total += best;
    }
    const need = qt.length <= 2 ? qt.length : qt.length - 1;
    return hits >= need ? total + (doc.boost || 0) : 0;
  };
  CC.searchDocs = (q, filter) => {
    const qt = words(q).filter((w) => w.length > 1 || /\d/.test(w));
    if (!qt.length) return [];
    return INDEX.filter((d) => !filter || filter(d))
      .map((d) => ({ d, s: score(d, qt) }))
      .filter((r) => r.s > 0)
      .sort((a, b) => b.s - a.s || String(b.d.date || "").localeCompare(String(a.d.date || "")))
      .map((r) => r.d);
  };
  const highlight = (text, q) => {
    let out = esc(text);
    words(q).filter((w) => w.length > 2).forEach((w) => {
      out = out.replace(new RegExp(`\\b(${w.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}[a-z]*)`, "gi"), "<mark>$1</mark>");
    });
    return out;
  };

  const resultsEl = document.getElementById("search-results");
  let selIdx = -1;
  function runSearch() {
    const q = input.value.trim();
    selIdx = -1;
    if (!q) { resultsEl.innerHTML = ""; return; }
    const hits = CC.searchDocs(q);
    if (!hits.length) {
      resultsEl.innerHTML = `<p class="search__empty">Nothing for “${esc(q)}” yet. Try a guest, a topic, or a show name — or <a class="pill-more" href="${url("pages/archive.html")}">browse the archive</a>.</p>`;
      return;
    }
    const groups = [["Episodes & videos", hits.filter((d) => d.type === "episode")], ["Shows", hits.filter((d) => d.type === "show")], ["Photography", hits.filter((d) => d.type === "photo")], ["Pages", hits.filter((d) => d.type === "page")]];
    resultsEl.innerHTML = groups.filter(([, g]) => g.length).map(([name, g]) => `
      <div class="search__group"><h3>${name} · ${g.length}</h3>
        ${g.slice(0, name.startsWith("Ep") ? 12 : 6).map((d) => `
          <a class="search__res" href="${esc(d.href)}"${/^https?:/.test(d.href) ? ' target="_blank" rel="noopener"' : ""} data-show="${esc(d.show || "")}">
            ${d.img ? `<img src="${esc(d.img)}" alt="" loading="lazy">` : `<span class="ph">${esc((d.title || "?")[0])}</span>`}
            <span><b>${highlight(d.title, q)}</b><small>${esc(d.sub || "")}${d.text ? " — " + highlight(d.text.slice(0, 160), q) : ""}</small></span>
          </a>`).join("")}
      </div>`).join("");
  }
  input.addEventListener("input", runSearch);
  input.addEventListener("keydown", (e) => {
    const items = [...resultsEl.querySelectorAll(".search__res")];
    if (!items.length) return;
    if (e.key === "ArrowDown" || e.key === "ArrowUp") {
      e.preventDefault();
      selIdx = (selIdx + (e.key === "ArrowDown" ? 1 : -1) + items.length) % items.length;
      items.forEach((el, i) => el.classList.toggle("is-sel", i === selIdx));
      items[selIdx].scrollIntoView({ block: "nearest" });
    } else if (e.key === "Enter") {
      (items[selIdx] || items[0]).click();
    }
  });

  /* ---------------- data ---------------- */
  const SHOW_ORDER = (shows) => [...shows].sort((a, b) => (b.flagship ? 1 : 0) - (a.flagship ? 1 : 0) || String(b.latest || "").localeCompare(String(a.latest || "")));
  CC.showOrder = SHOW_ORDER;
  CC.art = (s) => (s && s.art ? url(s.art) : "");
  CC.epImg = (e, show) => (e.image ? e.image : CC.art(show));
  CC.epHref = (e) => e.url || e.spotify_url || "#";
  CC.isNew = (iso) => iso && Date.now() - new Date(iso).getTime() < 21 * 86400000;
  CC.showLinks = (s) => {
    const l = [];
    if (s.spotify_url) l.push(["Spotify", s.spotify_url]);
    if (s.apple_url) l.push(["Apple Podcasts", s.apple_url]);
    if (s.youtube_url) l.push(["YouTube", s.youtube_url]);
    return l;
  };

  const loadJSON = (p) => fetch(url(p), { cache: "no-cache" }).then((r) => (r.ok ? r.json() : null)).catch(() => null);
  CC.ready = Promise.all([loadJSON("data/content.json"), loadJSON("data/photos.json"), loadJSON("data/shows.json")]).then(([content, photos, registry]) => {
    const data = content || { shows: [], episodes: [] };
    // registry edits (tier, feature, copy) apply immediately, before the next refresh
    const reg = Object.fromEntries(((registry && registry.shows) || []).map((s) => [s.key, s]));
    data.shows = (data.shows || []).map((s) => {
      const r = reg[s.key] || {};
      return { ...s, tier: r.tier || s.tier || "primary", feature: r.feature ?? s.feature, name: r.name || s.name, tagline: r.tagline || s.tagline, about: r.about || s.about, hosts: r.hosts || s.hosts };
    });
    const allPhotos = (photos && photos.photos) || [];
    data.photos = allPhotos.some((p) => p.featured) ? allPhotos.filter((p) => p.featured) : allPhotos;
    data.byKey = Object.fromEntries((data.shows || []).map((x) => [x.key, x]));
    data.shows = SHOW_ORDER(data.shows || []);
    data.primary = data.shows.filter((x) => x.tier !== "secondary");
    data.secondary = data.shows.filter((x) => x.tier === "secondary");
    CC.isPrimary = (k) => (data.byKey[k] || {}).tier !== "secondary";
    CC.data = data;

    INDEX = [];
    PAGES.forEach((p) => addDoc({ type: "page", title: p.label, sub: "Page", text: p.words, href: url(p.href), boost: 0.5 }));
    data.shows.forEach((s) => addDoc({ type: "show", show: s.key, title: s.name, sub: `${s.kind === "youtube" ? "YouTube show" : "Podcast"} · ${(s.hosts || []).join(", ")}`, text: [s.tagline, s.about, s.description].filter(Boolean).join(" "), img: CC.art(s), href: url(`pages/shows.html#${s.key}`), boost: 1 }));
    (data.episodes || []).forEach((e) => {
      const s = data.byKey[e.show] || {};
      addDoc({ type: "episode", show: e.show, title: e.title, sub: `${s.short || s.name || ""} · ${ago(e.date)}`, text: e.description || "", img: CC.epImg(e, s), href: CC.epHref(e), date: e.date });
    });
    data.photos.forEach((p) => addDoc({ type: "photo", title: p.alt || p.set, sub: `Photography · ${p.set}`, text: "photo photography " + p.set, img: url(p.thumb), href: url(`pages/art.html#${p.id}`) }));

    const ds = document.querySelector("[data-drawer-shows]");
    if (ds) ds.innerHTML = data.shows.map((s) => `<a href="${url(`pages/shows.html#${s.key}`)}" data-show="${s.key}">${s.art ? `<img src="${CC.art(s)}" alt="" loading="lazy">` : '<span class="ph"></span>'}${esc(s.name)}</a>`).join("");
    if (input.value) runSearch();
    const qp = new URLSearchParams(location.search).get("q");
    if (qp && page !== "archive") CC.openSearch(qp);
    return data;
  });


  /* ---------------- the network web (shows ↔ hosts) ---------------- */
  CC.network = (data, opts = {}) => {
    const W = 1000, H = 690, cx = 500, cy = 330;
    const pt = (deg, rx, ry) => [cx + rx * Math.cos((deg * Math.PI) / 180), cy + ry * Math.sin((deg * Math.PI) / 180)];
    const who = (s) => {
      const h = (s.hosts || []).join(" ").toLowerCase();
      return [h.includes("joshua") && "joshua", h.includes("janel") && "janel"].filter(Boolean);
    };
    const slots = {
      top: [[-90, 300, 215]],
      left: { primary: [[214, 300, 215], [146, 300, 215], [180, 330, 215]], secondary: [[244, 420, 290], [180, 360, 285], [120, 420, 290]] },
      right: { primary: [[-34, 300, 215], [34, 300, 215], [0, 330, 215]], secondary: [[16, 420, 260], [-64, 420, 290], [60, 420, 290]] },
      future: [[72, 430, 290], [90, 440, 300], [108, 430, 290]],
    };
    const used = { left: { primary: 0, secondary: 0 }, right: { primary: 0, secondary: 0 } };
    const nodes = data.shows.map((s) => {
      const hosts = who(s);
      const tier = s.tier === "secondary" ? "secondary" : "primary";
      let pos;
      if (s.flagship) pos = slots.top[0];
      else {
        const side = hosts.includes("janel") && !hosts.includes("joshua") ? "right" : "left";
        pos = slots[side][tier][used[side][tier]++] || slots[side][tier][0];
      }
      const [x, y] = pt(...pos);
      return { s, hosts, tier, x, y, r: s.flagship ? 58 : tier === "primary" ? 46 : 32 };
    });
    const people = { joshua: [cx - 150, cy + 25, "Joshua", "assets/people/joshua.jpg"], janel: [cx + 150, cy + 25, "Janel", "assets/people/janel.jpg"] };
    const line = (a, b, cls, key) => `<line class="web__edge ${cls}" data-edge="${key}" x1="${a[0]}" y1="${a[1]}" x2="${b[0]}" y2="${b[1]}"/>`;
    let edges = Object.keys(people).map((k) => line([cx, cy - 40], people[k], "web__edge--core", k)).join("");
    nodes.forEach((n) => n.hosts.forEach((h) => { edges += line(people[h], [n.x, n.y], `web__edge--${n.tier}`, `${h} ${n.s.key}`); }));
    const futures = slots.future.map((f, i) => { const [x, y] = pt(...f); return { x, y, i }; });
    futures.forEach((f) => { edges += line([cx, cy - 40], [f.x, f.y], "web__edge--future", "future"); });
    const img = (id, x, y, r, src, label) => `<clipPath id="${id}"><circle cx="${x}" cy="${y}" r="${r}"/></clipPath><circle class="web__ring" cx="${x}" cy="${y}" r="${r + 4}"/>${src ? `<image href="${esc(url(src))}" x="${x - r}" y="${y - r}" width="${r * 2}" height="${r * 2}" clip-path="url(#${id})" preserveAspectRatio="xMidYMid slice"/>` : `<circle cx="${x}" cy="${y}" r="${r}" fill="var(--c)"/>`}<text class="web__label" x="${x}" y="${y + r + 22}">${esc(label)}</text>`;
    const showNodes = nodes.map((n, i) => `<a class="web__node web__node--${n.tier}" href="${url(`pages/shows.html#${n.s.key}`)}" data-show="${n.s.key}" data-node="${n.s.key}" data-links="${n.hosts.join(" ")}" aria-label="${esc(n.s.name)}">${img("wc" + i, n.x, n.y, n.r, n.s.art, n.s.short || n.s.name)}${n.s.archive ? `<text class="web__tag" x="${n.x}" y="${n.y + n.r + 40}">archive</text>` : ""}</a>`).join("");
    const peopleNodes = Object.entries(people).map(([k, [x, y, label, src]]) => `<a class="web__node web__node--host" href="${url("pages/about.html")}" data-node="${k}" aria-label="${label}">${img("wp" + k, x, y, 40, src, label)}</a>`).join("");
    const futureNodes = futures.map((f) => `<g class="web__node web__node--future" aria-hidden="true"><circle cx="${f.x}" cy="${f.y}" r="26"/><text class="web__plus" x="${f.x}" y="${f.y + 7}">+</text><text class="web__label" x="${f.x}" y="${f.y + 50}">Next show</text></g>`).join("");
    const hub = `<g class="web__hub"><circle cx="${cx}" cy="${cy - 40}" r="62"/><text x="${cx}" y="${cy - 46}">Curious</text><text x="${cx}" y="${cy - 26}">&amp; Creative</text></g>`;
    return `<svg class="web" viewBox="0 0 ${W} ${H}" role="img" aria-label="The Curious & Creative network: Joshua and Janel connected to every show they host">${edges}${futureNodes}${hub}${peopleNodes}${showNodes}</svg>`;
  };
  CC.wireNetwork = (root) => {
    const svg = root.querySelector(".web");
    if (!svg) return;
    const focus = (key) => {
      svg.classList.toggle("is-focus", !!key);
      svg.querySelectorAll(".web__edge").forEach((e) => e.classList.toggle("is-on", !!key && e.dataset.edge.split(" ").includes(key)));
      svg.querySelectorAll(".web__node").forEach((n) => {
        const linked = n.dataset.node === key || (n.dataset.links || "").split(" ").includes(key) || (key && svg.querySelector(`[data-node="${key}"]`)?.dataset.links?.split(" ").includes(n.dataset.node));
        n.classList.toggle("is-on", !!key && !!linked);
      });
    };
    svg.querySelectorAll("[data-node]").forEach((n) => {
      n.addEventListener("mouseenter", () => focus(n.dataset.node));
      n.addEventListener("focus", () => focus(n.dataset.node));
      n.addEventListener("mouseleave", () => focus(null));
      n.addEventListener("blur", () => focus(null));
    });
  };

  /* ---------------- reveal on scroll ---------------- */
  CC.reveal = (scope = document) => {
    const els = scope.querySelectorAll(".rv:not(.is-in)");
    if (!("IntersectionObserver" in window) || matchMedia("(prefers-reduced-motion: reduce)").matches) { els.forEach((el) => el.classList.add("is-in")); return; }
    const io = new IntersectionObserver((ents) => ents.forEach((en) => { if (en.isIntersecting) { en.target.classList.add("is-in"); io.unobserve(en.target); } }), { rootMargin: "0px 0px -8% 0px" });
    els.forEach((el) => io.observe(el));
  };
  CC.reveal();
})();
