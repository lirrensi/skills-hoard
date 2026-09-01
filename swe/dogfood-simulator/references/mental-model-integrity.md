# Mental Model Integrity & Persona Lenses

## The Core Idea

Users build a mental model of how a product works. Every interaction either reinforces or violates that model. A product with strong mental model integrity feels "obvious" — users can predict how unfamiliar features will work. A product with weak integrity feels "full of bullshit" — unpredictable, contradictory, and exhausting.

Your job is to find the violations before they find the user.

---

## Mental Model Consistency

### The Predictability Test

After learning Feature A, can the user predict how Feature B works?

- If the product has multiple commands, do they share consistent flag naming? (-v always means verbose, -q always means quiet, --output always means output path)
- If the product has multiple pages, do they share consistent layout? (Navigation in same place, primary action in same place, help in same place)
- If the product has multiple endpoints, do they share consistent response shapes? (Same error format, same pagination format, same date format)
- Do similar concepts use the same words? (Not "project" on one page and "workspace" on another for the same thing)
- Do different concepts use different words? (Not "item" meaning three different things in three different contexts)

### The Contradiction Audit

Find every place the product contradicts itself:

- **Flag contradictions**: A flag works on one subcommand but not another, or works differently.
- **Behavior contradictions**: The same input produces different output depending on invisible state.
- **Terminology contradictions**: The same word means different things in different contexts.
- **Visual contradictions**: The same action looks different on different pages.
- **Flow contradictions**: The same workflow requires different steps depending on how you entered it.

### The Expectation Violation Audit

For each major interaction, ask:

1. **What would a reasonable user expect to happen?**
   - Based on how similar products work
   - Based on how this product works elsewhere
   - Based on the documentation or help text
   - Based on common conventions

2. **What actually happens?**
   - Is it different from the expectation?
   - Is the difference surprising or merely different?

3. **If it is different, is the difference justified?**
   - Is it better than the expected behavior?
   - Is it clearly communicated?
   - Does the user benefit from the difference, or is it an implementation artifact?

Expectation violations that are not clearly better AND clearly communicated are bugs. Even if the behavior is "correct" by the code — if it violates user expectation without good reason, it is a design bug.

### The Classification

| Type | Description | Severity |
|------|-------------|----------|
| **Consistent** | Behavior matches expectation and is consistent across similar features. | None — this is good. |
| **Surprising but Better** | Behavior differs from expectation but is clearly superior AND communicated. | Low — document the surprise. |
| **Arbitrarily Different** | Behavior differs from expectation for no clear benefit. Just different. | Medium — this taxes the user's mental model for no reason. |
| **Contradictory** | Behavior differs from similar feature elsewhere in the SAME product. | High — the product is fighting with itself. |
| **Hostile** | Behavior actively harms the user or violates a deeply held convention (e.g., Ctrl+C does not cancel). | Critical — the product is breaking trust. |

---

## Per-Feature Persona Lenses

Do not test the entire product as "a beginner" or "a power user." Instead, take each feature and apply multiple lenses. A single feature can be brilliant for power users and hostile to beginners. You need to see both.

### The Personas

| Persona | Mental state | Cares about | Will abandon if... |
|---------|-------------|-------------|-------------------|
| **First-Timer** | Curious but skeptical. Evaluating: "Is this worth learning?" | Quick wins, clear value, gentle onboarding | They cannot see value in 5 minutes. |
| **Daily User** | Productive. Wants speed, muscle memory, efficiency. | Shortcuts, batch ops, predictability, speed | The product slows them down or breaks their flow. |
| **Returning User** | Has context but it is stale. "How did this work again?" | Memory cues, history, consistency with their past experience | They cannot pick up where they left off. |
| **Automator** | Wants to embed the product in scripts/pipelines/CI. | Non-interactive mode, parseable output, exit codes, env config | The product requires human attention. |
| **Explorer** | Wants to discover what is possible. Pushes boundaries. | Progressive disclosure, undo, safety, "what happens if I..." | The product punishes exploration. |

### Applying the Lenses

For each feature you test, ask:

**First-Timer lens:**
- Is it obvious what this feature does from its name or placement?
- Can the user try it safely — with undo, preview, or no side effects?
- Does it show value immediately, or does it require setup?
- If it fails, does the error guide the user toward success?

**Daily User lens:**
- Is there a faster way to do this? (Keyboard shortcut, alias, template, default?)
- Does it behave consistently every time? (No invisible state changing the outcome?)
- Can it be batched or chained? (The daily user does many things, not just one.)
- Does it respect the user's time? (No unnecessary confirmations for safe actions.)

**Returning User lens:**
- Is the feature discoverable if you forgot it exists?
- Is there context or state that helps the user remember where they were?
- Does the feature work the same way it did when the user last used it?
- Is there a history or "recently used" mechanism?

**Automator lens:**
- Can this feature be used without human interaction?
- Can its output be parsed by a script?
- Are all configuration options available as flags or environment variables?
- Does it follow standard conventions for exit codes, stdout, stderr?

**Explorer lens:**
- What happens if the user tries this feature in an unusual way?
- Is there an undo or escape hatch if the result is undesirable?
- Does the feature reveal adjacent features naturally? (Discoverability for advanced use.)
- Does the product encourage exploration, or does it punish mistakes?

### Example: Applying Lenses to a "Create Project" Feature

**First-Timer lens findings:**
- "Create Project" button is prominent — good.
- But clicking it opens a form with 15 fields, most required. Overwhelming.
- No template or "quick create" option. User must understand all options upfront.
- **Finding**: Missing progressive disclosure. Force user to understand everything before they can create anything.

**Daily User lens findings:**
- No keyboard shortcut for "Create Project."
- Cannot duplicate an existing project as a starting point.
- Default values are not remembered from the last project created.
- **Finding**: Missing speed features for repeat users.

**Returning User lens findings:**
- Recent projects are shown, which is helpful.
- But there is no timeline or history of project creation.
- If the user last used this 3 months ago, the form looks the same — no indication of what changed.
- **Finding**: Good re-entry for finding old projects, poor re-entry for understanding what is new.

**Automator lens findings:**
- No CLI or API for creating projects. GUI only.
- Cannot import project configuration from a file.
- **Finding**: The feature is completely unavailable to automated workflows.

**Explorer lens findings:**
- Creating a project with experimental settings is risky — cannot preview the result.
- Some settings are irreversible after project creation.
- No "test project" or sandbox mode for experimentation.
- **Finding**: Punishes curiosity. Explorer will avoid touching settings.

---

## The Integrity Checklist

Run this for the entire product:

- [ ] Do similar features work similarly? (Commands, pages, endpoints, workflows)
- [ ] Does the same word always mean the same thing?
- [ ] Do different concepts always use different words?
- [ ] Can the user predict how Feature X works based on Feature Y?
- [ ] Are there any documented behaviors that contradict actual behavior?
- [ ] Are there any conventions the product violates? (Standard keyboard shortcuts, standard flag names, standard HTTP status codes)
- [ ] Would a user who learned a competitor product be confused by this product?
- [ ] Would a user who learned this product be confused by a new version?

If you answered "no" to any of these, there are mental model violations. Find them. Name them. They erode trust silently but permanently.
