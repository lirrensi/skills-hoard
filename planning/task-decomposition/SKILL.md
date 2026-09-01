---
name: task-decomposition
description: Build a scoped decomposition tree for any broad topic, field, project, or goal. Use whenever the user asks to break something down, wants a knowledge graph, learning map, prerequisite tree, task hierarchy, question array, or a way to see what they do not know yet before acting. Also use when a problem is too big to start and the right move is to map the territory first instead of jumping straight into answers or implementation, or when the real need is a structured intake interrogation before honest decomposition.
---

# Decomposition

Use this skill to turn an overwhelming topic into a navigable map.

The goal is not exhaustive coverage.
The goal is to give the user a usable map, tree, or question set of:

- the major branches
- the important prerequisites
- the thin or unknown areas
- the best next places to learn or act

This skill is about knowing what you do not know yet.
It should reduce overwhelm, expose missing structure, and create a starting path.

## What This Skill Is For

Use this skill when the user wants to:

- break a huge topic into understandable branches
- map a field before learning it
- turn a vague project into a task hierarchy
- turn an ambiguous ask into a structured question array before planning
- identify prerequisites, dependencies, and sequencing
- see blind spots before committing to execution
- create a compact knowledge tree or mini knowledge graph

Do not use this skill when:

- the task is already small and concrete
- the user clearly wants direct implementation right now
- the main problem is extracting structure from raw source material rather than decomposing the topic itself
- the main problem is deep reasoning between competing hypotheses rather than breadth mapping

If the user needs a durable corpus after the map exists, hand off to `knowledge-accumulator`.
If the user needs deep branching reasoning, use `thinking-graph`.
If the user first needs structure extracted from messy notes or documents, use `essence-workbench`.

## Core Stance

- Interrogate ambiguity before decorating it.
- Scope first, then branch.
- Call out vagueness before pretending to map it.
- Prefer a map over a dump.
- Show uncertainty instead of faking completeness.
- Go broad before going deep unless the user clearly wants a deep path.
- Decompose only until the next useful level, not forever.
- Make prerequisites and cross-links visible.
- End with a frontier: where the user should start.

## Separation Logic (MECE Heuristic)

When creating sibling nodes, aim for Mutually Exclusive and Collectively Exhaustive (MECE) *at that level of abstraction*.

Perfect MECE is not always possible or necessary. But if branches bleed into each other heavily, it usually means the decomposition axis is wrong. Change the lens:

- Instead of `Backend` vs `Database` (overlaps), use `Data Layer` vs `Compute Layer`.
- Instead of `Marketing` vs `Sales` (overlaps), use `Acquisition` vs `Conversion`.
- Instead of `Features` vs `Bugs` (overlaps), use `User-Facing` vs `System-Facing`.

If overlap is unavoidable or even useful (shared concerns, cross-cutting themes), label it explicitly: `(overlaps with X)` or `(touches all branches)`.

Do not force artificial separation just to look clean. Real problems have messy edges. Acknowledge them and move on.

## Pre-Decomposition Diagnostic

Before building the tree, check whether the request is actually ready for decomposition.

If the prompt is vague, bloated, contradictory, or performatively ambitious, say so plainly.
Do not politely produce a fake map from nonsense.

Common diagnostic states:

- `already small enough` - the task is concrete and scoped; decomposition would over-engineer it; just do it or answer it directly
- `too vague to map` - no real object, goal, or boundary yet
- `too broad for one pass` - needs scoping before branching
- `no clear entry point` - several valid starts, no decision rule
- `dependency fog` - too many hidden prerequisites or blockers
- `scope creep risk` - the user is already mixing adjacent projects together
- `spike first` - a short research pass is needed before honest decomposition

If one of these dominates, say what is missing and either narrow the scope yourself or ask for the minimum clarification needed.

## Output Modes, Artifact Shape, And Map Profile

Choose the dominant mode before building the tree:

- `knowledge-tree` - what must be understood
- `task-tree` - what must be done
- `question-tree` - what must be answered (decomposes a complex question into sub-questions that compose back into the parent answer)
- `question-array` - a flat but structured list of clarification or research questions, usually prioritized or grouped, when hierarchy would be premature or fake
- `hybrid-tree` - what must be understood and done together

