<!-- note-strategy: operational -->
[[Data structure]] [[DSA algorithms]] [[array]]

# Sorting algorithm

> Sorting puts elements in order — pick by stability, memory, and whether data is almost sorted.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Comparison sorts need ≥ O(n log n) worst case; counting/radix win on limited keys; timsort exploits runs.

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

---

## Standard config / commands

```js
arr.sort((a, b) => a - b) // know if stable in your runtime
// interview classics: merge, quick, heap, counting
```

| Knob | Why it matters |
|------|----------------|
| Comparator | Must be consistent |
| Key type | Integers → counting/radix possible |
| Partial sort | heapq / nth_element |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Unstable tie break | need stable | Stable sort or decorate keys |
| Worst-case blowup | naive quicksort | Use library / introsort |
| Wrong order | comparator bug | Antisymmetry checks |
| Too slow | O(n²) on large n | n log n algorithm |

---

## Gotchas

> [!WARNING]
> **JS sort without comparator** — lexicographic on strings; numbers need `(a,b)=>a-b`.

> [!WARNING]
> **“Quicksort always n log n”** — adversarial pivots → n² unless mitigated.

---

## When NOT to use

- **Already sorted stream** — maintain a structure instead.
- **Need order stats only** — quickselect / heap, not full sort.

## Related

[[DSA algorithms]] [[array]] [[algo/binary search]]
