# 13 — Resource Lifecycle

> **Core Question:** *When should this resource be created, used, and cleaned up?*

## Lifecycle Patterns

| Pattern | Type | Use Case |
|---------|------|----------|
| **RAII** | `Drop` trait | Auto cleanup on scope exit |
| **Lazy Init** | `OnceLock`, `LazyLock` | Deferred initialization |
| **Pool** | `r2d2`, `deadpool` | Connection reuse |
| **Guard** | `MutexGuard` pattern | Scoped lock release |
| **Scope** | Custom struct | Transaction boundaries |

## RAII — Resource Acquisition Is Initialization

```rust
// Resources are acquired at construction and released at Drop
struct TempFile {
    path: PathBuf,
    file: File,
}

impl TempFile {
    fn new(path: PathBuf) -> io::Result<Self> {
        let file = File::create(&path)?;
        Ok(Self { path, file })
    }

    fn write(&mut self, data: &[u8]) -> io::Result<()> {
        self.file.write_all(data)
    }
}

impl Drop for TempFile {
    fn drop(&mut self) {
        // Automatic cleanup when owner goes out of scope
        let _ = std::fs::remove_file(&self.path);
    }
}
// Usage: TempFile::new("temp.txt")?.write(b"data")?;
//        → file closed, temp deleted automatically
```

## Guard Pattern

```rust
struct Transaction<'a> {
    db: &'a Database,
    active: bool,
}

impl<'a> Transaction<'a> {
    fn begin(db: &'a Database) -> Result<Self, DbError> {
        db.execute("BEGIN")?;
        Ok(Self { db, active: true })
    }

    pub fn commit(mut self) -> Result<(), DbError> {
        self.db.execute("COMMIT")?;
        self.active = false;  // Prevent double-drop rollback
        Ok(())
    }
}

impl Drop for Transaction<'_> {
    fn drop(&mut self) {
        if self.active {
            // Auto-rollback on error or panic
            let _ = self.db.execute("ROLLBACK");
        }
    }
}

// Usage:
fn transfer(db: &Database, from: &str, to: &str, amount: f64) -> Result<()> {
    let tx = Transaction::begin(db)?;
    db.execute("UPDATE accounts SET balance = balance - $1 WHERE id = $2", &[amount, from])?;
    db.execute("UPDATE accounts SET balance = balance + $1 WHERE id = $2", &[amount, to])?;
    tx.commit()?;  // If this fails, tx drops → auto-rollback
    Ok(())
}
```

## Lazy Initialization

```rust
use std::sync::OnceLock;

// Thread-safe lazy singleton (Rust 1.70+)
static CONFIG: OnceLock<Config> = OnceLock::new();

fn get_config() -> &'static Config {
    CONFIG.get_or_init(|| {
        Config::load("config.toml").expect("config must be valid")
    })
}

// For single-threaded lazy init
use std::cell::OnceCell;

thread_local! {
    static CACHE: OnceCell<ExpensiveCache> = const { OnceCell::new() };
}
```

## Connection Pool Pattern

```rust
use std::sync::Mutex;
use tokio::sync::Semaphore;

struct Pool {
    semaphore: Semaphore,
    connections: Mutex<Vec<Connection>>,
}

impl Pool {
    fn new(size: usize) -> Self {
        Self {
            semaphore: Semaphore::new(size),
            connections: Mutex::new((0..size).map(|_| Connection::new()).collect()),
        }
    }

    async fn acquire(&self) -> PooledConnection<'_> {
        let permit = self.semaphore.acquire().await.unwrap();
        let conn = self.connections.lock().unwrap().pop().unwrap();
        PooledConnection { pool: self, conn: Some(conn), _permit: permit }
    }
}

// RAII guard returns connection to pool on drop
struct PooledConnection<'a> {
    pool: &'a Pool,
    conn: Option<Connection>,
    _permit: tokio::sync::SemaphorePermit<'a>,
}

impl Drop for PooledConnection<'_> {
    fn drop(&mut self) {
        if let Some(conn) = self.conn.take() {
            self.pool.connections.lock().unwrap().push(conn);
        }
    }
}
```

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| Resource leak | Forgot to implement `Drop` | Implement `Drop` or RAII wrapper |
| Use after drop | Dangling reference | Check lifetimes |
| E0509 — move out of drop | Moving field from type with `Drop` | `Option::take()` |
| Pool exhaustion | Connections not returned | Ensure `Drop` returns connections |

### ⚠️ CRITICAL: Drop in Async Context

`Drop` runs synchronously. If a transaction/connection `Drop` does implicit rollback that blocks (e.g., `sqlx` → blocking rollback in async runtime), it causes warnings or hangs.

```rust
// ❌ If commit fails, tx drops → implicit rollback may block inside async runtime
async fn run(db: &Pool) -> Result<Data> {
    let tx = db.transaction().await?;
    let result = do_work(&tx).await?;
    tx.commit().await?;  // what if this fails?
    Ok(result)  // tx drops here on early return too — implicit rollback in Drop
}

// ✅ Use a guard pattern with explicit rollback handling
struct TxGuard<'a> {
    tx: Option<Transaction<'a>>,
    committed: bool,
}
impl<'a> TxGuard<'a> {
    async fn begin(db: &'a Pool) -> Result<Self> {
        Ok(Self { tx: Some(db.transaction().await?), committed: false })
    }
    async fn commit(mut self) -> Result<()> {
        self.tx.take().unwrap().commit().await?;
        self.committed = true;
        Ok(())
    }

    async fn rollback(mut self) -> Result<()> {
        if let Some(tx) = self.tx.take() {
            tx.rollback().await?;
        }
        self.committed = true;
        Ok(())
    }
}
impl Drop for TxGuard<'_> {
    fn drop(&mut self) {
        if !self.committed {
            // Drop cannot await. At this point your only safe options are
            // logging, metrics, or other synchronous fallout handling.
            tracing::warn!("transaction dropped without explicit commit/rollback");
        }
    }
}
```

**Rule:** Be aware of what `Drop` does for your transaction/connection types. If cleanup is async or blocking, don't rely on `Drop` to perform it inside async code. Use explicit `commit().await` / `rollback().await`; let `Drop` only detect mistakes.

## Anti-Patterns

| Anti-Pattern | Why Bad | Better |
|--------------|---------|--------|
| Manual cleanup | Easy to forget | RAII / `Drop` |
| `lazy_static!` | External dependency | `std::sync::OnceLock` |
| Global mutable state | Thread unsafety | `OnceLock` or proper sync |
| Forget to close connections | Resource leak | Pool with `Drop` impl |
| `Box::leak` for static lifetime | Permanent leak | `OnceLock` or proper design |

## Related References

- **Up:** [02-resource-mgmt](02-resource-mgmt.md) for smart pointers
- **Down:** [07-concurrency](07-concurrency.md) for thread-safe init, [12-domain-modeling](12-domain-modeling.md) for aggregate lifecycle
- **Domain:** Web → request lifecycle, Embedded → hardware RAII
