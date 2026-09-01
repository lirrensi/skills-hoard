# Ideation Phase (02)

Assess research novelty and formalize mathematical foundations.

## Skills Consolidated

- **novelty-assessment**: Multi-round search-evaluate loops with harsh critic persona
- **math-reasoning**: Mathematical derivations, proofs, notation formalization

## Novelty Assessment Workflow

### Step 1: Define Research Idea
Clearly articulate:
- Core contribution
- Problem being solved
- Proposed approach
- Expected improvements

### Step 2: Multi-Round Search-Evaluate Loop
Run 5-10 rounds of:
1. **Search**: Find closest related work
2. **Evaluate**: Compare your idea against each paper
3. **Refine**: Adjust idea to differentiate or strengthen

### Step 3: Harsh Critic Persona
Generate adversarial critique:
- "This is just X from [paper] with minor changes"
- "The improvement is marginal (<5%)"
- "Method Y already achieves this"

### Step 4: Binary Decision
Output one of:
- **NOVEL**: Clear differentiation, significant contribution
- **NOT NOVEL**: Subsumed by existing work, incremental only

## Novelty Assessment Output

```markdown
# Novelty Assessment: [Idea Name]

## Core Contribution
[Clear statement of what's new]

## Closest Related Work
1. [Paper 1] - Similar in X, different in Y
2. [Paper 2] - Addresses Z but not A
3. [Paper 3] - Uses B approach, we use C

## Key Differentiators
- Differentiator 1 (quantified if possible)
- Differentiator 2
- Differentiator 3

## Critic's Harsh Assessment
"[Toughest critique generated]"

## Response to Critic
"[Direct counter-argument with evidence]"

## Verdict: [NOVEL / NOT NOVEL]
Confidence: High/Medium/Low

## Recommendation
[Proceed / Pivot / Abandon]
```

## Math Reasoning

### Notation Formalization

**Define clearly**:
- Variable names (consistent case: $x$ for vectors, $X$ for matrices)
- Domains ($x \in \mathbb{R}^d$)
- Operators and their meanings
- Assumptions explicitly stated

### Proof Templates

Use structured proof formats:

```latex
\begin{theorem}[Name]
Statement of theorem
\end{theorem}

\begin{proof}
\textit{Proof.} Step-by-step derivation...
\end{proof}
```

### Statistical Test Selection

| Scenario | Test | Assumptions |
|----------|------|-------------|
| Compare 2 means (paired) | Paired t-test | Normal distribution |
| Compare 2 means (independent) | Independent t-test | Equal variance, normal |
| Compare >2 means | ANOVA | Normal, equal variance |
| Non-parametric 2-group | Mann-Whitney U | Ordinal or non-normal |
| Correlation (linear) | Pearson | Normal, linear |
| Correlation (monotonic) | Spearman | Ordinal or non-normal |
| Categorical association | Chi-square | ≥5 expected per cell |

### Common Derivations

**Gradient of loss function**:
```
L = ||y - f(x; θ)||²
∂L/∂θ = -2(y - f(x; θ)) · ∂f/∂θ
```

**Bayes' theorem**:
```
P(H|E) = P(E|H) · P(H) / P(E)
```

## Validation Checklist

- [ ] Novelty verdict is binary and justified
- [ ] At least 5 closest papers identified
- [ ] Critic persona generated and responded to
- [ ] All notation defined before first use
- [ ] Statistical tests match data characteristics
- [ ] Proofs have clear theorem-proof structure

## Reference Files

- **Notation guide**: See original `math-reasoning/references/notation-guide.md`
- **Proof templates**: See original `math-reasoning/references/proof-templates.md`
- **Assessment prompts**: See original `novelty-assessment/references/assessment-prompts.md`

## Downstream

- **Feeds into**: Phase 03 (experiments design), Phase 05 (methods section)
- **Reference files**: `refs/03-experiments-phase.md`, `refs/05-writing-phase.md`