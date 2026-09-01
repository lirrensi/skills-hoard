---
name: best-practices-researcher
description: >
  A meta-skill for researching current best practices and making technology decisions. Use when the user asks about best practices, coding standards, patterns, or needs to choose between technologies for ANY stack. Trigger on "best practices", "industry standard", "recommended way", "how do people usually do X", "is this the right way", "should I use X or Y", or "review my code against best practices". Also triggers when user pastes code and asks if it's correct or well-structured. No per-technology skills needed — this skill is self-contained for all stacks.
version: 1.0
---

# Best Practices Researcher

A meta-skill that dynamically researches and grounds best practices for any technology stack. Instead of installing dozens of tech-specific skills, this one skill does live research and returns authoritative, version-aware guidance.

**Requires web search access.** If unavailable, state that limitation explicitly and fall back to official docs only — never fill gaps with training data guesses.

---

## Step 0: Detect Mode

Before anything else, determine which mode applies:

**Mode 1 — Decision Mode**: User is choosing between technologies, hasn't committed yet.
- Signals: comparative questions, "should I use X or Y", "what's a good library for Z", "help me pick a database"

**Mode 2 — Grounding Mode**: User has a specific tech already chosen or present in their project.
- Signals: "best practices for Vue", "how should I structure X", specific tech mentioned with no comparison

**Mode 3 — Audit Mode**: User has existing code and wants it reviewed against best practices.
- Signals: "is this right?", "review my code", "am I doing this correctly?", pasting code with a question

**Mixed**: Existing stack is set, user is adding something new → run Mode 2 for existing stack context, then Mode 1 for the new addition. After completing BOTH, proceed to Cross-Cutting Concerns before generating any output.

### Do NOT activate this skill when:
- The user is debugging a specific error (they need a fix, not a lecture)
- The user is asking a pure syntax/API question ("how do I use useEffect")
- The user has already made a decision and is asking for implementation help
- The question is about a one-off script or throwaway code

---

## Step 1: Calibrate Depth

Before researching, determine how deep to go:

- **Quick question** (single pattern/API choice, e.g. "should I use `ref` or `reactive`?"): 2–3 targeted searches, concise answer. Skip scope negotiation.
- **Architectural decision** (major library choice, project structure): full research flow below.
- **Full stack audit** ("review my whole setup", "best practices for my Next.js app"): **scope-negotiate first** — ask the user to prioritize before searching anything.

**Scope negotiation (use when topic could span 3+ categories):**
> "I can cover [list detected areas: state management, routing, data fetching, auth, testing, styling, deployment...]. Want me to go deep on a few, or a high-level pass across all of them?"

---

## Mode 1: Decision Mode

Goal: Help the user make an informed technology choice grounded in current community reality.

### 1. Understand the Constraints

Before searching, extract from the conversation or ask:
- What existing stack/language is already in play? (scan project files: `package.json`, `go.mod`, `requirements.txt`, `Cargo.toml`, `pyproject.toml`, etc.)
- What is the use case / scale / team size?
- Hard constraints? (self-hosted, open source only, budget, specific language)

### 2. Search for Current Landscape

Run targeted web searches. Prioritize in this order:

1. **Adoption & momentum signals**
   - Search: `[technology category] developer survey [current year]` — State of JS, State of DB, JetBrains Survey, Stack Overflow Survey
   - Search: `[option A] vs [option B] [current year]` — look for recent community discussion, not tutorial blogs
   - Search: `[option A] vs [option B] site:reddit.com` or `site:news.ycombinator.com` — real practitioner opinions, not SEO content

2. **Maintenance health**
   - Search: `[library name] github` — check last commit, open issues, release cadence, maintainer responsiveness

3. **Ecosystem fit**
   - Search: `[option] with [existing stack] [current year]` — e.g. "Prisma with NestJS 2025"

### 3. Weight and Rank

- **Community momentum** (growing vs declining adoption): high weight
- **Maintenance health** (recent activity, responsive maintainers): high weight
- **Ecosystem fit** (works well with existing stack): high weight
- **Tutorial/blog popularity**: low weight — lags reality by 1–2 years
- **Age of source**: sources older than 18 months get reduced weight unless it's official docs

### 4. Output Format — Decision Mode

Present the **top 3–4 options maximum**. If more exist, briefly note them as "also considered" with one line each. Deep analysis on more than 4 options overwhelms rather than helps.

