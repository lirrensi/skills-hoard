# 📟 Embedded Domain

> **Layer 3: Domain Constraints** — *No heap, interrupt safety, hardware ownership*

## Domain Constraints → Design Implications

| Domain Rule | Design Constraint | Rust Implication |
|-------------|-------------------|------------------|
| No heap | Stack allocation only | `heapless` collections, arrays |
| No std | Core library only | `#![no_std]` |
| Real-time | Predictable timing | No dynamic allocation |
| Resource limited | Minimal memory | Static buffers, minimal types |
| Hardware safety | Safe peripheral access | HAL takes ownership |
| Interrupt safe | No blocking in ISR | Atomic ops, critical sections |

## Critical Constraints

### No Dynamic Allocation

```
RULE: Cannot use heap (no allocator)
WHY: Deterministic memory, no OOM
RUST: heapless::Vec<T, N>, arrays
```

### Interrupt Safety

```
RULE: Shared state must be interrupt-safe
WHY: ISR can preempt at any time
RUST: Mutex<RefCell<T>> + critical section
```

### Hardware Ownership

```
RULE: Peripherals must have clear ownership
WHY: Prevent conflicting access
RUST: HAL takes ownership, singleton pattern
```

## Layer Stack

```
Application
    ↓
RTIC / Embassy    (async runtime for embedded)
    ↓
HAL               (hardware abstraction layer)
    ↓
PAC               (peripheral access crate)
    ↓
Hardware
```

## Key Crates

| Purpose | Crate |
|---------|-------|
| HAL | `embedded-hal` |
| Async executor | `embassy` |
| RTOS framework | `RTIC` |
| Heap-free collections | `heapless` |
| Fixed-point math | `fixed` |

## Common Mistakes in Embedded Domain

- Using `Box`/`Vec`/`String` in `no_std` context
- Non-atomic shared state in interrupts
- Blocking in interrupt service routines
- Not accounting for watchdogs
- Forgetting `cargo install` for target toolchain

## Related References

- [02-resource-mgmt](../references/02-resource-mgmt.md) — heapless alternatives
- [03-mutability](../references/03-mutability.md) — `Mutex<RefCell<T>>` for ISR safety
- [01-ownership](../references/01-ownership.md) — singleton peripheral ownership
