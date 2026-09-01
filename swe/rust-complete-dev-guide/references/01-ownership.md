# 01 — Ownership & Borrowing

> **Core Question:** *Who should own this data, and for how long?*

## The Ownership Rules

```
1. Each value has exactly ONE owner.
2. When the owner goes out of scope, the value is dropped.
3. You can borrow a value (immutably or mutably) without taking ownership.
```

## Borrowing Rules

```
At any time, you can have EITHER:
├─ Multiple &T (immutable borrows)
└─ OR one &mut T (mutable borrow)
Never both simultaneously.
```

## Ownership Patterns

| Pattern | Ownership | Cost | Use When |
|---------|-----------|------|----------|
| Move | Transfer | Zero | Caller doesn't need data anymore |
| `&T` | Borrow (shared) | Zero | Read-only access |
| `&mut T` | Borrow (exclusive) | Zero | Need to modify |
| `clone()` | Duplicate | Allocation + copy | Actually need a separate copy |
| `Rc<T>` | Shared (single-thread) | Ref-count | Multiple owners, one thread |
| `Arc<T>` | Shared (multi-thread) | Atomic ref-count | Multiple owners, any thread |
| `Cow<T>` | Clone-on-write | Alloc only if mutated | Sometimes borrowed, sometimes owned |

## Lifetime Basics

```rust
// Explicit lifetime: output lives for the shared overlap of both inputs
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() { x } else { y }
}

// Lifetime elision rules cover 85%+ of cases:
// 1. Each input reference gets its own lifetime
// 2. If there's one input, output gets its lifetime
// 3. If there's &self, output gets &self's lifetime
fn first_word(s: &str) -> &str {  // elided: 'a
    s.split_whitespace().next().unwrap_or("")
}
```

## `Cow` (Clone-on-Write)

```rust
use std::borrow::Cow;

// Zero-cost when no mutation needed
fn normalize(input: &str) -> Cow<'_, str> {
    if input.contains(' ') {
        Cow::Owned(input.replace(' ', "_"))  // allocates
    } else {
        Cow::Borrowed(input)  // zero-cost
    }
}
```

## Common Ownership Anti-Patterns

| Anti-Pattern | Why Bad | Better |
|--------------|---------|--------|
| `.clone()` everywhere | Hides ownership design issues | Restructure ownership |
| Fighting the borrow checker | Adds complexity | Work with compiler |
| `'static` for all lifetimes | Restricts flexibility | Use appropriate lifetimes |
| `Box::leak` to get `'static` | Memory leak | Proper lifetime design |
| `unsafe` to bypass borrow checker | UB risk | Find safe pattern |
| **Lifetime Laundering** — one lifetime ties input + output + cache | Fragile contract, collapses to ∅ in real code | Split lifetimes (`<'s, 'c>`) or store owned data |

## Error Code Quick Fix

| Error | Cause | Fix |
|-------|-------|-----|
| E0382 | Use after move | Clone, borrow, or redesign |
| E0507 | Move out of borrow | Clone or use reference |
| E0515 | Return local ref | Return owned value |
| E0597 | Reference outlives owner | Extend scope |
| E0716 | Temporary dropped | Bind to variable |
| E0106 | Missing lifetime | Add `'a` annotation |

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

After move: s1 is no longer valid
```

## Related References

- **Up:** [02-resource-mgmt](02-resource-mgmt.md) for smart pointers, [12-domain-modeling](12-domain-modeling.md) for Entity vs Value Object
- **Down:** [14-mental-models](14-mental-models.md) for understanding concepts
- **Domain:** Check domain mini-skills for domain-specific ownership rules
