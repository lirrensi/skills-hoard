# 🖥️ CLI Domain

> **Layer 3: Domain Constraints** — *User ergonomics, config precedence, exit codes*

## Domain Constraints → Design Implications

| Domain Rule | Design Constraint | Rust Implication |
|-------------|-------------------|------------------|
| User ergonomics | Clear help and errors | `clap` derive macros |
| Config precedence | CLI > env > file | Layered config loading |
| Exit codes | Non-zero on error | Proper `Result` handling |
| Stdout/stderr | Data vs errors | `eprintln!` for errors |
| Interruptible | Handle Ctrl+C | Signal handling |

## Critical Constraints

### Error Communication

```
RULE: Errors to stderr, data to stdout
WHY: Pipeable output, scriptability
RUST: eprintln! for errors, println! for data
```

### Configuration Priority

```
RULE: CLI args > env vars > config file > defaults
WHY: User expectation, override capability
RUST: Layered config with clap + figment
```

### Exit Codes

```
RULE: Return non-zero on any error
WHY: Script integration, automation
RUST: main() -> Result<(), Error> or process::exit(code)
```

## Key Crates

| Purpose | Crate |
|---------|-------|
| Argument parsing | `clap` (derive) |
| Interactive prompts | `dialoguer` |
| Progress bars | `indicatif` |
| Colored output | `colored` / `yansi` |
| Terminal UI | `ratatui` |
| Config layering | `figment` / `config` |

## Common Mistakes in CLI Domain

- Writing errors to stdout (breaks piping)
- Not handling SIGINT/SIGTERM gracefully
- Exiting with code 0 on error
- Not providing `--help` or poor error messages
- Blocking on I/O without progress indication

## Related References

- [05-type-driven](../references/05-type-driven.md) — derive-based arg structs
- [06-error-handling](../references/06-error-handling.md) — error propagation in main
- [13-lifecycle](../references/13-lifecycle.md) — progress bar as RAII
