[[Design pattern]] [[Design pattern/Factory Method]] [[Design pattern/Dependency Injection]]

# Singleton

> A Singleton guarantees one instance of a class and a global access point — useful for scarce resources, but it hides dependencies and complicates testing.

## What it solves

Some objects should exist exactly once in a process: configuration registries, connection pools, hardware interfaces, or logging sinks tied to a single output stream. Singleton centralizes creation so callers cannot accidentally instantiate duplicates.

## How it works

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

## Thread safety

In concurrent code, two threads calling `getInstance()` simultaneously can create two instances unless creation is synchronized. Prefer language primitives (`std::call_once`, Java enum, Go `sync.Once`) over ad-hoc locking.

## Trade-offs

Singleton is often criticized because it is **global state** dressed as a pattern:

- **Testing** — hard to substitute fakes; tests share state across cases.
- **Hidden dependencies** — callers do not declare they need the singleton.
- **Lifecycle** — unclear when the instance is torn down.

Modern designs often prefer **dependency injection** ([[Design pattern/Dependency Injection]]) or plain module-level variables with explicit wiring.

## When to use

- True single-resource constraints (file descriptor to one device).
- Performance-critical caches where one shared instance is required.

## When to skip

- "We might only need one" — use a normal object and inject it once at startup.
- Distributed systems — each process has its own instance; a Singleton does not coordinate cluster-wide uniqueness.

## Sources

- Gamma et al., *Design Patterns* (Singleton)
- [Singleton pattern — Wikipedia](https://en.wikipedia.org/wiki/Singleton_pattern) (cross-checked with GoF)
