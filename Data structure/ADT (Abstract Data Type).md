[[Data structure]] [[Data structure]] [[array]] [[DSA algorithms]]

# ADT (Abstract Data Type)

> An ADT describes behavior (ops + rules) — not the concrete bytes in memory.

```txt
        ADT (Abstract Data ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Why It Matters
- **Key signal:** ADTs show you can separate *what* operations mean from *how* they are stored

## Sources
- [Wikipedia — Abstract data type](https://en.wikipedia.org/wiki/Abstract_data_type) — overview
- [CLRS — Introduction to Algorithms (ADT framing)](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/) — deep-dive

## Key Concepts
```txt
ADT (what)  →  data structure (how)
Stack.push/pop  →  array or linked list
```

### Review map (words you can say)

| Word | Plain meaning | Say in review |
|------|---------------|------------------|
| **Interface** | Allowed operations | “push/pop/peek only.” |
| **Invariant** | Must always hold | “LIFO for stack.” |
| **Encapsulation** | Hide representation | “Callers don’t see nodes.” |
| **Complexity** | Cost of ops | “Pick impl for the hot op.” |

## Technical Details
```text
Stack ADT: push, pop, peek, isEmpty
Queue ADT: enqueue, dequeue, front
Map ADT: get, set, delete, contains
```

| Knob | Why it matters |
|------|----------------|
| Op set | Wrong ADT = awkward code |
| Complexity table | Review + prod choice |
| Thread-safety | Not in classic ADT — add explicitly |

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| API leaks nodes | encapsulation broken | Return values/copies |
| Wrong complexity | using list as array | Swap implementation |
| Invariant broken | peek empty | Define empty behavior |
| “ADT too slow” | bad impl | Profile; change structure |

## Mistakes to Avoid
- **Mistake:** Naming ADT as the impl
- **Mistake:** Mutating through leaked internals — breaks invariants silently

## Pros/Cons or Trade-offs
- **Trade-off:** One-off scripts — concrete arrays are fine.
- **Trade-off:** When the representation *is* the product — e.g. teaching memory layouts.
