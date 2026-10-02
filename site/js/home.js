/* Homepage renderers — everything here is built from data/content.json. */
(() => {
  const CC = window.CC;
  const { esc, url, ago, dur, icon } = CC;
  const reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const ext = (h) => (/^https?:/.test(h) ? ' target="_blank" rel="noopener"' : "");
  const listenVerb = (e) => (e.kind === "video" || e.kind === "short" ? "Watch" : "Listen");

  CC.ready.then((data) => {
    const shows = data.shows;
    const by = data.byKey;
    const eps = (data.episodes || []).filter((e) => by[e.show]);
    const longform = eps.filter((e) => e.kind !== "short");

    /* counts in copy */
    const fresh = longform.filter((e) => CC.isNew(e.date)).length;
    document.querySelectorAll("[data-new-count]").forEach((el) => { el.textContent = fresh ? ` ${fresh}` : ""; });
    document.querySelectorAll("[data-ep-count]").forEach((el) => { el.textContent = eps.length || "All"; });

    hero(shows, by, longform, data);
    latest(by, longform, data);
    videos(by, eps);
    podcasts(shows, by, eps);
    shortsRail(by, eps);
    ticker(shows, by, eps, data);
    photoStrip(data.photos);
    CC.reveal();
  });

  /* ------------------------------------------------ hero carousel */
  function hero(shows, by, eps, data) {
    const stage = document.getElementById("hero");
    if (!stage) return;
    const slides = [];
    const flag = by.ccpod;
    if (flag) {
      const latest = eps.find((e) => e.show === "ccpod");
      const links = CC.showLinks(flag);
      slides.push({
        show: "ccpod",
        kicker: [`<span class="chip"><span class="dot dot--live"></span> The flagship</span>`, latest ? `<span class="chip">New · ${esc(ago(latest.date))}</span>` : `<span class="chip">Joshua &amp; Janel</span>`],
        title: flag.name,
        href: latest ? CC.epHref(latest) : url("pages/shows.html#ccpod"),
        dek: latest ? `Latest: ${latest.title}` : flag.about || flag.tagline,
        meta: `Hosted by Joshua German &amp; Janel Moore`,
        img: CC.art(flag),
        actions: [
          latest ? [`${icon.play} Play the latest`, CC.epHref(latest), "btn"] : links[0] ? [`${icon.play} Listen on ${links[0][0]}`, links[0][1], "btn"] : ["Get new episodes", "#newsletter", "btn"],
          ["About the show", url("pages/shows.html#ccpod"), "btn btn--ghost"],
        ],
      });
    }
    slides.push({
      kicker: [`<span class="chip">Who we are</span>`],
      title: "Two curious minds, one creative hub",
      href: url("pages/about.html"),
      dek: "Joshua German and Janel Moore make podcasts, videos, photography, and inventions — and help brands find their story. This is where all of it lives.",
      meta: "Est. by two University of South Carolina grads",
      img: url("assets/people/duo.jpg"),
      photo: true,
      actions: [["Our story", url("pages/about.html"), "btn"], ["Work with the studio", url("pages/studio.html"), "btn btn--ghost"]],
    });
    shows.filter((s) => s.key !== "ccpod" && !s.archive).forEach((s) => {
      const e = eps.find((x) => x.show === s.key);
      if (!e) return;
      slides.push({
        show: s.key,
        kicker: [`<span class="chip"><span class="dot" style="background:var(--c)"></span> ${esc(s.short || s.name)}</span>`, `<span class="chip">${e.kind === "video" ? "New video" : "New episode"} · ${esc(ago(e.date))}</span>`],
        title: e.title,
        href: CC.epHref(e),
        dek: e.description || s.tagline,
        meta: [(s.hosts || []).join(" & "), dur(e.duration)].filter(Boolean).map(esc).join(" · "),
        img: e.kind === "video" ? e.image : CC.art(s) || e.image,
        video: e.kind === "video",
        actions: [[`${icon.play} ${listenVerb(e)} now`, CC.epHref(e), "btn"], [`More ${esc(s.short || s.name)}`, url(`pages/shows.html#${s.key}`), "btn btn--ghost"]],
      });
    });
    if (data.photos && data.photos.length) {
      const p = data.photos.find((x) => x.set === "Portraits") || data.photos[0];
      slides.push({
        kicker: [`<span class="chip">Photography</span>`, `<span class="chip">${data.photos.length} frames</span>`],
        title: "Portraits, fashion & nights out — on film and digital",
        href: url("pages/art.html"),
        dek: "Joshua's photography: people, places, and live events from Los Angeles to Rio de Janeiro.",
        meta: "Now booking shoots",
        img: url(p.src),
        photo: true,
        actions: [["See the photography", url("pages/art.html"), "btn"], ["Book a shoot", "https://joshuamgerman.com/photography/", "btn btn--ghost"]],
      });
    }
    const S = slides.slice(0, 6);
    const DUR = 8000;

    stage.style.setProperty("--dur", `${DUR}ms`);
    stage.innerHTML = S.map((s, i) => `
      <article class="hero__slide${i === 0 ? " is-active" : ""}" data-show="${esc(s.show || "")}" aria-roledescription="slide" aria-label="${i + 1} of ${S.length}" ${i ? 'aria-hidden="true"' : ""}>
        <div class="hero__bed" style="background-image:url('${esc(s.img)}')"></div>
        <div class="hero__grain"></div>
        <div class="hero__grid">
          <div class="hero__copy">
            <div class="hero__kicker">${s.kicker.join("")}</div>
            ${i === 0 ? "<h1" : "<h2"} class="hero__title${s.title.length > 70 ? " hero__title--xl" : s.title.length > 42 ? " hero__title--l" : ""}"><a href="${esc(s.href)}"${ext(s.href)}>${esc(s.title)}</a>${i === 0 ? "</h1>" : "</h2>"}
            <p class="hero__dek">${esc(s.dek || "")}</p>
            <p class="hero__meta">${s.meta || ""}</p>
            <div class="hero__actions">${s.actions.map(([l, h, c]) => `<a class="${c}${c.includes("ghost") ? "" : ""}" href="${esc(h)}"${ext(h)}${c.includes("ghost") ? ' style="color:#fff"' : ""}>${l}</a>`).join("")}</div>
          </div>
          <a class="hero__cover${s.photo ? " hero__cover--photo" : ""}" href="${esc(s.href)}"${ext(s.href)} tabindex="-1" aria-hidden="true" style="${s.video ? "aspect-ratio:16/10" : ""}">${s.img ? `<img src="${esc(s.img)}" alt="" ${i ? 'loading="lazy"' : ""}>` : ""}</a>
        </div>
      </article>`).join("") + `
      <div class="hero__bars" role="tablist" aria-label="Choose slide">${S.map((s, i) => `<button class="hero__bar${i === 0 ? " is-active" : ""}" role="tab" aria-label="Slide ${i + 1}: ${esc(s.title)}"><span></span></button>`).join("")}</div>
      <div class="hero__nav">
        <div class="hero__arrows"><button type="button" data-dir="-1" aria-label="Previous slide">${icon.left}</button><button type="button" data-dir="1" aria-label="Next slide">${icon.right}</button></div>
        <div class="hero__next" aria-label="Up next"></div>
      </div>`;

    const slideEls = [...stage.querySelectorAll(".hero__slide")];
    const bars = [...stage.querySelectorAll(".hero__bar")];
    const next = stage.querySelector(".hero__next");
    let cur = 0, timer = null, paused = false;

    const renderNext = () => {
      const up = [1, 2, 3].map((k) => (cur + k) % S.length).filter((v, i, a) => v !== cur && a.indexOf(v) === i);
      next.innerHTML = up.map((k) => `<button class="hero__mini" type="button" data-go="${k}">${S[k].img ? `<img src="${esc(S[k].img)}" alt="">` : '<span class="ph"></span>'}<span><small>Up next</small><b>${esc(S[k].title)}</b></span></button>`).join("");
    };
    const go = (n) => {
      started = Date.now();
      remaining = DUR;
      cur = (n + S.length) % S.length;
      slideEls.forEach((el, i) => { el.classList.toggle("is-active", i === cur); el.setAttribute("aria-hidden", String(i !== cur)); });
      bars.forEach((b, i) => {
        b.classList.remove("is-active");
        b.classList.toggle("is-done", i < cur);
        b.setAttribute("aria-selected", String(i === cur));
      });
      void bars[cur].offsetWidth;
      bars[cur].classList.add("is-active");
      renderNext();
      schedule();
    };
    const schedule = () => {
      clearTimeout(timer);
      if (reduced || paused || S.length < 2) return;
      timer = setTimeout(() => go(cur + 1), DUR);
    };
    let remaining = DUR, started = Date.now();
    const pause = () => { if (paused) return; paused = true; stage.classList.add("is-paused"); clearTimeout(timer); remaining = Math.max(800, DUR - (Date.now() - started)); };
    const resume = () => { if (!paused) return; paused = false; stage.classList.remove("is-paused"); clearTimeout(timer); if (!reduced) timer = setTimeout(() => go(cur + 1), remaining); };
    const goTracked = go;

    stage.addEventListener("click", (e) => {
      const b = e.target.closest(".hero__bar, [data-dir], [data-go]");
      if (!b) return;
      if (b.matches(".hero__bar")) goTracked(bars.indexOf(b));
      else if (b.dataset.dir) goTracked(cur + Number(b.dataset.dir));
      else goTracked(Number(b.dataset.go));
    });
    stage.addEventListener("mouseenter", pause);
    stage.addEventListener("mouseleave", resume);
    stage.addEventListener("focusin", pause);
    stage.addEventListener("focusout", (e) => { if (!stage.contains(e.relatedTarget)) resume(); });
    document.addEventListener("visibilitychange", () => (document.hidden ? pause() : resume()));
    let x0 = null;
    stage.addEventListener("touchstart", (e) => { x0 = e.touches[0].clientX; }, { passive: true });
    stage.addEventListener("touchend", (e) => { if (x0 === null) return; const dx = e.changedTouches[0].clientX - x0; if (Math.abs(dx) > 50) goTracked(cur + (dx < 0 ? 1 : -1)); x0 = null; });
    stage.addEventListener("keydown", (e) => { if (e.key === "ArrowRight") goTracked(cur + 1); if (e.key === "ArrowLeft") goTracked(cur - 1); });
    goTracked(0);
  }

  /* ------------------------------------------------ the latest */
  const mediaHTML = (e, s, cls = "") => {
    const isVid = e.kind === "video" || e.kind === "short";
    const img = isVid ? e.image : e.image || CC.art(s);
    return `<div class="card__media art ${isVid ? "art--video" : "art--contain"} ${cls}">
      ${!isVid && img ? `<div class="art__bed" style="background-image:url('${esc(img)}')"></div>` : ""}
      ${img ? `<img src="${esc(img)}" alt="" loading="lazy">` : `<span class="art__fx">${esc(s.short || s.name)}</span>`}
      <span class="card__badge chip">${isVid ? "Video" : "Episode"}</span>
      ${e.duration ? `<span class="card__dur">${esc(dur(e.duration))}</span>` : ""}
      <span class="card__play">${icon.play}</span>
    </div>`;
  };
  const card = (e, by, lead) => {
    const s = by[e.show] || {};
    const h = CC.epHref(e);
    return `<a class="card rv${lead ? " card--lead" : ""}" href="${esc(h)}"${ext(h)} data-show="${esc(e.show)}">
      ${mediaHTML(e, s)}
      <span class="show-tag" data-show="${esc(e.show)}"><i></i>${esc(s.short || s.name)}</span>
      <h3 class="card__title">${esc(e.title)}</h3>
      ${lead && e.description ? `<p class="card__desc">${esc(e.description)}</p>` : ""}
      <p class="card__meta"><span>${esc(ago(e.date))}</span>${e.duration ? `<span>${esc(dur(e.duration))}</span>` : ""}<span>${listenVerb(e)} ↗</span></p>
    </a>`;
  };

  function latest(by, eps, data) {
    const grid = document.getElementById("latest-grid");
    if (!grid) return;
    if (!eps.length) { grid.innerHTML = `<p class="eyebrow">New episodes load here automatically.</p>`; return; }
    // one per show first so a busy show can't crowd the shelf, then fill by date
    const seen = new Set(), picks = [];
    eps.forEach((e) => { if (!seen.has(e.show)) { seen.add(e.show); picks.push(e); } });
    eps.forEach((e) => { if (picks.length < 8 && !picks.includes(e)) picks.push(e); });
    picks.sort((a, b) => String(b.date).localeCompare(String(a.date)));
    const cards = picks.slice(0, 7);
    const perShow = data.shows.map((s) => [s, eps.find((e) => e.show === s.key)]).filter(([, e]) => e);
    const photo = data.photos && data.photos.find((p) => p.set === "Events & Live") || (data.photos || [])[0];
    let html = card(cards[0], by, true) + cards.slice(1, 5).map((e) => card(e, by)).join("");
    html += `<a class="special special--gold rv" href="${url("pages/inventions.html")}">
      <span class="special__label"><span class="dot dot--live"></span> Special project</span>
      <span class="special__title">Kindling</span>
      <span>Our first invention, now in development under the Curious &amp; Creative umbrella.</span>
      <span class="special__go">See what we're building ${icon.arrow}</span></a>`;
    if (photo) html += `<a class="special special--photo rv" href="${url("pages/art.html")}"><img src="${esc(url(photo.thumb))}" alt="${esc(photo.alt)}" loading="lazy"><span class="special__in"><span class="special__label">Photography</span><span class="special__title" style="font-size:1.6rem">${esc(photo.set)}</span><span class="special__go">Open the gallery ${icon.arrow}</span></span></a>`;
    html += `<div class="list-card rv"><div class="list-card__head"><span>Fresh from every show</span><span>${perShow.length}</span></div><ol>
      ${perShow.map(([s, e]) => `<li data-show="${s.key}"><a href="${esc(CC.epHref(e))}"${ext(CC.epHref(e))}><span>${esc(e.title)}<small>${esc(s.short || s.name)} · ${esc(ago(e.date))}</small></span></a></li>`).join("")}
    </ol></div>`;
    grid.innerHTML = html;
  }

  /* ------------------------------------------------ videos */
  function videos(by, eps) {
    const host = document.getElementById("vid");
    const section = document.getElementById("videos");
    const vids = eps.filter((e) => e.kind === "video");
    if (!host) return;
    if (!vids.length) { section.hidden = true; return; }
    const show = by[vids[0].show] || {};
    host.innerHTML = `
      <div>
        <p class="vid__label"><span>${esc(show.name || "Videos")}</span><a href="${esc(show.youtube_url || "#")}" target="_blank" rel="noopener">Channel ↗</a></p>
        <div class="vid__listwrap">
          <div class="vid__list" role="listbox" aria-label="Episodes">
            ${vids.map((v, i) => `<button class="vid__item${i ? "" : " is-active"}" type="button" role="option" aria-selected="${!i}" data-i="${i}">
              <span class="vid__thumb"><img src="${esc(v.image)}" alt="" loading="lazy"></span>
              <span><span class="vid__t">${esc(v.title)}</span><span class="vid__m">${esc(ago(v.date))}</span></span>
            </button>`).join("")}
          </div>
          <a class="btn vid__all" href="${url("pages/archive.html?show=approachable")}">All videos ${icon.arrow}</a>
        </div>
      </div>
      <div class="vid__main">
        <div class="vid__player" id="vid-player"></div>
        <h3 class="vid__ftitle" id="vid-title"></h3>
        <p class="vid__fdek" id="vid-dek"></p>
        <div class="vid__links" id="vid-links"></div>
      </div>`;
    const player = host.querySelector("#vid-player");
    const setVid = (i, autoplay) => {
      const v = vids[i];
      host.querySelectorAll(".vid__item").forEach((b, k) => { b.classList.toggle("is-active", k === i); b.setAttribute("aria-selected", String(k === i)); });
      host.querySelector("#vid-title").textContent = v.title;
      host.querySelector("#vid-dek").textContent = v.description || "";
      host.querySelector("#vid-links").innerHTML = `<a class="btn btn--light btn--sm" href="${esc(v.url)}" target="_blank" rel="noopener">Watch on YouTube ↗</a><span class="chip">${esc(ago(v.date))}</span>`;
      if (autoplay && v.youtube_id) {
        player.innerHTML = `<iframe src="https://www.youtube-nocookie.com/embed/${encodeURIComponent(v.youtube_id)}?autoplay=1&rel=0" title="${esc(v.title)}" allow="autoplay; encrypted-media; picture-in-picture; fullscreen" allowfullscreen></iframe>`;
      } else {
        player.innerHTML = `<img class="vid__poster" src="${esc(v.youtube_id ? `https://i.ytimg.com/vi/${v.youtube_id}/maxresdefault.jpg` : v.image)}" onerror="this.onerror=null;this.src='${esc(v.image)}'" alt=""><button class="vid__playbtn" type="button" aria-label="Play ${esc(v.title)}"><span>${icon.play}</span></button>`;
        player.querySelector(".vid__playbtn").addEventListener("click", () => setVid(i, true));
      }
    };
    host.querySelectorAll(".vid__item").forEach((b) => b.addEventListener("click", () => setVid(Number(b.dataset.i), false)));
    setVid(0, false);
  }

  /* ------------------------------------------------ podcasts stack */
  function podcasts(shows, by, eps) {
    const stack = document.getElementById("pods-stack");
    const list = document.getElementById("pods-list");
    if (!stack || !shows.length) return;
    const latestOf = (k) => eps.find((e) => e.show === k && e.kind !== "short");
    const wave = '<span class="wave" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i></span>';
    stack.innerHTML = shows.map((s) => {
      const e = latestOf(s.key);
      return `<article class="pcard" data-show="${s.key}" aria-label="${esc(s.name)}">
        <div class="pcard__row">${wave}<div class="pcard__art">${s.art ? `<img src="${esc(CC.art(s))}" alt="${esc(s.name)} cover art" loading="lazy">` : ""}</div>${wave}</div>
        <h4 class="pcard__name">${esc(s.name)}</h4>
        <p class="pcard__host">${esc((s.hosts || []).join(" · "))}</p>
        <p class="pcard__latest">${e ? `Latest: ${esc(e.title)}` : esc(s.tagline || "")}</p>
        <div class="pcard__links">${CC.showLinks(s).map(([l, h]) => `<a href="${esc(h)}" target="_blank" rel="noopener">${esc(l)}</a>`).join("")}<a href="${url(`pages/shows.html#${s.key}`)}">Episodes</a></div>
      </article>`;
    }).join("");
    list.innerHTML = shows.map((s, i) => {
      const fresh = s.latest ? (CC.isNew(s.latest) ? `<span class="pods__fresh is-new"><span class="dot dot--live"></span>New</span>` : `<span class="pods__fresh">${esc(ago(s.latest))}</span>`) : `<span class="pods__fresh">${s.flagship ? "Flagship" : "On Spotify"}</span>`;
      return `<button class="pods__row${i ? "" : " is-on"}" type="button" data-show="${s.key}" data-i="${i}">
        ${s.art ? `<img src="${esc(CC.art(s))}" alt="" loading="lazy">` : '<span class="ph"></span>'}
        <span><b>${esc(s.name)}</b><small>${esc((s.hosts || []).join(" & "))}${s.count ? ` · ${s.count} ${s.kind === "youtube" ? "videos" : "episodes"}` : ""}</small></span>
        ${fresh}</button>`;
    }).join("");

    const cards = [...stack.querySelectorAll(".pcard")];
    const rows = [...list.querySelectorAll(".pods__row")];
    let order = cards.map((_, i) => i), busy = false, timer = null;
    const paint = () => {
      order.forEach((ci, pos) => { cards[ci].className = cards[ci].className.replace(/\s?pos-\d/g, "") + ` pos-${Math.min(pos, 3)}`; cards[ci].setAttribute("aria-hidden", String(pos !== 0)); });
      rows.forEach((r, i) => r.classList.toggle("is-on", i === order[0]));
    };
    const advance = (to) => {
      if (busy) return;
      busy = true;
      const front = cards[order[0]];
      front.classList.add("is-flying");
      setTimeout(() => {
        front.classList.remove("is-flying");
        order = typeof to === "number" ? [to, ...order.filter((i) => i !== to)] : [...order.slice(1), order[0]];
        paint();
        busy = false;
      }, reduced ? 0 : 320);
    };
    const restart = () => { clearInterval(timer); if (!reduced) timer = setInterval(() => advance(), 7000); };
    document.getElementById("pods-shuffle").addEventListener("click", () => { advance(order[1 + Math.floor(Math.random() * (order.length - 1))]); restart(); });
    rows.forEach((r, i) => r.addEventListener("click", () => { if (order[0] !== i) advance(i); restart(); }));
    stack.addEventListener("click", (e) => { if (e.target.closest("a")) return; if (e.target.closest(".pcard.pos-0")) { advance(); restart(); } });
    paint();
    restart();
    new IntersectionObserver(([en]) => (en.isIntersecting ? restart() : clearInterval(timer))).observe(stack);
  }

  /* ------------------------------------------------ shorts */
  function shortsRail(by, eps) {
    const shorts = eps.filter((e) => e.kind === "short");
    const sec = document.getElementById("shorts");
    if (!sec || !shorts.length) return;
    sec.hidden = false;
    document.getElementById("shorts-rail").innerHTML = shorts.slice(0, 12).map((v) => `<a class="short" href="${esc(v.url)}" target="_blank" rel="noopener"><img src="https://i.ytimg.com/vi/${esc(v.youtube_id)}/oardefault.jpg" onerror="this.onerror=null;this.src='${esc(v.image)}'" alt="" loading="lazy"><span class="short__cap">${esc(v.title)}</span></a>`).join("");
  }

  /* ------------------------------------------------ ticker */
  function ticker(shows, by, eps, data) {
    const track = document.getElementById("tick");
    if (!track) return;
    const tilts = [-5, 3, -2, 5, -4, 2, -6, 4, -3, 6];
    const items = [];
    shows.forEach((s) => {
      const e = eps.find((x) => x.show === s.key);
      items.push(`<a class="tcard" data-show="${s.key}" href="${url(`pages/shows.html#${s.key}`)}">${s.art ? `<img class="tcard__art" src="${esc(CC.art(s))}" alt="" loading="lazy">` : ""}<b>${esc(s.name)}</b><small>${e ? `${e.kind === "video" ? "New video" : "Latest"} · ${esc(ago(e.date))}` : esc(s.tagline || "")}</small></a>`);
    });
    const total = eps.length;
    items.splice(1, 0, `<a class="tcard tcard--green" href="${url("pages/archive.html")}"><span class="tcard__big">${total}</span><b>episodes &amp; videos across ${shows.length} shows</b></a>`);
    items.splice(3, 0, `<a class="tcard tcard--gold" href="${url("pages/about.html")}"><b style="font-size:1.15rem">“Everything is interesting when you dig deep enough.”</b><small>— The Eclectic Polymath</small></a>`);
    (data.photos || []).filter((_, i) => i % 4 === 0).slice(0, 4).forEach((p, i) => items.splice(4 + i * 3, 0, `<a class="tcard tcard--photo" href="${url(`pages/art.html#${p.id}`)}"><img src="${esc(url(p.thumb))}" alt="${esc(p.alt)}" loading="lazy"></a>`));
    items.push(`<a class="tcard tcard--dark" href="${url("pages/inventions.html")}"><small>Invention No. 1</small><b style="font-size:1.6rem">Kindling</b><small>In development →</small></a>`);
    items.push(`<a class="tcard tcard--pink" href="#newsletter"><b style="font-size:1.2rem">Get new episodes in your inbox</b><small>Join the newsletter ↓</small></a>`);
    const set = items.map((h, i) => h.replace('class="tcard', `style="--tilt:${tilts[i % tilts.length]}deg" class="tcard`)).join("");
    track.innerHTML = set + set.replace(/<a /g, '<a tabindex="-1" aria-hidden="true" ');
  }

  /* ------------------------------------------------ photography strip */
  function photoStrip(photos) {
    const sec = document.getElementById("photography");
    if (!sec || !photos || !photos.length) return;
    // round-robin across sets so the strip shows range
    const sets = {};
    photos.forEach((p) => (sets[p.set] = sets[p.set] || []).push(p));
    const pick = [];
    for (let i = 0; pick.length < 9 && i < 12; i++) Object.values(sets).forEach((arr) => { if (arr[i] && pick.length < 9) pick.push(arr[i]); });
    sec.hidden = false;
    document.getElementById("photo-strip").innerHTML = pick.map((p) => `<a href="${url(`pages/art.html#${p.id}`)}"><img src="${esc(url(p.thumb))}" alt="${esc(p.alt)}" loading="lazy"><span class="chip">${esc(p.set)}</span></a>`).join("");
  }
})();
