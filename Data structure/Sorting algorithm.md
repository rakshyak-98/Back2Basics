[[Data structure]] [[DSA algorithms]] [[array]] [[algo/binary search]]

# Sorting algorithm

> Sorting puts elements in order — pick by stability, memory, and whether data is almost sorted.

## Interview Relevance

Sorting interviews check stability, average vs worst case, and when n log n is enough vs counting/radix.

## Sources

- [Wikipedia — Sorting algorithm](https://en.wikipedia.org/wiki/Sorting_algorithm) — overview
- [MIT 6.006 — Sorting](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/) — deep-dive

## Key Concepts

```txt
input → (compare | count keys) → ordered output
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Stable** | Equal keys keep order | “Needed for multi-key sorts.” |
| **In-place** | Little extra memory | “Heapsort yes; mergesort usually no.” |
| **Adaptive** | Faster on nearly sorted | “Insertion / timsort.” |
| **n log n barrier** | Comparison lower bound | “Unless you exploit key structure.” |

## Technical Details

```js
arr.sort((a, b) => a - b) // know if stable in your runtime
// interview classics: merge, quick, heap, counting
```

| Knob | Why it matters |
|------|----------------|
| Comparator | Must be consistent |
| Key type | Integers → counting/radix possible |
| Partial sort | heapq / nth_element |

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| Unstable tie break | need stable | Stable sort or decorate keys |
| Worst-case blowup | naive quicksort | Use library / introsort |
| Wrong order | comparator bug | Antisymmetry checks |
| Too slow | O(n²) on large n | n log n algorithm |

## Pros/Cons or Trade-offs

- **Trade-off:** Already sorted stream — maintain a structure instead.
- **Trade-off:** Need order stats only — quickselect / heap, not full sort.

## Mistakes to Avoid

- JS sort without comparator — lexicographic on strings; numbers need `(a,b)=>a-b`.
- “Quicksort always n log n” — adversarial pivots → n² unless mitigated.
