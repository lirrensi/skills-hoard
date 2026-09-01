# Mode: Propose

**Trigger:** Asked to create a change proposal for a new feature, refactor, or significant modification. Produces a `docs/changes/<name>/` folder with proposal, behavior deltas, design, and tasks.

---

## Workflow

### Step 1: Gather
Read the relevant existing docs first:
- `docs/overview/` — to understand product context
- `docs/spec/` — to understand current behavior you're modifying
- `docs/architecture/` — to understand implementation constraints

Ask clarifying questions if behavior, constraints, or boundaries are unclear.

### Step 2: Create the change folder
```
docs/changes/<kebab-case-name>/
├── proposal.md      # Why + scope
├── behavior.md      # Delta spec: ADDED/MODIFIED/REMOVED
├── design.md        # Technical approach
└── tasks.md         # Implementation checklist
```

Name the folder with kebab-case, descriptive: `add-rate-limiting`, `fix-auth-timeout`, `refactor-session-store`.

### Step 3: Write proposal.md

```markdown
---
node_type: change-proposal
title: Add Rate-Limiting
status: draft
updated: YYYY-MM-DD
tags: [api, security, performance]
links:
  depends_on: [/spec/features/api.md]
---

# Proposal: {Title}

## Intent
{1 paragraph: why are we doing this? what problem does it solve?}

## Scope
**In scope:**
- {item 1}
- {item 2}

**Out of scope:**
- {item 1}

## Approach
{1 paragraph: high-level approach — what layers change, not how}
```

### Step 4: Write behavior.md (Delta Spec)

This is the most important artifact. It describes behavioral changes as deltas:

```markdown
---
node_type: change-behavior
title: Rate-Limiting Behavior Changes
status: draft
updated: YYYY-MM-DD
links:
  depends_on: [proposal.md]
  documents: [/spec/features/api.md]
---

# Behavior Changes: Rate-Limiting

## ADDED Requirements

### Requirement: Request Throttling
The system MUST reject requests that exceed the rate limit.

#### Scenario: User exceeds rate limit
- **GIVEN** a user who has made 100 requests in the last minute
- **WHEN** the user makes another request
- **THEN** the system rejects the request with HTTP 429
- **AND** the response includes a `Retry-After` header

### Requirement: Rate Limit Headers
The system MUST include rate limit headers in every API response.

#### Scenario: Successful request includes headers
- **GIVEN** a user who has made 50 requests in the last minute
- **WHEN** the user makes a valid request
- **THEN** the response includes `X-RateLimit-Remaining: 50`
- **AND** the response includes `X-RateLimit-Reset: {timestamp}`

## MODIFIED Requirements

### Requirement: Authentication
The system MUST track rate limits per authenticated user.
(Previously: rate limits were global per IP only.)

#### Scenario: Authenticated user has separate quota
- **GIVEN** an authenticated user and an anonymous user
- **WHEN** both make requests from the same IP
- **THEN** each has their own rate limit counter

## REMOVED Requirements

### Requirement: Global IP-Based Throttling
(Removed — per-IP throttling was too aggressive for NAT and shared office environments.)
```

**Delta rules:**
- **ADDED** — new behavior. Archive appends to main spec.
- **MODIFIED** — changed behavior. MUST include "(Previously: ...)" note. Archive replaces the requirement.
- **REMOVED** — deprecated behavior. MUST include reason. Archive deletes from main spec.

### Step 5: Write design.md

```markdown
---
node_type: change-design
title: Rate-Limiting Design
status: draft
updated: YYYY-MM-DD
links:
  depends_on: [proposal.md, behavior.md]
---

# Design: {Title}

## Technical Approach
{How we'll implement this. Algorithms, data structures, patterns.}

## Architecture Decisions

### Decision: Token Bucket over Sliding Window
{Decision, rationale, alternatives considered.}

### Decision: Redis over In-Memory
{Decision, rationale, alternatives considered.}

## Data Flow
{ASCII diagram or description of data/control flow.}

```
Client → Gateway → Rate Limiter → Service
                ↓
              Redis
```

## File Changes
- `src/middleware/rate-limit.ts` (new)
- `src/services/rate-limiter.ts` (new)
- `src/config/limits.ts` (modified)
```

### Step 6: Write tasks.md

```markdown
---
node_type: change-tasks
title: Rate-Limiting Tasks
status: draft
updated: YYYY-MM-DD
links:
  depends_on: [design.md]
---

# Tasks: {Title}

## 1. Core Implementation
- [ ] 1.1 Implement token bucket algorithm
- [ ] 1.2 Add Redis-backed rate limit storage
- [ ] 1.3 Implement rate limit middleware

## 2. Protocol & Headers
- [ ] 2.1 Add `X-RateLimit-*` headers to all responses
- [ ] 2.2 Implement `Retry-After` header for 429 responses
- [ ] 2.3 Add rate limit to OpenAPI schema

## 3. Testing & Validation
- [ ] 3.1 Test per-user rate limits
- [ ] 3.2 Test per-IP rate limits
- [ ] 3.3 Test rate limit headers in responses
- [ ] 3.4 Test 429 response with retry logic
```

Every proposal that changes behavior MUST also update the verification strategy or explicitly record why no verification change is needed. The proposal should identify the affected verification IDs, new or changed checks, suite tier, environment, expected evidence, and any remaining gap. Keep implementation tasks separate from the evidence plan; “add tests” alone is not a verification strategy.

**Task best practices:**
- Group under numbered headings
- Use hierarchical numbering (1.1, 1.2)
- Keep tasks small — completable in one session
- Tasks describe work, not verification

### Step 7: Regenerate INDEX.md
Run `python scripts/index.py` — the script will pick up the new change folder and add it to `docs/changes/INDEX.md` automatically from frontmatter.

### Step 8: Report
Present the proposal structure to the user. Wait for approval before implementation.

---

## When to Use Propose vs Curate

| Situation | Use |
|-----------|-----|
| Adding one behavioral requirement to existing spec | **Curate** |
| Creating a new standalone doc | **Curate** |
| A feature that touches multiple specs + architecture | **Propose** |
| A refactor with behavioral changes | **Propose** |
| A new component that needs spec, design, and tasks | **Propose** |

---

## Reference Files

Always load:
- `../spec-format.md` — for writing behavior deltas in correct format
- `../ontology.md` — for frontmatter on change artifacts
- `../folder-structure.md` — for change folder layout

Load as needed:
- `../principles.md` — for layer boundaries and conflict rules
