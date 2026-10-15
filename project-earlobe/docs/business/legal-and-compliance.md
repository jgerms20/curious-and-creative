# Legal and compliance: what can go wrong and how we stay inside the lines

**The Curious & Creative Network · as of 2026-10-12 · DRAFT for Joshua and Janel.** Built from the [legal research note](../research/notes/legal-compliance-business-setup.md), the [standards](../standards/README.md) and the [facts sheet](../research/facts-and-figures.md) (IDs like `F-LEGAL-10`).

> **NOT LEGAL ADVICE.** This is a research summary to help the founders brief a licensed media lawyer and a CPA. Items tagged **[LAWYER]** or **[CPA]** need a professional before anyone relies on them. **Nothing here was checked live:** every statute, case, fee and platform rule comes from recall or earlier search snippets, and the facts sheet rates most legal rows medium or low confidence. *As of Oct 2026 — verify before buying or relying.* Our own reasoning is marked *(inference)*.

## The 30-second version

| Question | Short answer |
|---|---|
| **Who is liable?** | Curious & Creative LLC, as publisher of every episode. Section 230 does not cover scripts we write ourselves (F-LEGAL-11). |
| **Biggest exposure** | Naming private people in court and crime stories (Case Tracker, LA Courts Roundup, Cold Case Files, Breaking Desk). Saying someone committed a crime is libel per se if wrong. |
| **Main shield** | The fair report privilege: a fair, accurate, attributed account of official records. It holds only if every allegation is tied to an official source and we add nothing (section 3). |
| **Copyright** | Facts are free, wording is not. Our risk is in what we output, not in training (section 4). |
| **AI disclosure** | One standard everywhere: spoken at the end, in metadata, YouTube toggle on. Rules are converging, not conflicting (section 6). |
| **Voices** | Original synthetic voices only. Never clone or imitate a real person (section 7). |
| **Money items that matter** | Media liability (E&O) insurance, about $6,000 a year as a placeholder, and a one-time media-lawyer review, $2,500 to $7,500 (F-LEGAL-01, -02). Both before court or crime episodes auto-publish. |

## 1. Risk map by show

| Lane / show | Main exposure | Severity | Main protections |
|---|---|---|---|
| LA Courts Roundup, Case Tracker (strict) | Defamation, wrong-person errors, false light, sealed or juvenile records | **Highest** | Fair-report drafting, official-record-only naming, identity matching, insurance |
| The Breaking Desk | Naming unconfirmed suspects or victims; copying one outlet's scoop | High | Three independent sources; no names before an official release; credit "first reported by" |
| Cold Case Files, History of Hollywood | Defaming living people; invented dialogue; dead stars' voices; archive re-releases restart the clock; *Cold Case Files* name collision | Medium-high | No invented quotes, no uncharged suspects, no voice replicas, trademark clearance |
| Columbia Daily, LA Daily (then NYC, Chicago) | Close paraphrase of local outlets; blotter-style naming; misattribution | Medium | Multi-source synthesis, credit and link, no minor-offense naming |
| All shows | Disclosure, music, voice rights, privacy, ad rules | Medium | Sections 6 to 8 |

*Where code lags policy today (legal exposure until built):* crime items inside the dailies run the **standard** lane, not strict (CR-NE-1); no deterministic text-overlap check (NE-10; the Originality Checker is status `next`); no sealed-record marker or protected-names list (CR-NE-5, -6); no per-episode suppress for takedowns (CR-NE-7). Details in [crime and courts rules](../standards/crime-and-courts-rules.md) §9 and [editorial standards](../standards/editorial-standards.md) §17.

## 2. Who is liable

- **We are the publisher and the speaker.** Section 230 protects hosting information provided by *another* party. Our pipeline writes and voices its own scripts, so we are the content provider (statute text, high confidence). No US appellate court has held that 230 covers a company's own generative-AI output. It may still help for listener comments or tips the site hosts unchanged, but rewriting a tip into a script is creating content **[LAWYER]**.
- **Repeating someone else's claim does not help.** A publisher who repeats a defamatory statement is generally liable as if it said it first, unless a privilege such as fair report applies. Summarizing another outlet's crime story in our voice is our publication.
- **Fault turns on our care.** A plaintiff will argue that publishing from a system known to make errors, with no person reading, is negligent (private figures) or reckless (public figures) *(inference)*. Our defense is documented care: verifier reports, fact-check ratings, source snapshots and gate decisions stored per episode. Those logs prove care and are also discoverable. Keep them at least 3 years (F-LEGAL-08).

