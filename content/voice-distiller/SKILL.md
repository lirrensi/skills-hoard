---
name: voice-distiller
description: Distill a living VOICE.md from a large body of writing, then iteratively refine it in the same session as new samples or corrections arrive. Use when the user dumps articles, posts, drafts, comments, transcripts, or mixed writing and wants a reusable voice document rather than a one-off style summary.
---

# Voice Distiller

This skill turns a pile of real writing into a **living `VOICE.md`**.

It is not just extraction. It is **distillation + refinement**:

1. read a large corpus
2. separate true voice from context noise
3. draft a voice document
4. refine that document as more samples, corrections, and edge cases appear

Use it when the user says things like:

- “Here’s a dump of my articles—figure out my voice.”
- “Make me a reusable voice guide.”
- “Refine this VOICE.md based on more writing.”
- “Extract my style without making it sound like AI.”
- “Keep iterating until the voice doc feels right.”

---

## Core Philosophy

The job is **not** to invent a persona. The job is to **compress recurring reality**.

That means:

- prefer repeated patterns over flashy one-offs
- separate voice from topic, platform, and editing artifacts
- mark weak signals as tentative instead of pretending certainty
- refine the document in-place instead of rewriting it from scratch every pass

The result should feel like:

> “Yeah, that’s actually how I sound when I’m writing well.”

Not:

> “This is a cute horoscope wearing my jacket.”

---

## Default Mode

**Default behavior:**

- If a `VOICE.md` already exists, **refine it**.
- If no `VOICE.md` exists, **create a first draft** from the corpus.

This skill is meant for a long, thoughtful session where extraction and refinement happen together.

---

## Inputs

Collect or infer these before distilling:

- **Writing corpus** — articles, essays, posts, comments, transcripts, emails, notes, drafts
- **Existing `VOICE.md`** (optional but preferred for refinement)
- **Primary use context** (recommended) — personal essays, technical documentation, political writing, marketing copy, mixed use, etc.
- **Target use** (optional) — AI prompting, editing benchmark, ghostwriting, personal reference
- **Known anti-patterns** (optional) — words/tones the user already hates
- **Known audience split** (optional) — broad internet audience, clients, technical peers, etc.

If the user gives a giant dump with little explanation, proceed anyway. State assumptions and start with a corpus audit.

---

## Corpus Quality Gates

Before extracting, assess the source material.

### 1. Source Type Weighting

Weight sources roughly like this:

1. casual but genuine writing
   - comments
   - emails
   - transcripts
   - rough drafts
2. personal essays / long-form posts
3. polished articles
4. landing pages / marketing copy / obviously edited material

Heavily edited writing is still useful, but it should not dominate the conclusions.

### 2. Exclusions

Exclude or downweight:

- platform formatting tics
- SEO filler
- titles/headlines written in a different register
- quotes from other people
- obvious experiments that do not recur
- typos and accidental repetition

### 3. Sample Sufficiency

If the material is thin, say so clearly.

- under ~500 words: too thin for a reliable guide; produce only a provisional snapshot
- 500–1500 words: workable but limited
- 1500+ words across multiple pieces: solid
- large corpus: ideal for full distillation

Always report confidence honestly.

---

## Distillation Workflow

Follow this order.

### Phase 1: Corpus Audit

Output a short assessment:

- how much material exists
- what kinds of material it is
- which samples are strongest for authentic voice
- what will be excluded or downweighted
- whether this is a first-pass distillation or refinement pass

### Phase 2: Stable Pattern Extraction

Extract patterns that recur across the corpus:

- primary use context cues
- delivery mode
- opening habits
- transition habits
- emphasis moves
- ending habits
- sentence rhythm
- paragraph size
- diction level
- formality / informality
- humor / irony / snark / warmth
- degree of certainty
- abstraction vs concreteness
- use of examples, stories, lists, and asides

Quote exact evidence where possible.

For **primary use context**, identify what kind of writing situation the voice seems optimized for:

- personal / reflective
- technical / explanatory
- political / polemical / manifesto-like
- marketing / persuasive
- mixed

This is not mainly about audience demographics. It is about which signals the writer relies on most in practice.

For **delivery mode**, identify whether the voice is primarily:

- conversational / speakable
- written-first / editorial
- performative / rallying
- procedural / instructional
- hybrid

This helps define how the voice carries force without turning the skill into a writing-advice system.

### Phase 3: Separate Stable Voice from Context Noise

For each pattern, decide whether it is:

- **canonical** — strong recurring signal across contexts
- **probable** — appears often, but not everywhere
- **tentative** — interesting, but weak or context-bound

