# Legal, compliance and business setup for the Curious & Creative Network

*Research notes for Project Earlobe. Operator: Curious & Creative LLC (an existing US LLC). Compiled 2026-10-11.*

> **Not legal advice.** These are a research analyst's notes to help the founders brief counsel and set priorities. Every item marked **[LAWYER]** needs a licensed media lawyer, and every item marked **[CPA]** needs an accountant, before anyone relies on it.

## TL;DR

Curious & Creative LLC will be the **publisher** of every Earlobe episode, so it carries full defamation, privacy and copyright liability for what its AI writes and voices. Section 230 does not apply: Earlobe creates its own scripts, and the law protects only content provided by someone else. The highest-risk lanes are the court and crime trackers and Breaking Desk. Most people they name will be private figures, so in California and Illinois a plaintiff only needs to show **negligence** (New York and South Carolina differ; see §3.3). The main shield is the **fair report privilege**: a fair, accurate and attributed account of official records and proceedings. It is statutory in California (Civil Code §47(d)) and New York (Civil Rights Law §74) and comes from case law in Illinois and South Carolina. It only works if every allegation is tied to an official source and nothing is added. Copyright risk comes from what Earlobe outputs, not from model training: report facts in your own words from several sources, use short attributed quotes, and don't substitute for one outlet's article. Disclosure rules are converging, not conflicting. Apple wants prominent AI disclosure in the audio and in metadata. YouTube requires its synthetic-content toggle. Spotify removes impersonation. EU AI Act Art. 50 applies from 2026-08-02. California's SB 942 (delayed by AB 853 to 2026-08-02) mainly binds the voice vendor, not Earlobe. Earlobe already plans a spoken disclosure in every episode, which covers most of this. On voices, use only original synthetic voices or voices licensed with explicit written AI consent. Never clone a real person: Tennessee's ELVIS Act, California's digital-replica laws and Spotify's impersonation ban all point the same way. Business setup is cheap: a California fictitious business name statement (county fee plus four weeks of newspaper publication); South Carolina has no statewide DBA, though local business licenses may apply; USPTO filing at $350 per class (start with Class 41, then 9); a separate bank account; bookkeeping tracked by show. **The two P0 items that cost real money are media liability (E&O) insurance and a one-time media-lawyer setup review.** Both should be in place before any court or crime episode auto-publishes.

**Evidence status (read this first).** This pass could not collect live web evidence. The shared web-search budget for this run was used up before the first query, and every direct fetch of a primary source failed at DNS (leginfo.legislature.ca.gov, uspto.gov, podcasters.apple.com, support.google.com, artificialintelligenceact.eu, scstatehouse.gov). Each domain was tried once and not retried. The content below comes from background knowledge as of mid-2026, plus facts already sourced in sibling notes (Spotify's 2026-05-19 policy, Apple's guideline link, ElevenLabs plan rights). Confidence is capped accordingly:
- **high:** only for settled landmark law (statute text, Supreme Court holdings) and facts sourced in sibling notes;
- **medium:** dated facts I recall well;
- **low:** fees, prices and 2025-2026 case status.

Every number should be verified on a follow-up pass with search budget. The list is in "Open questions / gaps".

---

## 1. Risk map at a glance

| Lane / show | Main legal exposure | Severity | Primary mitigations |
|---|---|---|---|
| Court & true-crime trackers (Case Tracker, Court Watch) | Defamation (accusing a crime is libel per se), wrong-person errors, false light, sealed or juvenile records | **Highest** | Fair-report formatting; official-record-only naming; identity disambiguation; human sign-off at launch; E&O insurance |
| Breaking Desk (national) | Naming unconfirmed suspects or victims; speed errors; hot-news copying of one outlet's scoop | High | HOLD lane; two independent sources; "first reported by" credit; no names until official |
| Local daily briefs (Columbia SC, LA, then NYC, Chicago) | Copying or close paraphrase of local outlets; blotter-style naming; misattribution | Medium | Multi-source synthesis; originality checker; no minor-offense naming |
| Cold Case Files / History of Hollywood (archive) | Defamation of living people (suspects, investigators, relatives); private facts about rehabilitated people; dramatized quotes; post-mortem publicity rights for voice or likeness; name collision with A&E's *Cold Case Files* | Medium-high | No invented dialogue; living-person check; no celebrity voice replicas; trademark clearance |
| All shows | AI disclosure (platforms, EU), voice rights, music licensing, privacy on site and newsletter, ad disclosure | Medium | Spoken and metadata disclosure; original voices; business-tier music license; privacy and terms pages |

*(inference, built on the sections below)*

---

## 2. Who is liable: publisher status and Section 230

- **Earlobe is the publisher and the speaker.** Section 230(c)(1) stops a provider or user of an interactive computer service from being treated as the publisher of information provided by *another* information content provider. Under §230(f)(3), anyone "responsible, in whole or in part" for creating or developing content is its information content provider. Earlobe's pipeline writes and voices its own scripts, so it is the content provider and gets no §230 immunity for its episodes. *(official; high on statute text, recall; not re-read this session)*
- **Repeating a third party does not help either.** Under the common-law republication rule, a publisher who repeats a defamatory statement is generally liable as if it said it first. The exception is a recognized privilege, such as fair report. Summarizing another outlet's crime story in our own voice is our publication. *(official/common law; high on the doctrine)*
- **Where §230 may still help:** listener comments, community posts or user tips that the website hosts *unchanged*. The California Supreme Court's *Barrett v. Rosenthal* (2006) even protected individual users who reposted others' content online. But a podcast that rewrites tips into a script is creating content, not hosting it. *(official; medium; [LAWYER] before relying on it)*
- **Courts and lawmakers on generative AI:** no US appellate court has held that §230 covers a company's own generative-AI output. The prevailing view among commentators, and the drift of 2023-2025 bills such as the proposed "No Section 230 Immunity for AI Act", is that it does not. In the *Character.AI* wrongful-death case (M.D. Fla., May 2025) the judge declined, at the motion-to-dismiss stage, to treat chatbot output as protected speech. That was not a defamation ruling, but it shows courts are cautious. *(reported; medium)*
- **Who "knew" what (inference; [LAWYER]).** Fault standards ask about the *publisher's* state of mind or care. With no human in the loop, a plaintiff will argue that publishing from a system *known to hallucinate*, without human review, is (a) negligent, for a private figure, or (b) reckless disregard or purposeful avoidance of the truth (*Harte-Hanks v. Connaughton*, 1989), for a public figure. Earlobe's defense is the documented care in the Trust Stack: verifier and fact-check reports, source snapshots and gate decisions stored per episode. Keep those logs. They are the evidence of reasonable care, and they will also be discoverable.

## 3. Defamation

### 3.1 AI-defamation cases, 2023 to 2026 (recall; status after mid-2026 unverified)

| Case | What happened | Status (as recalled) | Lesson for Earlobe |
|---|---|---|---|
| *Walters v. OpenAI* (Gwinnett County Superior Court, Georgia; filed June 2023) | ChatGPT told a journalist that radio host Mark Walters had embezzled from a gun-rights group. Only that journalist saw the output. | **Summary judgment for OpenAI, 2025-05-19.** Grounds: the one reader did not believe it (he knew it was false, and there were disclaimers); no fault was shown under the applicable standard (the court treated Walters as a public figure); no damages proven. | That defense depended on a single private reader who knew better. A news podcast broadcast as fact to the public would lose the "no reasonable reader" argument. Treat *Walters* as **not** protective for Earlobe. *(reported; medium)* |
| *Starbuck v. Meta* (Delaware Superior Court; filed April 2025) | Meta AI falsely linked activist Robby Starbuck to the Jan. 6 riot. | **Settled Aug 2025.** Starbuck reportedly became an adviser to Meta on AI bias. | AI makers settle rather than test the law. A plaintiff who complains loudly gets leverage. *(reported; medium)* |
| *Starbuck v. Google* (Delaware; filed Oct 2025) | Claimed Google AI tools invented sexual-misconduct and criminal allegations; about $15M sought. | Pending as of last recall. | Fabricated criminal allegations are the core risk pattern. *(reported; low-medium)* |
| *Wolf River Electric v. Google* (Minnesota; filed mid-2025) | An AI Overview falsely said the state AG had sued a solar contractor; the company claimed lost contracts (more than $100M in alleged damages, as reported). | Reportedly moved to federal court; status unknown. | Businesses named in automated summaries sue too, and can show concrete lost business. *(reported; low-medium)* |
| *Battle v. Microsoft* (D. Md.; filed 2023) | Bing mixed up an aerospace educator with a convicted terrorist who had a similar name. | Sent to arbitration (2024, as recalled). | **Same-name confusion is the classic automated-news error.** Court and crime trackers must disambiguate identity. *(reported; low-medium)* |
| *Fanning v. Microsoft/MSN* (Ireland, 2024) | An automated MSN news aggregation ran a misconduct story with the wrong presenter's photo. | Proceeded in Irish High Court, as recalled. | Automated aggregation of other outlets' stories can create **new** defamation. *(reported; low)* |
| Gemma / Sen. Blackburn complaint (Nov 2025) | A Google open model invented sexual-misconduct claims about a senator; Google pulled the model from its AI Studio. | Political, not litigation. | Fabrications about public officials draw fast regulatory and political pressure. *(reported; low-medium)* |