## 3. Defamation and the fair report privilege

### 3.1 Fault, limits and local rules by state

*Recall, medium to low confidence. Public officials and public figures must prove actual malice; private figures need at least negligence, and most people named in court and crime coverage are private figures (F-LEGAL-09).*

| State (market) | Private-figure fault, public-concern speech | Anti-SLAPP | Time limit | Retraction law |
|---|---|---|---|---|
| **California** (LA) | Negligence | Strong, with fee shifting | 1 year | Civ. Code 48a: a correction within 3 weeks of a 20-day demand limits damages to proven losses. Whether it covers a podcast is unclear **[LAWYER]** |
| **New York** (NYC) | "Gross irresponsibility"; since 2020 anti-SLAPP changes, actual malice in public-interest suits | Broadened in 2020; limited in federal court | 1 year | None recalled |
| **Illinois** (Chicago) | Negligence | Narrow | 1 year | None recalled |
| **South Carolina** (Columbia) | Fault required; exact level unconfirmed | None recalled | 2 years | None recalled |

- **Re-releasing an archive episode can restart the clock** (F-LEGAL-08). Cold Case and History re-runs need a fresh legal pass.
- A podcast is heard everywhere, so a plaintiff can often sue at home and we lose friendlier-state protections. Do not rely on "neutral reportage" (repeating a serious charge from a responsible source while doubting it); few places recognize it.

### 3.2 What AI-defamation cases tell us

| Case | What happened | Lesson |
|---|---|---|
| *Walters v. OpenAI* | Summary judgment for OpenAI, 2025-05-19: one reader who knew the output was false, a public-figure plaintiff | Not protective for a podcast broadcast as fact to the public (F-LEGAL-11) |
| *Starbuck v. Meta* | AI falsely tied a person to a riot; settled Aug 2025 | AI makers settle rather than test the law; loud plaintiffs get leverage |
| *Wolf River Electric v. Google* | An AI summary falsely said a state AG sued a contractor; large lost-business claim (status unknown) | Businesses named in automated summaries sue and can show losses |
| *Battle v. Microsoft* | Search mixed up two people with similar names | Same-name confusion is the classic automated error: match identity before naming |

### 3.3 Fair report privilege by state

A fair and accurate report of an official proceeding or record is privileged even if the allegation is false. It is lost when we add outside matter, drop the attribution or abridge unfairly.

| State | Source | Scope and limits (recall) | Confidence |
|---|---|---|---|
| **California** | Civ. Code 47(d), statutory, treated as absolute | Fair and true report to a "public journal" of judicial, legislative or other official proceedings; applied to broadcast and online. Exceptions in 47(d)(2) (court orders, confidentiality). Lawyers' press conferences outside court generally not covered; police releases depend on the facts | medium-high |
| **New York** | Civil Rights Law 74, statutory, absolute | Fair and true means substantially accurate. No protection for added matter. Sealed or confidential proceedings are risky | medium-high |
| **Illinois** | Common law; *Solaia* (2006) adopted Restatement 611 | Accurate and complete, or a fair abridgment. Lost by omitting a dismissal or acquittal that was in the record | medium |
| **South Carolina** | Common law (Restatement approach); no statute recalled | Cites and whether it is absolute or qualified are unconfirmed **[LAWYER]**. Family court and juvenile matters are not public | low-medium |

**How the rules in our standards keep us inside it** *(inference, from F-LEGAL-10)*:

| Drafting rule | Where it lives |
|---|---|
| Name the official source of every allegation in the same sentence; never state an allegation as fact | CR-5, gate `L1`, `F1` |
| Use the record's legal word for the stage, never higher, and the status as of air time | CR-1 to CR-3, gate `F1`, `F2` |
| Add nothing outside the record: no motive, color or adjectives | gate `B2` (bias checker) |
| Be fair as a whole: report the plea or response, and always report a dismissal or acquittal | CR-7, follow-up within 72 hours |
| Only official records qualify: not tweets, neighbors, crowdfunding pages or out-of-court press conferences | CR-6, gate `V4`, NEVER-6 |
| Never use sealed, juvenile, family, expunged or confidential records; match same-name people on more than a name | CR-3, CR-NE-5 (not yet in code) |
| Snapshot every source with URL, hash and time in the trust log | trust log |

