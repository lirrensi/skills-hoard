# Quality: Architecture And Maintainability

> Structural smells, coupling, API and concurrency design issues, and maintainability debt.
>
> Load this when reviewing how the system is shaped, not just whether a single function works.

---

## 🌐 API Design

- [ ] 🟡 Version from day one — `/v1/resource` not `/resource`
- [ ] 🔴 Correct HTTP methods and status codes — 200/201/400/401/403/404/500 matter
- [ ] 🔴 Sensitive data never in GET params or URLs — use body or headers
- [ ] 🔴 Paginate all list endpoints — no unbounded queries, always limit
- [ ] 🔴 Rate limit every endpoint — sliding window, stricter on auth/expensive ops
- [ ] 🔴 Idempotency keys on mutations — retries must not cause double-charges
- [ ] 🟡 Consistent response structure — `{ success, data?, error?, meta? }` everywhere

---

## ⚡ Concurrency

- [ ] 🔴 No TOCTOU bugs — check-and-act must be atomic
- [ ] 🔴 Locks for shared mutable state — concurrent writes without sync = corruption
- [ ] 🔴 Never fire-and-forget async — always handle or await; silent failures are bugs
- [ ] 🔴 Missing await is deadly — async calls without await produce the funniest bugs
```
# BAD: sendEmail(user)         # forgot await, error vanishes
# GOOD: await sendEmail(user)  # error propagates
```

- [ ] 🔴 Timeouts on all external calls — no request hangs forever
- [ ] 🔴 Unhandled promise rejections — orphaned promises that crash the process or vanish silently
- [ ] 🔴 Sequential awaits that should be parallel — `await a(); await b()` when independent is wasteful
```
# BAD: 2 seconds total
const users = await fetchUsers();     # 1s
const orders = await fetchOrders();   # 1s

# GOOD: 1 second total
const [users, orders] = await Promise.all([
    fetchUsers(),
    fetchOrders()
]);
```

- [ ] 🟡 `async void` functions — no way to catch errors from them; always return the promise

---

## 🏗️ Architecture

- [ ] 🔴 Separate concerns — data layer ≠ business logic ≠ presentation
- [ ] 🔴 No circular dependencies — if A needs B and B needs A, refactor
- [ ] 🟡 Interface over implementation — depend on abstractions, not concrete classes
- [ ] 🔴 Config via environment — no hardcoded values that change between deployments
- [ ] 🟡 Feature flags for risky changes — deploy dark, enable gradually
- [ ] 🟡 Stateless services when possible — scale horizontally without sticky sessions
- [ ] 🟡 No service locator pattern — hidden dependencies retrieved at runtime; prefer explicit injection

---

## ⚡ Performance & Scalability

- [ ] 🔴 N+1 query detection — never fetch users then loop to fetch their orders one-by-one
```
# BAD: users.forEach(u => fetchOrders(u.id))    # 1 + N queries
# GOOD: fetchUsersWithOrders()                  # 1 query with join
```

- [ ] 🔴 Index your foreign keys and query columns — unindexed joins on big tables destroy you
- [ ] 🟡 Cache invalidation strategy defined — not just "we cache it," but when does it expire/bust?
- [ ] 🔴 No synchronous heavy ops on request thread — offload image processing, emails, reports to queues
- [ ] 🔴 String concatenation in loops is evil — `result += str` creates a new object every iteration
```
# BAD: result = ""; items.forEach(i => result += i)
# GOOD: result = items.join("")
```

- [ ] 🟡 Regex compiled inside a loop — compiling the same pattern 10,000 times is embarrassingly bad
- [ ] 🔴 Unbounded in-memory collection building — loading 500k rows to filter 3 of them

---

## 🧹 Dead Code & Cruft

- [ ] 🟡 Unreachable code after returns/throws — compilers may not warn, humans definitely won't read it
```
# BAD
function process() {
    return result;
    logger.info("done");  # never executes, just confuses
}
```

- [ ] 🟡 Unused variables, imports, and parameters — every one is a lie about what the code needs
- [ ] 🟡 Commented-out code blocks — that's what git history is for; delete it or restore it
- [ ] 🟡 Unused feature flags / dead branches — if the flag has been `true` for 6 months, remove the `if`
- [ ] 🟡 Orphaned functions/methods — no callers anywhere = dead weight; search before assuming it's needed
- [ ] 🟢 Vestigial interfaces / abstract classes with one implementation and no plans for more — abstraction without purpose
- [ ] 🟡 Zombie dependencies in your manifest — packages imported but never used, still downloading and scanning

