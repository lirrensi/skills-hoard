# Testing Strategy & Verification (The Proof of Life)

> Load when: Bastet is asked "prove it works", asked about testing strategy, needs to verify a change, or needs to assess whether E2E / manual testing exists in a repo.
>
> This is the verification arm of Lens 8 (Runability). It defines WHAT to run, WHEN to run it, and HOW to report proof that the home actually works.

---

## The Philosophy

**"When you ask 'prove it works', Bastet doesn't guess. She runs the ladder."**

Tests exist to give you evidence. The strategy is a **ladder** — climb as high as the repo allows, then report exactly where the proof ends and why.

---

## The Verification Ladder

| Level | What | Speed | Example |
|-------|------|-------|---------|
| **1. Static** | Lint, typecheck, format | Seconds | `eslint`, `ruff`, `tsc --noEmit` |
| **2. Unit** | Fast tests, no services | < 60s | `./dev test-fast`, `npm test -- --runInBand` |
| **3. Integration** | Tests needing services (DB, redis) | < 10 min | `./dev test`, `docker compose up db` + suite |
| **4. E2E** | Full user flows in a real-ish environment (browser, real auth) | Slow, precious, most convincing | `./dev test-e2e`, Playwright/Cypress run |
| **5. Manual** | What automation cannot do: visual checks, physical devices, external services, judgment | Human time | Checklist with expected vs actual |

**Rule: climb as high as the environment allows, then say exactly where you stopped and why. Never call it "proven" if you only ran level 1.**

---

## E2E — Detect It First

Does the repo HAVE end-to-end tests? Look for:

- Configs: `playwright.config.*`, `cypress.config.*`, `detox.config.*`
- Directories: `e2e/`, `tests/e2e/`, `__tests__/e2e/`
- Scripts: `test:e2e`, `test:integration`, `e2e`, `test-e2e` (package.json, Makefile, justfile, `./dev`)
- Frameworks: Playwright, Cypress, Puppeteer, Detox, Appium (mobile)

**If E2E exists** → run it as part of any serious proof (when the environment allows; headless if no display).

**If E2E is missing** → say so explicitly. E2E absence is a **gap**, not a failure — report it in the proof, and flag it as a recommendation (Osiris's domain to write them; Bastet just makes the home testable).

---

## When To Run What

| Situation | Run | Evidence |
|-----------|-----|----------|
| Quick sanity while working | Level 1 + 2 (`test-fast`) | Exit code + pass/fail counts |
| Before commit | Level 1 + 2 (via `./dev check`) | Same + lint JSON if parseable |
| "Prove it works" for a feature | Levels 1→4, plus targeted tests by name | JUnit/JSON artifacts + targeted test output |
| Full verification (final) | Levels 1→5 | Full artifact set + manual checklist |
| Environment degraded (no Docker/display) | What's still possible, in order | State the degradation + what was skipped |

---

## The "Prove It Works" Protocol

When the user asks **"prove it works"**, do this — in order:

1. **State the plan** — "I'll prove X via: static → unit → integration → E2E → manual checklist."
2. **Baseline first** — run the existing suite BEFORE your changes context; note pre-existing failures. Never claim you broke something that was already red.
3. **Climb the ladder** — run each level, capture structured output (JUnit XML / JSON where available — see dev_environment artifact paths).
4. **Targeted proof** — for the specific feature or change: identify and run the exact test(s) that cover it, by name. This is the sharpest evidence.
5. **Manual checklist** — enumerate what needs eyes: visual layout, real auth flow, external payment, physical device. Provide commands so a human (or agent) can click through in minutes.
6. **Report** — a table of what passed / failed / skipped + why. Never write "works" without listing what was actually executed.

### The Proof Report Shape

```markdown
## Proof: <feature/change>
| Level | Ran? | Result | Evidence |
|-------|------|--------|----------|
| Static (lint/type) | ✅ | pass | lint.json |
| Unit | ✅ | 42/42 | junit.xml |
| Integration | ✅ | 12/12 | junit.xml |
| E2E | ⚠️ skipped | no display | headless unavailable |
| Manual | 🔶 pending | needs human eyes on checkout flow | checklist.md |

Not proven: <what remains unverified and why>.
```

---

## Manual Testing Checklist

How to build one (Bastet doesn't write tests, but she DOES write checklists):

1. Start from the feature's user journey (entry → action → result)
2. Split into buckets: **visual** (layout, states), **flows** (happy path, edge cases), **errors** (empty state, failure state, slow network)
3. Mark which items are automatable later → feed them to Osiris
4. Keep it under ~15 steps for humans: copy-pasteable commands, `Expected | Actual` columns
5. Note environment assumptions (staging creds, seeded users — dev_environment prescribes `admin@local.dev` etc.)

---

## Degraded Environments

| Limitation | Response |
|-----------|----------|
| No Docker | Unit only; integration/E2E skipped — say so |
| No display | Browser tests `--headless` only |
| External service unreachable (Stripe, SSO) | Mock it, document the substitution — real service stays on the manual checklist |
| Tests flaky | Check for a flaky quarantine (dev_environment); don't trust a 30% red |

---

## What Bastet Does NOT Do (And Who Does)

- **Write tests** → that's Osiris (the judge). Bastet makes the home testable, runs the ladder, and writes the manual checklists.
- **Design test data strategies** → seed data, factories, fixtures, test DB isolation — Osiris's domain. Bastet detects whether they exist and flags gaps.
- **Set coverage targets** → thresholds, exclusions, branch vs line — Osiris decides what's meaningful. Bastet detects whether coverage is configured and enforced.
- **Write smoke tests** → the fast deploy-time health checks are Osiris's to design. Bastet runs whatever exists and reports the results.
- **Claim coverage that wasn't run** → proof is only as good as what actually executed. A skipped level is a skipped level, reported with a reason.

When Bastet finds gaps — no E2E suite, no coverage config, no test data seeding, no smoke tests — she **flags them and routes to Osiris** for design. The documentation of what EXISTS and how to RUN it is Bastet's domain.

---

*Meow — proof, not promises.*
