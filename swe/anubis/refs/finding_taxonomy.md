# Finding Taxonomy

Stable rule IDs for findings. Every finding carries `**Rule**: <ID>` so repeat reviews can dedupe and track.

| Prefix | Domain | Leaf |
|---|---|---|
| `SEC-INJ` | Injection, input handling, SSRF, path traversal | `security/core.md` |
| `SEC-CRY` | Secrets, crypto, PQC, hashing, randomness | `security/core.md` |
| `SEC-LOG` | Logging, privacy, PII, failure modes | `security/core.md` |
| `SEC-AUTH` | Authn, authz, sessions, tokens, CSRF, idempotency | `security/identity.md` |
| `SEC-WEB` | Headers, CORS, cookies, webhooks, WS/SSE, deep links | `security/remote_surfaces.md` |
| `SEC-ABUSE` | Business-logic abuse, rate limits, tenancy, mobile surface | `security/remote_surfaces.md` |
| `SEC-EXEC` | Files, shell/tool exec, CI/CD, supply chain, plugins, agents, MCP | `security/execution_and_supply_chain.md` |
| `QUAL-ERR` | Errors, exceptions, null/edge handling, defensive coding | `quality/core.md` |
| `QUAL-STATE` | State, resources, lifecycle, concurrency, encoding, collections | `quality/core.md` |
| `ARCH-DEP` | Dependencies, coupling, APIs, contracts, layering | `quality/architecture_and_maintainability.md` |
| `ARCH-DUP` | Duplication, dead code, complexity, bloat, over-engineering | `quality/architecture_and_maintainability.md` |
| `PERF-DB` | Queries, indexes, caching, queues, backend latency | `perf/services_and_data.md` |
| `PERF-FE` | Rendering, startup, bundle, storage I/O, runtime overhead | `perf/frontend_and_runtime.md` |
| `PERF-GEN` | Complexity, data structures, memory, measurement | `perf/core.md` |
| `VERIFY-TEST` | Tests, coverage claims, examples, docs drift, build/CI validation | `quality/verification_and_tooling.md` |
| `SPEC-VER` | Unverifiable requirement (no acceptance criteria / behavior missing) | `quality/verification_and_tooling.md` |
| `SPEC-ORPHAN` | Code with no parent requirement clause | `quality/verification_and_tooling.md` |
| `SPEC-DERIVED` | Silently absorbed derived requirement (never labeled/traced/flagged) | `quality/verification_and_tooling.md` |

Number findings sequentially per prefix per review: `SEC-INJ-01`, `SEC-INJ-02`. IDs are review-local unless the team tracks them across reviews.
