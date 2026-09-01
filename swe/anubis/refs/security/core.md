# Security: Core

> Trust-agnostic controls that apply to almost any codebase.
>
> Report findings by issue name + location. Add CWE/CVE tags when relevant. Do not rely on checklist numbers.

---

## 🧹 Input Validation & Injection

- [ ] 🔴 IF accepting any external input → THEN schema-validate with whitelist approach, reject unknown fields
- [ ] 🔴 IF building database queries → THEN use parameterized queries only — zero concatenated SQL, ever
- [ ] 🔴 IF using NoSQL databases (MongoDB, CouchDB) or ORMs → THEN strictly cast data types and never pass raw user JSON/objects into queries — prevents NoSQL/Object Injection
- [ ] 🔴 IF rendering user content in HTML → THEN sanitize/escape output — context-aware (HTML body vs attribute vs JS vs CSS)
- [ ] 🔴 IF accepting file uploads → THEN validate size + MIME (magic bytes, not just header) + extension + strip metadata + scan content
- [ ] 🔴 IF server fetches user-provided URLs → THEN enforce URL allowlists for SSRF prevention — block internal IPs/metadata endpoints
- [ ] 🔴 IF accepting XML input → THEN disable external entity processing (XXE) — no DTD loading
- [ ] 🔴 IF deserializing data (pickle, Java serialization, YAML.load, unserialize) → THEN never deserialize untrusted input — use safe loaders/formats
- [ ] 🔴 IF building OS commands with user input → THEN never use shell interpolation — use parameterized exec / library APIs
- [ ] 🔴 IF interpolating user input into server-side templates (Jinja2, Twig, Freemarker, ERB, Pug) → THEN use sandboxed rendering + never pass raw user strings as template source — prevents SSTI (Server-Side Template Injection → RCE)
- [ ] 🟡 IF querying LDAP/Active Directory with user input → THEN escape/parameterize LDAP filter values — prevents LDAP injection auth bypass

---

## 🔒 Secrets & Crypto

- [ ] 🔴 IF code references API keys, passwords, or credentials → THEN load from env/vault only, verify presence at startup, never hardcode
- [ ] 🔴 IF `.env` files exist → THEN confirm in `.gitignore` + audit git history for prior leaks (use tools like truffleHog/gitleaks)
- [ ] 🔴 IF generating tokens, session IDs, nonces, or random identifiers → THEN use CSPRNG — never `Math.random()` or `random.random()`
- [ ] 🔴 IF the app uses asymmetric encryption, key exchange, KEMs, or digital signatures → THEN require NIST-standardized post-quantum algorithms by default: `ML-KEM-512/768/1024` for encapsulation; `ML-DSA-44/65/87`, `SLH-DSA`, or `FN-DSA` for signatures
- [ ] 🔴 IF classical-only asymmetric crypto is present (`RSA`, `ECDH`, `ECDSA`, `DH`, `DSA`, `ElGamal`, `Ed25519`, `X25519`, or similar) → THEN flag it as non-compliant for net-new systems or major upgrades unless explicitly wrapped in an approved hybrid migration scheme
- [ ] 🟡 IF the system is in migration mode → THEN allow only explicit hybrid transitions such as `X25519+ML-KEM-768` or `P-256+ML-KEM-768`; pure classical asymmetric crypto is still a finding
- [ ] 🟡 IF the code uses non-NIST PQC candidates or vendor-specific claims (`NTRU`, `Classic McEliece`, custom PQC, or "quantum-safe" marketing names) → THEN flag for manual review unless paired with an approved NIST-standardized primitive
- [ ] 🟡 IF the algorithm, library, provider, or hardware-backed primitive is unfamiliar, newly introduced, renamed, or ambiguously documented → THEN do not guess; verify whether it is actually quantum-resistant by checking authoritative documentation/standards before calling it compliant
- [ ] 🟡 IF the real cryptographic primitive cannot be determined from code, configs, dependency metadata, or standard library usage — especially when wrappers, SDKs, HSMs, cloud KMS, native modules, or custom crypto abstractions hide the algorithm choice — THEN ask the developer directly which algorithms and modes are in use; treat unresolved ambiguity as a coverage gap, not a pass
- [ ] 🔴 IF symmetric crypto is used → THEN require PQ-ready parameters only: `AES-256-GCM` or `ChaCha20-Poly1305` are acceptable; reject weak/legacy modes like `DES`, `3DES`, `RC4`, `AES-ECB`, or unauthenticated encryption
- [ ] 🔴 IF comparing secrets (tokens, hashes, API keys) → THEN use constant-time comparison (`crypto.timingSafeEqual()`, `hmac.compare_digest()`) — never `===` or `==`
- [ ] 🟡 IF secrets have no rotation policy → THEN implement automated rotation + expiry — assume every secret eventually leaks

---

## 📊 Observability & Audit

- [ ] 🔴 IF logging anything → THEN never log passwords, tokens, card numbers, PII, or secrets
- [ ] 🔴 IF sensitive operations occur (login, permission change, data export, admin action) → THEN write immutable audit log: who, what, which resource, when, from where
- [ ] 🟡 IF application has logging → THEN use structured format (JSON) — machine-parseable, not grep-dependent
- [ ] 🟡 IF distributed system → THEN propagate request correlation IDs across all services for tracing
- [ ] 🔴 IF system is in production → THEN alert on anomalies — auth failure spikes, unusual access patterns, error rate changes
- [ ] 🟡 IF user input can appear in log output → THEN sanitize for log injection — attackers forge entries via `\n`, ANSI escape codes, or format strings
- [ ] 🔴 IF error occurs → THEN return generic message to client, log full detail server-side — never expose stack traces, DB errors, or internal paths to users

---

## 🧯 Error Handling & Failure Modes

- [ ] 🔴 IF security check fails → THEN fail closed (deny access) — never fail open
- [ ] 🔴 IF auth/lookup fails → THEN return identical responses for "user not found" vs "wrong password" — prevent user enumeration
- [ ] 🟡 IF external dependency fails → THEN implement circuit breaker + graceful degradation — don't cascade failures into security bypasses

---

## 🔐 Data Protection & Privacy

- [ ] 🔴 IF application handles PII (names, emails, addresses, phone numbers, government IDs) → THEN classify data by sensitivity tiers, encrypt at rest, and enforce access controls per tier — not all data is equal, treat PII as toxic
- [ ] 🔴 IF application operates under GDPR/CCPA/HIPAA or similar → THEN implement data subject rights: export, deletion, consent withdrawal — "we can't delete it" is a legal vulnerability
- [ ] 🔴 IF user requests account deletion → THEN hard-delete or cryptographically erase PII within regulatory timeframe — soft-delete that keeps PII indefinitely violates retention laws
- [ ] 🟡 IF sharing data with third parties (analytics, payment processors, marketing tools) → THEN minimize fields sent + ensure DPA (Data Processing Agreement) is in place — you're liable for your vendors' breaches
- [ ] 🟡 IF storing data long-term → THEN define and enforce retention policies — auto-purge data you no longer need. Stored data you don't need is liability, not asset
- [ ] 🟡 IF backups contain PII or secrets → THEN encrypt backups, restrict access, test restoration, and include in retention/deletion policies — backups are the most overlooked breach vector
- [ ] 🔴 IF backup encryption → THEN use separate keys from production + offline storage — prevents single point of compromise

---
