# Skill: Brief Writing

You have loaded this skill because it's time to write a brief — a directional guide for investigation, testing, review, or exploration.

A brief is **not** a step-by-step recipe. It's a compass. The agent reading this has judgment, can explore, and will report back findings.

---

## WHEN TO WRITE A BRIEF VS PLAN

| Write a **Brief** | Write an **Implementation Plan** |
|---|---|
| "Find out why X is slow" | "Add caching to X endpoint" |
| "Test the auth flows thoroughly" | "Write unit tests for auth module" |
| "Review this module for bugs" | "Fix the bug in line 42" |
| "Investigate memory usage" | "Implement connection pooling" |
| Exploratory, open-ended | Prescriptive, atomic steps |
| Agent uses judgment | Agent follows instructions blindly |

**Brief = direction + context + success criteria**  
**Plan = exact steps + success/failure branches**

---

## BRIEF FORMAT

```markdown
# Brief: [Title]
_[One sentence. What are we trying to learn or achieve?]_

---

## Target Agent
[Who should pick this up? Anubis, Osiris, or general exploration]

## Context
[What's the situation? What's been tried? What's suspicious?
Real file paths, real function names, real symptoms observed.]

---

## Focus Areas
[Where to look. What to pay attention to. Specific files, functions, patterns.
Be specific but don't prescribe exact steps.]

- `path/to/file.ts` — [why this file matters]
- `functionName()` in `other/file.ts` — [suspicion or relevance]
- Pattern: [what pattern to search for across codebase]

## Hypotheses *(optional)*
[If you have theories about what might be wrong or where issues lie.
The agent can confirm or rule these out.]

1. [Hypothesis 1]
2. [Hypothesis 2]

---

## Deliverable
[What does "done" look like? What should the agent produce or report?]

- [ ] [Finding 1]
- [ ] [Finding 2]
- [ ] [Recommendation or conclusion]

## Out of Scope
[What should the agent NOT spend time on. Boundaries to respect.]
```

---

## BRIEF RULES

| Rule | Meaning |
|---|---|
| **Directional, not prescriptive** | Point the agent where to look, don't tell them exactly what to do |
| **Context-rich** | Provide enough background that the agent understands the landscape |
| **Real paths** | Use actual file paths, function names, not placeholders |
| **Clear deliverable** | The agent should know what success looks like when they see it |
| **Scoped** | Define what's out of bounds to prevent endless exploration |

---

## EXAMPLE BRIEF

```markdown
# Brief: Investigate Slow Dashboard Load
_The dashboard takes 8+ seconds to load. Find out why._

---

## Target Agent
Anubis

## Context
Users report the main dashboard (`src/pages/Dashboard.tsx`) takes 8-12 seconds on first load. 
Backend logs show the `/api/dashboard` endpoint responds in ~6 seconds. Frontend rendering 
adds another 2-4 seconds. Need to identify bottlenecks and propose fixes.

Relevant files:
- `src/pages/Dashboard.tsx` — main component
- `src/api/dashboard.ts` — data fetching
- `backend/routes/dashboard.ts` — backend endpoint

---

## Focus Areas

- `backend/routes/dashboard.ts` — the endpoint logic. Check for N+1 queries, missing indexes, or unnecessary joins.
- `src/api/dashboard.ts` — are we fetching more data than needed? Multiple sequential requests?
- `src/pages/Dashboard.tsx` — heavy re-renders? Large component tree? Missing memoization?
- Database queries — look for queries without proper indexing or doing full table scans.

## Hypotheses

1. The dashboard fetches data for 12 widgets in sequence rather than parallel
2. User permissions check runs a heavy query per widget instead of once
3. Frontend re-renders entire dashboard on any state change

---

## Deliverable

- [ ] Root cause identified with evidence (logs, profiling, code analysis)
- [ ] List of specific bottlenecks found with file:line references
- [ ] Recommended fix approach for each bottleneck (no implementation needed)

## Out of Scope
- Don't implement fixes — just identify and recommend
- Don't investigate other pages or endpoints
- Don't look at network/infrastructure layer (this is app-level only)
```

---

## PRE-HANDOFF CHECKLIST

Before saving the brief, verify:

- [ ] Target agent is specified (who should read this)
- [ ] Context provides enough background without being a wall of text
- [ ] Focus areas point to real files/functions, not vague "the auth code"
- [ ] Deliverable is clear — agent knows what to produce
- [ ] Out of scope prevents scope creep

When ready: **"Brief complete. Handing off."**

Save to `.agents/reports/brief_{short-name}_{yyyy-mm-dd}.md`
