# 06 — Error Handling

> **Core Question:** *Is this failure expected or a bug?*

## Error Handling Strategy Decision

```
Is failure expected in normal operation?
├─ Yes → Is absence the only "failure"?
│         ├─ Yes → Option<T>
│         └─ No → Result<T, E>
│                  ├─ Library → thiserror (typed errors)
│                  └─ Application → anyhow (ergonomic)
└─ No → Is it a bug/invariant violation?
         ├─ Yes → panic! / expect("reason")
         └─ No → Reconsider — should be Result

Propagating with ? → Need context?
├─ Yes → .context("message") / .with_context(|| format!("..."))
└─ No → Plain ?
```

## Boundary-Based Error Guidance

| Boundary | Default | Why |
|---------|---------|-----|
| **Public library / reusable crate API** | `thiserror` | Callers need typed errors to match on |
| **Internal module boundary** | Typed error or concrete domain enum | Preserves structure while code is still reusable |
| **Executable edge (`main`, CLI command, job runner, HTTP handler edge)** | `anyhow` is often fine | Ergonomic context + top-level reporting |
| **Mixed workspace** | Both | `thiserror` at reusable boundaries, `anyhow` near executable edges |

`Library vs application` is only a shortcut. In real codebases, decide based on **boundary**, not just crate kind.

### Library: thiserror

```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum DbError {
    #[error("record not found: {id}")]
    NotFound { id: String },

    #[error("connection failed: {0}")]
    Connection(#[from] std::io::Error),

    #[error("validation error: {0}")]
    Validation(String),
}

// Usage — consumers can match on error variants
fn get_user(id: &str) -> Result<User, DbError> {
    let record = db.query(id).map_err(DbError::Connection)?;
    record.ok_or_else(|| DbError::NotFound { id: id.into() })
}
```

### Application: anyhow

```rust
use anyhow::{Context, Result, bail};

fn load_config(path: &str) -> Result<Config> {
    let content = std::fs::read_to_string(path)
        .with_context(|| format!("failed to read config from {path}"))?;

    let config: Config = toml::from_str(&content)
        .with_context(|| format!("failed to parse config at {path}"))?;

    if config.port == 0 {
        bail!("port must be non-zero");
    }

    Ok(config)
}
```

## Error Categorization (Domain Level)

| Error Type | Audience | Recovery | Example |
|------------|----------|----------|---------|
| **User-facing** | End users | Guide action | `InvalidEmail`, `NotFound` |
| **Internal** | Developers | Debug info | `DatabaseError`, `ParseError` |
| **System** | Ops/SRE | Monitor/alert | `ConnectionTimeout`, `RateLimited` |
| **Transient** | Automation | Retry | `NetworkError`, `ServiceUnavailable` |
| **Permanent** | Human | Investigate | `ConfigInvalid`, `DataCorrupted` |

## Recovery Patterns

| Pattern | When | Implementation |
|---------|------|----------------|
| **Retry** | Transient + idempotent failures | Exponential backoff |
| **Fallback** | Degraded mode | Cached/default value |
| **Circuit Breaker** | Cascading failures | `failsafe-rs` |
| **Timeout** | Slow operations | `tokio::time::timeout` |
| **Bulkhead** | Isolation | Separate thread pools |

### Retry Pattern

```rust
use tokio_retry::{Retry, strategy::ExponentialBackoff};

async fn with_retry<F, Fut, T, E>(operation: F) -> Result<T, E>
where
    F: Fn() -> Fut,
    Fut: Future<Output = Result<T, E>>,
    E: std::fmt::Debug,
{
    let strategy = ExponentialBackoff::from_millis(100)
        .max_delay(Duration::from_secs(10))
        .take(3);

    Retry::spawn(strategy, operation).await
}
```

## Common Mistakes

| Mistake | Why Wrong | Better |
|---------|-----------|--------|
| `unwrap()` everywhere | Panics in production | `?` or `expect("reason")` |
| Same error for all cases | No actionability | Categorize by audience |
| `panic!` for expected errors | Bad UX, no recovery | `Result` |
| Retry everything | Wasted resources | Only transient errors |
| Infinite retry | DoS yourself | Max attempts + backoff |
| Expose internal errors | Security risk | User-friendly messages |
| `Box<dyn Error>` everywhere | Lost type info | `thiserror` |
| Ignore errors silently | Bugs hidden | Handle or propagate |

## Error Handling Patterns in Async

```rust
// Timeout wrapper
use tokio::time::timeout;

async fn fetch_with_timeout(url: &str) -> Result<String> {
    timeout(Duration::from_secs(5), fetch(url))
        .await
        .map_err(|_| anyhow!("request timed out"))?
}
```

## Related References

- **Up:** [13-lifecycle](13-lifecycle.md) for RAII cleanup on error
- **Down:** [12-domain-modeling](12-domain-modeling.md) for domain error categorization
- **Domain:** Check domain mini-skills for domain-specific error requirements
