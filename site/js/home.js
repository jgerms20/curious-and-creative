/* Curious & Creative — homepage interactions (assembled from section modules) */

/* ---------- 01-header ---------- */
/* 01-header — search overlay + drawer menu behavior.
   Scoped entirely to #site-header; no-ops silently if a node is missing. */
(() => {
  const root = document.getElementById("site-header");
  if (!root) return;

  const qs = (sel) => root.querySelector(sel);
  const qsa = (sel) => Array.from(root.querySelectorAll(sel));

  const searchTrigger = qs("#hdr-search-trigger");
  const searchOverlay = qs("#hdr-search-overlay");
  const searchClose = qs("#hdr-search-close");
  const searchInput = qs("#hdr-search-input");
  const searchEmpty = qs("#hdr-search-empty");
  const searchItems = qsa(".hdr-search-item");
  const searchGroups = qsa(".hdr-search-group");

  const burger = qs("#hdr-burger");
  const drawer = qs("#hdr-drawer");
  const drawerBackdrop = qs("#hdr-drawer-backdrop");
  const drawerClose = qs("#hdr-drawer-close");

  let scrollLocks = 0;
  const lockScroll = () => {
    scrollLocks += 1;
    document.documentElement.style.overflow = "hidden";
  };
  const unlockScroll = () => {
    scrollLocks = Math.max(0, scrollLocks - 1);
    if (scrollLocks === 0) document.documentElement.style.overflow = "";
  };

  let lastFocused = null;

  const focusableIn = (container) => {
    if (!container) return [];
    return Array.from(
      container.querySelectorAll(
        'a[href], button:not([disabled]), input:not([disabled]), [tabindex]:not([tabindex="-1"])'
      )
    ).filter((el) => el.offsetParent !== null);
  };

  const trapTab = (e, container) => {
    if (e.key !== "Tab") return;
    const list = focusableIn(container);
    if (!list.length) return;
    const first = list[0];
    const last = list[list.length - 1];
    if (e.shiftKey && document.activeElement === first) {
      e.preventDefault();
      last.focus();
    } else if (!e.shiftKey && document.activeElement === last) {
      e.preventDefault();
      first.focus();
    }
  };

  /* ---------- Search overlay ---------- */
  const openSearch = () => {
    if (!searchOverlay || !searchTrigger) return;
    lastFocused = document.activeElement;
    searchOverlay.hidden = false;
    searchTrigger.setAttribute("aria-expanded", "true");
    lockScroll();
    requestAnimationFrame(() => {
      searchOverlay.classList.add("is-open");
    });
    if (searchInput) {
      searchInput.value = "";
      filterQuickLinks("");
      window.setTimeout(() => searchInput.focus(), 60);
    }
  };

  const closeSearch = () => {
    if (!searchOverlay || !searchTrigger) return;
    searchOverlay.classList.remove("is-open");
    searchTrigger.setAttribute("aria-expanded", "false");
    unlockScroll();
    window.setTimeout(() => {
      searchOverlay.hidden = true;
    }, 260);
    if (lastFocused && typeof lastFocused.focus === "function") lastFocused.focus();
  };

  function filterQuickLinks(query) {
    const q = query.trim().toLowerCase();
    let anyVisible = false;
    searchGroups.forEach((group) => {
      let groupHasMatch = false;
      group.querySelectorAll("[data-label]").forEach((item) => {
        const label = (item.getAttribute("data-label") || "").toLowerCase();
        const match = q.length === 0 || label.includes(q);
        item.hidden = !match;
        if (match) groupHasMatch = true;
      });
      group.hidden = !groupHasMatch;
      if (groupHasMatch) anyVisible = true;
    });
    if (searchEmpty) searchEmpty.hidden = anyVisible || q.length === 0;
  }

  if (searchTrigger) searchTrigger.addEventListener("click", openSearch);
  if (searchClose) searchClose.addEventListener("click", closeSearch);
  if (searchOverlay) {
    searchOverlay.addEventListener("click", (e) => {
      if (e.target === searchOverlay) closeSearch();
    });
    searchOverlay.addEventListener("keydown", (e) => {
      if (e.key === "Escape") {
        closeSearch();
        return;
      }
      trapTab(e, searchOverlay);
    });
  }
  if (searchInput) {
    searchInput.addEventListener("input", (e) => filterQuickLinks(e.target.value));
  }
  if (searchItems.length === 0) {
    /* nothing to filter — guard no-ops silently */
  }

  /* ---------- Drawer menu ---------- */
  const openDrawer = () => {
    if (!drawer || !drawerBackdrop || !burger) return;
    lastFocused = document.activeElement;
    drawer.hidden = false;
    drawerBackdrop.hidden = false;
    burger.setAttribute("aria-expanded", "true");
    lockScroll();
    requestAnimationFrame(() => {
      drawer.classList.add("is-open");
      drawerBackdrop.classList.add("is-open");
    });
    window.setTimeout(() => {
      if (drawerClose) drawerClose.focus();
    }, 60);
  };

  const closeDrawer = () => {
    if (!drawer || !drawerBackdrop || !burger) return;
    drawer.classList.remove("is-open");
    drawerBackdrop.classList.remove("is-open");
    burger.setAttribute("aria-expanded", "false");
    unlockScroll();
    window.setTimeout(() => {
      drawer.hidden = true;
      drawerBackdrop.hidden = true;
    }, 320);
    if (lastFocused && typeof lastFocused.focus === "function") lastFocused.focus();
  };

  if (burger) burger.addEventListener("click", openDrawer);
  if (drawerClose) drawerClose.addEventListener("click", closeDrawer);
  if (drawerBackdrop) drawerBackdrop.addEventListener("click", closeDrawer);
  if (drawer) {
    drawer.addEventListener("keydown", (e) => {
      if (e.key === "Escape") {
        closeDrawer();
        return;
      }
      trapTab(e, drawer);
    });
    qsa(".hdr-drawer__link, .hdr-drawer__show").forEach((link) => {
      link.addEventListener("click", closeDrawer);
    });
  }

  /* ---------- Global Escape fallback (covers focus outside dialog) ---------- */
  document.addEventListener("keydown", (e) => {
    if (e.key !== "Escape") return;
    if (searchOverlay && !searchOverlay.hidden) closeSearch();
    if (drawer && !drawer.hidden) closeDrawer();
  });

  /* ---------- Subtle scrolled shadow ---------- */
  const headerEl = root;
  const onScroll = () => {
    if (window.scrollY > 4) headerEl.classList.add("hdr-header--scrolled");
    else headerEl.classList.remove("hdr-header--scrolled");
  };
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();
})();

