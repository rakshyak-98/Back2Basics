[[Design pattern]] [[Design pattern/Factory Method]] [[Design pattern/Creation pattern/Abstract Factory]]

# Builder

> Builder separates **construction of a complex object** from its representation — so the same assembly steps can build different variants without a telescoping constructor.





## Interview Relevance
Builder interviews cover telescoping constructors, fluent steps, validation at build(), and how Builder differs from Factory Method.

## Sources
- Gamma et al., *Design Patterns* (Builder) — deep-dive

## Key Concepts
Objects with many optional fields invite constructors like `new House(3, true, false, "brick", null, …)`. Each new option multiplies overloads. Builder accumulates steps and validates before `build()`.

```
Director (optional) → Builder.setX().setY().build() → Product
```

| Role | Responsibility |
|------|----------------|
| **Builder** | Step methods + `build()` |
| **Product** | Immutable or fully configured object |
| **Director** (optional) | Fixed recipe of builder calls |

## Technical Details
```go
type QueryBuilder struct { sql string }
func (b *QueryBuilder) Select(cols string) *QueryBuilder { ...; return b }
func (b *QueryBuilder) From(table string) *QueryBuilder { ...; return b }
func (b *QueryBuilder) Build() (string, error) { ... }
```

## Real-World Applications
- Many optional parameters with validation rules (HTTP requests, SQL, config objects).
- Different representations from same process (JSON vs XML document builders).

## Comparison
**vs other patterns**

- **Factory Method / Abstract Factory** — create whole product in one shot; Builder **stages** assembly.
- **Prototype** — clone existing instance; Builder **constructs from scratch** via steps.

## Mistakes to Avoid
- Simple objects — a struct literal or named constructor is enough.
- Mutable builders returned to multiple callers — document whether steps are reusable or single-shot.
