# Quality: Core

> Correctness and readability traps that show up in almost every codebase.
>
> Report findings by issue name + location. Do not use checklist numbers.

---

## 🧩 Functions & Logic

- [ ] 🔴 Functions do ONE thing — if you can't name it with a single verb-noun, split it
- [ ] 🟡 Max 20 lines per function — longer means too many responsibilities
- [ ] 🟡 Max 3 arguments — pass objects/configs if you need more
- [ ] 🟡 One level of abstraction per function — no mixing business logic with SQL/API calls
- [ ] 🔴 No side effects on inputs — return new values, never mutate arguments
- [ ] 🟡 Guard clauses over deep nesting — return early, flatten the pyramid
- [ ] 🟢 Avoid boolean arguments — `render(item, true)` tells nothing; use named options
- [ ] 🟡 Prefer composition over inheritance — small composable functions beat deep class trees
- [ ] 🟢 No output arguments — don't pass a variable just to mutate it; return the result
- [ ] 🟡 No god objects/functions — if it knows about everything, it shouldn't exist

---

## 📝 Naming & Readability

- [ ] 🟢 Booleans read as questions — `isActive`, `hasPermission`, `canEdit`
- [ ] 🟢 No abbreviations — `user` not `usr`, `request` not `req`
- [ ] 🟢 Functions are verbs, data is nouns — `calculateTotal()` not `total()`
- [ ] 🟢 Collections are plural — `users`, `orderItems`, not `userList`
- [ ] 🟡 Named constants, never magic numbers — `MAX_RETRIES = 3` not `if retries > 3`
- [ ] 🟢 Self-documenting code > comments — rename if you need a comment to explain WHAT
- [ ] 🟢 Variable names must be searchable — `d`, `x`, `tmp` are ungoogleable; use `daysSinceLastLogin`

---

## 🔄 Data & State

- [ ] 🔴 Immutability by default — spread/clone for updates, never mutate in place
- [ ] 🔴 Single source of truth — derive computed values, don't duplicate state
- [ ] 🟡 Explicit state transitions — no implicit status changes; state machines for complex flows
- [ ] 🔴 Initialize before use — no "maybe undefined" variables that crash later
- [ ] 🔴 Avoid global mutable state — pass what you need, inject dependencies
- [ ] 🔴 Transactions for multi-step mutations — partial writes = data corruption

---

## ⚠️ Error Handling

- [ ] 🔴 Never swallow errors silently — empty `catch` blocks are crime scenes
- [ ] 🟡 Catch specific exceptions — broad `catch Exception` hides unrelated bugs
- [ ] 🔴 Preserve stack traces when re-throwing — don't murder the evidence
```
# BAD: catch (e) { throw e }           # stack trace nuked
# GOOD: catch (e) { throw }            # stack trace preserved
```

- [ ] 🟡 Error messages explain what AND what to do — not just "Invalid input"
- [ ] 🔴 Never expose internals to clients — no stack traces, query strings, file paths
- [ ] 🟡 Distinguish recoverable vs fatal — retry the first, alert on the second

---

## 🎭 Sneaky Bad Practices

- [ ] 🟢 `else` after a `return` — it's just noise and signals the dev wasn't thinking
```
# BAD
if (valid) {
    return process()
} else {
    return error()
}

# GOOD
if (valid) return process()
return error()
```

- [ ] 🔴 Comparing floats with `==` — `0.1 + 0.2 == 0.3` is FALSE, always use epsilon
```
# BAD: if (a == b)
# GOOD: if (abs(a - b) < EPSILON)
```

- [ ] 🟡 Swallowing null by defaulting silently — `user.name ?? "Unknown"` sounds nice until "Unknown" ends up in production
- [ ] 🔴 Date math without timezone awareness — `new Date()` has ruined more careers than job interviews
- [ ] 🔴 Mutable default arguments — `def func(data=[])` is an infamous trap; the list persists across calls
```
# BAD: def add(item, items=[])  # same list object every call
# GOOD: def add(item, items=None):
           items = items or []
```

