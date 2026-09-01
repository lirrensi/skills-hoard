# 03 — Mutability & Interior Mutability

> **Core Question:** *Why does this data need to change, and who can change it?*

## The Fundamental Borrow Rule

```
At any time, you can have EITHER:
├─ Multiple &T (immutable borrows)     ← shared read access
└─ OR one &mut T (mutable borrow)      ← exclusive write access
```

## When To Use Each Pattern

| Pattern | Thread-Safe | Runtime Cost | Use When |
|---------|-------------|--------------|----------|
| `&mut T` | N/A (compile-checked) | Zero | Exclusive mutable access |
| `Cell<T>` | No | Zero | Copy types, no references |
| `RefCell<T>` | No | Runtime borrow check | Non-Copy, need `&self` mutation |
| `Mutex<T>` | Yes | Lock contention | Thread-safe mutation |
| `RwLock<T>` | Yes | Lock contention | Many readers, few writers |
| `AtomicBool`, `AtomicUsize`, etc. | Yes | Minimal | Simple flags and counters |

## Interior Mutability Decision Tree

```
Need mutable access through &self?
├─ Yes → Single-threaded?
│         ├─ Yes → T: Copy?
│         │         ├─ Yes → Cell<T>
│         │         └─ No → RefCell<T>
│         └─ No → T: Copy?
│                  ├─ Yes → Atomic*
│                  └─ No → Mutex<T> or RwLock<T>
└─ No → Use &mut T (standard mutable borrow)
```

## Common Patterns

### RefCell — Runtime Borrow Checking

```rust
use std::cell::RefCell;

struct Cache {
    data: RefCell<HashMap<String, String>>,
}

impl Cache {
    fn get(&self, key: &str) -> Option<String> {
        self.data.borrow().get(key).cloned()  // borrow() returns Ref
    }

    fn insert(&self, key: String, value: String) {
        self.data.borrow_mut().insert(key, value);  // borrow_mut() returns RefMut
    }
}
```

### Mutex — Thread-Safe Mutation

```rust
use std::sync::{Arc, Mutex};

struct Counter {
    inner: Arc<Mutex<u64>>,
}

impl Counter {
    fn increment(&self) {
        let mut count = self.inner.lock().unwrap();  // Lock guard
        *count += 1;
    }  // Guard dropped here, lock released
}
```

### RwLock — Read-Heavy Workloads

```rust
use std::sync::RwLock;

struct Config {
    cache: RwLock<HashMap<String, String>>,
}

impl Config {
    fn get(&self, key: &str) -> Option<String> {
        self.cache.read().unwrap().get(key).cloned()  // Multiple readers OK
    }

    fn set(&self, key: String, value: String) {
        self.cache.write().unwrap().insert(key, value);  // Exclusive writer
    }
}
```

## Important: RefCell Panic

```rust
// This panics at runtime — don't do this:
let cell = RefCell::new(42);
let _ref1 = cell.borrow();
let _ref2 = cell.borrow_mut();  // PANIC: already borrowed

// Use try_borrow / try_borrow_mut for non-panicking version:
if let Ok(mut ref2) = cell.try_borrow_mut() {
    *ref2 = 43;
} else {
    // Handle borrow conflict gracefully
}
```

## Deadlock Prevention

```rust
// BAD: Lock order can cause deadlocks
// Thread 1: lock A → lock B
// Thread 2: lock B → lock A

// GOOD: Consistent lock ordering
// Always lock in the same order: A → B → C

// GOOD: Use try_lock for non-blocking attempts
if let Ok(guard) = mutex.try_lock() {
    // Got the lock
} else {
    // Do something else instead of blocking
}
```

## Anti-Patterns

| Anti-Pattern | Why Bad | Better |
|--------------|---------|--------|
| `RefCell` everywhere | Runtime panics hiding design issues | Clear ownership design |
| `Mutex` for single-thread | Unnecessary overhead | `RefCell` |
| Lock inside hot loop | Performance killer | Batch operations |
| `MutexGuard` across `.await` | Deadlock in async | Scope the lock tightly |

## Error Codes

| Error | Cause | Fix |
|-------|-------|-----|
| E0596 | Borrowing immutable as mutable | Add `mut` or redesign |
| E0499 | Multiple mutable borrows | Restructure code flow |
| E0502 | `&mut` while `&` exists | Separate borrow scopes |

## Related References

- **Up:** [02-resource-mgmt](02-resource-mgmt.md) for smart pointer choice
- **Down:** [07-concurrency](07-concurrency.md) for thread safety patterns
- **Domain:** Web → use `Arc<RwLock<T>>`, Embedded → use `Mutex<RefCell<T>>`
