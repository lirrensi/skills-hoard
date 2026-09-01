# Lane Selection

Pick the lightest lane that still gives the user a decision they can defend and act on.

## Triage Questions

Ask or infer these first:

1. What happens if we are wrong?
2. How reversible is the decision?
3. How soon must we decide?
4. What is genuinely uncertain?
5. Is this an individual choice or a stakeholder choice?

## Lane Map

| Lane | Use When | Core Output |
|---|---|---|
| `quick` | low stakes, reversible, time-limited | threshold call + next step |
| `trade-off` | several named alternatives with competing criteria | ranked or reasoned comparison |
| `sequence` | pilot, wait, or staged learning could change the choice | act-now vs wait vs pilot logic |
| `value` | costs, benefits, or payoffs can be estimated credibly | expected-value or cost-benefit view |
| `uncertainty` | future states or long horizon dominate | scenarios, no-regrets moves, signposts |
| `dynamic` | the environment changes quickly and feedback matters | looped action plan |
| `group` | authority, values, or stakeholder conflict are the blocker | owner, dissent, trade-offs, alignment path |

## Minimum Bundle By Decision Shape

- Small and reversible -> `quick` + one stress test
- Several options and many criteria -> `trade-off` + sensitivity check
- Need to learn before committing -> `sequence` + staged commitment
- Long-horizon unknowns -> `uncertainty` + signposts
- Fast-moving execution context -> `dynamic` + review loop
- High downside or suspicious consensus -> chosen lane + stronger stress test

## Fast Lane Heuristic

Use the quick lane when all of this is true:

- wrong is survivable
- reversal is affordable
- no major stakeholder alignment problem exists
- one more day of analysis is worth less than one day of action

If any of those fail, move up a lane.

## Escalation Rules

Escalate from a lighter lane when:

- the top options are close and the trade-offs matter
- the cost of being wrong is asymmetric
- the user keeps reopening the decision
- stakeholders disagree on what matters
- waiting has real informational value

## Anti-Patterns

- treating every decision like a one-way door
- pretending every decision deserves a spreadsheet
- choosing a heavy lane because it feels safer, not because it changes the decision