- [ ] 🟡 No "fix it later" comments — TODOs with no ticket are lies you tell yourself
- [ ] 🟡 Don't catch exceptions you can't handle — logging and re-raising is just noise
- [ ] 🟢 Avoid double negatives — `if (!notValid)` makes everyone's brain hurt
- [ ] 🟢 Negative named booleans — `isNotEnabled`, `disableSsl`; double negatives destroy brain cells. Name positively: `isEnabled`, `useSsl`

---

## 🛡️ Defensive Coding Gaps

- [ ] 🔴 No null/undefined check before property access — `user.address.city` when address can be null
```
# BAD: user.address.city          # TypeError if address is null
# GOOD: user.address?.city ?? ""  # safe navigation
```

- [ ] 🔴 Assumes array is non-empty — `items[0].id` without checking length first
- [ ] 🔴 parseInt / type coercion without radix or validation — `parseInt("08")` has bitten people for decades
```
# BAD: parseInt(input)
# GOOD: parseInt(input, 10)   # or Number(input) with validation
```

- [ ] 🔴 Division without zero check — `total / count` when count could be 0
- [ ] 🔴 `.map()` / `.filter()` on possibly-null collections — `data.items.map(...)` when `items` may not exist
- [ ] 🔴 Enum/union not exhaustively handled — new status added, 4 switch statements silently skip it
```
# In TypeScript:
function handle(s: Status): string {
    switch (s) {
        case "active": return "...";
        case "inactive": return "...";
        default: const _exhaustive: never = s;  # compile error if case missed
    }
}
```

- [ ] 🔴 Regex without anchoring — `/admin/` matches `"not-admin-really"`, use `/^admin$/`
- [ ] 🔴 Object spread overwrites in wrong order — `{ ...defaults, ...input }` vs `{ ...input, ...defaults }` is a silent bug
- [ ] 🔴 Accidental reference mutation — `const items = state.items; items.push(x)` mutates state! Spread it: `[...items, x]`

---

## 🔧 Resource & Cleanup

- [ ] 🔴 Opened resources without guaranteed close — DB connections, file handles, streams need `finally` / `using` / `with`
```
# BAD
const conn = await db.connect();
const result = await conn.query(sql);  # if this throws, conn leaks
conn.release();

# GOOD
const conn = await db.connect();
try {
    return await conn.query(sql);
} finally {
    conn.release();
}
```

- [ ] 🔴 Event listeners never removed — memory leak that grows quietly until OOM
- [ ] 🔴 Timers/intervals never cleared — `setInterval` without corresponding `clearInterval` on teardown
- [ ] 🟡 Temp files / artifacts never cleaned up — disk fills up slowly, then suddenly
- [ ] 🟡 Connection pools never configured — defaults are almost never right for your load

---

## 🔀 Control Flow Smells

- [ ] 🟡 Using exceptions for control flow — `try { parse(x) } catch { handleNotParseable() }` — check first, don't throw for expected cases
- [ ] 🟢 `for` loop that always runs exactly once — it's not a loop, it's a confusing `if`
- [ ] 🟢 Loop with `break` on first iteration — you wanted `.find()`, not `.forEach()`
- [ ] 🟢 Re-checking a condition inside a loop that was the loop's condition — redundant and confusing
- [ ] 🟡 Flag variables controlling flow — `let found = false; for (...) { if (...) found = true; }` — use early return or `.some()`
- [ ] 🟡 Multiple loops over the same collection for related tasks — combine into one pass
- [ ] 🔴 Recursion without base-case guarantees — stack overflow is not a theoretical concern
- [ ] 🟡 Temporal coupling — don't require callers to remember "call A before B" without enforcing it

---

## 📝 Encoding & Serialization

- [ ] 🔴 Implicit encoding assumptions — always specify UTF-8 explicitly for file/network I/O
```
# BAD: data = file.read()              # what encoding?
# GOOD: data = file.read(encoding="utf-8")
```

