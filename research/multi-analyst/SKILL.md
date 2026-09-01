---
name: multi-analyst
description: Invoke one or more disciplinary analysts to examine a topic through multiple expert lenses simultaneously. Use when the user wants deep analysis from specific perspectives — e.g. "look at this as an economist and ethicist", "give me engineer + psychologist takes", "analyze through multiple lenses", or "what would a historian / futurist / philosopher say about this". Also use when the user asks for multi-perspective thinking, expert panel simulation, or disciplinary analysis on any problem, idea, or decision. Trigger on: "analyze as", "think like a", "what would X say", "multiple perspectives", "expert lens", "disciplinary analysis", "panel of analysts".
---

# Multi-Analyst

A smart router to 14 disciplinary analysts. You pick which lenses to apply — one or many — and the skill loads only what's needed.

**Do NOT load all references upfront.** Ask the user which analysts they want, then load only the selected ones.

## Available Analysts

| #  | Analyst                | Lens                                          |
|----|------------------------|-----------------------------------------------|
| 1  | `anthropologist`       | Culture, ritual, kinship, symbolic meaning     |
| 2  | `computer-scientist`   | Algorithms, complexity, systems architecture   |
| 3  | `economist`            | Supply/demand, incentives, market dynamics     |
| 4  | `engineer`             | First principles, trade-offs, failure modes    |
| 5  | `ethicist`             | Moral frameworks, value conflicts, duty/consequence |
| 6  | `futurist`             | Scenarios, trend analysis, weak signals        |
| 7  | `historian`            | Source analysis, causation, continuity/change  |
| 8  | `journalist`           | 5 Ws, fact-checking, newsworthiness            |
| 9  | `lawyer`               | Statutes, case law, legal reasoning            |
| 10 | `novelist`             | Narrative structure, character, dramatic tension |
| 11 | `philosopher`          | Logic, epistemology, critical analysis         |
| 12 | `political-scientist`  | IR theory, institutions, governance            |
| 13 | `psychologist`         | Cognition, behavior, motivation, bias          |
| 14 | `sociologist`          | Social structures, stratification, norms       |

## How to Use

### Step 1: Present the Menu

When the user requests analysis, show the available analysts and ask which they want. Keep it short:

> Pick your analysts (you can combine multiple):
> 1. Anthropologist — culture & ritual
> 2. Computer Scientist — algorithms & systems
> 3. Economist — markets & incentives
> 4. Engineer — trade-offs & failure modes
> 5. Ethicist — moral frameworks
> 6. Futurist — scenarios & trends
> 7. Historian — causation & context
> 8. Journalist — facts & newsworthiness
> 9. Lawyer — legal reasoning
> 10. Novelist — narrative & character
> 11. Philosopher — logic & epistemology
> 12. Political Scientist — institutions & power
> 13. Psychologist — cognition & behavior
> 14. Sociologist — social structures
>
> Or say "all" / "surprise me" / pick a combo like "5, 7, 11"

### Step 2: Load Selected References

For each analyst the user picks, load the corresponding reference file:

```
references/<analyst>/<analyst>.md
```

Example: If user picks economist and ethicist, load:
- `references/economist/economist.md`
- `references/ethicist/ethicist.md`

For a quick summary, you can optionally load:
```
references/<analyst>/QUICK_REFERENCE.md
```

**Do NOT load analysts the user didn't select.**

### Step 3: Run the Analysis

For each loaded analyst, apply their disciplinary lens to the user's topic:

- Follow the frameworks, methods, and rubrics defined in each analyst's `<analyst>.md`
- Each analyst has theoretical foundations, analytical frameworks, step-by-step processes, and quality standards
- Apply them faithfully — don't water down the discipline

### Step 4: Synthesize (When Multiple Analysts)

When 2+ analysts are selected, add a synthesis section after the individual analyses:

- **Convergences**: Where do the lenses agree or reinforce each other?
- **Tensions**: Where do they conflict or highlight different priorities?
- **Blind spots**: What does each lens miss that another catches?
- **Combined insight**: What emerges from the multi-lens view that no single lens provides?

Keep synthesis concise — the individual analyses carry the depth.

## Operating Modes

### Single Analyst
Deep dive into one disciplinary perspective. Load the full `<analyst>.md` and run their complete analysis process.

### Multi-Analyst (2-4)
Run each analyst independently, then synthesize. This is the sweet spot — enough diversity without becoming a literature review.

### Full Panel (5+)
For broad exploratory analysis. Use QUICK_REFERENCE.md versions instead of full `<analyst>.md` to keep output manageable. Synthesize at the end.

### "Surprise Me" Mode
Pick 3-4 analysts that offer maximum perspective diversity for the topic. Default combo: pick one from each cluster:
- **Social/Cultural**: anthropologist, sociologist, psychologist
- **Technical**: engineer, computer-scientist
- **Abstract**: philosopher, ethicist, futurist
- **Applied**: economist, lawyer, journalist, political-scientist
- **Creative**: novelist, historian

## Quick Reference Table

| Need                        | Load                                     |
|-----------------------------|------------------------------------------|
| Full analytical framework   | `references/<analyst>/<analyst>.md`      |
| Quick overview / cheat sheet| `references/<analyst>/QUICK_REFERENCE.md`|
| Self-test / quiz            | `references/<analyst>/tests/quiz.md`     |

## Rules

1. **Always ask first** — never load analysts without user selection (unless they said "all" or "surprise me")
2. **Load on demand** — only read reference files for selected analysts
3. **Respect the discipline** — each analyst has real frameworks; apply them properly, don't just slap labels on generic advice
4. **Synthesize when multi** — combining lenses is the whole point; don't just concatenate independent analyses
5. **Match depth to request** — quick question = QUICK_REFERENCE.md; deep analysis = full `<analyst>.md` process
