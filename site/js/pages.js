/* Subpage renderers (shows, archive, photography) — built from data/*.json */
(() => {
  const CC = window.CC;
  const { esc, url, ago, dur, icon } = CC;
  const ext = (h) => (/^https?:/.test(h) ? ' target="_blank" rel="noopener"' : "");

  const epRow = (e, s) => {
    const h = CC.epHref(e);
    const vid = e.kind === "video" || e.kind === "short";
    const img = vid ? e.image : e.image || CC.art(s);
    return `<a class="ep${vid ? " ep--video" : ""}" href="${esc(h)}"${ext(h)} data-show="${esc(e.show)}">
      ${img ? `<img src="${esc(img)}" alt="" loading="lazy">` : '<span class="ph"></span>'}
      <span><b>${esc(e.title)}</b><small>${esc([s && (s.short || s.name), e.description].filter(Boolean).join(" — "))}</small></span>
      <span class="ep__when">${esc(ago(e.date))}${e.duration ? `<br>${esc(dur(e.duration))}` : ""}</span>
    </a>`;
  };
  CC.epRow = epRow;

  CC.ready.then((data) => {
    if (CC.page === "shows") shows(data);
    if (CC.page === "archive") archive(data);
    if (CC.page === "art") gallery(data);
    if (CC.page === "about") about(data);
    if (CC.page === "network") networkPage(data);
    if (CC.page === "shop") shop(data);
    CC.reveal();
  });

  /* ---------------- shows ---------------- */
  function shows(data) {
    const host = document.getElementById("shows-list");
    if (!host) return;
    const block = (s) => {
      const eps = (data.episodes || []).filter((e) => e.show === s.key && e.kind !== "short");
      const links = CC.showLinks(s);
      const status = s.archive ? "Archive · 2020–2023" : s.latest ? (CC.isNew(s.latest) ? "New episode " + ago(s.latest) : "Latest " + ago(s.latest)) : s.flagship ? "The flagship" : "On Spotify";
      return `<section class="showblock rv" id="${s.key}" data-show="${s.key}">
        <div><div class="showblock__art">${s.art ? `<img src="${esc(CC.art(s))}" alt="${esc(s.name)} cover art" loading="lazy">` : ""}</div></div>
        <div>
          <span class="show-tag" data-show="${s.key}"><i></i>${esc(s.kind === "youtube" ? "YouTube show" : "Podcast")} · ${esc((s.hosts || []).join(" & "))}</span>
          <h2 style="margin-top:.6rem">${esc(s.name)}</h2>
          <p class="showblock__about">${esc(s.about || s.description || s.tagline || "")}</p>
          <div class="showblock__facts">
            <span class="chip chip--line">${CC.isNew(s.latest) ? '<span class="dot dot--live"></span>' : ""}${esc(status)}</span>
            ${s.count && (s.feed || s.kind === "youtube") ? `<span class="chip chip--line">${s.count} ${s.kind === "youtube" ? (s.count === 1 ? "video" : "videos") : (s.count === 1 ? "episode" : "episodes")}</span>` : ""}
          </div>
          <div class="showblock__links">
            ${links.map(([l, h], i) => `<a class="btn ${i ? "btn--ghost" : ""} btn--sm" href="${esc(h)}" target="_blank" rel="noopener">${i ? "" : icon.play} ${esc(l)}</a>`).join("")}
            ${s.key === "ccpod" && !links.length ? `<a class="btn btn--sm" href="#newsletter-cta">Get notified</a>` : ""}
          </div>
          ${eps.length ? `<div class="eps">${eps.slice(0, 5).map((e) => epRow(e, s)).join("")}</div>
            ${eps.length > 5 ? `<a class="pill-more eps__more" href="${url(`pages/archive.html?show=${s.key}`)}">All ${eps.length} ${s.kind === "youtube" ? "videos" : "episodes"} →</a>` : ""}`
          : `<p class="eyebrow" style="margin-top:1.4rem">New episodes appear here automatically as they're published.</p>`}
        </div>
      </section>`;
    };
    const head = (t, d) => `<div class="pill-row"><h2 class="pill-title${t.includes("More") ? " pill-title--gold" : ""}">${t}</h2>${d ? `<a class="pill-more" href="${url("pages/network.html")}">${d}</a>` : ""}</div>`;
    host.innerHTML = head("The main lineup") + data.primary.map(block).join("") +
      (data.secondary.length ? head("More from the network", "See the network map →") + data.secondary.map(block).join("") : "");
    if (location.hash) { const el = document.querySelector(location.hash); if (el) setTimeout(() => el.scrollIntoView(), 50); }
  }

  /* ---------------- archive ---------------- */
  function archive(data) {
    const listEl = document.getElementById("arch-list");
    const filtersEl = document.getElementById("arch-filters");
    const input = document.getElementById("arch-q");
    const countEl = document.getElementById("arch-count");
    if (!listEl) return;
    const params = new URLSearchParams(location.search);
    let showF = params.get("show") || "all";
    let limit = 30;
    if (params.get("q")) input.value = params.get("q");

    const all = (data.episodes || []).filter((e) => data.byKey[e.show]);
    const types = [["all", "Everything"], ...data.shows.filter((s) => all.some((e) => e.show === s.key)).map((s) => [s.key, s.short || s.name]), ["video", "Videos"]];
    if (all.some((e) => e.kind === "short")) types.push(["short", "Shorts"]);
    filtersEl.innerHTML = types.map(([k, l]) => `<button class="filter" type="button" data-f="${k}" data-show="${k}">${data.byKey[k] ? "<i></i>" : ""}${esc(l)}</button>`).join("");

    const render = () => {
      filtersEl.querySelectorAll(".filter").forEach((b) => b.classList.toggle("is-on", b.dataset.f === showF));
      const filter = (e) => showF === "all" || e.show === showF || e.kind === showF;
      const q = input.value.trim();
      let items;
      if (q) {
        const ids = new Set(CC.searchDocs(q, (d) => d.type === "episode").map((d) => d.href + "|" + d.title));
        items = all.filter((e) => ids.has(CC.epHref(e) + "|" + e.title));
        const rank = [...ids];
        items.sort((a, b) => rank.indexOf(CC.epHref(a) + "|" + a.title) - rank.indexOf(CC.epHref(b) + "|" + b.title));
      } else items = all;
      items = items.filter(filter);
      countEl.textContent = `${items.length} ${items.length === 1 ? "result" : "results"}${q ? ` for “${q}”` : ""}`;
      listEl.innerHTML = items.length
        ? items.slice(0, limit).map((e) => epRow(e, data.byKey[e.show])).join("") + (items.length > limit ? `<button class="btn btn--dark" style="margin:1.5rem auto 0" type="button" id="arch-more">Show more (${items.length - limit} left)</button>` : "")
        : `<p class="search__empty">Nothing matches yet. Try another spelling, a guest, or a topic.</p>`;
      const more = document.getElementById("arch-more");
      if (more) more.addEventListener("click", () => { limit += 30; render(); });
      const u = new URL(location.href);
      showF === "all" ? u.searchParams.delete("show") : u.searchParams.set("show", showF);
      q ? u.searchParams.set("q", q) : u.searchParams.delete("q");
      history.replaceState(null, "", u);
    };
    filtersEl.addEventListener("click", (e) => { const b = e.target.closest("[data-f]"); if (b) { showF = b.dataset.f; limit = 30; render(); } });
    input.addEventListener("input", () => { limit = 30; render(); });
    render();
  }

  /* ---------------- photography ---------------- */
  function gallery(data) {
    const host = document.getElementById("gallery");
    const setsEl = document.getElementById("photo-sets");
    if (!host) return;
    const photos = data.photos || [];
    if (!photos.length) { host.innerHTML = `<p class="eyebrow">Photos load here from joshuamgerman.com.</p>`; return; }
    const sets = ["All", ...new Set(photos.map((p) => p.set))];
    let cur = "All";
    setsEl.innerHTML = sets.map((s) => `<button class="filter" type="button" data-set="${esc(s)}">${esc(s)} <small style="opacity:.6">${s === "All" ? photos.length : photos.filter((p) => p.set === s).length}</small></button>`).join("");
    const lb = document.createElement("div");
    lb.className = "lightbox";
    lb.setAttribute("role", "dialog");
    lb.setAttribute("aria-modal", "true");
    lb.setAttribute("aria-hidden", "true");
    lb.innerHTML = `<button class="icon-btn" type="button" data-lb-close aria-label="Close">${icon.close}</button><figure><img alt=""><p></p></figure><div class="lightbox__nav"><button type="button" data-lb="-1" aria-label="Previous">${icon.left}</button><button type="button" data-lb="1" aria-label="Next">${icon.right}</button></div>`;
    document.body.appendChild(lb);
    let shown = [], idx = 0;
    const show = (i) => {
      idx = (i + shown.length) % shown.length;
      const p = shown[idx];
      lb.querySelector("img").src = url(p.src);
      lb.querySelector("img").alt = p.alt;
      lb.querySelector("p").textContent = `${p.alt} — ${p.set}`;
      history.replaceState(null, "", "#" + p.id);
    };
    const render = () => {
      setsEl.querySelectorAll(".filter").forEach((b) => b.classList.toggle("is-on", b.dataset.set === cur));
      shown = photos.filter((p) => cur === "All" || p.set === cur);
      host.innerHTML = shown.map((p, i) => `<a href="${esc(url(p.src))}" id="${esc(p.id)}" data-i="${i}"><img src="${esc(url(p.thumb))}" alt="${esc(p.alt)}" loading="lazy"><figcaption>${esc(p.alt)}</figcaption></a>`).join("");
    };
    setsEl.addEventListener("click", (e) => { const b = e.target.closest("[data-set]"); if (b) { cur = b.dataset.set; render(); } });
    host.addEventListener("click", (e) => { const a = e.target.closest("a[data-i]"); if (!a) return; e.preventDefault(); show(Number(a.dataset.i)); CC.openLayer(lb, "[data-lb-close]"); });
    lb.addEventListener("click", (e) => {
      if (e.target.closest("[data-lb-close]") || e.target === lb) CC.closeLayer(lb);
      const n = e.target.closest("[data-lb]");
      if (n) show(idx + Number(n.dataset.lb));
    });
    document.addEventListener("keydown", (e) => {
      if (!lb.classList.contains("is-open")) return;
      if (e.key === "Escape") CC.closeLayer(lb);
      if (e.key === "ArrowRight") show(idx + 1);
      if (e.key === "ArrowLeft") show(idx - 1);
    });
    render();
    const hash = location.hash.slice(1);
    const at = shown.findIndex((p) => p.id === hash);
    if (at >= 0) { show(at); CC.openLayer(lb, "[data-lb-close]"); }
  }

  /* ---------------- network ---------------- */
  function networkPage(data) {
    const map = document.getElementById("net-map");
    if (map) { map.innerHTML = CC.network(data); CC.wireNetwork(map); }
    const tier = (list, el) => {
      const host = document.getElementById(el);
      if (!host) return;
      host.innerHTML = list.map((s) => {
        const e = (data.episodes || []).find((x) => x.show === s.key);
        return `<a class="net__show${s.feature ? " net__show--feature" : ""}" href="${url(`pages/shows.html#${s.key}`)}" data-show="${s.key}">
          ${s.art ? `<img src="${esc(CC.art(s))}" alt="" loading="lazy">` : '<span class="ph"></span>'}
          <span><small>${esc((s.hosts || []).join(" & "))}${s.count ? ` · ${s.count} ${s.kind === "youtube" ? "videos" : "episodes"}` : ""}</small><b>${esc(s.name)}</b><em>${esc(s.tagline || (e ? "Latest: " + e.title : ""))}</em></span></a>`;
      }).join("");
    };
    tier(data.primary, "net-primary");
    tier(data.secondary, "net-secondary");
  }

  /* ---------------- shop ---------------- */
  function shop() {
    const host = document.getElementById("shop-items");
    if (!host) return;
    const money = (c) => (c == null ? "" : `$${(c / 100).toFixed(c % 100 ? 2 : 0)}`);
    const GROUPS = [["prints", "Photo prints", "Joshua's photographs, printed to hang."], ["janel-art", "Art by Janel", "Original work from Janel Moore."], ["joshua-art", "Art by Joshua", "Paintings and mixed media from Joshua German."], ["merch", "Merch", "Wear the network."], ["other", "More", ""]];
    const itemHTML = (it) => {
      const href = it.buy_url || (it.status === "coming-soon" ? `mailto:jgerms20@gmail.com?subject=${encodeURIComponent("Notify me: " + it.title)}` : "");
      const label = it.status === "sold-out" ? "Sold out" : it.status === "coming-soon" ? "Notify me" : it.price_cents != null ? `Buy · ${money(it.price_cents)}` : "See details";
      return `<article class="item${it.status === "coming-soon" ? " item--soon" : ""}">
        <div class="item__media">${it.image_url ? `<img src="${esc(url(it.image_url))}" alt="${esc(it.title)}" loading="lazy">` : `<span class="item__ph">${esc(it.status === "coming-soon" ? "Coming soon" : it.title)}</span>`}${it.status !== "available" ? `<span class="chip item__flag">${esc(it.status.replace("-", " "))}</span>` : ""}</div>
        <h3>${esc(it.title)}</h3>
        <p>${esc([it.artist, it.description].filter(Boolean).join(" · "))}</p>
        ${href ? `<a class="btn btn--sm${it.status === "available" ? "" : " btn--ghost"}" href="${esc(href)}"${/^https?:/.test(href) ? ' target="_blank" rel="noopener"' : ""}>${label}</a>` : `<span class="eyebrow">${label}</span>`}
      </article>`;
    };
    const render = (items) => {
      host.innerHTML = GROUPS.map(([k, t, d]) => {
        const list = items.filter((i) => i.category === k);
        if (!list.length) return "";
        return `<section class="shop-group rv"><div class="pill-row"><h2 class="pill-title${k === "prints" ? " pill-title--gold" : k === "janel-art" ? " pill-title--pink" : ""}">${t}</h2>${d ? `<span class="eyebrow">${esc(d)}</span>` : ""}</div><div class="items">${list.map(itemHTML).join("")}</div></section>`;
      }).join("");
      CC.reveal(host);
    };
    const { url: SB, key } = CC.SUPABASE;
    fetch(`${SB}/rest/v1/shop_items?select=*&status=neq.hidden&order=sort.asc,created_at.desc`, { headers: { apikey: key, Authorization: `Bearer ${key}` } })
      .then((r) => (r.ok ? r.json() : Promise.reject(r.status)))
      .then(render)
      .catch(() => { host.innerHTML = `<p class="search__empty">The shop is restocking. Check back soon, or <a class="pill-more" href="${url("pages/contact.html")}">ask us about a piece</a>.</p>`; });
    // Kindling products straight from the game's own shop config
    fetch(url("data/kindling-shop.json")).then((r) => (r.ok ? r.json() : null)).then((k) => {
      const el = document.getElementById("shop-kindling");
      if (!k || !el) return;
      el.innerHTML = k.products.map((p) => `<a class="kprod" href="${url(`kindling/shop.html#${p.id}`)}" data-deck="${esc(p.deck || p.id)}">
        <small>${esc(p.kind || "")}</small><b>${esc(p.name)}</b><span>${esc(p.cards || "")}</span><em>$${esc(p.price)}</em></a>`).join("");
    }).catch(() => {});
  }

  /* ---------------- about: live counts ---------------- */
  function about(data) {
    const el = document.getElementById("about-shows");
    if (!el) return;
    el.innerHTML = data.primary.map((s) => `<a class="tile" href="${url(`pages/shows.html#${s.key}`)}" data-show="${s.key}">
      <span class="show-tag" data-show="${s.key}"><i></i>${esc((s.hosts || []).join(" & "))}</span>
      <h3>${esc(s.name)}</h3><p>${esc(s.tagline || "")}</p></a>`).join("");
  }
})();
