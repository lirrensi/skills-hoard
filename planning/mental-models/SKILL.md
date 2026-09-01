---
name: mental-models
description: Use then user wants to have a thinking session against common biases, errors, and so on. Contains a huge library of thinking tools to check for.
---
# Mental Models — Thinking Pattern Library

## What This Is

A reference library of reusable thinking patterns, logical fallacies, cognitive biases, and reasoning tools. Not a skill that *does* something — a skill you *consult*. Like having a bookshelf of thinking tools that other skills (and you) can pull from.

Every other skill in the library uses these patterns implicitly. This makes them explicit, searchable, and learnable.

## When to Use

- "What mental model applies here?"
- "Am I falling for a fallacy or bias?"
- "What's the name for that thinking pattern?"
- "How should I reason about this uncertainty?"
- "Is my argument well-structured?"
- "Am I framing this problem correctly?"
- Reference during any thinking session
- Teaching and learning
- "I feel like there's a principle I'm missing"

---

## Important: Explain Your Terms

When using mental models in conversation or output, **always explain the term in plain language**. Don't just drop jargon.

**Bad:** "You should apply bounded rationality here."
**Good:** "You're dealing with bounded rationality — the idea that we can't be perfectly rational because we have limited time and information, so we pick the first good enough option."

**Bad:** "This is a classic case of hedonic adaptation."
**Good:** "This is hedonic adaptation — we return to baseline happiness after positive events, so the new car will feel great for a while, then become normal."

**Rule of thumb:** If the term has a Wikipedia page, assume the user doesn't know it. Define it once, then use it freely.

---

## Decision Tree: Which Reference to Consult

```
User asks about...
│
├─ "What model/framework applies here?"
│  └─→ references/mental-models.md
│      (40+ models: decision, systems, strategy, human nature, creativity, growth)
│
├─ "Is this a fallacy?" / "Bad logic" / "Invalid argument"
│  └─→ references/fallacies.md
│      (25+ fallacies: relevance, presumption, ambiguity, statistical, systemic)
│
├─ "Am I biased?" / "Is this a cognitive bias?"
│  └─→ references/cognitive-biases.md
│      (70+ biases clustered by task: estimation, decision, hypothesis, attribution, recall, social)
│
├─ "How should I reason about this?" / "What kind of thinking is this?"
│  └─→ references/reasoning-patterns.md
│      (Deduction, induction, abduction, Bayesian updating, causal reasoning)
│
├─ "How do I handle uncertainty?" / "What are the odds?" / "Should I gather more info?"
│  └─→ references/uncertainty-tools.md
│      (Expected value, base rates, calibration, fat tails, scenario planning)
│
├─ "Is this a good argument?" / "How do I evaluate evidence?"
│  └─→ references/argumentation.md
│      (Burden of proof, evidence hierarchies, steelmanning, falsifiability)
│
├─ "Am I thinking about this correctly?" / "How do I check my own reasoning?"
│  └─→ references/metacognition.md
│      (Notice confusion, confidence calibration, circle of competence, thinking hygiene)
│
├─ "Am I solving the right problem?" / "How should I frame this?"
│  └─→ references/problem-framing.md
│      (Reframing, root cause analysis, Cynefin framework, constraint analysis)
│
├─ "Why do people/teams behave this way?" / "Group dynamics" / "Social patterns"
│  └─→ references/social-dynamics.md
│      (Groupthink, social proof, coordination, incentives, status games, tribalism)
│
├─ "Why do I/others feel/act this way?" / "Human psychology" / "Motivation"
│  └─→ references/psychological-realities.md
│      (Hedonic adaptation, cognitive dissonance, flow state, loss aversion, identity)
│
├─ "How does time/change affect this?" / "Statistics" / "Distributions" / "Math intuition"
│  └─→ references/quantitative-intuitions.md
│      (Power laws, mean reversion, compounding, fat tails, Goodhart's Law, S-curves)
│
└─ "What model/framework applies here?"
   └─→ references/mental-models.md
       (50+ models: decision, systems, strategy, human nature, creativity, growth, action)
```

---

## Reference Index

