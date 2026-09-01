# 02 — Resource Management (Smart Pointers)

> **Core Question:** *What ownership pattern does this resource need?*

## Decision Flowchart

```
Need heap allocation?
├─ Yes → Single owner?
│         ├─ Yes → Box<T>
│         └─ No → Multi-thread?
│                  ├─ Yes → Arc<T>
│                  └─ No → Rc<T>
└─ No → Stack allocation (default)

Reference cycles?
├─ Yes → Use Weak for one direction
└─ No → Regular Rc/Arc

Need interior mutability?
├─ Yes → Thread-safe?
│         ├─ Yes → Mutex<T> or RwLock<T>
│         └─ No → T: Copy? → Cell<T> : RefCell<T>
└─ No → &mut T
```

## Smart Pointer Comparison

| Type | Ownership | Thread-Safe | Use Case |
|------|-----------|-------------|----------|
| `Box<T>` | Single | Yes | Heap allocation, recursive types, trait objects |
| `Rc<T>` | Shared | **No** | Single-thread shared ownership |
| `Arc<T>` | Shared | Yes | Multi-thread shared ownership |
| `Weak<T>` | Weak ref | Same as parent | Break reference cycles |
| `Cell<T>` | Single copy | No | Interior mutability for `Copy` types |
| `RefCell<T>` | Single ref | No | Interior mutability with runtime borrow check |
| `Mutex<T>` | Single/multi | Yes | Thread-safe mutual exclusion |
| `RwLock<T>` | Single/multi | Yes | Read-heavy thread-safe access |
| `OnceLock<T>` | Single init | Yes | Lazy one-time initialization |

## Choosing the Right Pointer

### `Box<T>` — Single Owner, Heap

```rust
// Recursive type (can't have infinite stack size)
enum List<T> {
    Cons(T, Box<List<T>>),
    Nil,
}

// Trait object (dynamic dispatch)
let objects: Vec<Box<dyn Handler>> = vec![];
```

### `Rc<T>` vs `Arc<T>` — Shared Ownership

```rust
use std::rc::Rc;
use std::sync::Arc;

// Single-thread: Rc (cheaper, no atomics)
let shared: Rc<Data> = Rc::new(data);
let clone = Rc::clone(&shared);  // +1 ref count

// Multi-thread: Arc (atomic ref counting)
let shared: Arc<Data> = Arc::new(data);
let clone = Arc::clone(&shared);  // atomic +1
```

### `Weak<T>` — Breaking Cycles

```rust
use std::rc::{Rc, Weak};

struct Node {
    value: i32,
    children: Vec<Rc<Node>>,
    parent: Weak<Node>,  // Weak to avoid cycle
}

let leaf = Rc::new(Node { value: 3, children: vec![], parent: Weak::new() });
let branch = Rc::new(Node {
    value: 5,
    children: vec![Rc::clone(&leaf)],
    parent: Weak::new(),
});
// Update leaf's parent to weak reference
```

### Interior Mutability Decision

| Scenario | Solution |
|----------|----------|
| `T: Copy`, single-thread | `Cell<T>` |
| `T: !Copy`, single-thread | `RefCell<T>` |
| `T: Copy`, multi-thread | `AtomicBool`, `AtomicUsize`, etc. |
| `T: !Copy`, multi-thread | `Mutex<T>` or `RwLock<T>` |
| Read-heavy, multi-thread | `RwLock<T>` |
| Simple flags/counters | `AtomicBool`, `AtomicUsize` |

## Anti-Patterns

| Anti-Pattern | Why Bad | Better |
|--------------|---------|--------|
| `Arc` everywhere | Unnecessary atomic overhead | `Rc` for single-thread |
| `RefCell` everywhere | Runtime panics | Clear ownership |
| `Box` for small types | Unnecessary allocation | Stack allocation |
| Ignoring `Weak` for cycles | Memory leaks | Parent-child with `Weak` |

## Related References

- **Up:** [01-ownership](01-ownership.md) for ownership basics, [03-mutability](03-mutability.md) for interior mutability
- **Down:** [12-domain-modeling](12-domain-modeling.md) for aggregate ownership
