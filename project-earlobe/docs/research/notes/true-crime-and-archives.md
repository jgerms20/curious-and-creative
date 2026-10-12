# True Crime, Cold Cases and History Archives: Data Sources and Rules

Research notes for Project Earlobe (Curious & Creative Network). Prepared 2026-10-11.
Shows in scope: Cold Case Files, Case Tracker, LA Courts Roundup, History of Hollywood, plus the crime items in the dailies and the Breaking Desk, and the catalog's proposed Missing / Solved / Exonerated / Hometown History / Front Page 100 Years Ago series.

---

## READ THIS FIRST: verification status of this document

This note was written under a hard research limit, and the reader should weight every claim accordingly.

- **WebSearch was unavailable.** The run's shared search budget (200 calls per turn, spent by other agents in the workflow) was already used up before this task began. All six opening searches were refused. I did not try to get around the limit.
- **WebFetch was blocked on every domain I tried (once each, per the rules):** namus.nij.ojp.gov, murderdata.org, charleyproject.org, doenetwork.org, courtlistener.com, loc.gov, justice.gov, en.wikipedia.org, fbi.gov, archive.org, cdnc.ucr.edu, copyright.cornell.edu. Every call failed with a name-resolution error (network policy), not a page error.
- **A previous attempt left nothing.** The notes path did not exist when I started, so this is a fresh write, not a continuation of saved partial work.
- **Two kinds of content follow, and each is tagged:**
  - **[repo]** = read this session from the project's own files (standards, sensors, configs, agent catalog). These are accurate descriptions of what the project has decided or built. They are not external facts.
  - **[recalled]** = from the author's background knowledge (cutoff about mid-2026), **not retrieved or re-checked this session**. Every [recalled] item is `kind: inference` and no higher than `confidence: medium`. URLs, rate limits, counts, statute numbers and terms-of-use wording in particular must be re-verified before anything depends on them.
- **Do not treat this file as legal advice.** It is a research starting point for a lawyer and for the Beat / Archive agents. See "Open questions" for the verification worklist.

---

## TL;DR

For true crime, the safe architecture is: **official records are the only citable basis; community databases are leads; nobody's text is copied.** Federal and state press feeds (DOJ and U.S. Attorney releases, FBI Wanted / ViCAP appeals, state AG and DA releases, police cold-case pages) and court dockets (CourtListener RECAP for federal, state portals for local) are the whitelist for anything that names a person or states a legal status. NamUs is the best national missing / unidentified-persons record but should be used as a case index with manual or permissioned access, not scraped in bulk. The Charley Project and Doe Network are volunteer-written, copyrighted compilations: use them only to discover cases, then confirm and cite the agency. The Murder Accountability Project and the FBI Crime Data Explorer give aggregate context only (never individuals). Othram / DNA Doe Project announcements are good "solved" triggers, but only once a police agency or medical examiner has announced the result.

For history, the rule is a **rights gate**: quote only items that are clearly public domain (U.S. works published 1930 or earlier as of 2026; 1931 works enter on 2027-01-01), U.S. government works, or openly licensed items, and use everything else for facts in the show's own words. The machine-friendly, rights-clearer sources are Library of Congress (Chronicling America via loc.gov), Internet Archive, the Media History Digital Library / Lantern, the California Digital Newspaper Collection, Calisphere, HathiTrust and National Archives. Newspapers.com and similar licensed archives must not be scraped or quoted; Wikipedia is a tier-4 lead (and CC BY-SA if any wording is reused). The Margaret Herrick Library is a finding-aid source, since most holdings are unpublished and still protected.

On ethics and law, the project's existing standards (NEVER-2 minors, NEVER-3 sexual-assault victims, FAIR-4/5/6, ATT-3 to ATT-5, FC-LEGAL) already cover the core. The research adds six gaps to close before the strict-lane shows go live: (1) the Legal Screener never sees the episode **title, description, show notes, transcript or social copy**, which are separate publications with their own defamation exposure; (2) no built mechanism yet for **outcome follow-through** (dropped charges, acquittals) on past episodes; (3) the cold-case rules conflict with the catalog's **"Missing" series** (child appeals) and with **deceased child or sexual-assault homicide victims** whose names police publish in appeals; (4) a **family / subject takedown SLA**; (5) **wrong-person** matching rules for common names; (6) no **rights flag** enforced on history quotations. Recommendations for each are below.

---

## 1. Cold case and missing / unidentified persons data

### 1.1 Source-by-source

All access and terms details are [recalled] unless marked [repo]. Re-verify each before building.