Use `knowledge-tree` by default for broad fields and learning questions.
Use `task-tree` for concrete execution goals.
Use `question-tree` when the user has a complex question that needs to be broken into answerable sub-questions. This mode is especially useful for research, analysis, and decision-making.
Use `question-array` when the user is still defining the problem, when you need intake questions before a real tree exists, or when a complex project would benefit more from a grouped questionnaire than from premature decomposition.
Use `hybrid-tree` when knowledge gaps and action steps are tightly coupled.

Choose the **artifact shape** separately from the mode.
The same underlying problem might want different output shapes depending on user preference and current readiness.

Artifact shapes:

- `flat-list` - one plain list, minimal structure, fast scan
- `semi-organized-list` - grouped list with one light level of organization
- `tree-map` - explicit hierarchy with multiple levels
- `iterative-map` - a map that is expected to grow over multiple clarification rounds

Do not assume the biggest structure is the best structure.
Sometimes the smartest output is a flat list. Sometimes it is one grouped layer. Sometimes it is a dense map that evolves over time.

### Output-shape negotiation

When the request is broad, ambiguous, or likely to support multiple useful shapes, ask the user what kind of artifact they want before committing too hard.

Preferred prompt:

- `Do you want a flat list, a semi-organized list, a dense tree/map, or an iterative map we build over time?`

Use this especially when:

- the task could honestly fit multiple output shapes
- the user seems overwhelmed and may want less structure first
- the user seems exploratory and may want a growing artifact rather than a one-shot answer
- a huge tree would be technically valid but practically annoying

If the user does not specify, choose the lightest shape that still preserves the important structure.

Also choose how the map should behave:

- `breadth-first` - thin nodes, more coverage, shallow first pass
- `balanced` - moderate coverage with selective detail
- `deep-path` - fewer branches, richer nodes, deeper drilling

Set these controls explicitly when useful:

- `depth cap` - usually 2 to 5 levels
- `node richness` - `thin`, `standard`, or `rich`
- `visualization` - `markdown-list` (default), `mermaid-graph`, or `ascii-tree`

**When to use Mermaid**: When dependencies and cross-links matter more than hierarchy. Good for complex webs where the user needs to see relationships visually.

**When to use ASCII**: When the tree is deep and narrow, or the user is on mobile / in a context where rendering Mermaid is unreliable.

**When to use markdown-list** (default): For most cases. Clean, readable, works everywhere.

Default profile:

- mode: `knowledge-tree`
- profile: `breadth-first`
- depth cap: `3`
- node richness: `standard`
- visualization: `markdown-list`

### Interrogation-first trigger

Before choosing the final mode, check whether the user's request needs a **clarification sprint** first.

Trigger this when most of the following are true:

- the root request is broad, identity-level, or aspirational (`I want to build rockets`, `I want to start a company`, `help me design my whole platform`)
- there are multiple plausible meanings or end states
- the best decomposition depends heavily on constraints the user has not given yet
- a bad first tree would create fake certainty
- the user seems to need help discovering what they actually mean

If triggered, do **not** immediately emit a giant tree.
Instead run a short two-step intake:

1. **Rapid branch scan** — identify 3 to 6 plausible interpretations or branches of the ask.
2. **Shape check** — if useful, ask whether they want a flat list, semi-organized list, dense map, or iterative map.
3. **One-shot interrogation** — ask the user for a dense brain dump that resolves intent, constraints, and success criteria in one reply.

This is still part of task decomposition. It is a pre-map mode, not a failure.

### Expected scale by profile

Different profiles produce different sized trees. Set expectations accordingly:

| Profile | Typical total nodes | Reading strategy |
|---------|---------------------|------------------|
| `breadth-first` | 15-40 nodes | Scan the first two layers for orientation; drill into specific branches only |
| `balanced` | 30-80 nodes | Read top layer fully, selectively explore 2-3 branches in depth |
| `deep-path` | 20-60 nodes (but deeper) | Follow one or two branches deeply; other branches are thin |

If a tree exceeds ~100 nodes, it is probably too broad for one pass. Tighten scope or split into multiple maps.

If a tree has fewer than 8 nodes, it may not need decomposition at all. Consider whether the `already small enough` diagnostic applies.

## Default Workflow

### 0. Rapid interpretation scan

Before scoping the root, quickly infer what the user might mean.

For a broad ask, produce an internal or explicit shortlist like:

- possible meanings
- likely end states
- likely user levels
- obvious constraints that would radically change the map

