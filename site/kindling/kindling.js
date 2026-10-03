/* Kindling — shared runtime for /kindling/ pages (after js/cc.js).
   Loads data/kindling-cards.json + data/kindling-shop.json, renders cards,
   keeps the cart in localStorage, and mounts the Kindling sub-nav. */
(() => {
  const CC = window.CC || { root: "../", esc: (s) => String(s ?? "") };
  const esc = CC.esc;
  const root = CC.root;
  const K = (window.K = {});

  /* ---------- marks ---------- */
  K.mark = (cls = "") => `<svg class="k-mark ${cls}" viewBox="0 0 64 64" aria-hidden="true"><path class="l" d="M29 61C15 59 8 48 11 37c2.4-8.6 9.6-12.4 10-24.5 7.6 6.3 12.5 15 11 25-1 6.7-4.2 12.4-3 23.5z"/><path class="r" d="M35 61c13.2-1.6 19.6-11.5 17.6-21.5-1.6-7.8-7.3-10.8-7.6-19.5-6.2 5-10.2 12.3-9.7 20.2.4 6.6 3.4 11 -.3 20.8z"/><path class="core" d="M32 61c-4.6-2-6.4-6.6-5.2-10.8 1-3.4 3.7-5 4.2-9.2 3.1 2.7 5.4 6.2 5 10.4-.3 3.6-1.9 6.4-4 9.6z"/></svg>`;
  K.word = (text = "kindling") => `<span class="k-word">${K.mark()}<span>${text}</span></span>`;
  const FLAME = '<path d="M12 2.5c.6 3.2 3 4.9 4.6 7.2A7 7 0 1 1 5.6 12c.5-2 1.7-3.3 2.6-4.6.3 1.5 1 2.6 2.1 3.1-.4-2.9.2-5.6 1.7-8z"/>';
  K.flame = (on = true) => `<svg viewBox="0 0 24 24" class="${on ? "on" : ""}" aria-hidden="true">${FLAME}</svg>`;
  K.flames = (n) => Array.from({ length: 5 }, (_, i) => K.flame(i < n)).join("");
  const LINK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" aria-hidden="true"><circle cx="8.5" cy="12" r="5"/><circle cx="15.5" cy="12" r="5"/></svg>';

  K.HEAT = [
    null,
    { name: "Spark", desc: "Sweet and safe. First dates, old friends, a Tuesday." },
    { name: "Glow", desc: "Warm. A little vulnerable, a little flirty." },
    { name: "Flame", desc: "Real vulnerability, real kissing, a little less clothing." },
    { name: "Blaze", desc: "Clearly sexy, or deeply raw. Sometimes both." },
    { name: "Inferno", desc: "The boldest cards in the box. Only if everyone's in." },
  ];

  /* ---------- data ---------- */
  const get = (p) => fetch(root + p, { cache: "no-cache" }).then((r) => { if (!r.ok) throw new Error(p); return r.json(); });
  K.data = get("data/kindling-cards.json").then((d) => {
    K.cards = d.cards; K.rules = d.rules; K.decks = d.decks;
    K.deckById = Object.fromEntries(d.decks.map((x) => [x.id, x]));
    return d;
  });
  K.shop = get("data/kindling-shop.json").then((s) => { K.shopData = s; K.productById = Object.fromEntries(s.products.map((p) => [p.id, p])); return s; });

  /* ---------- card rendering ---------- */
  const deckName = (id) => (K.deckById && K.deckById[id] ? K.deckById[id].name : id);
  const sizeClass = (t) => (t.length > 150 ? "is-xlong" : t.length > 95 ? "is-long" : "");

  K.cardHTML = (c, opts = {}) => {
    if (c.deck === "rules") {
      return `<article class="kcard" data-deck="rules" data-id="${c.id}">
        <header class="kcard__top"><span class="kcard__type">Rules · ${c.id.slice(1)}/4</span></header>
        <div class="kcard__text">${c.html}</div>
        <footer class="kcard__foot"><span class="kcard__time"></span><span class="kcard__deck">${K.mark()}kindling</span><span></span></footer>
      </article>`;
    }
    const badge = c.match
      ? `<span class="kcard__badge">${LINK}Match</span>`
      : c.players === "3+" ? `<span class="kcard__badge kcard__badge--group">3+ players</span>` : "";
    const care = c.aftercare ? `<p class="kcard__care"><b>Aftercare</b>${esc(c.aftercare)}</p>` : "";
    const sparks = c.type === "wild" ? "★" : `+${c.sparks}`;
    const sparks2 = opts.double && c.type !== "wild" ? `+${c.sparks * 2}` : sparks;
    return `<article class="kcard" data-deck="${c.deck}" data-id="${c.id}" aria-label="${esc(c.label)} card, heat ${c.heat}: ${esc(c.text)}">
      <header class="kcard__top"><span class="kcard__type">${esc(c.label)}</span>${c.type === "wild" ? "" : `<span class="kcard__heat" title="Heat ${c.heat}: ${K.HEAT[c.heat].name}">${K.flames(c.heat)}</span>`}</header>
      ${badge}
      <p class="kcard__text ${sizeClass(c.text)}">${esc(c.text)}</p>
      ${care}
      <footer class="kcard__foot"><span class="kcard__time">${esc(c.time || (c.type === "wild" ? "Wild" : ""))}</span><span class="kcard__deck">${K.mark()}${esc(deckName(c.deck).toLowerCase())}</span><span class="kcard__sparks" title="Sparks">${sparks2}</span></footer>
    </article>`;
  };

  K.backHTML = (deck) => {
    const d = K.deckById && K.deckById[deck];
    const tag = deck === "afterdark" ? "18+ · after dark" : deck === "rules" ? "how to play" : d ? d.kind : "";
    return `<article class="kcard kcard--back" data-deck="${deck}" aria-hidden="true">
      <span class="kcard__backtag">${esc(tag)}</span>
      ${K.word()}
      <span class="kcard__backdeck">${esc(deck === "rules" ? "Rules" : deckName(deck))}</span>
    </article>`;
  };

  K.boxHTML = (deck = "embers", { title = "kindling", sub = "A card game for people who want more of each other.", meta = ["150 cards", "2+ players", "Heat 1–5"] } = {}) => `
    <div class="kbox" data-deck="${deck}">
      <div class="kbox__in">
        <div class="kbox__glow"></div>
        <div class="kbox__face kbox__back"></div>
        <div class="kbox__face kbox__lside"></div>
        <div class="kbox__face kbox__bottom"></div>
        <div class="kbox__face kbox__top"></div>
        <div class="kbox__face kbox__side"><span>${K.mark()}kindling</span></div>
        <div class="kbox__face kbox__front">
          <div class="kbox__tag"><span>Curious &amp; Creative</span><span>${deck === "afterdark" ? "18+" : "No. 01"}</span></div>
          <div class="kbox__title">${K.word(title)}</div>
          <p class="kbox__sub">${sub}</p>
          <div class="kbox__meta">${meta.map((m) => `<span>${m}</span>`).join("")}</div>
        </div>
      </div>
    </div>`;

  /* tilt a box toward the pointer */
  K.tilt = (el, base = { x: -9, y: -30 }) => {
    const inner = el.querySelector(".kbox__in");
    if (!inner || matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    const zone = el.closest("[data-tilt-zone]") || el;
    zone.addEventListener("pointermove", (e) => {
      const r = zone.getBoundingClientRect();
      const px = (e.clientX - r.left) / r.width - 0.5, py = (e.clientY - r.top) / r.height - 0.5;
      inner.style.setProperty("--ry", `${base.y + px * 30}deg`);
      inner.style.setProperty("--rx", `${base.x - py * 14}deg`);
    });
    zone.addEventListener("pointerleave", () => { inner.style.removeProperty("--ry"); inner.style.removeProperty("--rx"); });
  };

  /* ---------- random helpers ---------- */
  K.shuffle = (arr) => { const a = arr.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
  K.pick = (arr) => arr[Math.floor(Math.random() * arr.length)];

  /* ---------- storage (per-viewer convenience only) ---------- */
  K.store = {
    get(k, d) { try { const v = localStorage.getItem(k); return v ? JSON.parse(v) : d; } catch (e) { return d; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { /* storage blocked */ } },
    del(k) { try { localStorage.removeItem(k); } catch (e) { /* storage blocked */ } },
  };

  /* ---------- cart ---------- */
  const CART = "kindling-cart";
  K.cart = {
    items() { return K.store.get(CART, {}); },
    count() { return Object.values(this.items()).reduce((a, b) => a + b, 0); },
    set(id, qty) { const it = this.items(); if (qty > 0) it[id] = Math.min(qty, 20); else delete it[id]; K.store.set(CART, it); document.dispatchEvent(new CustomEvent("kindling:cart")); },
    add(id, n = 1) { this.set(id, (this.items()[id] || 0) + n); },
    clear() { K.store.del(CART); document.dispatchEvent(new CustomEvent("kindling:cart")); },
  };
  K.money = (n) => `$${Number(n).toFixed(Number(n) % 1 ? 2 : 0)}`;

  /* ---------- toast ---------- */
  let toastT;
  K.toast = (html) => {
    let t = document.querySelector(".k-toast");
    if (!t) { t = document.createElement("div"); t.className = "k-toast"; t.setAttribute("role", "status"); document.body.appendChild(t); }
    t.innerHTML = html;
    requestAnimationFrame(() => t.classList.add("is-on"));
    clearTimeout(toastT);
    toastT = setTimeout(() => t.classList.remove("is-on"), 3200);
  };

  /* age confirmation for 18+ products and the After Dark deck */
  K.isAdult = () => K.store.get("kindling-18", false) === true;
  K.confirmAdult = () => {
    if (K.isAdult()) return true;
    const ok = window.confirm("After Dark is an 18+ expansion with kink and adult content.\n\nAre you 18 or older?");
    if (ok) K.store.set("kindling-18", true);
    return ok;
  };

  /* ---------- sub-nav ---------- */
  const here = document.body.dataset.kpage || "";
  const nav = document.querySelector("[data-k-nav]");
  if (nav) {
    const link = (href, label, id) => `<a href="${href}"${here === id ? ' aria-current="page"' : ""}>${label}</a>`;
    nav.className = "k-nav";
    nav.setAttribute("aria-label", "Kindling");
    nav.innerHTML = `<a class="k-nav__brand" href="./">${K.word()}</a>
      ${link("./", "The game", "home")}${link("play.html", "Play free", "play")}${link("shop.html", "Shop", "shop")}${link("deck.html", "Inside the box", "deck")}
      <a class="k-nav__cart" href="shop.html#cart">Cart <b data-cart-count>0</b></a>`;
  }
  const paintCount = () => document.querySelectorAll("[data-cart-count]").forEach((el) => { el.textContent = K.cart.count(); });
  document.addEventListener("kindling:cart", paintCount);
  paintCount();
})();
