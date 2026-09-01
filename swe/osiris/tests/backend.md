# Testing: Backend

> Load when the repo exposes APIs, workers, queues, CLIs, libraries with side effects, databases, or external service integrations.

---

## API and Interface Boundaries

- [ ] CRITICAL IF the repo exposes HTTP, RPC, GraphQL, CLI commands, or other machine-facing interfaces -> THEN test success, validation failure, unauthorized, forbidden, not-found, conflict, and internal-error paths
- [ ] CRITICAL IF requests or commands accept structured input -> THEN verify shape, type, unknown fields, oversized payloads, and malformed encodings
- [ ] HIGH IF partial updates, money values, or large identifiers exist -> THEN test omitted-versus-null semantics, numeric precision, and serialization boundaries explicitly
- [ ] HIGH IF the interface supports protocol edge behavior such as `HEAD`, `OPTIONS`, redirects, or streaming -> THEN test those paths instead of assuming the main verb is the only contract
- [ ] HIGH IF responses are consumed by other systems -> THEN assert contract shape, field meaning, and backward-compatibility-sensitive behavior
- [ ] HIGH IF rate limits, idempotency, pagination, filtering, or sorting exist -> THEN test them as first-class behavior rather than optional polish

---

## Data and Persistence

- [ ] CRITICAL IF the repo writes to a database or durable store -> THEN test real reads, writes, constraints, rollbacks, and transactional boundaries against a dedicated test environment
- [ ] CRITICAL IF migrations or schema changes exist -> THEN test fresh apply, compatibility during rollout, and rollback safety where rollback is supported
- [ ] HIGH IF caching exists -> THEN test hit, miss, expiry, invalidation, and failure of the cache layer
- [ ] HIGH IF time-dependent logic exists -> THEN use a controlled clock and test expiry, scheduling, DST boundaries, and timezone-sensitive behavior
- [ ] HIGH IF reads can come from replicas, indexes, or delayed projections -> THEN test read-after-write expectations, replica lag tolerance, and when stale data is acceptable versus a bug

---

## Async, External, and Distributed Behavior

- [ ] CRITICAL IF the repo publishes or consumes queue/event messages -> THEN test schema correctness, side effects, retry behavior, idempotency, and out-of-order delivery assumptions
- [ ] CRITICAL IF it depends on external services -> THEN test timeout, retry, malformed response, partial failure, and sandbox integration behavior
- [ ] HIGH IF contracts exist between services or packages -> THEN verify consumer expectations explicitly rather than trusting shared assumptions
- [ ] HIGH IF notifications, webhooks, or outbound communications exist -> THEN test payload correctness, signature behavior, retry rules, and duplicate-send protection

---

## Concurrency, Scheduling, and Streaming

- [ ] CRITICAL IF shared mutable state exists outside a single transaction -> THEN test double-submit, read-modify-write races, lock or lease behavior, and high-contention invariants explicitly
- [ ] CRITICAL IF workers, schedulers, or cron jobs run in parallel -> THEN test duplicate execution, overlap prevention, catch-up versus skip semantics, and checkpoint or resume behavior
- [ ] HIGH IF the repo exposes realtime or streaming interfaces -> THEN test connection auth, reconnect behavior, message ordering, deduplication, and slow-consumer backpressure
- [ ] HIGH IF work is retried or replayed after failure -> THEN prove reruns do not duplicate side effects or corrupt durable state

---

## Auth, Abuse, and Data Exposure

- [ ] CRITICAL IF auth or authorization exists -> THEN test bypass attempts, horizontal access, vertical privilege escalation, and default-deny behavior
- [ ] CRITICAL IF user input reaches queries, templates, files, or outbound fetches -> THEN test injection and abuse cases appropriate to the stack
- [ ] HIGH IF the app redirects, derives absolute URLs, or trusts request host metadata -> THEN test open-redirect and host-header abuse paths explicitly
- [ ] HIGH IF the product is browser-exposed or session-based -> THEN test clickjacking defenses, CSP enforcement, and session fixation rather than only token validity
- [ ] HIGH IF the system handles secrets or PII -> THEN test that sensitive values stay out of logs, error payloads, URLs, and unsafe exports
- [ ] HIGH IF uploads or archives are accepted -> THEN test type confusion, archive or zip bombs, oversize payloads, traversal-style names, and malicious content rejection

---

## Tenancy, Files, Search, and Data Movement

- [ ] CRITICAL IF the product is multi-tenant -> THEN test read isolation, write isolation, background-job tenant context, and tenant-scoped caches, indexes, and exports
- [ ] CRITICAL IF files or object storage exist -> THEN test unauthorized fetches, path or filename sanitization, signed URL scope and expiry, and storage-versus-database lifecycle consistency
- [ ] HIGH IF search or indexing exists -> THEN test create, update, and delete index consistency, access control in results, and safe full reindex behavior
- [ ] HIGH IF import or export workflows exist -> THEN test malformed inputs, partial-success reporting, duplicate handling rules, authorization, and large-job memory or timeout behavior
- [ ] HIGH IF auth flows include reset, MFA, or token rotation -> THEN test one-time use, expiry, replay resistance, and claim validation rather than only the happy path