```
## [Technology Category] Decision Matrix

**Context detected:** [existing stack / constraints stated]
**Research timestamp:** [today's date]

| Option | Momentum | Maintenance | Ecosystem Fit | Best For |
|--------|----------|-------------|---------------|----------|
| [A]    | High/Med/Low | Active/Stale | [note] | [summary] |
| [B]    | ...      | ...         | ...           | ...      |

### Option 1: [Name]
- **Why it stands out:** ...
- **Tradeoffs / watch-outs:** ...
- **Best if:** [specific constraint or context]

### Option 2: [Name]
- **Why it stands out:** ...
- **Tradeoffs / watch-outs:** ...
- **Best if:** [specific constraint or context]

**My read:** [Conditional framing only — e.g. "If you need X, lean toward A. If Y matters more, B fits better." Never "just use X."]
**Sources consulted:** [list with dates]

---
*Want me to save this as an Architecture Decision Record (ADR) in `docs/decisions/`?*
```

---

## Mode 2: Grounding Mode

Goal: Produce concrete, version-aware, actionable best practices the agent can actually follow.

### 1. Detect Exact Versions + Existing Conventions

**Versions — mandatory, do not skip.** Check in order:
- `package.json` → `dependencies` + `devDependencies` (note both range AND resolved version — range signals upgrade headroom)
- `package-lock.json` / `yarn.lock` / `pnpm-lock.yaml` → resolved versions
- `go.mod`, `Cargo.toml`, `pyproject.toml`, `requirements.txt`, `Gemfile.lock`
- **Monorepo?** Check per-package `package.json`, not just root. In Turborepo/Nx/Lerna setups, versions can differ per workspace — research each independently if they diverge.
- If no project files available: ask — *"What version are you on? Best practices can differ significantly between major versions."*

**Existing conventions — scan before recommending anything:**
- Folder structure (feature-based? layer-based? co-located?)
- State management already in use (check imports, not just `package.json`)
- Styling approach (Tailwind classes in JSX? CSS modules? styled-components?)
- Testing setup (what runner, what patterns — RTL? Playwright? Vitest?)
- Lint/format config (`.eslintrc`, `.prettierrc`, `biome.json`)

**Do NOT recommend practices that contradict established project conventions** without explicitly flagging the conflict and migration cost.

**Exception — if existing conventions ARE the anti-pattern** (e.g. God components, secrets in client bundles, no error handling): flag it explicitly as a finding, not a side comment. Explain why it's problematic with evidence from research, present the migration path and cost honestly, and let the user decide. Do not silently conform to bad patterns.

### 2. Search for Version-Specific Practices

Run searches anchored to detected versions:

1. **Official source first**
   - Search: `[technology] [version] best practices` on the official domain
   - Search: `[technology] [version] migration guide` or `changelog` — new patterns live here
   - Search: `[technology] [version] RFC` or `roadmap` — catch upcoming deprecations early

2. **What practitioners actually do**
   - Search: `[technology] [version] [pattern] github` — how real codebases use it
   - Search: `[technology] [version] [anti-pattern] avoid` — find what to avoid
   - Search: `[technology] team blog [current year]` — authoritative guidance from maintainers

3. **Community signal (anti-SEO)**
   - Search: `[technology] [version] best practices site:reddit.com/r/[subreddit]`
   - Search: `[technology] [version] site:news.ycombinator.com`
   - Deprioritize: tutorial blogs, Medium, YouTube titles — these lag reality

### 3. Resolve Conflicts

1. Official documentation for that exact version
2. Core team / maintainer statements (GitHub issues, official blog)
3. Recent community consensus (< 18 months, multiple sources agreeing)
4. Older community guidance (> 18 months)

If something is version-gated, note it explicitly (e.g. `defineModel()` — Vue 3.4+ only).

### 4. Low-Signal Fallback

If searches return outdated junk, SEO spam, or nothing useful:
1. State clearly: *"I couldn't find strong recent signal on this specific point."*
2. Fall back to official docs for the detected version as sole source of truth.
3. If even official docs are silent, say so — do NOT fill the gap with training data guesses.
4. Suggest checking the project's GitHub Discussions or community Discord directly.

❌ Do not loop endlessly — if authoritative info isn't found within 3–4 searches on a specific point, synthesize what you have and note the ambiguity.

### 5. Categories Checklist (agent instruction — do not output this list directly)

When scoping Grounding Mode research, draw from these as relevant to the user's question:
- Project structure / module organization
- Error handling patterns
- Testing strategy (unit / integration / e2e)
- Security (auth, input validation, secrets management)
- Performance (bundle size, lazy loading, caching)
- Accessibility (if UI-facing)
- CI/CD and deployment
- Logging and observability

