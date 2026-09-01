# 💰 FinTech Domain

> **Layer 3: Domain Constraints** — *Precision, audit, consistency, compliance*

## Domain Constraints → Design Implications

| Domain Rule | Design Constraint | Rust Implication |
|-------------|-------------------|------------------|
| Audit trail | Immutable records | `Arc<T>`, event sourcing |
| Precision | No floating point for money | `rust_decimal::Decimal` |
| Consistency | Transaction boundaries | Clear ownership, RAII |
| Compliance | Complete logging | Structured `tracing` |
| Reproducibility | Deterministic execution | No race conditions |

## Critical Constraints

### Financial Precision

```
RULE: Never use f64 for money!
WHY: 0.1 + 0.2 != 0.3 in floating point
RUST: Use rust_decimal::Decimal for exact math
```

### Audit Requirements

```
RULE: All transactions must be immutable and traceable
WHY: Regulatory compliance, dispute resolution
RUST: Arc<T> for sharing, event sourcing pattern
```

### Consistency

```
RULE: Money can't disappear or appear
WHY: Double-entry accounting principles
RUST: Transaction types with validated totals
```

## Key Crates

| Purpose | Crate |
|---------|-------|
| Decimal math | `rust_decimal` |
| Date/time | `time` or `chrono` |
| UUID | `uuid` |
| Serialization | `serde` |
| Validation | `validator` |

## Common Mistakes in FinTech Domain

- Using `f64` for monetary values (precision loss!)
- Mutable transaction records (need audit trail)
- Not having transaction boundaries
- Ignoring rounding rules (banker's rounding)
- Missing idempotency keys for payments

## Related References

- [12-domain-modeling](../references/12-domain-modeling.md) — Value Objects for Currency, Amount
- [05-type-driven](../references/05-type-driven.md) — newtype for money, validated constructors
- [13-lifecycle](../references/13-lifecycle.md) — RAII transaction guards
