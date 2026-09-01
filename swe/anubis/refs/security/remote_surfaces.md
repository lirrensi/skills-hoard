# Security: Remote Surfaces

> Externally reachable attack surfaces: browsers, APIs, mobile clients, network edges, and abuse-prone product flows.
>
> Load this for web apps, public APIs, mobile clients, or anything reachable over a network.

---

## 🌐 Headers & Transport

- [ ] 🔴 IF serving HTTP responses → THEN set security headers: Content-Security-Policy, Strict-Transport-Security, X-Frame-Options, X-Content-Type-Options: nosniff
- [ ] 🔴 IF application is web-accessible → THEN HTTPS everywhere — redirect HTTP, no mixed content, HSTS preload
- [ ] 🔴 IF API uses CORS → THEN explicit origin allowlist — never `Access-Control-Allow-Origin: *` on authenticated endpoints
- [ ] 🟡 IF serving user-uploaded files → THEN serve from a separate domain/CDN with `Content-Disposition: attachment` — prevents stored XSS
- [ ] 🟡 IF using cookies → THEN set appropriate Path, Domain, and `__Host-`/`__Secure-` prefixes where possible
- [ ] 🟡 IF app sits behind a reverse proxy, load balancer, or CDN → THEN explicitly configure "trusted proxies" before evaluating `X-Forwarded-For` or `X-Real-IP` — prevents IP spoofing and rate-limit bypass
- [ ] 🟡 IF serving web app → THEN set `Permissions-Policy` header to restrict camera, mic, location, etc. — prevents opportunistic access via embedded content
- [ ] 🟡 IF cross-origin requests allowed → THEN set `Cross-Origin-Opener-Policy: same-origin` — prevents tab-napping via opener window
- [ ] 🟡 IF hosting sensitive resources → THEN set `Cross-Origin-Resource-Policy: same-origin` — prevents your resources from being embedded by malicious sites

---

## 🧬 API-Specific Security

- [ ] 🔴 IF API returns data → THEN filter response fields server-side — never return full DB objects (mass assignment / over-exposure)
- [ ] 🔴 IF API accepts nested/complex objects → THEN limit depth + size — prevent resource exhaustion via deeply nested JSON/GraphQL queries
- [ ] 🟡 IF API is public → THEN enforce rate limiting per-client — not just auth endpoints, ALL endpoints
- [ ] 🟡 IF API versioning exists → THEN deprecate and remove old versions — stale APIs are unpatched attack surface
- [ ] 🔴 IF GraphQL → THEN disable introspection in production, enforce query depth/cost limits, whitelist allowed queries
- [ ] 🔴 IF API receives webhooks from external services (Stripe, GitHub, Twilio, etc.) → THEN verify webhook signatures using the provider's signing secret — never trust payload authenticity based on source IP alone
- [ ] 🟡 IF API supports batch/bulk endpoints (`POST /users/bulk`, GraphQL batching, array of IDs) → THEN enforce per-request item limits + apply auth/rate-limits per sub-operation — prevents amplification attacks

---

## 🖥️ Frontend Security

- [ ] 🟡 IF loading scripts from CDNs → THEN use Subresource Integrity (SRI) — don't trust third-party CDNs blindly
```html
<script src="https://cdn.example.com/lib.js"
        integrity="sha384-abc123..."
        crossorigin="anonymous"></script>
```

- [ ] 🔴 IF sensitive data exists (tokens, passwords, PII) → THEN never put in URLs/query strings — leaked via browser history, referrer headers, server logs
- [ ] 🔴 IF rendering dynamic content → THEN never use `innerHTML`, `dangerouslySetInnerHTML`, `eval()`, `document.write()`, or `v-html` with untrusted data
- [ ] 🟡 IF client-side storage used (localStorage, sessionStorage, IndexedDB) → THEN never store secrets or sensitive PII — all are accessible to XSS
- [ ] 🟡 IF using `window.postMessage` or listening for message events → THEN always validate `event.origin` against an allowlist + schema-validate `event.data` — cross-origin message forgery leads to XSS and data exfiltration
- [ ] 🟡 IF application handles mobile deep links or custom URI schemes (`myapp://`) → THEN treat the entire URI payload as untrusted external input — prevents client-side execution and phishing

---

## 📱 Mobile & Native Clients

- [ ] 🔴 IF building mobile apps → THEN store nothing sensitive in SharedPreferences/Keychain without OS-level encryption (Android Keystore / iOS Secure Enclave) + biometric gating for high-risk actions
- [ ] 🔴 IF mobile app → THEN implement root/jailbreak detection + terminate if detected (or at minimum disable sensitive functionality)
- [ ] 🔴 IF using deep links/custom URL schemes → THEN validate + whitelist allowed domains/paths — prevent deep link hijacking
- [ ] 🟡 IF mobile app uses WebViews → THEN disable JavaScript Interface unless absolutely needed + use `file://` domain separation + CSP
- [ ] 🔴 IF distributing mobile app → THEN code-sign + verify signature at runtime (anti-tampering)
- [ ] 🟡 IF using WebRTC → THEN disable STUN/TURN IP leakage (RTCPeerConnection ICE candidate filtering) — prevents local IP exposure

---

## 🌐 Zero-Trust & Network Security

- [ ] 🔴 IF internal services talk to each other → THEN require mTLS everywhere — no "internal = trusted"
- [ ] 🔴 IF user auth → THEN implement continuous session risk scoring (impossible travel, device fingerprint changes, TOR exit nodes) + re-auth on high risk
- [ ] 🟡 IF remote access (SSH, RDP, bastion) → THEN require hardware security keys (YubiKey/WebAuthn) — no passwords/phishable MFA
- [ ] 🔴 IF any service account / machine identity exists → THEN use short-lived certs (SPIFFE/SPIRE, AWS IAM Roles Anywhere, GCP Workload Identity) — no long-lived service account keys
- [ ] 🟡 IF API keys exist → THEN scope them to exact IP + exact endpoint + exact permission + auto-expire after 90 days max
- [ ] 🟡 IF using caching layers (Redis, Memcached, etc.) → THEN disable public access + require auth + run in private VPC + encrypt sensitive data before caching
- [ ] 🟡 IF behind Cloudflare/AWS → THEN disable "I'm under attack mode" bypass techniques (direct IP access, old TLS versions)

---

## 💰 Business Logic & Abuse Prevention

- [ ] 🔴 IF processing payments, e-commerce, or quota limits → THEN calculate all prices, discounts, and totals securely on the backend — never trust or rely on pricing submitted by the frontend
- [ ] 🔴 IF coupons/gift cards/promos → THEN single-use + rate-limit redemption + atomic check-then-act — prevent race condition abuse
- [ ] 🟡 IF email/SMS verification codes → THEN rate-limit per user + per IP + expire in ≤10 min + one-time-use only
- [ ] 🔴 IF password reset / email change → THEN send delayed notification to old email ("email changed in 7 days unless canceled")
- [ ] 🟡 IF account recovery → THEN require multiple proofs + human review for high-value accounts
- [ ] 🔴 IF pricing/subscription logic → THEN use signed price IDs (Stripe style) — never trust client-sent price/amount
- [ ] 🟡 IF allowing bulk operations → THEN quota + cost analysis before execution — prevent "delete all my projects" abuse
- [ ] 🔴 IF accepting emails (contact forms, etc.) → THEN strip `\r\n` from user input — prevents SMTP header injection
- [ ] 🟡 IF using HTTP/2 or HTTP/3 → THEN test for request smuggling (TE/CL mismatches) — still possible

---