| Source | What it is | Machine access | Reuse terms (best recollection) | Recommended role | Tier |
|---|---|---|---|---|---|
| **NamUs** (National Missing and Unidentified Persons System, namus.nij.ojp.gov) | Federally funded (DOJ / NIJ) national database of missing, unidentified and unclaimed persons. Cases entered by law enforcement, medical examiners / coroners, and (after validation) the public / families. Public pages show limited fields; sensitive fields are law-enforcement-only. | Public search site. I believe the site is driven by an undocumented JSON backend, but there is no published public API contract. Do not assume an API. | U.S. federal program, but entries and photos are contributed by agencies and families, so government-work status is not guaranteed for every field. Site has terms of use; check for any automated-access language. | Case index and cross-check. Cite the NamUs case ID, then confirm status with the investigating agency. Statuses go stale (located people stay listed). Manual or permissioned access only until terms are checked. | 1 for "this record exists and says X"; treat the case status as unverified until the agency confirms |
| **Doe Network** (doenetwork.org) | All-volunteer nonprofit (founded around 1999) listing unidentified remains and long-term missing persons, with volunteer-written case summaries. | Website only. No API. | Volunteer-authored compilation; copyright and terms restrict copying. Treat as copyrighted. | **Lead only** [repo: the agent catalog already says "leads only"]. Never a source of record. | 4 |
| **Charley Project** (charleyproject.org) | Long-running, one-editor database of cold-case missing persons (thousands of cases, mostly pre-2000s plus many recent), each with a narrative written by the site's author. | Website only. No API. | Copyrighted narrative text. Do not reproduce or closely paraphrase. | **Lead only.** The facts must be re-sourced from the agency, NamUs or a news archive. | 4 |
| **Murder Accountability Project (MAP)** (murderdata.org) | Nonprofit that compiles U.S. homicide records (FBI Supplementary Homicide Reports plus records obtained from agencies that did not report). Includes clearance (solved / unsolved) flags. | Bulk CSV downloads (data page). | Offered for free download for research and journalism, with a request to cite MAP (recalled; confirm the exact license text). | **Aggregate context only** ("how many unsolved homicides in this county"). Records have no victim names, so never use it to identify a person. | 3 |
| **FBI Crime Data Explorer (CDE)** | FBI's UCR / NIBRS statistics portal and API (key via api.data.gov). SHR was retired in favor of NIBRS reporting, so older homicide tables and newer NIBRS data are not directly comparable. | JSON API with a free key. | U.S. government work, public domain. | Aggregate statistics with the as-of year and the agency-coverage caveat spoken or noted. | 1 for the figure, with coverage caveats |
| **FBI Wanted / ViCAP appeals** (fbi.gov/wanted, including the ViCAP missing, unidentified and unsolved-homicide categories) | FBI's public appeals: Ten Most Wanted, Seeking Information, Missing Persons, and ViCAP (Violent Criminal Apprehension Program) public alerts. | I believe a public JSON endpoint exists (api.fbi.gov/wanted/v1/list) with paging and category filters; confirm. Field-office news pages also publish releases. | U.S. government work; individual photos may be from third parties. Audio-only network, so we do not use images. | Strong "active appeal" trigger for Cold Case Files and Missing. Gives the official tip line to read out. | 1 |
| **State / local cold-case units: LAPD, LASD, NYPD, Chicago PD, SLED (SC)** | Each runs its own unsolved-homicide or missing-persons pages, some with rewards. Candidates I recall: LAPD Cold Case Homicide unit pages; LASD Homicide Bureau unsolved-cases site; NYPD Cold Case Squad; SLED's Missing Persons Information Center and unsolved-case postings. | Per-agency web pages, mostly no feeds. Beat agents must discover and verify each URL. | Public agency content, generally attributable; verify each site's terms. Photos and flyers may belong to third parties. | Primary source for a specific case. The tip line comes from this page and nowhere else. | 1 |
| **Medical examiner / coroner open data** (LA County Medical Examiner, Cook County Medical Examiner, SC county coroners) | Some publish decedent datasets (name fields vary by office). | Open-data portals (Socrata / ArcGIS style) for some offices. | Public records; naming rules vary by office. | Confirms death and manner; official source for NOK-notified naming (see VP-5.6 [repo]). | 1 |
| **Othram / DNASolves** (dnasolves.com, Texas-based forensic genomics company) | Company that does forensic genetic genealogy (FGG) for agencies; its DNASolves site posts case pages and press-style announcements, often jointly with the agency. | Website and press releases. | Company-written copy; copyrighted. Facts are free; wording is not. | "Solved / identified" trigger. **Air only after the agency or ME announces.** Attribute to the agency. | 3 (the agency announcement is the tier-1 basis) |
| **DNA Doe Project** (dnadoeproject.org) | Volunteer nonprofit that identifies unidentified decedents via FGG, with case pages and news posts. | Website. | Volunteer-written copy; copyrighted. | Same as Othram: lead and trigger, with the agency / ME as the cited source. | 3 |
| **Other unsolved-case sites** (Websleuths, Reddit r/UnresolvedMysteries, Project: Cold Case, Murderpedia, YouTube / TikTok true-crime channels, "justice for" Facebook groups, GoFundMe pages) | Crowdsourced or unvetted. | n/a | n/a | **Do not use as sources.** At most, a human-free system should not ingest them at all (NEVER-6 [repo]: no unverified social posts). Project: Cold Case is a lead index only. | 4 / excluded |

### 1.2 Practical implications

- **No bulk scraping of volunteer sites.** Doe Network and Charley Project are small, volunteer-run and copyrighted; scraping them is both a terms risk and a relationship risk. The only safe use is a human-scale lookup or a written permission. Recommend the Cold-Case Archivist agent record a `lead_url` for them but never copy fields into dossiers.
- **Facts versus expression.** Facts about a case (date, place, agency) are not copyrightable (Feist v. Rural Telephone, 1991 [recalled, well established]). What is protected is the compiler's wording and selection. The existing COPY-1 / COPY-5 rules [repo] (own words, store only our own summary or a short excerpt) already fit.
- **Status staleness is the main accuracy risk.** Missing-person entries are left up after someone is found, and cold cases are solved without the aggregator updating. The existing 7-day present-tense recheck for "still unsolved" [repo: verification-protocol, evergreen rows] should hit the agency page and NamUs, never an aggregator alone.
- **Tip lines must be quoted from the agency's own current page**, never recalled or carried from a database. A wrong or retired number is a harm.
- **Marsy's Law and victim-privacy statutes reduce what agencies release** in some states (South Carolina's constitution has a victims' rights amendment of this type [recalled, low]). Do not reconstruct a withheld victim name from side sources such as obituaries or court filings; if the agency did not name the person, we do not.

---

## 2. Live case tracking

### 2.1 Federal

| Source | What it gives | Access | Notes |
|---|---|---|---|
| **DOJ press releases** (justice.gov) | Nationwide releases from Main Justice and components. | I recall a JSON API at justice.gov/api/v1/press_releases.json with page, page-size (max about 50) and component filters [recalled, low], plus RSS. The repo's national config already points at `justice.gov/news/rss?type=press_release&m=1` flagged "query params from memory" [repo]. Expect bot filtering on justice.gov; send an identifying User-Agent and fall back to RSS. | U.S. government work. Releases usually carry the line that an indictment is an allegation and defendants are presumed innocent; keep that framing. DOJ policy is not to comment on uncharged people. |
| **U.S. Attorney offices** (justice.gov/usao-<district>/pr) | Per-district releases; the LA market's CDCA feed is in config as a guess [repo]. | Per-district RSS / page. | Best tier-1 source for federal charging, pleas and sentencings. |
| **FBI field offices and FBI Wanted** | Local appeals and arrests. | See table in 1.1. | Appeals, not convictions. |
| **CourtListener (Free Law Project)** | RECAP archive of PACER dockets, search, docket and docket-entry endpoints, search alerts and docket alerts, webhooks. | REST API v4 with a token. The repo's sensor already uses `GET /api/rest/v4/search/?type=r&court=...&filed_after=` [repo]; its docstring says the field names were not confirmed against live docs and must be checked on the first keyed run. Authenticated rate limits are in the low thousands of calls per hour (I recall 5,000/hour [recalled, low]). Docket alerts are limited per account tier [recalled, low]. | Coverage is only what RECAP users and court RSS feeds have supplied, so it is **incomplete**: a missing docket entry is not evidence nothing happened. Pair with PACER (fees about $0.10/page, $3 cap per document, with a small quarterly waiver [recalled, medium]) for any "status as of" claim on a strict-lane show. |
| **PACER** | Authoritative federal dockets. | Paid, per-page, no free bulk API. | Budget it as a line item for Case Tracker's status checks. |

### 2.2 State and local

