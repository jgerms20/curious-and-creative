# Voice & Persona Guide

**The Curious & Creative Network: who our six hosts are, how they sound, and how to write for them**

| | |
|---|---|
| **Publisher** | Curious & Creative LLC |
| **Applies to** | Every script, every voice render, every new persona |
| **Source of truth** | [`config/voices.yaml`](../../config/voices.yaml) (personas, roles, `disclosure_voice`) and [`config/shows.yaml`](../../config/shows.yaml) (who hosts what) |
| **Parent rules** | [Editorial Standards](editorial-standards.md) §14 `VOICE-1`–`VOICE-6`, `NEVER-4`, `NEVER-7`; [AI Disclosure](ai-disclosure.md) |
| **Owners** | `voice-director` (personas, status `next`), `pronunciation-keeper` (lexicon, `next`), `copy-editor` (script style, `next`) |
| **Version** | 1.0, October 12, 2026 |

> **How to read this page.** Pace figures, prompt wording and style targets are things we reasoned out, not
> measured results *(inference)*. Tune them by listening. Every respelling in §5 is from memory and must pass
> a source-confirmed listen check before it ships (P-3, P-4); **?** marks the least certain. "Legal note" means
> [legal-compliance-business-setup](../research/notes/legal-compliance-business-setup.md). Words in `code` are rule ids.

---

## 1. The cast at a glance

| Persona | Role (`voices.yaml`) | Shows | Voice env var |
|---|---|---|---|
| **Mara** | anchor | Columbia Daily; NYC Daily (wave 1, off) | `VOICE_MARA` |
| **Theo** | co-host | Columbia Daily; Case Tracker; Chicago Daily (wave 1, off) | `VOICE_THEO` |
| **Lena** | anchor | LA Daily; History of Hollywood; Chicago Daily (wave 1, off) | `VOICE_LENA` |
| **Marcus** | co-host | LA Daily; NYC Daily (wave 1, off) | `VOICE_MARCUS` |
| **Ava** | breaking_anchor | The Breaking Desk; **speaks the AI disclosure on every show** (`disclosure_voice`) | `VOICE_AVA` |
| **June** | courts_and_crime | LA Courts Roundup; Cold Case Files; Case Tracker | `VOICE_JUNE` |

**Three ground rules for every persona.**
1. **Voices, not lives.** A persona has a sound and a manner. It has no hometown, family, commute, coffee or credentials. Age words in a prompt describe sound only (`VOICE-6`, `NEVER-7`).
2. **Original, always.** No persona is modeled on, named after or imitating a real person (`VOICE-1`, `NEVER-4`). First names only, no surnames.
3. **Opinions stay out.** Warmth and curiosity are fine. Opinions on contested questions never are (`FAIR-9`).

## 2. Persona cards

Pace is a target in words per minute (the studio estimates 155; `F-TTS-15` uses 150). *(inference)*

| Persona | Sound and manner | Pace | Hands off to | Never |
|---|---|---|---|---|
| **Mara** | Warm, brisk, Southern-neutral morning voice. Opens the day with the date and the top line. Light touch on light stories only. | ~160, quick starts, short sentences | Theo (Columbia), Marcus (NYC). Cues the "why" or "what's the catch?" | Joke on a crime, death or court story. Claim a commute or a hometown. |
| **Theo** | Curious, conversational. Asks the question a listener would ask, at most one per story. | ~155, interest rises on questions | Takes the cue from Mara, June or Lena, asks, then hands back | Give an opinion. State a fact inside a question. Wonder aloud ("I wonder if…", `NEVER-1`). |
| **Lena** | Clear, cinematic, West Coast. Crisp and civic on LA Daily. Unhurried storyteller on History of Hollywood. | ~150 (~145 in History) | Marcus on LA Daily. Solo on History. | Dramatize past the record. Invent scene detail. Pass off a legend as fact (`FAIR-12`). |
| **Marcus** | Grounded. Explains the why in plain words: what changed, who it touches, what the record says is next. | ~150, even | Takes the cue from Lena or Mara | Speculate. His "why" is sourced context or an attributed explanation, never his own theory. |
| **Ava** | Calm under pressure, precise, no hype. A flash always runs Confirmed, By whom, Not yet known (`BRK-11`). As disclosure voice, a neutral, steady close. | ~150, even, never rushed | Solo. Takes the show's last beat for the disclosure | Alarm words. Name a suspect or the dead before an official release (`BRK-9`, `BRK-10`). |
| **June** | Measured, careful with names and allegations. Pauses before a name or a legal term. Warm, serious, never theatrical. Treats victims as people. | ~140, deliberate | Theo on Case Tracker: June gives status, Theo asks "what happens next", June answers only from the docket | Dramatic pauses on an accusation. "Alleged killer". Adjectives about a defendant (`FAIR-10`). |