---

## 🔁 Duplication & Copy-Paste

- [ ] 🟡 Near-identical functions differing by one line — extract the common part, parameterize the difference
- [ ] 🔴 Same validation logic in multiple places — one change, three places to forget
- [ ] 🟡 Repeated error-handling boilerplate — wrap in a middleware/decorator/higher-order function
- [ ] 🔴 Copy-pasted SQL/queries across files — one schema change, N bugs
- [ ] 🟡 Duplicated constants / config values — `TIMEOUT = 30` defined in 4 files, now they disagree

---

## 🧠 Complexity Smells

- [ ] 🟡 Nested ternaries — one ternary is fine; nested ternaries are a war crime. Prefer switch statements or if/else chains for multiple conditions.
```
# BAD
const label = a ? (b ? "X" : "Y") : (c ? "Z" : "W");

# GOOD
if (a && b) return "X";
if (a) return "Y";
if (c) return "Z";
return "W";
```

- [ ] 🟡 `switch` / `if-else` chains longer than 5 branches — use a lookup map/dictionary
```
# BAD
if (type === "A") return handleA();
else if (type === "B") return handleB();
// ... 12 more

# GOOD
const handlers = { A: handleA, B: handleB, ... };
return handlers[type]();
```

- [ ] 🟡 Deeply nested callbacks — flatten with async/await or extract named functions
- [ ] 🟡 Overly clever one-liners — if it needs a comment to explain, it's not clever, it's hostile. Prioritize readability over brevity. `arr.filter(x => x.active).map(x => x.id)[0]` is fine. `arr.reduce((a, b) => a || b.id, null)` is showing off.
- [ ] 🔴 Multiple return types from one function — returns `string | null | number | false` is a type nightmare
```
# BAD: returns User | null | false | undefined depending on mood
# GOOD: returns User | null — that's it
```

- [ ] 🔴 Functions that return *and* throw *and* mutate — pick ONE communication channel
- [ ] 🔴 Long parameter lists with same-type args — `createUser("John", "Smith", "John", "Active")` which "John" is what?
```
# BAD: createUser("John", "Smith", "john@x.com", "admin", true, true)
# GOOD: createUser({ firstName: "John", lastName: "Smith", ... })
```

- [ ] 🔴 Overuse of `any` / `Object` / `dynamic` — you opted into a type system then turned it off
- [ ] 🟡 Negated conditionals as the primary branch — put the positive/common path first
```
# BAD
if (!user.isDisabled) { ... long block ... }
else { return; }

# GOOD
if (user.isDisabled) return;
// ... long block ...
```

- [ ] 🟡 Cyclomatic complexity cap — if a function has too many branches, extract helpers (e.g., complexity <= 10)
- [ ] 🟡 File/class size > 300 lines — it's doing too much. Split by feature, not by type

---

## 🔢 Primitive Obsession

- [ ] 🔴 Strings doing the job of enums — `status = "actve"` (typo) compiles fine, an enum wouldn't
- [ ] 🟡 Parallel arrays instead of object arrays — `names[i]` + `ages[i]` + `emails[i]` is fragile; use `users[i].name`
- [ ] 🟡 Stringly-typed everything — passing `"USD"`, `"EUR"` as raw strings instead of a `Currency` type
- [ ] 🟡 Raw tuples for structured data — `[200, "OK", user]` — what's index 2 again? Use an object
- [ ] 🟡 Booleans that should be enums — `isActive, isVerified, isPending` → just use a `Status` enum
- [ ] 🟡 Encoding meaning in string formats — `"user:admin:readonly"` parsed with `.split(":")` — make a real data structure
- [ ] 🟢 Units in names — `timeout` → `timeoutMs`, `retry` → `retryCount`, `size` → `sizeBytes`

---

## 🏋️ Class & Module Smells

