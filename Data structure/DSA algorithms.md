[[Data structure]] [[dsa intuition]] [[Sorting algorithm]]

# DSA algorithms

> DSA algorithms are named techniques on data structures — pick by constraints, not by fashion.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Map the problem to a pattern (scan, two pointers, binary search, BFS/DFS, DP, greedy) then prove complexity.

```txt
constraints → pattern → structure → code → edges
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Brute → optimal** | Correct then faster | “Show both if asked.” |
| **Trade space** | Hash for speed | “O(n) memory for O(n) time.” |
| **Graph vs array** | Modeling choice | “Edges become adjacency.” |
| **Stable sort** | Equal keys keep order | “When ties matter.” |

---

## Standard config / commands

```text
n ≤ 20        → exponential / bit DP OK
n ≤ 1e5       → O(n log n) or better
need kth      → heap / quickselect
shortest path → BFS (unweighted) / Dijkstra
```

| Knob | Why it matters |
|------|----------------|
| n, m sizes | Kill wrong Big-O |
| Online vs offline | Streaming constraints |
| Mutability | In-place asks |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| TLE | Big-O vs n | Better pattern |
| MLE | huge DP table | Compress state |
| WA | edges | empty, overflow, dups |
| Can’t start | no model | Draw examples |

---

## Gotchas

> [!WARNING]
> **Memorizing code without the invariant** — one tweak and you’re stuck.

> [!WARNING]
> **Ignoring constraints** — O(n²) on 1e5 is dead on arrival.

---

## When NOT to use

- **CRUD application without hot path** — clarity over clever DSA.
- **When library sort/search suffices** — don’t reimplement.

## Related

[[Sorting algorithm]] [[algo/binary search]] [[algo/Two pointer]] [[dsa intuition]]
