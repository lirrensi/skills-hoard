# Deep Research Methodology

This file is the fuller operating guide behind `SKILL.md`. Use it when the task is substantial enough that the short in-skill rules are not enough.

## 0. Alignment / Mini Plan

Do this before search whenever the user's request is ambiguous enough that you might research the wrong thing.

Quick alignment checklist:

- restate what you think the user means
- name the main plausible interpretations if more than one exists
- show a tiny plan of what would be researched
- ask for correction or confirmation when a small wording difference changes the research path

Blunt but useful rule: shit in, shit out. If the user wants a precise answer, they should give enough context to aim correctly.

Do not over-drama this stage. It should be quick.

## 1. Capability Gate

Do this first. No fake starts.

Check whether the current harness has:

- search
- fetch or read-web
- parallel spawn
- file write/update

Rules:

- no search -> hard fail
- no file persistence -> stop
- no fetch -> continue only if local material plus available search output is enough
- no parallel -> continue sequentially

Record the capability result in `materials.md` before moving on.

## 2. Scope

Define the run tightly.

Capture:

- the actual question
- the user's goal
- in-scope and out-of-scope boundaries
- whether this is breadth, balanced, or depth
- what a useful answer must contain

Do not start searching until the question is specific enough to search honestly.

## 3. Scaffold

Create or reuse the default thread folder:

```text
research/<topic-slug>/
```

Default files:

- `materials.md`
- `summary.md`

Optional file:

- `plan.md`

These are the durable working artifacts. Do not depend on JSON state files by default.

## 4. Search Planning

Break the task into a few distinct tracks.

Typical tracks:

- orientation
- option or competitor comparison
- implementation or technical detail
- recency-sensitive updates
- risks or failure modes
- verification of exact claims

Good planning rule: split only when the merge path is obvious.

## 5. Breadth vs Depth

### Breadth mode

Use when the main goal is coverage.

Bias toward:

- more search angles
- more source diversity
- thinner reading per source
- fast mapping of the terrain

Stop when:

- the major angles are covered
- new searches mostly duplicate known material

### Depth mode

Use when the main goal is precision.

Bias toward:

- fewer but better sources
- deeper reading
- direct claim verification
- contradiction resolution

Stop when:

- the key claim is supported strongly enough
- remaining uncertainty is bounded and explicit

### Balanced mode

Use by default when neither extreme is clearly right.

## 6. Retrieval

Start with local material when relevant, then fill gaps with external sources.

Preferred order:

1. existing same-topic thread
2. local docs, notes, code, tickets
3. official or primary external sources
4. independent secondary sources
5. commentary and synthesis sources

Do not treat search snippets as evidence. Preserve actual useful extracts in `materials.md`.

Prefer saving over discarding. If text is relevant to the topic and likely to matter later, keep it.

`materials.md` should usually be dense enough that you can chat with the research later without rerunning everything.

For each source, keep:

- URL
- title or source label
- date when relevant
- snippet or short extract
- why it matters
- what claim or angle it supports

Often you should keep more than one snippet per source if the source supports multiple useful points.

## 7. Query Strategy

Good research usually moves through these passes:

1. orientation
2. angle-specific search
3. verification search
4. adversarial search when needed

Good query habits:

- include the exact topic or entity
- include the current year when recency matters
- vary wording instead of repeating weak phrasing
- search for direct evidence, not only summaries

Bad query habits:

- one vague search then immediate synthesis
- purely confirmatory phrasing
- using snippets as proof
- never checking for newer or opposing sources

## 8. Contradictions

Do not flatten disagreements into fake consensus.

When sources conflict, classify the reason:

- time drift
- scope mismatch
- definition mismatch
- source-quality mismatch
- genuine unresolved dispute

Then record:

- both claims
- both sources and dates
- likely cause
- whether one source wins or the point stays disputed

General preference order:

1. primary or official source
2. more recent source
3. tighter scope match
4. broader independent agreement

If none clearly wins, keep the answer conditional.

## 9. Verification

Before writing the final answer, test the collected material.

Check for:

- unsupported major claims
- overreliance on one domain
- outdated material
- contradictions not yet examined
- conclusions stronger than the evidence

Reduce confidence instead of padding weak sections.

## 10. Parallel Work

Use parallelism only when it actually helps.

Good splits:

- one worker per distinct angle
- one worker on collection, one on contradiction checking
- one critic to challenge the obvious answer
- one fact-checker for numbers, names, and dates

Bad splits:

- duplicate workers on the same angle
- splitting a tiny question into a committee
- parallel branches with no clean merge path

The lead should consolidate the durable evidence into `materials.md` and keep `summary.md` centrally synthesized.

## 11. Resume Rules

When resuming:

1. read `materials.md`
2. read `summary.md` if it exists
3. find the current stage in the status block
4. continue from the first incomplete or weak stage
5. do not redo completed work unless it is stale, contradictory, or explicitly reset

The files should let another agent resume without guessing.

They should also support follow-up conversation. If the file only supports one thin summary, it is under-saved.

## 12. Synthesis

`summary.md` should:

- answer the original question directly
- separate fact from interpretation
- make trade-offs explicit
- preserve unresolved uncertainty
- stay traceable back to `materials.md`

If evidence is mixed, say so plainly.

## 13. Final Check

Before calling the work done, ask:

- does the summary answer the real question?
- did the run align the question before searching when ambiguity mattered?
- are major claims backed by preserved evidence?
- are date-sensitive points dated?
- are contradictions resolved or clearly surfaced?
- could another pass resume from these files without confusion?
- is `materials.md` rich enough to support follow-up chat without rerunning the whole search?

If yes, the thread is in good shape.