### Handoff rules

- **H-1.** A handoff line carries **no new fact**. It is a cue ("Theo, what should people know?"). Facts live only in lines tied to claims (`ACC-1`).
- **H-2.** Questions never state a fact or hint at a conclusion. A co-host's answer comes only from sourced claims.
- **H-3.** At most one handoff per story. A story under 30 seconds stays in one voice.
- **H-4.** The lead host opens and closes the show. Hosts use first names and the show name, nothing more ("This is Columbia Daily, with Mara and Theo").
- **H-5.** The switch to the disclosure is a short pause and a soft transition sound. Ava speaks it even on shows she does not host (`DISC-2`).

## 3. Tone by lane

| Lane (shows) | Register | Do | Don't | Sound |
|---|---|---|---|---|
| **standard** (Columbia Daily, LA Daily) | Warm, brisk, conversational. Contractions are fine. | Light humor on weather, sports, culture. Name the neighborhood. | Levity near any crime, death, court or accident story. Loaded verbs ("slams", `ATT-6`). | Licensed bed under open and close, out under speech |
| **strict** (Courts Roundup, Case Tracker, Cold Case Files) | Measured, plain, slower. Attribute first: "Prosecutors allege…". | Full titles on first mention. Say what is not yet known. | "Brutal", "chilling", "monster". Teasers, cliffhangers, rhetorical questions about guilt. A victim as a plot device (`FAIR-10`). | No music stings on an accusation or a victim's name. Quiet bed or none |
| **breaking** (The Breaking Desk) | Flat-calm, short declaratives, time-stamped ("as of 3 p.m. Eastern", `BRK-8`). | "Here is what is confirmed." Then who confirmed it. Then what is unknown. | "Developing", "sources say", "reportedly" with no outlet (`ATT-7`). Any guess. | No bed under facts. One short alert tone at most |
| **archive** (History of Hollywood) | Narrative, scene-setting from records. | Label legends ("the story studio publicists told was…", `FAIR-12`). Say "not adjusted for inflation" (`NUM-5`). | Invented dialogue or thoughts. Recreated voices (`NEVER-4`). Film clips (`COPY-7`). | Period-flavored music only if licensed or original (`COPY-6`) |

## 4. Writing for the ear

Listeners cannot re-read. The Copy Editor applies these after the Producer writes.

| Rule | Do | Don't |
|---|---|---|
| **One idea a sentence** | Aim for under 20 words. Subject, verb, object. | Stack clauses with commas, dashes or parentheses. TTS cannot voice a parenthesis. |
| **Attribution first** | "Police said a man was hurt." (`ATT-1`) | "A man was hurt, according to police, in a crash on…" |
| **Numbers as spoken** | "About four million." "Three p.m. Eastern." Round only so the direction word stays true (`NUM-3`). | More than two numbers in a sentence. "$4.2M", "3/14", "%", "#", "&" in script text. |
| **Source, unit, period** | "The county recorded 412 crashes last year, state data show." (`NUM-2`) | A bare figure. |
| **Names** | Full name and title once, then the short form. | Strings of names. Two similar names close together. |
| **Addresses** | "The eleven-hundred block of Gervais Street." | "1100 Gervais St." |
| **Abbreviations** | Spell out on first use. Letters for LAPD, DA. Words for NASA. Put new ones in the lexicon. | Any abbreviation a listener must decode. |
| **Quotes** | Short, verbatim, signaled: "In her words… end quote." Read in the host's voice (`QUO-5`, `QUO-6`). | A quote that starts or ends without a cue. |
| **Time words** | True at air time, in the show's time zone (`ACC-10`). | "Today" in an episode that airs tomorrow. |
| **Signposts** | "Three things to know." "Next:" Lists of three or fewer. | A list of five the ear cannot hold. |
| **Say it once, then once more** | End a story on the one thing to remember. Repeat it, not new facts. | A closing line that adds a claim without a `claim_id`. |
| **No fake humanity** | Plain delivery. | "Um", "you know", fake breaths or stumbles, "I was there", "I spoke with" (`NEVER-7`). |
| **Punctuation for prosody** | Periods and commas. Short sentences make pauses. | Exclamation marks, ALL CAPS, emoji, markdown, ellipses. |
| **Length** | About 1,000 characters (about 150 words) a minute (`F-TTS-15`). A 7-minute brief is about 7,000 characters. | Padding to hit a runtime. A short episode is fine. |

