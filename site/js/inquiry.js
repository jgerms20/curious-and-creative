/* Inquiry form: CC.mountInquiry(el, { leg }) renders the company inquiry form into el.
   Submissions are saved to the Supabase "inquiries" table (anyone can insert, only the team can
   read; see the create_inquiries migration) and answered from admin@curiousandcreative.co.
   Nothing depends on the visitor's email app. */
(() => {
  const CC = window.CC || (window.CC = {});
  const INBOX = "admin@curiousandcreative.co";
  const LEGS = [["network", "The Network"], ["studio", "The Studio"], ["consultancy", "The Consultancy"], ["other", "Not sure yet"]];
  // older links still say ?topic=…; send them to the right part of the house
  const TOPIC_LEG = {
    request: "network", guest: "network", podcast: "network", network: "network",
    photo: "studio", video: "studio", editing: "studio", events: "studio", website: "studio", project: "studio", studio: "studio",
    strategy: "consultancy", ai: "consultancy", social: "consultancy", consultancy: "consultancy",
  };
  const BUDGETS = ["Under $1,000", "$1,000 to $5,000", "$5,000 to $15,000", "$15,000 to $50,000", "$50,000+", "Not sure yet"];
  const TIMELINES = ["This week", "Within a month", "In 1 to 3 months", "Later than that", "Just exploring"];
  const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);
  let n = 0;

  CC.mountInquiry = (el, opts = {}) => {
    if (!el) return;
    const id = `inq${++n}`;
    const q = new URLSearchParams(location.search);
    const preset = opts.leg || q.get("leg") || TOPIC_LEG[q.get("topic")] || "";
    el.innerHTML = `
      <form class="inq" novalidate>
        <fieldset class="inq__legs">
          <legend>Which part of the house?</legend>
          ${LEGS.map(([v, l]) => `<label class="inq__leg"><input type="radio" name="leg" value="${v}"${v === preset ? " checked" : ""} required><span>${l}</span></label>`).join("")}
        </fieldset>
        <div class="inq__grid">
          <label>Name<input name="name" required maxlength="200" autocomplete="name"></label>
          <label>Email<input name="email" type="email" required maxlength="320" autocomplete="email"></label>
          <label>Date or date range<input name="dates" maxlength="200" placeholder="e.g. Dec 12, or early 2027"></label>
          <label>Location<input name="location" maxlength="200" placeholder="City, venue, or remote"></label>
          <label class="inq__wide">Deliverables needed<textarea name="deliverables" maxlength="4000" rows="3" placeholder="What should exist when we're done?"></textarea></label>
          <label>Budget range<select name="budget"><option value="">Choose one</option>${BUDGETS.map((b) => `<option>${esc(b)}</option>`).join("")}</select></label>
          <label>Decision timeline<select name="timeline"><option value="">Choose one</option>${TIMELINES.map((t) => `<option>${esc(t)}</option>`).join("")}</select></label>
          <label class="inq__wide">Anything else<textarea name="message" maxlength="4000" rows="3"></textarea></label>
          <label class="inq__hp" aria-hidden="true">Leave this empty<input name="company_url" tabindex="-1" autocomplete="off"></label>
        </div>
        <p class="inq__status" role="status" aria-live="polite"></p>
        <button class="btn" type="submit">Send inquiry</button>
        <p class="inq__note">It goes straight to our shared inbox, ${INBOX}. No email app needed.</p>
      </form>`;
    const f = el.querySelector("form");
    const status = f.querySelector(".inq__status");
    const say = (msg, kind) => { status.textContent = msg; status.dataset.kind = kind || ""; };
    f.addEventListener("submit", async (e) => {
      e.preventDefault();
      if (f.company_url.value) return; // a bot filled the hidden field
      const leg = (f.querySelector("input[name=leg]:checked") || {}).value;
      if (!leg) { say("Pick the part of the house this belongs in.", "error"); f.querySelector("input[name=leg]").focus(); return; }
      if (!f.reportValidity()) return;
      const row = { leg, page: location.pathname.slice(0, 300) };
      ["name", "email", "dates", "location", "deliverables", "budget", "timeline", "message"].forEach((k) => { const v = f[k].value.trim(); if (v) row[k] = v; });
      const btn = f.querySelector("button[type=submit]");
      btn.disabled = true;
      say("Sending…");
      try {
        const sb = CC.SUPABASE;
        const r = await fetch(`${sb.url}/rest/v1/inquiries`, {
          method: "POST",
          headers: { apikey: sb.key, Authorization: `Bearer ${sb.key}`, "Content-Type": "application/json", Prefer: "return=minimal" },
          body: JSON.stringify(row),
        });
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        f.reset();
        f.querySelectorAll(".inq__grid, .inq__legs, button[type=submit], .inq__note").forEach((x) => { x.hidden = true; });
        say(`Thank you, it's in. We'll reply from ${INBOX}.`, "ok");
      } catch (err) {
        btn.disabled = false;
        say(`That didn't send. Please email us at ${INBOX} instead.`, "error");
      }
    });
  };
})();
