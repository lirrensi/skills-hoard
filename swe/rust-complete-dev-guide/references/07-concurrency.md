# 07 — Concurrency & Async

> **Core Question:** *Is this CPU-bound or I/O-bound, and what's the sharing model?*

## Workload Decision

```
What type of work?
├─ CPU-bound → std::thread or rayon
├─ I/O-bound → async/await (tokio)
└─ Mixed → hybrid with spawn_blocking

Need to share data?
├─ No → message passing (channels)
├─ Immutable → Arc<T>
└─ Mutable →
   ├─ Read-heavy → Arc<RwLock<T>>
   ├─ Write-heavy → Arc<Mutex<T>>
   └── Simple counter → AtomicUsize
```

## Send / Sync Explained

| Marker | Meaning | Common Types |
|--------|---------|--------------|
| `Send` | Ownership can be transferred across threads | Most types |
| `Sync` | References can be shared across threads | `Arc<T>`, `Mutex<T>` |
| `!Send` | Must stay on one thread | `Rc<T>`, `RefCell<T>` |
| `!Sync` | Cannot safely share references | `RefCell<T>`, `Cell<T>` |

## Concurrency Primitives

| Pattern | Thread-Safe | Blocking | Use When |
|---------|-------------|----------|----------|
| `std::thread` | Yes | Yes | CPU-bound parallelism |
| `rayon` | Yes | Yes | Data parallelism (easier) |
| `async/await` | Yes | No | I/O-bound concurrency |
| `Mutex<T>` | Yes | Yes | Shared mutable state |
| `RwLock<T>` | Yes | Yes | Read-heavy shared state |
| `mpsc::channel` | Yes | Optional | Message passing (MPSC) |
| `broadcast` | Yes | Optional | Pub/sub (MPMC) |
| `oneshot` | Yes | Optional | Single response |
| `watch` | Yes | No | Latest value updates |

## Async Patterns

### Tokio Runtime Setup

```toml
[dependencies]
tokio = { version = "1", features = ["full"] }
futures = "0.3"
```

```rust
#[tokio::main]
async fn main() -> Result<()> {
    // ...
    Ok(())
}
```

### Concurrent Tasks with JoinSet

```rust
use tokio::task::JoinSet;

async fn fetch_all(urls: Vec<String>) -> Result<Vec<String>> {
    let mut set = JoinSet::new();
    for url in urls {
        set.spawn(async move { fetch_url(&url).await });
    }

    let mut results = Vec::new();
    while let Some(res) = set.join_next().await {
        match res {
            Ok(Ok(data)) => results.push(data),
            Ok(Err(e)) => tracing::error!("Task failed: {}", e),
            Err(e) => tracing::error!("Join error: {}", e),
        }
    }
    Ok(results)
}
```

### Channels

```rust
use tokio::sync::{mpsc, broadcast, oneshot, watch};

// MPSC — work queue (multi-producer, single-consumer)
let (tx, mut rx) = mpsc::channel::<Job>(100);
tokio::spawn(async move {
    while let Some(job) = rx.recv().await {
        process(job).await;
    }
});

// Broadcast — pub/sub
let (tx, _) = broadcast::channel::<Event>(100);
let mut rx1 = tx.subscribe();
let mut rx2 = tx.subscribe();

// Oneshot — single response
let (tx, rx) = oneshot::channel::<Response>();
tokio::spawn(async move { tx.send(result).unwrap(); });
let response = rx.await.unwrap();

// Watch — latest value
let (tx, mut rx) = watch::channel("init");
tokio::spawn(async move {
    loop {
        rx.changed().await.unwrap();
        println!("New: {}", *rx.borrow());
    }
});
```

### Streams

```rust
use futures::stream::{self, StreamExt};

// Concurrency limit
let results: Vec<Result<String>> = stream::iter(urls)
    .map(|url| async move { fetch(&url).await })
    .buffer_unordered(10)  // max 10 concurrent
    .collect()
    .await;

// Merge streams
let merged = stream::select(stream1, stream2);
```

### Graceful Shutdown

```rust
use tokio_util::sync::CancellationToken;

async fn run_server() -> Result<()> {
    let token = CancellationToken::new();
    let worker_token = token.clone();

    // Worker that respects cancellation
    tokio::spawn(async move {
        loop {
            tokio::select! {
                _ = worker_token.cancelled() => {
                    tracing::info!("shutting down");
                    break;
                }
                _ = do_work() => {}
            }
        }
    });

    // Wait for Ctrl+C
    tokio::signal::ctrl_c().await?;
    token.cancel();  // Signal all workers
    Ok(())
}
```

## CRITICAL: Don't Hold Locks Across .await

```rust
// BAD: Lock held across await — blocks other tasks
async fn bad() {
    let guard = mutex.lock().await;
    do_something().await;  // guard still held!
}

// GOOD: Scope the lock
async fn good() {
    let result = {
        let guard = mutex.lock().await;
        compute(&guard)
    };  // guard dropped
    do_something().await;
}
```

## CRITICAL: `std::sync::Mutex` vs `tokio::sync::Mutex`