Example for `I want to learn how to build space rockets`:

- hobby model rocketry
- amateur high-power rocketry
- aerospace engineering as a field of study
- startup/company path for launch systems
- literal fabrication of propulsion, structures, avionics, and test systems

If those branches imply meaningfully different trees, pause and interrogate before decomposing.

### 1. Scope the root

Anchor the map in one clear root statement:

- what is being decomposed
- why the user wants the map
- what counts as in scope
- what is explicitly out of scope
- the user's assumed starting level, if relevant

If the user gives a broad prompt with no boundaries, make a reasonable default scope and state it briefly.
If multiple reasonable scopes compete, do not guess too hard. Use the interrogation protocol below.

## Interrogation Protocol (for ambiguous or oversized asks)

When the request is too broad for an honest first tree, ask **one structured interrogation** instead of drip-feeding clarifying questions over many turns.

### Goal

Get enough signal in one response to decide:

- whether the right output is a `question-array`, `task-tree`, `knowledge-tree`, `question-tree`, or `hybrid-tree`
- whether the right artifact shape is `flat-list`, `semi-organized-list`, `tree-map`, or `iterative-map`
- what the true root should be
- which branches are real versus decorative
- whether the user needs planning, learning, research, or execution support first

### How to ask

1. Start with a **brief interpretation check**:
   - `Here are the main ways I could read this.`
   - list 3 to 6 plausible meanings or branches
2. If shape is not obvious, ask what artifact shape they want.
3. Then ask for a **single detailed reply**.
4. Make the prompt feel like a compact intake form, not a bureaucratic survey.
5. Ask for paragraphs or bullets, whichever gets the user's real thinking out fastest.
6. Prefer one high-bandwidth message over 10 tiny follow-ups.

### Interrogation prompt shape

Use sections like these and customize them to the domain:

- **What do you actually mean?**
  - What outcome are you pointing at?
  - Which of the branch interpretations is closest?
- **What shape do you want back?**
  - flat list, semi-organized list, dense map/tree, or iterative map over time
- **Why now?**
  - What problem are you trying to solve, or what opportunity are you chasing?
- **Success looks like...**
  - What would count as a win in 1 month, 3 months, or 1 year?
- **Constraints and reality**
  - time, budget, team, tools, risk tolerance, legal/safety limits, geography
- **Current starting point**
  - skills, assets, existing work, assumptions, non-negotiables
- **What you do *not* want**
  - dead ends, styles of plan, scope you want excluded
- **Known unknowns**
  - what confuses you most right now?

### Output after interrogation

After the user replies, explicitly choose one:

- `question-array` if the next useful artifact is a grouped and prioritized list of questions
- `task-tree` if the user is ready for execution structure
- `knowledge-tree` if the user needs conceptual orientation first
- `question-tree` if the core job is answering a complex parent question
- `hybrid-tree` if understanding and execution are intertwined

Then explicitly choose artifact shape:

- `flat-list` for speed, low overhead, and easy scanning
- `semi-organized-list` for light grouping without deep hierarchy
- `tree-map` for dense structured decomposition
- `iterative-map` when the map should stay open and evolve over multiple turns

### Question-array guidance

When using `question-array`, do **not** pretend hierarchy exists if it doesn't yet.

Produce:

- 6 to 20 questions
- grouped into 3 to 6 themes
- each question labeled as `crux`, `gating`, `supporting`, or `nice-to-have`
- optional priority or suggested answer order
- optional note for what changes if the answer goes one way versus another

Good question-array use cases:

- pre-project intake
- discovery before scoping a large build
- coaching a user to clarify an ambitious goal
- strategy work where the unknowns matter more than the current plan

### Shape heuristics

Use `flat-list` when:

- the user asks for quick orientation
- the branch structure is weak or premature
- the value is mostly in enumeration, not hierarchy

Use `semi-organized-list` when:

- there are a few natural buckets
- one level of grouping adds clarity
- a full tree would be overkill

Use `tree-map` when:

- dependencies and parent-child relationships genuinely matter
- the user wants a knowledge map, roadmap, or decomposed system view
- depth changes decisions

Use `iterative-map` when:

- the space is large and evolving
- multiple clarification rounds are expected
- the user wants a map they can build over time rather than consume in one shot

### 2. Set the map profile

Before expanding the tree, decide:

