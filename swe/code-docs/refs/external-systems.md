# External Systems Boundaries

When documentation references an external system (API, service, database, library, platform), you must define the boundary clearly. Not everything gets documented equally — the level of integration determines what to document and how.

---

## How to Classify External Systems

For every external dependency, answer these questions in order:

### 1. Who owns the canonical docs?
- **External system has its own docs** → Link to them. Do NOT rewrite their docs locally.
- **No external docs exist** → Document the contract (what you expect from it) in a `reference/` doc.
- **It's our own system in another repo** → Link to that repo's `docs/`. Cross-reference, don't duplicate.

### 2. What level of integration?

| Integration Level | Meaning | How to document |
|------------------|---------|----------------|
| **Stable foundation** | Database, OS, language runtime — its API won't change under us | Document our usage patterns, not its API. Reference its official docs for details. |
| **Upstream dependency** | Framework, library with versioned releases — may change, but slowly | Document the version we depend on, our usage patterns, and upgrade notes. |
| **External API** | Third-party service with its own lifecycle — may change without notice | Document the contract we expect, our abstraction layer, and failure modes. |
| **Unstable integration** | Beta API, experimental service — expected to break | Document heavily. Define our abstraction so we can swap implementations. Flag as `confidence: tentative`. |

### 3. Do we create our own abstraction?

| Situation | Rule |
|-----------|------|
| **Database, filesystem, language stdlib** | No abstraction needed. Document usage patterns only. |
| **Stable library with clean API** | Light abstraction if it simplifies testing. Document the wrapper. |
| **External API that might change** | Always create an abstraction layer. Document the interface, not the implementation. |
| **Multiple competing services** | Abstraction is mandatory. Document the interface so backends are swappable. |

---

## How to Document Each Level

### Stable Foundation
```markdown
## Database: PostgreSQL 16
- **Canonical docs:** https://www.postgresql.org/docs/16/
- **Our usage:** read-heavy with connection pooling via pgBouncer
- **Reliability:** production-grade, no abstraction needed
- **What we document here:** schema design, migration strategy, connection config
- **What belongs to upstream:** SQL syntax, PG administration, PG tuning
```

### External API
```markdown
## Payment Provider: Stripe
- **Canonical docs:** https://stripe.com/docs/api
- **Integration level:** External API — we maintain an abstraction layer
- **Expected stability:** High. Stripe versions their API. Breaking changes get 12-month notice.
- **Our abstraction:** `src/payments/gateway.ts` — interface with `charge()`, `refund()`, `webhook()`
- **Failure modes:** Network timeout (30s), API rate limit (100 req/s), webhook replay
- **What we document:** our interface contract, auth, idempotency keys, webhook handling
- **What belongs to Stripe:** API reference, SDK docs, dashboard usage
```

### Unstable Integration
```markdown
## AI Provider: OpenAI (Beta endpoint)
- **Canonical docs:** https://platform.openai.com/docs/
- **Integration level:** Unstable — beta endpoint, may change without notice
- **Expected stability:** Low. Model names, request format, and pricing change frequently.
- **Our abstraction:** `src/ai/provider.ts` — interface `complete(prompt) → response`
- **Fallback:** We support swapping to Anthropic or local model
- **Confidence:** tentative — this integration is experimental
- **Document heavily:** failure modes, retry strategy, fallback chain, cost monitoring
```

---

## Boundary Rules

### What we ALWAYS document (regardless of integration level)
- The dependency name, version, and canonical docs link
- The integration level and expected stability
- Our abstraction (if any) with file paths
- Failure modes and our handling strategy

### What we NEVER document locally
- The external system's full API reference (link to their docs)
- Their internal architecture or implementation
- Their deployment, scaling, or operations (unless we operate it)
- Their changelog (link to it, don't duplicate)

### When we create a dedicated reference doc
Create `docs/reference/<system-name>.md` when:
- The integration is complex (multiple endpoints, auth flows, state machines)
- The dependency is critical (system fails if it's down)
- The integration level is "external API" or "unstable"
- Multiple components depend on the same external system

### When a note in the spec/architecture doc is enough
Add a paragraph or table when:
- The integration is simple (one endpoint, straightforward)
- The dependency is stable foundation (database, language)
- Only one component uses it

---

## The Abstraction Rule

> **If the external system could be swapped without rewriting business logic, you have the right abstraction. Document the abstraction interface, not the implementation behind it.**

This means:
- `spec/` describes WHAT the system needs from the external dependency (e.g., "MUST persist user sessions")
- `architecture/` describes HOW we fulfill that (e.g., "PostgreSQL via pgBouncer with connection pooling")
- `architecture/components/` describes the abstraction interface
- `reference/` documents the external system contract and reliability

---

## Link Format for External Systems

Always link to canonical docs with a stable URL:

```markdown
- **Stripe API:** https://stripe.com/docs/api (version 2024-06)
- **PostgreSQL 16:** https://www.postgresql.org/docs/16/
```

Never rely on a URL alone when a proper named standard exists:
```markdown
✅ "JWT per RFC 7519"
❌ "JWT — see https://jwt.io"
```