### 3.4 Other claims in the same lanes

- **Truthful public-record facts are strongly protected** (*Cox*, *Florida Star*; California's *Gates* even covers decades-old crimes), which helps Cold Case Files. That is a legal floor: our no-minors and no-victims rules go further on purpose.
- **False light** (CA and IL recognize it, NY does not; SC unconfirmed) comes from dramatization. Rule: **no invented quotes or dialogue attributed to real people**, even in archive shows.
- **Corrections help in court and with listeners:** a prompt, prominent, dated correction reduces damages and undercuts malice claims *(inference)*. See the [corrections policy](../standards/corrections-policy.md). Add a legal-notice mailbox and a postal address.

## 4. Copyright and news summarization

| Topic | Rule or case (recall) | What we do |
|---|---|---|
| Facts vs. wording | Facts are free (*Feist*, 1991); close paraphrase of structure and phrasing can infringe | Facts in our own words from two or more sources (COPY-1) |
| Hot news | *INS v. AP* survives narrowly, mostly NY; later cases limit it. Low risk, not zero for turning one outlet's scoops into rival audio within minutes | Credit "first reported by" and link (COPY-3, -4) |
| Quotes | Short attributed quotes are classic fair use; long reads are not | Never read articles aloud, paywalled or not (NEVER-5) |
| Publishers vs. AI firms | *Dow Jones v. Perplexity* (dismissal denied, Aug 2025) is the closest analog to a news-summary product; *NYT v. OpenAI* and a publishers' suit against Cohere add false-attribution theories; *Bartz v. Anthropic* settled for about $1.5B over pirated books (F-LEGAL-12). The Bartz and Kadrey rulings concern *training*, which we do not do | Our exposure is in outputs and how we collect text: no pirated or paywall-bypassed copies (COPY-2, -8), and never attribute text to an outlet unless the verifier matched it |
| Reuse licences | States Newsroom (SC Daily Gazette) is recalled as CC BY-NC-ND; Wikipedia is CC BY-SA (F-DATA-11) | Facts in our words plus a link; leads only; never adapt CC-ND text |
| Our own output | AI-only output is not protectable (*Thaler*, 2025-03-18; F-LEGAL-12), so others may copy it | Protect the brand with trademarks. Make theme music, art and policies human-authored or commissioned |
| Licensing | Paid licenses or partnerships with AP, regional dailies and local outlets lower copyright and hot-news risk and answer the free-rider charge *(inference)* | As revenue allows |
| Government and court material | Federal works are public domain; state and local vary; court opinions are not copyrightable. Courtroom recording needs the court's permission | Check each court's rules before using its audio; a TV station's footage is the station's |

## 5. Music licensing

*As of Oct 2026 — verify before buying. Prices are recall, low confidence (F-LEGAL-06).*

| Option | Notes | Cost |
|---|---|---|
| Commercial songs | Need separate licenses for the composition and the recording. Radio blanket licenses (ASCAP, BMI) do not cover downloadable podcasts. **Do not use** | n/a |
| Production-music library | Pick a **business** tier; personal or creator tiers often exclude company brands. A multi-show network may need an enterprise quote. Keep a license log per track and episode; whitelist YouTube channels to avoid Content ID claims | $15 to $50 a month |
| Commissioned theme and stems | Human composer, work-for-hire or buyout. Also gives a copyrightable brand asset | $500 to $5,000 once *(inference)* |
| AI-generated music | Label settlements reshaped the field in 2025 and terms keep moving. Use only with a written commercial license; expect such tracks to be uncopyrightable | Check terms |

At launch: one business-tier library license plus a commissioned sonic logo *(inference)*. Spoken clips of third-party audio need a license (COPY-6).

## 6. AI disclosure: laws and platform rules

*As of Oct 2026 — verify before relying. The [AI disclosure standard](../standards/ai-disclosure.md) holds the exact scripts; the Compliance and Platform Policy Watch agent re-checks quarterly.*

| Law | Reaches us? | What we do |
|---|---|---|
| **EU AI Act, Art. 50** (from 2026-08-02; fines up to EUR 15M or 3% of turnover) | Yes, if output is used in the EU. A fully automated pipeline cannot use the human-editorial exception *(inference)* | Spoken plus metadata disclosure meets it in substance. Geo-limit the EU or get counsel sign-off. Code of practice and "Digital Omnibus" status unverified |
| **California SB 942**, delayed by AB 853 to 2026-08-02 ($5,000 per violation per day) | Binds AI vendors with 1M+ monthly users, not us (F-LEGAL-13) | Never strip provenance marks or watermarks; expect platforms to auto-label synthetic audio from 2027 (low-medium) |
| **California bot law** (B&P 17940 ff.) | Social and community agents | They identify as automated |
| **FTC** Endorsement Guides, fake-review rule, impersonation rule; about $53,088 per violation (F-LEGAL-14) | Yes, for sponsors and show names | Ad rules below the tables |
| **State election deepfake laws** | About half the states | Never synthesize a candidate's or official's voice; describe what was said |
| **New York synthetic-performer ad disclosure** | Reported, date unverified (low) | Our sponsor read carries a "synthetic voice" tag as a precaution **[LAWYER]** |

| Platform | Rule | Our posture |
|---|---|---|
| **Apple Podcasts** | Prominent AI disclosure in the content and in show and episode metadata; enforcement not evident (F-HOST-15). Whether an end-of-episode line counts as "prominent" is unknown | Spoken end line plus first-line description text (gap G-2: move it to the front) |
| **Spotify** | No blanket AI ban; no podcast AI-label rule reported; Verified badges and removal of impersonating shows since 2026-05-19 (F-HOST-16) | Original voices, so impersonation rules do not touch us; same disclosure text |
| **YouTube** | Synthetic-content toggle since 2024-03-18, shown more prominently on news; July 2025 rule demonetizes mass-produced, repetitive channels (F-HOST-13) | Toggle **Yes on every upload**. A label does not protect a repetitive channel |
| **iHeart, discovery apps** | "Guaranteed Human" pledge on iHeart's own output (F-HOST-17); Castro, Podcast Index and Listen Notes filter AI feeds (F-HOST-18) | Few feeds, honest titles, full disclosure; get each host's AI-content position in writing before paying |

**Ad rules.** Sponsors are spoken aloud and ads stay out of stories (COI-1, -2). An AI host never claims personal experience (COI-3). No fake testimonials. Do not name or style a show to imply it comes from a court, police agency or news outlet. No sponsored news segments and no political ads at launch. Insertion orders carry an AI-voiced-read clause.

## 7. Voice and likeness rights

| Topic | Rule (recall, medium) | What we do |
|---|---|---|
| Voice of real people | Tennessee ELVIS Act (2024-07-01); California AB 1836 and AB 2602 (2025-01-01); California post-mortem right 70 years (F-LEGAL-16); NY and IL have digital-replica rules (low); SC none recalled | **Never clone, imitate or "sound like" a real person.** No dead stars' voices on History of Hollywood. Paraphrase officials; use real audio only if licensed |
| Our personas | Original voices from ElevenLabs Voice Design, controlled by the LLC | Keep a register: design prompt, date, env var, resemblance check ([voice guide](../standards/voice-and-persona-guide.md) §6). No human backstory or fake credentials |
| Vendor license | Free plan has **no commercial license** (F-TTS-01); Starter and above do (F-TTS-02). Library voices belong to real people who can withdraw them | Paid plan only; avoid Library voices. Ask sales if the API carries the same commercial rights (conflict C1) |
| Human voice actors, if ever | AB 2602 voids vague replica clauses | Written AI-replica agreement naming each use, paid for scope and term **[LAWYER]** |

## 8. Privacy and email

| Item | Rule (recall) | What we do |
|---|---|---|
| **CalOPPA** | Any commercial site collecting personal data from Californians needs a privacy policy (F-LEGAL-15) | Publish on day one |
| **CCPA/CPRA** | $26,625,000 revenue, or 100,000+ California consumers or households, or half of revenue from selling or sharing data. The 100,000 test is the realistic trigger, because ad insertion "shares" IP addresses and device IDs | Track California reach; add "Do Not Sell or Share", Global Privacy Control and request handling **before** 100,000 |
| **Tracking pixels** | California wiretap-law class actions target pixels and session replay | Minimal trackers; consent banner |
| **CAN-SPAM** | Accurate headers, postal address, opt-out honored within 10 business days (F-LEGAL-14) | Plus SPF, DKIM, DMARC and one-click unsubscribe |
| **BIPA** (Illinois) | Voiceprints are biometric: $1,000 or $5,000 per violation | No speaker ID or cloning on listener voicemails; store audio and transcripts with a retention limit |
| **COPPA, GDPR, other states** | Keep the network general-audience. GDPR if we target EU listeners. About 20 states have privacy laws; SC, IL and NY have none comprehensive (recall) | Minimal analytics; hosts with data-processing terms |

## 9. Insurance

*As of Oct 2026 — verify before buying. All figures are recall or inference (F-LEGAL-01). Get written broker quotes.*

| Item | Figure |
|---|---|
| Planning placeholder | **$6,000 a year ($500 a month)** for $1M media liability with a $10,000 retention. The cost model's $78 a month is not supported by the research notes; use $500 from the test stage |
| Small podcast policy | About $500 to $2,500 a year |
| Small news publisher | About $2,500 to $10,000+ a year; retention $2,500 to $25,000 |
| Our case | Automated court and crime content may be priced up, restricted or declined. Some carriers ask about pre-publication legal review |

- Covers defamation, privacy, copyright and trademark claims **and defense costs**, which are the main value: a baseless libel suit can cost tens of thousands to dismiss *(inference)*.
- **Ask every carrier about generative-AI exclusions.** Describe the automated pipeline accurately on the application: a misstatement can void coverage.
- Look at specialist media brokers and carriers, and news-association programs (LION Publishers, INN) if a for-profit LLC qualifies. Use trust-log numbers (corrections per 100 episodes, holds, kills) at renewal.

## 10. Business setup

*As of Oct 2026 — verify before paying. Fees are recall, low confidence.*

| Item | What to do | Cost / timing |
|---|---|---|
| **LLC state and tax** | State of formation is unknown. If the founders work from California, the LLC is likely doing business there: **$800 a year minimum franchise tax**, an extra fee above $250,000 in receipts, and foreign registration if formed elsewhere (F-LEGAL-05) **[CPA]** | $800 a year; confirm in the first 60 days |
| **Beneficial ownership report** | US-formed LLCs exempt since March 2025 (F-LEGAL-17); confirm | none |
| **Operating agreement and IP** | Founders and every contractor assign all IP to the LLC (code, prompts, personas, formats, brand). Set who can pull an episode on a legal threat **[LAWYER]** | in the lawyer review |
| **DBA** "Curious & Creative Network" | **CA:** fictitious name statement with the county clerk within 40 days of first use, 4 weeks of newspaper publication, valid 5 years. **SC:** no statewide DBA; a city or county business license may apply. **NY** (later): certificate of assumed name. **IL** (later): assumed name application (F-LEGAL-04) | CA about $26 plus $30 to $150 publication; NY about $25 plus county; IL up to about $150 |
| **Trademark** | File the network name in **Class 41** (intent-to-use) first, then **Class 9**; skip 38; add 35 for ad sales or services later. Use pre-approved wording to avoid surcharges | $350 per class (F-LEGAL-03); Statement of Use $150; renewals $325; attorney clearance $500 to $2,000 per mark |
| **Name clearance** | "Curious" is crowded; *Cold Case Files* is an A&E title; *Columbia Daily* and *LA Daily* echo papers; check *Breaking Desk* and *Case Tracker* and every persona name | before launch |
| **Bank, books, tax** | Business account and card in the LLC's name; free EIN; never mix personal money (it weakens the liability shield). Track revenue and cost by show. Sales tax on subscriptions and 1099 rules **[CPA]** | bookkeeping about $30 a month (F-INFRA-04) |
| **Domains and mail** | Network and show domains, privacy and lock; `legal@` and `corrections@` mailboxes; SPF, DKIM, DMARC | $10 to $25 per domain a year |
| **Day-one pages** | Terms of Use (with a license for listener submissions), Privacy Policy, Corrections and Ethics, "How this show is made", legal contact with postal address; transcripts for accessibility | in the lawyer review |
| **DMCA agent** | Register if the site hosts any user content | $6 per 3 years (F-LEGAL-07) |
| **Records** | Keep scripts, source packs, trust logs 3+ years; freeze deletion for any episode under a legal threat | F-LEGAL-08 |

## 11. Founder checklist

| When | Do this | Who |
|---|---|---|
| **P0: before any episode auto-publishes** | (1) Media-lawyer setup review, flat fee $2,500 to $7,500. (2) Bind E&O insurance with no AI exclusion. (3) Keep naming in court, crime and Breaking Desk stories under strict rules, with a recorded human sign-off, until (1) and (2) are done and 30 days of trust-log data look clean. The sign-off is an extra input, never an override of the gate (NEVER-10); the legal note recommends it, it is a founders' call and interacts with the no-human design *(inference)*. (4) Gate rules from section 3.3 switched on. (5) Disclosure everywhere. (6) Original voices on a paid plan, with a register. (7) Licensed music plus a log. (8) Copyright hygiene. (9) Privacy, Terms, Corrections and legal contact live. (10) Name clearance | Joshua, Janel, **[LAWYER]** |
| **P1: first 30 to 60 days** | DBA; confirm LLC state and California status; file trademarks; domains and mail; bank and books; IP assignment and operating agreement; sponsor rules; DMCA agent | **[CPA]**, **[LAWYER]** |
| **P2: before NYC, Chicago, EU or real monetization** | NY and IL review (CRL 74, 76-a, *Solaia*, BIPA); EU wording and GDPR or geo-limit; CCPA readiness; licensing deals with local outlets and AP; copyright registration for human-authored assets | **[LAWYER]** |
| **P3: ongoing** | Quarterly legal watch (AI-defamation cases, SB 942 and AB 853, the federal order on state AI laws, NO FAKES, platform rules); annual insurance renewal; annual Terms and Privacy refresh; retention and litigation-hold drill | Compliance agent, Contracts and IP Clerk |

## 12. What needs a media lawyer

1. South Carolina fair report: cites, absolute or qualified, and whether police statements and releases count as official proceedings in all four states.
2. Whether California's retraction statute covers a podcast network.
3. How a fully automated publisher's care will be judged, and how to design and retain the trust log, given it is discoverable.
4. Arbitration and class-waiver clauses in the Terms; voice-actor or likeness deals; any use of real public figures' audio.
5. Trademark clearance for the network and show names; the insurance application wording.
6. EU distribution (AI Act, GDPR) and election-season deepfake laws.
7. **Any demand letter, subpoena or takedown.** Escalate to a human within 1 hour. For minors, sexual-assault victims or a credible legal threat, suppress first and review after ([takedown rules](../standards/crime-and-courts-rules.md) §7).

**Free or low-cost help to ask about** (eligibility for a for-profit LLC unchecked): the Reporters Committee legal hotline, Lawyers for Reporters, the First Amendment Coalition (California) and the Media Law Resource Center directory.

## 13. Open gaps

- Verify live: USPTO fees, SB 942 and AB 853 dates, EU Art. 50 status, Apple's exact wording, YouTube rules for synthetic narrators, LA County DBA fees, SC license duty.
- Unknown: 2026 outcomes in *Starbuck v. Google*, *Wolf River*, *Dow Jones v. Perplexity*, *NYT v. OpenAI*; any ruling against a *publisher* of AI-written news; SC fair-report and fault law; state AI-news disclosure bills; NY synthetic-performer date; real insurer quotes; AI-music terms.

## Sources

None opened in this pass; verify at the source. [Legal note](../research/notes/legal-compliance-business-setup.md) §15 lists each statute and case link. Policy basis: [crime and courts rules](../standards/crime-and-courts-rules.md), [AI disclosure](../standards/ai-disclosure.md), [editorial standards](../standards/editorial-standards.md), [corrections policy](../standards/corrections-policy.md). Platform text: [Apple guidelines](https://podcasters.apple.com/support/891-content-and-subscription-guidelines), [Variety on Spotify](https://variety.com/2026/digital/news/spotify-bans-ai-generated-podcasts-impersonate-verified-badges-1236752944/).