- how many levels are worth showing
- how rich each node should be
- whether this pass should optimize for breadth, balance, or depth

Prefer breadth first for overwhelmed users.
One clean top layer is usually more valuable than five premature sublevels.

### 3. Choose a decomposition lens

Pick the lens that best exposes structure for the current problem. Do not stack every lens at once.

**Primary lenses** (choose one):

| Lens | Use when | Break down by | Default question |
|------|----------|---------------|------------------|
| **Conceptual** | Understanding a field or body of knowledge | foundations, domains, core concepts, subfields | What would someone need to understand before this stops feeling like a blur? |
| **Component** | Decomposing a system, product, or organization | subsystems, modules, actors, interfaces | What are the major parts, and how do they fit together? |
| **Lifecycle** | Sequence, stages, or progression matter | phases, milestones, states, transitions | How does this unfold over time? |
| **Task** | User needs execution structure | goals, subgoals, work packages, deliverables | What has to be done, in what chunks, for this to become real? |
| **Prerequisite** | User wants to know what unlocks what | foundations before advanced, gating decisions, dependencies | What has to come first for later branches to make sense? |
| **Risk** | Uncertainty, failure modes, or blind spots are central | assumptions, blockers, failure modes, unknowns | What could break this, and what do we still not understand? |

**Quick defaults:**
- field or discipline → conceptual + prerequisite
- system or product → component + lifecycle
- project or execution plan → task + dependency notes
- ambiguous or risky initiative → task or component + risk

**Strategy overlays** (optional, for complex problems):
- **Functional** — break down by what the system does (good for workflows, feature sets)
- **Structural** — break down by what the system is made of (good for architectures, organizations)
- **Data flow** — break down by how information moves (good for pipelines, integrations)
- **Temporal** — break down by sequence or timing (good for journeys, delivery phases)
- **Cost/resource** — break down by spend, capacity, or constraints (good for optimization, budgeting)

If the first tree feels wrong, do not keep polishing it. Switch lenses.

For the full lens reference with extended guidance, see `references/decomposition-lenses.md`.

### 4. Build the first layer

Create 3 to 7 top-level branches.
They should be broad enough to orient the user and distinct enough to reduce confusion.

Do not force fake neatness.
Branches do not need to be perfectly disjoint, but each one should earn its place.

Default to filling the first layer well before deepening individual branches.

### 5. Recurse only where useful

Decompose each branch only until it becomes one of these:

- a learnable concept
- an answerable question
- an executable task
- a decision point

Default maximum depth is 5 levels from the root.
Stop earlier if deeper breakdown would add noise instead of clarity.

If the profile is `breadth-first`, deepen only the most important or most uncertain branches.
Do not give every branch equal depth just because the tree visually wants symmetry.

### 6. Mark unknowns and weak spots

For major branches and important leaves, label the current state when useful:

- `known`
- `thin`
- `unknown`
- `assumption`
- `needs evidence`

Do not label every node mechanically.
Use labels where they help the user see what is missing.

Also flag **structural uncertainty** when the grouping itself might be wrong:

- `grouping uncertain` - the nodes are real but the parent-child relationship is debatable; a different lens might produce a better tree
- `axis unclear` - the decomposition axis (what makes siblings distinct) is fuzzy; the branches bleed together

These are different from content unknowns. Content unknowns say "we don't know what this node contains." Structural unknowns say "we're not sure this is the right way to carve up the problem." When structural uncertainty is high, suggest an alternative lens or grouping and let the user choose.

### 7. Add relationships that matter

After the tree exists, add non-parent-child links when they change how the map should be read:

- prerequisite for
- depends on
- data flows into
- controls or triggers
- happens before
- shares resources with
- often confused with
- feeds into
- can run in parallel with

If relationships dominate the problem more than the hierarchy does, say so plainly.

### 8. Land the map

End with a short frontier section that prescribes action, not just lists nodes. Use the Effort/Leverage matrix to categorize:

- **The Quick Win** (High Leverage / Low Effort) — the node that unlocks the most downstream progress for the least work. Start here.
- **The Blocker** (High Leverage / High Effort) — the node that must be resolved eventually but will take real work. Name it so the user can prepare.
- **The Rabbit Hole** (Low Leverage / High Effort) — the node that looks important but would consume disproportionate time with little payoff. Explicitly tell the user to avoid this for now.
- **The Unknown** (High Uncertainty) — the node where the answer could reshape the entire tree. Flag this as "verify before committing."

