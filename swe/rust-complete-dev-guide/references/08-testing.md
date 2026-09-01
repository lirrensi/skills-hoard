# 08 — Testing

> **Core Question:** *Does the code behave correctly for all expected and unexpected inputs?*

## TDD Workflow

```
RED     → Write a failing test first
GREEN   → Write minimal code to pass the test
REFACTOR → Improve code while keeping tests green
REPEAT  → Continue with next requirement
```

## Test Organization

```text
my_crate/
├── src/
│   └── lib.rs
├── tests/              # Integration tests
│   ├── api_test.rs     # Each file is a separate test binary
│   └── common/
│       └── mod.rs      # Shared test utilities
└── benches/
    └── benchmark.rs
```

## Unit Tests

```rust
// Module-level test module — co-located with code
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn creates_user_with_valid_email() {
        let user = User::new("Alice", "alice@example.com").unwrap();
        assert_eq!(user.display_name(), "Alice");
    }

    #[test]
    fn rejects_invalid_email() {
        let result = User::new("Bob", "not-an-email");
        assert!(result.is_err());
        assert!(result.unwrap_err().contains("invalid email"));
    }

    #[test]
    fn parse_succeeds() -> Result<(), Box<dyn std::error::Error>> {
        let config = parse_config(r#"{"port": 8080}"#)?;
        assert_eq!(config.port, 8080);
        Ok(())
    }
}
```

## Integration Tests

```rust
// tests/api_test.rs
use my_crate::{App, Config};

#[test]
fn full_request_lifecycle() {
    let config = Config::test_default();
    let app = App::new(config);
    let response = app.handle_request("/health");
    assert_eq!(response.status, 200);
}
```

## Async Tests

```rust
#[tokio::test]
async fn fetches_data_successfully() {
    let client = TestClient::new().await;
    let result = client.get("/data").await;
    assert!(result.is_ok());
}

#[tokio::test]
async fn handles_timeout() {
    let result = tokio::time::timeout(
        Duration::from_millis(100),
        slow_operation(),
    ).await;
    assert!(result.is_err());
}
```

## Parameterized Tests with rstest

```rust
use rstest::{rstest, fixture};

#[rstest]
#[case("hello", 5)]
#[case("", 0)]
#[case("rust", 4)]
fn test_length(#[case] input: &str, #[case] expected: usize) {
    assert_eq!(input.len(), expected);
}

#[fixture]
fn test_db() -> TestDb {
    TestDb::new_in_memory()
}

#[rstest]
fn test_insert(test_db: TestDb) {
    test_db.insert("key", "value");
    assert_eq!(test_db.get("key"), Some("value".into()));
}
```

## Property-Based Testing with proptest

```rust
use proptest::prelude::*;

proptest! {
    #[test]
    fn sort_preserves_length(mut vec in prop::collection::vec(any::<i32>(), 0..100)) {
        let len = vec.len();
        vec.sort();
        assert_eq!(vec.len(), len);
    }

    #[test]
    fn sort_produces_ordered_output(mut vec in prop::collection::vec(any::<i32>(), 0..100)) {
        vec.sort();
        for w in vec.windows(2) {
            assert!(w[0] <= w[1]);
        }
    }
}
```

## Mocking with mockall

```rust
use mockall::{automock, predicate::eq};

#[automock]
trait UserRepository {
    fn find_by_id(&self, id: u64) -> Option<User>;
}

#[test]
fn service_returns_user_when_found() {
    let mut mock = MockUserRepository::new();
    mock.expect_find_by_id()
        .with(eq(42))
        .times(1)
        .returning(|_| Some(User { id: 42, name: "Alice".into() }));

    let service = UserService::new(Box::new(mock));
    assert_eq!(service.get_user(42).unwrap().name, "Alice");
}
```

## Doc Tests

```rust
/// Adds two numbers.
///
/// # Examples
///
/// ```
/// use my_crate::add;
/// assert_eq!(add(2, 3), 5);
/// ```
///
/// # Errors
///
/// Returns an error if the result overflows.
pub fn add(a: i32, b: i32) -> i32 {
    a + b
}
```

## Benchmarking with Criterion

```toml
# Cargo.toml
[dev-dependencies]
criterion = { version = "0.5", features = ["html_reports"] }

[[bench]]
name = "benchmark"
harness = false
```

```rust
use criterion::{black_box, criterion_group, criterion_main, Criterion};

fn bench_fibonacci(c: &mut Criterion) {
    c.bench_function("fib 20", |b| b.iter(|| fibonacci(black_box(20))));
}

criterion_group!(benches, bench_fibonacci);
criterion_main!(benches);
```

## Coverage

```bash
cargo llvm-cov                    # Summary
cargo llvm-cov --html             # HTML report
cargo llvm-cov --fail-under-lines 80  # Fail if below 80%
```

## Testing Commands

```bash
cargo test                        # All tests
cargo test -- --nocapture         # With println output
cargo test test_name              # Specific test
cargo test --lib                  # Unit tests only
cargo test --test api_test        # Integration tests
cargo test --doc                  # Doc tests
cargo test -- --ignored           # Ignored tests
```

## Best Practices

**DO:**
- Write tests FIRST (TDD cycle)
- Use `#[cfg(test)] mod tests { }` for unit tests
- Test behavior, not implementation
- Use descriptive test names: `process_should_return_error_when_input_empty`
- Prefer `assert_eq!` over `assert!` for better error messages
- Use `result?` in tests returning `Result` for cleaner output
- Keep tests independent — no shared mutable state

**DON'T:**
- Use `#[should_panic]` when `Result::is_err()` works
- Mock everything — prefer integration tests when feasible
- Ignore flaky tests — fix or quarantine them
- Use `sleep()` in tests — use channels, barriers, or `tokio::time::pause()`

## Related References

- **Up:** [06-error-handling](06-error-handling.md) for error type design
- **Down:** [09-performance](09-performance.md) for benchmarking
- **Domain:** Web → integration test endpoints, CLI → test exit codes and piping
