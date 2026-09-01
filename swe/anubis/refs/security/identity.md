# Security: Identity

> Authentication, authorization, sessions, and privilege boundaries.
>
> Load this when the repo exposes login flows, tenants, roles, tokens, or privileged mutations.

---

## 🛡️ Authentication

- [ ] 🔴 IF implementing authentication → THEN use OAuth2/OIDC or battle-tested libraries — never roll your own
- [ ] 🔴 IF storing auth tokens client-side → THEN use `httpOnly; Secure; SameSite` cookies — never localStorage (XSS exfiltration)
- [ ] 🔴 IF storing passwords → THEN use Bcrypt (cost≥12) or Argon2id — never MD5/SHA1/SHA256 (too fast = crackable)
- [ ] 🔴 IF user logs out or resets password → THEN destroy/invalidate ALL active sessions server-side
- [ ] 🔴 IF endpoint accepts credentials → THEN rate-limit with exponential backoff + account lockout after N failures
- [ ] 🟡 IF supporting password-based auth → THEN enforce MFA on sensitive accounts/operations (admin, financial, PII access)
- [ ] 🟡 IF issuing tokens → THEN set short expiry + implement refresh token rotation (revoke family on reuse detection)
- [ ] 🔴 IF implementing password recovery/reset → THEN use unpredictable, single-use, short-lived tokens sent out-of-band — never reveal if email exists (prevents enumeration)
- [ ] 🟡 IF using OAuth → THEN enforce `state` parameter + PKCE on all flows (including mobile/native) — prevents CSRF and authorization code interception

---

## 🔐 Authorization

- [ ] 🔴 IF accessing user-owned resources → THEN verify resource ownership every request — `/me/orders` not `/user/123/orders`
- [ ] 🔴 IF endpoint has role restrictions → THEN enforce RBAC/ABAC server-side — frontend hiding buttons ≠ security
- [ ] 🟡 IF using database IDs in URLs/APIs → THEN use UUIDs over sequential IDs — prevents enumeration attacks
- [ ] 🟡 IF multi-tenant system → THEN enforce row-level security at DB layer — defense in depth, not just app layer
- [ ] 🔴 IF API has admin/elevated endpoints → THEN verify privilege escalation is impossible (horizontal AND vertical)
- [ ] 🟡 IF using JWTs for authorization → THEN validate issuer, audience, expiry, and algorithm (reject `alg: none`)

---

## 🔄 State & Session

- [ ] 🔴 IF forms/mutations change state → THEN implement CSRF protection — anti-CSRF tokens or SameSite cookies
- [ ] 🔴 IF actions have side effects (payments, deletes, config changes) → THEN require idempotency keys — prevent replay/double-submit
- [ ] 🔴 IF using WebSockets or long-lived connections → THEN authenticate on connect AND validate messages — don't trust the pipe
- [ ] 🟡 IF handling concurrent requests on shared state → THEN implement proper locking / optimistic concurrency — race conditions are security bugs (TOCTOU)
- [ ] 🟡 IF caching responses → THEN ensure `Cache-Control: no-store` on authenticated/sensitive responses — prevent cache poisoning and data leakage
- [ ] 🟡 IF using Server-Sent Events (SSE) or EventSource → THEN validate Origin header + set proper CORS + no open redirect in URL params

---
