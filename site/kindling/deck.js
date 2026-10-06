/* Inside the box: box lineup, card backs, filterable gallery.
   Print mode (used by scripts/kindling_print.mjs to make PDFs):
     deck.html?layout=letter&deck=embers         3×3 fronts + mirrored backs on US Letter, crop marks
     deck.html?layout=press&deck=embers&side=front   one 69×94 mm page per card (3 mm bleed)
     deck.html?layout=press&deck=all&side=back       one back per deck                      */
(() => {
  const K = window.K, esc = window.CC.esc;
  const $ = (s) => document.querySelector(s);
  const qs = new URLSearchParams(location.search);
  const layout = qs.get("layout");

  K.data.then(() => (layout ? printMode() : screenMode()));

  /* ---------------- print ---------------- */
  function printMode() {
    $("[data-screen]").remove();
    const want = qs.get("deck") || "all";
    const decks = want === "all" ? K.decks.map((d) => d.id) : want.split(",");
    const cardsFor = (d) => K.cards.filter((c) => c.deck === d);
    const out = $("[data-print]");
    let html = "";

    if (layout === "press") {
      if (qs.get("side") === "back") {
        html = decks.concat(qs.get("rules") === "0" ? [] : ["rules"]).map((d) => `<section class="kpr-page kpr-press">${K.backHTML(d)}</section>`).join("");
      } else {
        const list = (qs.get("rules") === "1" ? K.rules : []).concat(decks.flatMap(cardsFor));
        html = list.map((c) => `<section class="kpr-page kpr-press">${K.cardHTML(c)}</section>`).join("");
      }
    } else {
      const list = (qs.get("rules") === "0" ? [] : K.rules).concat(decks.flatMap(cardsFor));
      const pages = [];
      for (let i = 0; i < list.length; i += 9) pages.push(list.slice(i, i + 9));
      const crops = () => {
        let m = "";
        for (let x = 0; x <= 3; x++) m += `<i class="v" style="left:calc(5mm + ${x * 63}mm);top:0"></i><i class="v" style="left:calc(5mm + ${x * 63}mm);bottom:0"></i>`;
        for (let y = 0; y <= 3; y++) m += `<i class="h" style="top:calc(5mm + ${y * 88}mm);left:0"></i><i class="h" style="top:calc(5mm + ${y * 88}mm);right:0"></i>`;
        return `<div class="kpr-crop" style="inset:-5mm -5mm">${m}</div>`;
      };
      const name = want === "all" ? "All decks" : decks.map((d) => K.deckById[d].name).join(" + ");
      pages.forEach((pg, n) => {
        html += `<section class="kpr-page kpr-letter"><div class="kpr-grid">${crops()}${pg.map((c) => `<div class="kpr-cell">${K.cardHTML(c)}</div>`).join("")}</div><p class="kpr-label">Kindling prototype · ${esc(name)} · sheet ${n + 1}/${pages.length} · fronts · print at 100%, duplex, flip on long edge</p></section>`;
        // backs, mirrored per row so they line up with a long-edge duplex flip
        const rows = [];
        for (let r = 0; r < 3; r++) rows.push(pg.slice(r * 3, r * 3 + 3));
        const backs = rows.flatMap((row) => {
          if (!row.length) return [];
          const cells = [row[0], row[1], row[2]].map((c) => (c ? K.backHTML(c.deck) : "<span></span>"));
          return cells.reverse().map((h) => `<div class="kpr-cell">${h}</div>`);
        });
        html += `<section class="kpr-page kpr-letter"><div class="kpr-grid">${crops()}${backs.join("")}</div><p class="kpr-label">Kindling prototype · ${esc(name)} · sheet ${n + 1}/${pages.length} · backs</p></section>`;
      });
    }
    out.innerHTML = html;
    document.fonts.ready.then(() => { document.documentElement.dataset.ready = "1"; });
  }

  /* ---------------- screen ---------------- */
  function screenMode() {
    const lineup = $("[data-lineup]");
    const boxMeta = { embers: ["150 cards", "2+ players", "Heat 1–5"], wildfire: ["60 cards", "Challenges", "Heat 1–5"], slowburn: ["60 cards", "Dates & rituals", "Heat 1–5"], afterdark: ["60 cards", "18+", "Heat 3–5"] };
    lineup.innerHTML = K.decks.map((d) => K.boxHTML(d.id, {
      title: d.id === "embers" ? "kindling" : d.name.toLowerCase(),
      sub: d.id === "embers" ? "The core deck." : d.kind + ".",
      meta: boxMeta[d.id],
    })).join("");
    lineup.querySelectorAll(".kbox").forEach((b, i) => K.tilt(b, { x: -8, y: -22 + i * 6 }));
    $("[data-backs]").innerHTML = K.decks.map((d) => K.backHTML(d.id)).join("") + K.backHTML("rules");

    const f = { decks: new Set(["embers", "wildfire", "slowburn"]), heat: 0, q: "", limit: 48 };
    const deckRow = $("[data-f-decks]"), heatRow = $("[data-f-heat]");
    const paintFilters = () => {
      deckRow.innerHTML = K.decks.map((d) => `<button class="k-chip" type="button" data-fd="${d.id}" data-deck="${d.id}" aria-pressed="${f.decks.has(d.id)}"><i></i>${esc(d.name)} · ${d.count}${d.adult ? " · 18+" : ""}</button>`).join("")
        + `<button class="k-chip" type="button" data-fd="rules" data-deck="rules" aria-pressed="${f.decks.has("rules")}"><i></i>Rules · 4</button>`;
      heatRow.innerHTML = [0, 1, 2, 3, 4, 5].map((h) => `<button class="k-heat__btn" type="button" data-fh="${h}" aria-pressed="${f.heat === h}">${h ? `${K.flame()}${h} · ${K.HEAT[h].name}` : "Any heat"}</button>`).join("");
    };
    const grid = $("[data-grid]"), more = $("[data-more]"), count = $("[data-f-count]");
    const paintGrid = () => {
      const q = f.q.trim().toLowerCase();
      let list = K.cards.filter((c) => f.decks.has(c.deck) && (!f.heat || c.heat === f.heat) && (!q || (c.text + " " + c.label + " " + (c.aftercare || "")).toLowerCase().includes(q)));
      if (f.decks.has("rules") && !f.heat && (!q || K.rules.some((r) => r.html.toLowerCase().includes(q)))) list = K.rules.concat(list);
      count.textContent = `${list.length} card${list.length === 1 ? "" : "s"}`;
      grid.innerHTML = list.slice(0, f.limit).map((c) => K.cardHTML(c)).join("") || `<p class="k-sec__lede" style="grid-column:1/-1">No cards match that. Try another word, or turn on another deck.</p>`;
      more.hidden = list.length <= f.limit;
    };
    deckRow.addEventListener("click", (e) => {
      const b = e.target.closest("[data-fd]"); if (!b) return;
      const id = b.dataset.fd;
      if (f.decks.has(id)) f.decks.delete(id);
      else { if ((K.deckById[id] || {}).adult && !K.confirmAdult()) return; f.decks.add(id); }
      f.limit = 48; paintFilters(); paintGrid();
    });
    heatRow.addEventListener("click", (e) => { const b = e.target.closest("[data-fh]"); if (!b) return; f.heat = +b.dataset.fh; f.limit = 48; paintFilters(); paintGrid(); });
    $("[data-f-q]").addEventListener("input", (e) => { f.q = e.target.value; f.limit = 48; paintGrid(); });
    more.addEventListener("click", () => { f.limit += 48; paintGrid(); });
    paintFilters(); paintGrid();
  }
})();
