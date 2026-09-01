# Reasoning Patterns Library

How conclusions are formed — the engines of thought.

---

## Core Reasoning Modes

| Mode | What It Is | When It Matters |
|------|-----------|-----------------|
| **Deductive** | General rule → specific conclusion. If A then B; A; therefore B. Valid if premises are true. | Logic, math, formal argument, applying known rules |
| **Inductive** | Specific observations → general rule. "Every swan I've seen is white → all swans are white." | Science, pattern recognition, learning from experience |
| **Abductive** | Observed result → most likely explanation. "Best inference to the best explanation." | Diagnosis, debugging, detective work, medical reasoning |
| **Analogical** | This situation resembles that one → transfer the lesson | Strategy, creativity, communication, teaching |
| **Dialectical** | Thesis + antithesis → synthesis. Working through contradictions. | Debate, philosophy, resolving conflicting viewpoints |
| **Counterfactual** | "What if X had been different?" — reasoning about alternate realities | Post-mortems, causal understanding, learning from history |

---

## Bayesian Updating

The mathematically correct way to change your mind.

**Formula:** Posterior = Prior × Likelihood of Evidence

| Step | What to Do |
|------|-----------|
| 1. **Start with a prior** | What did you believe before seeing this evidence? Assign a probability. |
| 2. **Evaluate the evidence** | How likely is this evidence if your belief is true? How likely if it's false? |
| 3. **Update proportionally** | Strong evidence shifts belief more. Weak evidence shifts it less. |
| 4. **Repeat** | Your posterior becomes the next prior. Beliefs evolve continuously. |

**Key principles:**
- Extraordinary claims require extraordinary evidence (evidence must be very unlikely under the null)
- Weak evidence shouldn't flip you from 5% to 95%
- Your prior matters — two rational people can look at the same evidence and reach different conclusions
- Base rate neglect is the most common Bayesian error

**When to use:** Any ongoing learning under uncertainty. Forecasting, science, diagnosis, investment decisions.

---

## Causal Reasoning

Distinguishing mechanism from coincidence.

| Concept | What It Is | Example |
|---------|-----------|---------|
| **Necessary vs Sufficient** | Necessary = must be present for outcome. Sufficient = guarantees outcome on its own. | Oxygen is necessary for fire but not sufficient (need fuel + heat) |
| **Proximate vs Root Cause** | Proximate = immediate trigger. Root = underlying condition. | Proximate: server crashed. Root: no monitoring system. |
| **Confounders** | Third variable that causes both X and Y, creating false correlation | Ice cream sales correlate with drowning — confounder is summer heat |
| **Mechanism** | The actual causal pathway, not just correlation | Aspirin reduces pain *because* it inhibits prostaglandins |
| **Counterfactual Thinking** | "Would Y have happened without X?" | Would the project have failed without the budget cut? |
| **Intervention Effects** | What happens when you actively change X vs just observing it | Observational data ≠ experimental data |

---

## Reasoning Mode Selection Guide

| If the situation is... | Use this mode |
|------------------------|---------------|
| Applying known rules to a specific case | **Deductive** |
| Looking for patterns in data | **Inductive** |
| Something is broken and you need to figure out why | **Abductive** |
| You're in a new domain but have experience in a similar one | **Analogical** |
| Two smart people disagree and both have points | **Dialectical** |
| Analyzing what went wrong or could go wrong | **Counterfactual** |
| You have a belief and new evidence just arrived | **Bayesian Updating** |
| You need to understand *why*, not just *that* | **Causal Reasoning** |

---

## Common Reasoning Errors

| Error | What Goes Wrong |
|-------|----------------|
| **Using deduction with false premises** | Valid logic, wrong conclusion. "All birds fly. Penguins are birds. Therefore penguins fly." |
| **Over-generalizing from induction** | Small sample → big conclusion. "My two data points show a trend." |
| **Confusing correlation with causation** | Observing X and Y together, assuming X causes Y |
| **Anchoring on the first explanation** | Abduction stops at the first plausible explanation instead of considering alternatives |
| **Ignoring base rates** | Bayesian error — focusing on specific evidence while ignoring general statistics |
| **Motivated reasoning** | Starting from the conclusion you want and working backward |