**Non-litigation incidents that matter for an automated news brand** (recalled; some are in sibling notes): Apple paused AI notification summaries for news in Jan 2025 after a false BBC-attributed headline. A syndicated insert in the Chicago Sun-Times and Philadelphia Inquirer (May 2025) recommended books that don't exist. Inception Point's templated city crime logs named people from blotters. *(reported; medium)*

### 3.2 Fault standards: public figures vs private figures

- **Public officials and public figures** must prove **actual malice**, meaning knowledge of falsity or reckless disregard, by clear and convincing evidence (*NYT v. Sullivan*, 1964; *Curtis Publishing v. Butts*, 1967). *(official; high)*
- **Private figures:** states may set their own standard but must require at least **negligence** (*Gertz v. Robert Welch*, 1974). Presumed or punitive damages still require actual malice when the speech is on a matter of public concern. On such matters, the private plaintiff carries the burden of proving falsity (*Philadelphia Newspapers v. Hepps*, 1986). *(official; high)*
- **Most people named in court and crime coverage are private figures**: defendants, victims, witnesses and small businesses. Being arrested does not make someone a public figure. So the standard Earlobe will usually face is the state's private-figure standard, shown below. *(official/inference; medium-high)*

| State (market) | Private-figure fault standard, matter of public concern | Notes |
|---|---|---|
| **California** (LA) | Negligence (*Brown v. Kelly Broadcasting*, Cal. 1989) | Strong anti-SLAPP law (Code Civ. Proc. §425.16) with attorney-fee shifting. A retraction statute (Civ. Code §48a) limits damages if a correction runs on time; whether it covers a podcast is uncertain **[LAWYER]**. *(official; medium)* |
| **New York** (NYC) | "Gross irresponsibility" (*Chapadeau v. Utica Observer-Dispatch*, 1975), which is more protective than negligence. The **2020 anti-SLAPP amendments** (Civ. Rights Law §76-a) require **actual malice** in suits over communications on issues of public interest, even by private figures, and §70-a allows fee recovery. | Federal courts in the 2nd Circuit have limited use of state anti-SLAPP procedure. *(official; medium)* |
| **Illinois** (Chicago) | Negligence (*Troman v. Wood*, Ill. 1975) | Illinois has the "innocent construction" rule. Its anti-SLAPP law (Citizen Participation Act) is narrow after *Sandholm v. Kuecker* (2012). *(official; medium)* |
| **South Carolina** (Columbia) | Plaintiff must prove fault and cannot rely on common-law presumptions of malice or damages on matters of public concern (as recalled from *Erickson v. Jones Street Publishers*, S.C. 2006). The exact fault level should be confirmed. | **No general anti-SLAPP statute recalled.** Slander/libel limitation period recalled as **2 years** (S.C. Code §15-3-550). *(official; low-medium; [LAWYER])* |

- **Statutes of limitation (recall):** California 1 year (CCP §340(c)), New York 1 year (CPLR §215(3)), Illinois 1 year (735 ILCS 5/13-201), South Carolina 2 years. The **single-publication rule** generally starts the clock at first publication. **Re-editing and re-releasing an archive episode can count as a republication and restart it.** That matters for Cold Case and History of Hollywood re-runs. *(official; medium)*
- **Jurisdiction:** a podcast is heard everywhere, so a plaintiff can usually sue where their reputation was harmed (*Keeton v. Hustler*, 1984; *Calder v. Jones*, 1984). That means facing the plaintiff's home-state law and losing the benefit of anti-SLAPP laws in friendlier states. Foreign judgments are limited by the federal SPEECH Act (2010). *(official; medium-high)*
- **"Neutral reportage"** (reporting serious charges by a responsible source even if you doubt them) is recognized only in a few places and is not settled in New York state courts. **Do not rely on it.** *(official; medium)*

### 3.3 The fair report privilege, Earlobe's main shield

**General rule.** A fair and accurate report of an official proceeding or record is privileged even if the underlying allegation turns out to be false. The report must be a substantially accurate summary of what the official record says, attributed to that record, with nothing defamatory added from outside it. *(official/common law; high on concept)*

