/* Backstage — private planning for Joshua & Janel.
   Auth + data: Supabase (project "curious-and-creative"). Access is enforced
   in the database: only emails in public.team_members can read or write. */
(() => {
  const SUPABASE_URL = "https://zsgacmfbqqmbcexomyoo.supabase.co";
  const SUPABASE_KEY = "sb_publishable_2GNNUjTGciy6Wi_wxDuStg_tY1sP28y";
  if (!window.supabase) {
    document.getElementById("auth-msg").innerHTML = '<p class="bs-msg bs-msg--err">Couldn\'t load the sign-in service. Check your connection (or an ad-blocker) and refresh.</p>';
    return;
  }
  const sb = window.supabase.createClient(SUPABASE_URL, SUPABASE_KEY, { auth: { persistSession: true, detectSessionInUrl: true } });

  const $ = (s, el = document) => el.querySelector(s);
  const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const iso = (d) => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
  const today = iso(new Date());
  const nice = (s) => (s ? new Date(s + (s.length === 10 ? "T12:00:00" : "")).toLocaleDateString("en-US", { weekday: "short", month: "short", day: "numeric" }) : "");

  const STATUSES = [["idea", "Ideas"], ["booked", "Booked"], ["prep", "Prep"], ["recorded", "Recorded"], ["editing", "Editing"], ["scheduled", "Scheduled"], ["published", "Published"]];
  const KINDS = ["recording", "release", "meeting", "shoot", "deadline", "other"];
  const AREAS = ["shows", "studio", "photography", "inventions", "site", "other"];
  let SHOWS = [{ key: "ccpod", name: "The Curious & Creative Podcast" }];
  let PUBLIC = { episodes: [] };
  let TEAM = [];
  let me = null;
  let tab = "overview";
  let calMonth = new Date(); calMonth.setDate(1);
  let taskFilter = "open";

  /* theme */
  $("#bs-theme").addEventListener("click", () => {
    const t = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
    document.documentElement.dataset.theme = t;
    try { localStorage.setItem("cc-theme", t); } catch (e) { /* storage blocked */ }
  });

  /* public site data: show list + published episodes */
  fetch("../data/content.json", { cache: "no-cache" }).then((r) => (r.ok ? r.json() : null)).then((d) => {
    if (!d) return;
    PUBLIC = d;
    SHOWS = d.shows.map((s) => ({ key: s.key, name: s.name }));
    if (me) render();
  }).catch(() => {});
  const showName = (k) => (SHOWS.find((s) => s.key === k) || {}).name || k || "";

  /* ---------------- auth ---------------- */
  let mode = "signin";
  const authMsg = (text, kind = "") => { $("#auth-msg").innerHTML = text ? `<p class="bs-msg ${kind ? "bs-msg--" + kind : ""}">${text}</p>` : ""; };
  const setMode = (m) => {
    mode = m;
    $("#auth-title").textContent = { signin: "Sign in to backstage", signup: "Create your login", reset: "Reset your password", update: "Choose a new password" }[m];
    $("#auth-go").textContent = { signin: "Sign in", signup: "Create login", reset: "Email me a reset link", update: "Save password" }[m];
    $("#pw-wrap").hidden = m === "reset";
    $("#auth-form").email.closest("label").hidden = m === "update";
    $("#auth-form").password.required = m !== "reset";
    $("#auth-form").password.autocomplete = m === "signin" ? "current-password" : "new-password";
    document.querySelectorAll(".bs-auth__switch button").forEach((b) => { b.hidden = b.dataset.mode === m || (m !== "signin" && b.dataset.mode !== "signin"); });
    authMsg("");
  };
  document.querySelectorAll(".bs-auth__switch button").forEach((b) => b.addEventListener("click", () => setMode(b.dataset.mode)));

  $("#auth-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const f = e.target;
    const email = f.email.value.trim().toLowerCase();
    const password = f.password.value;
    const back = location.href.split("#")[0].split("?")[0];
    authMsg("Working…");
    let res;
    if (mode === "signin") res = await sb.auth.signInWithPassword({ email, password });
    else if (mode === "signup") res = await sb.auth.signUp({ email, password, options: { emailRedirectTo: back } });
    else if (mode === "reset") res = await sb.auth.resetPasswordForEmail(email, { redirectTo: back });
    else if (mode === "update") res = await sb.auth.updateUser({ password });
    if (res.error) return authMsg(esc(res.error.message), "err");
    if (mode === "signup" && !res.data.session) return authMsg("Check your inbox to confirm your email, then come back here and sign in.", "ok");
    if (mode === "reset") return authMsg("Reset link sent. Open it on this device to set a new password.", "ok");
    if (mode === "update") { authMsg(""); setMode("signin"); }
  });

  $("#bs-signout").addEventListener("click", () => sb.auth.signOut());

  sb.auth.onAuthStateChange(async (event, session) => {
    if (event === "PASSWORD_RECOVERY") { showAuth(); setMode("update"); return; }
    if (!session) { me = null; showAuth(); return; }
    me = session.user;
    const { data: ok } = await sb.rpc("is_team");
    if (!ok) {
      showAuth();
      authMsg(`You're signed in as <b>${esc(me.email)}</b>, but that email isn't on the team yet. Ask Joshua to add it under <b>Team</b>.`, "err");
      $("#bs-signout").hidden = false;
      return;
    }
    showApp();
  });

  function showAuth() {
    $("#bs-auth").hidden = false;
    $("#bs-app").hidden = true;
    $("#bs-signout").hidden = !me;
    $("#bs-who").textContent = "";
  }
  function showApp() {
    $("#bs-auth").hidden = true;
    $("#bs-app").hidden = false;
    $("#bs-signout").hidden = false;
    $("#bs-who").textContent = me.email;
    render();
  }

  /* ---------------- data ---------------- */
  const load = async (table, order = "created_at", asc = false) => {
    const { data, error } = await sb.from(table).select("*").order(order, { ascending: asc });
    if (error) { console.error(error); return []; }
    return data;
  };
  const save = async (table, row) => {
    const { id, ...rest } = row;
    Object.keys(rest).forEach((k) => { if (rest[k] === "") rest[k] = null; });
    const q = id ? sb.from(table).update(rest).eq("id", id) : sb.from(table).insert(rest);
    const { error } = await q;
    if (error) alert(error.message);
    return !error;
  };
  const remove = async (table, id) => {
    const { error } = await sb.from(table).delete().eq("id", id);
    if (error) alert(error.message);
  };

  /* ---------------- tabs ---------------- */
  document.querySelectorAll(".bs-tabs [data-tab]").forEach((b) => b.addEventListener("click", () => {
    tab = b.dataset.tab;
    document.querySelectorAll(".bs-tabs [data-tab]").forEach((x) => x.setAttribute("aria-selected", String(x === b)));
    render();
  }));

  async function render() {
    if (!me) return;
    const v = $("#bs-view");
    TEAM = await load("team_members", "added_at", true);
    if (tab === "overview") v.innerHTML = await overview();
    if (tab === "calendar") v.innerHTML = await calendar();
    if (tab === "episodes") v.innerHTML = await episodes();
    if (tab === "tasks") v.innerHTML = await tasks();
    if (tab === "ideas") v.innerHTML = await ideas();
    if (tab === "team") v.innerHTML = team();
    wire(v);
  }

  const showOpts = (sel) => SHOWS.map((s) => `<option value="${s.key}"${s.key === sel ? " selected" : ""}>${esc(s.name)}</option>`).join("") + `<option value=""${!sel ? " selected" : ""}>— Not show-specific —</option>`;
  const peopleOpts = (sel) => `<option value="">Unassigned</option>` + TEAM.map((t) => `<option${t.name === sel ? " selected" : ""}>${esc(t.name)}</option>`).join("") + `<option${sel === "Both" ? " selected" : ""}>Both</option>`;

  /* ---------------- overview ---------------- */
  async function overview() {
    const [eps, evs, tks] = await Promise.all([load("episodes", "updated_at"), load("events", "starts_on", true), load("tasks", "due_on", true)]);
    const soon = evs.filter((e) => e.starts_on >= today).slice(0, 6);
    const open = tks.filter((t) => !t.done);
    const inFlight = eps.filter((e) => !["idea", "published"].includes(e.status));
    const live = (PUBLIC.episodes || []).slice(0, 5);
    const first = me.email.split("@")[0];
    const name = (TEAM.find((t) => t.email === me.email) || {}).name || first;
    return `
      <div class="bs-h"><h2>Hey ${esc(name.split(" ")[0])} 👋</h2>
        <div style="display:flex;gap:.5rem;flex-wrap:wrap"><button class="btn btn--sm" data-new="episodes">+ Episode</button><button class="btn btn--ghost btn--sm" data-new="events">+ Event</button><button class="btn btn--ghost btn--sm" data-new="tasks">+ Task</button><button class="btn btn--ghost btn--sm" data-new="ideas">+ Idea</button></div></div>
      <div class="bs-stats">
        <div class="bs-stat"><b>${inFlight.length}</b><span>episodes in production</span></div>
        <div class="bs-stat"><b>${soon.length}</b><span>things on the calendar ahead</span></div>
        <div class="bs-stat"><b>${open.length}</b><span>open tasks${open.filter((t) => t.due_on && t.due_on < today).length ? ` · ${open.filter((t) => t.due_on && t.due_on < today).length} late` : ""}</span></div>
        <div class="bs-stat"><b>${(PUBLIC.episodes || []).length}</b><span>episodes live on the site</span></div>
      </div>
      <div class="bs-cols">
        <div class="bs-panel"><h3>Coming up <button data-go="calendar">Calendar →</button></h3>
          ${soon.length ? soon.map((e) => `<div class="bs-row" data-kind="${e.kind}"><span class="bs-tag"><i></i>${esc(e.kind)}</span><div><b>${esc(e.title)}</b><small>${nice(e.starts_on)}${e.start_time ? " · " + e.start_time.slice(0, 5) : ""}${e.show_key ? " · " + esc(showName(e.show_key)) : ""}</small></div></div>`).join("") : `<p class="bs-empty">Nothing scheduled yet.</p>`}</div>
        <div class="bs-panel"><h3>In production <button data-go="episodes">Pipeline →</button></h3>
          ${inFlight.length ? inFlight.slice(0, 6).map((e) => `<div class="bs-row" data-show="${esc(e.show_key)}"><span class="bs-tag"><i></i>${esc(e.status)}</span><div><b>${esc(e.title)}</b><small>${esc(showName(e.show_key))}${e.publish_date ? " · out " + nice(e.publish_date) : ""}</small></div></div>`).join("") : `<p class="bs-empty">No episodes in flight. Add one from the Episodes tab.</p>`}</div>
        <div class="bs-panel"><h3>Open tasks <button data-go="tasks">All →</button></h3>
          ${open.length ? open.slice(0, 6).map((t) => `<div class="bs-row"><input type="checkbox" data-done="${t.id}" aria-label="Mark done"><div><b>${esc(t.title)}</b><small>${esc(t.area)}${t.assignee ? " · " + esc(t.assignee) : ""}${t.due_on ? " · due " + nice(t.due_on) : ""}</small></div></div>`).join("") : `<p class="bs-empty">All clear.</p>`}</div>
        <div class="bs-panel"><h3>Live on the site <a href="../index.html">View →</a></h3>
          ${live.map((e) => `<div class="bs-row" data-show="${esc(e.show)}"><span class="bs-tag"><i></i>${esc(e.kind)}</span><div><b>${esc(e.title)}</b><small>${esc(showName(e.show))} · ${e.date ? nice(e.date.slice(0, 10)) : ""}</small></div></div>`).join("") || `<p class="bs-empty">Feeds refresh every 6 hours.</p>`}</div>
      </div>`;
  }

  /* ---------------- calendar ---------------- */
  async function calendar() {
    const [evs, eps] = await Promise.all([load("events", "starts_on", true), load("episodes", "updated_at")]);
    const y = calMonth.getFullYear(), m = calMonth.getMonth();
    const start = new Date(y, m, 1 - ((new Date(y, m, 1).getDay() + 6) % 7));
    const items = {};
    const add = (d, html) => { if (!d) return; (items[d] = items[d] || []).push(html); };
    evs.forEach((e) => add(e.starts_on, `<span class="bs-ev" data-kind="${e.kind}" data-edit="events:${e.id}" title="${esc(e.title)}">${e.start_time ? e.start_time.slice(0, 5) + " " : ""}${esc(e.title)}</span>`));
    eps.forEach((e) => {
      add(e.record_date, `<span class="bs-ev bs-ev--ghost" data-kind="recording" data-edit="episodes:${e.id}">🎙 ${esc(e.title)}</span>`);
      add(e.publish_date, `<span class="bs-ev bs-ev--ghost" data-kind="release" data-edit="episodes:${e.id}">🚀 ${esc(e.title)}</span>`);
    });
    (PUBLIC.episodes || []).forEach((e) => e.date && add(e.date.slice(0, 10), `<a class="bs-ev bs-ev--ghost" data-kind="live" href="${esc(e.url)}" target="_blank" rel="noopener">● ${esc(e.title)}</a>`));
    let cells = "";
    for (let i = 0; i < 42; i++) {
      const d = new Date(start); d.setDate(start.getDate() + i);
      const k = iso(d);
      cells += `<div class="bs-day${d.getMonth() !== m ? " is-out" : ""}${k === today ? " is-today" : ""}" data-day="${k}" role="button" tabindex="0" aria-label="${nice(k)}"><span class="bs-day__n">${d.getDate()}</span>${(items[k] || []).join("")}</div>`;
    }
    return `
      <div class="bs-h"><h2>Calendar</h2>
        <div class="bs-cal__nav"><button class="icon-btn" data-cal="-1" aria-label="Previous month">‹</button><b>${calMonth.toLocaleDateString("en-US", { month: "long", year: "numeric" })}</b><button class="icon-btn" data-cal="1" aria-label="Next month">›</button><button class="btn btn--ghost btn--sm" data-cal="0">Today</button><button class="btn btn--sm" data-new="events">+ Event</button></div></div>
      <p class="bs-filters">${KINDS.map((k) => `<span class="bs-tag" data-kind="${k}"><i></i>${k}</span>`).join("")}<span class="bs-tag" data-kind="live"><i></i>live episode</span></p>
      <div class="bs-cal">${["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"].map((d) => `<div class="bs-cal__dow">${d}</div>`).join("")}${cells}</div>
      <p class="eyebrow" style="margin-top:.8rem;text-transform:none;letter-spacing:0">Click a day to add something. Dashed items come from the episode pipeline and from what's already published.</p>`;
  }

  /* ---------------- episodes pipeline ---------------- */
  async function episodes() {
    const eps = await load("episodes", "updated_at");
    return `
      <div class="bs-h"><h2>Episode pipeline</h2><button class="btn btn--sm" data-new="episodes">+ Episode</button></div>
      <div class="bs-board">${STATUSES.map(([k, label]) => {
        const col = eps.filter((e) => e.status === k);
        return `<div class="bs-col" data-status="${k}"><h3><span>${label}</span><span>${col.length}</span></h3>
          ${col.map((e) => `<button class="bs-card" draggable="true" data-id="${e.id}" data-edit="episodes:${e.id}" data-show="${esc(e.show_key)}">
            <span class="show-tag" data-show="${esc(e.show_key)}"><i></i>${esc(showName(e.show_key))}</span>
            <b>${esc(e.title)}</b>
            ${e.guest ? `<small>with ${esc(e.guest)}</small>` : ""}
            <small>${[e.record_date && "🎙 " + nice(e.record_date), e.publish_date && "🚀 " + nice(e.publish_date), e.owner].filter(Boolean).map(esc).join(" · ")}</small>
          </button>`).join("")}
        </div>`;
      }).join("")}</div>
      <p class="eyebrow" style="text-transform:none;letter-spacing:0">Drag cards between columns, or open one to edit.</p>`;
  }

  /* ---------------- tasks ---------------- */
  async function tasks() {
    const all = await load("tasks", "due_on", true);
    const list = all.filter((t) => (taskFilter === "open" ? !t.done : taskFilter === "done" ? t.done : !t.done && t.area === taskFilter));
    return `
      <div class="bs-h"><h2>Tasks</h2><button class="btn btn--sm" data-new="tasks">+ Task</button></div>
      <div class="bs-filters">${["open", ...AREAS, "done"].map((f) => `<button class="filter${f === taskFilter ? " is-on" : ""}" data-tf="${f}">${f}</button>`).join("")}</div>
      <div class="bs-tasks">${list.map((t) => `<div class="bs-task${t.done ? " is-done" : ""}">
        <input type="checkbox" data-done="${t.id}" ${t.done ? "checked" : ""} aria-label="Done">
        <div><b data-edit="tasks:${t.id}">${esc(t.title)}</b><small>${esc(t.area)}${t.assignee ? " · " + esc(t.assignee) : ""}${t.notes ? " · " + esc(t.notes.slice(0, 80)) : ""}</small></div>
        <span class="bs-task__due${t.due_on && t.due_on < today && !t.done ? " is-late" : ""}">${t.due_on ? nice(t.due_on) : ""}</span>
      </div>`).join("") || `<p class="bs-empty">Nothing here.</p>`}</div>`;
  }

  /* ---------------- ideas ---------------- */
  async function ideas() {
    const all = await load("ideas", "created_at");
    all.sort((a, b) => b.pinned - a.pinned);
    return `
      <div class="bs-h"><h2>Idea board</h2><button class="btn btn--sm" data-new="ideas">+ Idea</button></div>
      <div class="bs-ideas">${all.map((i) => `<button class="bs-idea${i.pinned ? " is-pinned" : ""}" data-edit="ideas:${i.id}"><span class="bs-tag">${esc(i.area)}</span><b>${esc(i.title)}</b>${i.body ? `<p>${esc(i.body)}</p>` : ""}</button>`).join("") || `<p class="bs-empty">Episode ideas, guests, shoots, inventions, site changes — drop them here.</p>`}</div>`;
  }

  /* ---------------- team ---------------- */
  function team() {
    return `
      <div class="bs-h"><h2>Team</h2></div>
      <div class="bs-cols">
        <div class="bs-panel"><h3>Who has access</h3>
          ${TEAM.map((t) => `<div class="bs-row"><div style="flex:1"><b>${esc(t.name)}</b><small>${esc(t.email)}</small></div>${t.email !== me.email ? `<button class="btn btn--danger btn--sm" data-unteam="${esc(t.email)}">Remove</button>` : `<small>you</small>`}</div>`).join("")}
        </div>
        <form class="bs-panel form" id="team-add"><h3>Add someone</h3>
          <label>Name<input name="name" required placeholder="Janel Moore"></label>
          <label>Email<input name="email" type="email" required placeholder="their login email"></label>
          <button class="btn" type="submit">Give access</button>
          <p class="eyebrow" style="text-transform:none;letter-spacing:0">They then open this page, choose “Create your login” with that email, and confirm it from their inbox.</p>
        </form>
      </div>`;
  }

  /* ---------------- editors ---------------- */
  const FORMS = {
    episodes: (r) => `<h3>${r.id ? "Edit" : "New"} episode</h3><div class="bs-modal__grid">
      <label class="wide">Title<input name="title" required value="${esc(r.title)}"></label>
      <label>Show<select name="show_key">${showOpts(r.show_key ?? "ccpod")}</select></label>
      <label>Stage<select name="status">${STATUSES.map(([k, l]) => `<option value="${k}"${k === (r.status || "idea") ? " selected" : ""}>${l}</option>`).join("")}</select></label>
      <label>Guest<input name="guest" value="${esc(r.guest)}"></label>
      <label>Owner<select name="owner">${peopleOpts(r.owner)}</select></label>
      <label>Record date<input type="date" name="record_date" value="${esc(r.record_date)}"></label>
      <label>Publish date<input type="date" name="publish_date" value="${esc(r.publish_date)}"></label>
      <label class="wide">Link (doc, folder, or published URL)<input name="link" value="${esc(r.link)}"></label>
      <label class="wide">Notes<textarea name="notes">${esc(r.notes)}</textarea></label></div>`,
    events: (r) => `<h3>${r.id ? "Edit" : "New"} event</h3><div class="bs-modal__grid">
      <label class="wide">Title<input name="title" required value="${esc(r.title)}"></label>
      <label>Type<select name="kind">${KINDS.map((k) => `<option${k === (r.kind || "recording") ? " selected" : ""}>${k}</option>`).join("")}</select></label>
      <label>Show<select name="show_key">${showOpts(r.show_key ?? "")}</select></label>
      <label>Date<input type="date" name="starts_on" required value="${esc(r.starts_on || today)}"></label>
      <label>Time<input type="time" name="start_time" value="${esc((r.start_time || "").slice(0, 5))}"></label>
      <label class="wide">Where<input name="location" value="${esc(r.location)}"></label>
      <label class="wide">Notes<textarea name="notes">${esc(r.notes)}</textarea></label></div>`,
    tasks: (r) => `<h3>${r.id ? "Edit" : "New"} task</h3><div class="bs-modal__grid">
      <label class="wide">Task<input name="title" required value="${esc(r.title)}"></label>
      <label>Area<select name="area">${AREAS.map((a) => `<option${a === (r.area || "shows") ? " selected" : ""}>${a}</option>`).join("")}</select></label>
      <label>Who<select name="assignee">${peopleOpts(r.assignee)}</select></label>
      <label>Due<input type="date" name="due_on" value="${esc(r.due_on)}"></label>
      <label style="flex-direction:row;display:flex;align-items:center;gap:.5rem;margin-top:1.6rem"><input type="checkbox" name="done" ${r.done ? "checked" : ""}> Done</label>
      <label class="wide">Notes<textarea name="notes">${esc(r.notes)}</textarea></label></div>`,
    ideas: (r) => `<h3>${r.id ? "Edit" : "New"} idea</h3><div class="bs-modal__grid">
      <label class="wide">Idea<input name="title" required value="${esc(r.title)}"></label>
      <label>Area<select name="area">${AREAS.map((a) => `<option${a === (r.area || "shows") ? " selected" : ""}>${a}</option>`).join("")}</select></label>
      <label style="flex-direction:row;display:flex;align-items:center;gap:.5rem;margin-top:1.6rem"><input type="checkbox" name="pinned" ${r.pinned ? "checked" : ""}> Pin to top</label>
      <label class="wide">Details<textarea name="body">${esc(r.body)}</textarea></label></div>`,
  };
  const modal = $("#bs-modal"), mform = $("#bs-modal-form");
  async function openEditor(table, id, defaults = {}) {
    let row = { ...defaults };
    if (id) { const { data } = await sb.from(table).select("*").eq("id", id).single(); row = data || {}; }
    mform.innerHTML = FORMS[table](row) + `<div class="bs-modal__actions"><span>${id ? `<button class="btn btn--danger btn--sm" type="button" data-del>Delete</button>` : ""}</span><span style="display:flex;gap:.5rem"><button class="btn btn--ghost btn--sm" type="button" data-cancel>Cancel</button><button class="btn btn--sm" type="submit">Save</button></span></div>`;
    mform.dataset.table = table;
    mform.dataset.id = id || "";
    modal.classList.add("is-open");
    modal.setAttribute("aria-hidden", "false");
    setTimeout(() => mform.querySelector("input,select,textarea")?.focus(), 50);
  }
  const closeEditor = () => { modal.classList.remove("is-open"); modal.setAttribute("aria-hidden", "true"); };
  modal.addEventListener("click", (e) => { if (e.target === modal || e.target.closest("[data-cancel]")) closeEditor(); });
  document.addEventListener("keydown", (e) => { if (e.key === "Escape") closeEditor(); });
  mform.addEventListener("click", async (e) => {
    if (!e.target.closest("[data-del]")) return;
    if (!confirm("Delete this for both of you?")) return;
    await remove(mform.dataset.table, mform.dataset.id);
    closeEditor(); render();
  });
  mform.addEventListener("submit", async (e) => {
    e.preventDefault();
    const row = { id: mform.dataset.id || undefined };
    new FormData(mform).forEach((v, k) => { row[k] = v; });
    mform.querySelectorAll('input[type="checkbox"]').forEach((c) => { row[c.name] = c.checked; });
    if (await save(mform.dataset.table, row)) { closeEditor(); render(); }
  });

  /* ---------------- wiring ---------------- */
  function wire(v) {
    v.querySelectorAll("[data-new]").forEach((b) => b.addEventListener("click", () => openEditor(b.dataset.new)));
    v.querySelectorAll("[data-edit]").forEach((b) => b.addEventListener("click", (e) => { e.stopPropagation(); const [t, id] = b.dataset.edit.split(":"); openEditor(t, id); }));
    v.querySelectorAll("[data-go]").forEach((b) => b.addEventListener("click", () => $(`.bs-tabs [data-tab="${b.dataset.go}"]`).click()));
    v.querySelectorAll("[data-done]").forEach((c) => c.addEventListener("change", async () => { await save("tasks", { id: c.dataset.done, done: c.checked }); render(); }));
    v.querySelectorAll("[data-tf]").forEach((b) => b.addEventListener("click", () => { taskFilter = b.dataset.tf; render(); }));
    v.querySelectorAll("[data-cal]").forEach((b) => b.addEventListener("click", () => {
      const n = Number(b.dataset.cal);
      if (n === 0) { calMonth = new Date(); calMonth.setDate(1); } else calMonth.setMonth(calMonth.getMonth() + n);
      render();
    }));
    v.querySelectorAll("[data-day]").forEach((d) => {
      const open = (e) => { if (e.target.closest("[data-edit], a")) return; openEditor("events", null, { starts_on: d.dataset.day }); };
      d.addEventListener("click", open);
      d.addEventListener("keydown", (e) => { if (e.key === "Enter") open(e); });
    });
    v.querySelectorAll(".bs-card[draggable]").forEach((c) => c.addEventListener("dragstart", (e) => e.dataTransfer.setData("text/plain", c.dataset.id)));
    v.querySelectorAll(".bs-col").forEach((col) => {
      col.addEventListener("dragover", (e) => { e.preventDefault(); col.classList.add("is-drop"); });
      col.addEventListener("dragleave", () => col.classList.remove("is-drop"));
      col.addEventListener("drop", async (e) => {
        e.preventDefault();
        col.classList.remove("is-drop");
        const id = e.dataTransfer.getData("text/plain");
        if (id) { await save("episodes", { id, status: col.dataset.status }); render(); }
      });
    });
    const ta = v.querySelector("#team-add");
    if (ta) ta.addEventListener("submit", async (e) => {
      e.preventDefault();
      const { error } = await sb.from("team_members").insert({ name: ta.name.value.trim(), email: ta.email.value.trim().toLowerCase() });
      if (error) alert(error.message); else render();
    });
    v.querySelectorAll("[data-unteam]").forEach((b) => b.addEventListener("click", async () => {
      if (!confirm(`Remove ${b.dataset.unteam}?`)) return;
      const { error } = await sb.from("team_members").delete().eq("email", b.dataset.unteam);
      if (error) alert(error.message); else render();
    }));
  }

  setMode("signin");
})();
