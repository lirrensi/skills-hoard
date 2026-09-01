# 09 — Performance Optimization

> **Core Question:** *What's the bottleneck, and is optimization worth it?*

## The Golden Rule: Measure First

```
Without profiling, you're guessing.
With profiling, you're engineering.

Profile → Identify bottleneck → Fix → Measure again
```

## Optimization Priority

| Priority | Change | Typical Impact |
|----------|--------|----------------|
| 1 | Algorithm choice | 10× – 1000× |
| 2 | Data structure | 2× – 10× |
| 3 | Reduce allocations | 2× – 5× |
| 4 | Cache optimization | 1.5× – 3× |
| 5 | SIMD / Parallelism | 2× – 8× |

## Tools

| Tool | Purpose |
|------|---------|
| `cargo bench` | Benchmark entry point; built-in harness is nightly-only, stable users usually use Criterion |
| `criterion` | Statistical benchmarks (recommended) |
| `perf` / `flamegraph` | CPU profiling |
| `heaptrack` / `dhat` | Allocation tracking |
| `cachegrind` | Cache analysis |
| `tokio-console` | Async runtime debugging |
| **`cargo miri`** | **Detect UB in unsafe code** — run on ALL files with `unsafe` |

## Miri: Essential for Unsafe Code

`cargo miri` detects undefined behavior (null pointer deref, alignment violations, stacked borrows violations, etc.). In production LLM-generated unsafe code, ~55% of blocks contain UB detectable by Miri.

```bash
# Install (requires nightly)
rustup +nightly component add miri
cargo +nightly miri test

# CI recommendation: separate nightly job for all files with unsafe
cargo +nightly miri test --target-dir target/miri  # separate cache
```

**Warning:** Miri doesn't support FFI. For FFI-heavy crates, use `cargo careful` as a lighter alternative.

## Reducing Allocations

### Pre-allocation

```rust
// BAD: grows incrementally
let mut v = Vec::new();
for i in 0..1000 { v.push(i); }

// GOOD: pre-allocate exact capacity
let mut v = Vec::with_capacity(1000);
for i in 0..1000 { v.push(i); }
```

### Reuse Collections

```rust
// BAD: allocates new Vec each iteration
for chunk in data.chunks(100) {
    let mut results = Vec::new();
    process(chunk, &mut results);
}

// GOOD: reuse allocation
let mut results = Vec::new();
for chunk in data.chunks(100) {
    results.clear();
    process(chunk, &mut results);
}
```

### Avoid Cloning in Hot Paths

```rust
// BAD: clone when not needed
fn process(data: &Vec<u8>) {
    let owned = data.clone();  // Avoid unless necessary
    // ...
}

// GOOD: borrow instead
fn process(data: &[u8]) {
    // Just borrow — no allocation
}
```

### Small Vector Optimization

```rust
// Most vectors are small (0-10 elements)
// SmallVec avoids heap allocation for small sizes
use smallvec::{smallvec, SmallVec};

// Stack-allocate up to 4 elements
let v: SmallVec<[i32; 4]> = smallvec![1, 2, 3];
```

## Cache-Friendly Data Layout

```rust
// BAD: Array of Structs — bad cache for single-field access
struct Entity { id: u64, name: String, score: f64 }
let entities: Vec<Entity>;

// GOOD: Struct of Arrays — good cache for field-specific access
struct Entities {
    ids: Vec<u64>,
    names: Vec<String>,
    scores: Vec<f64>,
}
```

## Compiler Optimizations

### Cargo.toml for Release

```toml
[profile.release]
opt-level = 3
lto = "fat"           # Link-time optimization
codegen-units = 1     # Maximum optimization
panic = "abort"       # Smaller binary
strip = true          # Remove debug symbols

[profile.bench]
inherits = "release"
debug = true
strip = false
```

### Inline Hints

```rust
// Small hot function — inline across crate boundary
#[inline]
fn small_hot_function(x: i32) -> i32 { x + 1 }

// Cold path — never inline (save cache space)
#[inline(never)]
fn error_handler(e: Error) -> String { format!("error: {e}") }
```

### Cold Paths and Control-Flow Hints

```rust
// Stable Rust: split rare work into a cold function
#[cold]
#[inline(never)]
fn handle_error(err: &Error) {
    eprintln!("slow path: {err}");
}

if error_condition {
    handle_error(&err);
}
```

There is no stable `likely` / `unlikely` hint in `std`. In most application code, better branch structure and measurement matter more than manual prediction hints.

## Common Mistakes

| Mistake | Why Wrong | Better |
|---------|-----------|--------|
| Optimize without profiling | Wrong target | Profile first |
| Benchmark in debug mode | Meaningless results | Always `--release` |
| Using `LinkedList` | Cache-unfriendly | `Vec` or `VecDeque` |
| Hidden `.clone()` in hot path | Unnecessary allocs | Use references |
| Premature optimization | Wasted effort | Make it work first |
| `HashMap` for small sets | Overhead | `Vec` with linear search |
| **`Box::new([0u8; LARGE])`** | Goes through **stack first** → overflow! | `vec![0u8; N].into_boxed_slice()` |
| **Large array on stack** (`[u8; 1MB]`) | Stack overflow in debug mode | Heap allocation or `Box::new_uninit_slice` |

### Stack vs Heap: The Hidden Allocation Trap

```rust
// ❌ 1MB allocated on stack, THEN moved to heap — debug builds overflow
let buf: Box<[u8]> = Box::new([0u8; 1024 * 1024]);

// ✅ Direct heap allocation — no intermediate stack copy
let buf: Box<[u8]> = vec![0u8; 1024 * 1024].into_boxed_slice();

// ✅ Nightly: zero intermediate allocation
// let buf: Box<[u8]> = Box::<[u8]>::new_uninit_slice(1024 * 1024).assume_init();
```

**Rule:** Arrays > ~16KB should not live on the stack. `Box::new([val; N])` materializes the array on stack first. Use `vec![val; N].into_boxed_slice()` for guaranteed heap allocation.

## Anti-Patterns

| Anti-Pattern | Why Bad | Better |
|--------------|---------|--------|
| Clone to avoid lifetimes | Performance cost | Proper ownership design |
| `Box` everything | Indirection cost | Stack allocation when possible |
| String concat in loop | O(n²) | `String::with_capacity` or `join()` |
| Unbounded `Arc` usage | Atomic overhead | `Rc` for single-thread |

## Related References

- **Up:** [01-ownership](01-ownership.md) for reducing clones
- **Down:** [07-concurrency](07-concurrency.md) for parallelism options
- **Domain:** Embedded → minimal allocations, Web → latency requirements