Never promote a weak signal to a hard rule just because it sounds clever.

### Phase 4: Draft or Refine `VOICE.md`

If no `VOICE.md` exists:

- create one from the template in this skill

If a `VOICE.md` exists:

- preserve stable sections
- sharpen vague claims
- merge duplicates
- remove unsupported rules
- add stronger examples
- demote overconfident claims to tentative ones when needed

### Phase 5: Validation

Generate a small validation pack:

- **sounds like you** example
- **doesn’t sound like you** contrast example
- **what changed** in the latest refinement pass
- **open questions** where confidence is still low

Then ask for correction:

> “What feels dead-on, what feels fake, and what feels overclaimed?”

### Phase 6: Iterative Refinement Loop

When the user adds more writing or feedback, do **targeted updates**, not a full rewrite.

For each new pass:

1. compare new material against current `VOICE.md`
2. confirm what strengthens existing rules
3. note what contradicts them
4. revise only the affected sections
5. append a short update note

Keep going until returns diminish.

---

## Evidence Rules

These rules keep the skill from making shit up.

### A. Every strong claim needs evidence

Whenever possible, support rules with:

- repeated examples
- quoted phrases
- cross-context recurrence

### B. Do not confuse topic with voice

If the user writes about serious topics, do not assume the voice is “serious.”
Look for how they explain, pivot, joke, qualify, insist, and land points.

### C. Do not confuse polish with authenticity

Clean writing may hide the real rhythm. Messier writing often reveals it.

### D. Preserve contradictions when they are real

Some writers are both:

- warm and blunt
- casual and precise
- skeptical and generous
- structured and conversational

Good voice docs preserve that tension instead of flattening it.

---

## What the `VOICE.md` Should Include

Use the bundled template as the base structure.

At minimum, the output document should contain:

1. **Core Identity**
   - one-paragraph summary of the voice
   - natural role (teacher, challenger, guide, etc.)
   - default energy

2. **Primary Use Context**
   - the main writing situation this voice is optimized for
   - what signals matter most in that context

3. **Delivery Mode**
   - whether the voice is conversational, editorial, performative, procedural, or hybrid
   - how that affects rhythm, force, and texture

4. **Reader Relationship**
   - how the writer relates to the reader
   - peer, guide, translator, provocateur, companion, etc.

5. **Rhythm & Structure**
   - sentence length tendencies
   - paragraph habits
   - opening/transition/ending habits
   - use of lists, questions, fragments, asides

6. **Diction & Register**
   - plainspoken vs elevated
   - slang/casuality level
   - favorite word types
   - banned or unnatural phrases

7. **Signature Moves**
   - recurring rhetorical moves
   - e.g. reframing, contrast, direct address, concrete examples, mini-rants, admissions, callbacks

8. **Confidence Calibration**
   - what topics get full authority
   - what topics get earned perspective
   - what topics stay exploratory

9. **Anti-Patterns**
   - words, tones, and structures that feel fake

10. **Evidence & Examples**
   - exact excerpts or paraphrased evidence
   - not just vibes

11. **Open Questions**
   - unresolved tensions or unclear signals

12. **Refinement Log**
    - what changed in each pass

13. **AI Prompt Block**
    - compact prompt-ready summary for reuse

---

## Required Behaviors

### When creating the first draft

- build a usable `VOICE.md`, not a loose summary
- include confidence labels where uncertainty exists
- prefer a compact, readable artifact over bloated theory
- favor definitions that are easy to apply later because they are clear, non-contradictory, and free of meaningless buzzwords

### When refining an existing `VOICE.md`

- do not rewrite sections that still hold up
- highlight what changed and why
- remove claims that are not supported by the expanded corpus
- improve examples before inventing new categories

### When evidence conflicts

- preserve the contradiction if it appears genuine
- otherwise split by context, such as:
  - essays
  - casual posts
  - technical explanations
  - argumentative writing

---

## Output Format

After analysis, return:

1. a short corpus audit
2. the drafted or refined `VOICE.md`
3. a concise refinement summary:
   - added
   - sharpened
   - downgraded
   - removed
   - still uncertain

---

## Boundaries

This skill is great for:

- distilling a voice from many articles or posts
- refining a living voice document over time
- preparing a reusable style reference for AI or editors

This skill is not for:

- inventing a new fake persona from scratch
- rewriting content into the extracted voice automatically
- deriving hard rules from tiny sample sets and pretending certainty

If the user wants actual rewriting after the voice is distilled, use the resulting `VOICE.md` as the input contract for writing or editing work.