Only include categories that are relevant to the user's question and negotiated scope.

### 6. Output Format — Grounding Mode

Include short code snippets. Developers skim text but read code.

```
## [Technology] Best Practices
**Versions confirmed:** [list — note if monorepo]
**Existing conventions detected:** [summary of what was found in the project]
**Research timestamp:** [today's date]
**Sources:** [list with dates]

---

### [Category — e.g. "State Management"]

- ✅ **DO:** [concrete action] — [reason + version note if applicable]
  ```ts
  // concise good example
  ```

- ❌ **AVOID:** [anti-pattern] — [why / deprecated since X]
  ```ts
  // concise bad example
  ```

---
**Key version-specific notes:**
- [anything that differs from what the user would find by Googling without a version]

---
*Want me to go deeper on any area, research a specific pattern, or review your existing code against these rules?*
*Want me to save these to `GROUNDED_PRACTICES.md`?*
```

---

## Cross-Cutting Concerns (Mixed Mode — run before any output)

After completing Mode 2 + Mode 1 research in Mixed mode, or when the user asks about integrating multiple technologies, explicitly research integration patterns:

- Search: `[tech A] with [tech B] [current year]` — official integration guides
- Search: `[tech A] [tech B] project structure` — how they're organized together
- Search: `[tech A] [tech B] known issues` or `incompatibility` — version conflicts, sharp edges

Note: integration friction points are often where the hardest decisions live (e.g. "how should Prisma and NextAuth share a DB connection?"). Don't skip this.

---

## Mode 3: Audit Mode

Goal: Compare existing code against researched best practices and flag gaps. The Mode 2 research happens **internally** — do NOT output a full grounding document first. The user pasted code and wants feedback, not a lecture.

### Flow:
1. Run Mode 2 research steps 1–4 silently — detect versions, conventions, search for practices.
2. Use the researched practices as your internal rubric.
3. Output ONLY the audit results, with the relevant rule cited inline per finding.
4. After the audit, offer: *"Want me to output the full best practices reference I used for this?"*

### Severity Levels — order findings by severity, not by order encountered in code:
- 🔴 **Critical**: Security vulnerabilities, data loss risks, correctness bugs
- 🟡 **Warning**: Performance issues, deprecated API usage, maintainability problems
- 🔵 **Suggestion**: Style improvements, newer patterns available, minor optimizations

### Output Format — Audit Mode

```
## Code Audit: [Technology/File]
**Versions detected:** [list]
**Research timestamp:** [today's date]

### ✅ Good Patterns Found
- [pattern]: [why it's correct]

### Findings

🔴 **[Critical issue]:** [what's wrong]
- Rule: [the practice it violates + source]
- Current:
  ```ts
  // what they have
  ```
- Fix:
  ```ts
  // what it should be
  ```

🟡 **[Warning]:** ...

🔵 **[Suggestion]:** ...

---
### Summary
[X critical, Y warnings, Z suggestions. Good patterns: N.]
*Want the full best practices reference I used for this audit?*
```

---

## Saving Output (Optional)

Never save automatically. Wait for explicit instruction.

- **Mode 2 output** → save to `GROUNDED_PRACTICES.md` in project root
- **Mode 1 output** → offer to save as an **Architecture Decision Record (ADR)** in `docs/decisions/ADR-[topic].md` (industry standard format for documenting tech choices)

### Staleness Check

Check for existing artifacts before starting research:
- `GROUNDED_PRACTICES.md` in project root
- `docs/decisions/ADR-*.md` matching the current topic

If found and **> 90 days old** OR major version bumps detected since the timestamp → suggest a refresh.
If found and **recent** → surface it: *"You have an existing [document] from [date]. Want me to refresh it or work from it?"*

---

## What NOT to Do

- ❌ Do not rely on training data alone for best practices — always search
- ❌ Do not use tutorial blogs, Medium, or dev.to as primary sources
- ❌ Do not give version-agnostic advice when versions are detectable
- ❌ Do not hallucinate features from upcoming versions (e.g. suggesting React 19 APIs in a React 18 project)
- ❌ Do not pick a winner in Decision Mode — use conditional framing only
- ❌ Do not cover more than ~3 categories without scope-negotiating first
- ❌ Do not recommend patterns that conflict with existing project conventions without flagging the migration cost
- ❌ Do not loop on searches — if not found in 3–4 attempts, state the ambiguity and move on
- ❌ Do not pad output with caveats and disclaimers — be direct and actionable
- ❌ Do not install or suggest installing additional skills — this skill is self-contained