[[Functional Programing]] [[Descriptive/Mermaid (DSL)]] [[flutter widget]]

# Purely declarative

> Describe the desired result, not the step-by-step mutations — the runtime figures out how to reach that state (UI, infra, queries).

## Interview Relevance

Interviewers contrast imperative loops/mutations with declarative UI (React/Flutter), SQL, and IaC — and want limits (debugging, leaky abstractions).

## Sources

- [Wikipedia — Declarative programming](https://en.wikipedia.org/wiki/Declarative_programming) — overview

## Key Concepts

- **Imperative:** statements change state in order.
- **Declarative:** specify what; engine supplies how.
- **Examples:** SQL queries, React/Flutter widget trees, Kubernetes manifests, CSS layout.
- **Escape hatches:** still drop to imperative for performance or awkward edges.

## Technical Details

```txt
Imperative: for each item, mutate array, update DOM node…
Declarative: UI = f(state); SQL = filter/join projection
```

| Style | Example |
|-------|---------|
| Imperative | Manual DOM updates |
| Declarative | `return <List items={items} />` |
| Hybrid | Declarative UI + imperative event handlers |

## Real-World Applications

React components declare UI from state; React reconciler patches the DOM. Terraform declares cloud resources; providers apply diffs.

**Example:** Rewrite nested jQuery DOM tweaks as state → render — bugs shrink to state mistakes.

## Pros/Cons or Trade-offs

- **Pro:** Less local bookkeeping; easier to see intent.
- **Con:** Harder to debug when the engine’s “how” surprises you.

## Comparison

- vs [[Functional Programing]]: FP often enables declarative style but is not identical.
- vs configs/DSLs: declarative does not mean “no code” — it means “no manual how” when possible.

## Mistakes to Avoid

- Calling any YAML “declarative” while embedding imperative scripts everywhere.
- Fighting the framework with deep imperative DOM/state hacks.
- Assuming declarative means zero performance cost.