| Mutex | Hold Across `.await` | When To Use |
|-------|---------------------|-------------|
| `std::sync::Mutex` | ❌ **Never** — blocks executor threads and can deadlock | Short, sync critical sections |
| `tokio::sync::Mutex` | ⚠️ **Possible but usually avoid** — wait is async, guard stays locked until drop | Async critical sections that truly must span async code |

```rust
// BAD: std::sync::Mutex held across .await — blocks executor threads and can deadlock
async fn bad() {
    let guard = STD_MUTEX.lock().unwrap();  // std::sync::Mutex!
    do_something().await;  // guard is still held here
}

// BETTER: even with tokio::sync::Mutex, keep the critical section small
async fn good_tokio() {
    let guard = TOKIO_MUTEX.lock().await;  // tokio::sync::Mutex
    do_something_with_locked_data(&guard);
}  // lock released here

// POSSIBLE but often a smell: tokio::sync::Mutex guard held across .await
async fn sometimes_ok() {
    let mut guard = TOKIO_MUTEX.lock().await;
    guard.prepare();
    do_something().await;  // guard is STILL held here
}

// GOOD: Scope std::sync::Mutex tightly before .await
async fn good_scoped() {
    let result = {
        let guard = STD_MUTEX.lock().unwrap();
        compute(&guard)
    };  // dropped before .await
    do_something().await;
}
```

## CRITICAL: Async Cancellation Safety

Every `async fn` can be cancelled at any `.await` point (e.g., via `tokio::select!` or `tokio::time::timeout`). This is **not expressed in the type system** — you must document it manually.

### Cancel-Safe Operations (can be cancelled at any `.await`)

| Operation | Cancel-Safe? | Notes |
|-----------|-------------|-------|
| `tokio::io::AsyncReadExt::read` | ✅ Yes | Partial read OK |
| `tokio::io::AsyncReadExt::read_exact` | ❌ **No** | Partial read = data loss |
| `tokio::time::sleep` | ✅ Yes | No side effects |
| `Mutex::lock().await` | ✅ Yes | If cancelled while waiting, no lock is acquired |
| Channel `send().await` | ✅ Yes | Message not sent if cancelled |
| Channel `recv().await` | ✅ Yes | Message not consumed if cancelled |
| Database `query().await` | ❌ **Assume NOT** | Partial side effects possible |

### Protect Critical Sections

```rust
// Pattern: detach owned work from caller cancellation
async fn process(mut stream: TcpStream, db: Arc<Db>) -> Result<()> {
    let data = read_message(&mut stream).await?;  // can be cancelled

    // Move owned state into a spawned task. If the caller is cancelled while
    // awaiting the JoinHandle, the task may continue running in the background.
    let handle = tokio::spawn(async move {
        db.insert(&data).await?;
        send_ack(&mut stream).await?;
        Ok::<_, Error>(())
    });

    handle.await?
}

// Pattern: document cancel safety on every public async fn
/// Fetches and processes a message from the stream.
/// 
/// # Cancel safety
/// 
/// **NOT cancel-safe** — calls `db.insert()` before `send_ack()`,
/// which creates partial side effects if cancelled between them.
async fn process(stream: TcpStream, db: &Db) -> Result<()> { ... }
```

### Why This Matters

```rust
// If this future is used inside tokio::select! or timeout():
// The db.insert() may complete but send_ack() never runs.
// Client retries → duplicate data.
// No borrow checker error. No clippy warning. Only production pain.
async fn process(stream: TcpStream, db: &Db) -> Result<()> {
    let data = read_message(&stream).await?;
    db.insert(&data).await?;  // ◄── cancel point
    send_ack(&stream).await?;
    Ok(())
}
```

**Rule:** Every `async fn` that could appear inside `select!` / `timeout` must have a `// cancel-safe` or `// NOT cancel-safe` comment. If you use `tokio::spawn`, describe the real guarantee precisely: it detaches work from the caller's cancellation, but it does **not** make the task immune to runtime shutdown or process termination.

## Async Best Practices

### Do's

- Use `tokio::select!` for racing/timeout operations
- Prefer channels over shared state when possible
- Use `JoinSet` for managing dynamic task groups
- Instrument with `tracing` for debugging async code
- Handle cancellation with `CancellationToken`
- **Annotate cancel safety** on every public `async fn`
- Use `tokio::sync::Mutex` only when shared mutable state truly must survive across async boundaries

### Don'ts

- Never use `std::thread::sleep` in async (use `tokio::time::sleep`)
- Never hold `std::sync::Mutex` across `.await` (causes deadlocks)
- Never spawn unboundedly (use semaphores for limits)
- Don't ignore `Send` bounds for spawned futures
- Don't use `Rc` in async context (use `Arc`)
- Don't assume cancel safety — **document it explicitly**
- Don't assume `tokio::sync::Mutex` magically unlocks on `.await` — the guard stays held until drop

## Related References

- **Up:** [03-mutability](03-mutability.md) for interior mutability, [02-resource-mgmt](02-resource-mgmt.md) for smart pointers
- **Down:** [09-performance](09-performance.md) for optimizing async, [13-lifecycle](13-lifecycle.md) for resource cleanup
- **Domain:** Web → async by default, Embedded → no_std considerations, Cloud-Native → graceful shutdown