/* ---------- 03-shelves ---------- */
(() => {
  // 03-shelves has no interactive behavior of its own — the hover-fade,
  // pulsing "special project" dot, and list hover states are pure CSS.
  // This guard exists only so the fragment is safe to include even if
  // the shell markup for #latest hasn't loaded yet.
  const root = document.getElementById('latest');
  if (!root) return;
})();

/* ---------- 04-videos ---------- */
(() => {
  /* 04-videos — radio-style episode list drives the featured player. */
  const root = document.getElementById("videos");
  if (!root) return;

  const items = Array.from(root.querySelectorAll(".vid-item"));
  const title = root.querySelector("#vid-featured-title");
  const dek = root.querySelector("#vid-featured-dek");
  const duration = root.querySelector("#vid-duration");
  if (!items.length) return;

  const activate = (item) => {
    items.forEach((i) => {
      const on = i === item;
      i.classList.toggle("is-active", on);
      i.setAttribute("aria-checked", on ? "true" : "false");
      i.tabIndex = on ? 0 : -1;
    });
    if (title) title.textContent = item.dataset.title || "";
    if (dek) dek.textContent = item.dataset.dek || "";
    if (duration) duration.innerHTML = item.dataset.duration || "&mdash;:&mdash;";
  };

  items.forEach((item, idx) => {
    item.addEventListener("click", () => activate(item));
    item.addEventListener("keydown", (e) => {
      let next = null;
      if (e.key === "ArrowDown" || e.key === "ArrowRight") next = items[(idx + 1) % items.length];
      if (e.key === "ArrowUp" || e.key === "ArrowLeft") next = items[(idx - 1 + items.length) % items.length];
      if (next) {
        e.preventDefault();
        activate(next);
        next.focus();
      }
    });
  });
})();

/* ---------- 05-ticker-shorts ---------- */
(() => {
  /* Duplicate the ticker card set once so translateX(-50%) loops seamlessly. */
  const track = document.querySelector("#universe [data-tick-track]");
  if (!track || track.dataset.cloned) return;
  track.dataset.cloned = "1";
  const cards = Array.from(track.children);
  cards.forEach((card) => {
    const clone = card.cloneNode(true);
    clone.setAttribute("aria-hidden", "true");
    clone.tabIndex = -1;
    clone.querySelectorAll("a, button").forEach((el) => (el.tabIndex = -1));
    track.appendChild(clone);
  });
})();

/* ---------- 06-podcasts-footer ---------- */
(() => {
  /* --- Podcast shuffle stack --- */
  const stack = document.querySelector("[data-pods-stack]");
  if (stack) {
    const cards = Array.from(stack.querySelectorAll(".pods-card"));
    const dots = Array.from(document.querySelectorAll("[data-pods-dot]"));
    let order = cards.map((_, i) => i);
    let busy = false;
    let timer = null;
    const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    const paint = () => {
      order.forEach((cardIdx, pos) => {
        const card = cards[cardIdx];
        card.className = card.className.replace(/\bpos-\d\b/g, "").trim();
        card.classList.add("pos-" + pos);
      });
      dots.forEach((d, i) => d.classList.toggle("is-on", i === order[0]));
    };

    const advance = (toFront) => {
      if (busy) return;
      busy = true;
      const front = cards[order[0]];
      front.classList.add("is-flying");
      window.setTimeout(() => {
        front.classList.remove("is-flying");
        if (typeof toFront === "number") {
          order = [toFront, ...order.filter((i) => i !== toFront)];
        } else {
          order.push(order.shift());
        }
        paint();
        busy = false;
      }, 300);
    };

    const rest = () => {
      if (timer) window.clearInterval(timer);
      if (!reduced) timer = window.setInterval(() => advance(), 6000);
    };

    const shuffleBtn = document.getElementById("pods-shuffle");
    if (shuffleBtn) shuffleBtn.addEventListener("click", () => { advance(); rest(); });
    dots.forEach((d, i) =>
      d.addEventListener("click", () => { if (order[0] !== i) { advance(i); } rest(); })
    );

    /* click (or start a drag on) the front card → next */
    stack.addEventListener("pointerdown", (e) => {
      const front = cards[order[0]];
      if (!front.contains(e.target)) return;
      if (e.target.closest("a")) return; /* let links work */
      advance();
      rest();
    });

    paint();
    rest();
  }

  /* --- Newsletter form shell --- */
  const form = document.querySelector("[data-nl-form]");
  const done = document.querySelector("[data-nl-done]");
  if (form && done) {
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      form.hidden = true;
      done.hidden = false;
    });
  }
})();
