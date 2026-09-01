# Security: Execution And Supply Chain

> Runtime execution surfaces, local/runtime trust boundaries, automation, tooling, and supply-chain risks.
>
> Load this for CLIs, scanners, CI/CD, agentic systems, file handling, extensions, plugins, or broad platform reviews.

---

## 📦 Supply Chain & CI/CD

- [ ] 🔴 IF project has dependencies → THEN pin exact versions + use lockfile — reproducible builds, no `^` ranges in production
- [ ] 🔴 IF CI pipeline exists → THEN run vulnerability scanning (SCA) — block deploys on critical/high CVEs
- [ ] 🟡 IF merging code → THEN require at least one independent review — no self-approvals
- [ ] 🔴 IF deploying to production → THEN have tested rollback plan — know how to undo before you ship
- [ ] 🟡 IF using containers → THEN minimal base images, run as non-root, no secrets baked into image layers
- [ ] 🟡 IF CI/CD pipeline has secrets → THEN use ephemeral credentials, scope to minimum access, audit access logs
- [ ] 🟡 IF distributing software → THEN generate & publish SBOM (Software Bill of Materials) + sign images (Sigstore/Notary) — track transitive dependencies for CVE response, prevent tampered images
- [ ] 🔴 IF running CI/CD pipelines → THEN integrate SAST + DAST + IaC scanning + fuzz testing on every PR/merge (in addition to SCA) — auto-block deploys on critical/high findings
- [ ] 🔴 IF building/deploying containerized or cloud-native workloads → THEN adopt SLSA Level 2+ provenance, verify image signatures, and enforce Pod Security Standards / NetworkPolicies / seccomp profiles

---

## 🏗️ Infrastructure & Runtime

- [ ] 🔴 IF handling file paths with user input → THEN canonicalize + validate against base directory — prevent path traversal (`../../../etc/passwd`)
- [ ] 🔴 IF application processes data in loops/buffers → THEN enforce size limits + timeouts — prevent DoS via resource exhaustion (zip bombs, regex DoS, billion laughs)
- [ ] 🟡 IF running services → THEN apply principle of least privilege — minimum permissions for files, network, database, cloud IAM
- [ ] 🟡 IF application accepts regex from users → THEN sanitize or use RE2/safe regex — prevent ReDoS (catastrophic backtracking)
- [ ] 🔴 IF running in production → THEN disable debug modes, development endpoints, verbose errors, default credentials
- [ ] 🟡 IF using cloud services → THEN audit IAM policies, ensure no `*:*` permissions, enable CloudTrail/audit logging
- [ ] 🟡 IF database is accessible → THEN encrypt at rest + in transit, restrict network access, separate read/write credentials
- [ ] 🟡 IF writing in unmanaged languages (C, C++) or using FFI/Native modules → THEN enforce strict bounds checking + compile with OS-level memory protections (ASLR, DEP, PIE) — prevents buffer overflows

---

## 🤖 AI/LLM Security

> Use this section for code-first review of ML/LLM/agentic systems.
>
> Anubis inspects code, configuration, and existing tests. It does not prove safety through live red-team interaction, broad manual prompting, or heavy end-to-end runtime validation. For ML-heavy systems, call out that limitation explicitly in coverage.

- [ ] 🔴 IF using LLM APIs → THEN implement prompt injection detection & output sanitization — attacker manipulates prompts to bypass restrictions or extract data
- [ ] 🔴 IF accepting user input as LLM context → THEN separate untrusted content from system prompts — prevents prompt injection via context injection
- [ ] 🔴 IF building prompts or model context from user text, files, OCR, email, web pages, tool output, or retrieved chunks → THEN sanitize, normalize, size-bound, and label each untrusted input before interpolation — prompt builders are input-validation boundaries too
- [ ] 🔴 IF using RAG, retrieval, or vector search → THEN treat retrieved documents as untrusted input, isolate them from system instructions, verify source trust, and enforce retrieval-store access controls
- [ ] 🔴 IF model output can flow into tools, SQL, shell, HTML/Markdown, notifications, memory, follow-up prompts, or downstream automation → THEN apply context-specific output filtering/validation before reuse — model output is untrusted until proven otherwise
- [ ] 🔴 IF model responses can include secrets or internal data from prompts, tools, memory, or retrieved sources → THEN apply redaction and secret-filtering before rendering, logging, storing, indexing, or forwarding outputs
- [ ] 🔴 IF tools, memory, traces, or RAG connectors can surface secrets/credentials/tokens → THEN prevent those values from entering general model context unless strictly required, and redact them from logs, eval traces, and user-visible output
- [ ] 🔴 IF LLM generates code/commands → THEN sandbox execution + validate output — prevents RCE via model-generated shell commands
- [ ] 🟡 IF storing LLM training data → THEN verify no PII/secrets in training corpus — prevents privacy violations and credential leakage
- [ ] 🔴 IF using agentic AI (autonomous code gen, auto-PR, deployment agents) → THEN sandbox every AI-executed action, implement goal-hijacking detection, and log/audit all agent decisions for replay attacks
- [ ] 🟡 IF the system is ML-heavy, non-deterministic, or safety-critical → THEN perform a deeper architecture review of trust boundaries, fallback behavior, mutation paths, and observability; also report where static review plus existing tests still cannot prove runtime safety
- [ ] 🟡 IF AI-generated code is in production → THEN maintain an AI code inventory (what % of each repo is AI-generated) + run weekly automated security scans against OWASP LLM Top 10 + Agentic AI Top 10
- [ ] 🔴 IF non-deterministic systems (ML/AI) touch and mutate data → THEN maintain automated, tested backups with point-in-time recovery — AI data corruption is harder to detect and reverse than traditional bugs
- [ ] 🟡 IF the repo depends on many AI/ML/agent packages, stale model-serving libraries, plugin ecosystems, or unusual install sources → THEN recommend a package/dependency supply-chain audit — ML stacks accumulate risky transitive dependencies fast

