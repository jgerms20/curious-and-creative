/* Homepage: the copy is static HTML; this file fills the data-driven slots
   (proof rail, Network covers, Studio mosaic, inquiry form). */
(() => {
  const CC = window.CC;
  if (!CC) return;
  const { esc } = CC;

  /* ---------------- 2. selected proof (company work only) ---------------- */
  const rail = document.getElementById("proof-rail");
  if (rail) {
    const slot = rail.closest("[data-slot]");
    // cases.js renders nothing (and hides the slot) when there is no matching work
    if (typeof CC.renderCases === "function") CC.renderCases(rail, { variant: "rail", limit: 6 });
    else if (slot) slot.hidden = true;
  }

  /* ---------------- 7. contact: inquiry form ---------------- */
  const inquiry = document.getElementById("inquiry");
  if (inquiry && typeof CC.mountInquiry === "function") {
    inquiry.innerHTML = "";
    CC.mountInquiry(inquiry);
  }

  /* ---------------- 1 + 3. the Network: leg-card covers and the cover wall ---------------- */
  CC.ready.then((data) => {
    const shows = (data.shows || []).filter((s) => s.art);
    // the flagship tier (primary, still running) first and larger, then everything else
    const big = (s) => s.tier !== "secondary" && !s.archive;
    const ordered = [...shows.filter(big), ...shows.filter((s) => !big(s))];

    const leg = document.getElementById("leg-covers");
    if (leg) leg.innerHTML = ordered.slice(0, 12).map((s) => `<img src="${esc(CC.art(s))}" alt="" loading="lazy">`).join("");

    const wall = document.getElementById("cover-wall");
    if (!wall) return;
    if (!ordered.length) { wall.hidden = true; return; }
    wall.innerHTML = ordered.map((s) => `<li class="${big(s) ? "wall__big" : ""}" data-show="${esc(s.key)}">
      <a href="${esc(CC.showHref(s))}"><img src="${esc(CC.art(s))}" alt="${esc(s.name)}" loading="lazy" width="300" height="300"></a>
    </li>`).join("");
  });

  /* ---------------- 4. the Studio: photo mosaic from photos.json ---------------- */
  const mosaic = document.getElementById("studio-mosaic");
  if (mosaic) {
    // event work leads (the specialty), then portraits and fashion; skip photos already on the page
    const PICK = ["events-jmg_2254", "events-jmg_7895", "fashion-jmg_8075", "events-jmg_2854", "portraits-jmg_8929",
      "events-dsc00021", "fashion-jmg_3641", "portraits-jmg_6968", "events-dsc00028"];
    const SETS = ["Events & Live", "Portraits", "Fashion"];
    const onPage = new Set([...document.images].map((i) => i.getAttribute("src")));
    fetch(CC.url("data/photos.json"), { cache: "no-cache" })
      .then((r) => (r.ok ? r.json() : null))
      .catch(() => null)
      .then((json) => {
        const all = ((json && json.photos) || []).filter((p) => !onPage.has(p.thumb) && !onPage.has(p.src));
        const byId = Object.fromEntries(all.map((p) => [p.id, p]));
        const picked = PICK.map((id) => byId[id]).filter(Boolean);
        all.filter((p) => SETS.includes(p.set) && !picked.includes(p)).forEach((p) => { if (picked.length < PICK.length) picked.push(p); });
        if (!picked.length) { mosaic.hidden = true; return; }
        mosaic.innerHTML = picked.map((p, i) => `<figure class="mosaic__tile${i === 0 ? " mosaic__tile--lead" : ""}">
          <img src="${esc(CC.url(i === 0 ? p.src : p.thumb))}" alt="${esc(p.alt || "")}" loading="lazy">
          ${i === 0 ? `<figcaption><b>Event Coverage</b> Documentary stills and video, captured as the room actually felt.</figcaption>` : ""}
        </figure>`).join("");
      });
  }
})();
