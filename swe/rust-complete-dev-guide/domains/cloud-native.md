# ☁️ Cloud-Native Domain

> **Layer 3: Domain Constraints** — *12-Factor, stateless, graceful shutdown, observability*

## Domain Constraints → Design Implications

| Domain Rule | Design Constraint | Rust Implication |
|-------------|-------------------|------------------|
| 12-Factor app | Config from environment | Environment-based config |
| Observability | Metrics + traces | `tracing` + `opentelemetry` |
| Health checks | Liveness/readiness | Dedicated endpoints |
| Graceful shutdown | Clean termination | Signal handling |
| Horizontal scale | Stateless design | No local persistent state |
| Container-friendly | Small binaries | Release optimization |

## Critical Constraints

### Stateless Design

```
RULE: No local persistent state
WHY: Pods can be killed/rescheduled anytime
RUST: External state (Redis, DB), no static mut
```

### Graceful Shutdown

```
RULE: Handle SIGTERM, drain connections
WHY: Zero-downtime deployments
RUST: tokio::signal + graceful shutdown
```

### Observability

```
RULE: Every request must be traceable
WHY: Debugging distributed systems
RUST: tracing spans, opentelemetry export
```

## Key Crates

| Purpose | Crate |
|---------|-------|
| gRPC | `tonic` |
| Kubernetes | `kube`, `kube-runtime` |
| Docker | `bollard` |
| Tracing | `tracing`, `opentelemetry` |
| Metrics | `metrics` + `prometheus` |

## Common Mistakes in Cloud-Native Domain

- Storing state locally (breaks horizontal scaling)
- Not handling SIGTERM (causes connection drops)
- No health check endpoints
- Missing distributed tracing context propagation
- Large binary sizes (use LTO, strip)

## Related References

- [07-concurrency](../references/07-concurrency.md) — graceful shutdown, signal handling
- [13-lifecycle](../references/13-lifecycle.md) — connection draining
- [09-performance](../references/09-performance.md) — release optimization
