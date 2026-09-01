# 04 — Zero-Cost Abstractions (Generics & Dispatch)

> **Core Question:** *Do we need compile-time or runtime polymorphism?*

## Dispatch Comparison

| Pattern | Dispatch | Code Size | Runtime Cost | Use When |
|---------|----------|-----------|--------------|----------|
| `fn foo<T: Trait>()` | Static (monomorphized) | +bloat per type | Zero | Types known at compile |
| `fn foo(x: &dyn Trait)` | Dynamic (vtable) | Minimal | Single vtable lookup | Types unknown until runtime |
| `impl Trait` return | Static | +bloat per type | Zero | Return opaque type |
| `Box<dyn Trait>` | Dynamic | Minimal | Allocation + vtable | Owned trait object |

## Decision Guide

```
Type known at compile time?
├─ Yes → Need heterogeneous collection?
│         ├─ Yes → Closed set? → enum
│         │         └─ Open set → Vec<Box<dyn Trait>>
│         └─ No → Generics / impl Trait
└─ No → dyn Trait

Performance critical?
├─ Yes → Generics (monomorphization)
└─ No → dyn Trait (faster compile, smaller binary)
```

## Syntax Comparison

```rust
// STATIC DISPATCH — type resolved at compile time

// Generic function
fn process<T: Display>(x: T) { println!("{x}"); }

// impl Trait (sugar for generic)
fn process(x: impl Display) { println!("{x}"); }

// Return position (opaque type)
fn get_default() -> impl Display { 42 }

// DYNAMIC DISPATCH — type resolved at runtime

// Reference to trait object
fn process(x: &dyn Display) { println!("{x}"); }

// Owned trait object
let obj: Box<dyn Handler> = Box::new(MyHandler);

// Heterogeneous collection
let handlers: Vec<Box<dyn Handler>> = vec![
    Box::new(EmailHandler),
    Box::new(SmsHandler),
];
```

## Object Safety

A trait is **object-safe** (can be used as `dyn Trait`) if ALL methods:
- Don't return `Self`
- Don't have generic type parameters
- Don't have `Self: Sized` bounds
- Are not `const` functions

```rust
// Object-safe — can be used as dyn Trait
trait Handler: Send + Sync {
    fn handle(&self, req: &Request) -> Response;
}

// NOT object-safe — can't be dyn Trait
trait Clone {
    fn clone(&self) -> Self;  // Returns Self!
}

trait FromStr {
    fn from_str(s: &str) -> Self;  // Returns Self!
}

// Fix: make non-object-safe methods conditional
trait Safe {
    fn method(&self);
    fn clone_me(&self) -> Self
    where
        Self: Sized;  // Only available when type is known
}
```

## When to Use Each

| Scenario | Choose | Why |
|----------|--------|-----|
| Performance-critical hot path | Generics | Zero runtime overhead |
| Heterogeneous collection | `dyn Trait` | Different types in one container |
| Plugin/extension architecture | `dyn Trait` | Unknown types at compile time |
| API boundary (library) | `impl Trait` or generics | Caller flexibility |
| Reduce compile times | `dyn Trait` | Less monomorphization |
| Small, known type set | `enum` | No indirection, exhaustive |

## Enum as Alternative

```rust
// Often better than dyn Trait for closed type sets
enum Shape {
    Circle(f64),
    Rectangle(f64, f64),
    Triangle(f64, f64, f64),
}

impl Shape {
    fn area(&self) -> f64 {
        match self {
            Shape::Circle(r) => std::f64::consts::PI * r * r,
            Shape::Rectangle(w, h) => w * h,
            Shape::Triangle(b, h) => 0.5 * b * h,
        }
    }
}
```

## Anti-Patterns

| Anti-Pattern | Why Bad | Better |
|--------------|---------|--------|
| Over-generic everything | Slow compile, complex code | Concrete types when possible |
| `dyn` for known types | Unnecessary indirection | Generics |
| Complex trait hierarchies | Hard to understand | Simple design |
| Ignoring object safety | Limits future flexibility | Plan for `dyn` if needed |

## Related References

- **Up:** [05-type-driven](05-type-driven.md) for type-level patterns
- **Down:** [07-concurrency](07-concurrency.md) for Send/Sync bounds, [09-performance](09-performance.md)
