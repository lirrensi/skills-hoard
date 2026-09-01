# Spec Format — BDD + RFC

Every behavioral specification document (`node_type: spec`) follows this merged format: BDD's Given/When/Then scenarios + RFC 2119 normative keywords + goal-driven structure.

---

## Document Template

```markdown
# {Feature Name} Behavior

## Purpose
{1-3 sentences: what this spec covers, why it matters}

## Boundaries
**Handles:** {X, Y — what this feature/system is for}
**Explicitly does NOT:** {Z, W — the negative space. What this feature rejects or is out of scope.}
**If it happens anyway:** {where the rejected case goes instead — "[Other System]", "not supported", "future work", etc.}

## Goals
- **G1:** {measurable, testable goal}
- **G2:** {measurable, testable goal}

## Requirements

### Requirement: {Name}
The system MUST {behavior}. Use RFC 2119: MUST, SHOULD, MAY.

**As a** {role}
**I want** {feature}
**So that** {benefit or value}

#### Scenario: {Happy path — what working looks like}
- **GIVEN** {initial context}
- **WHEN** {triggering event}
- **THEN** {expected outcome}
- **AND** {additional outcome}

*Definition of Done: If this scenario passes, the requirement is met.*

#### Scenario: {Edge case or error}
- **GIVEN** {context for this edge case}
- **WHEN** {trigger}
- **THEN** {expected outcome}

*Definition of Done: If this scenario fails to produce the expected error, the system is broken.*

## Data Contracts

### {Interface Name}
| Field | Type | Required | Notes |
|-------|------|----------|-------|
| field | string | yes | description |

## State Transitions
| From State | Event | To State | Side Effects |
|-----------|-------|----------|-------------|
| logged_out | login | authenticated | JWT issued |

## Error Handling
| Error Code | HTTP | When | Response |
|-----------|------|------|---------|
| invalid_creds | 401 | Wrong credentials | `{ "error": "..." }` |

## Security Considerations
- {Security requirement using MUST/SHOULD/MAY}

## Limits
| Constraint | Value | Reason |
|-----------|-------|--------|
| Max attempts | 5 / 15 min | Brute force prevention |
```

---

## Section Guide

### Purpose
1-3 sentences. What does this spec cover, and why is it important?

### Boundaries (the negative space)

Every spec MUST make its borders explicit — a map is useless without borders. Three lines:

- **Handles:** what this feature/system is for.
- **Explicitly does NOT:** what it rejects or is out of scope.
- **If it happens anyway:** where the rejected case goes instead — "[Other System]", "not supported", "future work".

The rule: a reader should be able to look at the Boundaries section for 30 seconds and know exactly where this feature's responsibility ends — and who owns the case it refuses. If nothing is rejected, that is itself a decision worth stating explicitly.

### Goals
Numbered goals (G1, G2...). Each must be:
- **Measurable** — can verify whether it's met
- **Testable** — a test could confirm compliance
- **Behavioral** — describes outcome, not implementation

Good: "No plaintext credentials touch persistent storage."
Bad: "Use bcrypt for hashing." (implementation detail)

### Requirements
Each requirement states a single behavior with an RFC 2119 keyword:

| Keyword | Meaning |
|---------|---------|
| **MUST / MUST NOT** | Absolute, non-negotiable |
| **SHOULD / SHOULD NOT** | Recommended default; exceptions need justification |
| **MAY** | Optional, implementation's choice |

Follow each requirement with:
1. A user story (As a / I want / So that)
2. At least one scenario (Given / When / Then)

### User Stories
Capture WHO benefits, WHAT they want, and WHY it matters. Keeps specs grounded in user value.

### Definition of Done

Every scenario includes a *"Definition of Done"* — a one-line proof that the behavior exists and works as specified. This is NOT a success message or a test assertion. It is a contract:

- **Happy path:** "If this scenario passes, the requirement is met."
- **Error path:** "If this scenario fails to produce the expected error, the system is broken."
- **Conflict path:** "If this scenario throws a different error, we cannot proceed — the conflict must be resolved first."
- **Boundary path:** "If the input exceeds the limit, the system MUST reject it. Accepting it means the limit is not enforced."

This turns every scenario from "here's a nice example" into "here's exactly what Done means, and here's exactly what broken means."

### Verification Traceability

Every important requirement MUST point to at least one verification check or an explicit documented gap in `/verification/strategy.md`. Use stable verification IDs such as `V-AUTH-001`; the spec describes the behavior and completion contract, while the verification strategy describes the actual tool, command, environment, evidence, and suite tier.

A verification reference MUST answer whether the behavior is mechanically tested, verified by evidence that the check covers the intended requirement, and validated against product/user intent where automated checks cannot establish that alone.

Do not put framework-specific test instructions into the behavioral spec. Link to the verification strategy instead. If no credible check exists, write `Verification gap: ...` and state the risk rather than implying coverage.

### Scenarios
Every requirement has ≥1 scenario. Scenarios must be:
- **Concrete** — specific values, not placeholders
- **Testable** — could write an automated test from it
- **Declarative** — what happens, not UI clicks (see below)
- **Cover both paths** — minimum: happy path + error/edge case
- **Have a Definition of Done** — what confirms this behavior is correct
- **Have verification traceability** — a strategy ID/evidence reference or an explicit coverage gap

Pattern:
- **GIVEN** — preconditions, existing state before the event
- **WHEN** — triggering event (action, system event, timer)
- **THEN** — expected outcomes (state changes, responses, side effects)
- **AND** — additional context or outcomes (anywhere after GIVEN/WHEN/THEN)