- [ ] 🟢 Data classes with no behavior — if it's just getters/setters, it's a struct pretending to be a class
- [ ] 🟡 Feature envy — method uses 10 fields from another class and 0 from its own; it belongs over there
- [ ] 🔴 Shotgun surgery — one change requires touching 15 files; your abstractions are wrong
- [ ] 🟡 Divergent change — one class changes for 5 unrelated reasons; it's doing 5 jobs
- [ ] 🟢 Middle-man classes that just delegate — `this.service.doThing()` adds zero value; call service directly
- [ ] 🟢 Lazy classes that do almost nothing — justify every class's existence; merge or delete
- [ ] 🟡 Inappropriate intimacy — classes accessing each other's private/internal details; respect boundaries
- [ ] 🟡 Excessive method chaining where intermediate state is unclear — `obj.load().parse().validate().transform().save()` — where did the error happen?
- [ ] 🟡 Static method abuse — untestable, unhookable, essentially global functions wearing a class costume
- [ ] 🟡 Constructor doing real work — constructors that call APIs, read files, or do heavy computation; use factory methods

---

## 📐 Literals, Defaults & Config

- [ ] 🟡 Hardcoded timeouts/limits buried in logic — `setTimeout(fn, 86400000)` — what is that number?
```
# BAD: setTimeout(fn, 86400000)
# GOOD:
const ONE_DAY_MS = 24 * 60 * 60 * 1000;
setTimeout(fn, ONE_DAY_MS);
```

- [ ] 🟡 Format strings / templates duplicated — date formats, URL patterns, error templates defined inline everywhere
- [ ] 🟡 Implicit defaults that differ across call sites — one place defaults `pageSize` to 10, another to 50
- [ ] 🟡 Environment-specific logic via `if (env === "prod")` scattered everywhere — use config objects
- [ ] 🟡 Logging format/level inconsistency — `console.log`, `logger.warn`, `print()` mixed in the same codebase

---

## 🪵 Logging & Debug Leftovers

- [ ] 🔴 `console.log` / `print` / `System.out` left in production code — use proper logger with levels
- [ ] 🔴 Debug-only code behind no flag — `if (true) { dumpState() }` committed accidentally
- [ ] 🔴 Logging inside tight loops — 1M log lines per second is not observability, it's a DDoS on your log infra
- [ ] 🔴 Log messages with no context — `logger.error("Failed")` — failed WHAT? For WHICH user/request?
- [ ] 🟡 Inconsistent log levels — `logger.error("User logged in")` — that's info, not an error
- [ ] 🔴 Log injection — user input in logs (`log('User ' + name)`) lets attackers forge log entries via `\n`
- [ ] 🟡 Don't log-and-throw blindly — either add context or let it bubble; double-logging destroys signal

---

## 👃 Code Smell Classics

- [ ] 🟡 Law of Demeter violations (train wrecks) — `user.getProfile().getAddress().getZipCode()` violates encapsulation
- [ ] 🟡 Data clumps — same 3-4 arguments passed together in multiple functions → make them an object
- [ ] 🔴 Variable shadowing — reusing a variable name in a nested scope confuses humans and compilers
```
# BAD
let user = getUser();
if (active) {
  let user = getAdmin();  # WTF is 'user' now?
}
```

- [ ] 🟢 Scope minimization — declare variables as close to their usage as possible, not at the top
- [ ] 🔪 YAGNI violations — delete "just in case" code. If it's not called now, it's a bug waiting to happen. **The Rule:** "If I delete this, will anything break?" Yes → keep it. No → DELETE IMMEDIATELY. "Maybe in the future?" → DELETE. Git remembers.
- [ ] 🟡 Re-assigning function arguments — treat inputs as `const`. Create a new variable if you need to change it
- [ ] 🟢 Boolean blindness — `setFlag(true)` is meaningless. `enableFeature()` or `disableValidation()` is self-documenting
- [ ] 🟡 Comments are deodorant — if the code stinks, rewrite it. Don't explain the smell away. **If you write a comment, you failed to make the code clear.** Rename the variable. Extract the function. Kill the comment.

---

## 📦 Contract & Boundary Smells

- [ ] 🔴 Validate at boundaries once — don't re-validate the same input 5 layers deep
- [ ] 🔴 No hidden I/O in "utility" functions — helpers shouldn't secretly read env, disk, network, globals
- [ ] 🟡 No time-dependent logic without injection — wrap `now()`/clock so code is testable and deterministic
- [ ] 🟡 Don't mix sync and async styles — e.g., callbacks + promises together; pick one per module
- [ ] 🟡 DTOs vs Entities — never return DB entities directly. Map to a DTO to hide internal schema changes
- [ ] 🟡 Custom error types over generic Error — `throw new NotFoundError()` > `throw new Error("404")`

---

## 🔢 Advanced Primitive Smells

