# Source maps for Columbia SC, Los Angeles, New York City and Chicago, plus the next 20 markets: research notes

*Prepared 2026-10-11 for Project Earlobe. **Status: PARTIAL and UNVERIFIED.** Read the "Research status" box first.*

## TL;DR

This pass could not collect new web evidence. The web-search budget for the turn was already spent when the task started (every call returned "budget used up"), and every direct fetch of a primary source (PACER, CourtListener, LA Superior Court, NY Courts, Cook County Clerk, SC Judicial Branch) failed at the network level with a DNS error. So nothing below was checked live. The file is a **source map built from background knowledge plus the repo's own config**, with every entry labeled by how sure I am. What it is good for: (1) a complete checklist of outlets, official feeds, court portals, federal courts and meeting platforms for each market, so the Beat agents and Court Watch know what to look for; (2) the repo's five feed files compared against what I remember, with the least-certain URLs flagged; (3) a scored proposal for the next 20 markets, with the method spelled out; and (4) a ready-to-send list of verification searches. What it is **not** good for: quoting a fee, a URL or a DMA rank as fact. Every number here is *(inference)* from memory and must be confirmed (and added to the facts sheet with a source) before use. Headline planning items: PACER is recalled as **$0.10 per page, $3.00 cap per document, free if you stay at or under $30 a quarter**; CourtListener's court id for the South Carolina district is `scd`, not `dsc` (the sensor already aliases it, but `config/markets.yaml` still says `dsc`); and in the biggest markets the "news desert" is rarely a missing outlet. It is more often a **hollowed legacy daily plus thin county-level coverage** inside the DMA, which changes how to choose wave 3 and later markets.

## Research status (read first)

| Item | What happened |
|---|---|
| Web search | 0 of 6 planned first-wave searches ran. The tool returned "budget used up" (200-call per-turn limit shared by all agents). I did not work around it (no search through curl, readers or archives). |
| Direct fetches | Tried once each, all failed with ENOTFOUND: pacer.uscourts.gov, www.courtlistener.com, www.lacourt.ca.gov, www.nycourts.gov, www.cookcountyclerkofcourt.org, www.sccourts.org. Not retried. |
| What this file contains | (a) Background recall, every item labeled *(inference)* with a confidence; (b) facts from the repo itself (`config/markets.yaml`, `config/sources/*.yaml`, `config/owners.yaml`, `earlobe/sensors/courtlistener.py`, `docs/blueprint/agent-catalog.md`), cited by path; (c) reasoning about market selection. |
| What is NOT here | Any live-confirmed RSS URL; any current fee schedule; any 2026 DMA rank; any 2025 or 2026 Medill news-desert county counts; current court-portal terms of use. |
| To finish | A follow-up message can re-run the searches listed in section 11, written out and ready to send. |

**Confidence key used in this file.** *high* = I am sure and it is stable public knowledge (for example, "NYC Council publishes on Legistar"). *medium* = I am fairly sure but it may have moved. *low* = a pattern or a vague recollection; do not rely on it. Nothing is marked "official" in the findings table, because I read no official page this session.

---

## 1. Cross-market building blocks

### 1.1 PACER (federal court records) fees

- **Recalled fee schedule:** $0.10 per page; a **$3.00 cap per document** (about 30 pages) for most documents and docket reports; **no charge when a user's total is $30 or less in a calendar quarter**; judicial opinions are free; case-specific audio files cost a few dollars each. *(inference; medium on the $0.10 and $3 cap, medium-low on the $30 waiver and on whether anything changed in 2025-2026)*. Expected source to confirm: PACER's "pricing: how fees work" page.
- **Who gets fee exemptions:** by court order, indigent parties, some researchers and some nonprofit or educational users. Commercial and media users generally do not. A synthetic-voice news network should plan on paying. *(inference; low)*
- **Planning math** *(inference)*: if Court Watch pulled 10 docket sheets or documents a day at an average of $1.50, that is about $450 a month; at the $3 cap for 20 a day it is about $1,800 a month worst case. The cheaper design is to read **CourtListener (RECAP) first** and only buy from PACER for items it lacks. A reasonable starting cap for the Budget Controller is **$150-$300 a month for all federal courts**, tightened once RECAP hit rates are known. This is a proposal, not a sourced figure.
- **Coverage realism** *(inference)*: C.D. Cal. and S.D.N.Y. each take in thousands of new civil filings a month. N.D. Ill. is also large. E.D.N.Y. is large. D.S.C. is far smaller. A relevance filter is needed for the big four or the daily brief drowns in routine filings (prisoner petitions, social security appeals, debt collection).

### 1.2 CourtListener / RECAP (Free Law Project)

- **What it is:** a free archive of federal dockets and documents, filled by (a) users of the RECAP browser extension who share what they buy from PACER and (b) court-provided RSS feeds of new docket entries, which CourtListener polls for many districts. It is not a complete mirror of PACER: a docket exists only if someone bought it or the court RSS exposed it. *(inference; medium)*
- **API:** REST v4 with token authentication (`Authorization: Token ...`), a search endpoint where `type=r` returns RECAP dockets, plus docket and docket-entry endpoints and alerts. Rate limits exist for authenticated users (I recall a few thousand requests an hour; not verified). The repo's sensor already uses `GET /api/rest/v4/search/?type=r&court=...&filed_after=...`; its own header says field names were not checked against a live response. *(repo: `earlobe/sensors/courtlistener.py`; medium)*
- **Court ids (CourtListener style)** *(inference; medium-high, standard ids)*:

| Market | Federal court | CourtListener id | In `config/markets.yaml` |
|---|---|---|---|
| Columbia SC | D.S.C. (Columbia Division) | `scd` | `dsc` (**mismatch**; the sensor maps `dsc` to `scd` via `COURT_ALIASES`, so it works, but fix the config or the docs to avoid confusion) |
| Los Angeles | C.D. Cal. | `cacd` | `cacd` |
| New York City | S.D.N.Y. (Manhattan, Bronx) and E.D.N.Y. (Brooklyn, Queens, Staten Island, Long Island) | `nysd`, `nyed` | `nysd`, `nyed` |
| Chicago | N.D. Ill. | `ilnd` | `ilnd` |
| National | U.S. Supreme Court | `scotus` | `scotus` |

- **Court RSS (free, from the court itself):** many district courts publish public RSS feeds of docket entries or opinions through CM/ECF. Which of the five courts do, and with what filter, is not confirmed. *(inference; low)* Check each court's "RSS feeds" page.
- **Cost to Earlobe:** the CourtListener API token is free to request; no price was verified. Keep the PACER spend line separate (above).

