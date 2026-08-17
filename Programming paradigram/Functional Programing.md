[[purely declarative]] [[Design pattern/Strategy pattern]]

# Functional programming

> Compose pure functions and immutable data — minimize shared mutable state so behavior is easier to test, reason about, and parallelize.





## Interview Relevance
Interviewers want purity, immutability, higher-order functions, and honest trade-offs vs imperative code — not buzzwords.

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

## Real-World Applications
Reducers, data transforms in ETL, React render functions as pure with respect to props/state inputs.

**Example:** Move date formatting and pricing math into pure helpers; keep DB writes in adapters.

## Pros/Cons or Trade-offs
- **Pro:** Testability and safer concurrency stories.
- **Con:** Naive deep-copy immutability can hurt performance; learn structural sharing tools.

## Comparison
- vs OOP: FP centers values/transforms; OOP centers objects/messages — hybrids are normal.
- vs [[purely declarative]]: FP is a paradigm; declarative UI/config is one application style.

## Mistakes to Avoid
- Claiming “we are functional” while mutating global arrays everywhere.
- Overusing monadic jargon in interviews without concrete examples.
- Copying huge structures on every update without need.
