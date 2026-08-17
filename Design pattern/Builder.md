[[Design pattern]] [[Design pattern/Factory Method]] [[Design pattern/Creation pattern/Abstract Factory]]

# Builder

> Builder separates **construction of a complex object** from its representation — so the same assembly steps can build different variants without a telescoping constructor.

```txt
        Builder ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Builder interviews cover telescoping constructors, fluent steps, validation a…

## Sources
- Gamma et al., *Design Patterns* (Builder) — deep-dive

## Key Concepts
- **Note:** Objects with many optional fields invite constructors like `new House(3, true…

```
- **Note:** Director (optional) → Builder.setX().setY().build() → Product
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

## Mistakes to Avoid
- **Mistake:** Simple objects — a struct literal or named constructor is enough
- **Mistake:** Mutable builders returned to multiple callers

## Comparison
- **vs other patterns**

- **Factory Method / Abstract Factory**
- **Prototype** — clone existing instance; Builder **constructs from scratch** via steps.


### Use cases
- Many optional parameters with validation rules (HTTP requests, SQL, config objects).
- Different representations from same process (JSON vs XML document builders).