### 1.3 Public-meeting platforms (how to find agendas)

- **Legistar (Granicus):** city and county clerks publish calendars, agendas, legislation and votes. Many have a Legistar Web API at `webapi.legistar.com/v1/<client>`; some clients require a token. *(inference; medium that the pattern exists, low that a given city is open)*
- **Granicus** (video and agenda management), **CivicPlus Agenda Center**, **BoardDocs** (school boards), **PrimeGov**, **CivicClerk**, **Municode Meetings** and custom clerk sites are the other common platforms. The repo's Public Meetings agent already lists Legistar, Granicus, CivicPlus, BoardDocs and PrimeGov. *(repo: `docs/blueprint/agent-catalog.md` line ~516)*
- **Practical rule** *(inference)*: discover the platform per governing body by looking at the clerk's "agendas and minutes" page, then check for an iCal or RSS link before scraping. Do not assume the platform from the city name.

### 1.4 Documenters-style civic sources

- **City Bureau Documenters** (Chicago, since 2018): paid community members attend public meetings and publish notes, with a public meeting calendar at documenters.org. The model spread to a handful of other cities, mostly in the Midwest and through partner newsrooms; the current list of cities was not confirmed. Chicago is the only one of our four markets where I am confident a Documenters program exists. *(inference; medium for Chicago, low for the network list)*
- **Why it matters:** Documenters notes are a human-written, attributed record of meetings that otherwise get no coverage. They are third-party content: **check the reuse license and terms before any use beyond linking and summarizing facts in our own words.** Do not assume a permissive license.
- **Substitutes where no Documenters program exists** *(inference)*: clerk meeting calendars, recorded meeting video with captions, minutes, public-comment sign-up lists, and local news outlets' own meeting previews.

### 1.5 Reuse licenses (matters for a monetized podcast)

- **States Newsroom outlets** (SC Daily Gazette is one) invite republishing under a Creative Commons license I recall as **CC BY-NC-ND 4.0** (attribution, non-commercial, no derivatives). *(inference; medium)* A monetized podcast is commercial and a script adapted from an article is a derivative, so **we should not treat these as republishable text**. Per Convention 7 we report facts in our own words and link the source.
- Other nonprofit newsrooms in this file (Block Club, THE CITY, LAist, Chalkbeat, Gothamist and others) each have their own republishing policy; none were checked. *(open question)*

### 1.6 Other free official feeds that apply everywhere

