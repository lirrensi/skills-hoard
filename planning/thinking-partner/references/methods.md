# Thinking Partner Methods

Use this file when you want a more deliberate technique choice instead of relying only on general conversational instinct.

Do not stack methods for show.
Pick the lightest tool that helps the user think better.

## Principles

- attention before technique
- one method at a time unless the user clearly benefits from a sequence
- externalize when the reasoning gets tangled
- move from exploration to evaluation explicitly
- if prior memory or artifacts exist, use them to spot repeated patterns and reduce needless rehashing

## Method Palette

| Method | Use when | What it does | Good prompt |
|---|---|---|---|
| OARS | user is still unfolding the issue | open questions, affirm, reflect, summarize | `Tell me more about that, and I will play back what I hear.` |
| ORID | facts, feelings, meaning, and decisions are mixed together | separates layers so the user stops arguing with themselves | `Let us split this into facts, reactions, meaning, and decision.` |
| Five Whys | the surface issue is probably not the real issue | drills toward the root driver | `Why does that matter so much here?` |
| Contrast cases | a term or category is fuzzy | sharpens definition with examples and non-examples | `What would count, and what would not count?` |
| Correction-seeking paraphrase | the user is close to the meaning but not landing it cleanly | a slight misread invites a sharper correction | `So it is really about leaving, not staying differently?` |
| Steelman then critique | a view needs honest challenge | proves good faith before pressure-testing | `Let me state the strongest version first, then test it.` |
| Premortem | a plan looks attractive but fragile | imagines failure early and extracts risks | `It is six months later and this failed. Why?` |
| Ladder of inference rewind | someone is leaping from data to certainty | traces conclusion back through meaning and assumption | `What observation led you there, and what meaning did you add?` |
| Double-loop inquiry | the same pattern keeps recurring | questions the governing assumptions, not just the tactic | `What rule or value is driving this pattern?` |
| Concept mapping | there are too many moving parts | exposes nodes, links, gaps, and hidden structure | `Let us name the main elements and how they affect each other.` |
| Argument mapping | the issue is a claim with reasons and objections | separates claims, support, objections, and rebuttals | `What is the claim, what supports it, and what pushes back?` |
| Consider-the-opposite | the user is anchored to one story | reduces confirmation bias | `If the opposite were partly true, what would we notice?` |
| Inversion | direct solving is stuck | unlocks through reverse framing | `How would we guarantee failure?` |
| Perspective shift | the user is trapped inside one frame | changes the angle without forcing a conclusion | `How would a smart critic or future you see this?` |
| Thread tracking | the conversation keeps branching into several live issues | prevents spiraling by naming, parking, and sequencing threads | `I see three threads here. Which one is primary, and which two should we park for later?` |

## Suggested Sequences

Use these as light defaults, not rigid scripts.

### Messy and overloaded

1. OARS
2. ORID
3. thread tracking
4. one-sentence synthesis

### Vague but important decision

1. define criteria
2. Ladder of inference rewind
3. premortem
4. next information test

### Idea generation before evaluation

1. broaden options
2. use inversion or constraints
3. cluster themes
4. steelman top option
5. stress-test top option

### Repeated pattern or recurring failure

1. summarize the pattern across examples
2. double-loop inquiry
3. surface assumptions
4. choose one experiment that would break the pattern

## Externalization Rules

When reasoning is too tangled to hold in working memory, put it into a simple structure.

Prefer:

- list for options, assumptions, criteria, or risks
- short thread register for active, parked, and next-up topics
- concept map for systems or causality
- argument map for claims and objections
- timeline for sequence confusion

Do not create a formal artifact if a two-line summary will do the job.

## Debiasing Without Becoming Annoying

Do not accuse the user of being biased.
Instead, redesign the thinking process.

Prefer prompts like:

- `What would make the opposite case stronger than it currently looks?`
- `Are we overweighting the first fact that showed up?`
- `Would this still look good if the sunk time disappeared?`
- `What evidence are we missing because the current story feels neat?`

## Transition Phrases

Use explicit transitions so the user knows what kind of thinking is happening.

- `Let us stay in exploration mode for a minute longer.`
- `I think we have enough raw material. Let me structure it.`
- `I think we have three threads live. I am going to name them so we do not spiral.`
- `Let us park two threads and stay with the one that has the most charge or leverage.`
- `Want me to pressure-test this now, or keep drawing it out?`
- `I am going to challenge one assumption, not because it is wrong, but because it looks load-bearing.`
- `Let me compress what we have into the cleanest version so far.`

## Watchouts

- Do not hide advice inside fake questions.
- Do not use Socratic questioning like cross-examination.
- Do not map so much that the conversation loses life.
- Do not keep exploring once the user clearly needs a decision.
- Do not keep challenging once the user has reached genuine clarity.