Also include:
- what not to worry about yet (nodes that are downstream of the frontier)
- which unknowns are most dangerous (if wrong, the whole plan breaks) vs. most informative (if resolved, the most other nodes become clear)

## Iterative Refinement (Drill-Down Protocol)

A decomposition is a conversation, not a monument. The first tree is a starting point, not a final answer.

### If the user asks to "expand", "zoom in", or "drill down" into a node:

1. Treat that node as the **new root**.
2. Keep the original tree visible above (collapsed or referenced by path, e.g., `Root > Branch 2 > Sub-branch b`).
3. Run the full Decomposition workflow again on just that node.
4. **Inherit the `mode` and `profile` from the parent map** unless the user explicitly changes them. Do not switch from `task-tree` to `knowledge-tree` mid-conversation without a reason.

### If the user says "I already know X" or "skip branches 1 and 2":

1. Mark those nodes as `known` in the tree.
2. Collapse them to a single line: `(known) <node name>`.
3. Reallocate depth budget to the remaining unknown branches.
4. Update the frontier to focus on what is still unknown.

### If the user says "this grouping feels wrong" or "restructure":

1. Ask what feels wrong specifically: too broad, too narrow, wrong axis, missing branch, or overlapping.
2. If the lens is wrong, switch lenses and rebuild the first layer.
3. If a single branch is misplaced, move it and explain the new parent.
4. Do not rebuild the entire tree unless the root itself is wrong.

### If the user provides new information mid-conversation:

1. Re-run the Pre-Decomposition Diagnostic with the new info included.
2. If the new info resolves a vagueness flag, rebuild the tree.
3. If the new info just fills in a leaf or branch, update that node's status to `known` and adjust the frontier.
4. If the new info contradicts existing nodes, flag the conflict explicitly and ask which version to keep.

### If the user asks "where do I start?" after seeing the tree:

Do not re-decompose. Point to the existing `Suggested Frontier`. If the frontier is stale or empty, pick 3 nodes based on:
- Highest uncertainty (`unknown` or `assumption`)
- Highest leverage (unlocks the most downstream nodes)
- Lowest effort to resolve

## Anti-Patterns

Avoid these failure modes:

- `fake precision` - acting more certain than the source material justifies
- `depth creep` - diving too many levels down before the first layer is coherent
- `flat dump` - listing many items without hierarchy, grouping, or unlock logic
- `research forever` - using decomposition to avoid choosing a starting point
- `technical decomposition without value` - generating implementation chores with no user-facing outcome
- `perfect tree syndrome` - polishing the map instead of making it useful
- `flat earth syndrome` - refusing to decompose because "it's all connected"; dumping 50 ungrouped bullets and calling it a map; treating every topic as too entangled to structure

Preferred correction moves:

- tighten scope
- go back up one level
- reduce node richness
- fill the first layer before deepening
- split the work into a later pass instead of forcing completeness now

## Tree Quality Checks

A good decomposition should make these easier, not harder:

- explain the territory in plain language
- see what is missing
- choose what to learn or do next
- tell which branches are foundational versus optional
- avoid drowning in flat lists
- preserve breadth before unnecessary depth

If the map becomes bloated or repetitive:

- tighten scope
- change lens
- lower the depth cap
- reduce node richness
- merge decorative branches
- stop decomposing low-value leaves

## Response Structure

When using this skill in conversation, prefer this shape:

```markdown
# <topic> decomposition

## Diagnostic
- state: <ready | already small enough | too vague to map | too broad for one pass | no clear entry point | dependency fog | scope creep risk | spike first>
- note: <brief call-out if the prompt is weak or overloaded>

## Mode
- type: knowledge-tree | task-tree | question-tree | question-array | hybrid-tree
- artifact shape: flat-list | semi-organized-list | tree-map | iterative-map
- profile: breadth-first | balanced | deep-path
- depth cap: <1-5>
- node richness: thin | standard | rich
- visualization: markdown-list | mermaid-graph | ascii-tree
- objective: <why this map exists>
- in scope: <boundary>
- out of scope: <boundary>
- assumed starting point: <optional>

## Tree
- <root>
  - <branch> - why it matters
    - <sub-branch> - why it matters or what it unlocks

## Flat List
- <item> - <why it matters>

## Semi-Organized List
### <group>
- <item> - <why it matters>

## Question Array
### <theme>
- [crux|gating|supporting|nice-to-have] <question> - <why it matters>
- [crux|gating|supporting|nice-to-have] <question> - <what changes depending on the answer>

## Dependency Notes
- <important cross-links, prerequisites, or sequencing>

## Unknowns And Blind Spots
- <thin, missing, assumed, or disputed areas>
- <structural uncertainty: grouping uncertain | axis unclear, if applicable>

## Suggested Frontier
1. **Quick Win** (High Leverage / Low Effort): <node> - <why>
2. **Blocker** (High Leverage / High Effort): <node> - <why>
3. **Rabbit Hole** (Low Leverage / High Effort): <node> - <AVOID FOR NOW>
4. **The Unknown** (High Uncertainty): <node> - <verify before committing>
```

If the request is **not ready** for decomposition and you are using the interrogation protocol, prefer this shape instead:

```markdown
# Clarify the root before we fake a plan

## What I think you might mean
- <interpretation 1>
- <interpretation 2>
- <interpretation 3>

## Why I am pausing
- <what would make the first tree misleading>

## One-shot interrogation
Reply in bullets or paragraphs. Messy is fine.

1. What outcome are you actually aiming for?
2. Which interpretation above is closest, and what did I miss?
3. What shape do you want back: flat list, semi-organized list, dense map/tree, or iterative map over time?
4. Why do you care about this now?
5. What constraints are real? (time, budget, people, tools, safety, legal, etc.)
6. What do you already know / have / believe?
7. What does success look like at the first meaningful milestone?
8. What do you definitely *not* want this to turn into?

## Next move after your reply
- I will turn your answer into the right mode and the right shape: question-array, task-tree, knowledge-tree, question-tree, or hybrid-tree, delivered as a flat list, semi-organized list, tree-map, or iterative map.
```

If a file would help, use `templates/decomposition_map.md` as the starting artifact.

## Heuristics For Good Nodes

Each useful node should be one or more of these:

- a coherent domain of knowledge
- a meaningful subsystem
- a real stage in a process
- a concrete dependency or prerequisite
- a distinct risk, constraint, or blocker
- a unit that can later become a question, lesson, or task

Avoid vague filler nodes like `other stuff`, `general knowledge`, or `implementation details` unless they are immediately refined.

## Stop Rule

Stop decomposing when deeper branching no longer changes the user's next decisions.
A leaf is usually good enough when it can be phrased clearly as:

- `I need to understand X.`
- `I need to answer Y.`
- `I need to do Z.`

When in doubt, stop one level earlier and improve breadth, boundaries, or dependency notes.

## Question Quality (for question-tree and question-array modes)

When decomposing into sub-questions, each question node should be:

- **Specific** — not "what about the data?" but "what is the expected latency for the primary database queries?"
- **Answerable** — the question can be resolved with available information or a defined research step
- **Scoped** — narrow enough that answering it is a real task, not another decomposition
- **Composable** — answering all children should substantially answer the parent question

Distinguish between:

- **Crux questions** — the 1-3 questions where the answer changes the shape of everything downstream. If the answer to Q is "yes", the rest of the tree looks different than if it's "no". Flag these explicitly.
- **Supporting questions** — questions that fill in context or detail but don't reshape the tree. These are important but not pivotal.
- **Gating questions** — questions that must be answered before other questions become meaningful. These are prerequisites in question form.

If you cannot formulate a sub-question that is specific and answerable, the branch is not ready for decomposition. Go back up one level or flag it as `needs scoping`.

## Domain Examples

- software architecture -> modules, services, layers, data stores, and coupling points
- business process -> steps, approvals, handoffs, blockers, and cycle-time risks
- learning a field -> foundations, subfields, prerequisites, and open knowledge gaps
- user experience -> journey stages, pain points, dependencies, and redesign opportunities
- cost optimization -> cost centers, major drivers, constraints, and quick-win branches

## Example Triggers

- `Break down what I need to know to build a rocket.`
- `Map the field of distributed systems so I know where to start.`
- `Turn launching this product into a task hierarchy with dependencies.`
- `I am overwhelmed by AI security. Give me a knowledge tree.`
- `Decompose this giant project into the branches that actually matter.`
