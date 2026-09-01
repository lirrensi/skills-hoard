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
- assumed starting point: <what the user likely already knows or has>

## Tree
- <root>
  - <branch> - <why it matters>
    - <sub-branch> - <what it unlocks>
      - <leaf> - <learnable concept, answerable question, executable task, or decision point>

## Flat List (use when minimal structure is better)
- <item> - <why it matters>
- <item> - <why it matters>

## Semi-Organized List (use when one level of grouping is enough)
### <group>
- <item> - <why it matters>
- <item> - <why it matters>

## Question Array (use instead of Tree when hierarchy is premature)
### <theme>
- [crux|gating|supporting|nice-to-have] <question> - <why this matters>
- [crux|gating|supporting|nice-to-have] <question> - <what changes depending on the answer>

## Dependency Notes
- <A is prerequisite for B>
- <C can run in parallel with D>
- <E is often confused with F>

## Unknowns And Blind Spots
- <unknown area>
- <assumption that needs validation>
- <thin branch that needs more evidence>
- <structural uncertainty: grouping uncertain | axis unclear, if applicable>

## Suggested Frontier
1. **Quick Win** (High Leverage / Low Effort): <node> - <why it's easy and unlocks stuff>
2. **Blocker** (High Leverage / High Effort): <node> - <why you must do this, but prepare for pain>
3. **Rabbit Hole** (Low Leverage / High Effort): <node> - <AVOID THIS FOR NOW>
4. **The Unknown** (High Uncertainty): <node> - <verify before committing>

## Optional Follow-On
- if the user wants a durable corpus next -> build it with `knowledge-accumulator`
- if the user wants deeper branch-by-branch reasoning -> use `thinking-graph`

---

# Interrogation-first template (use when the root is not ready)

## What I think you might mean
- <interpretation 1>
- <interpretation 2>
- <interpretation 3>

## Why I am pausing
- <why a decomposition now would be fake or misleading>

## One-shot interrogation
Reply in bullets or paragraphs. Messy is fine.

1. <actual desired outcome>
2. <closest interpretation + missing nuance>
3. <preferred artifact shape: flat list | semi-organized list | dense map/tree | iterative map>
4. <why now>
5. <constraints>
6. <starting point>
7. <first milestone definition of success>
8. <what to exclude>

## Next move after your reply
- convert the answer into the right mode and shape