| Source | Notes |
|---|---|
| **State attorney general releases** | CA, NY, IL, SC AG offices all publish news pages / feeds (California DOJ also runs the OpenJustice data portal and a missing / unidentified persons unit). Tier 1 for what the AG alleges or announces. Attribute. |
| **DA and Solicitor releases** | LA County DA releases (config guess: da.lacounty.gov [repo]). **South Carolina uses "Solicitors", not district attorneys**; Columbia sits in the Fifth Judicial Circuit (Richland and Kershaw) and Lexington County is in the Eleventh Circuit [recalled]. Scripts must use the right title. Tier 1 for the office's own allegations, attributed as claims, never as established fact (ATT-5 [repo]). |
| **State court portals** | SC Judicial Branch public index by county (Richland: `publicindex.sccourts.org/...` [recalled, medium-low]); LA Superior Court case access and calendars; NY eCourts / WebCrims; Cook County Clerk. These are not designed for machines, often CAPTCHA-gated, and their terms commonly bar automated scraping. Treat as **manual or low-rate, permission-checked** lookups; the engine's `markets.yaml` already lists them by name [repo]. California limits remote access to some criminal court records; expect case-number-driven lookups rather than name searches [recalled, low]. |
| **Court calendars** | Useful as a forward-looking trigger (arraignment dates, trial dates), but a calendar entry is not an outcome. Never report an outcome from a calendar. |
| **Courtroom audio or video** | Do not use. Federal criminal courts bar broadcasting, California requires permission for recording (Rule 1.150), and COPY-6 [repo] already bars third-party audio. |

### 2.3 Tracking rules the engine should enforce (recommendations, all inference)

1. A person enters a tracked case only once there is an **official charging record** (complaint, information, indictment) or an on-record agency naming (FAIR-5 [repo]).
2. Every status sentence carries an **"as of" date**, and the status word matches the newest docket entry (FC-LEGAL-3 [repo]).
3. **Match defendants on case number plus court plus a second identifier**, never on name alone (wrong-person guard; see 4.8).
4. Poll cadence: federal tracked dockets every 30 to 60 minutes while a case is "hot"; otherwise daily; weekly docket sweep for all tracked cases to catch dismissals, sealing, transfers and verdicts that arrive quietly.

---

## 3. History of Hollywood and hometown history archives

### 3.1 Source-by-source

All [recalled] unless marked; verify before building.

| Source | What it holds | Access | Rights / reuse | Role |
|---|---|---|---|---|
| **Media History Digital Library (MHDL) and Lantern** (mediahist.org, lantern.mediahist.org) | Large digitized collection of film, broadcasting and sound trade periodicals (for example Variety, Motion Picture Herald, Photoplay, Moving Picture World, Film Daily). Lantern is the full-text search layer; the scans live on the Internet Archive. | Lantern search site; underlying items and OCR text reachable through Internet Archive APIs. | The library says materials are in the public domain or used by permission, but **rights vary per title and year**. Apply the date rule in 3.2 per issue. | Primary-period trade-press source for History of Hollywood. Tier 2 for contemporary reporting; remember trade press repeats studio publicity (VP-9.22 [repo]). |
| **Library of Congress, Chronicling America** | Digitized U.S. newspapers; coverage reaches into the 1960s. | The classic chroniclingamerica.loc.gov search / OCR URLs and JSON are being moved under loc.gov (JSON via `?fo=json`) [recalled, low-medium]: **confirm which endpoints are current before coding**. LoC publishes request-rate limits and blocks clients that exceed them [recalled]; start at 1 request per second with backoff. | LoC states it does not hold the copyright and flags that newspapers more than 95 years old are public domain; later issues are "rights unknown" and the user bears the burden [recalled, medium]. | Primary source for hometown history and "Front Page, 100 Years Ago". Tier 2 for contemporary reports; treat period reporting on crime and race with caution (see 4.10). |
| **Internet Archive** (archive.org) | Books, periodicals, audio, video, Wayback captures. | Advanced Search, metadata API per item, full-text search, Wayback availability API; open-source `internetarchive` client. | The Archive is a host, not the rights owner. Read each item's license / rights metadata; user-uploaded items can be mislabeled. | Source of scans; rights check required per item. |
| **California Digital Newspaper Collection (CDNC)** (cdnc.ucr.edu; UC Riverside, funded through the California State Library) | Digitized California newspapers, for example the Los Angeles Herald and San Francisco Call among others, with page-level OCR. | Search site and per-page URLs; no formal public API recalled. Ask UCR about bulk access. | Site states the Center does not own the content and asks for citation; items are public domain or used with permission; commercial reuse may need permission [recalled, medium-low]. | Primary source for LA and California history, where the gap in LoC coverage matters. |
| **Calisphere and DPLA** | Aggregators of California / U.S. library and museum collections. | APIs (DPLA API key; Calisphere has data access). | Rights statement per item; must be read per item. | Image and document leads (we do not use images in audio, but show notes can link). |
| **National Archives catalog; HathiTrust; Smithsonian Open Access** | U.S. records; full-view public-domain volumes; CC0 items. | APIs (NARA key; HathiTrust data APIs; Smithsonian Open Access API). | U.S. government works are public domain; HathiTrust opens items by year as the PD line moves; Smithsonian marks CC0. | Rights-clear sources. |
| **Margaret Herrick Library** (Academy of Motion Picture Arts and Sciences, Beverly Hills) | Major research collection on film: scripts, production files, studio publicity, personal papers. | Finding aids online; items by reading-room visit or reproduction request; limited digital collections. | Mostly **unpublished** or restricted papers, so copyright generally runs life-plus-70 and the library imposes its own use conditions. | Source of **facts and leads via finding aids**. Never quote or reproduce unpublished items. A fully automated pipeline cannot visit; use published books and PD periodicals instead. |
| **Wikipedia** | Encyclopedia, CC BY-SA 4.0 (since 2023, with GFDL still offered) [recalled, medium]. | MediaWiki REST and Action APIs; Wikimedia requires an identifying User-Agent and publishes rate guidance [recalled]. | CC BY-SA requires attribution (credit the authors, link the page or history, give the license link, indicate changes) and **share-alike for adaptations**. The license lets attribution be given in a manner reasonable for the medium, so an on-air or show-notes credit with a link is the practical approach [recalled, medium]. | **Tier-4 lead only** [repo: encyclopedias are tier-4 leads]. If any wording or structure is reused, apply CC BY-SA attribution and keep the episode's text share-alike. Simplest and safest: take no wording. For living people, never rely on it. |
| **Newspapers.com, Newspaper Archive, GenealogyBank, ProQuest historical newspapers, Variety Archive, trade-paper paywalls** | Licensed digitized newspapers and trade papers, including the post-PD LA Times and Variety runs. | Subscription sites; terms of service forbid automated access, bulk downloading and commercial reuse (typical, Newspapers.com is owned by Ancestry [recalled, medium]). | Clippings are the publisher's copyright for non-PD material; the site license is personal use. | **Do not scrape, quote or republish.** A human with a subscription can use it to find a fact, which must then be confirmed in a PD or open source before it airs. |

### 3.2 The public-domain line (as of 2026-10-11)