| File | Contents | Model Count |
|------|----------|-------------|
| `references/mental-models.md` | Core mental models across 9 categories | ~50 models |
| `references/fallacies.md` | Logical fallacies with detection guide | ~25 fallacies |
| `references/cognitive-biases.md` | Cognitive biases clustered by task type | ~70 biases |
| `references/reasoning-patterns.md` | How conclusions are formed | ~10 patterns |
| `references/uncertainty-tools.md` | Probability and uncertainty tools | ~12 tools |
| `references/argumentation.md` | Building and evaluating arguments | ~10 concepts |
| `references/metacognition.md` | Thinking about thinking | ~12 practices |
| `references/problem-framing.md` | Defining problems before solving them | ~10 techniques |
| `references/psychological-realities.md` | How humans actually work (not errors, features) | ~20 models |
| `references/social-dynamics.md` | How groups, networks, and collective behavior work | ~20 models |
| `references/quantitative-intuitions.md` | How numbers, time, and distributions actually behave | ~20 models |

---

## Output Format

When consulted during a thinking session:

```markdown
## Applicable Thinking Tools

### 🧭 Sense-Making (How to see this)
1. **[Model/Pattern Name]** — [one-line explanation]
   → How it applies: [specific to user's context]
   → Watch out for: [common misuse]

### ⚡ Action (What to do)
2. **[Model/Pattern Name]** — [one-line explanation]
   → Actionable step: [concrete next action]

### 🚨 Errors Detected
- **[Fallacy/Bias Name]** — [where it appears in user's reasoning]
  → Fix: [how to correct the thinking]

### 🔍 Check Your Thinking
- **[Meta-cognitive practice]** — [what to examine about your own reasoning]

### 📚 Related Reading
- [Other models/patterns that might also apply]
```

---

## Cross-Reference Map

Some situations pull from multiple reference files:

| Situation | Primary | Also Check |
|-----------|---------|------------|
| Making a decision under uncertainty | `uncertainty-tools.md` | `mental-models.md` (decision section), `cognitive-biases.md` (decision biases) |
| Evaluating someone's argument | `fallacies.md` | `argumentation.md`, `cognitive-biases.md` (hypothesis assessment) |
| Planning a project | `problem-framing.md` | `mental-models.md` (systems section), `quantitative-intuitions.md` (S-curves, compounding) |
| Debugging your own thinking | `metacognition.md` | `cognitive-biases.md`, `reasoning-patterns.md` |
| Preparing for a debate | `argumentation.md` | `fallacies.md`, `reasoning-patterns.md` |
| Understanding why a group made a bad decision | `social-dynamics.md` | `cognitive-biases.md` (social section), `psychological-realities.md` |
| Choosing a strategy | `mental-models.md` (strategy section) | `uncertainty-tools.md`, `problem-framing.md`, `quantitative-intuitions.md` |
| Learning a new skill | `mental-models.md` (growth section) | `metacognition.md` (circle of competence), `psychological-realities.md` (flow state) |
| Understanding someone's behavior | `psychological-realities.md` | `cognitive-biases.md` (attribution section), `social-dynamics.md` |
| Analyzing risk over time | `quantitative-intuitions.md` | `uncertainty-tools.md` (fat tails), `mental-models.md` (inversion) |
| Designing incentives or systems | `social-dynamics.md` | `mental-models.md` (incentives), `quantitative-intuitions.md` (Goodhart's Law) |

---

## Quick Reference: Top 10 Most Useful

If you only remember ten, remember these:

1. **Inversion** — Ask "how to fail" to find success paths
2. **Second-Order Thinking** — "And then what?"
3. **Map vs Territory** — Your model is not reality
4. **Bayesian Updating** — Update beliefs proportionally to evidence
5. **Opportunity Cost** — What you give up by choosing
6. **Steel-manning** — Argue the strongest version of the opposition
7. **Circle of Competence** — Know what you don't know
8. **Root Cause Analysis** — Ask "why" five times
9. **Confirmation Bias** — The most common and dangerous bias
10. **Reversible vs Irreversible** — Decide fast or slow based on reversibility
