[[purely declarative]] [[Design pattern/Strategy pattern]]

# Functional programming

> Compose pure functions and immutable data — minimize shared mutable state so behavior is easier to test, reason about, and parallelize.

```txt
        Functional program ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers want purity, immutability, higher-order functions, and honest tr…

## Sources
- [Wikipedia — Functional programming](https://en.wikipedia.org/wiki/Functional_programming) — overview
- [HaskellWiki — Functional programming](https://wiki.haskell.org/Functional_programming) — deep-dive

## Key Concepts
- **Pure function:** same inputs → same outputs; no side effects.
- **Immutability:** prefer new values over in-place edits.
- **HOFs:** `map`/`filter`/`reduce`, functions as values.
- **Composition:** small functions pipe into pipelines.
- **Controlled effects:** isolate I/O at the edges.

## Technical Details
```js
const total = items
  .filter((i) => i.active)
  .map((i) => i.price)
  .reduce((a, b) => a + b, 0);
```

| Idea | Why it matters |
|------|----------------|
| Referential transparency | Replace expression with value safely |
| Avoid shared mutable state | Fewer race bugs |
| Pure core | Unit test without mocks for I/O |

## Mistakes to Avoid
- **Mistake:** Claiming “we are functional” while mutating global arrays everyw…
- **Mistake:** Overusing monadic jargon in interviews without concrete examples
- **Mistake:** Copying huge structures on every update without need

## Pros/Cons or Trade-offs
- **Pro:** Testability and safer concurrency stories.
- **Con:** Naive deep-copy immutability can hurt performance; learn structural sharing tools.

## Comparison
- vs OOP: FP centers values/transforms; OOP centers objects/messages — hybrids are normal.
- vs [[purely declarative]]: FP is a paradigm; declarative UI/config is one application style.


### Use cases
- Reducers, data transforms in ETL, React render functions as pure with respect…

- **Example:** Move date formatting and pricing math into pure helpers