- **U.S. works first published in 1930 or earlier are in the public domain**, per the project's brief and consistent with the 95-year term for works from that period [recalled, medium; confirm on Cornell's "Copyright Term and the Public Domain" chart]. The line moves on 1 January each year: **1931 works enter the public domain on 2027-01-01** (inference from the same rule). 1930 works that became free on 2026-01-01 include the Marx Brothers' *Animal Crackers* and *All Quiet on the Western Front* (film) [recalled, medium]; check any title before use.
- Sound recordings follow a different schedule (Music Modernization Act: recordings from 1923 to 1946 become free 100 years after publication, so 1925 recordings in 2026) [recalled, medium-low]. We play no recordings (COPY-6 [repo]), so this matters only for describing them.
- **Unpublished works** (letters, diaries, studio memos, archive papers) are protected for the author's life plus 70 years, or longer for anonymous or corporate works; the 1930 line does **not** apply to them.
- **Works from 1931 to 1963** might also be free if the notice was missing or the copyright was never renewed, but that needs a renewal-record check per work (Copyright Office records and the Stanford renewal database). An automated pipeline should treat these as **"unknown, facts only"** unless a rights step explicitly clears them.
- **Foreign works restored to U.S. copyright** in 1996 have the same 95-year term from publication, so the 1930 cutoff works for first-published-abroad items too, but check the first publication year [recalled, medium-low].
- **Public domain is not the same as free to use for everything.** Limits that survive: trademarks (a character can be PD while the studio's logo is not), new copyright in restorations, new scores, new translations and annotated editions, and archive access conditions. Right of publicity is its own matter (see 4.9).
- **Facts from non-PD sources are free**; the wording is not. Re-expressing in our own words from a non-PD article is allowed, but a close paraphrase is a copyright risk (COPY-1 [repo]).

### 3.3 Recommended rights gate for history shows (inference)

Every archive item the Archive Miner returns must carry a `rights` flag, and the script checker rejects any quotation whose source item is not flagged clear:

| Flag | Meaning | What the script may do |
|---|---|---|
| `PD` | U.S. publication year 1930 or earlier (2026), or a U.S. government work, or CC0 | Brief attributed quote: up to about 50 words per quote, at most three quotes per episode |
| `OPEN_LICENSE` | CC BY or CC BY-SA with attribution recorded | Quote briefly with the attribution in show notes and spoken credit if the license requires it |
| `UNKNOWN` | 1931 or later, no clearance, or archive mislabels | Facts in our own words only; at most a short phrase of about ten words where the phrasing itself is the point |
| `RESTRICTED` | Unpublished archive paper, licensed archive, or terms bar reuse | Facts only after independent confirmation in a non-restricted source; no quote |

---

## 4. Ethics and legal rules for true crime

The project already has a strong rule set [repo]. This section lists what exists, then the research-based gaps and recommendations. Legal points are [recalled] and flagged for counsel.

### 4.1 What the repo already enforces

- **NEVER-2 (minors):** never name or identify anyone under 18 in crime, court, accident, abuse, health or family-crisis stories, including people who were minors at the time of cold-case events, and jigsaw identification (parent name, address, school plus detail). Hard stop at any severity in every lane (gate rule L2, Legal Screener `naming_minor`).
- **NEVER-3 (sexual-assault victims):** never name or identify anyone who says, or is reported, to have been sexually assaulted, abused or trafficked, even if other outlets have; no exceptions today. Hard stop (`naming_victim`).
- **FAIR-4 / FAIR-5 / FAIR-6:** presumption of innocence; uncharged people are not named as suspects (a named suspect needs an arrest, a charge or an on-the-record agency naming; "person of interest" is not used); private people are named only when the story needs the name.
- **FAIR-10 / FAIR-11:** victims are people, no graphic detail beyond need; if we reported an arrest or charge we report the outcome when we learn it (not yet enforced in code: NE-14).
- **ATT-3 to ATT-5; FC-LEGAL-1 to -8:** every allegation names its accuser; the legal word matches the record **as of air time**; police and prosecutor accounts are attributed.
- **VP-5.6:** a crime victim is named only on a coroner / ME / police basis with next-of-kin status recorded.
- **NEVER-1, NEVER-4, NEVER-7:** no "solving" cold cases on air, no cloned or invented voices or quotes, no pretending to have reported.
- **Corrections (AUTO-6):** note / reissue / retract; any error about a named person in a crime or court story gets a reissue.

### 4.2 Why these rules matter legally (recalled; for counsel)

- **Defamation standard.** Public officials and public figures must show "actual malice" (New York Times v. Sullivan, 1964; Curtis v. Butts, 1967). Private people need only show the media defendant was negligent in most states (Gertz v. Welch, 1974); on matters of public concern the plaintiff carries the burden of proving falsity (Hepps, 1986). There is no general "opinion" safe harbor for statements implying false facts (Milkovich, 1990). Private individuals charged with a crime are the **most exposed category** for us.
- **Fair report privilege** protects accurate, fair reports of official proceedings and records; the usual way to lose it is to drop the attribution, overstate the record, report an outdated status, or add our own embellishment. California codifies this in Civil Code section 47(d); New York in Civil Rights Law section 74; Illinois and South Carolina rely on common law [recalled, medium-low on exact cites]. This is the legal basis for the repo's "attribute to the record, match the legal word, state the as-of date" rules.
- **Republication.** Repeating another outlet's or a database's defamatory statement is a fresh publication. This is why single-source or aggregator-sourced claims about named people are unsafe.
- **No Section 230 shield for our own generated text.** Section 230 protects hosting third-party content; the network is the author of its scripts [recalled, medium]. Recent suits over AI-generated false statements about real people (for example Walters v. OpenAI in Georgia, where the AI provider won summary judgment in 2025 on facts specific to a chatbot with disclaimers [recalled, low-medium]) are not a reliable precedent for an authoritative-sounding news podcast. **Treat every generated sentence about a real person as our own statement.**
- **Statutes of limitation for defamation** in the test markets: California 1 year, New York 1 year, Illinois 1 year, South Carolina 2 years [recalled, medium-low; verify]. Retaining scripts, source packs and trust-log entries for **at least 3 years** covers the longest, with a buffer (inference).
- **Anti-SLAPP protection varies:** strong in California (Code of Civil Procedure 425.16), present in New York and Illinois, and, as I recall, absent in South Carolina [recalled, low; verify]. Practical effect: the Columbia market carries the least litigation protection, so apply the strictest posture there.
- **Juveniles.** Courts have protected truthful publication of a juvenile's lawfully obtained name (Smith v. Daily Mail, 1979), but juvenile court files are confidential or sealed under state law (for example California Welfare and Institutions Code section 827) [recalled, medium-low]. Network policy (never name) is stricter than the law, which is the right call for an unreviewed system.
- **Sexual-assault victims.** Truthful publication from lawfully obtained government records is constitutionally protected (Florida Star v. B.J.F., 1989; Cox Broadcasting v. Cohn, 1975) [recalled, medium], yet journalism standards (SPJ, AP, Dart Center guidance) are not to name them without consent. Some states also restrict identification. Network policy (never name) again exceeds the law.
- **Right of publicity for the dead** (relevant to History of Hollywood): California gives a post-mortem right of publicity for 70 years (Civil Code section 3344.1), with exemptions for news, public affairs, and expressive works such as books, films and programs; it chiefly bites on advertising and merchandise use [recalled, medium-low]. Digital-replica laws (California, Tennessee's ELVIS Act) target voice and likeness cloning [recalled, medium-low]. NEVER-4 already bans synthetic voices of real people. **Rule: no deceased celebrity's name or likeness in ad reads, sponsor copy or promos beyond a factual episode description.**
- **Defamation of the dead** is generally not actionable in the U.S., but surviving family can bring privacy, false-light or emotional-distress claims in some states, and the ethical duty remains (FAIR-12 [repo]).
- **Journalism codes to cite in the standards:** SPJ Code of Ethics (minimize harm; avoid pandering to lurid curiosity; weigh the implications of identifying suspects before charges; update and correct) and the Dart Center's trauma-informed reporting guidance; AP Stylebook discourages "person of interest" [recalled, medium].

### 4.3 Gap 1: titles, descriptions, show notes, transcripts and social copy are not screened

**[repo, verified in code at commit f552995.]** The Legal Screener's prompt contains the episode date, the script lines and the claim list. It does not receive `Script.title`, and the `Episode` fields `title`, `description`, `show_notes_md` and the social posts are generated at the publish stage, where `earlobe/publish/` currently holds only an `__init__.py`. NE-2 in the standards already notes that the gate never sees episode metadata.

**Why it matters:** an episode title like "The Man Who Killed ..." or a social post is its own publication, appears in search and in podcast-app feeds, and is the text most likely to be read without the audio. Titles are where presumption-of-innocence slips happen. **Recommendation:** run title, description, show notes, transcript and every social post through the same Legal Screener, Bias Checker and name checks, with `naming_minor` / `naming_victim` as hard stops, before any publish. Add a title rule for strict-lane shows: no verdict words unless a verdict exists; "faces charges", "is accused", "is charged" only.

### 4.4 Gap 2: outcome follow-through and "right to be forgotten"

FAIR-11 and NE-14 [repo] promise follow-through but nothing is built. Journalism practice (SPJ guidance; newsroom "update or unpublish" programs such as those run by the Boston Globe and Cleveland.com [recalled, medium-low]) is to update stories when charges are dropped or a person is acquitted, and to consider removing names of people who were arrested but never convicted. Recommendations (all inference):

1. **Weekly docket sweep** for every person ever named in a Case Tracker or Courts Roundup episode; a dismissal, acquittal, declination, nolle prosequi, sealing or expungement raises `case.development` for the Tracker and a `Correction` for the original episode.
2. **Follow-up within 72 hours** of an outcome favorable to the accused, given equal prominence to the original story.
3. **Re-issue or note the original episode:** for a private individual whose charges were dropped or who was acquitted, use the existing `reissue` action with the name removed or the episode updated; otherwise attach a dated update note to the show notes and transcript. Never edit silently (AUTO-7 [repo]).
4. **Never name a living private person who is only accused in an evergreen show** (Cold Case Files, History of Hollywood, Front Page 100 Years Ago). Evergreen episodes live indefinitely and cannot be kept current on every accused person.
5. **Sealed or expunged records:** if a record is sealed, expunged or the case is dismissed under a diversion or similar program, stop naming the person and do not republish the old coverage's name.
6. **No mugshots** in show notes, art or social posts.

### 4.5 Gap 3: places where the current hard stops and the planned series collide

These are decisions for the owner, not errors in the rules. Defaults below keep the system safe.

1. **"Missing: {Region}" (proposed series).** Missing-child appeals depend on the child's name being public (AMBER alerts, NCMEC). NEVER-2 forbids naming any minor in a crime story, and there is no exception. **Default for launch: adults only; exclude missing minors entirely.** If the owner later wants child appeals, the narrow exception should be: agency or NCMEC appeal that is **currently active** (re-verified within 24 hours before air), name taken from that appeal, no jigsaw details, expire when the case resolves, and a hard check that the child is not in a custody or protective context. That would be a deliberate code change to the L2 gate, not a prompt tweak.
2. **Deceased child victims in cold cases.** Police routinely publish the name of a murdered child in a cold-case appeal. NEVER-2 explicitly covers people who were minors at the time. **Default: keep the hard stop; tell the story as "a nine-year-old girl" with the agency's tip line.** Cost: some tip-generating power is lost. Revisit in the same decision as item 1.
3. **Deceased victims whose case involved sexual assault.** NEVER-3 as written covers anyone "reported" assaulted, which would bar naming many homicide victims whom police name in their own appeals. **Recommended policy to evaluate: "name or assault detail, not both."** Either name the deceased homicide victim (when the agency names her in a current appeal, she is an adult, and the next of kin question is moot because of the years elapsed) and omit sexual-assault details, or tell the story anonymously with the assault described only as far as the official record requires. Needs a code decision because the Legal Screener currently treats naming as a hard stop at any severity.
4. **Old minors.** NEVER-2 also protects people who were minors in 1926 or 1955 and are certainly dead. For "Front Page, 100 Years Ago" this will flag many stories. Options: keep (simple, safe) or exempt persons documented as deceased for more than 50 years. **Default: keep** until the Legal Screener can handle a date-of-death field.

### 4.6 Gap 4: a family and subject request process

Victims' families and named people will find these episodes. Competitive research in this repo already recommends a codified takedown / correction SLA [repo: liquid-studios-pivot note]. Recommendation (inference): a visible contact address on every show page and feed; `event:legal.threat` and `Correction` records created automatically; **suppress the named content within 24 hours of a credible request** (hide or pull the feed item pending review) and resolve within 7 days; a subject can ask for correction, removal of a name, or removal of detail, and the answer is logged in the public trust log without repeating the name of a minor or sexual-assault victim (the fact-check protocol already says this [repo]). Recommend media liability (errors-and-omissions) insurance be in place before the strict-lane shows go live; the catalog's Contracts & IP Clerk already tracks insurance [repo]. Cost not researched.

### 4.7 Cold-case-specific ethics

- **Do not solve, speculate or crowdsource** (NEVER-1). No theories from forums, no "what really happened".
- **Never name an uncharged suspect.** A deceased suspect that police have named on the record, in a formal announcement, may be named with attribution (FAIR-5). Genetic-genealogy leads are not charges: wait for an arrest, a charge or the agency's formal naming. Never name or describe the genetic relatives whose DNA matched.
- **Unidentified remains:** no graphic description beyond what the agency published, no reconstruction images (audio-only anyway), cite the NamUs case ID. After an identification, wait for the agency or ME announcement and next-of-kin notification (VP-5.6).
- **Always end with the agency's own tip line,** read from its current page and re-verified within 7 days.
- **Don't make families the plot.** State only what the official record or the family said publicly; do not characterize grief or invent quotes (NEVER-4).
- **Minimum case age.** Only air a case as "cold" when the agency calls it cold or it is at least about 3 years old with no arrest; otherwise it is an active investigation and belongs, if anywhere, in the daily news lane. (3 years is an inference from common agency practice; confirm with a former investigator or counsel.)

### 4.8 Wrong-person and stale-status risk (the largest automated-defamation hazards)

- A common name matched across dockets is the classic mistake. **Require case number + court + one more identifier (age or date of birth from the record, or city) on every claim about a named defendant.** If the record cannot supply a second identifier, do not name.
- A stale status (arrested but later released without charge; indicted but later dismissed) is the second hazard. The 7-day rule [repo] helps; for strict-lane shows, any tracked case claim older than 24 hours before air should be re-queried, and if the docket cannot be reached the line carries an as-of date or is cut (FC-LEGAL-3 already says this).
- Standard caveat language comes from the record: "charged", "accused", "pleaded not guilty". Include the defendant's plea or denial when it is on the record (FAIR-3).

### 4.9 History of Hollywood-specific

- **Myth control:** trace each anecdote to its earliest instance (VP-3.15, VP-9.21 [repo]). Hollywood scandal lore is the highest-risk category; a studio publicity story is "legend", not fact (VP-9.22).
- **Hollywood crime history** (unsolved deaths, scandals) is cold-case content. Apply the cold-case rules, especially for events with living relatives or a living accused.
- **No impersonation of the dead:** no invented dialogue, no voice cloning (NEVER-4); PD period quotes only, labeled as such.
- **Ads and promos must not use celebrity names or likenesses** beyond factual episode description (California post-mortem publicity right).
- **No clips or music** (COPY-6, COPY-7 [repo]).

### 4.10 Hometown history (Columbia, Los Angeles)

- **Period newspapers reflect the bias of their time.** Contemporary coverage of racial violence, immigration or labor conflict often used slurs and one-sided framing. Use such text as evidence of what was reported, corroborate with later scholarship, and do not repeat slurs.
- **Descendants exist.** Apply FAIR-12 [repo]: people long dead are still people, and wrongful accusations a century ago can still harm living relatives. Use "was charged with" language, not "murderer", unless there was a conviction on the record.

---

## 5. Recommended source whitelist

Tier labels follow the repo's `SOURCE_TIERS`: 1 official record, 2 established newsroom or wire, 3 specialist, 4 lead only. "Citable" means a sentence may rest on it (with attribution); "lead" means it may only point us to a primary record. Items marked (verify) have URLs or access methods that are unconfirmed.

### 5.1 Tier-1 citable

- DOJ press releases and every U.S. Attorney district feed; FBI Wanted and ViCAP appeals; FBI field-office releases.
- State attorney general news (CA, NY, IL, SC).
- DA / Solicitor / State's Attorney releases (LA County DA, Fifth Circuit Solicitor, Cook County State's Attorney, Manhattan DA).
- Police and sheriff **official** cold-case and appeal pages (LAPD, LASD, NYPD, Chicago PD, SLED, Columbia PD, Richland County Sheriff) (verify each URL).
- Court records: CourtListener RECAP (with PACER confirmation for status claims), state court portals, court press offices, SCOTUS.
- Medical examiner / coroner statements for death and identification.
- NamUs case record (for what the record says; confirm status with the agency).
- FBI Crime Data Explorer for statistics.

### 5.2 Tier-2 corroboration

AP, Reuters (via the GDELT / Google News sensors per the repo config), and established metro and local newsrooms already in the market configs (LA Times, LAist, The State, Post and Courier, SC Daily Gazette, WIS, WLTX, and so on). Used for corroboration and to find original reporting, credited by name (COPY-3).

### 5.3 Tier-3 / tier-4 leads only

Charley Project, Doe Network, Project: Cold Case, DNA Doe Project and Othram / DNASolves pages (valid as triggers; the agency announcement is the cited basis), MAP (aggregate context), Wikipedia (leads), local history society pages.

### 5.4 Excluded

Websleuths and forum posts, Reddit, YouTube / TikTok / podcast true-crime content, social posts and "justice for" pages, GoFundMe and crowdfunding pages, people-search and mugshot sites, Murderpedia, any paywalled archive scraped without a licence, any site whose terms bar automated access.

### 5.5 History whitelist (rights-first)

- **Use and quote when `rights = PD / OPEN_LICENSE`:** Library of Congress (Chronicling America and other collections), National Archives, HathiTrust full-view, Internet Archive items with verified PD status, MHDL / Lantern issues dated 1930 or earlier, CDNC items dated 1930 or earlier, Smithsonian Open Access (CC0), Calisphere / DPLA items with open rights statements.
- **Facts only:** any item dated after 1930 or without a clear rights status; Margaret Herrick finding aids; published books and articles; Wikipedia (lead only).
- **Never scraped or quoted:** Newspapers.com and other licensed archives; unpublished archive papers.

---

## 6. Rules per show

Shows and lanes are from `config/shows.yaml` [repo].

### Cold Case Files (strict lane, 2 Tue / Thu)
1. Entry gate: the case has a **current public agency appeal** with a tip line, confirmed on the agency page within 7 days before publish.
2. Case age at least about 3 years with no arrest, or agency-labeled cold.
3. Name rules: no uncharged suspects; no persons of interest; no minors; adult victims named only when the agency names them in the current appeal; sexual-assault cases follow the Gap 3 decision (default: no name).
4. Leads from Charley Project, Doe Network, forums: never cited; re-source to the agency, NamUs, or tier-1/2 coverage.
5. FGG: air an identification only after the agency or ME announcement; no suspect named from a genetic lead until arrest or charge; do not describe relatives.
6. Update loop: re-check for arrest, solve, identification or located person before publish and weekly for the first 90 days in the feed; a changed status triggers `reissue`.
7. Absolute dates and "as of" wording on all present-tense statements (FC-DATE-4).
8. End with the agency tip line; no theories; no graphic detail beyond the official record.

### Case Tracker (strict lane)
1. Enter a case on an official charging record plus a newsworthiness threshold (at least two independent tier-2 outlets or a tier-1 DOJ / AG release).
2. Status ladder and as-of stamps (FC-LEGAL); defendant's plea or response included.
3. Wrong-person guard (case number + court + second identifier).
4. Weekly docket sweep, 72-hour outcome follow-up, outcome equal in prominence to the charge; name-handling per 4.4.
5. No verdict language in titles; no mugshots; no sealed or juvenile information.

### LA Courts Roundup (strict lane, daily)
1. Sources: LA County DA releases, C.D. Cal. dockets via CourtListener (confirmed with PACER for status), LASC calendars and case summaries (manual / low rate), U.S. Attorney CDCA releases.
2. A calendar entry is a schedule, not an outcome.
3. Name felony defendants only where the story is of public interest; keep low-level private-person matters out (FAIR-6); never juvenile-court or family / probate matters; never sexual-offense complainants.
4. Same follow-through rules as the Case Tracker.

### The Breaking Desk and daily briefs (crime items)
1. Police, sheriff and fire releases and coroner statements attributed as accounts.
2. No suspect names before arrest or charge; no victim names before NOK notified and an official release (VP-5.6); no minors; no cause of death or motive in our own voice.
3. Breaking lane's hold-and-recheck behavior applies; any claim that cannot reach an official record is cut.

### History of Hollywood (archive lane)
1. Rights gate (section 3.3) on every quotation.
2. Primary-period sources first (MHDL / Lantern, CDNC, Chronicling America), earliest-instance tracing for anecdotes (VP-3.15), studio-publicity labeling (VP-9.22).
3. No clips, no music, no cloned or invented voices or dialogue, no celebrity names in ad copy.
4. Unsolved-crime and scandal episodes follow cold-case rules; deceased subjects still get fairness (FAIR-12).
5. Plan a "1931 enters the public domain" content moment for 2027-01-01 (opportunity, inference).

### Hometown History: Columbia / Lost Los Angeles / Central Avenue / Front Page 100 Years Ago (archive lane, proposed)
1. LoC, CDNC and state-library collections only, with `PD` flag for every quote.
2. Contemporary-bias handling (4.10); no slurs; corroborate period crime and race reporting.
3. "Was charged with" language for century-old accusations; keep NEVER-2 for those who were minors, with the old-minors exception as an open decision.

### Missing / Solved / Exonerated (proposed)
- **Missing:** adults only at launch; agency appeal active and re-verified within 24 hours; expire on resolution (Gap 3 item 1).
- **Solved:** from official announcements only; same naming rules as Case Tracker for any accused.
- **Exonerated:** court orders only (vacatur, dismissal, certificate of innocence); use the exact legal outcome word.

---

## 7. Engine implementation notes (for the Beat, Archive Miner and Cold-Case Archivist agents)

These follow from the repo's current sensor design [repo: `earlobe/sensors/courtlistener.py`, `config/sources/*.yaml`].

1. **All national and market feed URLs are marked `verified: false`** and flagged "from memory". The first keyed run must confirm HTTP 200, feed parse and recent items for DOJ, USAO CDCA, FBI, LA DA and every police page before anyone relies on them.
2. **CourtListener:** confirm the v4 field names against a live response (the sensor's own docstring says they were not checked). Add a docket-sweep job for tracked cases and a `COURTLISTENER_TOKEN`. Note CourtListener's alias for the South Carolina district (`scd`) is already handled in `COURT_ALIASES`.
3. **Add sensors:** FBI Wanted (if the JSON endpoint is confirmed), the DOJ press-release API, and a loc.gov Chronicling America client with polite rate limiting. NamUs and state portals stay manual or permission-gated.
4. **Rights metadata:** add a `rights` field to the archive pack item and have the Legal Screener's copyright category reject any quote whose source is not `PD` or `OPEN_LICENSE`.
5. **Screening coverage:** extend the Legal Screener input to include title, description, show notes, transcript and social copy (Gap 1).
6. **Takedown path:** wire the family / subject request channel to `event:legal.threat` and `Correction` (Gap 4).
7. **Audio-only simplification:** no images are used on air, so image-licensing risk is limited to episode art (generated) and any images in show notes (avoid).

---

## 8. Findings table

Kind: O = official or primary document (here: the project's own files), R = reported, I = inference. Confidence reflects what happened this session: nothing external was retrieved, so [recalled] items are capped at medium.

| Fact | Value | As-of | Source | Kind | Confidence |
|---|---|---|---|---|---|
| Project hard stop on naming minors | NEVER-2: no naming or identifying under-18s in crime / court / abuse stories, including minors at time of cold-case events; jigsaw identification covered | repo, 2026-10-11 | editorial-standards.md | O (project policy) | high |
| Project hard stop on sexual-assault victims | NEVER-3: no naming or identifying; no exceptions today | repo, 2026-10-11 | editorial-standards.md | O | high |
| Suspect naming rule | FAIR-5: only after arrest or charge, or on-the-record agency naming; "person of interest" not used | repo | editorial-standards.md | O | high |
| Legal Screener input excludes title and metadata | Prompt = date + script lines + claims; `Script.title` and Episode description / show notes / social posts not passed; `earlobe/publish/` holds only `__init__.py` | commit f552995 | earlobe/trust/legal.py, schemas.py | O | high |
| Follow-through rule not yet built | FAIR-11 / NE-14: outcome tracking and spoken corrections not implemented | repo | editorial-standards.md | O | high |
| Agent catalog treats Doe Network and Charley Project as leads only | "leads only" | repo | agent-catalog.md (cold-case-archivist) | O | high |
| CourtListener sensor field names unconfirmed | Docstring: sandbox could not reach live docs; confirm on first keyed run | repo | courtlistener.py | O | high |
| All source-feed URLs unverified | `verified: false` and "from memory" on national, LA and Columbia configs | repo | config/sources/*.yaml | O | high |
| U.S. public-domain line for published works | 1930 and earlier as of 2026; 1931 on 2027-01-01 | 2026 | brief + Cornell copyright term chart (not fetched) | I | medium |
| Unpublished works not covered by the 1930 line | life plus 70 years (or longer for anonymous / corporate) | 2026 | U.S. Copyright Act (not fetched) | I | medium |
| Facts are not copyrightable | Feist v. Rural Telephone (1991) | n/a | case law (not fetched) | I | medium |
| Wikipedia text license | CC BY-SA 4.0; attribution and share-alike for adaptations; attribution may be reasonable to the medium | 2026 | Wikipedia reuse guidance (not fetched) | I | medium |
| DOJ press-release API | JSON at justice.gov/api/v1/press_releases.json; page size up to about 50; bot filtering likely | 2026 | justice.gov developer docs (not fetched) | I | low |
| FBI Wanted JSON endpoint | api.fbi.gov/wanted/v1/list with paging and filters | 2026 | fbi.gov (not fetched) | I | low |
| CourtListener limits | token auth; thousands of calls per hour; docket-alert caps by tier; RECAP coverage incomplete | 2026 | CourtListener API docs (not fetched) | I | low |
| PACER fees | about $0.10 per page, $3 cap per document, small quarterly waiver | 2026 | PACER (not fetched) | I | medium |
| LoC Chronicling America API in transition | Legacy endpoints moving to loc.gov (`?fo=json`); published rate limits; confirm current | 2026 | loc.gov (not fetched) | I | low |
| LoC rights statement for newspapers | No LoC copyright claim; items over 95 years old are public domain; later issues rights unknown | 2026 | loc.gov rights page (not fetched) | I | medium |
| NamUs access | Public site, no documented public API; sensitive fields law-enforcement-only; entries can go stale | 2026 | namus.nij.ojp.gov (not fetched) | I | low |
| Doe Network and Charley Project reuse | Copyrighted volunteer compilations; no API | 2026 | sites (not fetched) | I | low |
| MAP data | Free CSV downloads of compiled homicide data; no victim names; cite MAP | 2026 | murderdata.org (not fetched) | I | low |
| FGG announcement sources | Othram / DNASolves and DNA Doe Project publish identification announcements, typically with the agency | 2026 | company sites (not fetched) | I | medium |
| Defamation standards | Sullivan (1964), Butts (1967), Gertz (1974), Hepps (1986), Milkovich (1990) | n/a | case law (not fetched) | I | medium |
| Fair-report privilege cites | CA Civil Code 47(d); NY Civil Rights Law 74; IL / SC common law | 2026 | statutes (not fetched) | I | low |
| Defamation limitation periods | CA 1 yr; NY 1 yr; IL 1 yr; SC 2 yrs | 2026 | state statutes (not fetched) | I | low |
| Anti-SLAPP coverage | Strong in CA; present in NY and IL; I recall none in SC | 2026 | state statutes (not fetched) | I | low |
| Juvenile and victim-name case law | Smith v. Daily Mail (1979); Florida Star v. B.J.F. (1989); Cox v. Cohn (1975) | n/a | case law (not fetched) | I | medium |
| Post-mortem publicity right (CA) | 70 years; news / expressive-work exemptions; bites on advertising | 2026 | Civil Code 3344.1 (not fetched) | I | low |
| AI-defamation precedent | Walters v. OpenAI (Georgia) summary judgment for OpenAI in 2025; limited relevance to a news podcast | 2025 | court reports (not fetched) | I | low |
| Section 230 and own-generated content | No shield for content the network itself generates | 2026 | statute (not fetched) | I | medium |

---

## 9. Recommended numbers (all inference, adjustable in config)

| Setting | Recommended value | Why |
|---|---|---|
| Public-domain cutoff (publication year) | 1930 now; 1931 from 2027-01-01 | Brief + 95-year term |
| Minimum cold-case age | about 3 years without arrest, or agency-labeled cold | Avoids active investigations |
| Cold-case agency page recheck before publish | within 7 days (24 hours for any missing-person appeal) | Matches existing present-tense rule; tighter for appeals |
| Strict-lane tracked-claim requery | any status older than 24 hours before air | Stale-status hazard |
| Outcome follow-up SLA | 72 hours | FAIR-11 follow-through |
| Family / subject suppression SLA | 24 hours to suppress, 7 days to resolve | Harm containment |
| PD quotation limit | about 50 words per quote, max 3 per episode | "Brief" in COPY-7 |
| Non-PD verbatim limit | about 10 words, only when wording is the point | COPY-1 |
| Record retention | at least 3 years for scripts, source packs, trust logs | Longest defamation limitation period in test markets (2 yrs) plus buffer |
| LoC polling rate | 1 request per second with backoff | Stay inside published limits |
| Tracked-docket polling | 30 to 60 min while hot; daily otherwise; weekly sweep of all | Timely outcomes |

---

## 10. Open questions and gaps

**Verification worklist (nothing below was confirmed this session):**
1. Terms of use for NamUs (automated access), Doe Network, Charley Project (reuse), MAP (license wording), CourtListener (data license, current rate limits, docket-alert caps), Wikimedia (current API limits), CDNC and MHDL (rights statements), Herrick Library (use conditions).
2. Whether the DOJ JSON API and the FBI Wanted JSON endpoint exist as described; actual field names and rate limits.
3. Current status of the Chronicling America API after the loc.gov migration.
4. Verified URLs and feeds for LAPD / LASD / NYPD / Chicago PD / SLED cold-case pages, LA County DA, Fifth Circuit Solicitor, SC Judicial Branch public index, LASC case access.
5. Current counts (NamUs open cases, Charley Project, MAP unsolved totals, Chronicling America pages, MHDL pages, Othram solved cases) were deliberately left out because I could not check them.
6. State-law specifics for counsel: fair-report cites, limitation periods, anti-SLAPP status in South Carolina, juvenile and sexual-assault confidentiality statutes, victim-rights amendments and what agencies may withhold, California correction-demand statute and whether it covers podcasts.
7. Whether the public-domain claims for specific 1930 titles hold (check each title before an episode builds on it).

**Decisions for the owner:**
- Missing-child appeals and deceased child victims: keep the absolute rule, or build a narrow, auditable exception? (4.5, items 1 to 2)
- Deceased sexual-assault homicide victims named by police: adopt "name or assault detail, not both"? (4.5, item 3)
- Century-old minors: exempt long-dead persons, or keep the rule? (4.5, item 4)
- Whether to buy media liability insurance and retain media-law counsel before the strict-lane shows launch.
- Whether to fund PACER for Case Tracker status checks.

**Research I could not do:** the competitive question of how existing AI-produced true-crime podcasts handle these rules, and any 2026 enforcement or litigation news affecting AI-generated true crime. Both need live search.

---

## 11. Sources

**Documents read this session (repo):**
- [Editorial standards](../../standards/editorial-standards.md)
- [Fact-check protocol](../../standards/fact-check-protocol.md)
- [Verification protocol](../../standards/verification-protocol.md)
- [Agent catalog](../../blueprint/agent-catalog.md)
- [Show registry](../../../config/shows.yaml) and [markets](../../../config/markets.yaml)
- [National source feeds](../../../config/sources/national.yaml), [Los Angeles](../../../config/sources/los-angeles.yaml), [Columbia SC](../../../config/sources/columbia-sc.yaml)
- [Legal Screener](../../../earlobe/trust/legal.py), [CourtListener sensor](../../../earlobe/sensors/courtlistener.py), [press sensor](../../../earlobe/sensors/press.py), [schemas](../../../earlobe/schemas.py)
- [Liquid Studios pivot and press notes](liquid-studios-pivot-and-press.md) (takedown / correction SLA recommendation)

**External pages to verify (listed from memory; NOT fetched, not confirmed to exist at these addresses):**
- [NamUs](https://namus.nij.ojp.gov/)
- [Doe Network](https://www.doenetwork.org/)
- [Charley Project](https://charleyproject.org/)
- [Murder Accountability Project](https://www.murderdata.org/)
- [FBI Wanted and ViCAP](https://www.fbi.gov/wanted/vicap)
- [DOJ developer / API documentation](https://www.justice.gov/developer)
- [CourtListener REST API help](https://www.courtlistener.com/help/api/rest/)
- [Library of Congress APIs](https://www.loc.gov/apis/)
- [Internet Archive terms](https://archive.org/about/terms.php)
- [California Digital Newspaper Collection](https://cdnc.ucr.edu/)
- [Media History Digital Library](https://mediahist.org/) and [Lantern](https://lantern.mediahist.org/)
- [Wikipedia: Reusing Wikipedia content](https://en.wikipedia.org/wiki/Wikipedia:Reusing_Wikipedia_content)
- [Cornell: Copyright term and the public domain](https://copyright.cornell.edu/publicdomain)
- [DNASolves (Othram)](https://dnasolves.com/) and [DNA Doe Project](https://dnadoeproject.org/)
- [SPJ Code of Ethics](https://www.spj.org/ethicscode.asp) and [Dart Center for Journalism and Trauma](https://dartcenter.org/)
