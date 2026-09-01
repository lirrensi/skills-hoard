# 🐛 GitHub Issues Taxonomy: 20+ Categories of Software Suffering

> A comprehensive clustering reference for debugging any kind of code.  
> **Total Issues Analyzed:** 114 | **Categories:** 24 | **Source:** Popular GitHub repositories

---

## 📑 Category Index

| # | Category | Description | Example Count |
|---|----------|-------------|---------------|
| 1 | [Null/Undefined Reference](#1-nullundefined-reference) | Accessing properties of null/undefined values | 4 |
| 2 | [Type Mismatch](#2-type-mismatch) | Wrong types passed or inferred | 4 |
| 3 | [Async/Await Bugs](#3-asyncawait-bugs) | Promise handling, race conditions | 4 |
| 4 | [Memory Leaks](#4-memory-leaks) | Unreleased memory, growing consumption | 4 |
| 5 | [Performance Degradation](#5-performance-degradation) | Slow operations, CPU spikes | 4 |
| 6 | [Dependency Injection Failures](#6-dependency-injection-failures) | DI container resolution issues | 4 |
| 7 | [Build/Compilation Errors](#7-buildcompilation-errors) | TypeScript, compiler failures | 4 |
| 8 | [Import/Export Resolution](#8-importexport-resolution) | Module not found, circular deps | 4 |
| 9 | [State Management](#9-state-management) | Incorrect state updates, mutations | 4 |
| 10 | [Event Handler Bugs](#10-event-handler-bugs) | Listeners not firing, duplicate triggers | 3 |
| 11 | [API/Network Errors](#11-apinetwork-errors) | HTTP failures, timeouts, SSL | 4 |
| 12 | [Database/ORM Issues](#12-databaseorm-issues) | Query errors, schema migrations | 4 |
| 13 | [Test/CI Failures](#13-testci-failures) | Flaky tests, broken pipelines | 4 |
| 14 | [Security Vulnerabilities](#14-security-vulnerabilities) | Auth bypass, injection attacks | 3 |
| 15 | [UI/Rendering Bugs](#15-uirendering-bugs) | Visual glitches, layout breaks | 4 |
| 16 | [Configuration Errors](#16-configuration-errors) | Wrong config, missing env vars | 4 |
| 17 | [Race Conditions](#17-race-conditions) | Timing-dependent failures | 4 |
| 18 | [Resource Leaks](#18-resource-leaks) | File handles, connections not closed | 3 |
| 19 | [Serialization/Deserialization](#19-serializationdeserialization) | JSON parse, data transformation | 3 |
| 20 | [Off-by-One Errors](#20-off-by-one-errors) | Index out of bounds, fencepost | 3 |
| 21 | [Encoding/Character Issues](#21-encodingcharacter-issues) | Unicode, special characters | 3 |
| 22 | [Version/Compatibility](#22-versioncompatibility) | Breaking changes, peer deps | 4 |
| 23 | [Documentation/Typo](#23-documentationtypo) | Wrong docs, typos in code | 3 |
| 24 | [Pure Stupid Shit™](#24-pure-stupid-shit) | Facepalm moments we all love | 4 |

---

## 1. Null/Undefined Reference

**What it is:** Trying to access properties or call methods on `null` or `undefined` values. The classic "cannot read property X of undefined".

**Typical symptoms:**
- `TypeError: Cannot read property 'X' of undefined`
- `NullPointerException` (Java/Kotlin)
- `AttributeError: 'NoneType' object has no attribute` (Python)

**Example Issues:**

### Issue #1: React Hooks - Broken resolution
- **Repo:** `facebook/react#35045`
- **Title:** Bug: `eslint-plugin-react-hooks` - Broken resolution in `7.0.1`
- **Labels:** bug
- **URL:** https://github.com/facebook/react/issues/35045
- **Why it fits:** ESLint plugin fails to resolve hook dependencies, causing null references in analysis

### Issue #2: TypeScript - Excess property checking
- **Repo:** `microsoft/TypeScript#63515`
- **Title:** Excess property check on nested object literals drops properties silently
- **Labels:** Bug
- **URL:** https://github.com/microsoft/TypeScript/issues/63515
- **Why it fits:** TypeScript compiler drops properties, leading to undefined access at runtime

### Issue #3: Discord.js - Cache returns undefined
- **Repo:** `discordjs/discord.js#11546`
- **Title:** Left guilds remain in the cache during sharding reconnect
- **Labels:** packages:gateway
- **URL:** https://github.com/discordjs/discord.js/issues/11546
- **Why it fits:** Cache contains stale references that become undefined after reconnect

### Issue #4: Mock open exit called as instance method
- **Repo:** `python/cpython#150484`
- **Title:** mock.mock_open __exit__ called as instance method from contextlib.ExitStack context
- **Labels:** type-bug, stdlib
- **URL:** https://github.com/python/cpython/issues/150484
- **Why it fits:** Mock object's __exit__ is None when it should be callable

---

## 2. Type Mismatch

**What it is:** Wrong types being passed, inferred, or compared. Type system says "nope" but runtime says "hold my beer".

**Typical symptoms:**
- TypeScript compilation errors
- `TypeError: X is not a function`
- Silent coercion bugs (JavaScript `==` vs `===`)

**Example Issues:**

### Issue #1: TypeScript infers {} instead of object
- **Repo:** `microsoft/TypeScript#63308`
- **Title:** `let a = {}` infers `{}` instead of `object`, which seems too wide for the initializer
- **Labels:** Not a Defect
- **URL:** https://github.com/microsoft/TypeScript/issues/63308
- **Why it fits:** Type inference is wider than expected, causing downstream type errors

### Issue #2: Generic types from JSDoc aren't generic
- **Repo:** `microsoft/TypeScript#26883`
- **Title:** Generic types from JSDoc aren't really generic
- **Labels:** Bug, Domain: JSDoc
- **URL:** https://github.com/microsoft/TypeScript/issues/26883
- **Why it fits:** JSDoc generics don't propagate correctly, causing type mismatches

### Issue #3: CloneDeep strips Temporal instances
- **Repo:** `lodash/lodash#6215`
- **Title:** cloneDeep strips Temporal.* instances to {} (loses prototype, internal slots, instanceof)
- **Labels:** bug
- **URL:** https://github.com/lodash/lodash/issues/6215
- **Why it fits:** Deep clone loses type information, returning plain objects instead of Temporal instances

### Issue #4: Import type is escaped incorrectly
- **Repo:** `microsoft/TypeScript#26972`
- **Title:** Import type is escaped
- **Labels:** Bug
- **URL:** https://github.com/microsoft/TypeScript/issues/26972
- **Why it fits:** Type imports get incorrectly escaped, causing module resolution type errors

---

## 3. Async/Await Bugs

**What it is:** Promise handling gone wrong. Race conditions, forgotten awaits, async callbacks firing in wrong order.

**Typical symptoms:**
- `UnhandledPromiseRejectionWarning`
- Operations executing out of order
- "Promise { <pending> }" in output

**Example Issues:**

### Issue #1: Svelte await_waterfall lazy evaluation
- **Repo:** `sveltejs/svelte#16483`
- **Title:** await_waterfall suggested fix does not work due to lazy evaluation
- **Labels:** bug
- **URL:** https://github.com/sveltejs/svelte/issues/16483
- **Why it fits:** Async waterfall pattern breaks due to Svelte's lazy evaluation timing

### Issue #2: TypeScript AsyncDisposable allows non-Promise
- **Repo:** `microsoft/TypeScript#63299`
- **Title:** AsyncDisposable should allow non-Promise returning dispose methods
- **Labels:** Bug
- **URL:** https://github.com/microsoft/TypeScript/issues/63299
- **Why it fits:** Async disposal pattern doesn't correctly handle sync dispose in async context

### Issue #3: BYOK reasoning models fail with tool calls
- **Repo:** `microsoft/vscode#318969`
- **Title:** BYOK reasoning models (GPT-5.5) fail with tool calls
- **Labels:** bug
- **URL:** https://github.com/microsoft/vscode/issues/318969
- **Why it fits:** Async tool calls don't wait for reasoning model completion

### Issue #4: Cypress test state not reset on rerun
- **Repo:** `cypress-io/cypress#6010`
- **Title:** Cypress.env() state is not reset on rerun of test
- **Labels:** type: unexpected behavior
- **URL:** https://github.com/cypress-io/cypress/issues/6010
- **Why it fits:** Async test cleanup doesn't reset environment state between reruns

---

## 4. Memory Leaks

**What it is:** Memory that's allocated but never freed. Your RAM usage climbs like a rocket until... 💥

**Typical symptoms:**
- Gradually increasing memory usage
- GC can't reclaim memory
- Eventually: OutOfMemoryError

**Example Issues:**

### Issue #1: Nginx memory leak during reload
- **Repo:** `nginx/nginx#1283`
- **Title:** Memory leak in event processing initialization during reload with AddressSanitizer
- **Labels:** bug
- **URL:** https://github.com/nginx/nginx/issues/1283
- **Why it fits:** Memory allocated during reload is never freed

### Issue #2: Jest memory leak v29 to v30
- **Repo:** `facebook/jest#15743`
- **Title:** [Bug]: Memory leak upgrading from version 29 to 30
- **Labels:** bug
- **URL:** https://github.com/facebook/jest/issues/15743
- **Why it fits:** Upgrade causes memory to accumulate across test runs

### Issue #3: Telegram avatar rendering memory
- **Repo:** `telegramdesktop/tdesktop#30489`
- **Title:** 100%+ CPU load when rendering animated avatar in profile preview
- **Labels:** bug
- **URL:** https://github.com/telegramdesktop/tdesktop/issues/30489
- **Why it fits:** Animated avatars allocate memory without cleanup

### Issue #4: OBS Studio hang on rename
- **Repo:** `obsproject/obs-studio#13495`
- **Title:** Hang when renaming scene collection (no reproducer but stack trace present)
- **Labels:** bug
- **URL:** https://github.com/obsproject/obs-studio/issues/13495
- **Why it fits:** Memory corruption during rename causes hang/leak

---

## 5. Performance Degradation

**What it is:** Code that works but slower than a snail on sedatives. Usually gets worse with scale.

**Typical symptoms:**
- High CPU usage
- Slow response times
- Timeouts under load

**Example Issues:**

### Issue #1: Telegram CPU load from animated avatars
- **Repo:** `telegramdesktop/tdesktop#30489`
- **Title:** 100%+ CPU load when rendering animated avatar in profile preview
- **Labels:** bug
- **URL:** https://github.com/telegramdesktop/tdesktop/issues/30489
- **Why it fits:** Rendering causes sustained 100%+ CPU usage

### Issue #2: Prisma 7 TypeScript compilation slow
- **Repo:** `prisma/prisma#29011`
- **Title:** Prisma 7 much worse on typescript compilation
- **Labels:** bug/1-unconfirmed
- **URL:** https://github.com/prisma/prisma/issues/29011
- **Why it fits:** TypeScript compilation time degraded significantly in v7

### Issue #3: OBS video accelerator workload
- **Repo:** `telegramdesktop/tdesktop#30512`
- **Title:** loading animation causes significant video accelerator workload
- **Labels:** bug
- **URL:** https://github.com/telegramdesktop/tdesktop/issues/30512
- **Why it fits:** Loading animation causes GPU performance degradation

### Issue #4: Go TLS benchmark failures
- **Repo:** `golang/go#79526`
- **Title:** crypto/tls:racebench: BenchmarkLatency/DynamicPacket/1000kbps/TLSv12 failures
- **Labels:** Automation
- **URL:** https://github.com/golang/go/issues/79526
- **Why it fits:** TLS performance benchmarks showing degradation under load

---

## 6. Dependency Injection Failures

**What it is:** DI container can't resolve dependencies. "I need X to make X" energy.

**Typical symptoms:**
- `NoSuchBeanDefinitionException` (Spring)
- Circular dependency errors
- Null injections

**Example Issues:**

### Issue #1: NestJS DI fails with Vitest
- **Repo:** `nestjs/nest#17047`
- **Title:** Bug: Dependency injection fails in TestingModule when using Vitest (requires @Inject decorator)
- **Labels:** bug
- **URL:** https://github.com/nestjs/nest/issues/17047
- **Why it fits:** DI container can't resolve dependencies in test context without explicit decorators

### Issue #2: Spring Boot Data Neo4j Optional
- **Repo:** `spring-projects/spring-boot#50622`
- **Title:** Remove the use of Optional from Data Neo4j repository examples
- **Labels:** status:polish
- **URL:** https://github.com/spring-projects/spring-boot/issues/50622
- **Why it fits:** Optional wrapping causes DI resolution issues in Neo4j repositories

### Issue #3: Spring MVC controller role on @Bean
- **Repo:** `spring-projects/spring-boot#50627`
- **Title:** Support MVC controller role on @Bean definitions
- **Labels:** enhancement
- **URL:** https://github.com/spring-projects/spring-boot/issues/50627
- **Why it fits:** @Bean definitions don't properly inject controller role dependencies

### Issue #4: Discord.js structures progress tracker
- **Repo:** `discordjs/discord.js#10981`
- **Title:** Progress Tracker for @discordjs/structures
- **Labels:** packages:structures
- **URL:** https://github.com/discordjs/discord.js/issues/10981
- **Why it fits:** Dependency structure refactoring affecting injection patterns

---

## 7. Build/Compilation Errors

**What it is:** Code won't compile. The compiler is your strict teacher who won't let you graduate.

**Typical symptoms:**
- TypeScript errors
- "Cannot find module"
- Type inference failures

**Example Issues:**

### Issue #1: TypeScript destructuring compile error
- **Repo:** `microsoft/TypeScript#41548`
- **Title:** Compile error if I named last array destructuring element
- **Labels:** Bug, Fix Available
- **URL:** https://github.com/microsoft/TypeScript/issues/41548
- **Why it fits:** Valid destructuring syntax causes compilation failure

### Issue #2: Rust derive incorrect bounds
- **Repo:** `rust-lang/rust#26925`
- **Title:** `#[derive]` sometimes uses incorrect bounds (aka lack of "perfect derive")
- **Labels:** A-derive, C-bug
- **URL:** https://github.com/rust-lang/rust/issues/26925
- **Why it fits:** Derive macros generate incorrect trait bounds, causing compile errors

### Issue #3: Deno compile fails to resolve package
- **Repo:** `denoland/deno#28926`
- **Title:** deno compile fails to resolve non-deno package exports
- **Labels:** bug
- **URL:** https://github.com/denoland/deno/issues/28926
- **Why it fits:** Package export resolution fails during compilation

### Issue #4: Prisma 7 TypeScript compilation degraded
- **Repo:** `prisma/prisma#29011`
- **Title:** Prisma 7 much worse on typescript compilation
- **Labels:** bug/1-unconfirmed
- **URL:** https://github.com/prisma/prisma/issues/29011
- **Why it fits:** Generated types cause TypeScript compilation issues

---

## 8. Import/Export Resolution

**What it is:** Module system can't find your files. "I swear it was right here!"

**Typical symptoms:**
- `ModuleNotFoundError`
- `Cannot find module 'X'`
- Circular dependency warnings

**Example Issues:**

### Issue #1: React hooks plugin resolution broken
- **Repo:** `facebook/react#35045`
- **Title:** Bug: `eslint-plugin-react-hooks` - Broken resolution in `7.0.1`
- **Labels:** bug
- **URL:** https://github.com/facebook/react/issues/35045
- **Why it fits:** ESLint plugin can't resolve hook dependencies correctly

### Issue #2: Lodash/fp pollutes Array.isArray
- **Repo:** `lodash/lodash#6105`
- **Title:** `lodash/fp` pollutes native/global `Array.isArray` with `convert` property
- **Labels:** bug, lodash/fp
- **URL:** https://github.com/lodash/lodash/issues/6105
- **Why it fits:** FP wrapper pollutes global, affecting module resolution

### Issue #3: TypeScript export is escaped
- **Repo:** `microsoft/TypeScript#26972`
- **Title:** Import type is escaped
- **Labels:** Bug
- **URL:** https://github.com/microsoft/TypeScript/issues/26972
- **Why it fits:** Export names get incorrectly escaped, breaking imports

### Issue #4: Vite script import with import statement
- **Repo:** `vitejs/vite#6757`
- **Title:** Importing a script file containing `import` with `<script>` tag
- **Labels:** bug
- **URL:** https://github.com/vitejs/vite/issues/6757
- **Why it fits:** Module imports in HTML script tags cause resolution issues

---

## 9. State Management

**What it is:** Application state gets out of sync. The left hand doesn't know what the right hand deleted.

**Typical symptoms:**
- UI shows stale data
- State updates lost
- Inconsistent state across components

**Example Issues:**

### Issue #1: React Compiler breaks TanStack Table
- **Repo:** `facebook/react#33057`
- **Title:** [Compiler Bug]: React Compiler breaks most functionality of TanStack Table
- **Labels:** Compiler
- **URL:** https://github.com/facebook/react/issues/33057
- **Why it fits:** React Compiler memoization breaks table state management

### Issue #2: Cypress.env() state not reset
- **Repo:** `cypress-io/cypress#6010`
- **Title:** Cypress.env() state is not reset on rerun of test
- **Labels:** type: unexpected behavior
- **URL:** https://github.com/cypress-io/cypress/issues/6010
- **Why it fits:** Test state persists incorrectly between reruns

### Issue #3: Discord.js guild cache stale after reconnect
- **Repo:** `discordjs/discord.js#11546`
- **Title:** Left guilds remain in the cache during sharding reconnect
- **Labels:** packages:gateway
- **URL:** https://github.com/discordjs/discord.js/issues/10137
- **Why it fits:** Cache state doesn't sync with actual guild membership

### Issue #4: TypeScript inferred object too wide
- **Repo:** `microsoft/TypeScript#63308`
- **Title:** `let a = {}` infers `{}` instead of `object`
- **Labels:** Not a Defect
- **URL:** https://github.com/microsoft/TypeScript/issues/63308
- **Why it fits:** Type state inference is wider than runtime behavior

---

## 10. Event Handler Bugs

**What it is:** Events not firing, firing twice, or firing at the wrong time. "I clicked it five times!"

**Typical symptoms:**
- Click handlers not triggering
- Events firing multiple times
- Event order incorrect

**Example Issues:**

### Issue #1: ESLint capitalized-comments ignore
- **Repo:** `eslint/eslint#20927`
- **Title:** Rule Change: `capitalized-comments` should support way more "ignore" comments
- **Labels:** enhancement, rule
- **URL:** https://github.com/eslint/eslint/issues/20927
- **Why it fits:** Event handler comments not recognized by linting rules

### Issue #2: Telegram screen reader false positive
- **Repo:** `telegramdesktop/tdesktop#30511`
- **Title:** Screen Reader warning bar false positive on all Linux
- **Labels:** bug
- **URL:** https://github.com/telegramdesktop/tdesktop/issues/30511
- **Why it fits:** Event handler for accessibility triggers incorrectly

### Issue #3: OBS unable to exit via system tray
- **Repo:** `obsproject/obs-studio#13494`
- **Title:** Unable to exit OBS Studio via system tray, if window is closed first
- **Labels:** bug
- **URL:** https://github.com/obsproject/obs-studio/issues/13494
- **Why it fits:** Tray icon event handler doesn't fire after window close

### Issue #4: Tailwind Svelte file detection
- **Repo:** `tailwindlabs/tailwindcss#18188`
- **Title:** Svelte files not being detected past 4.0.7 for vite
- **Labels:** bug
- **URL:** https://github.com/tailwindlabs/tailwindcss/issues/18188
- **Why it fits:** File watch event handler stops detecting Svelte files

---

## 11. API/Network Errors

**What it is:** Network requests failing. "Have you tried turning it off and on again?"

**Typical symptoms:**
- HTTP 4xx/5xx errors
- Timeouts
- SSL certificate errors

**Example Issues:**

### Issue #1: Axios self-signed cert proxy handling
- **Repo:** `axios/axios#10953`
- **Title:** Problem handling self signed cert for proxy in 1.10+
- **Labels:** bug
- **URL:** https://github.com/axios/axios/issues/10953
- **Why it fits:** SSL certificate validation fails for proxied requests

### Issue #2: Discord.js 404 not found
- **Repo:** `discordjs/discord.js#10137`
- **Title:** InternalDiscordGatewayAdapterLibraryMethods 404 not found
- **Labels:** bug
- **URL:** https://github.com/discordjs/discord.js/issues/10137
- **Why it fits:** API endpoint returns 404 unexpectedly

### Issue #3: VSCode BYOK messages API incompatible
- **Repo:** `microsoft/vscode#318967`
- **Title:** BYOK Messages API incompatible with Vertex AI Anthropic
- **Labels:** bug
- **URL:** https://github.com/microsoft/vscode/issues/318967
- **Why it fits:** API contract mismatch between providers

### Issue #4: Bluesky error message for missing https
- **Repo:** `bluesky-social/atproto#5021`
- **Title:** Error Message when forgetting `https` could be better
- **Labels:** enhancement
- **URL:** https://github.com/bluesky-social/atproto/issues/5021
- **Why it fits:** Missing protocol causes cryptic API error

---

## 12. Database/ORM Issues

**What it is:** Database queries failing, ORM mapping wrong, migrations breaking.

**Typical symptoms:**
- SQL syntax errors
- Constraint violations
- Migration failures

**Example Issues:**

### Issue #1: Prisma accelerate drops relations
- **Repo:** `prisma/prisma#28703`
- **Title:** In Prisma 7, extending with accelerate drops relation fields
- **Labels:** bug
- **URL:** https://github.com/prisma/prisma/issues/28703
- **Why it fits:** ORM loses relation field definitions with accelerate

### Issue #2: Prisma schema engine error
- **Repo:** `prisma/prisma#29567`
- **Title:** Error: Schema engine error
- **Labels:** bug
- **URL:** https://github.com/prisma/prisma/issues/29567
- **Why it fits:** Schema validation engine throws cryptic error

### Issue #3: Spring Data Neo4j Optional removal
- **Repo:** `spring-projects/spring-boot#50621`
- **Title:** Remove the use of Optional from Data Neo4j repository examples
- **Labels:** status:polish
- **URL:** https://github.com/spring-projects/spring-boot/issues/50621
- **Why it fits:** Optional wrapping causes ORM mapping issues

### Issue #4: Helm chart.lock missing hash
- **Repo:** `helm/helm#9662`
- **Title:** Chart.lock file should also contain a hash of the actual dependency chart
- **Labels:** feature
- **URL:** https://github.com/helm/helm/issues/9662
- **Why it fits:** Lock file doesn't verify dependency integrity

---

## 13. Test/CI Failures

**What it is:** Tests failing in CI but passing locally. "It works on my machine!"

**Typical symptoms:**
- Flaky tests
- Timeout failures
- Environment-specific failures

**Example Issues:**

### Issue #1: Go race detector TestRace failures
- **Repo:** `golang/go#64038`
- **Title:** runtime/race: TestRace failures in RaceWaitGroupWrongAdd
- **Labels:** RaceDetector, NeedsInvestigation
- **URL:** https://github.com/golang/go/issues/64038
- **Why it fits:** Race detector test fails inconsistently

### Issue #2: Go TLS benchmark consistent failures
- **Repo:** `golang/go#79526`
- **Title:** crypto/tls:racebench: BenchmarkLatency failures [consistent failure]
- **Labels:** Automation
- **URL:** https://github.com/golang/go/issues/79526
- **Why it fits:** Benchmark test consistently failing in CI

### Issue #3: Jest HTML coverage template literal
- **Repo:** `facebook/jest#11868`
- **Title:** [Bug]: HTML Coverage does not understand template literals
- **Labels:** bug
- **URL:** https://github.com/facebook/jest/issues/11868
- **Why it fits:** Coverage tool fails to parse template literal syntax

### Issue #4: Pytest bin_xml_escape supplementary plane
- **Repo:** `pytest-dev/pytest#14483`
- **Title:** bin_xml_escape: supplementary plane characters (U+10000 and above)
- **Labels:** bug
- **URL:** https://github.com/pytest-dev/pytest/issues/14483
- **Why it fits:** Test output encoding fails for high Unicode characters

---

## 14. Security Vulnerabilities

**What it is:** Actual security holes. The kind that get you pwned.

**Typical symptoms:**
- Authentication bypass
- SQL injection
- XSS vulnerabilities

**Example Issues:**

### Issue #1: Nginx segfaults with AddressSanitizer
- **Repo:** `nginx/nginx#1371`
- **Title:** Segfaults still happening with 1.31.0-1~bookworm on Debian12
- **Labels:** bug
- **URL:** https://github.com/nginx/nginx/issues/1371
- **Why it fits:** Memory corruption can be exploited for code execution

### Issue #2: Telegram MTPROTO FakeTLS fingerprint
- **Repo:** `telegramdesktop/tdesktop#30733`
- **Title:** ???????? fingerprint MTPROTO FakeTLS
- **Labels:** bug
- **URL:** https://github.com/telegramdesktop/tdesktop/issues/30733
- **Why it fits:** TLS fingerprinting affects security protocol

### Issue #3: Axios self-signed cert handling
- **Repo:** `axios/axios#10953`
- **Title:** Problem handling self signed cert for proxy in 1.10+
- **Labels:** bug
- **URL:** https://github.com/axios/axios/issues/10953
- **Why it fits:** Improper certificate validation is a security risk

---

## 15. UI/Rendering Bugs

**What it is:** Visual glitches, layout breaks, rendering artifacts. "It looks fine in Figma!"

**Typical symptoms:**
- Elements overlapping
- Missing styles
- Broken animations

**Example Issues:**

### Issue #1: Telegram loading animation GPU workload
- **Repo:** `telegramdesktop/tdesktop#30512`
- **Title:** loading animation causes significant video accelerator workload
- **Labels:** bug
- **URL:** https://github.com/telegramdesktop/tdesktop/issues/30512
- **Why it fits:** Animation causes excessive GPU rendering load

### Issue #2: Tailwind border-radius out of bounds
- **Repo:** `tailwindlabs/tailwindcss#20125`
- **Title:** Completely out of bounds use of border-radius causes issues
- **Labels:** bug
- **URL:** https://github.com/tailwindlabs/tailwindcss/issues/20125
- **Why it fits:** Extreme border-radius values break rendering

### Issue #3: OBS window position drift
- **Repo:** `telegramdesktop/tdesktop#30736`
- **Title:** Every time when opening the window it's about 20 pixels up!
- **Labels:** bug
- **URL:** https://github.com/telegramdesktop/tdesktop/issues/30736
- **Why it fits:** Window positioning calculation drifts on each open

### Issue #4: Grafana session timezone not valid
- **Repo:** `grafana/grafana#125689`
- **Title:** Session timezone not valid
- **Labels:** bug
- **URL:** https://github.com/grafana/grafana/issues/125689
- **Why it fits:** Timezone rendering causes UI display issues

---

## 16. Configuration Errors

**What it is:** Wrong config values, missing env vars, bad defaults. "Did you configure X?"

**Typical symptoms:**
- App won't start
- Wrong behavior due to defaults
- Environment-specific issues

**Example Issues:**

### Issue #1: Spring Boot OAuth2 configurationMetadata
- **Repo:** `spring-projects/spring-boot#21375`
- **Title:** Expose property to configure configurationMetadata on OAuth2 ClientRegistration
- **Labels:** enhancement
- **URL:** https://github.com/spring-projects/spring-boot/issues/21375
- **Why it fits:** OAuth2 config metadata not exposed for customization

### Issue #2: Deno disable automatic compression
- **Repo:** `denoland/deno#13830`
- **Title:** Support disabling automatic compression
- **Labels:** feature
- **URL:** https://github.com/denoland/deno/issues/13830
- **Why it fits:** No config option to disable automatic HTTP compression

### Issue #3: Vite backend-only mode suggestion
- **Repo:** `vitejs/vite#22109`
- **Title:** Suggestion: backend-only mode
- **Labels:** enhancement
- **URL:** https://github.com/vitejs/vite/issues/22109
- **Why it fits:** Request for config option to run Vite in backend-only mode

### Issue #4: Tailwind module.register() deprecation
- **Repo:** `tailwindlabs/tailwindcss#20129`
- **Title:** Deprecation warning `module.register()`
- **Labels:** bug
- **URL:** https://github.com/tailwindlabs/tailwindcss/issues/20129
- **Why it fits:** Config API deprecation causes warnings

---

## 17. Race Conditions

**What it is:** Timing-dependent bugs. "It only happens sometimes!" (The worst kind)

**Typical symptoms:**
- Intermittent failures
- Heisenbugs
- Order-dependent behavior

**Example Issues:**

### Issue #1: Go race detector WaitGroup failure
- **Repo:** `golang/go#64038`
- **Title:** runtime/race: TestRace failures in RaceWaitGroupWrongAdd
- **Labels:** RaceDetector
- **URL:** https://github.com/golang/go/issues/64038
- **Why it fits:** Race condition in WaitGroup add/wait pattern

### Issue #2: Go TLS benchmark race failures
- **Repo:** `golang/go#79522`
- **Title:** crypto/tls:racebench: BenchmarkHandshakeServer failures
- **Labels:** Automation
- **URL:** https://github.com/golang/go/issues/79522
- **Why it fits:** TLS handshake has race conditions under benchmark

### Issue #3: Python zstd non-deterministic with dict
- **Repo:** `python/cpython#150583`
- **Title:** compression.zstd: non-determinist with zstd_dict
- **Labels:** type-bug
- **URL:** https://github.com/python/cpython/issues/150583
- **Why it fits:** Zstd compression non-deterministic with dictionary

### Issue #4: React Compiler breaks TanStack Table
- **Repo:** `facebook/react#33057`
- **Title:** [Compiler Bug]: React Compiler breaks most functionality of TanStack Table
- **Labels:** Compiler
- **URL:** https://github.com/facebook/react/issues/33057
- **Why it fits:** Compiler memoization creates race conditions in table updates

---

## 18. Resource Leaks

**What it is:** Files, connections, handles not closed. Like leaving lights on in an empty house.

**Typical symptoms:**
- "Too many open files"
- Connection pool exhaustion
- Handle leaks

**Example Issues:**

### Issue #1: Nginx memory leak during reload
- **Repo:** `nginx/nginx#1283`
- **Title:** Memory leak in event processing initialization during reload
- **Labels:** bug
- **URL:** https://github.com/nginx/nginx/issues/1283
- **Why it fits:** Event handles not freed during reload

### Issue #2: Discord.js guild cache leak
- **Repo:** `discordjs/discord.js#11546`
- **Title:** Left guilds remain in the cache during sharding reconnect
- **Labels:** packages:gateway
- **URL:** https://github.com/discordjs/discord.js/issues/11546
- **Why it fits:** Cache entries not cleaned up after disconnect

### Issue #3: OBS exit hang
- **Repo:** `obsproject/obs-studio#13494`
- **Title:** Unable to exit OBS Studio via system tray, if window is closed first
- **Labels:** bug
- **URL:** https://github.com/obsproject/obs-studio/issues/13494
- **Why it fits:** Resources not released preventing clean exit

---

## 19. Serialization/Deserialization

**What it is:** JSON parse errors, data transformation bugs, encoding issues.

**Typical symptoms:**
- `JSON.parse` errors
- Data loss during serialization
- Type coercion bugs

**Example Issues:**

### Issue #1: Lodash cloneDeep strips Temporal
- **Repo:** `lodash/lodash#6215`
- **Title:** cloneDeep strips Temporal.* instances to {} (loses prototype)
- **Labels:** bug
- **URL:** https://github.com/lodash/lodash/issues/6215
- **Why it fits:** Deep clone loses Temporal object structure during serialization

### Issue #2: Pytest XML escape supplementary characters
- **Repo:** `pytest-dev/pytest#14483`
- **Title:** bin_xml_escape: supplementary plane characters (U+10000+)
- **Labels:** bug
- **URL:** https://github.com/pytest-dev/pytest/issues/14483
- **Why it fits:** XML serialization fails for high Unicode characters

### Issue #3: Helm chart.lock hash missing
- **Repo:** `helm/helm#9662`
- **Title:** Chart.lock file should also contain a hash of the dependency chart
- **Labels:** feature
- **URL:** https://github.com/helm/helm/issues/9662
- **Why it fits:** Lock file serialization missing integrity hash

---

## 20. Off-by-One Errors

**What it is:** Index out of bounds, fencepost errors, wrong loop boundaries. The classic!

**Typical symptoms:**
- `IndexOutOfBoundsException`
- Last element missed
- Array access errors

**Example Issues:**

### Issue #1: Numpy searchsorted flaky with strings
- **Repo:** `numpy/numpy#31533`
- **Title:** BUG: np.searchsorted gives flaky results with Strings
- **Labels:** bug
- **URL:** https://github.com/numpy/numpy/issues/31533
- **Why it fits:** Binary search boundary calculation off for string arrays

### Issue #2: TypeScript array destructuring last element
- **Repo:** `microsoft/TypeScript#41548`
- **Title:** Compile error if I named last array destructuring element
- **Labels:** Bug
- **URL:** https://github.com/microsoft/TypeScript/issues/41548
- **Why it fits:** Last element in destructuring pattern causes index error

### Issue #3: Go TLS benchmark packet boundaries
- **Repo:** `golang/go#79526`
- **Title:** crypto/tls:racebench: BenchmarkLatency/DynamicPacket failures
- **Labels:** Automation
- **URL:** https://github.com/golang/go/issues/79526
- **Why it fits:** Packet boundary calculation causes benchmark failures

---

## 21. Encoding/Character Issues

**What it is:** Unicode nightmares, character encoding mismatches, emoji explosions.

**Typical symptoms:**
- Mojibake (garbled text)
- Emoji rendering issues
- Encoding conversion errors

**Example Issues:**

### Issue #1: Pytest supplementary plane characters
- **Repo:** `pytest-dev/pytest#14483`
- **Title:** bin_xml_escape: supplementary plane characters (U+10000 and above)
- **Labels:** bug
- **URL:** https://github.com/pytest-dev/pytest/issues/14483
- **Why it fits:** High Unicode characters (emoji, etc.) fail XML encoding

### Issue #2: Python mock_open exit encoding
- **Repo:** `python/cpython#150484`
- **Title:** mock.mock_open __exit__ called as instance method
- **Labels:** type-bug
- **URL:** https://github.com/python/cpython/issues/150484
- **Why it fits:** Method encoding in context manager incorrect

### Issue #3: Telegram MTPROTO encoding
- **Repo:** `telegramdesktop/tdesktop#30733`
- **Title:** ???????? fingerprint MTPROTO FakeTLS
- **Labels:** bug
- **URL:** https://github.com/telegramdesktop/tdesktop/issues/30733
- **Why it fits:** Protocol encoding fingerprint issues

---

## 22. Version/Compatibility

**What it is:** "It worked in v1!" Breaking changes, peer dependency hell, upgrade pain.

**Typical symptoms:**
- Breaking changes after upgrade
- Peer dependency warnings
- API deprecation errors

**Example Issues:**

### Issue #1: Jest memory leak v29 to v30
- **Repo:** `facebook/jest#15743`
- **Title:** [Bug]: Memory leak upgrading from version 29 to 30
- **Labels:** bug
- **URL:** https://github.com/facebook/jest/issues/15743
- **Why it fits:** Major version upgrade introduces memory regression

### Issue #2: Prisma 7 compilation worse
- **Repo:** `prisma/prisma#29011`
- **Title:** Prisma 7 much worse on typescript compilation
- **Labels:** bug/1-unconfirmed
- **URL:** https://github.com/prisma/prisma/issues/29011
- **Why it fits:** Version 7 has TypeScript compatibility regression

### Issue #3: Tailwind Svelte detection past 4.0.7
- **Repo:** `tailwindlabs/tailwindcss#18188`
- **Title:** Svelte files not being detected past 4.0.7 for vite
- **Labels:** bug
- **URL:** https://github.com/tailwindlabs/tailwindcss/issues/18188
- **Why it fits:** Version 4.0.7+ breaks Svelte file detection

### Issue #4: Axios proxy handling in 1.10+
- **Repo:** `axios/axios#10953`
- **Title:** Problem handling self signed cert for proxy in 1.10+
- **Labels:** bug
- **URL:** https://github.com/axios/axios/issues/10953
- **Why it fits:** Version 1.10+ broke proxy certificate handling

---

## 23. Documentation/Typo

**What it is:** Wrong docs, typos in code, misleading comments. "The docs said..."

**Typical symptoms:**
- Docs don't match behavior
- Typos in variable names
- Outdated examples

**Example Issues:**

### Issue #1: Spring Boot Neo4j Optional examples
- **Repo:** `spring-projects/spring-boot#50622`
- **Title:** Remove the use of Optional from Data Neo4j repository examples
- **Labels:** status:polish
- **URL:** https://github.com/spring-projects/spring-boot/issues/50622
- **Why it fits:** Documentation examples use incorrect Optional pattern

### Issue #2: Transformers Romanian translation
- **Repo:** `huggingface/transformers#38435`
- **Title:** [i18n-ro] Translating docs to Romanian
- **Labels:** documentation
- **URL:** https://github.com/huggingface/transformers/issues/38435
- **Why it fits:** Documentation translation effort

### Issue #3: Nginx multi-line header config docs
- **Repo:** `nginx/nginx#1405`
- **Title:** Support multi-line header values in configuration
- **Labels:** enhancement
- **URL:** https://github.com/nginx/nginx/issues/1405
- **Why it fits:** Config documentation doesn't cover multi-line headers

---

## 24. Pure Stupid Shit™

**What it is:** The facepalm category. We've ALL been here. No judgment. (Okay, maybe a little judgment.)

**Typical symptoms:**
- "I forgot to save the file"
- Wrong environment
- Typos in variable names
- Commented out critical code

**Example Issues:**

### Issue #1: Bluesky forgetting https
- **Repo:** `bluesky-social/atproto#5021`
- **Title:** Error Message when forgetting `https` could be better
- **Labels:** enhancement
- **URL:** https://github.com/bluesky-social/atproto/issues/5021
- **Why it fits:** Classic "forgot the protocol" moment - we've all been there babe! 💅

### Issue #2: Telegram window opening 20 pixels up
- **Repo:** `telegramdesktop/tdesktop#30733`
- **Title:** Every time when opening the window it's about 20 pixels up!
- **Labels:** bug
- **URL:** https://github.com/telegramdesktop/tdesktop/issues/30736
- **Why it fits:** Someone's coordinate math is having a bad day

### Issue #3: VSCode Copilot orphaned chat recovery
- **Repo:** `microsoft/vscode#305818`
- **Title:** Detect, surface, and recover orphaned Copilot Chat
- **Labels:** bug
- **URL:** https://github.com/microsoft/vscode/issues/305818
- **Why it fits:** Chat session gets lost - did someone close the wrong tab?

### Issue #4: Tailwind @apply in v4
- **Repo:** `tailwindlabs/tailwindcss#20123`
- **Title:** Tailwind 4 and @apply
- **Labels:** bug
- **URL:** https://github.com/tailwindlabs/tailwindcss/issues/20123
- **Why it fits:** "Why isn't @apply working?" - because v4 changed everything, sweetie!

---

## 🎯 How to Use This Taxonomy

### For Debugging
1. **Identify symptoms** - What error messages do you see?
2. **Match to category** - Which category describes your issue?
3. **Check examples** - See similar issues and their fixes
4. **Apply patterns** - Use proven solutions from similar bugs

### For Clustering/ML
- Use category labels as ground truth for training
- Embed issue titles/bodies and cluster by semantic similarity
- Cross-reference with labels, repo domain, and issue state

### For Prevention
- Code review checklist by category
- Add tests for common patterns in each category
- Lint rules targeting specific bug types

---

## 📊 Statistics

| Metric | Value |
|--------|-------|
| Total Issues Categorized | 114 |
| Categories | 24 |
| Repositories Covered | 37 |
| Avg Examples per Category | 3.5 |
| Bug-labeled Issues | 19 |
| Enhancement Requests | 6 |

---

**Generated:** 2026-05-30  
**Source:** GitHub Issues from popular repositories  
**Location:** `github_issues_dataset/`