### Declarative vs Imperative — Critical Rule

Scenarios MUST be declarative (business language), NEVER imperative (UI/implementation details).

**Declarative (correct):**
> **GIVEN** a registered user with valid credentials  
> **WHEN** they authenticate  
> **THEN** a session is established and their default view is displayed

**Imperative (wrong):**
> **GIVEN** the login page is loaded  
> **WHEN** the user types "user@example.com" in the email field  
> **AND** clicks the "#login-button"  
> **THEN** the browser navigates to "/dashboard"

Why this matters: declarative scenarios survive UI redesigns, framework changes, and implementation rewrites. Imperative scenarios break the moment you change a CSS selector. If a scenario mentions a button, a field name, a URL path, or a DOM element, rewrite it declaratively.

**Protocol-level declarative (correct):**
> **GIVEN** a client with valid API credentials  
> **WHEN** they send a POST request to `/api/v1/auth` with `{email: string, password: string}`  
> **THEN** the system responds with `200 OK` and a body containing `{access_token: string, expires_in: 3600}`  
> **AND** the token is valid for subsequent authenticated requests

**Imperative protocol (wrong):**
> **GIVEN** the user opens the auth dialog  
> **WHEN** the user fills in the form and clicks submit  
> **THEN** the dialog shows a loading spinner  
> **AND** the page redirects to the dashboard

**Protocol-level declarative scenarios** describe the *contract* — what messages are sent, what fields are expected, what responses are returned. These survive complete rewrites of the UI, the framework, or the transport layer.

### Data Contracts
Tables of inputs/outputs with types and constraints. Use real field names — implementers code against this.

### State Transitions
`From State | Event | To State | Side Effects`. For stateful behavior: auth, workflows, ordering.

### Error Handling
Exhaustive table: error codes, conditions, response bodies. Every error the system can produce.

### Security Considerations
Required even if brief. If no special concerns: "No special security considerations beyond standard practices."

### Limits
Every spec defines boundaries: rate limits, sizes, timeouts, retries, with exact values and reasons.

---

## Protocol Contracts

Every spec that involves external communication (API, events, messages) MUST define the protocol contract:

### Request Format
| Field | Type | Required | Notes |
|-------|------|----------|-------|
| field | type | yes/no | description, constraints |

### Response Format
| Field | Type | Required | Notes |
|-------|------|----------|-------|
| field | type | yes/no | description |

### Message Flow
```
Client → Gateway → Auth Service
         ↓
       Audit Log
```

### State Machine
| State | Events | Next State | Side Effects |
|-------|--------|------------|-------------|
| idle | request received | processing | request logged |
| processing | success | completed | response emitted |
| processing | failure | error | retry scheduled |

---

## Internal Behavior

Document how the system processes things internally. This is the invisible machinery that makes the external behavior possible.

### Processing Pipeline
| Stage | Input | Output | Rules |
|-------|-------|--------|-------|
| validation | raw request | validated request | schema check, rate limit check |
| authorization | validated request | authorized request | permission check, token validation |
| execution | authorized request | result | business logic, state mutation |
| response | result | formatted response | error wrapping, audit logging |

### Decision Logic
Describe the rules the system uses to make decisions internally:
- "If the request contains a `session_id`, the system MUST validate it against the cache before processing."
- "If the cache lookup fails, the system MUST fall back to the database and update the cache on success."

### Internal State
| State | Description | Transitions |
|-------|-------------|-------------|
| state_name | what this internal state means | events that change it |

---

## User Experience (Non-UI)

Document what the user *experiences* and *perceives* — not the interface they use to get there.

**Good:** "The user is informed that their action was successful."
**Bad:** "A green toast notification appears in the top-right corner with the text 'Success!'"

**Good:** "The user can access their saved data."
**Bad:** "The user clicks the 'Dashboard' tab in the sidebar menu."

The UI is implementation detail. The user experience is behavioral contract.

---

## What Does NOT Belong in a Spec

- ❌ Class names, function names, file paths, framework choices
- ❌ Step-by-step implementation instructions
- ❌ UI layout, CSS, pixel values, button labels, modal animations
- ❌ Database queries, ORM configuration
- ❌ Non-behavioral trivia ("this file was created by Bob in 2023")
- ❌ Screen-by-screen walkthroughs ("click X, then Y, then Z")

**Quick test:** If the implementation can change without changing externally visible behavior, it does NOT belong in a spec. A UI redesign, framework swap, or component refactor should never require a spec update.

---

## Spec vs Architecture vs Overview

| Layer | Answers | Contains | Does NOT contain |
|-------|---------|----------|-----------------|
| **overview/** | WHY does this exist? | Identity, purpose, users, value, non-goals | Behavior details, tech choices |
| **spec/** | WHAT must it do? | Requirements, scenarios, contracts, errors, protocols, internal behavior | Implementation structure, UI details, framework choices |
| **architecture/** | HOW is it built? | Components, dependencies, boundaries, ADRs, file structure | Behavioral requirements, user-facing contracts |

### The Spec Completeness Test

Could you hand the spec to an independent team and they'd build the **correct system** without seeing the code? The spec must contain enough information for them to:

1. **Implement the user experience** — what users experience and perceive
2. **Implement the protocol** — API contracts, message formats, wire protocols, state transitions
3. **Implement the internal behavior** — state machines, processing pipelines, decision logic, error handling
4. **Verify correctness** — every scenario has a Definition of Done and a verification reference or explicit gap

**The spec must be the complete source of truth for the system. Code is one rendering. If the spec is strong enough, you could delete the code and rebuild from the spec alone.**
