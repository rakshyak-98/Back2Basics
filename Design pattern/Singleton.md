[[Design pattern]] [[Design pattern/Factory Method]] [[Design pattern/Dependency Injection]]

# Singleton

> A Singleton guarantees one instance of a class and a global access point — useful for scarce resources, but it hides dependencies and complicates testing.





## Interview Relevance
Singleton is a classic trap question — interviewers want thread safety, testability pain, and when dependency injection is better.

## Sources
- Gamma et al., *Design Patterns* (Singleton) — deep-dive

## Key Concepts
Some objects should exist exactly once in a process: configuration registries, connection pools, hardware interfaces, or logging sinks tied to a single output stream. Singleton centralizes creation so callers cannot accidentally instantiate duplicates.

```
Caller → getInstance() → returns cached instance
              ↓
         (first call creates; later calls reuse)
```

The constructor is hidden (private or module-scoped). A static method or closure holds the sole instance. Languages differ:

| Approach | Mechanism | Risk |
|----------|-----------|------|
| Static property | `static instance` on class | Instance may be reachable and replaceable |
| Lazy initialization | Create on first `getInstance()` | Thread safety needs locks or `sync.Once` |
| Enum singleton (Java) | Single enum constant | Cleanest in Java; not portable |
| Module singleton | One export from a module file | Natural in Node/Go packages |

In concurrent code, two threads calling `getInstance()` simultaneously can create two instances unless creation is synchronized. Prefer language primitives (`std::call_once`, Java enum, Go `sync.Once`) over ad-hoc locking.

## Real-World Applications
- True single-resource constraints (file descriptor to one device).
- Performance-critical caches where one shared instance is required.

## Pros/Cons or Trade-offs
Singleton is often criticized because it is **global state** dressed as a pattern:

- **Testing** — hard to substitute fakes; tests share state across cases.
- **Hidden dependencies** — callers do not declare they need the singleton.
- **Lifecycle** — unclear when the instance is torn down.

Modern designs often prefer **dependency injection** ([[Design pattern/Dependency Injection]]) or plain module-level variables with explicit wiring.

- "We might only need one" — use a normal object and inject it once at startup.
- Distributed systems — each process has its own instance; a Singleton does not coordinate cluster-wide uniqueness.

## Mistakes to Avoid
- Treating Singleton as default for "only one needed" — inject a normal object once at startup instead.
- Assuming process Singleton means cluster-wide uniqueness — each process has its own instance.
