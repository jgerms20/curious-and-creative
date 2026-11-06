/* Curious & Creative Company — shared site runtime.
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
    { label: "Our Story", href: "pages/about.html", nav: true, words: "about our story who joshua janel founders team duo company" },
    { label: "Podcast Network", href: "pages/shows.html", nav: true, menu: "shows", words: "podcasts shows network curious + creative network listen episodes spotify apple youtube flagship regular culture news reads sports industry jazz riff morning read la daily global read business of hollywood fast break waiver wire gamecocks columbia" },
    { label: "Studio", href: "pages/studio.html", nav: true, words: "studio services offerings photography websites website build social media digital presence community management growth ads advertising ai workflow enablement podcast setup marketing funnel podcast production editing video strategy consulting branding events hire work with us" },
    { label: "Shop", href: "pages/shop.html", nav: true, words: "shop store buy order prints art artwork janel joshua kindling deck inventions apps tools games research lab gen alpha" },
    { label: "Manifesto", href: "pages/manifesto.html", words: "manifesto mission standards accuracy journalism principles corrections request a show ideas" },
    { label: "Inventions", href: "pages/inventions.html", words: "inventions apps tools games life gamified grandmaster meme library jukeboxd aetheria gen alpha research lab" },
    { label: "Photography", href: "pages/studio.html#photography", words: "photography photos gallery portraits fashion events rio landscapes travel views by germ" },
    { label: "Videos", href: "pages/videos.html", words: "videos youtube watch approachable ai video episodes" },
    { label: "Writing", href: "pages/writing.html", words: "writing substack essays newsletter posts" },
    { label: "Kindling", href: "kindling/", words: "kindling card game couples intimacy deck play" },
    { label: "Archive", href: "pages/archive.html", words: "archive every episode all back catalog history" },
    { label: "Contact", href: "pages/contact.html", words: "contact email hello pitch guest press request a show" },
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
    const here = page && (href === `pages/${page}.html` || (page === "index" && href === "index.html"));
    return `<a href="${url(href)}"${here ? ' aria-current="page"' : ""}>${label}</a>`;
  };
  // a nav item with a dropdown panel (filled once the data loads); opens on hover or keyboard focus
  const navItem = (p) => (!p.menu ? navLink(p.href, p.label) : `
    <div class="hdr__dd" data-dd>
      ${navLink(p.href, p.label).replace("<a ", '<a aria-haspopup="true" aria-expanded="false" ')}
      <div class="hdr__menu" data-nav-menu="${p.menu}">
        <div class="hdr__menu-list"></div>
        <p class="hdr__menu-foot"><a href="${url("pages/manifesto.html")}">Our standards →</a><a href="${url(p.href + "#network")}">The network map →</a><a href="${url(p.href)}">All shows →</a><a href="${url("pages/archive.html")}">Every episode →</a></p>
      </div>
    </div>`);

  const header = `
    <a class="skip" href="#main">Skip to content</a>
    <header class="hdr" id="hdr">
      <div class="hdr__bar wrap">
        <a class="wordmark" href="${url("index.html")}" aria-label="The Curious &amp; Creative Company — home"><span class="the">The</span><span class="g">Curious</span><span class="a">&amp;</span><span class="p">Creative</span><span class="co">Co.</span></a>
        <button class="hdr__search" type="button" data-open-search aria-haspopup="dialog">${icon.search}<span>Discover anything</span><kbd>/</kbd></button>
        <nav class="hdr__links" aria-label="Primary">${PAGES.filter((p) => p.nav).map(navItem).join("")}</nav>
        <button class="icon-btn hdr__search-mobile" type="button" data-open-search aria-label="Search">${icon.search}</button>
        <button class="icon-btn theme-btn" type="button" data-theme-toggle aria-label="Switch to dark mode">${icon.moon}${icon.sun}</button>
        <button class="icon-btn" type="button" data-open-drawer aria-label="Open menu" aria-expanded="false" aria-controls="drawer">${icon.menu}</button>
      </div>
    </header>`;

  const footer = `
    <footer class="ftr wrap">
      <div class="ftr__bar">
        <a class="wordmark" href="${url("index.html")}"><span class="the">The</span><span class="g">Curious</span><span class="a">&amp;</span><span class="p">Creative</span><span class="co">Co.</span></a>
        <nav class="ftr__links" aria-label="Footer">${PAGES.filter((p) => p.label !== "Home").map((p) => `<a href="${url(p.href)}">${p.label}</a>`).join("")}</nav>
        <p class="ftr__copy">© ${new Date().getFullYear()} The Curious &amp; Creative Company · Joshua German &amp; Janel Moore</p>
      </div>
      <p class="ftr__sign">Built curious. Made creative. · <a href="${url("backstage/")}" style="opacity:.7">Team</a></p>
    </footer>`;

  const drawer = `
    <div class="scrim" data-close-drawer></div>
    <aside class="drawer" id="drawer" role="dialog" aria-modal="true" aria-label="Menu" aria-hidden="true">
      <div class="drawer__top">
        <a class="wordmark" href="${url("index.html")}"><span class="the" style="color:#fff">The</span><span class="g" style="color:#5BD36B">Curious</span><span class="a">&amp;</span><span class="p" style="color:#FF6FB0">Creative</span><span class="co">Co.</span></a>
        <button class="icon-btn" type="button" data-close-drawer aria-label="Close menu">${icon.close}</button>
      </div>
      <nav class="drawer__nav" aria-label="Menu">${PAGES.map((p) => `<a href="${url(p.href)}">${p.label}</a>`).join("")}</nav>
      <div><h3>Our shows</h3><div class="drawer__shows" data-drawer-shows></div></div>
      <div><h3>Find us</h3><div class="drawer__social">
        <a href="https://instagram.com/jgerms20" target="_blank" rel="noopener">Instagram</a>
        <a href="https://www.youtube.com/@Approachable.A.I" target="_blank" rel="noopener">YouTube</a>
        <a href="https://jgerms20.substack.com" target="_blank" rel="noopener">Joshua on Substack</a>
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
  document.querySelectorAll("[data-dd]").forEach((dd) => {
    const trigger = dd.querySelector("a"); let t, hush = false;
    const set = (open) => { clearTimeout(t); dd.classList.toggle("is-open", open); trigger.setAttribute("aria-expanded", String(open)); };
    dd.addEventListener("mouseenter", () => set(true));
    dd.addEventListener("mouseleave", () => { t = setTimeout(() => set(false), 120); }); // a little grace for the cursor
    dd.addEventListener("focusin", () => { if (!hush) set(true); hush = false; });
    dd.addEventListener("focusout", (e) => { if (!dd.contains(e.relatedTarget)) set(false); });
    dd.addEventListener("keydown", (e) => { if (e.key === "Escape" && dd.classList.contains("is-open")) { set(false); hush = document.activeElement !== trigger; trigger.focus(); } });
  });
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
  // one color per show: who makes it. AI-generated shows and hybrids (a host + AI) get their own groups.
  const isHybrid = (s) => !!s && (s.ai === "hybrid" || s.ai === "assisted");
  CC.isHybrid = isHybrid;
  CC.hostGroup = (s) => {
    if (s && s.ai === "full") return "ai";
    if (isHybrid(s)) return "hybrid";
    const h = ((s && s.hosts) || []).join(" ").toLowerCase();
    const jo = h.includes("joshua"), ja = h.includes("janel");
    return jo && ja ? "shared" : ja ? "janel" : "joshua";
  };
  // every group a show belongs to, for the sorter (a hybrid also counts under its host)
  CC.showTags = (s) => {
    const h = ((s && s.hosts) || []).join(" ").toLowerCase();
    const t = new Set([CC.hostGroup(s)]);
    if (h.includes("joshua") && !h.includes("janel")) t.add("joshua");
    if (h.includes("janel") && !h.includes("joshua")) t.add("janel");
    return [...t];
  };
  const firstName = (n) => (n || "").split(" ")[0];
  CC.showByline = (s) => {
    if (!s) return "";
    if (isHybrid(s)) return `Hybrid · ${(s.hosts || []).map(firstName).join(" & ") || "Joshua"} + AI`;
    if (s.ai === "full") return "AI-generated";
    return CC.HOST_LABEL[CC.hostGroup(s)];
  };
  CC.HOST_LABEL = { joshua: "Joshua", janel: "Janel", shared: "Joshua & Janel", ai: "AI-generated", hybrid: "Hybrid · human + AI" };
  CC.showHref = (s) => url(s && s.page ? s.page : `pages/shows.html#${s && s.key}`);
  CC.art = (s) => (s && s.art ? url(s.art) : "");
  CC.epImg = (e, show) => (e.image ? e.image : CC.art(show));
  CC.epHref = (e) => e.url || e.spotify_url || "#";
  // the episode's own page on this site when one is published, else its listen link
  CC.epLink = (e) => (e.page ? url(e.page) : CC.epHref(e));
  CC.isNew = (iso) => iso && Date.now() - new Date(iso).getTime() < 21 * 86400000;
  CC.showLinks = (s) => {
    const l = [];
    if (s.spotify_url) l.push(["Spotify", s.spotify_url]);
    if (s.apple_url) l.push(["Apple Podcasts", s.apple_url]);
    if (s.youtube_url) l.push(["YouTube", s.youtube_url]);
    return l;
  };

  const loadJSON = (p) => fetch(url(p), { cache: "no-cache" }).then((r) => (r.ok ? r.json() : null)).catch(() => null);
  CC.ready = Promise.all([loadJSON("data/content.json"), loadJSON("data/photos.json"), loadJSON("data/shows.json"), loadJSON("data/episode-pages.json"), loadJSON("data/show-pages.json")]).then(([content, photos, registry, epPages, showPages]) => {
    const data = content || { shows: [], episodes: [] };
    // published episode pages, keyed show:number:spotifyId (tools/build_episodes.py)
    const pageBy = {};
    Object.entries((epPages && epPages.pages) || {}).forEach(([k, path]) => {
      const [show, n, sid] = k.split(":");
      pageBy[`${show}:${n}:${sid}`] = { path, sid };
      pageBy[`${show}:${n}`] = pageBy[`${show}:${n}`] === undefined ? { path, sid } : null; // null = ambiguous number
    });
    (data.episodes || []).forEach((e) => {
      const m = /^\s*#\s*(\d+)/.exec(e.title || "");
      if (!m || e.kind === "short") return;
      const n = +m[1], sid = ((e.spotify_url || "").match(/episode\/([A-Za-z0-9]{22})/) || [])[1];
      const hit = (sid && pageBy[`${e.show}:${n}:${sid}`]) || pageBy[`${e.show}:${n}`];
      if (!hit) return;
      e.page = hit.path;
      e.spotify_url = e.spotify_url || `https://open.spotify.com/episode/${hit.sid}`;
    });
    // the registry is the roster: its edits apply immediately, a newly registered show appears
    // before its first refresh, and a show taken out of it disappears
    const regList = (registry && registry.shows) || [];
    const reg = Object.fromEntries(regList.map((s) => [s.key, s]));
    const fetched = Object.fromEntries((data.shows || []).map((s) => [s.key, s]));
    CC.categories = (registry && registry.categories) || {};
    data.shows = regList.length ? regList.map((r) => {
      const s = fetched[r.key] || { count: 0, spotify_url: r.spotify && `https://open.spotify.com/show/${r.spotify}` };
      return { ...s, key: r.key, kind: r.kind || s.kind, ai: r.ai || s.ai, tier: r.tier || s.tier || "primary", feature: r.feature ?? s.feature, flagship: r.flagship ?? s.flagship,
        name: r.name || s.name, short: r.short || s.short, tagline: r.tagline || s.tagline, about: r.about || s.about, hosts: r.hosts || s.hosts, principal: r.principal || s.principal,
        category: r.category, cadence: r.cadence, archive: r.archive ?? s.archive, spotify_url: s.spotify_url || r.spotify_url || (r.spotify && `https://open.spotify.com/show/${r.spotify}`) };
    }) : data.shows || [];
    const pagesOf = (showPages && showPages.pages) || {};
    data.shows.forEach((s) => { s.page = pagesOf[s.key]; });
    const live = new Set(data.shows.map((s) => s.key));
    data.episodes = (data.episodes || []).filter((e) => live.has(e.show));
    const allPhotos = (photos && photos.photos) || [];
    data.photos = allPhotos.some((p) => p.featured) ? allPhotos.filter((p) => p.featured) : allPhotos;
    data.byKey = Object.fromEntries((data.shows || []).map((x) => [x.key, x]));
    data.shows = SHOW_ORDER(data.shows || []);
    data.primary = data.shows.filter((x) => x.tier !== "secondary");
    data.secondary = data.shows.filter((x) => x.tier === "secondary");
    // counts quoted in copy come from the data, so they never go stale
    document.querySelectorAll("[data-show-count]").forEach((el) => { el.textContent = data.shows.length; });
    document.querySelectorAll("[data-show-episodes]").forEach((el) => { const n = (data.byKey[el.dataset.showEpisodes] || {}).count; if (n) el.textContent = n; });
    CC.isPrimary = (k) => (data.byKey[k] || {}).tier !== "secondary";
    CC.data = data;

    INDEX = [];
    PAGES.forEach((p) => addDoc({ type: "page", title: p.label, sub: "Page", text: p.words, href: url(p.href), boost: 0.5 }));
    data.shows.forEach((s) => addDoc({ type: "show", show: s.key, title: s.name, sub: `${s.kind === "youtube" ? "YouTube show" : "Podcast"} · ${(s.hosts || []).join(", ")}`, text: [s.tagline, s.about, s.description].filter(Boolean).join(" "), img: CC.art(s), href: CC.showHref(s), boost: 1 }));
    (data.episodes || []).forEach((e) => {
      const s = data.byKey[e.show] || {};
      addDoc({ type: "episode", show: e.show, title: e.title, sub: `${s.short || s.name || ""} · ${ago(e.date)}`, text: e.description || "", img: CC.epImg(e, s), href: CC.epLink(e), date: e.date });
    });
    data.photos.forEach((p) => addDoc({ type: "photo", title: p.alt || p.set, sub: `Photography · ${p.set}`, text: "photo photography " + p.set, img: url(p.thumb), href: url(`pages/studio.html#${p.id}`) }));

    const menu = document.querySelector('[data-nav-menu="shows"] .hdr__menu-list');
    // the flagships by name, then one entry per category of regular shows
    const catCount = {};
    data.secondary.forEach((s) => { const k = s.category || "more"; catCount[k] = (catCount[k] || 0) + 1; });
    if (menu) menu.innerHTML = data.primary.map((s) => `<a href="${CC.showHref(s)}" data-show="${s.key}">
      ${s.art ? `<img src="${CC.art(s)}" alt="" loading="lazy" width="44" height="44">` : '<span class="ph"></span>'}
      <span><b>${esc(s.name)}</b><small>${esc(CC.showByline(s) || s.tagline || "")}</small></span></a>`).join("")
      + Object.keys(catCount).sort((a, b) => Object.keys(CC.categories).indexOf(a) - Object.keys(CC.categories).indexOf(b)).map((k) => `<a href="${url(`pages/shows.html#cat-${k}`)}" class="hdr__menu-cat">
      <span class="ph">${catCount[k]}</span><span><b>${esc(CC.categories[k] || "More shows")}</b><small>${catCount[k]} shows on the network</small></span></a>`).join("");

    const ds = document.querySelector("[data-drawer-shows]");
    if (ds) ds.innerHTML = data.shows.map((s) => `<a href="${CC.showHref(s)}" data-show="${s.key}">${s.art ? `<img src="${CC.art(s)}" alt="" loading="lazy">` : '<span class="ph"></span>'}${esc(s.name)}</a>`).join("");
    if (input.value) runSearch();
    const qp = new URLSearchParams(location.search).get("q");
    if (qp && page !== "archive") CC.openSearch(qp);
    return data;
  });


  /* ---------------- the network: a solar system that lays itself out ----------------
     The network is the sun. Joshua, Janel, and AI orbit closest. The flagships ride the upper
     orbit beside whoever makes them; every regular show is a moon of its category's planet in
     the lower half, and one open planet waits for the next show someone asks for. Nothing is
     hand-placed: a new show or category takes its slot on the next refresh. */
  CC.network = (data) => {
    const W = 1000, H = 1000, C = [500, 470];
    const rad = (d) => (d * Math.PI) / 180;
    const at = (r, deg, o = C) => [Math.round(o[0] + r * Math.cos(rad(deg))), Math.round(o[1] + r * Math.sin(rad(deg)))];
    const line = (p, q, cls, key) => `<line class="web__edge ${cls}" data-edge="${key}" x1="${p[0]}" y1="${p[1]}" x2="${q[0]}" y2="${q[1]}"/>`;
    const text = (x, y, cls, t) => `<text class="${cls}" x="${x}" y="${y}">${esc(t)}</text>`;
    const initials = (s) => (s.short || s.name).replace(/^The /, "").split(/\s+/).map((w) => w[0]).join("").slice(0, 2);
    const disc = (id, x, y, r, s, hybrid) => `<clipPath id="${id}"><circle cx="${x}" cy="${y}" r="${r}"/></clipPath><circle class="web__ring" cx="${x}" cy="${y}" r="${r + (r > 20 ? 4 : 2)}"/>${hybrid ? `<path class="web__ring-ai" d="M${x} ${y - r - 4}A${r + 4} ${r + 4} 0 0 1 ${x} ${y + r + 4}"/>` : ""}`
      + (s && s.art ? `<image href="${esc(url(s.art))}" x="${x - r}" y="${y - r}" width="${r * 2}" height="${r * 2}" clip-path="url(#${id})" preserveAspectRatio="xMidYMid slice"/>`
        : `<circle cx="${x}" cy="${y}" r="${r}" class="web__noart"/>${s ? `<text class="web__initials" x="${x}" y="${y + r * 0.22}" style="font-size:${Math.round(r * 0.62)}px">${esc(initials(s))}</text>` : ""}`);
    const soon = (s) => !s.archive && !s.count && s.kind !== "youtube";

    // makers on the inner orbit
    const makers = { joshua: [...at(150, 200), "Joshua", "assets/people/joshua.jpg"], janel: [...at(150, 340), "Janel", "assets/people/janel.jpg"], ai: [...at(165, 90), "AI-generated"] };

    // flagships across the upper orbit: Joshua's on the left, the shared flagship at the top, Janel's on the right
    const flag = data.shows.filter((s) => s.tier !== "secondary");
    const side = (s) => { const g = CC.hostGroup(s); return g === "shared" ? 1 : g === "janel" ? 2 : 0; };
    const left = flag.filter((s) => side(s) === 0), top = flag.filter((s) => side(s) === 1), right = flag.filter((s) => side(s) === 2);
    const spread = (list, from, to) => list.map((s, i) => ({ s, deg: list.length === 1 ? (from + to) / 2 : from + ((to - from) * i) / (list.length - 1) }));
    const topSpan = top.length > 1 ? 24 * (top.length - 1) : 0;
    const fnodes = [...spread(left, 190, 270 - topSpan / 2 - 34), ...spread(top, 270 - topSpan / 2, 270 + topSpan / 2), ...spread(right, 270 + topSpan / 2 + 34, 345)];
    // the shared flagship sits highest with its label above it, clear of its neighbours' labels below theirs
    fnodes.forEach((n, i) => { n.r = n.s.flagship ? 54 : 40; n.above = side(n.s) === 1; [n.x, n.y] = at(n.above ? 268 : i % 2 ? 330 : 300, n.deg); });

    // regular shows: one planet per category, its shows as moons, plus an open planet for requests
    const regular = data.shows.filter((s) => s.tier === "secondary");
    const cats = [...new Set(regular.map((s) => s.category || "more"))];
    cats.sort((a, b) => Object.keys(CC.categories).indexOf(a) - Object.keys(CC.categories).indexOf(b));
    const planets = cats.map((k) => ({ k, shows: regular.filter((s) => (s.category || "more") === k) }));
    planets.forEach((p, i) => {
      p.deg = planets.length === 1 ? 90 : 30 + (120 * i) / (planets.length - 1);
      [p.x, p.y] = at(345, p.deg);
      p.ring = Math.max(62, Math.min(92, p.shows.length * 8.5));
      p.label = p.k === "open" ? "Coming soon" : CC.categories[p.k] || p.k;
      p.moons = p.shows.map((s, j) => { const [x, y] = at(p.ring, -90 + (360 * j) / p.shows.length, [p.x, p.y]); return { s, x, y }; });
    });

    const orbits = [150, 310].map((r) => `<circle class="web__orbit" cx="${C[0]}" cy="${C[1]}" r="${r}"/>`).join("")
      + planets.map((p) => `<circle class="web__orbit web__orbit--moon" cx="${p.x}" cy="${p.y}" r="${p.ring}"/>`).join("");
    const stars = Array.from({ length: 60 }, (_, i) => { const [x, y] = at(40 + ((i * 97) % 470), (i * 137.508) % 360); return `<circle class="web__star" cx="${x}" cy="${y}" r="${1 + (i % 3) * 0.6}"/>`; }).join("");

    let edges = Object.entries(makers).map(([k, m]) => line(C, m, `web__edge--core${k === "ai" ? " web__edge--ai" : ""}`, k)).join("");
    const flagLinks = (s) => { const g = CC.hostGroup(s); return g === "shared" ? ["joshua", "janel"] : g === "hybrid" ? ["joshua", "ai"] : g === "ai" ? ["ai"] : [g]; };
    fnodes.forEach((n) => flagLinks(n.s).forEach((k) => { edges += line(makers[k], [n.x, n.y], `web__edge--primary${k === "ai" ? (CC.isHybrid(n.s) ? " web__edge--hybrid" : " web__edge--ai") : ""}`, `${k} ${n.s.key}`); }));
    planets.forEach((p) => { edges += line(makers.ai, [p.x, p.y], "web__edge--ai", `ai cat-${p.k}`); });
    // the open seat for the next show someone asks for, out in the free corner
    const open = [C[0] + 400, C[1] - 250];
    edges += line(C, open, "web__edge--future", "future");

    const flagNodes = fnodes.map((n, i) => {
      const s = n.s, hybrid = CC.isHybrid(s), tag = hybrid ? "hybrid · human + AI" : soon(s) ? "coming soon" : s.archive ? "archive" : "";
      // left-hand flagships label to their left, so stacked neighbours don't collide; the rest label below (or above, for the top one)
      const name = s.flagship ? "The Curious & Creative Podcast" : s.short || s.name;
      const beside = !n.above && n.x < C[0] - 60 && n.x - n.r - 12 - name.length * 13 > 8; // only if it fits at phone label size
      const ly = n.above ? n.y - n.r - (tag ? 30 : 14) : beside ? n.y + (tag ? -2 : 6) : n.y + n.r + 22;
      const lx = beside ? n.x - n.r - 12 : n.x;
      return `<a class="web__node web__node--primary${hybrid ? " web__node--hybrid" : ""}" href="${CC.showHref(s)}" data-show="${s.key}" data-node="${s.key}" data-links="${flagLinks(s).join(" ")}" aria-label="${esc(s.name)}">`
        + disc("wf" + i, n.x, n.y, n.r, s, hybrid) + text(lx, ly, `web__label${beside ? " web__label--end" : ""}`, name)
        + (tag ? text(lx, ly + 18, `web__tag${hybrid ? " web__tag--hybrid" : ""}${beside ? " web__label--end" : ""}`, tag) : "") + "</a>";
    }).join("");
    const openNode = `<a class="web__node web__node--future web__planet" href="${url("pages/manifesto.html#request")}" data-node="open" aria-label="Coming soon: ask us for a show"><circle cx="${open[0]}" cy="${open[1]}" r="30"/>${text(open[0], open[1] + 9, "web__plus", "?")}${text(open[0], open[1] + 56, "web__label web__label--quiet", "Coming soon")}${text(open[0], open[1] + 74, "web__tag", "ask us for a show")}</a>`;
    const planetNodes = planets.map((p, i) => {
      const moons = p.moons.map((m, j) => `<a class="web__node web__moon" href="${CC.showHref(m.s)}" data-show="${m.s.key}" data-node="${m.s.key}" data-links="cat-${p.k}" aria-label="${esc(m.s.name)}"><title>${esc(m.s.name)}</title>${disc(`wm${i}-${j}`, m.x, m.y, 15, m.s)}</a>`).join("");
      return `<g class="web__system" data-cat="${p.k}">${moons}<a class="web__node web__planet" href="${url(`pages/shows.html#cat-${p.k}`)}" data-node="cat-${p.k}" data-links="ai" aria-label="${esc(p.label)}: ${p.shows.length} shows"><circle class="web__planet-body" cx="${p.x}" cy="${p.y}" r="30"/>${text(p.x, p.y + 6, "web__planet-n", String(p.shows.length))}</a>${text(p.x, p.y + p.ring + 30, "web__label", p.label)}</g>`;
    }).join("");
    const makerNodes = Object.entries(makers).map(([k, [x, y, name, src]]) => (k === "ai"
      ? `<g class="web__node web__node--ai" data-node="ai" tabindex="0" aria-label="AI-generated"><circle cx="${x}" cy="${y}" r="34"/><path transform="translate(${x} ${y}) scale(.85)" d="M0-22 5-5 22 0 5 5 0 22-5 5-22 0-5-5Z"/>${text(x, y - 46, "web__label", name)}</g>`
      : `<a class="web__node web__node--host" href="${url("pages/about.html")}" data-node="${k}" aria-label="${name}"><clipPath id="wp${k}"><circle cx="${x}" cy="${y}" r="34"/></clipPath><circle class="web__ring" cx="${x}" cy="${y}" r="38"/><image href="${esc(url(src))}" x="${x - 34}" y="${y - 34}" width="68" height="68" clip-path="url(#wp${k})" preserveAspectRatio="xMidYMid slice"/>${text(x, y + 56, "web__label", name)}</a>`)).join("");
    const hub = `<g class="web__hub"><clipPath id="whub"><circle cx="${C[0]}" cy="${C[1]}" r="58"/></clipPath><circle class="web__hub-glow" cx="${C[0]}" cy="${C[1]}" r="86"/><circle class="web__hub-ring" cx="${C[0]}" cy="${C[1]}" r="63"/><image href="${esc(url("assets/brand/cc-logo.jpg"))}" x="${C[0] - 58}" y="${C[1] - 58}" width="116" height="116" clip-path="url(#whub)" preserveAspectRatio="xMidYMid slice"/></g>`;
    return `<svg class="web web--orbit" viewBox="0 0 ${W} ${H}" role="img" aria-label="The Curious + Creative Network: ${data.shows.length} shows. Flagships orbit Joshua and Janel; ${regular.length} regular shows orbit their categories.">${stars}${orbits}${edges}${makerNodes}${planetNodes}${openNode}${flagNodes}${hub}</svg>`;
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
    // moons are too small to label; name the one under the pointer (or keyboard focus)
    const tip = document.createElementNS("http://www.w3.org/2000/svg", "text");
    tip.setAttribute("class", "web__label web__tip");
    svg.appendChild(tip);
    const name = (n) => {
      const c = n.classList.contains("web__moon") && n.querySelector("circle:not(.web__ring)");
      if (!c) { tip.textContent = ""; return; }
      tip.textContent = n.getAttribute("aria-label");
      tip.setAttribute("x", c.getAttribute("cx"));
      tip.setAttribute("y", +c.getAttribute("cy") - 24);
    };
    svg.querySelectorAll("[data-node]").forEach((n) => {
      n.addEventListener("mouseenter", () => { focus(n.dataset.node); name(n); });
      n.addEventListener("focus", () => { focus(n.dataset.node); name(n); });
      n.addEventListener("mouseleave", () => { focus(null); tip.textContent = ""; });
      n.addEventListener("blur", () => { focus(null); tip.textContent = ""; });
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
