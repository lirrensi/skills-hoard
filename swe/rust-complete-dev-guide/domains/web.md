# 🌐 Web Domain

> **Layer 3: Domain Constraints** — *Async by default, thread-safe state, request lifecycle*

## Domain Constraints → Design Implications

| Domain Rule | Design Constraint | Rust Implication |
|-------------|-------------------|------------------|
| Stateless HTTP | No request-local globals | State in extractors |
| Concurrency | Handle many connections | Async, `Send` + `Sync` |
| Latency SLA | Fast response | Efficient ownership |
| Security | Input validation | Type-safe extractors |
| Observability | Request tracing | `tracing` + tower layers |

## Critical Constraints

### Async by Default

```
RULE: Web handlers must not block
WHY: Blocking one task blocks many requests
RUST: async/await, spawn_blocking for CPU work
```

### State Management

```
RULE: Shared state must be thread-safe
WHY: Handlers can run on any thread
RUST: Prefer immutable `Arc<T>` first; if mutation is unavoidable, choose the narrowest sync primitive and keep lock scopes tiny
```

### Request Lifecycle

```
RULE: Resources live only for request duration
WHY: Memory management, no leaks
RUST: Extractors, proper ownership
```

## Framework Comparison

| Framework | Style | Best For |
|-----------|-------|----------|
| **axum** | Functional, tower-based | Modern APIs, ergonomic |
| **actix-web** | Actor-based | High performance |
| **warp** | Filter composition | Composable APIs |
| **rocket** | Macro-driven | Rapid development |

## Common Mistakes in Web Domain

- Using `Rc` in shared state (must be `Arc`)
- Blocking in async handlers (use `spawn_blocking`)
- Not implementing graceful shutdown
- Missing `Send`/`Sync` bounds on handlers
- Over-collecting body data (use streaming)

## Recommended Crates

| Purpose | Crate |
|---------|-------|
| HTTP framework | `axum` |
| Serialization | `serde` + `serde_json` |
| Async runtime | `tokio` |
| Database | `sqlx` |
| Tracing | `tracing` + `tracing-subscriber` |
| Validation | `validator` |

These are defaults, not obligations. If your service is also **cloud-native**, **fintech**, or heavily streaming, load those domain mini-skills too before committing.

## Related References

- [07-concurrency](../references/07-concurrency.md) — async patterns, Send/Sync
- [03-mutability](../references/03-mutability.md) — shared mutable state
- [05-type-driven](../references/05-type-driven.md) — type-safe extractors
