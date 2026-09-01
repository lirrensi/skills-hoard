# Selection questions

Use these questions when the right essence is not obvious yet.

The goal is not to design the final output. The goal is to decide what structure in the source most needs to survive.

## If the choice is ambiguous

Do not hand the user the full menu unless they explicitly ask for it.

Instead:

1. Look at the user's initial want.
2. Look at the structure already visible in the source.
3. Suggest the top 3 candidate essences.
4. Recommend one default.

Each candidate should include:

- why it fits
- what it preserves well
- what it would flatten or weaken

Good defaults:

- Put the best overall fit first.
- Put a second option that preserves a different important structure.
- Put a third option only if it is genuinely plausible, not filler.

If none of the three is sufficient alone, recommend a small essence set.

## First-pass questions

- What kind of structure repeats in the source: events, terms, claims, tasks, metrics, categories, or relationships?
- What would be most damaging to flatten: chronology, wording, tradeoffs, evidence, uncertainty, or ownership?
- Does the source mostly explain, compare, instruct, classify, argue, narrate, or report?
- Will a future user need to browse by question, by timeline, by category, by metric, or by relationship?
- Is one structure clearly primary, or do you actually need a small essence set?

## Neighbor distinctions

### Summary vs patterns and themes

- Choose `summary` when the job is faithful compression of the whole.
- Choose `patterns-and-themes` when the job is synthesis across repeated examples or many sources.

### Claims and evidence vs arguments and counterarguments

- Choose `claims-and-evidence` when you need an audit trail from assertion to support.
- Choose `arguments-and-counterarguments` when you need positions in tension, objections, and rebuttals.

### Timeline vs cause and effect chains

- Choose `timeline` when order in time is the main structure.
- Choose `cause-and-effect-chains` when mechanism matters more than dates.

### Entities and relations vs taxonomy vs prerequisites and dependencies

- Choose `entities-and-relations` for network structure between actors, objects, and concepts.
- Choose `taxonomy` for category hierarchy.
- Choose `prerequisites-and-dependencies` for readiness, unlock order, or what must exist first.

### Comparison vs claims and evidence

- Choose `comparison` when several options are being evaluated on a shared rubric.
- Choose `claims-and-evidence` when the source mostly makes assertions that need grounding.

### Rules and constraints vs steps and procedures vs action items

- Choose `rules-and-constraints` for guardrails, prohibitions, and invariants.
- Choose `steps-and-procedures` for repeatable execution order.
- Choose `action-items` for concrete follow-through commitments with owners and timing.

### Document structure vs summary

- Choose `document-structure` when the source skeleton itself matters and should survive intact.
- Choose `summary` when the source can be compressed without preserving its full section flow.

### Decisions and rationale vs action items vs comparison

- Choose `decisions-and-rationale` when the main value is what was chosen and why.
- Choose `action-items` when the main value is who must do what next.
- Choose `comparison` when options still need to be lined up on a shared rubric.

### Requirements and acceptance vs rules and constraints vs steps and procedures

- Choose `requirements-and-acceptance` when you need testable success conditions.
- Choose `rules-and-constraints` when you need guardrails and prohibitions.
- Choose `steps-and-procedures` when you need execution order.

### Scenarios and use cases vs steps and procedures vs examples and cases

- Choose `scenarios-and-use-cases` for actor-goal situations and possible paths.
- Choose `steps-and-procedures` for the recommended way to execute work.
- Choose `examples-and-cases` for illustrative instances that teach by example.

### Quotes and excerpts vs summary vs sentiment and opinion

- Choose `quotes-and-excerpts` when the exact wording itself must survive.
- Choose `summary` when faithful compression is enough.
- Choose `sentiment-and-opinion` when the stance matters more than the exact phrasing.

### Stakeholders and positions vs entities and relations

- Choose `stakeholders-and-positions` when incentives, stance, leverage, and conflict matter.
- Choose `entities-and-relations` when the main job is mapping the domain or system structure.

### Observations and signals vs patterns and themes vs gaps and unknowns

- Choose `observations-and-signals` when you are still collecting findings and anomalies.
- Choose `patterns-and-themes` when repeated meaning has already emerged across observations.
- Choose `gaps-and-unknowns` when what matters most is what is missing or unresolved.

## Split when needed

If two structures are equally important, do not force one bad essence.

Common good splits:

- `summary` + `data-and-metrics`
- `concepts-and-definitions` + `taxonomy`
- `claims-and-evidence` + `gaps-and-unknowns`
- `timeline` + `entities-and-relations`
- `document-structure` + `summary`
- `quotes-and-excerpts` + `patterns-and-themes`
- `decisions-and-rationale` + `action-items`

Keep each file small, explicit, and editable.
