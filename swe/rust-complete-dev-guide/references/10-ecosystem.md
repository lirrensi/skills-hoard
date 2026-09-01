# 10 — Ecosystem & Crate Integration

> **Core Question:** *What's the right crate for this job, and how should it integrate?*

## Essential Crate Categories

| Need | Recommended Crate | Why |
|------|-------------------|-----|
| Serialization | `serde` + `serde_json` | Industry standard, derive-based |
| Async runtime | `tokio` | Most popular, extensive ecosystem |
| HTTP client | `reqwest` | Ergonomic, async, TLS support |
| HTTP server | `axum` | Modern, tower-based, ergonomic |
| SQL database | `sqlx` | Compile-time checked queries |
| CLI parsing | `clap` (derive) | Type-safe, auto-generated help |
| Error handling (lib) | `thiserror` | Typed errors with derive |
| Error handling (app) | `anyhow` | Context, ergonomic propagation |
| Logging / tracing | `tracing` | Structured, async-aware, spans |
| Date/time | `time` (or `chrono`) | Type-safe durations, timezones |

These are **default starting points**, not mandatory answers. Before choosing one, check the domain mini-skills and ask: “What constraint would make this a bad fit?”

## Choose / Avoid Heuristics

| Crate / Tool | Good Default When | Reconsider When |
|--------------|-------------------|-----------------|
| `tokio` | General async services, web apps, background jobs | You are `no_std`, deeply embedded, or a tiny sync CLI with no async needs |
| `axum` | HTTP APIs with tower middleware and modern async stack | You need a different ecosystem style, already standardized elsewhere, or no HTTP server at all |
| `reqwest` | Standard HTTP client with ergonomic TLS + JSON | You need extreme minimalism, custom transport, or non-async constraints |
| `sqlx` | SQL-first apps that benefit from typed queries | You need a higher-level ORM, offline constraints, or non-SQL storage |
| `clap` | Full-featured CLIs with derive ergonomics | Your CLI is tiny enough that a minimal parser is simpler |
| `validator` | Request/input validation at boundaries | Your invariants are better expressed directly in types/newtypes |

## Crate Selection Criteria

| Criterion | Good Sign | Warning Sign |
|-----------|-----------|--------------|
| Maintenance | Recent commits, active releases | Years inactive |
| Community | Active issues, PRs accepted | No response to issues |
| Documentation | Examples, API docs, book | Minimal docs |
| Stability | Semver, stable releases | Frequent breaking changes |
| Dependencies | Minimal, well-known crates | Heavy, obscure deps |

## Cargo Features

```toml
[package]
name = "my-crate"

[features]
default = ["full"]
full = ["http", "cache"]
http = ["dep:reqwest"]
cache = ["dep:redis"]

[dependencies]
reqwest = { version = "0.12", optional = true }
redis = { version = "0.27", optional = true }

# Conditional dependency with features
tokio = { version = "1", features = ["rt", "macros"], optional = true }
```

## Language Interop

| Integration | Crate/Tool | Use Case |
|-------------|------------|----------|
| C/C++ → Rust | `bindgen` | Auto-generate Rust FFI bindings |
| Rust → C | `cbindgen` | Export C-compatible headers |
| Python ↔ Rust | `pyo3` | Python native extensions |
| Node.js ↔ Rust | `napi-rs` | Node.js addons |
| WebAssembly | `wasm-bindgen` | Browser/WASI targets |

## Workspace Setup

```toml
# Root Cargo.toml
[workspace]
resolver = "2"
members = ["crates/*"]

[workspace.dependencies]
serde = "1"
tokio = "1"
anyhow = "1"

[workspace.lints.clippy]
pedantic = "warn"
perf = "deny"
correct = "deny"
```

```toml
# crates/my-crate/Cargo.toml
[package]
name = "my-crate"
version.workspace = true
edition.workspace = true

[dependencies]
serde.workspace = true
tokio.workspace = true
```

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| E0433 | Can't find crate | Add to `Cargo.toml` dependencies |
| E0603 | Private item | Check visibility / re-exports |
| Feature not enabled | Optional feature missing | Enable in `features` |
| Version conflict | Incompatible transitive deps | `cargo update` or unify versions |

## Anti-Patterns

| Anti-Pattern | Why Bad | Better |
|--------------|---------|--------|
| `extern crate` | Outdated (pre-2018) | Just `use` |
| `#[macro_use]` | Global namespace pollution | Explicit `use` |
| Wildcard dep `"*"` | Unpredictable | Specific semver |
| Too many deps | Supply chain risk, compile time | Evaluate necessity |
| Vendoring everything | Maintenance burden | Vendor selectively; otherwise evaluate crates with supply-chain judgment |
| `Box<dyn Error>` for lib errors | Lost type info | `thiserror` |

## Related References

- **Up:** [06-error-handling](06-error-handling.md) for error type compatibility
- **Down:** [04-zero-cost](04-zero-cost.md) for trait integration with external types
- **Domain:** Check domain mini-skills for domain-specific crate recommendations
