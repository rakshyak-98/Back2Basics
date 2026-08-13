<!-- note-strategy: operational -->
[[Data structure]] [[ADT (Abstract Data Type)]]

# array

> An array is a contiguous block of same-size slots — index `i` means `base + i * size` (that’s why zero-based is natural).

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Random access O(1); insert/delete in the middle is O(n) because you shift elements.

```txt
base → [0][1][2]…[n-1]   address(i) = base + i*elem_size
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Contiguous** | Neighbors in memory | “Great cache locality.” |
| **Zero-based** | First offset is 0 | “No extra subtract in address math.” |
| **Dynamic array** | Resizable buffer | “Amortized append O(1).” |
| **vs linked list** | Trade access vs insert | “Arrays win reads; lists win middle insert.” |

---

## Standard config / commands

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

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| OOB / segfault | index vs length | Validate bounds |
| Slow inserts | middle splice loop | Use better structure |
| Memory blow | huge sparse use | Map/dict instead |
| Off-by-one | loop `<= n` | Prefer half-open `[lo, hi)` |

---

## Gotchas

> [!WARNING]
> **JS “arrays” are objects** — holes and mixed types change performance.

> [!WARNING]
> **Assuming O(1) insert** — only at the end for dynamic arrays.

---

## When NOT to use

- **Frequent middle insert/delete** — list / gap buffer / rope.
- **Sparse keys** — hash map.

## Related

[[ADT (Abstract Data Type)]] [[linked list]] [[Data structure]]