## 5. Pronunciation

A mispronounced street tells a local listener we are not from there. The goal is zero, and a log that shows we are getting there.

### The practice

- **P-1. One lexicon per market,** at `config/lexicon/<market>.yaml` *(proposed path; not yet created)*. Loaded into the voice engine's pronunciation dictionary before every render. Test that the chosen voice model honors dictionaries before relying on it (as of Oct 2026 — verify against ElevenLabs docs).
- **P-2. Alias first.** Replace the written word with a plain-English respelling the engine says correctly. This works across models. Use phoneme (IPA) rules only where a model supports them *(recall; verify)*.
- **P-3. Every entry records:** written form (exact case), respelling, source, date, listen-check pass or fail, status `confirmed` or `unconfirmed`.
- **P-4. Sources, best first:** the institution's own audio or guide; a local broadcaster's recorded on-air use; a city or county guide; a native-speaker listen by a founder. We never phone anyone to ask (`NEVER-7`).
- **P-5. Unconfirmed names:** say the most common way, mark `unconfirmed`, fix on the first flag. If the name belongs to a private person and the story works without it, leave it out (`FAIR-6`).
- **P-6. Every flag becomes an entry** (`event:qa.mispronunciation` from the QA Listener, or a listener report) **and a regression render** of the same sentence.
- **P-7. Always in the lexicon:** "LLC" (L L C), "AI" (A I), every host name, every show name.
- **P-8. History of Hollywood** adds entries per episode for archaic or foreign names from reference sources (for example DeMille: duh-MILL). Film titles are read as titles.

### Columbia, Richland and Lexington (starter entries, proposed)

In South Carolina the prosecutor is the **solicitor**, not the "DA". Say it, do not translate it.

| Written | Say it | Written | Say it |
|---|---|---|---|
| Columbia | kuh-LUM-bee-uh | Richland | RITCH-lund |
| Lexington | LEK-sing-tun | Congaree | KON-guh-ree |
| Saluda | suh-LOO-duh | Cayce | KAY-see |
| Irmo | ER-moh | Chapin | CHAY-pin |
| Blythewood | BLY-thwood **?** | Devine Street | duh-VINE **?** |
| Gervais Street | jer-VAYS **?** | Huger Street | HYOO-jee **?** |
| Lugoff | LOO-gawf **?** | Swansea | SWAN-zee **?** |

### Los Angeles (starter entries, proposed)

Say "district attorney" in full on first mention, then "the DA's office".

| Written | Say it | Written | Say it |
|---|---|---|---|
| Los Angeles | los AN-juh-lus | Los Feliz | los FEE-liss |
| Cahuenga | kuh-WENG-guh | Tujunga | tuh-HUNG-guh |
| Sepulveda | seh-PUL-vuh-duh | La Cienega | la sy-EN-uh-guh |
| La Brea | la BRAY-uh | Figueroa | fig-uh-ROH-uh |
| Pico | PEE-koh | Reseda | ruh-SEE-duh |
| Encino | en-SEE-noh | Van Nuys | van NICE |
| Pacoima | puh-COY-muh | Canoga Park | kuh-NOH-guh |
| Topanga | tuh-PANG-guh | Azusa | uh-ZOO-suh |
| El Segundo | el seh-GUN-doh | Crenshaw | CREN-shaw |
| Foltz (courthouse) | FOLTS | Roybal (federal building) | ROY-bal |

