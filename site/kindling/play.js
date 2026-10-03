/* Kindling — the digital table. Pass-the-phone play for 2–8 players.
   State lives in localStorage ("kindling-game") so a game survives a refresh. */
(() => {
  const K = window.K, esc = window.CC.esc;
  const el = document.getElementById("game");
  const SAVE = "kindling-game";
  const HEAT_NAME = (h) => `${h} · ${K.HEAT[h].name}`;

  const defaultSetup = () => ({
    players: [{ name: "", heat: 0, wish: "" }, { name: "", heat: 0, wish: "" }],
    mode: "partners",
    decks: ["embers", "slowburn"],
    goal: 25,
    pot: 0,
  });

  let S = K.store.get(SAVE, null);
  if (!S || !S.setup) S = { phase: "setup", setup: defaultSetup() };
  const save = () => K.store.set(SAVE, S);

  let byId = {};
  let modal = null; // { kind: "heat", idx }

  /* ---------------- helpers ---------------- */
  const pname = (i) => (S.players ? S.players[i].name : S.setup.players[i].name) || `Player ${i + 1}`;
  const cap = () => Math.max(1, Math.min(5, S.baseCap + (S.capTurns > 0 ? S.capMod : 0)));
  const card = () => (S.current ? byId[S.current] : null);
  const owner = () => (S.owner ?? S.turn);
  const eligible = (c) => {
    if (c.heat > cap()) return false;
    if (S.setup.mode === "friends" && c.pairing !== "any") return false;
    if (S.players.length < 3 && c.players === "3+") return false;
    return true;
  };

  /* ---------------- setup ---------------- */
  const tableHeat = () => {
    const hs = S.setup.players.map((p) => p.heat || 0);
    return hs.every(Boolean) ? Math.min(...hs) : 0;
  };

  const renderSetup = () => {
    const su = S.setup;
    const th = tableHeat();
    const friends = su.mode === "friends";
    el.innerHTML = `
      <div class="kp-setup">
        <section class="kp-panel">
          <span class="eyebrow">New game</span>
          <h2>Who's playing tonight?</h2>
          <p class="hint">Add everyone at the table, then pass the phone so each person can set their max heat in private.</p>
          <div class="kp-players" style="margin-top:1.1rem">
            ${su.players.map((p, i) => `
              <div class="kp-player">
                <input type="text" maxlength="24" placeholder="Player ${i + 1}" value="${esc(p.name)}" data-name="${i}" aria-label="Player ${i + 1} name" />
                <button class="btn btn--sm ${p.heat ? "btn--ghost" : "btn--dark"}" type="button" data-act="heat" data-i="${i}">${p.heat ? "Heat set ✓" : "Set heat 🔒"}</button>
                ${su.players.length > 2 ? `<button class="kp-x" type="button" data-act="rm" data-i="${i}" aria-label="Remove player">×</button>` : `<span class="kp-x" style="visibility:hidden"></span>`}
              </div>`).join("")}
          </div>
          ${su.players.length < 8 ? `<button class="pill-more" type="button" data-act="add" style="margin-top:.9rem">+ Add a player</button>` : ""}
          <div class="kp-heatnote">
            ${th ? `<span class="kcard__heat">${K.flames(th)}</span><span>Table heat: <b>${HEAT_NAME(th)}</b>. That's the most careful player's pick.</span>`
                 : `<span>🔒</span><span>Waiting on ${su.players.filter((p) => !p.heat).length} heat pick${su.players.filter((p) => !p.heat).length > 1 ? "s" : ""}. The table plays at the lowest one.</span>`}
          </div>

          <h3>How you know each other</h3>
          <div class="kp-seg" role="group" aria-label="Mode">
            <button type="button" data-act="mode" data-v="partners" aria-pressed="${!friends}">Partners or lovers</button>
            <button type="button" data-act="mode" data-v="friends" aria-pressed="${friends}">Friends: keep it platonic</button>
          </div>
          <p class="hint">${friends ? "Friends mode only deals the friend-safe cards (heat 1–2, nothing sexual), so it works for a double date or a group of friends." : "Every card is in play up to your table heat."}</p>

          <h3>Decks</h3>
          <div class="k-chips" role="group" aria-label="Decks">
            ${K.decks.map((d) => {
              const off = friends && d.adult;
              return `<button class="k-chip" type="button" data-act="deck" data-v="${d.id}" data-deck="${d.id}" aria-pressed="${su.decks.includes(d.id) && !off}" ${off ? "disabled" : ""}><i></i>${esc(d.name)}${d.adult ? " · 18+" : ""}</button>`;
            }).join("")}
          </div>

          <h3>How long</h3>
          <div class="kp-seg" role="group" aria-label="Goal">
            ${[[25, "Quick · first to 25"], [50, "Long night · 50"], [0, "Endless"]].map(([v, l]) => `<button type="button" data-act="goal" data-v="${v}" aria-pressed="${su.goal === v}">${l}</button>`).join("")}
          </div>

          <h3>Rewards (optional)</h3>
          <p class="hint">Each player writes up to three things they'd love to receive. The winner picks one from someone else's list, and that person makes it happen.</p>
          <div class="kp-wish" style="margin-top:.7rem">
            ${su.players.map((p, i) => `<label class="kp-field"><span data-wish-label="${i}">${esc(p.name || `Player ${i + 1}`)}'s wish list</span><textarea data-wish="${i}" rows="2" placeholder="A slow massage&#10;Breakfast in bed on Sunday">${esc(p.wish)}</textarea></label>`).join("")}
          </div>

          <h3>The Pot (optional)</h3>
          <label class="kp-field" style="max-width:260px">Each player puts in ($)
            <input type="number" min="0" step="5" inputmode="numeric" value="${su.pot || ""}" placeholder="0 = no pot" data-pot />
          </label>

          <div class="kp-start">
            <button class="btn btn--flame" type="button" data-act="start">Light it up</button>
            <span class="hint">${th ? "" : "Players who skip the heat pick play at 2 · Glow."}</span>
          </div>
        </section>
        <aside class="kp-aside">
          ${K.cardHTML(K.rules[0])}
          ${K.cardHTML(K.rules[2])}
        </aside>
      </div>
      ${modal && modal.kind === "heat" ? heatModal(modal.idx) : ""}`;
  };

  const heatModal = (i) => `
    <div class="scrim is-open" data-act="close-modal" style="opacity:1;visibility:visible"></div>
    <div role="dialog" aria-modal="true" aria-label="Set your heat" style="position:fixed;inset:0;display:grid;place-items:center;z-index:80;padding:16px;pointer-events:none">
      <div class="kp-panel" style="pointer-events:auto;max-width:440px;width:100%;box-shadow:var(--shadow-lg)">
        <span class="eyebrow">Only ${esc(pname(i))} should be looking</span>
        <h2 style="margin-top:.4rem">How hot can it get tonight?</h2>
        <p class="hint">This is your ceiling. Nobody sees your answer, only the table's lowest pick.</p>
        <div style="display:grid;gap:.45rem;margin-top:1rem">
          ${[1, 2, 3, 4, 5].map((h) => `<button class="k-heat__btn" style="justify-content:flex-start;border-radius:14px;padding:.75em 1em" type="button" data-act="setheat" data-i="${i}" data-h="${h}">${K.flame()}<span><b>${HEAT_NAME(h)}</b><br><small style="font-weight:600;opacity:.75">${K.HEAT[h].desc}</small></span></button>`).join("")}
        </div>
      </div>
    </div>`;

  const start = () => {
    const su = S.setup;
    if (su.mode === "friends") su.decks = su.decks.filter((d) => !(K.deckById[d] || {}).adult);
    if (!su.decks.length) su.decks = ["embers"];
    const heats = su.players.map((p) => p.heat || 2);
    S.phase = "table";
    S.players = su.players.map((p, i) => ({ name: p.name.trim() || `Player ${i + 1}`, sparks: 0, wood: [], tokens: { freepass: 0, pass: 0 } }));
    S.baseCap = Math.min(...heats);
    S.capMod = 0; S.capTurns = 0;
    S.double = false; S.reverse = null; S.owner = null;
    S.turn = 0; S.current = null; S.sub = null; S.history = [];
    S.deck = K.shuffle(K.cards.filter((c) => su.decks.includes(c.deck)).map((c) => c.id));
    S.ended = null; S.chosen = null;
    save(); render();
  };

  /* ---------------- table ---------------- */
  const draw = () => {
    const i = S.deck.findIndex((id) => eligible(byId[id]));
    if (i < 0) return endGame("empty");
    S.current = S.deck.splice(i, 1)[0];
    S.owner = null; S.sub = null;
    const c = byId[S.current];
    if (c.match) S.sub = { kind: "vote", votes: {} };
    save(); render();
  };

  const score = (pi, n, { useDouble = true } = {}) => {
    let amt = n;
    if (useDouble && S.double && n > 0) { amt = n * 2; S.double = false; }
    S.players[pi].sparks += amt;
    return amt;
  };

  const checkWin = () => {
    if (!S.setup.goal) return false;
    const hit = S.players.findIndex((p) => p.sparks >= S.setup.goal);
    if (hit >= 0) { endGame("win"); return true; }
    return false;
  };

  const nextTurn = () => {
    if (S.current) S.history.push({ id: S.current, by: owner() });
    if (checkWin()) return;
    if (S.capTurns > 0) { S.capTurns -= 1; if (!S.capTurns) S.capMod = 0; }
    S.turn = (S.turn + 1) % S.players.length;
    S.current = null; S.sub = null; S.owner = null;
    save(); render();
  };

  const toast = (msg) => K.toast(msg);

  const playWild = (c) => {
    const me = S.turn, n = S.players.length;
    switch (c.effect) {
      case "pass": S.players[me].tokens.pass += 1; toast(`${esc(pname(me))} keeps a Pass It On.`); return nextTurn();
      case "double": S.double = true; toast("Double Down: the next card scores double."); return nextTurn();
      case "coolit": S.capMod = -1; S.capTurns = 3 * n; toast("Cool it: heat drops by one for a few turns."); return nextTurn();
      case "turnup": S.sub = { kind: "turnup" }; return render();
      case "steal": {
        const any = S.players.some((p, i) => i !== me && p.wood.length);
        if (!any) { toast("Every other Woodpile is empty. Lucky them."); return nextTurn(); }
        S.sub = { kind: "steal" }; return render();
      }
      case "reverse": S.reverse = me; toast(`Reverse: on ${esc(pname(me))}'s next turn, ${esc(pname((me - 1 + n) % n))} does the card to them.`); return nextTurn();
      case "freepass": S.players[me].tokens.freepass += 1; toast(`${esc(pname(me))} keeps a Free Pass.`); return nextTurn();
      case "callback": {
        const done = S.history.filter((h) => byId[h.id].type !== "wild");
        if (!done.length) { toast("Nothing to call back yet. Keep this energy for later."); return nextTurn(); }
        S.sub = { kind: "callback" }; return render();
      }
      case "yourrules": S.sub = { kind: "yourrules", heat: 0 }; return render();
      case "truce": S.players.forEach((p) => (p.sparks += 3)); toast("Truce: everyone +3. Go get water."); return nextTurn();
      default: return nextTurn();
    }
  };

  const actionsFor = (c) => {
    const me = S.turn, p = S.players[me];
    const sub = S.sub;
    if (c.type === "wild") {
      if (sub && sub.kind === "turnup") return `<div class="kp-vote"><p>Turn It Up raises the heat cap by one for a few turns, but only if <b>everyone</b> agrees out loud. One no keeps it where it is.</p><div class="kp-actions"><button class="btn btn--flame" data-act="turnup-yes">Everyone agrees</button><button class="btn btn--ghost" data-act="turnup-no">Someone said no</button></div></div>`;
      if (sub && sub.kind === "steal") {
        const opts = S.players.flatMap((pl, i) => i === me ? [] : pl.wood.map((id) => `<button type="button" data-act="steal" data-from="${i}" data-id="${id}">${esc(pl.name)}: ${esc(byId[id].text.slice(0, 48))}${byId[id].text.length > 48 ? "…" : ""}</button>`));
        return `<div class="kp-vote"><p>Pick a claimed card to steal. It moves to your Woodpile, and so do the Sparks.</p><div class="kp-pick">${opts.join("")}</div></div>`;
      }
      if (sub && sub.kind === "callback") {
        const seen = new Set();
        const opts = S.history.slice().reverse().filter((h) => byId[h.id].type !== "wild" && !seen.has(h.id) && seen.add(h.id)).slice(0, 8)
          .map((h) => `<button type="button" data-act="callback" data-id="${h.id}">${esc(byId[h.id].text.slice(0, 52))}${byId[h.id].text.length > 52 ? "…" : ""} (+${byId[h.id].sparks})</button>`);
        return `<div class="kp-vote"><p>Pick a card from tonight to do again, for full Sparks.</p><div class="kp-pick">${opts.join("")}</div></div>`;
      }
      if (sub && sub.kind === "yourrules") {
        return `<div class="kp-vote"><p>Make up a card and play it. Whoever's receiving it picks the heat, and the heat is the score.</p>
          <div class="kp-input"><textarea data-custom placeholder="Write your card…">${esc(sub.text || "")}</textarea></div>
          <div class="kp-pick">${[1, 2, 3, 4, 5].filter((h) => h <= cap()).map((h) => `<button type="button" data-act="custom-heat" data-h="${h}" ${sub.heat === h ? 'style="background:var(--k-flame);color:#1D0A04"' : ""}>${HEAT_NAME(h)}</button>`).join("")}</div>
          <div class="kp-actions"><button class="btn btn--flame" data-act="custom-done" ${sub.heat ? "" : "disabled"}>We did it ${sub.heat ? `(+${sub.heat})` : ""}</button><button class="btn btn--ghost" data-act="skip">Skip</button></div></div>`;
      }
      return `<div class="kp-actions"><button class="btn btn--flame" data-act="wild">Play it</button><button class="btn btn--ghost" data-act="skip">Skip</button></div>`;
    }

    if (c.match) {
      const v = sub.votes || {};
      const n = S.players.length, voted = Object.keys(v).length;
      if (sub.reveal === true) {
        return `<div class="kp-vote"><p><b style="color:var(--k-gold)">Everyone said yes.</b> Do it together and everyone scores double.</p><div class="kp-actions"><button class="btn btn--flame" data-act="match-done">We did it (everyone +${c.sparks * 2})</button><button class="btn btn--ghost" data-act="skip">Changed our minds</button></div></div>`;
      }
      if (sub.reveal === false) {
        return `<div class="kp-vote"><p>Not tonight. The card disappears, and nobody needs to know who said no.</p><div class="kp-actions"><button class="btn btn--cream" data-act="skip">Next</button></div></div>`;
      }
      return `<div class="kp-vote"><p><b>Match card.</b> Pass the phone. Everyone votes in secret, and it only happens if it's unanimous.</p>
        <div class="kp-vote__row">${S.players.map((pl, i) => v[i] ? `<div class="kp-voter is-voted"><b>${esc(pl.name)}</b><span>Voted ✓</span></div>` : `<div class="kp-voter"><b>${esc(pl.name)}</b><div class="btns"><button type="button" data-act="vote" data-i="${i}" data-v="yes">Yes</button><button type="button" data-act="vote" data-i="${i}" data-v="no">No</button></div></div>`).join("")}</div>
        ${voted === n ? `<button class="btn btn--flame" data-act="reveal">Reveal</button>` : ""}</div>`;
    }

    if (sub && sub.kind === "passto") {
      return `<div class="kp-vote"><p>Who's taking it? They play it as if they drew it.</p><div class="kp-pick">${S.players.map((pl, i) => i === me ? "" : `<button type="button" data-act="passto" data-i="${i}">${esc(pl.name)}</button>`).join("")}<button type="button" data-act="passto-cancel">Never mind</button></div></div>`;
    }

    const who = owner();
    const amt = c.sparks * (S.double ? 2 : 1);
    const isMe = who === me;
    return `<div class="kp-actions">
      <button class="btn btn--flame" data-act="do">${isMe ? "Done" : `${esc(pname(who))} did it`} · +${amt}</button>
      <button class="btn btn--cream" data-act="claim">Claim for later</button>
      <button class="btn btn--ghost" data-act="skip">Skip (free)</button>
      ${isMe && p.tokens.freepass ? `<button class="btn btn--ghost" data-act="freepass">Use Free Pass · +1</button>` : ""}
      ${isMe && p.tokens.pass ? `<button class="btn btn--ghost" data-act="pass">Pass It On →</button>` : ""}
    </div>`;
  };

  const renderTable = () => {
    const c = card();
    const me = S.turn, n = S.players.length;
    const goal = S.setup.goal;
    const banners = [];
    if (S.double) banners.push("Double Down is live: the next card scores double.");
    if (S.capTurns > 0) banners.push(S.capMod < 0 ? "Cool It: the heat is down by one for a few turns." : "Turned up: the heat is up by one for a few turns.");
    if (S.reverse === me && !c) banners.push(`Reverse: ${esc(pname((me - 1 + n) % n))} reads this one and does it to ${esc(pname(me))}.`);
    if (S.owner != null && S.owner !== me) banners.push(`${esc(pname(S.owner))} is playing this one.`);

    el.innerHTML = `
      <div class="kp-table">
        <section>
          <div class="kp-status">
            <span class="chip">Table heat · ${HEAT_NAME(cap())}</span>
            <span class="chip">${S.deck.filter((id) => eligible(byId[id])).length} cards left</span>
            <span class="chip">${goal ? `First to ${goal}` : "Endless"}</span>
          </div>
          <div class="kp-turn"><small>${c ? "Read it out loud" : "Pass the phone to"}</small><b>${esc(pname(me))}${c ? "" : "'s turn"}</b></div>
          <div class="kp-stage">
            <div class="kflip ${c ? "" : "is-down"}" data-flip><div class="kflip__in">${c ? K.cardHTML(c, { double: S.double && !c.match }) + K.backHTML(c.deck) : K.cardHTML(K.rules[0]) + K.backHTML(S.setup.decks[0])}</div></div>
            ${banners.map((b) => `<p class="kp-banner">${b}</p>`).join("")}
            ${c ? actionsFor(c) : `<div class="kp-actions"><button class="btn btn--flame" data-act="draw">Draw a card</button></div>`}
          </div>
        </section>
        <aside class="kp-side">
          <div class="kp-board">
            ${S.players.map((p, i) => `<div class="kp-score ${i === me ? "is-turn" : ""}">
              <div class="kp-score__top"><b>${esc(p.name)}</b><span>${p.sparks}</span></div>
              ${goal ? `<div class="kp-bar"><i style="width:${Math.min(100, (p.sparks / goal) * 100)}%"></i></div>` : ""}
              ${p.tokens.freepass || p.tokens.pass ? `<div class="kp-tokens">${p.tokens.freepass ? `<span>Free Pass ×${p.tokens.freepass}</span>` : ""}${p.tokens.pass ? `<span>Pass It On ×${p.tokens.pass}</span>` : ""}</div>` : ""}
            </div>`).join("")}
          </div>
          <div class="kp-wood">
            <h3>The Woodpile</h3>
            ${S.players.some((p) => p.wood.length) ? `<ul>${S.players.flatMap((p, i) => p.wood.map((id) => {
              const wc = byId[id];
              return `<li data-deck="${wc.deck}"><em>${esc(p.name)} · +${wc.sparks}${wc.time ? ` · ${esc(wc.time)}` : ""}</em>${esc(wc.text)}<div><button class="do" data-act="wood-done" data-p="${i}" data-id="${id}">Done ✓</button><button data-act="wood-drop" data-p="${i}" data-id="${id}">Let it go</button></div></li>`;
            })).join("")}</ul>` : `<p class="empty">Claimed cards wait here until you do them, tonight or before next game night. They score when they're done.</p>`}
          </div>
          <div class="kp-tools">
            <button type="button" data-act="coolit" title="Lower the heat cap by one for the rest of the game">Cool it</button>
            <button type="button" data-act="end">End game</button>
            <button type="button" class="ember" data-act="ember" title="Anyone can say it. The game ends now.">Ember out</button>
          </div>
        </aside>
      </div>`;
  };

  /* ---------------- end ---------------- */
  const endGame = (why) => {
    S.phase = "end"; S.ended = why;
    if (S.current) { S.history.push({ id: S.current, by: owner() }); S.current = null; }
    save(); render();
  };

  const renderEnd = () => {
    const ps = S.players.map((p, i) => ({ ...p, i })).sort((a, b) => b.sparks - a.sparks);
    const win = ps[0], last = ps[ps.length - 1];
    const ember = S.ended === "ember";
    const wishes = S.setup.players.flatMap((p, i) => i === win.i ? [] : (p.wish || "").split("\n").map((w) => w.trim()).filter(Boolean).map((w) => ({ w, i })));
    const pot = (S.setup.pot || 0) * S.players.length;
    el.innerHTML = `
      <div class="kp-end">
        <span class="pill-title pill-title--gold">${ember ? "Ember out" : S.ended === "empty" ? "Out of cards" : "Game over"}</span>
        <h2 style="margin-top:1.25rem">${ember ? "Good call." : `${esc(win.name)} caught fire.`}</h2>
        <p>${ember ? "The game's over, no questions asked. Get some water, snacks, and a hug, in any order. The scores are below if anyone's curious." : `${win.sparks} Sparks. ${wishes.length ? `${esc(win.name)} picks a reward from someone else's wish list, and they make it happen.` : "Winner's choice: something small and lovely from the person in last place."}`}</p>
        <div class="kp-end__board">${ps.map((p) => `<div><b>${p.sparks}</b>${esc(p.name)}</div>`).join("")}</div>
        ${!ember && wishes.length ? `<div class="kp-reward">${wishes.map((x, k) => `<button type="button" data-act="reward" data-k="${k}" aria-pressed="${S.chosen === k}"><small>From ${esc(pname(x.i))}'s list</small>${esc(x.w)}</button>`).join("")}</div>` : ""}
        ${!ember && S.chosen != null && wishes[S.chosen] ? `<p class="kp-chosen">${esc(win.name)} chose <em>${esc(wishes[S.chosen].w)}</em>. ${esc(pname(wishes[S.chosen].i))} delivers.${pot ? ` The Pot (${K.money(pot)}) pays, and ${esc(last.name)} plans it.` : ""}</p>` : !ember && pot ? `<p class="kp-chosen">The Pot: <em>${K.money(pot)}</em>. ${esc(win.name)} picks the experience, and ${esc(last.name)} plans it.</p>` : ""}
        ${S.players.some((p) => p.wood.length) ? `<p style="margin-top:1.25rem;color:var(--k-soft)">Still in the Woodpile: ${S.players.reduce((a, p) => a + p.wood.length, 0)} claimed card${S.players.reduce((a, p) => a + p.wood.length, 0) > 1 ? "s" : ""}. Keep your promises.</p>` : ""}
        <div class="kp-actions" style="margin:2rem auto 0">
          <button class="btn btn--flame" data-act="again">Play again</button>
          <button class="btn btn--ghost" style="color:var(--k-cream)" data-act="new">New setup</button>
          <a class="btn btn--cream" href="shop.html">Get the real deck</a>
        </div>
      </div>`;
  };

  /* ---------------- render + events ---------------- */
  const render = () => {
    if (S.phase === "setup") renderSetup();
    else if (S.phase === "table") renderTable();
    else renderEnd();
  };

  el.addEventListener("input", (e) => {
    const t = e.target;
    if (t.matches("[data-name]")) {
      const i = +t.dataset.name;
      S.setup.players[i].name = t.value; save();
      const sum = el.querySelector(`[data-wish-label="${i}"]`);
      if (sum) sum.textContent = `${t.value.trim() || `Player ${i + 1}`}'s wish list`;
    }
    else if (t.matches("[data-wish]")) { S.setup.players[+t.dataset.wish].wish = t.value; save(); }
    else if (t.matches("[data-pot]")) { S.setup.pot = Math.max(0, +t.value || 0); save(); }
    else if (t.matches("[data-custom]")) { S.sub.text = t.value; save(); }
  });

  el.addEventListener("click", (e) => {
    const b = e.target.closest("[data-act]");
    if (!b || b.disabled) return;
    const a = b.dataset.act, su = S.setup;
    const c = card();
    switch (a) {
      /* setup */
      case "add": su.players.push({ name: "", heat: 0, wish: "" }); break;
      case "rm": su.players.splice(+b.dataset.i, 1); break;
      case "heat": modal = { kind: "heat", idx: +b.dataset.i }; break;
      case "setheat": su.players[+b.dataset.i].heat = +b.dataset.h; modal = null; break;
      case "close-modal": modal = null; break;
      case "mode": su.mode = b.dataset.v; break;
      case "deck": {
        const id = b.dataset.v;
        if (su.decks.includes(id)) { if (su.decks.length > 1) su.decks = su.decks.filter((d) => d !== id); }
        else { if ((K.deckById[id] || {}).adult && !K.confirmAdult()) return; su.decks.push(id); }
        break;
      }
      case "goal": su.goal = +b.dataset.v; break;
      case "start": save(); return start();

      /* table */
      case "draw": if (S.reverse === S.turn) S.reverse = null; return draw();
      case "do": { const amt = score(owner(), c.sparks); toast(`+${amt} for ${esc(pname(owner()))}`); return nextTurn(); }
      case "claim": S.players[owner()].wood.push(S.current); S.current = null; toast("Claimed. It scores when it's done."); return nextTurn();
      case "skip": S.current = null; return nextTurn();
      case "freepass": S.players[S.turn].tokens.freepass -= 1; score(S.turn, 1, { useDouble: false }); S.current = null; return nextTurn();
      case "pass": S.sub = { kind: "passto" }; break;
      case "passto": S.players[S.turn].tokens.pass -= 1; S.owner = +b.dataset.i; S.sub = null; break;
      case "passto-cancel": S.sub = null; break;
      case "wild": return playWild(c);
      case "turnup-yes": S.capMod = 1; S.capTurns = 3 * S.players.length; toast("Turned up. Look after each other."); return nextTurn();
      case "turnup-no": toast("Heat stays put. That's the rule working."); return nextTurn();
      case "steal": {
        const from = S.players[+b.dataset.from], id = b.dataset.id;
        from.wood = from.wood.filter((x) => x !== id); S.players[S.turn].wood.push(id);
        toast(`Stolen from ${esc(from.name)}.`); return nextTurn();
      }
      case "callback": { const amt = score(S.turn, byId[b.dataset.id].sparks); toast(`Encore: +${amt}`); return nextTurn(); }
      case "custom-heat": S.sub.heat = +b.dataset.h; break;
      case "custom-done": { const amt = score(S.turn, S.sub.heat); toast(`+${amt} for ${esc(pname(S.turn))}`); return nextTurn(); }
      case "vote": S.sub.votes[b.dataset.i] = b.dataset.v; break;
      case "reveal": S.sub.reveal = Object.values(S.sub.votes).every((v) => v === "yes"); break;
      case "match-done": { const dbl = S.double; S.double = false; S.players.forEach((p) => (p.sparks += c.sparks * 2 * (dbl ? 2 : 1))); toast("Everyone scores double."); return nextTurn(); }
      case "wood-done": {
        const p = S.players[+b.dataset.p], id = b.dataset.id;
        p.wood = p.wood.filter((x) => x !== id); p.sparks += byId[id].sparks;
        toast(`+${byId[id].sparks} for ${esc(p.name)}. Promise kept.`);
        save(); if (checkWin()) return; break;
      }
      case "wood-drop": { const p = S.players[+b.dataset.p]; p.wood = p.wood.filter((x) => x !== b.dataset.id); break; }
      case "coolit": S.baseCap = Math.max(1, S.baseCap - 1); toast(`Cooled. Table heat is now ${HEAT_NAME(cap())}.`); break;
      case "end": return endGame("end");
      case "ember": return endGame("ember");

      /* end */
      case "reward": S.chosen = +b.dataset.k; break;
      case "again": return start();
      case "new": S = { phase: "setup", setup: S.setup }; S.setup.players.forEach((p) => (p.heat = 0)); break;
      default: return;
    }
    save(); render();
  });

  document.addEventListener("keydown", (e) => { if (e.key === "Escape" && modal) { modal = null; render(); } });

  K.data.then(() => {
    byId = Object.fromEntries(K.cards.concat(K.rules).map((c) => [c.id, c]));
    if (S.phase !== "setup" && (!S.players || (S.current && !byId[S.current]))) S = { phase: "setup", setup: defaultSetup() };
    render();
  }).catch(() => { el.innerHTML = `<p class="hint" style="padding:3rem 0;text-align:center">Couldn't load the deck. Refresh to try again.</p>`; });
})();
