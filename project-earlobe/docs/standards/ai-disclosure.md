# AI Disclosure Standard

**The Curious & Creative Network: how we tell listeners, every time, that software made the show**

| | |
|---|---|
| **Publisher** | Curious & Creative LLC (publisher of record; accountable for every episode) |
| **Applies to** | Every episode, clip and post on every show, in every market |
| **Parent rules** | [Editorial Standards](editorial-standards.md) §14 `VOICE-1`–`VOICE-6` and §15 `AUTO-1`. If the two disagree, Editorial Standards win |
| **Code** | `earlobe/producer/disclosure.py` (spoken), `earlobe/publish/__init__.py` `disclosure_text()` (metadata), gate rule `S1` |
| **Voices** | Original personas only: [`config/voices.yaml`](../../config/voices.yaml), [Voice & Persona Guide](voice-and-persona-guide.md) |
| **Version** | 1.0, October 12, 2026 |

> **How to read this page.** Sections 1 to 4 are the policy and the exact scripts. Section 5 is the text we
> paste into each platform. Section 8 lists what to re-check because platform rules change. Spoken lengths
> are estimates at 155 words a minute (the studio's own estimator in `studio/tts.py`; the planning basis is
> 150 wpm, `F-TTS-15`). "Legal note" means [legal-compliance-business-setup](../research/notes/legal-compliance-business-setup.md).
> Gaps between this page and the code are in [§9](#9-not-yet-in-code).

---

## 1. The policy: ten rules

| # | Rule | Backed by |
|---|---|---|
| **DISC-1** | **Spoken, and last.** Every episode ends with the spoken disclosure. Only a music tail may follow it. | `VOICE-3`, gate `S1` (presence); position is `NE-1` |
| **DISC-2** | **One disclosure voice.** Ava (`disclosure_voice`) speaks it on every show, so listeners learn one "this is the disclosure" voice. A host never reads their own. | `NE-3` |
| **DISC-3** | **Five things, every time**, in every variant: see §2. | `VOICE-4` |
| **DISC-4** | **Spoken and written.** The same facts sit in the metadata of every show and every episode. | `VOICE-5`, `NE-2` |
| **DISC-5** | **Plain words.** Say "AI", "synthetic", "software", "automated". Never "virtual team", "our newsroom of editors", "our reporter" or "we spoke to". | `NEVER-7`, `VOICE-6` |
| **DISC-6** | **Original voices only.** No cloned, imitated or "in the style of" voices. No real person's words in a synthetic copy of their voice. | `NEVER-4`, `VOICE-1`, `QUO-6` |
| **DISC-7** | **Over-disclose when unsure.** Where a platform's rule is unclear, use its strictest setting. The cost is a label. The risk we avoid is a takedown for hiding one. *(inference)* | legal note §7 |
| **DISC-8** | **Never for sale, never stripped.** No sponsor, partner or distributor can buy or request removal. We never strip vendors' provenance metadata or watermarks. *(inference)* | `COI-1`, legal note §6.1 |
| **DISC-9** | **Clips and posts count.** Anything we cut from an episode or post carries a visible "AI-voiced" label and a link to the full disclosure (§5). | `VOICE-3` spirit |
| **DISC-10** | **The company answers.** "The AI made a mistake" is never an excuse, on air or off. | `AUTO-1` |

## 2. The five things every disclosure says

| | Must say | Ear version |
|---|---|---|
| **a** | Written and voiced using AI | "AI wrote and voiced this episode." |
| **b** | Voices are synthetic, not real people | "The voices are synthetic, not real people." |
| **c** | Facts checked by automated systems against independent sources | "Software checked every fact against independent sources." |
| **d** | Sources and corrections are in the show notes | "Sources, corrections and error reports are in the show notes." |
| **e** | Published by Curious & Creative LLC | "Published by Curious and Creative LLC, which is responsible for it." |

## 3. The end-of-episode scripts

Spoken by Ava. "And" replaces "&" because it is read aloud. Placeholders in `{braces}` are filled by code.

| Script | Shows | Brief's target | As drafted | Words | Est. time |
|---|---|---|---|---|---|
| **A. Daily brief** | Columbia Daily, LA Daily, NYC and Chicago Daily | ~15 s | ~16 s | 41 | 15.9 s |
| **B. Breaking** | The Breaking Desk | ~8 s | ~11 s | 29 | 11.2 s |
| **C. Crime and courts** | LA Courts Roundup, Case Tracker, Cold Case Files | ~15 s | ~22 s | 58 | 22.5 s |
| **D. Archive** | History of Hollywood | ~12 s | ~14 s | 37 | 14.3 s |
| **E. Sponsored** | any show with a sponsor | n/a | +7 s (+10 s with the ad tag) | 19 (27) | +7.3 s (+10.4 s) |

**Why some run over the brief's targets.** All five items in §2 are required, and they take about 11 seconds
at the very least (B). The crime script pays about 6 seconds for care language (`FAIR-4`, `FAIR-10`) and we
think that is worth it. To hit 8 s for Breaking, `VOICE-4` itself would have to drop an item. We recommend
against it. *(inference; founders' call)*

### A. Daily brief

> AI wrote and voiced this episode. The voices are synthetic, not real people. Software checked every fact
> against independent sources. Sources, corrections and error reports are in the show notes. Published by
> Curious and Creative LLC, which is responsible for it.

### B. The Breaking Desk

> AI wrote and voiced this report. The voice is synthetic. Software checked it against independent sources.
> Sources and corrections are in the show notes. Curious and Creative LLC publishes.

The "details may change" promise is made inside the flash, not here: every flash says what is confirmed, by whom, and what is unknown (`BRK-11`).

### C. True crime and courts (care language)

> AI wrote and voiced this episode. The voices are synthetic, not real people. Software checked every fact
> against independent sources. Anyone named is presumed innocent unless a court has ruled otherwise. We handle
> victims' stories with care. Sources, corrections and error reports are in the show notes. Published by
> Curious and Creative LLC, which is responsible for it.

The sentence about "presumed innocent" is the wording already in `disclosure.py` (`PRESUMPTION`, shortened). The care line is a promise we can keep (`FAIR-10`): no graphic detail beyond what the story needs, no minors, no sexual-assault survivors named (`NEVER-2`, `NEVER-3`).

### D. Archive (History of Hollywood)

> AI wrote and voiced this episode. The voices are synthetic, and no real person's voice was recreated.
> Software checked every claim against independent sources. Sources and corrections are in the show notes.
> Curious and Creative LLC publishes.

The "no real person's voice was recreated" clause answers the obvious question when a long-dead star is quoted. It is true only while we never synthesize a real voice (`NEVER-4`).

### E. Sponsored episodes (sponsor lines, then the normal script)

The sponsor lines come **before** the disclosure. **The disclosure (A to D) is still the last thing spoken.**

| Where | Script | Rule |
|---|---|---|
| Ad break, open | "This episode is supported by `{sponsor}`." | `COI-2`: ads sit in marked breaks, never inside a story |
| Ad break, end of read | "This ad is read by a synthetic voice." *(precaution; see §8)* | NY synthetic-performer ad law, low confidence |
| Ad break, close | "That was a message from `{sponsor}`. Sponsors never see or influence our reporting." | `COI-1` |
| Inside a story that involves a sponsor | "`{Sponsor}` is a sponsor of this network." | `COI-4` (also in show notes) |

Ad reads are announcer-style: **no personal experience, ever** ("I use it every day" is banned, `COI-3`). Insertion orders carry an "AI-voiced read" clause (legal note §10.8). Ad copy is checked separately because the Trust Stack never sees it (`COI-7`).

## 4. What the scripts do not do

- They do not apologize for being AI, and they do not oversell it ("revolutionary").
- They do not name an AI vendor or model. Vendor relationships are disclosed inside a story only when the story involves them (`COI-5`).
- They do not change by mood or by show. Wording is versioned in one place, `disclosure.py`; every episode follows it.

## 5. Metadata and platform text

Same facts as the audio, written for eyes. Placeholders: `{show}`, `{url_how}` ("How this show is made" page), `{url_err}` (the report-an-error link, `corrections_url()`).

| Surface | Text or setting |
|---|---|
| **Show description** (RSS channel, Apple, Spotify, YouTube channel) | "`{show}` is made by AI. An automated newsroom writes it, synthetic voices read it, and software checks every fact against independent sources before it airs. The voices are original and are not real people. Published by Curious & Creative LLC, which is responsible for it. How it is made, sources and corrections: `{url_how}`." |
| **Episode description, line 1** (canonical, built in `disclosure_text()`) | "This episode was written and voiced using AI. The voices you hear are synthetic, not real people. Facts were checked by automated systems against independent sources. Sources and corrections are in the show notes. `{show}` is published by Curious and Creative LLC." |
| **Crime and courts add-on** (append to the line above) | "Charges are accusations. Anyone named in connection with a criminal case is presumed innocent unless a court has ruled otherwise. If we got something wrong about you or someone you know, use `{url_err}`. Errors about named people get a dated public correction." |
| **Apple Podcasts** | The show and episode text above in the description fields, plus the spoken line. Apple asks for "prominent" disclosure in content and metadata (`F-HOST-15`). Put it first, not last: see gap `G-2`. |
| **Spotify** | Same description text. No podcast AI-label rule reported (`F-HOST-16`). Our voices are original, so the impersonation takedowns do not apply. |
| **YouTube** | Set "altered or synthetic content" to **Yes on every upload**, even where narration alone might be exempt (`DISC-7`). Line 1 of the description is the episode line above. |
| **Website footer** | "The Curious & Creative Network is produced by an automated newsroom using AI. Every voice is an original synthetic voice, not a real person. Software checks facts against independent sources. [How this is made] · [Corrections] · [Report an error]. Published by Curious & Creative LLC." |
| **Social bio** | "Automated, AI-voiced local news and stories. Not a person. Published by Curious & Creative LLC." |
| **Social post** | Ends with "AI-voiced. Sources and corrections: `{link}`". Never "our reporter", "we heard", "sources say". |
| **Replies and DMs** | "This account is automated. Curious & Creative LLC is accountable for it. Report an error: `{url_err}`." |
| **Clips and audiograms** | Caption and first on-screen frame: "AI-voiced. Synthetic voices." Link to the full episode and the disclosure. |
| **Newsletter footer** | The website footer text. |

**"How this show is made" page** (linked from every footer and show note): the Trust Stack in plain words, the six voices and that they are original, the corrections policy (note, reissue, retract), the public trust log, and this page.

## 6. Voices are original personas, not impersonations

| We say | We never say or do |
|---|---|
| "Mara is an AI host." "These voices were designed for this network." | "Sounds like…", "in the style of…", "inspired by…", the name of any real broadcaster, actor or public figure |
| A host reads a quote in the host's own voice, with the start and end signaled (`QUO-5`) | A synthetic copy of a real person's voice, even for their own words (`QUO-6`) |
| "The voices are synthetic." | A human backstory, hometown, family or credentials for a persona (`VOICE-6`) |
| For history: quotes are read by our voices | Recreating a dead performer's voice. California extended its digital-replica law to the deceased in 2025 (legal note §8; **verify**) |

Each persona has a register entry: the Voice Design prompt (verbatim), the date, the env-var name, and the resemblance check. See the [Voice & Persona Guide](voice-and-persona-guide.md) §6.

## 7. Accountability

- **Curious & Creative LLC** is the publisher of record and answers for every episode (`AUTO-1`). The page, the audio and the footer all say so.
- A mistake gets a **note**, a **reissue** or a **retraction**, dated, in public, and the next episode says it aloud (`AUTO-6`, `AUTO-7`).
- Owners can stop any show or the whole network. They cannot push an episode past the gate (`NEVER-10`).
- Anyone can report an error at `{url_err}`. It is checked against evidence, not against who is asking (`AUTO-5`).

## 8. Verify current platform policy

*As of Oct 2026 — verify before relying.* Every row can change without notice. The **Compliance & Platform Policy Watch** agent ([`agents/business-ops/compliance-policy-watch.md`](../../agents/business-ops/compliance-policy-watch.md)) owns this table. Re-check quarterly and on any platform notice.

| Surface | What we rely on | Source | Re-check |
|---|---|---|---|
| **Apple Podcasts** | Prominent AI disclosure in content and in show/episode metadata. Enforcement not evident. Older "material portion" wording exists. | `F-HOST-15` | Exact current wording. Any machine-readable AI tag. Whether an end-of-episode line counts as "prominent". |
| **Spotify** | No blanket AI ban. No podcast AI-label rule reported. "Verified by Spotify" badges and removal of impersonating shows (2026-05-19). | `F-HOST-16` | Whether a podcast AI-label field now exists. |
| **YouTube** | Synthetic-content setting since 2024-03-18, shown more prominently on news topics (legal note §7). July 2025 "inauthentic content" rule hits mass-produced, repetitive channels. | `F-LEGAL-13`, `F-HOST-13` | Rules for synthetic *narrators* (not just impersonation). A disclosure does not protect a repetitive channel. |
| **Distribution partners** | iHeartMedia's "Guaranteed Human" pledge: no AI on-air voices on what it publishes. Third-party Spreaker shows: unknown. | `F-HOST-17` | Whether any partner or ad network excludes synthetic shows. |
| **EU AI Act Art. 50** | Applies from 2026-08-02. Fines up to EUR 15M or 3% of turnover. Our voices are not deepfakes of real people. A fully automated pipeline cannot use the human-review exception *(inference)*. | `F-LEGAL-13` | Code of practice. Whether the disclosure must come at first exposure, not at the end: our metadata line is visible before play, which helps *(inference; **[LAWYER]**)*. |
| **California SB 942** | Binds AI vendors with 1M+ monthly users, not us. Operative 2026-08-02. Our duty is indirect: never strip provenance marks. | `F-LEGAL-13` | Dates and scope. |
| **FTC and NY ad rules** | Material connections are disclosed in the audio. An AI host never claims personal use. NY synthetic-performer ad disclosure: reported, low confidence. | legal note §6.3 | NY effective date. Whether the "synthetic voice" ad tag (§3E) is required or enough. **[LAWYER]** |

## 9. Not yet in code

| # | Gap | Proposed fix |
|---|---|---|
| **G-1** | `disclosure.py` speaks a longer form: 101 to 112 words, about 39 to 43 s, with three variants (daily, breaking, archive), plus 17 words on strict-lane shows. This page defines shorter scripts A to E. | Replace `VARIANTS`, add the crime wording, update tests, in one change (`AUTO-9`). Until then the long form airs. |
| **G-2** | `feed.py` appends the disclosure at the **end** of an item description and the show description. Platform previews cut off the end. | Put the disclosure sentence first in the description. |
| **G-3** | Position, metadata presence and speaker are unchecked (`NE-1`, `NE-2`, `NE-3`). | Gate `S2`, `S3`, `S4` as proposed in Editorial Standards §17. |
| **G-4** | No sponsor registry or ad segment, so sponsor lines in §3E are not yet inserted (`NE-12`). | `config/sponsors.yaml`, an `ad` segment, `S6`. |
| **G-5** | YouTube packager says the setting is applied "as policy requires", not "always". Clip labels (`DISC-9`) are not specified in the clip maker. | Update `agents/distribution/youtube-packager.md` and `clip-maker.md`. |

| Date | Version | Change |
|---|---|---|
| 2026-10-12 | 1.0 | First edition: ten rules, five scripts, platform text, verify table. |
