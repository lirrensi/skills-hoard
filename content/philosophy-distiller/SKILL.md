---
name: philosophy-distiller
description: Distill a living PHILOSOPHY.md from a large body of writing, then iteratively refine it in the same session as new samples or corrections arrive. Use when the user dumps essays, posts, comments, drafts, transcripts, or mixed writing and wants a reusable worldview document rather than a one-off topic summary.
---

# Philosophy Distiller

This skill turns a pile of real writing into a **living `PHILOSOPHY.md`**.

It is not just extraction. It is **distillation + refinement**:

1. read a large corpus
2. separate recurring convictions from context noise
3. draft a philosophy document
4. identify recurring bullshit patterns, evasions, and coherence failures
5. crystallize the worldview into memorable, evidence-earned lines
6. refine that document as more samples, corrections, and edge cases appear

Use it when the user says things like:

- “Here’s a dump of my essays—figure out what I keep believing.”
- “Extract my worldview from all this writing.”
- “Refine this PHILOSOPHY.md based on more samples.”
- “Tell me what I’m always arguing for and against.”
- “Map the themes, values, tensions, and obsessions that actually recur.”

---

## Core Philosophy

The job is **not** to psychoanalyze the writer. The job is to **compress recurring reality**.

That means:

- prefer repeated commitments over flashy one-off declarations
- separate worldview from topic, platform, mood, and debate-specific rhetoric
- notice where the writer regularly cheats, hedges, overreaches, or hides
- when helpful, connect the worldview to existing thinkers, traditions, or concept clusters instead of reinventing familiar ideas in flatter language
- mark weak signals as tentative instead of pretending certainty
- refine the document in-place instead of rewriting it from scratch every pass

The result should feel like:

> “Yeah, that’s actually what I keep trying to say about the world.”

and also:

> “Yeah, fuck, that is exactly how I bullshit when I haven’t fully earned the claim.”

Not:

> “This is a Pinterest mood board for my opinions.”

---

## Default Mode

**Default behavior:**

- If a `PHILOSOPHY.md` already exists, **refine it**.
- If no `PHILOSOPHY.md` exists, **create a first draft** from the corpus.

This skill is meant for a long, thoughtful session where extraction and refinement happen together.

---

## Inputs

Collect or infer these before distilling:

- **Writing corpus** — essays, articles, posts, threads, comments, transcripts, notes, drafts, manifestos, explainers
- **Existing `PHILOSOPHY.md`** (optional but preferred for refinement)
- **Primary use context** (recommended) — essays, political writing, technical criticism, cultural commentary, mixed use, etc.
- **Target use** (optional) — AI prompting, editorial guidance, worldview mapping, archive/reference
- **Known convictions** (optional) — beliefs the user already claims as core
- **Known anti-positions** (optional) — positions, vibes, or frameworks the user rejects

If the user gives a giant dump with little explanation, proceed anyway. State assumptions and start with a corpus audit.

---

## Corpus Quality Gates

Before extracting, assess the source material.

### 1. Source Type Weighting

Weight sources roughly like this:

1. casual but genuine writing
   - comments
   - transcripts
   - notes
   - rough drafts
2. long-form essays / posts
3. polished articles
4. commissioned copy / heavily constrained writing / debate performances aimed at an external frame

Highly edited or strategically constrained material is still useful, but it should not dominate the conclusions.

### 2. Exclusions

Exclude or downweight:

- platform formatting tics
- SEO filler
- quotes from other people presented without endorsement
- arguments made only to answer a narrow prompt and not seen elsewhere
- obvious experiments that do not recur
- ironic posturing with no supporting pattern

### 3. Sample Sufficiency

If the material is thin, say so clearly.

- under ~500 words: too thin for a reliable worldview guide; produce only a provisional snapshot
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
- which samples are strongest for authentic convictions
- what will be excluded or downweighted
- whether this is a first-pass distillation or refinement pass

### Phase 2: Stable Pattern Extraction

Extract patterns that recur across the corpus:

- primary use context cues
- central questions
- recurring themes
- moral instincts
- sacred values
- recurring enemies / targets / irritants
- favored explanations
- assumptions about human nature
- assumptions about power, institutions, truth, agency, obligation, freedom, dignity, beauty, progress, or decline
- what tradeoffs the writer repeatedly chooses
- where emotional intensity spikes and why
- where reasoning quality repeatedly drops
- where the writer goes vague, performative, evasive, inflated, or prematurely certain
- which thinkers, traditions, schools, or concept families the writing most plausibly resonates with

Quote exact evidence where possible.

Where genuinely clarifying, map the worldview to existing intellectual frames such as:

- thinkers
- schools of thought
- traditions
- ideological lineages
- named concepts

Examples of the type of move:

- “closest to a disappointed Locke with anarchist tendencies”
- “more Simone Weil in moral mood than Marxist in method”
- “civilizationally conservative, but psychologically closer to existentialism than Burkean comfort”

Use these mappings to enrich the read, not to cosplay intelligence.

For **primary use context**, identify what kind of writing situation the philosophy seems optimized for:

- reflective / essayistic
- political / polemical / manifesto-like
- analytical / explanatory
- cultural criticism
- strategic / persuasive
- mixed

This is not mainly about audience demographics. It is about which intellectual and moral signals matter most in practice.

For **delivery mode**, identify whether the philosophy is usually carried through:

- reflective / exploratory
- declarative / thesis-driven
- combative / oppositional
- constructive / prescriptive
- diagnostic / analytical
- hybrid

This helps define how conviction is expressed without collapsing into generic writing advice.

### Phase 3: Separate Stable Philosophy from Context Noise

For each pattern, decide whether it is:

- **canonical** — strong recurring signal across contexts
- **probable** — appears often, but not everywhere
- **tentative** — interesting, but weak or context-bound

Never promote a weak signal to a hard rule just because it sounds profound.

Also separate:

- **core belief** — the thing the writer actually seems to mean
- **habitual overreach** — the place where they claim too much
- **evasion pattern** — the place where they stop saying the sharp thing plainly
- **borrowed intensity** — the place where rhetoric outruns substance

### Phase 4: Draft or Refine `PHILOSOPHY.md`

If no `PHILOSOPHY.md` exists:

- create one from the template in this skill

If a `PHILOSOPHY.md` exists:

- preserve stable sections
- sharpen vague claims
- merge duplicates
- remove unsupported rules
- add stronger evidence
- demote overconfident claims to tentative ones when needed

### Phase 5: Crystallization

Create a top-of-document compression layer that can act as both summary and vibe check.

Include:

- **Philosophy Crystal** — 1–3 lines capturing the worldview in compressed, memorable form
- **Failure Crystal** — 1–2 lines capturing the most recurring self-deception or coherence failure
- **Thinker / Tradition Anchors** — closest-fit references to existing thinkers, schools, or concepts

Rules for crystallization:

- compression must be earned by the evidence, not just sound cool
- prefer specificity over generic elegance
- use existing thinkers or traditions when they genuinely clarify the pattern
- if a thinker comparison is only partial, say so
- if no single anchor fits, give 2–3 partial anchors instead of forcing a fake synthesis
- if evidence is too thin, produce candidate crystal lines rather than pretending certainty

### Phase 6: Validation

Generate a small validation pack:

- **yes, that tracks** summary of the strongest commitments
- **doesn’t track** contrast claims the corpus does not support
- **bullshit detector** summary of the most recurring failure modes
- **crystal check** whether the compression lines feel true, sharp, and memorable
- **what changed** in the latest refinement pass
- **open questions** where confidence is still low

Then ask for correction:

> “What feels dead-on, what feels fake, and what feels overclaimed?”

### Phase 7: Iterative Refinement Loop

When the user adds more writing or feedback, do **targeted updates**, not a full rewrite.

For each new pass:

1. compare new material against current `PHILOSOPHY.md`
2. confirm what strengthens existing claims
3. note what contradicts them
4. revise only the affected sections
5. append a short update note

Keep going until returns diminish.

---

## Evidence Rules

These rules keep the skill from making shit up.

### A. Every strong claim needs evidence

Whenever possible, support claims with:

- repeated examples
- quoted phrases
- recurring judgments
- cross-context recurrence

The same rule applies to negative judgments about the writer's reasoning. If you say they often dodge, overclaim, or hide behind abstraction, point to repeated evidence.

The same rule also applies to thinker or tradition comparisons. If you compare the writer to Locke, Weil, Nietzsche, Marx, Ellul, Lasch, or whoever else, the fit should be traceable to recurring patterns, not just aesthetic vibes.

### B. Do not confuse topic with philosophy

If the user writes about politics, technology, religion, culture, gender, or institutions, do not assume the philosophy is just those topic labels.
Look for the judgments, values, hierarchies, fears, loyalties, and preferred explanations that keep returning.

### C. Do not confuse emotional intensity with core belief

A dramatic rant may be memorable without being central. Repetition beats drama.

### D. Track recurring bullshit patterns without turning into a scold

Look for patterns like:

- vague abstractions where a concrete claim should exist
- complexity language used to avoid commitment
- certainty performed before argument is earned
- rhetorical force replacing reasoning
- selective nuance used only when a claim becomes inconvenient
- favorite conclusions reached faster than the evidence warrants

Name the pattern cleanly. Do not moralize or diagnose the soul.

### E. Preserve contradictions when they are real

Some writers are both:

- elitist and populist
- skeptical and idealistic
- anti-institutional and hungry for order
- compassionate and punitive

Good philosophy docs preserve that tension instead of flattening it.

### F. Distinguish diagnostic claims from normative claims

Separate:

- what the writer thinks **is true**
- what the writer thinks **is good**
- what the writer thinks **should be done**

Do not blur those together.

### G. Distinguish incoherence from development

Not every contradiction is hypocrisy or bullshit.

Sometimes the writer is:

- genuinely changing their mind
- testing a frame
- speaking differently across contexts for legitimate reasons

Only call it a bullshit pattern when the evasion or overreach itself recurs.

### H. Use thinker references as compression tools, not as substitute reasoning

Good:

- “closest to civic republicanism with anti-bureaucratic instincts”
- “moral psychology closer to Weil than to utilitarian reformism”

Bad:

- random philosopher name-dropping with no explanatory gain
- forcing a neat lineage where the corpus is obviously mixed
- pretending the writer has read or endorsed the thinker being used as an anchor

---

## What the `PHILOSOPHY.md` Should Include

Use the bundled template as the base structure.

At minimum, the output document should contain:

1. **Core Orientation**
    - one-paragraph summary of the worldview
    - default moral/intellectual posture
    - what this writer seems fundamentally for and against

2. **Crystal Layer**
   - a top-of-file compression of the worldview
   - a top-of-file compression of the failure mode
   - closest thinker / tradition / concept anchors

3. **Primary Use Context**
    - the main writing situation this philosophy is optimized for
    - what signals matter most in that context

4. **Delivery Mode**
    - whether the philosophy is reflective, declarative, combative, constructive, diagnostic, or hybrid
    - how that affects force, clarity, and interpretive risk

5. **Central Questions**
    - what questions the writer keeps circling

6. **Core Commitments**
    - recurring beliefs and values

7. **Moral Instincts**
    - how the writer tends to judge actions, people, systems, and tradeoffs

8. **Recurring Themes & Obsessions**
    - what topics or conflicts keep returning and why they matter

9. **Targets, Enemies, and Resistances**
    - what the writer repeatedly pushes against

10. **Preferred Explanations**
    - favored causal stories, lenses, and interpretive habits

11. **Human Nature & Society Assumptions**
    - what the writer seems to assume about people, power, institutions, and collective life

12. **Tensions & Contradictions**
    - genuine internal tensions worth preserving

13. **Bullshit Detector**
    - recurring weak moves, evasions, overclaims, and coherence failures

14. **Confidence & Scope**
    - where the writer sounds certain, exploratory, or conflicted

15. **Evidence Bank**
     - exact excerpts or paraphrased evidence
     - not just vibes

16. **Open Questions**
     - unresolved tensions or unclear signals

17. **Refinement Log**
     - what changed in each pass

18. **AI Prompt Block**
     - compact prompt-ready summary for reuse

---

## Required Behaviors

### When creating the first draft

- build a usable `PHILOSOPHY.md`, not a loose summary
- include confidence labels where uncertainty exists
- prefer a compact, readable artifact over bloated theory
- favor definitions that are clear, non-contradictory where possible, and free of fake-smart buzzwords
- include at least one section that names the writer's recurring bullshit patterns in a way that is precise, evidenced, and actually usable
- include a top crystal layer that is memorable enough to serve as a quick vibe check later
- prefer existing thinker / tradition / concept anchors when they genuinely enrich clarity

### When refining an existing `PHILOSOPHY.md`

- do not rewrite sections that still hold up
- highlight what changed and why
- remove claims that are not supported by the expanded corpus
- improve evidence before inventing new categories

### When evidence conflicts

- preserve the contradiction if it appears genuine
- otherwise split by context, such as:
  - essays
  - casual posts
  - polemics
  - explanatory writing

---

## Output Format

After analysis, return:

1. a short corpus audit
2. the drafted or refined `PHILOSOPHY.md`
3. a concise refinement summary:
   - added
   - sharpened
   - downgraded
   - removed
   - still uncertain
4. if applicable, a note on why the chosen thinker/tradition anchors fit better than nearby alternatives

---

## Boundaries

This skill is great for:

- distilling a worldview from many essays or posts
- refining a living philosophy document over time
- detecting recurring self-deception and argument failure patterns
- preparing a reusable intellectual reference for AI or editors

This skill is not for:

- diagnosing the writer’s personality or pathology
- inventing a fake ideology from scratch
- reducing a worldview to topic tags
- doing lazy gotcha criticism from one edgy passage
- deriving hard rules from tiny sample sets and pretending certainty

If the user wants actual writing or argument generation after the philosophy is distilled, use the resulting `PHILOSOPHY.md` as the input contract for preserving intellectual center.
