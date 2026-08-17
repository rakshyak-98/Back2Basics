[[Data structure]] [[sliding window]] [[dsa problem solving Scaffold]] [[Prefix sum]]

# Two pointer

> Two pointers walk a sequence from ends or in tandem — linear passes instead of nested loops when order helps.

```txt
        Two pointer ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Why It Matters
- **Key signal:** Two pointers compress O(n²) scans when order or a monotonic invariant allows

## Sources
- [Wikipedia — Two-pointer technique (algorithmic pattern)](https://en.wikipedia.org/wiki/Two_pointers_technique) — overview
- [NeetCode — Two Pointers](https://neetcode.io/practice) — overview

## Key Concepts
```txt
L →→→    ←←← R     or    L,R both →→ (fast/slow, window)
```

### Review map (words you can say)

| Word | Plain meaning | Say in review |
|------|---------------|------------------|
| **Opposite ends** | sorted pair/sum | “Shrink from the large side.” |
| **Same direction** | remove dups / windows | “Read & write pointers.” |
| **Fast/slow** | cycle detection | “Floyd.” |
| **Invariant** | what stays true | “Say it every move.” |

## Technical Details
```js
// two-sum on sorted
let l = 0, r = a.length - 1
while (l < r) {
  const s = a[l] + a[r]
  if (s === t) return [l, r]
  if (s < t) l++
  else r--
}
```

| Knob | Why it matters |
|------|----------------|
| Sorted? | Opposite-end needs order |
| `l < r` vs `<=` | Duplicates / mid |
| Monotonic window | Sliding window cousin |

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| Infinite loop | pointer never moves | Ensure progress each branch |
| Missed pairs | duplicates | Skip dups deliberately |
| Wrong on unsorted | used opposite ends | Sort copy or other pattern |
| Off-by-one | bounds | Draw array + indices |

## Mistakes to Avoid
- **Mistake:** Two pointers ≠ always O(n)
- **Mistake:** Mutating while iterating — read/write pointers need clear roles

## Pros/Cons or Trade-offs
- **Trade-off:** Unordered hashable pair without sort need — hash set may be simpler.
- **Trade-off:** Graph problems — BFS/DFS, not array pointers.
