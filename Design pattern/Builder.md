[[Design pattern]] [[Design pattern/Factory Method]] [[Design pattern/Creation pattern/Abstract Factory]]

# Builder

> Builder separates **construction of a complex object** from its representation — so the same assembly steps can build different variants without a telescoping constructor.

## Problem

Objects with many optional fields invite constructors like `new House(3, true, false, "brick", null, …)`. Each new option multiplies overloads. Builder accumulates steps and validates before `build()`.

```
Director (optional) → Builder.setX().setY().build() → Product
```

## Parts

| Role | Responsibility |
|------|----------------|
| **Builder** | Step methods + `build()` |
| **Product** | Immutable or fully configured object |
| **Director** (optional) | Fixed recipe of builder calls |

## Fluent builder (common in Java/Go)

```go
type QueryBuilder struct { sql string }
func (b *QueryBuilder) Select(cols string) *QueryBuilder { ...; return b }
func (b *QueryBuilder) From(table string) *QueryBuilder { ...; return b }
func (b *QueryBuilder) Build() (string, error) { ... }
```

## vs other patterns

- **Factory Method / Abstract Factory** — create whole product in one shot; Builder **stages** assembly.
- **Prototype** — clone existing instance; Builder **constructs from scratch** via steps.

## When it helps

- Many optional parameters with validation rules (HTTP requests, SQL, config objects).
- Different representations from same process (JSON vs XML document builders).

## Pitfalls

- Simple objects — a struct literal or named constructor is enough.
- Mutable builders returned to multiple callers — document whether steps are reusable or single-shot.

## Sources

- Gamma et al., *Design Patterns* (Builder)
- [Builder pattern — Wikipedia](https://en.wikipedia.org/wiki/Builder_pattern)
