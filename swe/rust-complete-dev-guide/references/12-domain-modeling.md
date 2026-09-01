# 12 — Domain Modeling (DDD in Rust)

> **Core Question:** *What is this concept's role in the domain?*

## Domain Concepts → Rust Patterns

| DDD Concept | Rust Pattern | Ownership Implication |
|-------------|--------------|----------------------|
| **Entity** | Struct with ID field | Owned, unique identity via ID |
| **Value Object** | Struct with `Clone`/`Copy` | Shareable, immutable by value |
| **Aggregate Root** | Struct owns children | Clear ownership tree |
| **Repository** | Trait | Abstracts persistence |
| **Domain Event** | Enum | Captures state changes |
| **Domain Service** | `impl` block / free fn | Stateless operations |

## Entity vs Value Object

```rust
// ENTITY — identity matters
#[derive(Debug)]
struct User {
    id: UserId,         // Identity-defining field
    email: Email,       // Can change, not identity
    name: String,
}

impl PartialEq for User {
    fn eq(&self, other: &Self) -> bool {
        self.id == other.id  // Compare by identity only
    }
}

// VALUE OBJECT — interchangeable by value
#[derive(Debug, Clone, PartialEq)]
struct Email(String);

impl Email {
    pub fn new(s: &str) -> Result<Self, ValidationError> {
        if !s.contains('@') {
            return Err(ValidationError("invalid email"));
        }
        Ok(Self(s.to_string()))
    }
}
```

## Aggregate Pattern

```rust
// Aggregate root — single entry point, enforces invariants
mod order {
    pub struct Order {
        id: OrderId,
        items: Vec<OrderItem>,  // Owned children
        status: OrderStatus,
        total: Amount,
    }

    impl Order {
        pub fn add_item(&mut self, item: OrderItem) -> Result<(), Error> {
            // Enforce aggregate invariants:
            // - Can't add items to shipped/cancelled orders
            // - Can't exceed max items
            if !self.status.can_modify() {
                return Err(Error::OrderFinalized);
            }
            self.items.push(item);
            self.recalculate_total();
            Ok(())
        }

        pub fn submit(self) -> SubmittedOrder {
            // State transition: consume Order, produce SubmittedOrder
            SubmittedOrder {
                id: self.id,
                items: self.items,
                total: self.total,
            }
        }

        fn recalculate_total(&mut self) {
            self.total = self.items.iter()
                .map(|i| i.price * i.quantity as f64)
                .sum();
        }
    }
}
```

## Repository Pattern

```rust
// Repository trait — abstracts data access
#[async_trait]
pub trait UserRepository: Send + Sync {
    async fn find_by_id(&self, id: UserId) -> Result<Option<User>, DbError>;
    async fn find_by_email(&self, email: &Email) -> Result<Option<User>, DbError>;
    async fn save(&self, user: &User) -> Result<(), DbError>;
    async fn delete(&self, id: UserId) -> Result<(), DbError>;
}

// Implementation — concrete database logic
pub struct PostgresUserRepository {
    pool: sqlx::PgPool,
}

#[async_trait]
impl UserRepository for PostgresUserRepository {
    async fn find_by_id(&self, id: UserId) -> Result<Option<User>, DbError> {
        sqlx::query_as("SELECT * FROM users WHERE id = $1", id.0)
            .fetch_optional(&self.pool)
            .await
            .map_err(DbError::from)
    }

    async fn save(&self, user: &User) -> Result<(), DbError> {
        sqlx::query("INSERT INTO users (id, email, name) VALUES ($1, $2, $3) ON CONFLICT (id) DO UPDATE SET email = $2, name = $3",
            user.id.0, user.email.as_ref(), user.name)
            .execute(&self.pool)
            .await?;
        Ok(())
    }
    // ...
}
```

## Domain Events

```rust
#[derive(Debug, Clone)]
pub enum OrderEvent {
    Created { order_id: OrderId, customer_id: CustomerId },
    ItemAdded { order_id: OrderId, item: OrderItem },
    Submitted { order_id: OrderId, total: Amount },
    Cancelled { order_id: OrderId, reason: String },
}
```

## Common Mistakes

| Mistake | Why Wrong | Better |
|---------|-----------|--------|
| Primitive obsession | No type safety | Newtype wrappers for domain concepts |
| Public fields with invariants | Invariants can be violated | Private fields + validated constructors |
| Leaked aggregate internals | Broken encapsulation | All access via aggregate root |
| `String` for domain types | No validation | Validated newtypes |
| Entity comparison by value | Wrong equality semantics | Compare by identity (ID field) |

## Anti-Patterns

| Anti-Pattern | Why Bad | Better |
|--------------|---------|--------|
| God struct (everything in one type) | Unmaintainable | Split into aggregates |
| Anemic domain model | Business logic scattered | Rich domain model with methods |
| Exposing internal collections | Break invariants | Return immutable views |
| `Clone` for entities | Unclear intent, cost | Explicit methods |

## Related References

- **Up:** [05-type-driven](05-type-driven.md) for implementation patterns
- **Down:** [01-ownership](01-ownership.md) for aggregate ownership, [06-error-handling](06-error-handling.md) for domain errors
- **Domain:** Each domain has specific modeling rules
