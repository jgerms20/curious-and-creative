/* Kindling shop: products from data/kindling-shop.json, cart in localStorage,
   checkout via pre-order reservation (default), Shopify cart permalink, or Stripe Payment Links. */
(() => {
  const K = window.K, esc = window.CC.esc;
  const $ = (s) => document.querySelector(s);
  let shop, done = false, sending = false;

  const fanFor = (deck, n = 2) => {
    const pool = deck === "bundle" ? ["embers", "wildfire", "slowburn"] : [deck];
    const want = [4, 3, 5, 2];
    return pool.length > 1
      ? pool.slice(0, n).map((d, i) => K.cards.find((c) => c.deck === d && c.heat === want[i] && c.type !== "wild" && c.text.length < 120))
      : want.slice(0, n).map((h) => K.cards.find((c) => c.deck === deck && c.heat === h && c.type !== "wild" && c.text.length < 120));
  };

  const boxFor = (p) => K.boxHTML(p.deck === "bundle" ? "embers" : p.deck, {
    title: p.deck === "bundle" || p.deck === "embers" ? "kindling" : p.name.toLowerCase(),
    sub: p.deck === "bundle" ? "Every deck. One fire." : p.kind,
    meta: [p.cards.split(" ")[0] + " cards", p.adult ? "18+" : "2+ players", p.deck === "embers" ? "Heat 1–5" : "Kindling"],
  });

  const qtyCtl = (id) => `<span class="ks-qty"><button type="button" data-q="-1" data-id="${id}" aria-label="Fewer">−</button><span data-qv="${id}">1</span><button type="button" data-q="1" data-id="${id}" aria-label="More">+</button></span>`;

  const renderProducts = () => {
    const f = shop.products.find((p) => p.id === "embers");
    const hero = $("[data-featured]");
    hero.innerHTML = `
      <div class="ks-hero__stage"><div class="k-hero__fan">${fanFor("embers", 3).map((c) => K.cardHTML(c)).join("")}</div><div data-box>${boxFor(f)}</div></div>
      <div style="display:flex;flex-direction:column">
        ${f.badge ? `<span class="ks-badge">${esc(f.badge)}</span>` : ""}
        <span class="ks-prod__kind" style="margin-top:1rem">${esc(f.kind)} · ${esc(f.cards)}</span>
        <h2 class="ks-prod__name">${esc(f.name)}</h2>
        <div class="ks-prod__price">${K.money(f.price)}</div>
        <p class="ks-prod__blurb">${esc(f.blurb)}</p>
        <ul class="ks-prod__inc">${f.includes.map((x) => `<li>${esc(x)}</li>`).join("")}</ul>
        <div class="ks-buy">${qtyCtl(f.id)}<button class="btn btn--flame" type="button" data-add="${f.id}">Add to cart · ${K.money(f.price)}</button></div>
      </div>`;
    K.tilt(hero.querySelector(".kbox"));

    $("[data-products]").innerHTML = shop.products.filter((p) => p.id !== "embers").map((p) => `
      <article class="ks-card" id="${p.id}" data-deck="${p.deck}">
        <div class="ks-card__art">${fanFor(p.deck).map((c) => c ? K.cardHTML(c) : "").join("")}${boxFor(p)}</div>
        <div class="ks-card__body">
          <span class="ks-prod__kind">${esc(p.kind)}${p.adult && p.deck === "afterdark" ? " · 18+" : ""}</span>
          <h3 class="ks-prod__name">${esc(p.name)}</h3>
          <div class="ks-prod__price">${K.money(p.price)}${p.compareAt ? ` <s>${K.money(p.compareAt)}</s>` : ""}${p.badge ? ` <span class="ks-badge" style="font-size:10px">${esc(p.badge)}</span>` : ""}</div>
          <p class="ks-prod__blurb">${esc(p.blurb)}</p>
          <ul class="ks-prod__inc">${p.includes.map((x) => `<li>${esc(x)}</li>`).join("")}</ul>
          ${p.requires ? `<p class="ks-card__note">Expansion: plays with the Embers core deck.</p>` : ""}
          <div class="ks-buy">${qtyCtl(p.id)}<button class="btn btn--dark" type="button" data-add="${p.id}">Add · ${K.money(p.price)}</button></div>
        </div>
      </article>`).join("");
  };

  /* ---------- cart ---------- */
  const lines = () => Object.entries(K.cart.items()).filter(([id]) => K.productById[id]).map(([id, qty]) => ({ p: K.productById[id], qty }));
  const totals = () => {
    const ls = lines();
    const sub = ls.reduce((a, l) => a + l.p.price * l.qty, 0);
    const ship = !sub || sub >= shop.freeShippingOver ? 0 : shop.flatShipping;
    return { ls, sub, ship, total: sub + ship };
  };

  const checkoutForm = () => {
    const mode = shop.checkout.mode;
    if (mode === "shopify" && shopifyUrl()) return `<a class="btn btn--flame" href="${esc(shopifyUrl())}">Checkout</a><p class="ks-fine">Secure checkout on our Shopify store.</p>`;
    if (mode === "stripe") {
      const ls = lines(), links = shop.checkout.stripe.paymentLinks;
      if (ls.length === 1 && links[ls[0].p.id]) return `<a class="btn btn--flame" href="${esc(links[ls[0].p.id])}">Checkout · ${esc(ls[0].p.name)}</a><p class="ks-fine">Secure checkout by Stripe. You can set the quantity there.</p>`;
      if (ls.length > 1 && ls.every((l) => links[l.p.id])) return `<p class="ks-fine" style="margin-top:1rem">Stripe checks out one product at a time. Tip: The Whole Fire bundle covers everything in one go.</p>${ls.map((l) => `<a class="btn btn--dark btn--sm" href="${esc(links[l.p.id])}">Checkout · ${esc(l.p.name)}</a>`).join("")}`;
    }
    return `<form class="form" data-preorder novalidate>
      <label>Name<input name="name" autocomplete="name" required /></label>
      <label>Email<input name="email" type="email" autocomplete="email" required /></label>
      <label>Ship-to ZIP / postcode<input name="zip" autocomplete="postal-code" /></label>
      <label>Anything we should know? <span style="font-weight:500;color:var(--ink-soft)">(optional)</span><textarea name="note" style="min-height:70px" placeholder="It's a gift, wholesale, a podcast review copy…"></textarea></label>
      <button class="btn btn--flame" type="submit" ${sending ? "disabled" : ""}>${sending ? "Reserving…" : "Reserve my box"}</button>
      <p class="ks-fine">${esc(shop.status)}</p>
    </form>`;
  };

  const shopifyUrl = () => {
    const s = shop.checkout.shopify, ls = lines();
    if (!s.storeDomain || !ls.length || !ls.every((l) => s.variants[l.p.id])) return "";
    return `https://${s.storeDomain}/cart/${ls.map((l) => `${s.variants[l.p.id]}:${l.qty}`).join(",")}`;
  };

  const renderCart = () => {
    const box = $("[data-cart]");
    if (done) {
      box.innerHTML = `<div class="ks-done">${K.mark()}<b>You're on the list.</b><p style="color:var(--ink-soft);margin-top:.6rem">We'll email you when boxes land, with a checkout link. Nothing is charged until then.</p><a class="btn btn--dark" href="play.html">Play free while you wait</a></div>`;
      box.querySelector(".k-mark").style.cssText = "width:48px;height:48px;margin:0 auto 1rem";
      return;
    }
    const { ls, sub, ship, total } = totals();
    const needsCore = ls.some((l) => l.p.requires) && !ls.some((l) => ["embers", "bundle"].includes(l.p.id));
    const left = Math.max(0, shop.freeShippingOver - sub);
    box.innerHTML = `
      <h2>Your cart <small>${K.cart.count()} item${K.cart.count() === 1 ? "" : "s"}</small></h2>
      ${ls.length ? `<div class="ks-lines">${ls.map((l) => `
        <div class="ks-line" data-deck="${l.p.deck}">
          <span class="ks-line__sw">${K.mark()}</span>
          <span><b>${esc(l.p.name)}</b><small>${K.money(l.p.price)} · ${esc(l.p.kind)}</small></span>
          <span class="ks-qty"><button type="button" data-cq="-1" data-id="${l.p.id}" aria-label="Fewer">−</button><span>${l.qty}</span><button type="button" data-cq="1" data-id="${l.p.id}" aria-label="More">+</button></span>
        </div>`).join("")}</div>
        ${needsCore ? `<p class="kp-heatnote" style="font-size:.88rem;margin:0 0 1rem">Expansions play with the Embers core deck. <button class="pill-more" type="button" data-add="embers">Add Embers</button></p>` : ""}
        <div class="ks-sum">
          <div><span>Subtotal</span><span>${K.money(sub)}</span></div>
          <div><span>Shipping</span><span>${ship ? K.money(ship) : "Free"}</span></div>
          <div class="total"><span>Total</span><span>${K.money(total)}</span></div>
          <div class="ks-ship">${left ? `${K.money(left)} away from free shipping` : "You've got free shipping."}<div class="kp-bar"><i style="width:${Math.min(100, (sub / shop.freeShippingOver) * 100)}%"></i></div></div>
        </div>
        ${checkoutForm()}`
      : `<p class="ks-empty">Nothing here yet. Start with <button class="pill-more" type="button" data-add="embers">Embers, the core deck</button>, the only one you need to play.</p>`}`;
  };

  const add = (id, n = 1) => {
    const p = K.productById[id];
    if (!p) return;
    if (p.adult && !K.confirmAdult()) return;
    K.cart.add(id, n);
    K.toast(`Added ${esc(p.name)}${n > 1 ? ` ×${n}` : ""}. <a href="#cart">View cart</a>`);
  };

  const submit = async (form) => {
    const fd = new FormData(form);
    const name = (fd.get("name") || "").trim(), email = (fd.get("email") || "").trim();
    if (!name || !/^\S+@\S+\.\S+$/.test(email)) { K.toast("Add your name and a real email so we can reach you."); return; }
    const { ls, total } = totals();
    const summary = ls.map((l) => `${l.qty} × ${l.p.name} (${K.money(l.p.price * l.qty)})`).join("\n");
    const payload = { name, email, zip: fd.get("zip") || "", note: fd.get("note") || "", order: summary, total: K.money(total), _subject: `Kindling pre-order: ${name}` };
    const cfg = shop.checkout.preorder;
    if (cfg.formEndpoint) {
      sending = true; renderCart();
      try {
        const r = await fetch(cfg.formEndpoint, { method: "POST", headers: { "Content-Type": "application/json", Accept: "application/json" }, body: JSON.stringify(payload) });
        if (!r.ok) throw new Error(r.status);
        done = true; K.cart.clear();
      } catch (e) { K.toast("That didn't go through. Try again, or email us directly."); }
      sending = false; renderCart();
      return;
    }
    const body = `Hi! I'd like to reserve:\n\n${summary}\n\nTotal: ${K.money(total)}\nName: ${name}\nEmail: ${email}\nZIP: ${payload.zip}\n${payload.note ? `Note: ${payload.note}\n` : ""}`;
    location.href = `mailto:${cfg.email}?subject=${encodeURIComponent(payload._subject)}&body=${encodeURIComponent(body)}`;
    done = true; K.cart.clear(); renderCart();
  };

  document.addEventListener("click", (e) => {
    const t = e.target.closest("[data-add],[data-q],[data-cq]");
    if (!t) return;
    if (t.dataset.add) {
      const qv = document.querySelector(`[data-qv="${t.dataset.add}"]`);
      add(t.dataset.add, qv && t.closest(".ks-buy") ? +qv.textContent : 1);
    } else if (t.dataset.q) {
      const v = document.querySelector(`[data-qv="${t.dataset.id}"]`);
      v.textContent = Math.max(1, Math.min(10, +v.textContent + +t.dataset.q));
    } else if (t.dataset.cq) {
      const id = t.dataset.id;
      K.cart.set(id, (K.cart.items()[id] || 0) + +t.dataset.cq);
    }
  });
  document.addEventListener("submit", (e) => { if (e.target.matches("[data-preorder]")) { e.preventDefault(); submit(e.target); } });
  document.addEventListener("kindling:cart", () => renderCart());

  Promise.all([K.data, K.shop]).then(([, s]) => {
    shop = s;
    $("[data-status]").textContent = `${s.status} The whole game is also free to play right here.`;
    renderProducts();
    renderCart();
    if (location.hash && location.hash !== "#cart") { const t = document.querySelector(location.hash); if (t) t.scrollIntoView(); }
  });
})();
