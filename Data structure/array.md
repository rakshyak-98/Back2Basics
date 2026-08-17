[[Data structure]] [[ADT (Abstract Data Type)]] [[linked list]]

# array

> An array is a contiguous block of same-size slots — index `i` means `base + i * size` (that’s why zero-based is natural).

```txt
        array ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Why It Matters
- **Key signal:** Arrays are the baseline structure

## Sources
- [Wikipedia — Array data structure](https://en.wikipedia.org/wiki/Array_(data_structure)) — overview
- [CS 61B — Arrays](https://sp18.datastructur.es/) — overview

## Key Concepts
```txt
base → [0][1][2]…[n-1]   address(i) = base + i*elem_size
```

### Review map (words you can say)

| Word | Plain meaning | Say in review |
|------|---------------|------------------|
| **Contiguous** | Neighbors in memory | “Great cache locality.” |
| **Zero-based** | First offset is 0 | “No extra subtract in address math.” |
| **Dynamic array** | Resizable buffer | “Amortized append O(1).” |
| **vs linked list** | Trade access vs insert | “Arrays win reads; lists win middle insert.” |

## Technical Details
```js
const a = [10, 20, 30]
a.push(40)        // end
a.splice(1, 0, 15) // middle insert — shifts
```

| Knob | Why it matters |
|------|----------------|
| Capacity growth | Realloc cost |
| Typed arrays | Dense numeric data |
| Bounds checks | Safety vs speed |

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| OOB / segfault | index vs length | Validate bounds |
| Slow inserts | middle splice loop | Use better structure |
| Memory blow | huge sparse use | Map/dict instead |
| Off-by-one | loop `<= n` | Prefer half-open `[lo, hi)` |

## Mistakes to Avoid
- **Mistake:** JS “arrays” are objects
- **Mistake:** Assuming O(1) insert — only at the end for dynamic arrays

## Pros/Cons or Trade-offs
- **Trade-off:** Frequent middle insert/delete — list / gap buffer / rope.
- **Trade-off:** Sparse keys — hash map.
