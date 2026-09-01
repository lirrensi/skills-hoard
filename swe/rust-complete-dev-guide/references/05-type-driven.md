# 05 — Type-Driven Design

> **Core Question:** *How can the type system prevent invalid states?*

## Philosophy: Make Illegal States Unrepresentable

Before reaching for runtime checks, ask:
- Can the compiler catch this error?
- Can invalid states be impossible to represent?
- Can the type encode the invariant?

## Core Patterns

| Pattern | Purpose | Example |
|---------|---------|---------|
| **Newtype** | Type safety for primitives | `struct Email(String)` |
| **Type State** | Compile-time state machine | `Connection<Authenticated>` |
| **PhantomData** | Type/lifetime markers without data | `PhantomData<&'a T>` |
| **Marker Type / Trait** | Capability flags | `UserInput<Sanitized>` |
| **Builder** | Gradual construction | `Builder::new().field(x).build()` |
| **Sealed Trait** | Prevent external implementations | `mod private { trait Sealed {} }` |

## Pattern Details

### Newtype

```rust
// Type-safe wrapper → no more swapping arguments
struct UserId(u64);
struct OrderId(u64);

fn get_order(user: UserId, order: OrderId) -> Order { ... }
// Compiler catches: get_order(order_id, user_id) // type error!

// Validated newtype — parse once, trust forever
#[derive(Debug, Clone)]
struct Email(String);

impl Email {
    pub fn new(s: &str) -> Result<Self, ValidationError> {
        if !s.contains('@') {
            return Err(ValidationError("invalid email"));
        }
        Ok(Self(s.to_string()))
    }
}

impl AsRef<str> for Email {
    fn as_ref(&self) -> &str { &self.0 }
}
```

### Type State Pattern

```rust
// Compile-time state machine — invalid transitions are compiler errors
struct Connection<State> {
    stream: TcpStream,
    _state: std::marker::PhantomData<State>,
}

// State marker types (zero-sized)
struct Connected;
struct Authenticated;

impl Connection<Connected> {
    fn connect(addr: &str) -> Self {
        Self { stream: TcpStream::connect(addr).unwrap(), _state: PhantomData }
    }
    fn authenticate(self, token: &str) -> Connection<Authenticated> {
        // authenticate...
        Connection { stream: self.stream, _state: PhantomData }
    }
}

impl Connection<Authenticated> {
    fn send(&self, data: &[u8]) { /* ... */ }
}
// Compile error: c.send() before authenticate!
// Compile error: c.authenticate() twice!
```

### Builder Pattern

```rust
#[derive(Debug)]
struct Request {
    url: String,
    method: String,
    headers: Vec<(String, String)>,
    body: Option<String>,
}

struct RequestBuilder {
    url: String,
    method: String,
    headers: Vec<(String, String)>,
    body: Option<String>,
}

impl RequestBuilder {
    fn new(url: impl Into<String>) -> Self {
        Self { url: url.into(), method: "GET".into(), headers: vec![], body: None }
    }
    fn method(mut self, method: impl Into<String>) -> Self { self.method = method.into(); self }
    fn header(mut self, key: impl Into<String>, value: impl Into<String>) -> Self {
        self.headers.push((key.into(), value.into())); self
    }
    fn body(mut self, body: impl Into<String>) -> Self { self.body = Some(body.into()); self }
    fn build(self) -> Request {
        Request { url: self.url, method: self.method, headers: self.headers, body: self.body }
    }
}
// Usage: RequestBuilder::new("https://api.example.com")
//     .method("POST")
//     .header("Content-Type", "application/json")
//     .body(r#"{"key": "value"}"#)
//     .build()
```

### ⚠️ Sealed Trait — PROTECT Against Blanket Impl Semver Hazards

```rust
// Users of your crate can USE the trait but not IMPLEMENT it
mod private {
    pub trait Sealed {}
}

pub trait MyTrait: private::Sealed {
    fn do_thing(&self);
}

// Only you (in your crate) can implement MyTrait
pub struct MyType;
impl private::Sealed for MyType {}
impl MyTrait for MyType {
    fn do_thing(&self) { /* ... */ }
}
```

### ⚠️ CRITICAL: Blanket Impl Semver Hazard

**Never add a blanket `impl<T: Foo> Bar for T` in a public API unless the trait is sealed.**

Why: Downstream crates may have their own `impl Bar for MyType`. If you later add or change a blanket impl in a minor release, it breaks downstream compilation. The compiler error appears on YOUR CI only when downstream builds — not yours.

```rust
// Crate A v1.0:
pub trait Bar { fn bar(&self) -> String; }

// Downstream crate B:
struct MyType;
impl Display for MyType { /* ... */ }
impl Bar for MyType { /* custom behavior */ }  // ✅ Compiles against A v1.0

// Crate A v1.1 (minor release):
impl<T: Display> Bar for T { /* generic behavior */ }
// ❌ Downstream crate B now fails to compile because MyType matches both impls

// ✅ SAFE: sealed trait prevents external impl, so blanket impl can't conflict
mod private { pub trait Sealed {} }
pub trait Bar: private::Sealed { fn bar(&self) -> String; }
// Blanket impl only for types YOU know about
```

**Rule:** Blanket `impl` in public API → only with sealed trait. Otherwise, write per-type `impl` blocks.

### Marker Traits / Marker Types

```rust
use std::marker::PhantomData;

// Capability markers — zero-cost type-level flags
pub struct Raw;
pub struct Sanitized;

pub struct UserInput<State> {
    value: String,
    _state: PhantomData<State>,
}

impl UserInput<Raw> {
    pub fn new_raw(s: &str) -> Self {
        Self { value: s.to_string(), _state: PhantomData }
    }

    pub fn sanitize(self) -> UserInput<Sanitized> {
        let sanitized = sanitize_html(&self.value);
        UserInput { value: sanitized, _state: PhantomData }
    }
}

// Can only render after sanitization
impl UserInput<Sanitized> {
    pub fn render(&self) -> String {
        format!("<div>{}</div>", self.value)
    }
}
```

### PhantomData

```rust
use std::marker::PhantomData;

// Type that acts like it owns a &'a T (but doesn't)
struct Iter<'a, T> {
    ptr: *const T,
    _marker: PhantomData<&'a T>,  // Tells borrow checker about lifetime
}

// Variance marker
struct MyCell<T> {
    value: UnsafeCell<T>,
    _marker: PhantomData<*mut T>,  // Invariant over T
}
```

`PhantomData<&'a T>` is covariant over `'a` and `T`. `PhantomData<*const T>` is also covariant. If you need invariance, use something like `PhantomData<*mut T>` or `PhantomData<fn(T) -> T>`.

## Decision Guide

| Need | Pattern |
|------|---------|
| Type safety for primitives | Newtype |
| Compile-time state validation | Type State |
| Lifetime/variance markers | PhantomData |
| Capability flags | Marker Type / Trait |
| Gradual construction | Builder |
| Closed set of impls | Sealed Trait |
| Zero-sized type marker | ZST `struct MyMarker;` |

## Anti-Patterns

| Anti-Pattern | Why Bad | Better |
|--------------|---------|--------|
| Boolean flags for states | Runtime errors | Type state |
| String for semantic types | No type safety | Newtype with validation |
| `Option` for always-present fields | Unclear invariant | Remove `Option` |
| Public fields with invariants | Invariant violation | Private + validated constructor |

## Related References

- **Up:** [12-domain-modeling](12-domain-modeling.md) for DDD concepts
- **Down:** [04-zero-cost](04-zero-cost.md) for trait design