- [ ] 🔴 Bitwise flags for booleans — `if (permissions & 4)` is unreadable. Use `hasPermission('WRITE')`
- [ ] 🟡 Stringly typed IDs — passing `"user_123"` everywhere. Wrap it: `new UserId("123")`
- [ ] 🟡 Switch statements on type — if you switch on `class.type`, use polymorphism. The class should have a `handle()` method
- [ ] 🟢 Loop-switch sequence — a loop containing a large switch often means you're iterating over a mixed collection that should be normalized first

---

## ⚡ Additional Async Smells

- [ ] 🔴 `Promise.all` fail-fast ignorance — if one promise rejects, others are silently cancelled. Is that what you want?
- [ ] 🟡 `.then()` pyramid of doom — if you have 3+ `.then()`, use `async/await`
```
# BAD
getUser().then(u => getOrders(u).then(o => getItems(o)))

# GOOD
const u = await getUser();
const o = await getOrders(u);
const i = await getItems(o);
```

- [ ] 🟢 Mixed async styles in same file — don't mix callbacks, `.then()`, and `async/await`. Pick one per module

---

## 🏗️ OOP Structural Smells

- [ ] 🟡 Anemic domain model — classes with only getters/setters and no logic are just expensive Maps. Move behavior into the class
- [ ] 🟡 Inheritance for code reuse — "I need a `User` class, I'll inherit from `DatabaseRecord`." **No.** Use composition. Inheritance is for polymorphism
- [ ] 🟢 Public fields everywhere — if every field is public, you have a struct, not a class. Hide the data

---

## 🔪 Over-Engineering & Bloat

*Focus: Ruthless deletion. If it's not pulling its weight, kill it.*

- [ ] 🔪 **Unnecessary abstraction layers** — Controller → Service → Manager → Repository → DAO where each just delegates to the next. If a layer adds no decisions, collapse it.
```
# BAD: 5 files to save a user
UserController → UserService → UserManager → UserRepository → UserDAO

# GOOD: 2-3 files
UserController → UserService → UserRepository
```

- [ ] 🔪 **Premature abstraction (Rule of Three)** — Interfaces/base classes created with only ONE implementation. Wait until you have 2+ real cases that need them. Abstractions must earn their complexity.
- [ ] 🔪 **Forced DRY — coupling unrelated code** — Two functions that share 80% code but serve different domains. Merging them creates a fragile frankenstein that breaks when either domain changes independently. Duplication is cheaper than wrong abstraction.
```
# BAD: Forced together because they "look the same"
function processEntity(entity, type) {
    if (type === "user") { /* 20 user-specific lines */ }
    if (type === "order") { /* 20 order-specific lines */ }
    // 10 shared lines
}

# GOOD: Duplication is cheaper than coupling
function processUser(user) { ... }
function processOrder(order) { ... }
```

- [ ] 🔪 **Over-fragmented code (Ravioli)** — 50-line feature spread across 12 files with 3-line functions. Locality of behavior matters. If understanding a flow requires opening 8 tabs, you over-split.
- [ ] 🟢 **Nano-functions that obscure flow** — Extracting every 2 lines into a named function when inline is clearer. The reader now has to jump around to follow logic.
```
# BAD: Extraction that hurts readability
function processOrder(order) {
    validateExists(order);
    checkStatus(order);
    applyDiscount(order);
    updateTotal(order);
    saveOrder(order);
}
// ...where each function is 1-2 lines and only called here

# GOOD: Inline when it's clearer
function processOrder(order) {
    if (!order) throw new NotFoundError();
    if (order.status !== 'pending') throw new InvalidStateError();
    order.total = order.subtotal * (1 - order.discountRate);
    await db.orders.save(order);
}
```

- [ ] 🟢 **Comment-delimited sections in functions** — Block comments like `// --- Validate ---` separating "phases" are extract-method signals. The comment should become the function name.
```
# BAD
function processOrder(order) {
    // --- Validate order ---
    if (!order.items.length) throw ...
    // --- Calculate totals ---
    let subtotal = 0;
    // --- Apply discounts ---
    if (order.coupon) { ... }
    // --- Save to database ---
    await db.save(order);
}

# GOOD: The comments became function names
function processOrder(order) {
    validateOrder(order);
    const total = calculateTotal(order.items, order.coupon);
    await saveOrder({ ...order, total });
}
```

