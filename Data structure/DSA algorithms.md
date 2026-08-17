[[Data structure]] [[dsa intuition]] [[Sorting algorithm]] [[algo/binary search]] [[algo/Two pointer]]

# DSA algorithms

> DSA algorithms are named techniques on data structures — pick by constraints, not by fashion.

```txt
        DSA algorithms ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Why It Matters
- **Key signal:** Named algorithm families (two pointers, sliding window, DFS/BFS, DP) are how …

## Sources
- [LeetCode Explore — Review patterns](https://leetcode.com/explore/) — overview
- [MIT 6.006](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/) — deep-dive

## Key Concepts
```txt
constraints → pattern → structure → code → edges
```

### Review map (words you can say)

| Word | Plain meaning | Say in review |
|------|---------------|------------------|
| **Brute → optimal** | Correct then faster | “Show both if asked.” |
| **Trade space** | Hash for speed | “O(n) memory for O(n) time.” |
| **Graph vs array** | Modeling choice | “Edges become adjacency.” |
| **Stable sort** | Equal keys keep order | “When ties matter.” |

## Technical Details
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

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| TLE | Big-O vs n | Better pattern |
| MLE | huge DP table | Compress state |
| WA | edges | empty, overflow, dups |
| Can’t start | no model | Draw examples |

## Mistakes to Avoid
- **Mistake:** Memorizing code without the invariant
- **Mistake:** Ignoring constraints — O(n²) on 1e5 is dead on arrival

## Pros/Cons or Trade-offs
- **Trade-off:** CRUD application without hot path — clarity over clever DSA.
- **Trade-off:** When library sort/search suffices — don’t reimplement.
