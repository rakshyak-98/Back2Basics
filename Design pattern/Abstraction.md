[[Design pattern]] [[Design pattern/OOPS]] [[Design pattern/Private Properties and Methods]]

# Abstraction

> Abstraction exposes only the behaviors callers need through a defined interface, hiding implementation detail behind that boundary.

## Mental model

**Say it in one breath:** Callers depend on the interface, not the concrete class — you can swap implementations without changing consumer code.

- Users interact through a **well-defined interface** and see only the operations you expose.
- Additional methods may exist on the concrete class, but they stay hidden from consumers.
- Functional languages achieve the same idea with function composition instead of abstract classes.

> [!INFO]
> Functional programming languages support abstraction through functions and modules; they do not require abstract classes.

> [!NOTE]
> In functional style, behavior is often passed as a function rather than inherited — data plus functions, composed at call sites.

## Standard config / commands

```typescript
interface Storage {
  get(key: string): Promise<string | null>;
  set(key: string, value: string): Promise<void>;
}

class RedisStorage implements Storage { /* ... */ }
class InMemoryStorage implements Storage { /* ... */ }
```

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| Leaky abstraction | Consumers import concrete types | Depend on interface only |
| Interface too wide | Unused methods on impl | Split interfaces (interface segregation) |
| Test doubles hard to write | Concrete deps in constructors | Inject interface; mock in tests |

## Gotchas

> [!WARNING]
> **God interfaces** — every new method breaks all implementers; keep surfaces small.

## When NOT to use

- **Single implementation, no variation** — a plain class is enough; do not abstract prematurely.

## Related

[[Design pattern/OOPS]] [[Design pattern/Private Properties and Methods]] [[Design pattern/Strategy pattern]]
