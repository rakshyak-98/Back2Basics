<!-- note-strategy: operational -->
[[Data structure]] [[sliding window]] [[dsa problem solving Scaffold]]

# Two pointer

> Two pointers walk a sequence from ends or in tandem — linear passes instead of nested loops when order helps.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Move the pointer that can still fix the invariant (sum too big → move right-end left on sorted arrays).

```txt
L →→→    ←←← R     or    L,R both →→ (fast/slow, window)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Opposite ends** | sorted pair/sum | “Shrink from the large side.” |
| **Same direction** | remove dups / windows | “Read & write pointers.” |
| **Fast/slow** | cycle detection | “Floyd.” |
| **Invariant** | what stays true | “Say it every move.” |

---

## Standard config / commands

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

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Infinite loop | pointer never moves | Ensure progress each branch |
| Missed pairs | duplicates | Skip dups deliberately |
| Wrong on unsorted | used opposite ends | Sort copy or other pattern |
| Off-by-one | bounds | Draw array + indices |

---

## Gotchas

> [!WARNING]
> **Two pointers ≠ always O(n)** — if you binary search inside, say the real cost.

> [!WARNING]
> **Mutating while iterating** — read/write pointers need clear roles.

---

## When NOT to use

- **Unordered hashable pair without sort need** — hash set may be simpler.
- **Graph problems** — BFS/DFS, not array pointers.

## Related

[[sliding window]] [[Prefix sum]] [[dsa problem solving Scaffold]]
