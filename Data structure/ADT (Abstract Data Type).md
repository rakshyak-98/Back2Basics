[[Data structure]] [[Data structure]] [[array]] [[DSA algorithms]]

# ADT (Abstract Data Type)

> An ADT describes behavior (ops + rules) — not the concrete bytes in memory.

## Interview Relevance

ADTs show you can separate *what* operations mean from *how* they are stored — interviewers use this to frame complexity and API contracts.

## Sources

- [Wikipedia — Abstract data type](https://en.wikipedia.org/wiki/Abstract_data_type) — overview
- [CLRS — Introduction to Algorithms (ADT framing)](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/) — deep-dive

## Key Concepts

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

## Technical Details

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

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| API leaks nodes | encapsulation broken | Return values/copies |
| Wrong complexity | using list as array | Swap implementation |
| Invariant broken | peek empty | Define empty behavior |
| “ADT too slow” | bad impl | Profile; change structure |

## Pros/Cons or Trade-offs

- **Trade-off:** One-off scripts — concrete arrays are fine.
- **Trade-off:** When the representation *is* the product — e.g. teaching memory layouts.

## Mistakes to Avoid

- Naming ADT as the impl — “we used a Stack” doesn’t say array vs list costs.
- Mutating through leaked internals — breaks invariants silently.
