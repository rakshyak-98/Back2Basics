[[Data structure]] [[Data structure]]

# ADT (Abstract Data Type)

> An ADT describes behavior (ops + rules) — not the concrete bytes in memory.

---

## How it works

```txt
ADT (what)  →  data structure (how)
Stack.push/pop  →  array or linked list
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Interface** | Allowed operations | “push/pop/peek only.” |
| **Invariant** | Must always hold | “LIFO for stack.” |
| **Encapsulation** | Hide representation | “Callers don’t see nodes.” |
| **Complexity** | Cost of ops | “Pick impl for the hot op.” |

---


## Configuration and commands

```text
Stack ADT: push, pop, peek, isEmpty
Queue ADT: enqueue, dequeue, front
Map ADT: get, set, delete, contains
```

| Knob | Why it matters |
|------|----------------|
| Op set | Wrong ADT = awkward code |
| Complexity table | Interview + prod choice |
| Thread-safety | Not in classic ADT — add explicitly |

---


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| API leaks nodes | encapsulation broken | Return values/copies |
| Wrong complexity | using list as array | Swap implementation |
| Invariant broken | peek empty | Define empty behavior |
| “ADT too slow” | bad impl | Profile; change structure |

---


## Gotchas

> [!WARNING]
> **Naming ADT as the impl** — “we used a Stack” doesn’t say array vs list costs.

> [!WARNING]
> **Mutating through leaked internals** — breaks invariants silently.

---


## When not to use

- **One-off scripts** — concrete arrays are fine.
- **When the representation *is* the product** — e.g. teaching memory layouts.


## Related

[[Data structure]] [[array]] [[DSA algorithms]]

## Sources

- [Wikipedia — ADT](https://en.wikipedia.org/wiki/ADT)
