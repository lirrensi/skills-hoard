# 11 — Anti-Patterns & Common Mistakes

> **Core Question:** *Is this pattern solving the symptom or the cause?*

## The Top 5 Beginner Mistakes

| Rank | Mistake | Why It Happens | Fix |
|------|---------|----------------|-----|
| 1 | `.clone()` to escape borrow checker | Don't understand ownership | Use references properly |
| 2 | `.unwrap()` in production | Laziness/panic | Propagate with `?` |
| 3 | `String` for everything | Habit from other langs | Use `&str`, `Cow<str>` |
| 4 | Index loops instead of iterators | C/Python habits | `.iter()`, `.enumerate()` |
| 5 | Fighting lifetimes instead of restructuring | Wrong data design | Own data instead of borrowing |

## Anti-Pattern Catalog

### Ownership & Borrowing

| Anti-Pattern | Why Bad | Better |
|--------------|---------|--------|
| `.clone()` everywhere | Hides design issues; performance cost | Proper references or ownership |
| Fighting borrow checker | Complex, hard-to-maintain code | Restructure data flow |
| `'static` on everything | Restricts flexibility unnecessarily | Use appropriate lifetimes |
| `unsafe` to bypass borrow checker | Undefined behavior risk | Find a safe pattern |
| `Rc` when single owner suffices | Unnecessary overhead | Simple owned value |

### Error Handling

| Anti-Pattern | Why Bad | Better |
|--------------|---------|--------|
| `.unwrap()` in production | Runtime panics | `?`, `expect("reason")`, or match |
| `panic!` for expected errors | Bad UX, no recovery | `Result<T, E>` |
| `Box<dyn Error>` for libraries | Lost type information | `thiserror` |
| Ignoring errors silently (`let _ =`) | Hidden bugs | Handle or propagate |
| Infinite retry | DoS yourself | Max attempts + backoff |

### Performance

| Anti-Pattern | Why Bad | Better |
|--------------|---------|--------|
| Clone to avoid lifetimes | Performance cost | Proper ownership design |
| `Box` everything | Indirection cost | Stack allocation when possible |
| `HashMap` for <10 items | Overhead | `Vec` with linear search |
| String concat in loop | O(n²) allocation | `with_capacity` or `join()` |
| `Arc` for single-threaded use | Atomic overhead | `Rc` or simple ownership |

### Concurrency & Async

| Anti-Pattern | Why Bad | Better |
|--------------|---------|--------|
| `Arc<Mutex<T>>` everywhere | Contention, complexity | Message passing |
| `std::thread::sleep` in async | Blocks entire executor | `tokio::time::sleep` |
| Holding locks across `.await` | Deadlocks other tasks | Scope the lock tightly |
| Unbounded task spawning | Resource exhaustion | `Semaphore` for limits |
| `Rc` in async context | !Send, can't spawn | `Arc` |

### Design

| Anti-Pattern | Why Bad | Better |
|--------------|---------|--------|
| Boolean flags for states | Runtime errors from invalid combos | Type state or enums |
| Primitive obsession | No type safety, argument swaps | Newtype wrappers |
| `&String` / `&Vec<T>` in params | Forces callers to own those types | `&str` / `&[T]` |
| Over-abstraction with generics | Slow compile, hard to read | Concrete types by default |
| Premature optimization | Wasted effort, complexity | Measure first |
| Making everything `pub` | Broken encapsulation | `pub(crate)`, private by default |
| Giant match arms (50+ lines) | Unmaintainable | Extract to methods |

## Code Smell → Refactoring

| Smell | Indicates | Refactoring |
|-------|-----------|-------------|
| Many `.clone()` calls | Ownership unclear | Trace ownership, use references |
| Many `.unwrap()` calls | Error handling missing | Add `?` or proper error types |
| Many `pub` fields | Encapsulation broken | Private + accessor methods |
| Deep nesting (>4 levels) | Complex logic | Extract methods |
| Long functions (>50 lines) | Multiple responsibilities | Split into smaller functions |
| Giant enums (>10 variants) | Missing abstraction | Consider trait + types |
| `todo!()` in production | Incomplete implementation | Implement or mark as `unimplemented!()` |

## Quick Review Checklist

- [ ] No `.clone()` without justification
- [ ] No `.unwrap()` in library/production code
- [ ] No `pub` fields with invariants
- [ ] No index loops when iterators work
- [ ] No `String` where `&str` or `Cow<str>` suffices
- [ ] No ignored `#[must_use]` warnings
- [ ] No `unsafe` without `// SAFETY:` comment
- [ ] No giant functions (>50 lines)
- [ ] No `Box<dyn Error>` in libraries
- [ ] No blocking calls in async context
- [ ] No `MutexGuard` held across `.await`
- [ ] No empty error handling (`if let Err(_) = ... { }`)

## Related References

- **Up:** Each anti-pattern links to its reference
- **Down:** [01-ownership](01-ownership.md), [06-error-handling](06-error-handling.md), [07-concurrency](07-concurrency.md)
- **Domain:** Each domain has its own anti-patterns