- [ ] 🔴 JSON serialization of dates/decimals — `JSON.stringify(new Date())` gives different results across runtimes
- [ ] 🟡 Binary vs text mode confusion — reading a binary file as text silently corrupts data
- [ ] 🟡 Locale-dependent formatting in logic — `toString()` on numbers gives `"1,000"` in Germany, breaking parsers

---

## 🗂️ Collection & Iteration Traps

- [ ] 🔴 Mutating a collection while iterating — `ConcurrentModificationException` in every language
```
# BAD
for item in items:
    if item.expired:
        items.remove(item)    # skips elements or crashes

# GOOD
items = [i for i in items if not i.expired]
```

- [ ] 🔴 Off-by-one errors in manual indexing — use iterators/range-based loops; manual `i < len` is a trap
- [ ] 🟡 HashMap/dict key mutation — mutating an object used as a key makes it unfindable
- [ ] 🟡 Sorting with inconsistent comparators — `compare(a,b)` must be transitive or sort is undefined behavior
- [ ] 🟡 Relying on iteration order of unordered collections — dict/set order is implementation-defined in many languages

---

## ⚖️ Equality & Comparison Gotchas

- [ ] 🔴 Identity vs equality confusion — `==` vs `===` vs `.equals()` — know which your language uses by default
- [ ] 🔴 Broken custom equality — if you override `equals`, override `hashCode`; collections break otherwise
- [ ] 🟡 Null comparison traps — `null == undefined` is `true` in JS; `None == 0` behavior varies by language
- [ ] 🟡 String comparison for non-ASCII — `"café" == "café"` can be `false` due to Unicode normalization (NFC vs NFD)

---

## 🧠 Memory & Lifecycle Smells

- [ ] 🔴 Closure capturing more than intended — lambdas holding references to entire scopes, preventing GC
```
# BAD
function setup() {
    const hugeData = loadGigabytes();
    return () => console.log(hugeData.length);
    # entire hugeData kept alive just for .length
}

# GOOD
function setup() {
    const len = loadGigabytes().length;
    return () => console.log(len);
}
```

- [ ] 🟡 Unbounded caches without eviction — `cache[key] = value` growing forever is a slow memory leak
- [ ] 🟡 Retaining references in error objects — stack traces capturing large local variables in some runtimes
- [ ] 🟡 Circular references preventing cleanup — two objects referencing each other in non-GC or weak-ref contexts

---

## 🔢 Type Coercion & Conversion

- [ ] 🔴 Silent type coercion in comparisons — `"5" > "10"` is `true` (string comparison); convert first
- [ ] 🔴 Lossy numeric conversions — `int(3.9)` gives `3`, not `4`; be explicit about truncation vs rounding
- [ ] 🟡 Integer overflow/underflow — unbounded arithmetic wrapping silently in fixed-width integer languages
- [ ] 🟡 Truthy/falsy misuse — `if (count)` fails when `count = 0` is a valid value, not an absence

---

## 🧠 Cognitive Load Smells

- [ ] 🟡 Explaining variables over complex booleans — Don't make readers parse logic in their head
```
# BAD
if (auth.user && auth.user.role === 'admin' && (order.status === 'paid' || order.status === 'shipped')) { ... }

# GOOD
const isAdmin = auth.user?.role === 'admin';
const isOrderActive = ['paid', 'shipped'].includes(order.status);
if (isAdmin && isOrderActive) { ... }
```

- [ ] 🟡 Tramp data (drilling) — passing a variable through 4 layers just because the 5th layer needs it
- [ ] 🔴 Getters with side effects — `user.isActive` should return a boolean, not trigger a DB call or mutate state
- [ ] 🟢 Yoda conditions — `if (5 === count)` was for C compilers. Modern linters save you. Just write `if (count === 5)`
- [ ] 🔴 Assignments inside conditions — `if (user = getUser())` looks like a typo and is hard to read
- [ ] 🟡 Speculative generality — "I'll add this extra parameter just in case" — delete it; it confuses code now for a future that may never happen

---
