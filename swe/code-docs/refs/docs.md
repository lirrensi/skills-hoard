# Documentation Writing Standards

General writing standards for all documentation produced under this system. For structure and format specifics, see `spec-format.md`, `ontology.md`, and `folder-structure.md`.

---

## Language

- Use precise, stable terminology. Define shared terms once in `docs/reference/glossary.md`.
- Avoid hedging: "usually", "kind of", "probably", "roughly" — unless uncertainty is the point.
- If something is undecided, label it explicitly: "**[UNDECIDED]** The retry strategy has not been finalized."
- Prefer active voice: "The system returns a token" not "A token is returned by the system."
- Use present tense: "validates" not "will validate."
- **Protocol language:** When describing API contracts, use exact field names, types, and values. Not "a token is sent" but "the response body includes `access_token: string` with `expires_in: 3600` (seconds)."

---

## Code Examples

- Must be copy-pasteable when presented as runnable examples.
- Include language tags on all fenced code blocks.
- Use placeholders for variable values and mark them clearly.

Good:
````markdown
```typescript
const client = new AuthClient({ baseUrl: "<your_base_url>" });
await client.login({ email: "<user_email>", password: "<user_password>" });
// Replace placeholders before running.
```
````

Bad:
````markdown
```typescript
const client = new AuthClient({ baseUrl: url });
await client.login(credentials);
```
````

---

## Diagrams

- Prefer text-first, versionable diagrams: Mermaid, PlantUML, ASCII art.
- Use diagrams when structure or flow is easier to see than explain.
- Every diagram needs a caption or preceding sentence explaining what it shows.
- **Protocol diagrams** are mandatory for any spec involving communication. Show message formats, sequence, and state transitions.

ASCII example:
```
Client → Gateway → Auth Service → DB
                ↘ Cache
```

Protocol diagram example:
```
Client                    Gateway                    Auth Service
  | POST /login              |                            |
  |------------------------->|                            |
  |                          | POST /validate             |
  |                          |--------------------------->|
  |                          |                            |
  |                          |<---------------------------|
  |                          | 200 + {token, user_id}     |
  |                          |                            |
  |<-------------------------| 200 + {token, expires_at}  |
  |                          |                            |
```

Mermaid example:
````markdown
```mermaid
sequenceDiagram
    Client->>Gateway: POST /login {email, password}
    Gateway->>Auth: validate(credentials)
    Auth->>DB: lookup user
    DB-->>Auth: user record
    Auth-->>Gateway: JWT token
    Gateway-->>Client: 200 + {token, expires_at}
```
````

---

## Internal Behavior Documentation

Every spec and architecture document must explain what the system does *internally* — not just what the user sees. Internal behavior includes:

- **State machines** — states, events, transitions, side effects
- **Processing pipelines** — stages, inputs, outputs, decision rules
- **Decision logic** — the rules the system uses to make choices internally
- **Message flows** — how components communicate at the protocol level
- **Error propagation** — how errors flow through the system internally

**Good:** "The system validates the request against the schema, then checks the rate limiter. If the rate limit is exceeded, the system rejects the request immediately without reaching the business logic."
**Bad:** "The user sees an error message."

**Good:** "The system enters a retry loop with exponential backoff, capped at 5 attempts."
**Bad:** "The API returns a 500 error."

## Links and Boundaries

- Cross-link related sections: "See [Error Handling](/spec/error-handling.md) for failure modes."
- Link to ADRs for important design decisions.
- For external systems, document the contract and expectations — not their internals.
- If another repo has canonical docs, link to that repo instead of rewriting locally.
- Use repository-rooted paths beginning with `/` for all internal links, as required by the ontology.

---

## Verification Documentation

Every maintained project MUST have a discoverable `docs/verification/strategy.md` with `node_type: verification` (or an explicitly linked equivalent). Verification documentation is a first-class evidence layer, not a generic “Testing” paragraph hidden in architecture docs.

The strategy MUST document:

- the product goals, behavioral requirements, protocols, user journeys, and operational properties being verified;
- the actual tools, versions or package sources, fixtures, environments, and exact commands;
- the verification taxonomy used by the project: static checks, unit/component, integration, contract/API, UI/end-to-end, manual/exploratory, and operational/release checks as applicable;
- fast/smoke, standard, long/exhaustive, and release suite tiers, including prerequisites, cadence, and evidence;
- a traceability matrix mapping important claims to checks, commands, environments, evidence, and status;
- explicit coverage gaps, flaky or blocked checks, manual-only areas, and compensating controls.

Use these distinctions precisely:

| Term | Meaning |
|------|---------|
| **Test result** | A mechanical check passed. |
| **Verification result** | The check passed and its scope/evidence supports the specified behavior. |
| **Validation result** | The behavior also matches product/user intent, including human judgment where needed. |

Do not write “run the tests” when the repository has a concrete command. Do not claim that a unit test verifies a full UI journey, or that one happy-path browser test verifies every backend error contract. If a layer is absent, say so and record the risk.

---

## Deprecation

- Never silently delete documented behavior.
- Mark deprecated behavior clearly: state replacement, timeline, and reason.

```markdown
> **Deprecated since vX.Y.** Use [new-thing] instead. Planned removal: vX.Z.
> Reason: [why it was deprecated].
```

- Add `status: deprecated` to the document's frontmatter.
- On the replacement doc, add `links: supersedes: [old-doc.md]`.

---

## Intentionally Undocumented

When a detail is deliberately left unstable or internal:

```markdown
> Intentionally undocumented — internal detail, subject to change without notice.
```

---

## Tables

- Every table has a header row.
- Align pipes for readability when practical.
- Include units in column headers when applicable: "Timeout (ms)", "Size (bytes)".

Example:
```markdown
| Field | Type | Required | Notes |
|-------|------|----------|-------|
| email | string | yes | Must be valid email format |
| timeout_ms | number | no | Default: 5000 |
```

---

## Recommended Reading Order

When onboarding or orienting to the documentation:

1. `docs/INDEX.md` — master map
2. `docs/overview/product.md` — what this is and why
3. `docs/reference/glossary.md` — shared vocabulary
4. `docs/spec/INDEX.md` → relevant spec files — behavioral contracts
5. `docs/architecture/INDEX.md` → relevant arch files — implementation shape
6. `docs/verification/strategy.md` — how behavior and implementation are checked
7. `docs/architecture/decisions/` — decision history
8. Code — only when docs are silent, stale, or ambiguous

---

## When Reporting

Always structure answers as:

- **What overview says** — product identity and scope, user experience principles
- **What spec says** — exact behavioral requirements, protocol contracts, internal behavior
- **What architecture says** — implementation structure, internal processing, component communication
- **What verification says** — checks, tools, suite tiers, evidence, traceability, and known gaps
- **What code does** (if inspected) — actual behavior
- **Whether they agree** — flag discrepancies between any layer and whether verification covers the claimed behavior

When reporting on a spec, always include:
- **User experience** — what the user experiences and perceives
- **Protocol** — API contracts, message formats, wire protocols
- **Internal behavior** — state machines, processing pipelines, decision logic
- **Verification** — the check/evidence that supports the behavior, or an explicit gap

---

## Quick Reference — Doc Types

| Doc Type | Audience | Primary Question | Contains | Does NOT contain |
|----------|----------|-----------------|----------|-----------------|
| Overview | Humans, stakeholders | Why does this exist? | Identity, purpose, user experience principles, non-goals | Behavior details, tech choices |
| Spec | Implementers, testers, agents | What must it do? | Requirements, scenarios, protocol contracts, internal behavior, state machines | UI details, implementation structure, framework choices |
| Architecture | Maintainers, agents | How is it built? | Components, dependencies, internal processing, communication protocols | Behavioral requirements, user-facing contracts |
| Verification | Implementers, testers, reviewers, agents | How do we know it works? | Strategy, taxonomy, toolchain, commands, evidence, traceability, gaps | Product requirements or implementation design |
| Guide | Users, contributors | How do I do X? | Step-by-step procedures | Specs, architecture decisions |
| ADR | Maintainers | Why was this decided? | Decision context, rationale, consequences | Implementation details |
| Runbook | Operators | How do I operate X? | Operational procedures, incident response | Business logic, specs |
| INDEX.md | Everyone | Where is everything? | Maps, links, summaries | Content |
