// Link crawl: loads the main pages on the local server and checks every internal link returns 200.
// Usage (server running on :8765): node .claude/skills/run-site/crawl.mjs
import pw from "/opt/node22/lib/node_modules/playwright/index.js";
const b = await pw.chromium.launch(); const ctx=await b.newContext(); const pg=await ctx.newPage();
const errs=[]; pg.on("pageerror",e=>errs.push(pg.url()+" "+e.message));
const seen=new Set(), bad=[]; const q=["/","/pages/about.html","/pages/studio.html","/pages/consultancy.html","/pages/shows.html","/pages/contact.html","/pages/manifesto.html","/pages/shop.html","/pages/videos.html","/pages/writing.html","/pages/art.html","/pages/archive.html","/shows/eclectic-polymath/"];
for (const u of q){ await pg.goto("http://localhost:8765"+u,{waitUntil:"load"}); await pg.waitForTimeout(1500);
  const hrefs = await pg.$$eval("a[href]",as=>as.map(a=>String(a.href.baseVal ?? a.href)));
  for (const h of hrefs){ const x=h.split("#")[0]; if(!x.startsWith("http://localhost:8765")||seen.has(x))continue; seen.add(x);
    const r=await ctx.request.get(x); if(r.status()!==200) bad.push(r.status()+" "+x+" (from "+u+")"); } }
console.log("checked",seen.size,"bad",bad.length+"\n"+bad.slice(0,20).join("\n")); console.log("errors",errs);
await b.close();