---

## 🧠 Context & Semantic Supply Chain

- [ ] 🔴 IF agent or LLM consumes repository-controlled instruction files (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, prompts, memory files) → THEN treat them as executable supply-chain inputs: code review them, pin ownership, and require explicit approval before privileged runs
- [ ] 🔴 IF agent/CI context includes commits, PR descriptions, issues, code comments, docs, or copied terminal output from untrusted contributors → THEN sanitize/label as untrusted data before prompting tools/models — never let natural-language artifacts become privileged instructions
- [ ] 🔴 IF installing/updating packages or running generators with agent assistance → THEN disable or strictly allowlist lifecycle scripts/hooks (`preinstall`, `postinstall`, `prepare`), verify provenance/signatures, and inspect package metadata/README tasking before execution
- [ ] 🟡 IF agent fetches external web pages, package docs, changelogs, or release notes into context → THEN isolate retrieved text from system intent and require human confirmation before any network, shell, or file-mutating action derived from that content

---

## 🔮 Post-Quantum & Future-Proofing

- [ ] 🟡 IF long-term secrets (≥10 years) → THEN migrate to hybrid post-quantum KEM (Kyber + X25519) — prepares for quantum computing threats
- [ ] 🟡 IF using TLS → THEN monitor for TLS 1.2 deprecation + enable TLS 1.3 only + post-quantum in flight (Cloudflare does this already)
- [ ] 🟡 IF multi-region → THEN ensure data residency compliance (GDPR, data localization laws) — legal exposure

---

## 🛡️ Operational Security

- [ ] 🟡 IF team uses 2FA → THEN require hardware keys (FIDO2/WebAuthn) for high-privilege accounts — SMS/Authenticator apps vulnerable to SIM-swapping
- [ ] 🟡 IF has incident response plan → THEN test it regularly via tabletop exercises — untested plans fail when needed most
- [ ] 🟡 IF using open source → THEN audit for abandoned/unmaintained dependencies — "零日" (zero-day) in unpatched libs
- [ ] 🟡 IF CI runs tests → THEN ensure test suites can't be bypassed via CI config tampering — attackers could disable security tests

---

## 🧰 Tooling, Integrations & Review Surfaces

- [ ] 🔴 IF extracting untrusted archives (`.zip`, `.tar`, `.tgz`, `.7z`) → THEN normalize every entry path, enforce destination-root containment, and reject symlinks/hardlinks before extraction — prevents zip-slip and filesystem escape
- [ ] 🔴 IF verifying webhook/HMAC signatures → THEN reject missing or malformed signatures before constant-time compare, validate expected length/encoding first, and fail closed when verification cannot run
- [ ] 🔴 IF internal/admin/webhook endpoints rely on shared secrets → THEN require configured secrets at startup and refuse insecure defaults — never ship hardcoded fallback secrets
- [ ] 🔴 IF updating or deleting tenant-scoped records → THEN include tenant/org/account scope in the final database mutation, not only in a prior authorization check — avoids cross-tenant writes via guessed IDs
- [ ] 🔴 IF users can configure outbound integrations (webhooks, Slack, Discord, callbacks) → THEN treat destinations as SSRF sinks: validate scheme/host and block loopback, private, link-local, and metadata ranges
- [ ] 🔴 IF API keys carry scopes, roles, or permissions → THEN enforce those scopes on every route/action — storing scopes without checking them is fake security
- [ ] 🟡 IF findings, filenames, titles, or repo-controlled text are rendered into HTML, Markdown, email, CSV, SARIF, IDE webviews, or chat notifications → THEN context-escape every dynamic field before interpolation
- [ ] 🟡 IF security tooling supports ignore files or suppression rules → THEN review them as attack surface — never let defaults exclude first-party security-sensitive code, providers, plugins, or whole app trees
- [ ] 🔴 IF CI, agent plugins, or automation install tools at runtime → THEN pin exact package versions and GitHub Actions by immutable version or commit SHA — never use `@latest` in privileged automation
- [ ] 🔴 IF LLMs or automation can call tools/MCP servers → THEN validate tool inputs, require authorization per tool, and minimize tool permissions/capabilities — tool surfaces are privilege boundaries

---
