# 14 — Mental Models

> **Core Question:** *What's the right way to think about this Rust concept?*

## Key Mental Models

| Concept | Mental Model | Analogy |
|---------|--------------|---------|
| **Ownership** | Unique key | Only one person has the house key at a time |
| **Move** | Key handover | You give away your key — you can't enter anymore |
| **`&T` (immutable borrow)** | Lending for reading | You lend a book — others can read it too |
| **`&mut T` (mutable borrow)** | Exclusive editing | Only you can edit the document right now |
| **Lifetime `'a`** | Valid scope / ticket | "This ticket is valid until December 31st" |
| **`Box<T>`** | Heap pointer | Remote control to a TV (the TV is on the heap) |
| **`Rc<T>`** | Shared remote | Multiple remotes for one TV; last to leave turns it off |
| **`Arc<T>`** | Room-to-room remote | Remotes work from any room (thread-safe) |
| **`RefCell<T>`** | Runtime borrowing | Borrow checker lets you through, but bouncer checks at runtime |
| **`Mutex<T>`** | Keyed lockbox | Only one person can open the box at a time |

## Coming From Other Languages

| From | Key Shift |
|------|-----------|
| **Java / C#** | Values are *owned*, not references by default. No GC. No null — use `Option`. |
| **C / C++** | Compiler enforces safety rules. No manual `free()`. No dangling pointers. |
| **Python / JS** | No GC, deterministic destruction. Variables own their data. |
| **Go** | No goroutine-shared mutable state without `Mutex`. Ownership prevents data races. |
| **Functional (Haskell, etc.)** | Mutability is *safe* via ownership tracking. Shared mutation is controlled. |

## Ownership Visualization

```
Stack                          Heap
+----------------+            +----------------+
| main()         |            |                |
|   s1 ─────────────────────> │ "hello"        |
|                |            |                |
| fn takes(s) {  |            |                |
|   s2 (moved) ─────────────> │ "hello"        |
| }              |            | (s1 invalid)   |
+----------------+            +----------------+

After move: s1 is no longer valid — trying to use s1 is E0382.
```

## Reference Visualization

```
+----------------+
| data: String   |────────────> "hello" on heap
+----------------+
       ↑
       │ &data (immutable borrow)
       │
+------+------+
| reader1    reader2    (multiple OK — all read-only)
+------+------+

+----------------+
| data: String   |────────────> "hello"
+----------------+
       ↑
       │ &mut data (exclusive mutable borrow)
       │
+------+
| writer (only ONE — exclusive access)
+------+
```

## Common Misconceptions

| Error | Wrong Mental Model | Correct Mental Model |
|-------|-------------------|----------------------|
| E0382: use after move | "GC will clean up the old reference" | "Ownership key was transferred — you no longer have it" |
| E0502: borrow conflict | "Multiple writers should be fine" | "Only one active writer at a time prevents data races" |
| E0499: multiple mut borrows | "I can alias mutable references" | "Exclusive access is required for mutation" |
| E0106: missing lifetime | "Lifetimes are optional" | "All references have a validity scope — sometimes you must name it" |
| E0507: move from `&T` | "I can take ownership from a reference" | "References don't own data — you can't take what you don't have" |
| E0515: return local ref | "The reference will still be valid" | "Local data is destroyed when the function returns" |

## Deprecated Thinking

| Deprecated | Better |
|------------|--------|
| "Rust is like C++" | Different ownership model — Rust's compiler enforces what C++ leaves to convention |
| "Lifetimes are like GC" | Compile-time validity scopes — zero runtime cost |
| "Clone solves everything" | Restructure ownership — cloning hides design issues |
| "Fight the borrow checker" | Work with the compiler — it's preventing bugs |
| "`unsafe` to avoid rules" | Understand safe patterns first — 99% of Rust can be safe |
| "`Box` is like `new` in C++" | `Box` is just heap allocation — ownership semantics are different |

## Learning Path

| Stage | Focus | References |
|-------|-------|------------|
| 🐣 **Beginner** | Ownership, borrowing, basic types | [01](01-ownership.md), this module |
| 🚶 **Intermediate** | Smart pointers, error handling, traits, testing | [02](02-resource-mgmt.md), [04](04-zero-cost.md), [06](06-error-handling.md), [08](08-testing.md) |
| 🏃 **Advanced** | Concurrency, async, performance, type-driven design | [05](05-type-driven.md), [07](07-concurrency.md), [09](09-performance.md) |
| 🧙 **Expert** | Domain modeling, lifecycle, anti-patterns, ecosystem | [10](10-ecosystem.md), [11](11-anti-patterns.md), [12](12-domain-modeling.md), [13](13-lifecycle.md) |

## Related References

- **Down:** [01-ownership](01-ownership.md) for ownership patterns, [02-resource-mgmt](02-resource-mgmt.md) for smart pointers
- **Side:** [11-anti-patterns](11-anti-patterns.md) for common mistakes rooted in wrong mental models
