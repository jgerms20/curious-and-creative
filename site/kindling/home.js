/* Kindling landing page: hero box + fan, draw-a-card, pillars, decks, pot calculator. */
(() => {
  const K = window.K, esc = window.CC.esc;
  const $ = (s) => document.querySelector(s);

  // wordmark in the hero
  const w = $("[data-k-word]");
  if (w) w.outerHTML = K.word();

  // 3D box
  const boxSlot = $("[data-hero-box]");
  boxSlot.innerHTML = K.boxHTML("embers");
  K.tilt(boxSlot.querySelector(".kbox"));

  K.data.then(() => {
    const pickText = (start) => K.cards.find((c) => c.text.startsWith(start));

    // hero fan: three hand-picked favorites
    const fan = [
      pickText("What makes you feel wanted"),
      pickText("Perform a slow, sultry striptease of exactly one sock"),
      pickText("Read aloud to them while they're in the bath"),
    ].filter(Boolean);
    $("[data-hero-fan]").innerHTML = fan.map((c) => K.cardHTML(c)).join("");

    /* ---------- draw a card ---------- */
    const state = { heat: 3, decks: new Set(["embers", "wildfire", "slowburn"]), last: null };
    const heatBtns = $("[data-heat-buttons]");
    heatBtns.innerHTML = [1, 2, 3, 4, 5].map((h) => `<button class="k-heat__btn" type="button" data-h="${h}" aria-pressed="${h === state.heat}">${K.flame()}${h} · ${K.HEAT[h].name}</button>`).join("");
    const chips = $("[data-deck-chips]");
    chips.innerHTML = K.decks.map((d) => `<button class="k-chip" type="button" data-deck="${d.id}" data-d="${d.id}" aria-pressed="${state.decks.has(d.id)}"><i></i>${esc(d.name)}${d.adult ? " · 18+" : ""}</button>`).join("");
    const desc = $("[data-heat-desc]");
    const flipIn = $("[data-draw-in]"), flip = $("[data-draw-flip]");

    const pool = () => K.cards.filter((c) => c.heat === state.heat && state.decks.has(c.deck) && c.type !== "wild");
    const draw = () => {
      let p = pool();
      if (!p.length) p = K.cards.filter((c) => c.heat === state.heat && c.type !== "wild");
      if (!p.length) p = K.cards.filter((c) => c.heat <= state.heat && c.type !== "wild");
      let c = K.pick(p);
      if (p.length > 1) while (c === state.last) c = K.pick(p);
      state.last = c;
      flip.classList.add("is-down");
      setTimeout(() => {
        flipIn.innerHTML = K.cardHTML(c) + K.backHTML(c.deck);
        requestAnimationFrame(() => flip.classList.remove("is-down"));
      }, flipIn.innerHTML ? 380 : 0);
    };
    const paint = () => {
      heatBtns.querySelectorAll("button").forEach((b) => b.setAttribute("aria-pressed", String(+b.dataset.h === state.heat)));
      chips.querySelectorAll("button").forEach((b) => b.setAttribute("aria-pressed", String(state.decks.has(b.dataset.d))));
      desc.textContent = `${K.HEAT[state.heat].name}: ${K.HEAT[state.heat].desc}`;
    };
    heatBtns.addEventListener("click", (e) => {
      const b = e.target.closest("button"); if (!b) return;
      state.heat = +b.dataset.h; paint(); draw();
    });
    chips.addEventListener("click", (e) => {
      const b = e.target.closest("button"); if (!b) return;
      const id = b.dataset.d;
      if (state.decks.has(id)) { if (state.decks.size > 1) state.decks.delete(id); }
      else {
        if (id === "afterdark" && !K.confirmAdult()) return;
        state.decks.add(id);
      }
      if (id === "afterdark" && state.decks.has(id) && state.heat < 3) state.heat = 3;
      paint(); draw();
    });
    $("[data-draw]").addEventListener("click", draw);
    paint();
    const first = pickText("Kiss them somewhere you've never deliberately kissed") || K.cards[0];
    state.last = first;
    flipIn.innerHTML = K.cardHTML(first) + K.backHTML(first.deck);

    /* ---------- pillars ---------- */
    const pillars = [
      { n: "i.", t: "Talk", p: "Questions and confessions, from \"what's your weird useless skill\" to \"what have you never forgiven me for.\"", q: pickText("What makes you feel wanted") },
      { n: "ii.", t: "Touch", p: "Specific, named, consensual touch. A hand on their back that stays until the next card is done.", q: pickText("Slide one hand under their shirt") },
      { n: "iii.", t: "Play", p: "Silly and flirty, the kind of cards that make you laugh and blush at the same time.", q: pickText("Hot or Cold") },
      { n: "iv.", t: "Explore", p: "Dates, rituals, challenges, and an 18+ pack for kink, power, and roleplay without judgment.", q: pickText("Bathe them and wash their hair") },
    ];
    $("[data-pillars]").innerHTML = pillars.map((x) => `<article class="k-pillar"><span class="k-pillar__n">${x.n}</span><h3>${x.t}</h3><p>${x.p}</p>${x.q ? `<q>${esc(x.q.text)}</q>` : ""}</article>`).join("");

    /* ---------- decks ---------- */
    K.shop.then((shop) => {
      const sampleFor = (deck) => {
        const want = { embers: [1, 3, 5], wildfire: [2, 4, 5], slowburn: [1, 3, 4], afterdark: [3, 4, 5] }[deck];
        return want.map((h) => K.cards.find((c) => c.deck === deck && c.heat === h && c.type !== "wild" && c.text.length < 90) || K.cards.find((c) => c.deck === deck));
      };
      $("[data-decks]").innerHTML = K.decks.map((d) => {
        const p = shop.products.find((x) => x.id === d.id) || {};
        return `<article class="k-deck" data-deck="${d.id}">
          <div class="k-deck__art">${sampleFor(d.id).map((c) => K.cardHTML(c)).join("")}</div>
          <div class="k-deck__body">
            <span class="k-deck__kind">${esc(d.kind)}${d.adult ? " · 18+" : ""}</span>
            <h3>${esc(d.name)}</h3>
            <p>${esc(d.blurb)}</p>
            <div class="k-deck__foot"><span class="k-deck__price">${K.money(p.price || 0)}<small>${d.count} cards</small></span><a class="btn btn--flame btn--sm" href="shop.html#${d.id}">Shop</a></div>
          </div>
        </article>`;
      }).join("");
    });
  });

  /* ---------- pot calculator ---------- */
  const range = $("[data-pot-range]"), players = $("[data-pot-players]");
  const ideas = [
    [0, "Enough for a very good dinner, a bottle you'd normally skip, and dessert somewhere else."],
    [150, "A night in a hotel across town, plus room service at midnight."],
    [300, "A couples massage, a pole class for two, or a weekend cabin with no signal."],
    [500, "A long weekend away. Somewhere with a bathtub big enough for the Slow Burn deck."],
    [900, "A flight. Pick the city from the Wildfire card you never got around to."],
  ];
  const paintPot = () => {
    const each = +range.value, n = +players.value, total = each * n;
    $("[data-pot-each]").textContent = `${K.money(each)} · ${n} players`;
    $("[data-pot-total]").textContent = K.money(total);
    $("[data-pot-ideas]").textContent = ideas.filter(([min]) => total >= min).pop()[1];
  };
  range.addEventListener("input", paintPot);
  players.addEventListener("input", paintPot);
  paintPot();
})();