| Jurisdiction | Source of the privilege | Scope (as recalled) | Key limits |
|---|---|---|---|
| **California** | **Civil Code §47(d)** (statutory; treated as **absolute**, with no malice exception) | A fair and true report "in, or a communication to, a public journal" of: a judicial, legislative or other public official proceeding; anything said in the course of one; or a verified charge or complaint made to a public official on which a warrant has issued. §47(e) separately covers fair reports of public meetings. Courts apply "public journal" to broadcast and online media. *(official; medium-high)* | §47(d)(2): no protection where the report breaks the trial-publicity rule of professional conduct, a court order, or a confidentiality requirement imposed by law. Lawyers' press-conference statements *outside* court are generally not covered (*Rothman v. Jackson*, 1996, as recalled). Whether police press releases count as "official proceedings" depends on the facts. *(medium)* |
| **New York** | **Civil Rights Law §74** (statutory; absolute) | No civil action for a "fair and true report" of any judicial, legislative or other official proceeding, or a fair headline of it. "Fair and true" means **substantially accurate** (*Holy Spirit Ass'n v. NY Times*, 1979). Some courts have applied it to official agency and police statements. *(official; medium-high)* | No protection for libel in *added* matter, or for things said at the proceeding that were not part of it. Sealed or confidential proceedings are risky. |
| **Illinois** | **Common law**; *Solaia Technology v. Specialty Publishing* (Ill. 2006) adopted Restatement (Second) of Torts §611 | Covers reports of official actions or proceedings, including a complaint once it is filed in court, if the report is accurate and complete or a fair abridgment. *(official; medium)* | Lost through inaccuracy or unfair abridgment, for example omitting a dismissal or an acquittal that was in the record. |
| **South Carolina** | **Common law**, recognized by SC courts (Restatement §611 approach). No codified statute recalled. | Fair and accurate reports of judicial and official proceedings. *(official; low-medium; [LAWYER] to confirm cites and whether it is qualified or absolute)* | Family court and juvenile matters are not public in SC (sibling notes). Expungement can remove records. |

**Drafting rules the Trust Stack should enforce for fair report** *(inference; aligns with existing legal-screener rule L1/L2)*:
1. **Attribute every allegation to a named official source in the same sentence.** For example: "according to a criminal complaint filed Tuesday in Richland County General Sessions court" or "LAPD said in a statement". Never state an allegation as fact.
2. **Use the record's words for the charge** ("charged with", "accused of", "arrested on suspicion of"). Never say or imply guilt before a conviction. Say when the person has pleaded not guilty, if the record shows it.
3. **Add nothing outside the record**: no color, no motive, no prior history from social media, no adjectives. Added material falls outside the privilege.
4. **Be fair as a whole.** Include the defense's response or plea when the record has it, and **always report a dismissal, acquittal or reversal the system finds** (the recheck monitor). Leaving out a known exculpatory outcome risks being an unfair abridgment.
5. **Only official records and proceedings qualify.** A tweet, a neighbor, a victim's GoFundMe or a lawyer's press conference outside court is *not* covered. Those claims need independent verification or must be left out.
6. **Sealed, juvenile, family-court and confidential records:** never use them. The intake drop rule is already in the repo.
7. **Identity disambiguation:** match the person by full name plus age or date of birth, city, or case number before naming. If there is any doubt, don't name.
8. **Snapshot the source document**, with URL, hash and timestamp, in the trust log for every named person.

### 3.4 Other torts in the same lanes

- **Truthful public-record facts are strongly protected.** *Cox Broadcasting v. Cohn* (1975), *Smith v. Daily Mail* (1979) and *Florida Star v. B.J.F.* (1989) protect truthful publication of lawfully obtained information on matters of public significance. That is a legal floor, not an ethics standard. Earlobe's no-victims and no-minors rules go further on purpose. *(official; high)*
- **Cold cases and rehabilitation.** In California, *Gates v. Discovery Communications* (Cal. 2004) held that truthful reports of facts from public court records about a decades-old crime are not actionable as private-facts invasion, in effect limiting the older *Briscoe v. Reader's Digest* (1971). This is helpful for Cold Case Files, but it protects only accurate public-record facts. *(official; medium)*
- **False light** is recognized in California and Illinois but **not in New York**. The South Carolina position should be confirmed. Risk comes from **dramatization, invented dialogue and composite scenes**. Rule: **no invented quotes or reconstructed dialogue attributed to real people**, even in archive shows. *(official; medium)*
- **Misappropriation / right of publicity:** see §7. News and public-affairs uses are generally exempt, but **voice replicas are not**.
- **Libel per se.** Saying someone committed a crime, has a loathsome disease, is professionally incompetent, or (in some states) engaged in sexual misconduct is per se. Damages can be presumed in some cases, so most court and crime errors land here. *(official; high on concept)*

### 3.5 Corrections and retraction

- **California Civ. Code §48a (recall):** for a daily or weekly news publication or broadcast, a plaintiff who doesn't serve a correction demand within **20 days** of learning of the publication, or who gets a correction within **3 weeks** of the demand that is substantially as conspicuous, is limited to special (proven economic) damages. Whether a podcast or network counts as a covered publication is **[LAWYER]**. *(official; medium on the mechanism, low on coverage of podcasts)*
- New York, Illinois and South Carolina: **no general media retraction statute recalled**; verify. A prompt, prominent correction still reduces damages, undercuts claims of malice or negligence, and often ends disputes. *(inference; medium)*
- **Corrections policy contents** (recommended): how to report an error; response targets (acknowledge within 24 h; decide within 72 h; spoken correction in the next episode of the same show; feed and show notes updated within 1 h of a decision, as in the repo's corrections-agent KPI); correction categories (note, reissue, retract, already in the editorial standards); a **legal-notice contact** (email plus postal address of the LLC); and an **update or unpublishing policy** for named arrestees whose cases end in dismissal or acquittal. *(inference)*

---

## 4. Copyright and news summarization

### 4.1 Doctrine

- **Facts are not copyrightable; expression is** (*Feist v. Rural Telephone*, 1991). Reporting who, what, when and where in our own words is lawful. Close paraphrase that tracks an article's structure, sequence and distinctive phrasing can still infringe. *(official; high)*
- **"Hot news" misappropriation** comes from *INS v. AP* (1918). It survives only narrowly as state law, mainly New York. *NBA v. Motorola* (2d Cir. 1997) limited it to time-sensitive information gathered at cost, where the defendant free-rides in direct competition and threatens the plaintiff's incentive to gather the news. *Barclays Capital v. Theflyonthewall.com* (2d Cir. 2011) held a claim pre-empted where the defendant reported the news under its own name, attributing the source. **Practical risk is low but not zero** for a network that systematically turns one local outlet's fresh scoops into competing audio within minutes. *(official; medium-high)*
- **Fair use for quotes:** short, attributed quotes for news reporting are classic fair use. Long reads of another outlet's copy are not. The repo's originality-checker (12-word unquoted-run limit) enforces this mechanically. *(official/inference; medium-high)*

### 4.2 News publishers vs AI companies (recall; 2026 status unverified)

| Case | Core claim | Status as recalled | Implication |
|---|---|---|---|
| *NYT v. Microsoft & OpenAI* (S.D.N.Y., filed 2023-12-27), now part of a consolidated OpenAI copyright MDL in S.D.N.Y. | Training on, and outputs that reproduce, Times articles | Motion to dismiss largely **denied** (spring 2025); discovery, including a fight over preserving ChatGPT logs. Daily News and other Alden papers joined. | Courts treat **outputs that regurgitate or substitute** for articles as a live theory. *(reported; medium)* |
| *Dow Jones & NY Post v. Perplexity* (S.D.N.Y., filed Oct 2024) | An answer engine copying and summarizing articles, plus false attribution | Motion to dismiss or transfer **denied** (Aug 2025, as recalled). Other publishers (Britannica/Merriam-Webster, then reportedly NYT and the Chicago Tribune in late 2025) also sued Perplexity. | **Closest analog to Earlobe**: a product that summarizes current news. Substitutive summaries plus **misattributing invented text to a real outlet** are the theories at stake. *(reported; medium-low)* |
| *Advance Local et al. v. Cohere* (S.D.N.Y., Feb 2025; 14 publishers) | Copyright, plus **Lanham Act** claims for hallucinated articles attributed to the publishers | Motion to dismiss largely denied (late 2025, as recalled). | **Never attribute something to an outlet unless the verifier matched it**; misattribution is a trademark issue too. *(reported; low-medium)* |
| *Thomson Reuters v. Ross Intelligence* (D. Del., 2025-02-11) | Copying Westlaw headnotes to build a competing (non-generative) AI tool | **Not fair use** (partial summary judgment). An interlocutory appeal to the 3rd Circuit was accepted; outcome unknown. | Copying to build a **directly competing** product weighs against fair use. *(official; medium)* |
| *Bartz v. Anthropic* (N.D. Cal., June 2025) / *Kadrey v. Meta* (N.D. Cal., June 2025) | Training on books | Training on lawfully acquired books was ruled fair use (Bartz); pirated library copies were not, followed by a reported **$1.5B class settlement** (Sept 2025). *Kadrey*: fair use on that record, but the judge flagged "market dilution". | These cases are about **training**. Earlobe doesn't train models; its exposure is in its **outputs** and in **how it collects source text** (no pirated or paywall-bypassed copies). *(reported; medium)* |
| Licensing trend | AP, Axel Springer, News Corp, FT, Amazon-NYT and others licensed content to AI firms (2023-2025) | Ongoing | A market for licensed news inputs exists. Licensing local outlets or AP is a real option and answers the "free rider" critique. *(reported; medium)* |

**What this means for Earlobe** *(inference)*:
1. Build every script from **two or more sources** where possible. Report facts, not prose. Credit "first reported by X" for scoops, and link sources in show notes.
2. **Do not ingest full text from behind paywalls or against site terms.** Respect robots.txt and publisher AI opt-outs as a good-faith posture. Under *Van Buren* (2021) and *hiQ v. LinkedIn* (9th Cir. 2022), scraping public pages is unlikely to violate the CFAA, but breach-of-terms claims remain possible.
3. **Citations must be verified**: the verifier must confirm that the cited outlet actually said it (Cohere/Perplexity misattribution theory).
4. **Creative Commons news** (for example States Newsroom's SC Daily Gazette, recalled as CC BY-NC-ND per the markets note) does **not** allow commercial derivative use. Summarize facts and link; don't adapt the text.
5. Consider paid licensing (AP local, regional dailies) when revenue allows.

### 4.3 Earlobe's own outputs may not be copyrightable

- The US Copyright Office's AI report Part 2 (Jan 2025) and *Thaler v. Perlmutter* (D.C. Cir., 2025-03-18) confirm that **material generated by AI without enough human authorship is not protected**. Registration applications must disclose and disclaim AI-generated material (USCO guidance, March 2023). *(official; medium-high; the outcome of any Supreme Court cert petition in Thaler is unverified)*
- **Implication** *(inference)*: fully automated scripts and audio may be freely copyable by others. Protect the **brand** with trademarks. Make **theme music, artwork and written policies** human-authored or commissioned, which are copyrightable assets. Rely on platform terms and DMCA takedowns of *re-uploads*, but expect weak claims on purely AI parts.

### 4.4 Court audio, government material and clips *(recall; verify per source)*

- Federal government works are public domain. **State and local government works are not automatically public domain**; it varies by state. Court opinions and statutes are not copyrightable (*Georgia v. Public.Resource.Org*, 2020, the government-edicts doctrine). Private lawyers' filings are technically copyrighted, but quoting them in news is fair use. *(official; medium)*
- **Courtroom recording and rebroadcast:** federal courts generally bar broadcast; California Rules of Court 1.150 needs a judge's permission to record. Some courts livestream with terms that forbid rebroadcast. **Check each court's rules before using its audio.** A local TV station's footage of a press conference belongs to the station. *(official; medium-low)*

## 5. Music beds

- **Two rights in every recording**: the musical work (composition) and the sound recording (master). ASCAP, BMI, SESAC and GMR blanket licenses cover *public performance* for broadcasters and venues. They do **not** cover the reproduction and sync rights that downloadable podcasts need. **Commercial music in a podcast needs direct licenses from both owners**, which is impractical, so don't use it. *(official/industry; medium-high)*
- **Practical options** *(prices recalled; low confidence; verify)*:
  - **Production-music subscriptions** (Epidemic Sound, Artlist, Musicbed, Soundstripe, Audio Network). **Pick a business or commercial tier**: "personal" or "creator" plans are usually limited to an individual's own channels and exclude company brands. Rough range: **$15 to $50 a month** for small-business tiers; multi-show networks and broadcast use usually need an **enterprise quote**. Whitelist YouTube channels to avoid Content ID claims. Keep a license log per track and episode. *(reported; low)*
  - **Commissioned network theme and stems** from a human composer, as a work-for-hire or buyout. Rough one-time range **$500 to $5,000** *(inference; low)*. It also gives a **copyrightable** brand asset (see §4.3).
  - **AI music.** Label litigation reshaped the field in 2025: UMG settled with Udio (Oct 2025) and Udio moved to a walled-garden model with downloads restricted; WMG settled with Suno (Nov 2025) and Suno announced licensed models for 2026. ElevenLabs launched **Eleven Music** (Aug 2025), citing publisher and indie-label licensing deals for commercial use on paid plans. Terms are shifting; **use only with a written commercial license, and expect AI-generated tracks to be uncopyrightable** (others could reuse them). *(reported; low-medium)*
- **Recommendation** *(inference)*: at launch, use one business-tier library license plus a commissioned network sonic logo. Add AI music only after its terms are confirmed in writing.

---

## 6. AI disclosure laws

### 6.1 California AI Transparency Act (SB 942, 2024), as amended by AB 853 (2025)

- **Who it binds:** "covered providers", meaning companies that create a generative-AI system publicly accessible in California with **more than 1,000,000 monthly visitors or users**. They must: offer a free AI-detection tool; embed **latent disclosures** (provenance metadata or watermark) in AI-generated image, video and audio; offer users an option for a **manifest** (visible or audible) disclosure; and **revoke the license** of a third-party licensee who modifies the system to strip disclosures. Penalty: **$5,000 per violation**, with each day counting separately; enforced by the AG and local prosecutors. *(official; medium)*
- **Timing:** originally operative **2026-01-01**; **AB 853 (signed Oct 2025) delayed it to 2026-08-02**. AB 853 also added duties for **large online platforms** to detect and surface provenance data (from **2027-01-01**) and for capture-device makers (from **2028**). *(official; medium; verify exact dates)*
- **Application to Earlobe** *(inference)*: Earlobe is **not** a covered provider. ElevenLabs (the voice vendor) and possibly the LLM vendors are. Earlobe's duties are indirect: **don't strip or alter provenance metadata or watermarks** from vendor output, and expect platforms such as Spotify and YouTube to **auto-label** synthetic audio from 2027. The federal executive order of Dec 2025 targeting "onerous" state AI laws (it set up a DOJ AI litigation task force) could bring challenges, but it doesn't repeal state law by itself. *(reported; medium-low)*
- **Related California laws** *(official; medium)*:
  - **B&P Code §17940-17943** (2019 bot law): it is unlawful to use a bot to communicate with Californians online to mislead them about its artificial identity in order to drive a sale or influence a vote. **The community-manager and social agents must identify as automated.**
  - The 2024 election-deepfake laws AB 2839 and AB 2655 were struck down or enjoined in federal court (2024-2025). AB 2355 requires AI disclosure in political ads.
  - Roughly half the states now regulate **AI deepfakes of candidates** near elections. **Rule: never synthesize a candidate's or official's voice**; quote real audio only with a license, or describe what was said.

### 6.2 EU AI Act, Article 50 (if distributing to EU listeners)

- **Applies from 2026-08-02** (the Act entered into force 2024-08-01). It reaches providers and deployers outside the EU when the system's **output is used in the EU** (Art. 2(1)(c)). *(official; medium-high)*
- **Art. 50(2):** *providers* of generative systems must machine-mark output, which is the voice vendor's duty. **Art. 50(4):** *deployers* must disclose (a) **deep fakes**, meaning AI image, audio or video that resembles real persons, places or events and would falsely appear authentic, and (b) AI-generated or AI-manipulated **text published to inform the public on matters of public interest**. The exception for (b) is content that has gone through **human review or editorial control** with a person or company holding editorial responsibility. *(official; medium)*
- **Application** *(inference)*: a fully automated news pipeline **cannot use the human-review exception**, so disclosure is needed. Earlobe's spoken plus metadata disclosure in every episode should satisfy Art. 50(4) in substance. Art. 50 fines go up to **€15M or 3% of worldwide turnover** (Art. 99(4)). A Commission **code of practice on marking and labelling AI content** was being drafted from late 2025 (final expected mid-2026), and the **"Digital Omnibus"** proposal (Nov 2025) floated grace periods for some marking duties. **Status of both unverified.** Also consider **GDPR** basics for EU listener data, or geo-limiting EU distribution until counsel signs off. *(reported; low-medium)*

### 6.3 FTC (advertising, endorsements, impersonation)

- **Endorsement Guides (16 CFR Part 255; revised 2023-06-29):** material connections must be disclosed clearly and conspicuously. **In audio, say it.** Endorsers must be bona fide users, and virtual or AI influencers are covered. **An AI host must never claim personal experience** ("I've used this mattress for a year"). Use announcer-style reads ("This episode is sponsored by..."). *(official; medium-high)*
- **Rule on fake reviews and testimonials (16 CFR Part 465; effective 2024-10-21):** bans fake or AI-generated reviews and testimonials attributed to people who don't exist or have no experience. Civil penalties are about **$53,088 per violation** (2025 inflation figure, recalled). *(official; medium)*
- **Rule on impersonation of government and businesses (16 CFR Part 461; effective 2024-04-01):** don't name or brand shows in a way that implies they come from a court, police agency or news outlet. Avoid names like "LA County Court Updates" with official-looking seals. *(official; medium-high)*
- **Native advertising (2015 enforcement policy statement):** ads must be identifiable as ads. **No sponsored news segments**, which the editorial standards already ban. *(official; medium)*
- **New York synthetic-performer ad disclosure (signed Dec 2025, recalled):** ads using AI "synthetic performers" must disclose them, effective around mid-2026. It matters if Earlobe voices ads for NY audiences. *(reported; low-medium; verify)*

### 6.4 Federal AI and likeness landscape (recall)

- **TAKE IT DOWN Act** (signed 2025-05-19): criminalizes non-consensual intimate imagery, including AI deepfakes. Platforms that host user content must remove reported items within 48 h (compliance by May 2026). Low relevance unless the site hosts user uploads. *(official; medium)*
- **NO FAKES Act** (federal voice and likeness right): reintroduced in April 2025 with industry support; **not enacted as of last recall**. *(reported; medium-low)*
- **Executive order of Dec 2025** on a national AI policy framework: targets state AI laws through litigation and federal funding conditions. Watch for its effect on SB 942 and state deepfake laws. *(reported; medium-low)*

---

## 7. Platform policies

| Platform | Rule relevant to Earlobe | As of | Confidence |
|---|---|---|---|
| **Apple Podcasts** | Content guidelines require **prominent disclosure** when AI generates a meaningful part of the audio (synthetic voices, AI hosts), both **in the content and in show/episode metadata**. Deceptive or impersonating content is barred. Enforcement was not evident in sibling research. | 2026 live guidelines (per sibling notes) | medium-high |
| **Spotify** | **Verified by Spotify** badges for podcasts (authentic listenership is one factor) and **removal of shows impersonating a creator, including with AI voice clones** (2026-05-19). No blanket AI ban; reportedly no mandatory AI-disclosure rule for podcasts. Platform rules bar deceptive synthetic media presented as authentic in harmful ways. On the music side (Sept 2025), Spotify announced an AI-impersonation policy, a spam filter and AI credits through the DDEX standard. | 2026-05-19 (badges, impersonation, high); 2025-09 (music policy, medium) | high / medium |
| **YouTube** | Since **2024-03-18**, creators must use the **"altered or synthetic content"** setting for realistic synthetic content, including realistic synthetic voices of real people or depictions of real events. The label shows in the description, and **more prominently on the player for sensitive topics such as news, elections, health and finance**. Clearly unrealistic content and production help (script drafting, captions) are exempt. Repeated non-disclosure can mean removal or loss of Partner Program status. **July 2025 "inauthentic content"** rule: mass-produced, repetitive content is not monetizable (sibling note). | 2024-03 / 2025-07 | medium (recall) |
| **Distribution and ad partners** | iHeartMedia's "Guaranteed Human" pledge (2025-11; sibling notes) suggests some partners will avoid or limit synthetic shows. | 2025-11 | medium |

**Recommendation** *(inference)*: one disclosure standard everywhere:
1. a spoken line at the top of every episode (already gate rule S1);
2. a disclosure sentence in **every show description and episode description**;
3. YouTube's synthetic toggle **on** for all Earlobe uploads, since news is a "sensitive topic";
4. a public **"How this show is made"** page explaining the Trust Stack, the voices and the corrections policy.

---

## 8. Voice and likeness rights

- **Tennessee ELVIS Act** (signed 2024-03-21; effective 2024-07-01): adds **voice**, actual or simulated, to Tennessee's right of publicity. It creates liability for publishing or transmitting someone's voice or likeness without authorization, and for distributing a tool whose **primary purpose** is reproducing a specific person's voice without authorization. There are exemptions for news, commentary, satire and documentary uses **to the extent the First Amendment protects them**. Those exemptions don't cover making a false impression that a recording is authentic. *(official; medium-high)*
- **California** *(official; medium)*:
  - Civil Code §3344 covers living persons in commercial use.
  - Civil Code §3344.1 covers deceased personalities for 70 years after death, with exemptions for news, public affairs and documentary work. **AB 1836 (2024; effective 2025-01-01)** extended this to **digital replicas** of deceased personalities in audiovisual works and sound recordings. **This matters for History of Hollywood: no synthetic recreations of dead stars' voices.**
  - **AB 2602 (2024; Labor Code §927)** makes contract terms allowing a digital replica of a living performer's voice or likeness unenforceable unless the intended uses are specifically described and the performer had a lawyer or union representation.
- **New York:** Civil Rights Law §§50-51 (commercial use of name, voice or likeness) and §50-f (post-mortem rights, including digital replicas), with late-2025 amendments recalled. **Illinois:** amendments to the Right of Publicity Act on digital replicas and the **Digital Voice and Likeness Protection Act** (2024). **South Carolina:** no statute recalled; common-law appropriation applies. *(official; low-medium)*
- **Vendor terms:** ElevenLabs bars cloning a voice without the owner's consent and blocks some political-figure voices. A **paid plan is required for a commercial license**; the Free plan has none (sibling voice note). Shared "Voice Library" voices belong to real people who can withdraw them under the platform's notice rules. *(reported; medium on the commercial-license point, low on Voice Library terms)*
- **Recommendation** *(inference; [LAWYER] for any human voice deal)*:
  1. Build personas from **fully synthetic designed voices** (ElevenLabs Voice Design) that the LLC controls, and record the design prompt and voice ID in a register.
  2. If you ever use a human voice actor, get a **written AI-replica agreement** that lists the specific uses (meeting AB 2602 and the Illinois rules), pays for scope and duration, and allows termination.
  3. **No persona resembling a real journalist**, no invented human backstory and no fake credentials (the Inception Point lesson).
  4. **Never voice real people's words in a synthetic copy of their voice**, including officials, celebrities, victims and defendants. Paraphrase instead, or use licensed real audio.

---

## 9. Privacy (website, newsletter, listener data)

- **CalOPPA** (Bus. & Prof. Code §22575 ff.): **any** commercial website or online service that collects personally identifiable information from California residents must post a privacy policy, regardless of size. It must cover the categories of data collected, third parties, Do Not Track handling and the effective date. **This applies on day one.** *(official; medium-high)*
- **CCPA/CPRA** applies to for-profit businesses that do business in California and meet **one** of these tests:
  - gross annual revenue over **$26,625,000** (CPI-adjusted figure effective 2025-01-01; next adjustment due 2027);
  - buy, sell or **share** personal information of **100,000+ California consumers or households** a year;
  - earn 50%+ of revenue from selling or sharing personal information.

  *(official; medium)* **The 100,000 test is the realistic trigger.** Dynamic ad insertion and ad-tech pixels "share" IP addresses and device IDs for cross-context behavioral advertising, and an LA market plus national shows could reach 100,000 Californians. Once triggered, Earlobe needs:
  - a "Do Not Sell or Share" link;
  - honoring **Global Privacy Control** signals;
  - data-subject request handling;
  - vendor contracts;
  - the newer regulations (approved Sept 2025, phased in from 2026) on risk assessments and automated decision-making.

  *(inference/official; medium)*
- **Pixel and wiretap litigation:** a wave of **California Invasion of Privacy Act (CIPA)** class actions targets websites using tracking pixels, chat widgets and session replay. The VPPA is a risk for sites with video and Meta Pixel. A 2025 reform bill (SB 690) stalled, as recalled. **Keep trackers to a minimum; use a consent banner.** *(reported; medium-low)*
- **Newsletter (CAN-SPAM):** accurate headers and subject lines, a valid **postal address**, a working unsubscribe honored within **10 business days**, and ads identified as ads. Penalties are about $53,088 per email (2025 figure, recalled). Gmail and Yahoo bulk-sender rules (2024) require SPF, DKIM, DMARC and **one-click unsubscribe** for large senders. *(official; medium)*
- **Illinois BIPA:** voiceprints are biometric identifiers. **Do not run speaker identification or voice cloning on listener voicemails or tips.** Store them as audio and transcripts only, with a retention limit. BIPA damages are statutory, at $1,000 or $5,000 per violation. *(official; medium)*
- **COPPA:** keep the network general-audience; don't knowingly collect data from under-13s. **Other state privacy laws:** about 20 states have comprehensive laws with thresholds near 100,000 residents. **South Carolina, Illinois and New York have no comprehensive consumer privacy law recalled**; New York has the SHIELD Act on data security and breach notice. *(official; medium-low)*
- **GDPR** applies if Earlobe targets EU listeners. Use a podcast host with a data-processing agreement and minimal analytics. *(inference)*

---

## 10. Business setup

### 10.1 Entity, tax status and ownership *(confirm with [CPA] and [LAWYER])*

- **Unknown: the LLC's state of formation.** If the founders or managers work from **California**, the LLC is very likely "doing business" in California under Rev. & Tax. Code §23101, triggering the **$800 minimum annual franchise tax**, the LLC fee once gross receipts pass $250,000, and **foreign-LLC registration** with the CA Secretary of State if it was formed elsewhere. Penalties for non-registration are meaningful. *(official; medium)*
- **Beneficial ownership (CTA/BOI):** FinCEN's **March 2025 interim final rule exempted US-formed companies** from beneficial-ownership reporting. Only foreign-formed reporting companies must file. Confirm nothing has changed. *(official; medium)*
- **Founder and contractor IP assignment** *(inference; high priority)*: the founders (the repo names Joshua German and Janel Moore) and every contractor should **assign all IP to the LLC** (code, prompts, persona designs, show formats, brand). Update the **operating agreement** to cover ownership splits, decision rights over legal threats (who can pull an episode), and what happens if a founder leaves. Investors, grant-makers, insurers and acquirers will ask.

### 10.2 DBA / assumed name for "Curious & Creative Network"

Adding "Network" makes this a different name from the LLC's legal name, so a DBA filing is needed wherever the state requires one.

| State | Requirement (as recalled) | Cost and timing (recall; verify) | Confidence |
|---|---|---|---|
| **California** | **Fictitious Business Name (FBN) statement** filed with the **county clerk where the principal place of business is** (LA County Registrar-Recorder/County Clerk), or **Sacramento County** if there is no California place of business (B&P §17910 ff.). File within **40 days** of first using the name. **Publish** in a newspaper of general circulation in that county **once a week for 4 straight weeks**, starting within **30 days** of filing, then file the proof of publication. Valid **5 years**; refile when facts change. Banks generally want the filed FBN before accepting payments in the DBA name. | LA County filing about **$26** for one name and one owner, plus about **$5** for each extra name or owner (recall; low). Publication about **$30 to $150** in LA through low-cost legal newspapers (inference; low). | medium (process) / low (fees) |
| **South Carolina** | **No statewide DBA or assumed-name registration** for LLCs (the Secretary of State does not register trade names). Protect the name by registering a **state trademark or service mark** with the SC Secretary of State (small fee), or federally. Separately, a **municipal or county business license** may be required: City of Columbia within city limits, Richland County in unincorporated areas. SC standardized local business licensing in 2020-2022 (license year May 1 to April 30; a statewide online portal). Whether a remote podcast producer with no SC office needs a Columbia license is **[LAWYER]/[CPA]**. | Business license tax is based on gross receipts; base fees are small (low). | low-medium |
| **New York** (later) | An LLC files a **Certificate of Assumed Name** with the NY Department of State, with county fees for each county where it does business. Only if it has a NY presence. | about $25 plus county fees (low) | low |
| **Illinois** (later) | An LLC files an **assumed name application** with the Illinois Secretary of State; the fee varies with the year of the 5-year cycle. | about $150 at most (low) | low |

### 10.3 Trademark

- **USPTO fees (Final Rule effective 2025-01-18, recall):**
  - **Base application $350 per class.** This replaced TEAS Plus/Standard.
  - Surcharges: **$100 per class** for insufficient information; **$200 per class** for free-form text instead of the ID Manual; **$200 per additional 1,000 characters** of free-form description.
  - After filing: Statement of Use **$150 per class**; extension of time to file it **$250 per class**; Section 8 declaration and Section 9 renewal **$325 per class** each.

  *(official; medium; verify on the fee schedule)* Using **pre-approved ID Manual wording** avoids the surcharges.
- **Classes** *(inference, based on recalled USPTO practice)*:
  - **Class 41 (file first):** entertainment and education services, namely providing non-downloadable podcasts in the fields of news, current events, true crime and history; news reporter services. This is the core service.
  - **Class 9 (file second):** downloadable podcasts and audio recordings. It covers downloadable goods.
  - **Class 38:** "podcasting services" in Class 38 means *transmission*, which a hosting company provides. **Low value for Earlobe**, which uses third-party hosts. Skip unless counsel advises otherwise.
  - **Class 35 (later):** advertising services for others, if Earlobe sells ad inventory or runs a services arm.
- **Filing basis:** **intent-to-use (§1(b))** before launch locks in priority. Each extension of the use deadline costs money. A US-domiciled LLC may file pro se, but **clearance plus filing through a trademark attorney** is advisable for the network name. *(official/inference; medium)*
- **Clearance flags** *(inference)*:
  - "Curious" is crowded in media and education; CuriosityStream is a documentary streaming brand in Classes 9, 38 and 41.
  - *Cold Case Files* is an established A&E title.
  - *Columbia Daily* and *LA Daily* echo existing papers.
  - "Breaking Desk" and "Case Tracker" need checks.

  The repo's contracts-ip-clerk is meant to run USPTO plus common-law searches. Budget for an attorney clearance opinion on the network name.
- **Budget** *(inference; low)*: USPTO $700 for Classes 41 and 9; an attorney clearance search and filing typically costs **$500 to $2,000 per mark**.

### 10.4 Domains and email *(inference)*

- Register the network .com, plus each show's short domain (or subpaths of one domain to cut cost), common typos and obvious variants. Turn on **WHOIS privacy** and **registrar lock**. Rough cost **$10 to $25 per domain per year** (recall; low).
- Use one **legal/notices@** mailbox and one **corrections@** mailbox, monitored by the contracts-ip-clerk and corrections agents, with a human backup.
- Set up **SPF, DKIM and DMARC** before sending the newsletter.

### 10.5 Bank, card, bookkeeping *(inference unless marked)*

- **Business checking and a business card in the LLC's name**, with the DBA added after the FBN is filed. Never mix personal and business funds; mixing undermines the LLC's liability shield. **Get the EIN** from the IRS for free.
- **Bookkeeping:** QuickBooks Online, Xero or Wave. Use **classes or tags per show and market**, because the ROI model needs revenue and cost by show. Track API, voice, hosting and music subscriptions as cost of revenue.
- **Sales tax:** ad revenue is generally not taxable. Direct subscription or digital-goods sales can be taxable in some states; Apple, Patreon and Spotify act as marketplace facilitators **[CPA]**.
- **1099 reporting:** the 1099-K threshold for payment platforms went back to $20,000 and 200 transactions under the 2025 federal tax law, as recalled *(official; low-medium)*. Issue 1099-NEC to US contractors.

### 10.6 Media liability / E&O insurance

- **What it covers:** defamation, invasion of privacy, copyright and trademark infringement in content, and **defense costs**. Defense costs are the main value: even a meritless libel suit costs tens of thousands of dollars to dismiss *(inference)*.
- **Cost ranges** *(reported/recall; low; get broker quotes)*:
  - Small independent podcasts: roughly **$500 to $2,500 a year** for a $1M limit.
  - Small digital news publishers: roughly **$2,500 to $10,000+ a year** for $1M per claim/aggregate, with **retentions (deductibles) of $2,500 to $25,000**.
  - True-crime and court-heavy, high-volume, **fully automated** publishing is likely to be priced higher, restricted or declined. Some carriers ask whether there is **pre-publication legal review**.
- **AI-specific underwriting** *(reported; low-medium)*: the industry has been introducing **generative-AI exclusions** (ISO filed GenAI exclusion endorsements for general liability policies around 2025-2026). Ask every carrier whether AI-generated content is excluded. **Describe the automated pipeline accurately on the application**, because misrepresentation can void coverage.
- **Where to look** *(recall; verify)*: specialist media brokers and carriers (Hiscox, Media/Professional, Markel, AXIS, Beazley, Chubb), and news-association member programs (LION Publishers, INN) where a for-profit LLC qualifies. **Free and low-cost legal help:** the Reporters Committee for Freedom of the Press legal hotline; Lawyers for Reporters (pro bono for local news; check eligibility); the First Amendment Coalition (California); and the Media Law Resource Center's lawyer directory.
- **Planning recommendation** *(inference)*: budget **$6,000 a year** as a placeholder for $1M media liability with a $10,000 retention. Hold the court and true-crime trackers in strict mode with human sign-off until a policy is bound.

### 10.7 Policies and site pages (day-one set)

1. **Terms of Use:** site and newsletter rules; a **license for listener submissions** (tips, voicemails, comments); no reliance on content as legal or medical advice; DMCA notice procedure; governing law and venue; whether to add an arbitration clause **[LAWYER]**.
2. **Privacy Policy:** compliant with CalOPPA now and CCPA-ready. Cover cookies and pixels, podcast-host analytics, the newsletter, tips and voicemails (no biometrics), retention and contact.
3. **Corrections & Ethics Policy:** see §3.5. Link it from every show's notes.
4. **AI Disclosure / "How this show is made":** the Trust Stack, synthetic voices, sources and the public trust log.
5. **Legal notice and contact page:** postal address, legal@ email and response commitment.
6. **DMCA designated agent** registered with the US Copyright Office (**$6 per filing, renewed every 3 years**, recall; medium) if the site hosts any user content.
7. **Accessibility:** transcripts for every episode. This supports ADA website accessibility and is already natural for a text-first pipeline.
8. **Records retention and litigation hold:** keep scripts, sources, verifier reports and audio for at least the longest limitation period (2 years in SC; longer for archive shows that get re-released). Freeze deletion for any episode under a legal threat. *(inference)*

### 10.8 Contracts register *(inference; the repo's contracts-ip-clerk owns this)*

Templates and records to keep:
- contractor agreements with IP assignment;
- a voice-actor AI-replica agreement, if one is ever used;
- the music license log;
- insertion orders with an **AI-voiced read disclosure** clause and **no personal-experience claims**;
- syndication or licensing term sheets with local outlets;
- vendor terms on file (ElevenLabs commercial license, LLM vendors' usage policies on news and election content, hosting terms).

---

## 11. Prioritized founder legal checklist

**P0: before any episode auto-publishes**
1. **Engage a media lawyer** for a one-time setup review covering lanes and naming rules, the fair-report drafting rules, disclosure wording, the corrections policy, Terms and Privacy, and a **legal-threat escalation path**. Ask for a flat fee. *(budget placeholder $2,500 to $7,500, inference)* **[LAWYER]**
2. **Bind media liability / E&O insurance** ($1M) and disclose the automation honestly. Confirm there is no generative-AI exclusion.
3. **Launch posture:** daily briefs may auto-publish in the standard lane. **Court and true-crime trackers and Breaking Desk naming stay strict, with a recorded human sign-off, until (1) and (2) are done** and the first 30 days of trust-log data look clean.
4. **Hard Trust Stack rules:**
   - every allegation attributed to an official record in the same sentence;
   - identity disambiguation before naming;
   - no naming for minor offenses;
   - no minors, victims, sealed or juvenile material;
   - **no invented quotes or dramatized dialogue**;
   - follow-up when cases are dismissed or end in acquittal;
   - source snapshots stored.
5. **AI disclosure everywhere:** spoken line, show and episode descriptions, YouTube synthetic toggle, a "How this is made" page, and bot self-identification in social and community replies.
6. **Voices:** original designed synthetic voices only, on a **paid ElevenLabs plan with a commercial license**. Keep a voice register. Never clone or simulate real people. Never strip provenance metadata.
7. **Music:** a business-tier library license and/or a commissioned theme, with a license log. No commercial songs.
8. **Copyright hygiene:** multi-source synthesis, the originality checker (12-word limit), credit and links in show notes, verified attribution, no paywall-bypass ingestion, no adapting CC-ND text.
9. **Publish the Privacy Policy, Terms, Corrections policy and legal contact.** Make the newsletter CAN-SPAM-compliant. Keep trackers minimal and add a consent banner.
10. **Name clearance** on the network and every show and persona name (USPTO plus common-law). Rename anything that collides (for example *Cold Case Files*).

**P1: first 30 to 60 days**

11. **DBA:** a California FBN in the county of the principal place of business (or Sacramento County), with 4 weeks of publication. In South Carolina, check City of Columbia and Richland County business-license duties. **[CPA]**
12. **Confirm the LLC's formation state and California "doing business" status** (the $800 minimum tax and foreign registration). **[CPA]**
13. **File trademarks:** network name in **Class 41** (intent-to-use), then **Class 9**. Hold off on Class 38. Consider Class 35 later. **[LAWYER]** for clearance on "Curious".
14. **Domains and email:** network and show domains, WHOIS privacy, legal@ and corrections@, SPF, DKIM and DMARC.
15. **Bank and card in the LLC name** (add the DBA once filed). Set up bookkeeping with show-level classes. Note that domestic companies are exempt from BOI reporting under the March 2025 rule; confirm.
16. **Founder IP assignment and operating-agreement update; contractor IP assignment.** **[LAWYER]**
17. **Advertising rules:** spoken sponsor disclosure; no AI personal-experience endorsements; legal-screener ad mode on; **no political ads** at launch.
18. **DMCA agent registration** ($6) if the site takes comments or uploads.

**P2: before NYC and Chicago, EU distribution, or real monetization**

19. **New York and Illinois review:**
   - New York: Civil Rights Law §74 and the §76-a actual-malice and anti-SLAPP rules;
   - Illinois: common-law fair report under *Solaia*, and BIPA (no listener voiceprints);
   - New York's synthetic-performer ad disclosure if AI voices sell ads.

   **[LAWYER]**
20. **EU:** confirm the Art. 50(4) disclosure wording and GDPR basics, or geo-limit. Watch the code of practice and the Digital Omnibus.
21. **CCPA readiness:** track California audience reach and ad-tech "sharing". Add "Do Not Sell or Share", Global Privacy Control and request handling **before** 100,000 California consumers.
22. **Content licensing:** pursue deals or partnerships with local outlets and AP. They lower copyright and hot-news risk and buy goodwill.
23. **Copyright registrations** for human-authored assets (theme music, written policies, artwork), disclaiming AI material.

**P3: ongoing**

24. **Quarterly legal watch** on Walters-type and Perplexity/Cohere-type case outcomes, SB 942/AB 853, the federal executive order litigation, NO FAKES, state deepfake and AI-news disclosure bills, and platform policy changes. The Compliance & Platform Policy Watch agent owns this.
25. **Annual insurance renewal** with trust-log metrics (corrections per 100 episodes, holds and kills) to support better pricing.
26. **Records retention and litigation-hold drill**; **annual Terms and Privacy refresh.**

## 12. Where a media lawyer is specifically needed

- The fair-report scope in **South Carolina**: cites, and whether it is absolute or qualified. Whether **police statements and press releases** count as official proceedings in each of the four states.
- Whether **California Civ. Code §48a** (retraction) covers a podcast network.
- The **actual malice and negligence posture of a fully automated publisher**: what process evidence courts will look at, and how the trust log should be designed and retained, given it is discoverable.
- Whether to use **arbitration and class-waiver clauses** in the Terms.
- **Voice-actor or likeness deals**, and any use of real public figures' audio.
- **Trademark clearance** for "Curious & Creative Network" and the show names.
- **EU distribution** under the AI Act and GDPR, and **election-season** coverage under state deepfake laws.
- Any **demand letter, subpoena or takedown**. Escalate within 1 hour, per the repo KPI.

---

## 13. Findings table

All rows: **not fetched this session** (no search budget; direct fetches failed DNS). The "Source" column gives where to verify.

| Fact | Value | As-of | Source | Confidence |
|---|---|---|---|---|
| §230 immunity for Earlobe's own AI-written episodes | None: Earlobe is the information content provider (§230(f)(3)) | statute (recall) | [47 U.S.C. §230](https://www.law.cornell.edu/uscode/text/47/230) | high (official) |
| *Walters v. OpenAI* | Summary judgment for OpenAI | 2025-05-19 (recall) | [CourtListener search](https://www.courtlistener.com/?q=%22Walters%22+%22OpenAI%22+defamation) | medium (reported) |
| *Starbuck v. Meta* | Filed April 2025; settled Aug 2025 | 2025-08 (recall) | [CourtListener search](https://www.courtlistener.com/?q=Starbuck+Meta+defamation) | medium (reported) |
| *Starbuck v. Google* | Filed Oct 2025, about $15M sought; pending | 2025-10 (recall) | [CourtListener search](https://www.courtlistener.com/?q=Starbuck+Google+defamation) | low-medium (reported) |
| *Wolf River Electric v. Google* | AI Overview defamation suit; claimed damages over $100M | 2025 (recall) | [CourtListener search](https://www.courtlistener.com/?q=%22Wolf+River+Electric%22+Google) | low-medium (reported) |
| Actual malice standard (public figures) | Knowledge of falsity or reckless disregard | 1964 | [NYT v. Sullivan, 376 U.S. 254](https://supreme.justia.com/cases/federal/us/376/254/) | high (official) |
| Private-figure minimum fault | At least negligence; actual malice for presumed or punitive damages | 1974 | [Gertz, 418 U.S. 323](https://supreme.justia.com/cases/federal/us/418/323/) | high (official) |
| California private-figure standard | Negligence (*Brown v. Kelly Broadcasting*, 1989) | recall | [CourtListener search](https://www.courtlistener.com/?q=%22Brown+v.+Kelly+Broadcasting%22) | medium (official) |
| New York private-figure standard | Gross irresponsibility; actual malice for public-interest suits under §76-a (2020) | 2020 (recall) | [NY Civ. Rights Law §76-a](https://www.nysenate.gov/legislation/laws/CVR/76-A) | medium (official) |
| Illinois private-figure standard | Negligence (*Troman v. Wood*, 1975) | recall | [CourtListener search](https://www.courtlistener.com/?q=%22Troman+v.+Wood%22) | medium (official) |
| South Carolina private-figure posture | Fault required; no presumed malice on public-concern speech (*Erickson*, 2006) | recall | [CourtListener search](https://www.courtlistener.com/?q=%22Erickson+v.+Jones+Street+Publishers%22) | low-medium (official) |
| California fair report privilege | Civ. Code §47(d): fair and true report of judicial, legislative or official proceedings; absolute; §47(d)(2) exceptions | recall | [Cal. Civ. Code §47](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=47) | medium-high (official) |
| New York fair report privilege | Civ. Rights Law §74; "substantially accurate" test | recall | [NY Civ. Rights Law §74](https://www.nysenate.gov/legislation/laws/CVR/74) | medium-high (official) |
| Illinois fair report privilege | Common law; Restatement §611 adopted in *Solaia* (2006) | recall | [CourtListener search](https://www.courtlistener.com/?q=%22Solaia+Technology%22+%22Specialty+Publishing%22) | medium (official) |
| South Carolina fair report privilege | Common law; no statute recalled | recall | [SC Code of Laws](https://www.scstatehouse.gov/code/statmast.php) | low-medium (official) |
| Defamation limitation periods | CA 1 yr; NY 1 yr; IL 1 yr; SC 2 yrs | recall | [SC Code §15-3-550](https://www.scstatehouse.gov/code/t15c003.php); [Cal. CCP §340](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CCP&sectionNum=340) | medium (official) |
| California retraction statute | §48a: 20-day demand; correction within 3 weeks limits damages to special damages | recall | [Cal. Civ. Code §48a](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=48a) | medium (official) |
| Facts not copyrightable | *Feist* (1991) | 1991 | [Feist, 499 U.S. 340](https://supreme.justia.com/cases/federal/us/499/340/) | high (official) |
| Hot-news doctrine narrowed | *NBA v. Motorola* (1997); *Barclays v. Theflyonthewall* (2011) pre-emption | 2011 | [CourtListener search](https://www.courtlistener.com/?q=%22Theflyonthewall%22+Barclays) | medium-high (official) |
| *NYT v. OpenAI/Microsoft* | Motion to dismiss largely denied; consolidated MDL ongoing | 2025 (recall) | [CourtListener search](https://www.courtlistener.com/?q=%22New+York+Times%22+OpenAI+Microsoft) | medium (reported) |
| *Dow Jones v. Perplexity* | Motion to dismiss or transfer denied | 2025-08 (recall) | [CourtListener search](https://www.courtlistener.com/?q=%22Dow+Jones%22+Perplexity) | medium-low (reported) |
| *Thomson Reuters v. Ross* | Not fair use (non-generative AI); 3rd Cir. appeal | 2025-02-11 | [CourtListener search](https://www.courtlistener.com/?q=%22Thomson+Reuters%22+Ross+Intelligence) | medium (official) |
| *Bartz v. Anthropic* | Training on lawfully bought books is fair use; piracy not; about $1.5B settlement | 2025-06 / 2025-09 (recall) | [CourtListener search](https://www.courtlistener.com/?q=Bartz+Anthropic) | medium (reported) |
| AI-only output copyrightability | Not protected without enough human authorship (*Thaler*, D.C. Cir.) | 2025-03-18 | [USCO AI hub](https://www.copyright.gov/ai/) | medium-high (official) |
| SB 942 covered-provider threshold | GenAI system with over 1M monthly users | 2024 | [SB 942](https://leginfo.legislature.ca.gov/faces/billNavClient.xhtml?bill_id=202320240SB942) | medium (official) |
| SB 942 operative date | 2026-08-02 (delayed from 2026-01-01 by AB 853) | 2025-10 (recall) | [AB 853](https://leginfo.legislature.ca.gov/faces/billNavClient.xhtml?bill_id=202520260AB853) | medium (official) |
| SB 942 penalty | $5,000 per violation, per day | 2024 | [SB 942](https://leginfo.legislature.ca.gov/faces/billNavClient.xhtml?bill_id=202320240SB942) | medium (official) |
| Large-platform provenance duty (AB 853) | From 2027-01-01 | 2025-10 (recall) | [AB 853](https://leginfo.legislature.ca.gov/faces/billNavClient.xhtml?bill_id=202520260AB853) | low-medium (official) |
| EU AI Act Art. 50 application | 2026-08-02; deployers disclose deep fakes and public-interest AI text unless human editorial control | 2024 Act | [EUR-Lex Reg. 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj) | medium-high (official) |
| EU Art. 50 maximum fine | €15M or 3% of worldwide turnover (Art. 99(4)) | 2024 | [EUR-Lex Reg. 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj) | medium (official) |
| FTC Endorsement Guides revision | 2023-06-29; virtual influencers covered; audio disclosure must be spoken | 2023 | [16 CFR Part 255](https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-255) | medium-high (official) |
| FTC fake reviews rule | Effective 2024-10-21; about $53,088 per violation (2025 figure) | 2024-2025 | [16 CFR Part 465](https://www.ecfr.gov/current/title-16/chapter-I/subchapter-D/part-465) | medium (official) |
| FTC impersonation rule | Government and business impersonation; effective 2024-04-01 | 2024 | [16 CFR Part 461](https://www.ecfr.gov/current/title-16/chapter-I/subchapter-D/part-461) | medium-high (official) |
| Apple Podcasts AI rule | Prominent disclosure of AI or synthetic audio in content and metadata | 2026 (sibling notes) | [Apple guidelines](https://podcasters.apple.com/support/891-content-and-subscription-guidelines) | medium-high (official) |
| Spotify AI-impersonation and verified badges | Removes AI clones that impersonate; "Verified by Spotify" for podcasts | 2026-05-19 | [Variety](https://variety.com/2026/digital/news/spotify-bans-ai-generated-podcasts-impersonate-verified-badges-1236752944/) | high (reported, 2+ sources in sibling notes) |
| YouTube synthetic disclosure | Required for realistic altered or synthetic content; prominent label on news topics | 2024-03-18 | [YouTube Help](https://support.google.com/youtube/answer/14328491) | medium (official) |
| Tennessee ELVIS Act | Voice added to right of publicity; effective 2024-07-01 | 2024 | [TN HB 2091](https://wapp.capitol.tn.gov/apps/BillInfo/Default.aspx?BillNumber=HB2091&GA=113) | medium-high (official) |
| California digital replica laws | AB 1836 (deceased), AB 2602 (contracts); effective 2025-01-01 | 2024 | [AB 1836](https://leginfo.legislature.ca.gov/faces/billNavClient.xhtml?bill_id=202320240AB1836); [AB 2602](https://leginfo.legislature.ca.gov/faces/billNavClient.xhtml?bill_id=202320240AB2602) | medium (official) |
| ElevenLabs commercial license | Paid plans only; Free has none | 2026-10 | [ElevenLabs pricing](https://elevenlabs.io/pricing) (via sibling voice note) | high (sibling note) |
| CCPA revenue threshold | $26,625,000 (from 2025-01-01) | 2025 | [CPPA](https://cppa.ca.gov/regulations/) | medium (official) |
| CCPA consumer threshold | 100,000+ California consumers or households bought, sold or shared | statute | [CA AG CCPA](https://oag.ca.gov/privacy/ccpa) | medium-high (official) |
| CalOPPA | Privacy policy required for any commercial site collecting PII from Californians | statute | [B&P §22575](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=BPC&sectionNum=22575) | medium-high (official) |
| CAN-SPAM opt-out window | 10 business days | statute | [FTC CAN-SPAM guide](https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business) | medium-high (official) |
| USPTO base application fee | $350 per class (from 2025-01-18) | 2025 | [USPTO fee schedule](https://www.uspto.gov/learning-and-resources/fees-and-payment/uspto-fee-schedule) | medium (official) |
| USPTO surcharges | $100 insufficient info; $200 free-form ID; $200 per extra 1,000 characters (per class) | 2025 | [USPTO fee schedule](https://www.uspto.gov/learning-and-resources/fees-and-payment/uspto-fee-schedule) | medium (official) |
| USPTO post-filing fees | Statement of Use $150; extension $250; §8 and §9 $325 (per class) | 2025 | [USPTO fee schedule](https://www.uspto.gov/learning-and-resources/fees-and-payment/uspto-fee-schedule) | low-medium (official) |
| California FBN process | File with county clerk within 40 days; publish 4 weeks; valid 5 years | statute | [B&P §17910](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=BPC&sectionNum=17910); [LA County RR/CC](https://www.lavote.gov/home/county-clerk/fictitious-business-names) | medium (official) |
| LA County FBN fee | About $26 first name and owner, plus about $5 each extra | recall | [LA County RR/CC](https://www.lavote.gov/home/county-clerk/fictitious-business-names) | low (official) |
| South Carolina DBA | No statewide DBA registration; local business license may apply | recall | [SC Secretary of State](https://sos.sc.gov/) | low-medium (official) |
| California minimum franchise tax (LLC doing business in CA) | $800 a year | recall | [CA FTB](https://www.ftb.ca.gov/file/business/types/limited-liability-company/index.html) | medium (official) |
| BOI reporting for US companies | Exempt (FinCEN interim final rule) | 2025-03 | [FinCEN BOI](https://www.fincen.gov/boi) | medium (official) |
| DMCA designated agent fee | $6, renew every 3 years | recall | [USCO DMCA directory](https://www.copyright.gov/dmca-directory/) | medium (official) |
| Media liability premium, small podcast | About $500 to $2,500 a year for $1M | recall | broker quotes needed | low (inference) |
| Media liability premium, small news publisher | About $2,500 to $10,000+ a year; retention $2,500 to $25,000 | recall | broker quotes needed | low (inference) |
| Production music business tier | About $15 to $50 a month; enterprise by quote | recall | [Epidemic Sound pricing](https://www.epidemicsound.com/pricing/) | low (reported) |

---

## 14. Open questions / gaps

1. **Nothing was verified live this session.** Re-run with search budget to confirm, in priority order:
   - USPTO fee table;
   - SB 942/AB 853 dates and scope;
   - EU Art. 50 status (code of practice, Digital Omnibus);
   - Apple's exact AI-disclosure wording and any RSS tag;
   - YouTube's current synthetic-content rules for synthetic *narrators* (not just impersonation);
   - LA County FBN fees;
   - SC business-license duty for a remote producer;
   - 2026 outcomes in *Starbuck v. Google*, *Wolf River*, *Dow Jones v. Perplexity*, *NYT v. OpenAI* and *Thomson Reuters v. Ross* (3rd Cir.).
2. **Any 2026 AI-defamation ruling against a *publisher*** (as opposed to an AI vendor) using AI-written news. None is known; that would be the most relevant precedent.
3. **South Carolina law:** the fair-report cites and nature; the exact private-figure fault level; whether there is any retraction statute; whether there is any 2025-2026 anti-SLAPP enactment.
4. **Whether California Civ. Code §48a covers podcasts.** Whether police press releases fall under §47(d) and §74.
5. **The LLC's state of formation and principal place of business.** This drives the FBN county, the California franchise tax and foreign registration.
6. **Insurance:** actual quotes, and whether carriers will write fully automated news and true-crime at all; which carriers carry generative-AI exclusions.
7. **Platform specifics:** whether Spotify has added a podcast AI-label requirement since May 2026; Apple's enforcement practice; whether iHeart or Amazon distribution excludes synthetic shows.
8. **State "AI-generated news" disclosure bills** (proposals were seen in some legislatures, recalled with low confidence). Any enacted by Oct 2026 would apply directly.
9. **NY synthetic-performer ad disclosure law:** exact effective date and scope.
10. **AI music licensing terms after the 2025 label settlements** (Suno, Udio, Eleven Music) for a commercial podcast network.
11. **Effect of the Dec 2025 federal executive order** on California and other state AI laws, including any litigation.

## 15. Sources

*None of these were opened this session; they are where to verify. Sibling-note sources are marked.*

- [47 U.S.C. §230 (Cornell LII)](https://www.law.cornell.edu/uscode/text/47/230)
- [California Civil Code §47 (leginfo)](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=47)
- [California Civil Code §48a (leginfo)](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=48a)
- [California Code of Civil Procedure §340 (leginfo)](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CCP&sectionNum=340)
- [New York Civil Rights Law §74 (NY Senate)](https://www.nysenate.gov/legislation/laws/CVR/74)
- [New York Civil Rights Law §76-a (NY Senate)](https://www.nysenate.gov/legislation/laws/CVR/76-A)
- [South Carolina Code Title 15, Chapter 3 (limitations)](https://www.scstatehouse.gov/code/t15c003.php)
- [South Carolina Code of Laws index](https://www.scstatehouse.gov/code/statmast.php)
- [NYT v. Sullivan, 376 U.S. 254 (Justia)](https://supreme.justia.com/cases/federal/us/376/254/)
- [Gertz v. Robert Welch, 418 U.S. 323 (Justia)](https://supreme.justia.com/cases/federal/us/418/323/)
- [Feist v. Rural Telephone, 499 U.S. 340 (Justia)](https://supreme.justia.com/cases/federal/us/499/340/)
- [INS v. Associated Press, 248 U.S. 215 (Justia)](https://supreme.justia.com/cases/federal/us/248/215/)
- [CourtListener case search (Walters, Starbuck, Wolf River, Perplexity, NYT v. OpenAI, Ross, Bartz, Solaia, Erickson)](https://www.courtlistener.com/)
- [US Copyright Office: Copyright and AI](https://www.copyright.gov/ai/)
- [US Copyright Office: DMCA designated agent directory](https://www.copyright.gov/dmca-directory/)
- [California SB 942 (AI Transparency Act)](https://leginfo.legislature.ca.gov/faces/billNavClient.xhtml?bill_id=202320240SB942)
- [California AB 853 (2025 amendments)](https://leginfo.legislature.ca.gov/faces/billNavClient.xhtml?bill_id=202520260AB853)
- [California AB 1836 (digital replicas, deceased)](https://leginfo.legislature.ca.gov/faces/billNavClient.xhtml?bill_id=202320240AB1836)
- [California AB 2602 (digital replica contracts)](https://leginfo.legislature.ca.gov/faces/billNavClient.xhtml?bill_id=202320240AB2602)
- [California B&P §22575 (CalOPPA)](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=BPC&sectionNum=22575)
- [California B&P §17910 (fictitious business names)](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=BPC&sectionNum=17910)
- [LA County Registrar-Recorder/County Clerk: Fictitious Business Names](https://www.lavote.gov/home/county-clerk/fictitious-business-names)
- [California Privacy Protection Agency: regulations](https://cppa.ca.gov/regulations/)
- [California Attorney General: CCPA](https://oag.ca.gov/privacy/ccpa)
- [California FTB: LLC](https://www.ftb.ca.gov/file/business/types/limited-liability-company/index.html)
- [EU AI Act, Regulation (EU) 2024/1689 (EUR-Lex)](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- [EU AI Act Article 50 (explainer site)](https://artificialintelligenceact.eu/article/50/)
- [FTC Endorsement Guides, 16 CFR Part 255 (eCFR)](https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-255)
- [FTC Consumer Reviews and Testimonials Rule, 16 CFR Part 465 (eCFR)](https://www.ecfr.gov/current/title-16/chapter-I/subchapter-D/part-465)
- [FTC Impersonation Rule, 16 CFR Part 461 (eCFR)](https://www.ecfr.gov/current/title-16/chapter-I/subchapter-D/part-461)
- [FTC CAN-SPAM compliance guide](https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business)
- [Tennessee ELVIS Act (HB 2091)](https://wapp.capitol.tn.gov/apps/BillInfo/Default.aspx?BillNumber=HB2091&GA=113)
- [Apple Podcasts for Creators: content guidelines](https://podcasters.apple.com/support/891-content-and-subscription-guidelines) (sibling notes)
- [Variety: Spotify bans AI impersonation podcasts, adds verified badges (2026)](https://variety.com/2026/digital/news/spotify-bans-ai-generated-podcasts-impersonate-verified-badges-1236752944/) (sibling notes)
- [Music Business Worldwide: Verified badges extended to podcasts](https://www.musicbusinessworldwide.com/spotify-extends-verified-by-spotify-badges-to-podcasts-further-cracking-down-on-ai-impersonators/) (sibling notes)
- [YouTube Help: disclosing altered or synthetic content](https://support.google.com/youtube/answer/14328491)
- [ElevenLabs pricing](https://elevenlabs.io/pricing) (sibling voice note)
- [ElevenLabs terms of use](https://elevenlabs.io/terms-of-use)
- [USPTO fee schedule](https://www.uspto.gov/learning-and-resources/fees-and-payment/uspto-fee-schedule)
- [South Carolina Secretary of State](https://sos.sc.gov/)
- [FinCEN: Beneficial Ownership Information](https://www.fincen.gov/boi)
- [Epidemic Sound pricing](https://www.epidemicsound.com/pricing/)
- [Reporters Committee for Freedom of the Press: legal hotline](https://www.rcfp.org/legal-hotline/)
- [Media Law Resource Center](https://medialaw.org/)
- [First Amendment Coalition](https://firstamendmentcoalition.org/)
- Sibling notes in this folder: `hosting-and-monetization-platforms.md`, `competitive-landscape.md`, `voice-tts-costs.md`, `markets-sources-and-courts.md`, `liquid-studios-pivot-and-press.md`
