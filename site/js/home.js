/* Homepage: the pitch and leg summaries are static HTML; this file fills the
   three data-driven slots (proof rail, flagship shows, inquiry form). */
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

  /* ---------------- 3. the Network: flagship shows ---------------- */
  CC.ready.then((data) => {
    const list = document.getElementById("flagships");
    if (!list) return;
    const shows = (CC.showOrder ? CC.showOrder(data.primary || []) : data.primary || []).filter((s) => !s.archive).slice(0, 5);
    if (!shows.length) { list.closest(".legsec__aside").hidden = true; return; }
    list.innerHTML = shows.map((s) => `<li data-show="${esc(s.key)}">
      <a class="flagship" href="${esc(CC.showHref(s))}">
        ${s.art ? `<img src="${esc(CC.art(s))}" alt="" loading="lazy">` : '<span class="ph" aria-hidden="true"></span>'}
        <span class="flagship__txt"><b>${esc(s.name)}</b>${s.tagline ? `<small>${esc(s.tagline)}</small>` : ""}</span>
        <span class="flagship__go" aria-hidden="true">→</span>
      </a>
    </li>`).join("");
  });
})();