- **National Weather Service API** (`api.weather.gov`): free, no key, but it expects a descriptive `User-Agent` header; alerts are available by `area=` (state) or `point=` (latitude, longitude). *(inference; high on the User-Agent rule, medium on the `.atom` path used in the repo's configs)*
- **Local open-data portals** (Socrata-style): NYC Open Data (`opendata.cityofnewyork.us`), Chicago Data Portal (`data.cityofchicago.org`), Cook County Open Data (`datacatalog.cookcountyil.gov`), City of Los Angeles open data (`data.lacity.org`). Crime, 311, permits and similar datasets, many updated daily. *(inference; high that they exist, medium that specific datasets are current)*
- **U.S. Attorney press pages** at `justice.gov/usao-<district>` for each federal district (`usao-sc`, `usao-cdca`, `usao-sdny`, `usao-edny`, `usao-ndil`). The per-district RSS path is not confirmed (see section 6). *(inference; high on the pages, low on the RSS paths)*

---

## 2. Columbia, SC (wave 0; Richland County; DMA recalled as roughly mid-70s, band 71-80)

**State of the repo:** `config/sources/columbia-sc.yaml` lists 8 feeds, all `verified: false`. Owner groups are in `config/owners.yaml`.

### 2.1 Outlets

| Outlet | Type | Owner group (repo or recall) | Feed in repo | My read on the feed |
|---|---|---|---|---|
| The State | Daily newspaper | McClatchy | McClatchy `widgetName=rssfeed` URL | Pattern plausible but the widget id is a guess (the repo says so). **Unconfirmed.** |
| The Post and Courier (Columbia edition) | Daily newspaper (Charleston-based, statewide) | Evening Post Industries | Search-RSS URL with `c=columbia` | Pattern plausible; section slug is a guess. **Unconfirmed.** |
| SC Daily Gazette | Nonprofit statehouse and policy newsroom | States Newsroom | `https://scdailygazette.com/feed/` | WordPress `/feed/` is the standard path; most likely to work. **Unconfirmed live; medium.** |
| WIS (NBC) | TV | Gray Media | `.../arc/outboundfeeds/rss/?outputType=xml` | Gray stations use this Arc pattern in many markets; medium-low. |
| WLTX (CBS) | TV | TEGNA | `.../feeds/syndication/rss/news` | Pattern from memory; medium-low. |
| WACH (Fox 57), WOLO (ABC Columbia) | TV | not in repo (recall: Sinclair-affiliated and Bahakel respectively; **low**) | none | Add to the source list and to `owners.yaml` once ownership is confirmed. |
| Free Times | Former alt-weekly | Evening Post Industries | none | Recalled as folded into the Post and Courier around 2020; **low, verify**. |

*(all rows: inference except the owner groups and feeds taken from the repo)*

### 2.2 Public radio, student and other

- **SC Public Radio** (SCETV): Columbia is the home of the state public broadcaster, which also produces a statehouse report. Local stations recalled as WLTR 91.3 FM. *(inference; medium-low)*
- **WUSC 90.5** (University of South Carolina) and **The Daily Gamecock** (USC student paper): student and community outlets; useful for campus news, low priority for sourcing. *(inference; medium)*
- **Nonprofit newsrooms:** SC Daily Gazette is the main one. No other nonprofit newsroom focused on Columbia was recalled. *(inference; low; verify with a search on "South Carolina nonprofit news")*

### 2.3 Official feeds and press pages

| Source | Why | Feed in repo | Note |
|---|---|---|---|
| City of Columbia (columbiasc.gov) | Mayor, council, city press releases | CivicPlus "news flash" URL | The path is the standard CivicPlus pattern, but whether the city runs CivicPlus is unknown. **Unconfirmed; low.** |
| Richland County (richlandcountysc.gov) | County government news | CivicPlus pattern | Same caveat. **Unconfirmed; low.** |
| Columbia Police Department | Incident and arrest releases | none | Add. Site not confirmed. |
| Richland County Sheriff's Department (rcsd.net) | Arrests, incidents | none | Add. |
| Fifth Judicial Circuit Solicitor (covers Richland and Kershaw counties) | Prosecutor press releases | none | Add; site not confirmed. *(inference; medium that the Fifth Circuit covers Richland)* |
| SC Attorney General (scag.gov), SLED (sled.sc.gov) | State criminal cases, investigations | none | Add. |
| SC Statehouse (scstatehouse.gov) | Bills, committees, session calendar, video | none | Columbia is the state capital, so this is a local beat (the blueprint already says so). Session runs January to May with possible returns. *(inference; medium)* |
| National Weather Service alerts for SC | Weather | `api.weather.gov/alerts/active.atom?area=SC` | See 1.6. |

### 2.4 Courts

- **State:** the SC Judicial Branch runs a **Public Index** with county-level search; the Richland County index covers Common Pleas (civil) and General Sessions (criminal) case information. Free to search by name or case number; family court and juvenile matters are not public. It is a lookup tool, not a bulk feed, and carries disclaimers that it is not the official record. *(inference; medium)* Expected entry point: the "case records search" page on sccourts.org and the Public Index site.
- **Fees:** I recall no fee for index lookups. Copies from the clerk of court cost money; amounts not recalled. *(open question)*
- **Automated access:** terms of use not checked. The blueprint already routes this through Compliance & Platform Policy Watch before Court Watch scrapes anything. *(repo)*
- **Federal:** D.S.C., Columbia Division (CourtListener id `scd`). Smaller docket than the other three markets. Charleston, Greenville and other divisions share the same district court. *(inference; medium)*

### 2.5 Public meetings (platform not confirmed for any body below)

Columbia City Council, Richland County Council, Richland One and Richland Two school boards (recalled as BoardDocs users; **low**), SC General Assembly. No Documenters-style program recalled for Columbia. *(inference)*

---

## 3. Los Angeles (wave 0; DMA #2)

**State of the repo:** `config/sources/los-angeles.yaml` lists 14 feeds, all `verified: false`.

### 3.1 Outlets

| Outlet | Type | Owner group | Feed in repo | My read |
|---|---|---|---|---|
| Los Angeles Times | Daily newspaper | LA Times | `latimes.com/<section>/rss2.0.xml` (local, business, sports) | Pattern is familiar from memory; **medium**. |
| LAist | Public-media digital newsroom (formerly KPCC) | Southern California Public Radio | `https://laist.com/index.rss` | Repo says "pattern from memory"; **low**. Use feed autodiscovery. |
| Los Angeles Daily News | Daily newspaper | MediaNews Group | `dailynews.com/feed/` | WordPress style; **medium**. |
| KTLA 5 | TV | Nexstar | `ktla.com/feed/` | **Medium**. |
| NBC Los Angeles (KNBC) | TV | Comcast NBCUniversal | `nbclosangeles.com/news/local/?rss=y` | NBC station pattern; **medium**. |
| ABC7 Los Angeles (KABC) | TV | Disney | `abc7.com/feed/` | ABC station pattern; **medium**. |
| CBS Los Angeles (KCBS/KCAL) | TV | Paramount | `cbsnews.com/losangeles/latest/rss/main` | **Medium-low** (CBS moved local sites in 2022). |
| Fox 11 (KTTV), Telemundo 52, Univision 34 (KMEX) | TV | Fox / NBCU / TelevisaUnivision | none | Add; the Spanish-language outlets matter for the planned Spanish edition. *(inference)* |

### 3.2 Public radio, alt-weekly, nonprofits, others (none in the repo's feed file)

- **Public radio:** KPCC 89.3 (now LAist), KCRW (Santa Monica), KPFK (Pacifica), PBS SoCal (formerly KCET), KUSC. *(inference; medium)*
- **Alt-weekly and magazines:** LA Weekly (revived under new ownership after its 2017 sale and 2018 shake-up), Los Angeles Magazine, LA Taco (food and culture). Status of each in 2026 not checked. *(inference; low)*
- **Nonprofit and independent newsrooms:** CalMatters (state politics, calmatters.org), Crosstown LA (USC Annenberg data journalism, domain recalled as xtown.la), LA Public Press, Capital & Main, Knock LA, Streetsblog LA (transit), EdSource (education). *(inference; medium for existence, low for current activity)*
- **Spanish and community press:** La Opinion, Los Angeles Sentinel. *(inference; medium)*
- **Legal trade:** Daily Journal (courts and legal news; paywalled). *(inference; medium)*

### 3.3 Official feeds and press pages

| Source | Feed in repo | Note |
|---|---|---|
| City of Los Angeles | `lamayor.org/rss.xml` | "Drupal pattern; guess" per the repo. **Low.** Also look at the city's newsroom and the City Clerk. |
| LA Metro (The Source) | `thesource.metro.net/feed/` | WordPress blog; **medium**. |
| LA County District Attorney | `da.lacounty.gov/rss.xml` | "Drupal pattern; guess." **Low.** The DA posts a news page; look there for a feed. |
| U.S. Attorney, C.D. Cal. | `justice.gov/usao-cdca/pr/rss.xml` | DOJ pattern, guess. **Low.** |
| LAPD (lapdonline.org), LA County Sheriff (lasd.org) | none | Add; media-relations pages. Not confirmed. |
| LA City Attorney, LA County Board of Supervisors | none | Add; city attorney prosecutes misdemeanors (relevant for Court Watch). *(inference; medium)* |
| NWS alerts (point 34.05,-118.24) | in repo | See 1.6. |

### 3.4 Courts

- **State:** LA Superior Court is the largest trial court system in the US. Its public site offers online case lookup; civil case summaries and registers of action are recalled as free to view, while **document images carry a per-document fee** whose amount I do not remember with any confidence (do not use a number from this file). Criminal case information online is more limited than civil. Tentative rulings for civil motions are posted publicly for free. *(inference; medium on structure, low on every price)*
- **Media access:** the court has historically had a news-media office and credentialing; whether media get fee-free document access was not checked. *(open question)*
- **Federal:** C.D. Cal. (Western Division is in downtown LA); id `cacd`. High volume. *(inference; medium)*
- **Expect the notable-case flow to come from:** DA and City Attorney press releases, federal indictments announced by the U.S. Attorney, and civil suits against celebrities or companies, which is where the entertainment-business beat gets story material. *(inference)*

### 3.5 Public meetings (platform not confirmed)

LA City Council (agendas and the Council File Management System via the City Clerk; PrimeGov recalled for agendas, **low**), LA County Board of Supervisors, LAUSD Board of Education, LA Metro Board (Legistar recalled, **low**), LA Police Commission (publishes agendas and video; key public-safety oversight body), plus the Sheriff Civilian Oversight Commission. No Documenters program for LA recalled. *(inference)*

---

## 4. New York City (wave 1; DMA #1)

**State of the repo:** `config/sources/new-york.yaml` lists 11 feeds, all `verified: false`. `config/owners.yaml` does not list any NYC group except the New York Times Company.

### 4.1 Outlets

| Outlet | Type | Owner (recall) | Feed in repo | My read |
|---|---|---|---|---|
| The New York Times (Metro) | Daily | NYT Company | `rss.nytimes.com/services/xml/rss/nyt/NYRegion.xml` | Well-known official pattern; **medium-high**. |
| Gothamist | Public-media digital (WNYC) | New York Public Radio | `gothamist.com/feed` | **Low-medium**; the CMS changed after NYPR bought the site. |
| New York Daily News | Daily | Alden-affiliated | `nydailynews.com/feed/` | **Low-medium** (may be an Arc-style path). |
| amNY | Free daily/weekly | Schneps Media | `amny.com/feed/` | WordPress style; **medium**. |
| THE CITY | Nonprofit | independent nonprofit | `thecity.nyc/feed/` | **Medium**. |
| NBC New York, ABC7 New York, CBS New York, PIX11 | TV | NBCU, Disney, Paramount, Nexstar | station patterns | **Medium** (PIX11 higher; CBS lower). |

*(all rows: inference; ownership recalled, not from the repo, unless stated)*

### 4.2 Public radio, alt-weekly, nonprofits, others (not in the repo)

- **TV not in the repo:** WNBC is covered; add Fox 5 (WNYW), WWOR, WNET/PBS, Telemundo 47, Univision 41, and Spectrum News NY1 (24-hour cable). *(inference; medium)*
- **Public radio:** WNYC (NYPR, with Gothamist), WBAI (Pacifica), WFUV (Fordham). *(inference; medium)*
- **Dailies and weeklies:** New York Post (News Corp), Newsday (Long Island), Staten Island Advance/SILive, Brooklyn Paper and Queens-area weeklies (Schneps), City & State (politics). *(inference; medium)*
- **Alt and independent:** Hell Gate (worker-owned, founded 2022 by former Gothamist staff), The Indypendent, Documented (immigrant news nonprofit). The Village Voice's status after its post-2018 shutdown and later relaunch attempts is unknown. *(inference; medium for the first three, low for the Voice)*
- **Nonprofit and specialist:** THE CITY, Chalkbeat New York (education), NY Focus (state politics), Documented. *(inference; medium)*

### 4.3 Official feeds and press pages

| Source | Note |
|---|---|
| Mayor's Office, NYPD (nyc.gov), NYC agencies | City press pages; feeds not confirmed. Not in the repo. |
| District attorneys for each borough: Manhattan, Brooklyn, Queens, Bronx, Richmond (Staten Island) | Five separate prosecutors with separate press pages; not in the repo. Add all five. *(inference; high that there are five)* |
| U.S. Attorney, S.D.N.Y. (in repo) and E.D.N.Y. (**missing from the repo**) | SDNY path is a "guess" per the repo; EDNY should be added since Brooklyn and Queens are in the E.D.N.Y. |
| NY Attorney General (ag.ny.gov) | State enforcement releases; not in the repo. |
| MTA press releases and board materials | Transit beat; not in the repo. |
| City Record Online (NYC's official public-notice and procurement journal) | Hearings, contract awards, rule changes; a Documenters-style source. Feed or Open Data dataset recalled but unconfirmed. *(inference; medium)* |
| NYC Open Data | NYPD complaint, arrest and 311 data; daily. *(inference; high that it exists)* |

### 4.4 Courts

- **NY eCourts** is the umbrella. Three public tools matter: **WebCivil** (Supreme Court and local civil court lookups), **WebCrims** (criminal court lookups) and **NYSCEF** (e-filed documents). *(inference; high on the names, medium on details)*
  - **NYSCEF:** free public viewing of documents in e-filed cases (the fee is for filers); searchable by index number and, for some tools, by party name. Matrimonial, sealed and some other case types are not publicly viewable. Coverage is mandatory e-filing in many counties for civil cases, so it is the richest free state-court document source of the four markets. *(inference; medium)*
  - **WebCrims:** shows case status, next appearance date, judge and part, and charges for criminal cases; no documents. State law seals records after favorable outcomes (acquittal, dismissal) under the criminal procedure sealing provisions, and the Clean Slate Act adds automatic sealing for older convictions on a phased timeline. Cases may therefore disappear from public view; this is a Trust Stack concern. *(inference; medium on sealing, low on exact Clean Slate dates)*
- **Fees:** viewing in these tools was recalled as free; certified copies and some clerk services cost money. *(inference; low)*
- **Federal:** S.D.N.Y. (`nysd`) for Manhattan and Bronx, and E.D.N.Y. (`nyed`) for Brooklyn, Queens and Staten Island. Both are high-volume and high-profile (financial crime, terrorism, organized crime, major civil suits). *(inference; high on the geography)*
- **Volume realism:** SDNY and EDNY together will produce more notable cases per day than the daily brief can use. The ranking logic (case type, parties, press-release backing) matters more than coverage. *(inference)*

### 4.5 Public meetings

- **NYC Council:** Legistar at `legistar.council.nyc.gov`; I recall the Web API needs a token for NYC. *(inference; high on Legistar, low on the token)*
- Panel for Educational Policy, City Planning Commission (land-use calendar), MTA board, 59 community boards (no single platform), Rent Guidelines Board. *(inference; medium)*
- State-level: NY Senate Open Legislation API (free key). *(inference; medium)*
- No NYC Documenters program recalled. *(inference; low)*

---

## 5. Chicago (wave 1; DMA #3)

**State of the repo:** `config/sources/chicago.yaml` lists 10 feeds, all `verified: false`. `config/owners.yaml` knows Chicago Public Media only (Sun-Times and WBEZ); the Tribune and others count as their own groups.

### 5.1 Outlets

| Outlet | Type | Owner (repo or recall) | Feed in repo | My read |
|---|---|---|---|---|
| Chicago Sun-Times | Daily | Chicago Public Media (nonprofit; repo) | `chicago.suntimes.com/rss/index.xml` | **Low-medium.** |
| Chicago Tribune | Daily | Alden-affiliated (recall) | `.../arcio/rss/category/news/` | "Arc pattern; guess." **Low.** |
| WBEZ | Public radio | Chicago Public Media (repo) | `wbez.org/rss/index.xml` | "Low confidence" per the repo. |
| Block Club Chicago | Nonprofit neighborhood newsroom | independent nonprofit | `blockclubchicago.org/feed/` | WordPress style; **medium-high**. |
| WGN, NBC Chicago, ABC7 Chicago, CBS Chicago | TV | Nexstar, NBCU, Disney, Paramount | station patterns | **Medium** (CBS lower). |

### 5.2 Public radio, alt-weekly, nonprofits, others (not in the repo)

- **TV not in the repo:** Fox 32 (WFLD), WTTW (PBS, with WTTW News), Telemundo 44, Univision 66. *(inference; medium)*
- **Public radio:** WBEZ and Vocalo (Chicago Public Media), WTTW, WNUR. *(inference; medium)*
- **Alt-weekly:** Chicago Reader (went nonprofit around 2022); South Side Weekly (nonprofit). *(inference; medium)*
- **Nonprofit and specialist:** City Bureau (Documenters), Injustice Watch (Cook County courts and justice system), Capitol News Illinois (statehouse), Chalkbeat Chicago (education), Better Government Association (watchdog), Illinois Answers Project, Borderless Magazine (immigration). *(inference; medium for existence, low for current activity)*
- **Community and Black press:** Chicago Defender, Chicago Crusader, Wednesday Journal and Growing Community Media suburban papers; Spanish-language outlets such as Hoy. *(inference; low)*
- **Business and legal trade:** Crain's Chicago Business, Chicago Daily Law Bulletin. *(inference; medium)*

### 5.3 Official feeds and press pages

| Source | Note |
|---|---|
| City of Chicago (mayor, departments), Chicago Police Department (news affairs) | Not in the repo. Add. |
| Civilian Office of Police Accountability (COPA) | Releases on police shootings and complaints; useful for public-safety coverage. Not in the repo. *(inference; medium)* |
| Cook County State's Attorney, Cook County Sheriff, Cook County Medical Examiner | Not in the repo. The Medical Examiner's case archive and the State's Attorney's felony case data are on Cook County Open Data (daily to periodic). *(inference; medium)* |
| Illinois State Police, Illinois Attorney General | Not in the repo. |
| U.S. Attorney, N.D. Ill. (in repo) | Path is a "guess" per the repo. |
| Chicago Data Portal | Crimes, 311, permits; daily. *(inference; high that it exists)* |

### 5.4 Courts

- **State:** the Clerk of the Circuit Court of Cook County runs an online case search for civil divisions (law, chancery, domestic relations and others); lookup is free, copies cost per page. Criminal docket access online has been a long-standing gap, and I could not recall whether it is fully online in 2026. The **State's Attorney's open data on felony intake, initiation, disposition and sentencing** is the best free substitute for outcomes. *(inference; medium on civil, low on criminal and on fee amounts)*
- **Federal:** N.D. Ill. (`ilnd`), Eastern Division in Chicago. High volume. *(inference; high on the geography)*
- **Illinois e-filing:** a statewide e-filing system exists (filers pay); public search is by county. *(inference; low)*

### 5.5 Public meetings

- **City Council** uses the City Clerk's own system (eLMS) rather than Legistar today, with a possible API; Legistar was the legacy platform. *(inference; low-medium)*
- **Cook County Board of Commissioners:** Legistar recalled. *(inference; low-medium)*
- **Chicago Board of Education, CTA, Metra, Chicago Police Board, Plan Commission:** platforms not confirmed. *(open)*
- **Illinois General Assembly (ilga.gov):** bill and committee data with RSS, recalled. *(inference; medium)*
- **City Bureau Documenters** publish notes and a meeting calendar for Chicago. *(inference; medium)*

---

## 6. Feeds we could not confirm (consolidated)

**None of the repo's 43 market feeds (8 + 14 + 11 + 10) was confirmed live in this session.** All five files already mark `verified: false` and tell the Beat agent to verify on the first run. My read of their reliability, from the URL pattern alone:

| Likelihood of working | Feeds |
|---|---|
| Higher (standard, widely known or WordPress `/feed/`) | NYT NYRegion; `scdailygazette.com/feed/`; `blockclubchicago.org/feed/`; `thecity.nyc/feed/`; `thesource.metro.net/feed/`; `ktla.com/feed/`; `pix11.com/feed/`; `dailynews.com/feed/`; `amny.com/feed/`; ABC station `/feed/` URLs; NBC station `?rss=y` URLs; NPR; BBC; Guardian |
| Medium | LA Times section feeds; CBS `latest/rss/main` URLs; NWS alert URLs (need a User-Agent) |
| Low (guessed patterns, per the repo's own comments) | The State (widget id); Post and Courier (section slug); City of Columbia and Richland County (CivicPlus guess); `lamayor.org/rss.xml`; `da.lacounty.gov/rss.xml`; all `justice.gov/usao-*/pr/rss.xml` URLs; LAist `index.rss`; WBEZ; Chicago Tribune Arc path; NY Daily News; Gothamist; Supreme Court slip-opinion path |

**Recommendations** *(inference)*:
1. Add **feed autodiscovery** to the RSS sensor: fetch the page and read `<link rel="alternate" type="application/rss+xml">`, rather than hard-coding patterns. This fixes most of the low-confidence group without any research.
2. Fix the `dsc` vs `scd` mismatch in `config/markets.yaml` (or document the alias there).
3. Add the missing official feeds per market (police, sheriff, prosecutors, five NYC DAs, E.D.N.Y. U.S. Attorney, COPA, Cook County State's Attorney, SC Solicitor, SLED, SC Attorney General).
4. Add the missing owner groups to `config/owners.yaml` (Nexstar for WGN and PIX11; Alden/MediaNews for NY Daily News and Chicago Tribune; New York Public Radio for Gothamist/WNYC; Schneps for amNY; Fox for the Fox stations; News Corp for the Post; Newsday). Ownership must be verified first. Without these, two outlets with one owner can look like two independent sources to the Trust Stack.

---

## 7. Court-data access comparison

| Court system | Entry point (recalled) | Free lookup? | Documents | Bulk or API | Main caveat |
|---|---|---|---|---|---|
| LA Superior Court | Court's online case access | Civil summaries: yes (recalled) | Per-document fee in civil (amount unverified) | None recalled | Criminal data thin online; terms not checked |
| NY eCourts: WebCivil / WebCrims / NYSCEF | State Unified Court System | Yes | NYSCEF documents free to view for e-filed cases; WebCrims has none | None recalled | Sealing removes records; matrimonial and sealed cases hidden |
| Cook County Clerk of the Circuit Court | Online case search | Civil: yes | Copies cost per page | County open data for SAO felony and ME data | Criminal docket access unclear |
| SC Judicial Branch Public Index (Richland County) | Public Index | Yes | Clerk copies cost money | None | Lookup only; family and juvenile excluded |
| Federal (all four) | PACER; CourtListener mirror | CourtListener: yes where archived; PACER: $0.10/page | PACER: $3 cap per document | CourtListener REST v4 | RECAP is incomplete; PACER costs add up |

*(all cells: inference; medium-low overall; confirm each before relying on it)*

---

## 8. The next 20 markets (proposal)

### 8.1 Starting point and method

- The blueprint already has a "next 20" list (`docs/blueprint/agent-catalog.md`, Expansion roster, section A) built around a Southeast cluster plus national-beat cities plus music-history cities. It deliberately **left DMA rank and audience out** until they are sourced (Convention 1). This section adds the missing size and news-desert lens and proposes some swaps.
- **Scoring (all *(inference)*):** size band of the DMA (bigger audience and ad pool), news-gap signal (how thin or hollowed the local coverage is), operational reuse (same state or federal court as an existing market, so work is shared) and data openness. Each is scored 1-3 and read as a tie-break, not a precise ranking.
- **DMA rank bands** below are from memory of recent Nielsen rankings and may be off by a few places or a band. **Do not cite them until sourced.**
- **Important point on "news deserts"** *(inference; medium)*: the research literature (Northwestern's Medill State of Local News reports) counts true "news desert" counties, which are overwhelmingly rural. In the top-50 DMAs the opportunity is usually different: a **hollowed legacy daily** (steep newsroom cuts, fewer print days), a **thin suburban and exurban county layer**, and **little or no local daily audio**. An AI network can serve county-level briefs inside a large DMA. That argues for choosing big DMAs with weak county coverage rather than hunting for small markets.

### 8.2 Proposed 20

Federal court ids are standard CourtListener ids (medium-high). "Gap signal" is my recollection of the state of local news and must be checked against Medill data and local press before any use.

| # | Market | DMA band (recalled) | Gap signal (recalled; verify) | Reuse / data note | Fed. court id | Proposed wave |
|---|---|---|---|---|---|---|
| 1 | Charleston, SC | 91-100 | Strong Post and Courier; opportunity is county and audio, not the main daily | Reuses SC courts, statehouse, owner map; hurricanes | `scd` | 2 |
| 2 | Greenville-Spartanburg-Asheville, SC/NC | 31-40 | Gannett-owned daily recalled as hollowed | SC courts and statehouse reuse; DMA straddles NC | `scd` (Greenville), `ncwd` (Asheville side) | 2 |
| 3 | Charlotte, NC | 21-30 | McClatchy daily recalled as hollowed | Carolinas cluster; NC courts (portal terms unknown) | `ncwd` | 2 |
| 4 | Atlanta, GA | 6-10 | Main daily recalled as ending print at the end of 2025 (**low; verify**) | Southeast hub; Fulton County cases | `gand` | 2 |
| 5 | Houston, TX | 6-10 | A large nonprofit startup recalled as closing in 2025 (**low; verify**); Spanish audience | Second Spanish edition; Harris County | `txsd` | 2 |
| 6 | Washington, DC | 6-10 | Many outlets but federal-centric; thin hyperlocal | Supports Breaking Desk; federal courts | `dcd` (+ `cadc`) | 3 |
| 7 | Philadelphia | 4-6 | Civic-news culture is strong, nonprofits active; moderate gap | Large pool; Pennsylvania courts | `paed` | 3 |
| 8 | Dallas-Fort Worth | 4-6 | Daily recalled as shrunk; very large suburban layer | Sports and business beats | `txnd` | 3 |
| 9 | Phoenix | 11-15 | Thin audio coverage for a fast-growing metro (**inference**) | Weather and air quality | `azd` | 3 |
| 10 | Miami-Fort Lauderdale | 11-20 | Spanish and Haitian Creole audiences | Spanish edition; hurricanes | `flsd` | 3 |
| 11 | Tampa-St. Petersburg | 11-15 | Daily recalled as cutting print days; large county layer | Florida cluster with Orlando and Miami | `flmd` | 3 |
| 12 | Orlando | 16-20 | Daily recalled as hollowed under hedge-fund ownership | Florida cluster; tourism and weather | `flmd` | 3 |
| 13 | Detroit | 11-15 | Legacy dailies shrunk; strong nonprofits exist (partners or competition) | Music-history archive fits | `mied` | 4 |
| 14 | Denver | 16-20 | Main daily recalled as hollowed; nonprofit competitors exist | State capital beat | `cod` | 4 |
| 15 | Baltimore | 21-30 | Daily recalled as downsized | Maryland courts; crime-heavy interest | `mdd` | 4 |
| 16 | Pittsburgh | 21-30 | A main daily was recalled as planning to cease publication in 2026 (**low; verify**) | If true, the largest single gap in the list | `pawd` | 4 |
| 17 | Sacramento | 16-25 | Daily recalled as hollowed; state capital | Reuses California statehouse work from LA | `caed` | 4 |
| 18 | San Francisco Bay Area | 6-10 | Many strong nonprofits; moderate gap | Reuses California work; very large ad pool | `cand` | 4 |
| 19 | Nashville | 26-35 | Gannett daily recalled as hollowed | Music-history archive; state capital | `tnmd` | 4 |
| 20 | Raleigh-Durham | 21-30 | State capital; growing; moderate gap | Carolinas cluster | `nced` | 4 |

*(all rows: inference; DMA bands and gap signals unverified)*

### 8.3 How this differs from the blueprint list, and why

- **Added:** Tampa-St. Petersburg, Orlando, Baltimore, Pittsburgh, Sacramento, Raleigh-Durham. Reason: large DMAs with hollowed legacy dailies, and clusters (Florida, Carolinas, California) that reuse state-level work.
- **Moved to alternates:** Seattle, Boston, Minneapolis-St. Paul, Austin, Las Vegas, New Orleans. Reason: Seattle, Boston and the Twin Cities have strong existing local-news ecosystems *(inference; low-medium)*, so the gap is smaller; Austin, Las Vegas and New Orleans are smaller DMAs.
- **Caveat on the music-history lens:** the blueprint put Detroit, New Orleans, Nashville and Las Vegas in wave 5 because their **archive series** (Motown, birth of jazz, Music City, Vegas history) are strong. That is a different axis from daily-brief opportunity, and archive shows do not need a local daily at all. **Recommendation:** decide archive-show cities separately from daily-brief cities, and keep New Orleans, Las Vegas and Boston on the archive list even if they never get a daily. *(inference)*
- **Alternates (next 10):** Seattle-Tacoma, Boston, Minneapolis-St. Paul, Austin, Las Vegas, New Orleans, Cleveland-Akron, San Diego, St. Louis, Indianapolis.
- **Do not lock the order** until: (a) DMA ranks and household counts are sourced and added to the facts sheet, (b) the Medill county-level data is checked per DMA, (c) each state's court-portal terms are cleared by Compliance & Platform Policy Watch, and (d) the first two markets show real download numbers (the sibling notes show planning assumptions of tens to a few hundred downloads per local episode, so market choice matters less than getting the Columbia and Los Angeles economics right).

---

## 9. Risk flags for court and crime content (for the Trust Stack)

*(all inference; general, not legal advice; the repo already drops sealed, juvenile and victim-identity items at intake, `docs/blueprint/agent-catalog.md` line ~456)*

- **Arrest is not conviction.** WebCrims, Public Index and county lookups show charges and statuses that change. The fact-check protocol should require the latest status and the right verb ("charged", "accused", "pleaded").
- **Sealing and expungement differ by state** (New York sealing rules and Clean Slate, California record-relief laws, Illinois sealing and expungement, South Carolina expungement). A record seen once may later vanish; keep source snapshots with dates.
- **Terms of use:** court portals often forbid bulk automated collection or require a license for bulk data. Clear each one before Court Watch scrapes it. The CourtListener route is explicitly built for programmatic use.
- **Volume is not importance** in SDNY, EDNY, C.D. Cal. and N.D. Ill.: rank by case type, party and independent press coverage.

---

## 10. Findings table

All rows: as-of is "recalled; not verified 2026-10-11". Source is the page to confirm against; none was fetched. Rows from the repo cite the file path.

| Fact | Value | As-of | Source | Confidence |
|---|---|---|---|---|
| PACER per-page fee | $0.10 per page | recalled, undated | [PACER pricing](https://pacer.uscourts.gov/pacer-pricing-how-fees-work) | medium / inference |
| PACER per-document cap | $3.00 (about 30 pages) | recalled, undated | [PACER pricing](https://pacer.uscourts.gov/pacer-pricing-how-fees-work) | medium / inference |
| PACER fee waiver | No charge if total is $30 or less in a quarter | recalled, undated | [PACER pricing](https://pacer.uscourts.gov/pacer-pricing-how-fees-work) | low / inference |
| Judicial opinions on PACER | Free | recalled, undated | [PACER pricing](https://pacer.uscourts.gov/pacer-pricing-how-fees-work) | medium / inference |
| CourtListener API | REST v4, token auth, `type=r` search for RECAP dockets | per repo sensor | `earlobe/sensors/courtlistener.py` | medium / inference |
| CourtListener id for D.S.C. | `scd` (repo config says `dsc`; sensor aliases) | per repo | `earlobe/sensors/courtlistener.py` | high / inference |
| CourtListener ids for other four markets' courts | `cacd`, `nysd`, `nyed`, `ilnd` | recalled | [CourtListener](https://www.courtlistener.com/) | medium-high / inference |
| RECAP completeness | Partial; only dockets someone bought or court RSS exposed | recalled | [Free Law Project](https://free.law/) | medium / inference |
| SC Judicial Branch Public Index | Free county-level lookup of civil (Common Pleas) and criminal (General Sessions) | recalled | [SC Judicial Branch](https://www.sccourts.org/) | medium / inference |
| LA Superior Court online access | Civil summary lookup free; document images carry a fee of unknown amount | recalled | [LA Superior Court](https://www.lacourt.ca.gov/) | low / inference |
| NYSCEF public access | Free to view e-filed case documents; some case types restricted | recalled | [NYSCEF](https://iapps.courts.state.ny.us/nyscef/) | medium / inference |
| WebCrims | Criminal case status and next appearance; no documents; sealing removes records | recalled | [NY Courts](https://www.nycourts.gov/) | medium / inference |
| Cook County civil case search | Online and free to look up; criminal docket access unclear | recalled | [Clerk of the Circuit Court](https://www.cookcountyclerkofcourt.org/) | low-medium / inference |
| Cook County open data | State's Attorney felony datasets and Medical Examiner case data | recalled | [Cook County Open Data](https://datacatalog.cookcountyil.gov/) | medium / inference |
| NYC Council platform | Legistar (`legistar.council.nyc.gov`); API token possibly required | recalled | [NYC Council Legistar](https://legistar.council.nyc.gov/) | high on Legistar, low on token / inference |
| Cook County Board platform | Legistar (recalled) | recalled | [Cook County Legistar](https://cook-county.legistar.com/) | low-medium / inference |
| Chicago City Council platform | City Clerk eLMS (not Legistar, recalled) | recalled | [Chicago City Clerk eLMS](https://chicityclerkelms.chicago.gov/) | low-medium / inference |
| City Bureau Documenters | Chicago program with public notes and meeting calendar | recalled | [Documenters](https://www.documenters.org/) | medium / inference |
| States Newsroom republish license | CC BY-NC-ND (recalled); SC Daily Gazette is a States Newsroom outlet | recalled | [SC Daily Gazette](https://scdailygazette.com/) | medium / inference |
| NWS API | Free; requires descriptive User-Agent | recalled | [NWS API docs](https://www.weather.gov/documentation/services-web-api) | high / inference |
| Repo feed count | 43 market feeds (8 + 14 + 11 + 10), all `verified: false` | 2026-10-11 | `config/sources/*.yaml` | high (repo fact) / inference |
| Repo owner-group gaps | Only McClatchy, Evening Post, Gray, TEGNA, States Newsroom, LA Times, SCPR, Nexstar (partial), NBCU, Disney, Paramount, MediaNews, NYT, Chicago Public Media listed | 2026-10-11 | `config/owners.yaml` | high (repo fact) / inference |
| Missing from repo feeds | E.D.N.Y. U.S. Attorney; five NYC DAs; NYPD; LAPD; LASD; CPD; COPA; Cook County SAO; Columbia PD; Richland Sheriff; SC Solicitor; SLED; SC AG | 2026-10-11 | `config/sources/*.yaml` | high (repo fact) / inference |
| Blueprint "next 20" | Charleston, Greenville, Charlotte, Atlanta, Houston, DC, Philadelphia, Phoenix, DFW, Miami, Bay Area, Seattle, Denver, Austin, Boston, Detroit, New Orleans, Nashville, Las Vegas, Twin Cities | 2026-10-11 | `docs/blueprint/agent-catalog.md` | high (repo fact) / inference |
| Proposed swaps | Add Tampa, Orlando, Baltimore, Pittsburgh, Sacramento, Raleigh-Durham; alternates: Seattle, Boston, Twin Cities, Austin, Las Vegas, New Orleans | 2026-10-11 | section 8 | low-medium / inference |
| Columbia SC DMA band | about 71-80 | recalled | [Nielsen DMA ranks](https://www.nielsen.com/) | low / inference |
| Los Angeles / New York / Chicago DMA ranks | 2 / 1 / 3 | recalled | [Nielsen DMA ranks](https://www.nielsen.com/) | medium-high / inference |
| True news-desert counties are mostly rural | Medill State of Local News reports | recalled | [Medill Local News Initiative](https://localnewsinitiative.northwestern.edu/) | medium / inference |
| PACER planning cap for Court Watch | $150-$300 a month for all federal courts (proposal) | 2026-10-11 | section 1.1 | low / inference |

---

## 11. Open questions / gaps, with ready-to-send searches

**Gaps:**
1. Current PACER fee schedule and whether anything changed in 2025-2026; which of the five district courts publish public RSS feeds and what they include.
2. CourtListener v4: exact field names, rate limits, RECAP hit rate for our five courts, and whether a court's new-case RSS is polled quickly enough for a daily brief.
3. LA Superior Court: current fee schedule for document images, criminal case access online, and media-specific access.
4. NYC: current WebCrims/NYSCEF scope, Clean Slate sealing dates, and any terms against automated access.
5. Cook County: whether criminal case search is online, per-page copy fees, bulk or open-data coverage of the Clerk's own data.
6. SC: Richland County Public Index scope (magistrate and municipal courts?), fees for copies, automated-access terms.
7. Which public-meeting platform each body uses (all four markets); whether Legistar APIs are open or token-gated.
8. Reuse licenses of each nonprofit newsroom; Documenters network cities and notes license.
9. Live status of all 43 repo feeds; feed paths for the missing official sources.
10. Nielsen DMA ranks and household counts for all 24 markets (the four plus the proposed 20); Medill county-level counts per DMA; current state of the "gap signal" recollections for Atlanta, Houston, Pittsburgh and others.
11. Ownership of Columbia's Fox and ABC stations, and of the NYC and Chicago outlets missing from `owners.yaml`.

**Searches to send in a follow-up (standard unless noted):**
1. `PACER fees $0.10 per page $3 cap quarterly waiver 2026` (standard)
2. `CourtListener REST API v4 rate limits search RECAP dockets` (standard)
3. `PACER RSS feeds district court Central District of California Southern District of New York` (standard)
4. `Los Angeles Superior Court online case access fees civil document images criminal` (extended)
5. `New York eCourts WebCrims NYSCEF public access Clean Slate sealing 2026` (extended)
6. `Cook County Clerk of the Circuit Court criminal case search online fees` (extended)
7. `South Carolina Judicial Branch Public Index Richland County scope fees terms` (extended)
8. `Documenters network cities City Bureau 2026 license` (standard)
9. `Medill State of Local News 2025 report metro areas newspapers lost` (extended)
10. `Nielsen DMA rankings 2025-26 top 60` (standard)
11. `Pittsburgh Post-Gazette cease publication 2026` (extended)
12. `Atlanta Journal-Constitution end print edition` (standard)
13. `Houston Landing shut down` (standard)
14. `SC Daily Gazette republish Creative Commons license` (standard)
15. `Block Club Chicago republishing policy`, `LAist republish policy`, `THE CITY republish policy` (standard)
16. `NYC Council Legistar API token`, `Chicago City Clerk eLMS API`, `Cook County Board Legistar` (standard)
17. `Richland County Council agendas platform`, `City of Columbia SC council agenda Legistar`, `Richland One BoardDocs` (standard)
18. `LA City Council agendas PrimeGov`, `LA Metro board Legistar`, `LAUSD Board of Education agendas platform` (standard)
19. `Richland County SC Solicitor Fifth Circuit press releases`, `Columbia Police Department press releases` (standard)
20. For feed checks, fetch each site's homepage once and read the `<link rel="alternate">` tag (the Beat agent can do this at run time).

---

## 12. Sources

None of these was fetched in this session. They are the pages to confirm each claim against.

- [PACER: pricing and how fees work](https://pacer.uscourts.gov/pacer-pricing-how-fees-work)
- [CourtListener](https://www.courtlistener.com/) and [Free Law Project](https://free.law/)
- [SC Judicial Branch](https://www.sccourts.org/) and the Public Index
- [LA Superior Court](https://www.lacourt.ca.gov/)
- [NY Courts](https://www.nycourts.gov/) and [NYSCEF](https://iapps.courts.state.ny.us/nyscef/)
- [Cook County Clerk of the Circuit Court](https://www.cookcountyclerkofcourt.org/) and [Cook County Open Data](https://datacatalog.cookcountyil.gov/)
- [NYC Council Legistar](https://legistar.council.nyc.gov/), [Cook County Legistar](https://cook-county.legistar.com/), [Chicago City Clerk eLMS](https://chicityclerkelms.chicago.gov/)
- [Documenters (City Bureau)](https://www.documenters.org/)
- [SC Daily Gazette (States Newsroom)](https://scdailygazette.com/)
- [NWS API documentation](https://www.weather.gov/documentation/services-web-api)
- [Medill Local News Initiative](https://localnewsinitiative.northwestern.edu/)
- [Nielsen](https://www.nielsen.com/) (DMA rankings)
- Repo files: `project-earlobe/config/markets.yaml`, `config/sources/{columbia-sc,los-angeles,new-york,chicago,national}.yaml`, `config/owners.yaml`, `earlobe/sensors/courtlistener.py`, `docs/blueprint/agent-catalog.md`, `docs/CONVENTIONS.md`
