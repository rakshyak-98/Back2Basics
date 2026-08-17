[[Design pattern]] [[Design pattern/Factory Method]] [[Design pattern/Dependency Injection]]

# Singleton

> A Singleton guarantees one instance of a class and a global access point — useful for scarce resources, but it hides dependencies and complicates testing.

```txt
        Singleton ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Pitfalls
               ├── Trade-offs
               └── Use cases
```

## Interview Relevance
- **Interview probes:** Singleton is a classic trap question

## Sources
- Gamma et al., *Design Patterns* (Singleton) — deep-dive

## Key Concepts
- **Note:** Some objects should exist exactly once in a process: configuration registries…

```
Caller → getInstance() → returns cached instance
              ↓
         (first call creates; later calls reuse)
```

- **Note:** The constructor is hidden (private or module-scoped)

| Approach | Mechanism | Risk |
|----------|-----------|------|
| Static property | `static instance` on class | Instance may be reachable and replaceable |
| Lazy initialization | Create on first `getInstance()` | Thread safety needs locks or `sync.Once` |
| Enum singleton (Java) | Single enum constant | Cleanest in Java; not portable |
| Module singleton | One export from a module file | Natural in Node/Go packages |

- **Note:** In concurrent code, two threads calling `getInstance()` simultaneously can cr…

## Mistakes to Avoid
- **Mistake:** Treating Singleton as default for "only one needed"
- **Mistake:** Assuming process Singleton means cluster-wide uniqueness

## Pros/Cons or Trade-offs
Singleton is often criticized because it is **global state** dressed as a pattern:

- **Testing** — hard to substitute fakes; tests share state across cases.
- **Hidden dependencies** — callers do not declare they need the singleton.
- **Lifecycle** — unclear when the instance is torn down.

Modern designs often prefer **dependency injection** ([[Design pattern/Dependency Injection]]) or plain module-level variables with explicit wiring.

- "We might only need one" — use a normal object and inject it once at startup.
- Distributed systems

## Real-World Applications
- **True single-resource:** True single-resource constraints (file descriptor to one device).
- **Performance-critical caches:** Performance-critical caches where one shared instance is required.