- [ ] 🔪 **Over-configurable code** — 12 options/params where only 2 are ever used. Every option doubles the testing surface. Hard-code until you genuinely need flexibility.
```
# BAD: 12 options, 3 ever used
createServer({
    port: 3000,
    host: 'localhost',
    protocol: 'http',
    encoding: 'utf-8',
    maxHeaderSize: 8192,
    keepAliveTimeout: 5000,
    // ... 6 more that are always defaults
})

# GOOD: Sensible defaults, expose only what varies
createServer({ port: 3000 })
```

- [ ] 🟢 **Unnecessary async wrappers** — Synchronous logic wrapped in `async`/`Promise` for no reason. Adds stack trace noise and cognitive overhead.
```
# BAD
async function getFullName(user) {
    return `${user.first} ${user.last}`;  // nothing async here
}

# GOOD
function getFullName(user) {
    return `${user.first} ${user.last}`;
}
```

- [ ] 🔪 **Polymorphism for ≤2 cases** — Interface + 2 implementations + factory + registry... for "free" vs "premium." An if/else is 3 lines. Patterns are solutions to recurring problems. No problem = no pattern needed.
- [ ] 🟢 **Storing easily derived values** — Caching computed state (`itemCount`, `totalPrice`, `isEmpty`) that then requires manual synchronization instead of computing on access via getters.
```
# BAD
class Cart {
    items = [];
    itemCount = 0;      // redundant — items.length
    totalPrice = 0;     // redundant — sum of items
    isEmpty = true;     // redundant — items.length === 0
}

# GOOD
class Cart {
    items = [];
    get itemCount() { return this.items.length; }
    get totalPrice() { return this.items.reduce((s, i) => s + i.price, 0); }
    get isEmpty() { return this.items.length === 0; }
}
```

- [ ] 🔪 **Helper/Utility class sprawl** — `StringUtils`, `DateHelper`, `MathEx` with static methods. If it's a pure function, put it in the module that uses it. Don't create grab-bag classes.
- [ ] 🔪 **Unnecessary design patterns** — Observer with 1 subscriber, Strategy with 1 strategy, Factory that returns the same class. The pattern IS the complexity if you don't have the problem.
- [ ] 🔪 **Config hell** — `if (config.features.isNewThingEnabled)` scattered through business logic. Pass a context object or use strategy pattern. Don't hunt for flags in the logic.
- [ ] 🔪 **Ceremony layers** — Request → Controller → Service → Manager → Provider → Helper where each just passes data along. Each layer should justify itself with a decision or transformation.
- [ ] 🔪 **Over-generalized solutions** — A function handling 15 cases via config/switches when you only ever use 2. The config complexity exceeds the problem complexity.

---

## 🧠 Cognitive Load & Hidden Coupling

*Focus: "Don't make me think." Hidden dependencies and cognitive overhead.*

- [ ] 🟡 **Hidden coupling — temporal APIs** — `init()` must be called before `run()`. The API should enforce this (constructor, state machine) or do it internally. Don't make callers guess.
- [ ] 🟡 **Destructuring abuse** — Deeply nested object destructuring in function signatures saves lines but destroys readability and makes null-reference bugs harder to spot.
```
# BAD
function printCity({ user: { profile: { address: { city } } } }) { ... }

# GOOD
function printCity(data) {
    const city = data?.user?.profile?.address?.city;
}
```

- [ ] 🟡 **Deeply nested object access (Law of Demeter)** — `user.profile.address.city` violates encapsulation. Ask for what you need, don't navigate the object graph. Pass `city` directly. (See also: Law of Demeter violations)
- [ ] 🟢 **Over-defensive checks** — Re-validating what the type system or upstream validation already guarantees. Redundant guards add noise and suggest code is less safe than it is. (See also: validate at boundaries once)
- [ ] 🟡 **Unnecessary generic type parameters** — `class Repository<T extends BaseEntity<T>>` when you only ever use `Repository<User>`. Add generics at the second use case, not the first.
- [ ] 🟢 **Type gymnastics** — If the type definition is harder to read than the code it types, simplify. Types should clarify, not obscure.
- [ ] 🔪 **"WTF/min" density** — Clever one-liners, heavy chaining, missing intermediate variables. `arr.reduce((a, b) => a || b.id, null)` is showing off, not engineering. (See also: overly clever one-liners; explaining variables over complex booleans)
- [ ] 🟢 **Preserve helpful intermediate variables** — Don't inline everything. A well-named `const` for a complex boolean is self-documenting code. (Pairs with: explaining variables over complex booleans)

---