## 6. Voice Design: creating original voices

Voices are made with ElevenLabs Voice Design on a **paid plan with a commercial license** (Free has none, `F-TTS-01`; Starter and up do, `F-TTS-02`). Plan limits for Voice Design and custom-voice slots are not confirmed (open item in the facts sheet; as of Oct 2026 — verify before buying).

### Prompt rules

1. **Describe sound, never a person.** Allowed: age range, accent family, pitch, pace, warmth, energy. Banned: any name, character, show, brand, "sounds like", "in the style of", "reminiscent of".
2. **One prompt per persona,** saved verbatim in the voice register.
3. **Generate several previews, pick one, lock it.** Never regenerate to "improve" a locked voice; a new generation is a different voice.
4. **Resemblance check before locking.** Two founders listen to the final three candidates once (setup step, not an episode gate). Reject any that calls a specific known voice to mind. Record the result.
5. **Contrast check.** The six must be easy to tell apart. Mara and Lena differ in accent and age. Ava and June differ in pitch and pace.
6. **Name check per market** before launch: first name only, no collision with a working broadcaster in Columbia or Los Angeles.

### Starting prompts

Each ends with "Clean studio recording, no background noise."

| Persona | Voice Design prompt |
|---|---|
| **Mara** | A woman who sounds mid-thirties, with a warm, bright, Southern-neutral American accent and no heavy drawl. Brisk, friendly morning-news delivery, clear consonants, a light smile in the voice, steady mid-range pitch. Confident, never breathless or sing-song. |
| **Theo** | A man who sounds around thirty, general American accent with no strong regional markers. Relaxed, curious and conversational, with natural rising interest when he asks a question. Medium-low pitch, friendly, unforced. |
| **Lena** | A woman who sounds early forties, with a clear, polished West Coast American accent. Smooth, unhurried storyteller cadence with gentle emphasis on key words. Low-mid pitch, rich but not breathy. |
| **Marcus** | A man who sounds mid-forties, with a warm, steady baritone and a neutral American accent with easy West Coast warmth. Patient, plain-spoken, even pace, reassuring without being stern. |
| **Ava** | A woman who sounds late thirties, with a neutral American accent. Calm, precise, crisp articulation, even low-mid pitch, no emotional coloring and no hype. Focused and steady under pressure. |
| **June** | A woman who sounds early fifties, soft-spoken but clear, with a neutral American accent. Slow, deliberate pacing with clean pauses. Warm but serious, low-mid pitch, never theatrical. |

### Voice register (one row per persona, kept by `voice-director`)

Persona · prompt (verbatim) · date designed · env-var name (never the ID's value in a doc) · TTS model and voice settings used · resemblance-check result and who listened · name-check result · status. This is the record that shows each voice is ours (legal note §8, recommendation 1).

## 7. Not yet in place

| # | Gap | Fix |
|---|---|---|
| **V-1** | No persona bibles exist yet (`docs/shows/bibles/` is empty). | `voice-director` writes one per persona from §2 and §6. |
| **V-2** | No lexicon files; `pronunciation-keeper` and the QA Listener are status `next`. | Create `config/lexicon/columbia-sc.yaml` and `los-angeles.yaml` from §5. |
| **V-3** | No voice register, and no resemblance or name check on record. | Run §6 rules 4 and 6, then fill the register. |
| **V-4** | No dedicated sponsor-read voice. The agent catalog plans one (`voice-director`, `future`). Until then, ad reads are announcer-style and stay out of Ava's and June's voices *(inference)*. | Design a non-news voice under §6. |
| **V-5** | `voices.yaml` has no per-persona pace or voice settings. | Add `speed` and stability fields once the engine call supports them. |

| Date | Version | Change |
|---|---|---|
| 2026-10-12 | 1.0 | First edition: six personas, handoffs, lane tone, ear style, lexicon practice, Voice Design prompts. |
