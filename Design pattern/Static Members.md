[[Design pattern]] [[Design pattern/OOPS]] [[Design pattern/Abstraction]]

# Static Members

> Static members belong to the type itself, not to any instance — shared constants, factory hooks, and singleton holders live here, but static overuse creates hidden global state.

```txt
        Static Members ──┬── Interview
               ├── Sources
               ├── Mechanism
               ├── Pitfalls
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Static member questions probe shared mutable state, testability, and when ins…

## Sources
- Java Language Specification — static members — deep-dive

## Technical Details
- **Class-level vs instance-level:** 

```typescript
class Counter {
  static total = 0      // one value for all instances
  count = 0             // per instance
}
```

- Static methods cannot access instance fields without an instance reference.

- **Common uses:** 

| Use | Example |
|-----|---------|
| Constants | `Math.PI`, enum-like `static readonly` |
| Factory / utility | `Date.parse()`, `Vector.zero()` |
| Singleton holder | `getInstance()` on class |
| Counters / registries | Process-wide metrics (careful with tests) |

- **Language notes:** 

- **Java/C#:** — `static` fields and methods explicit.
- **JavaScript/TypeScript:** — `static` on class; module-level `const` often replaces class statics.
- **Go:** — no class statics; package-level variables and functions.
- **Rust:** — associated functions on `impl` (`String::from`).

## Mistakes to Avoid
- **Mistake:** **Global mutable statics** — race conditions and test pollution
- **Mistake:** **Static abuse for "helpers"**
- **Mistake:** **method shadowing**

## Comparison
- **vs Singleton**

- Static accessors on a class often implement [[Design pattern/Singleton]]
