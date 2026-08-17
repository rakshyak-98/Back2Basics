[[Data structure/dsa genera formula]] [[Data structure/sliding window]] [[Data structure/Prefix sum]] [[Data structure/algo/greedy algorithm]] [[Data structure/linked list]]

# Binary search

> Binary search — requires sorted array or monotonic predicate. Maintain window [left, right] where answer lies. Mid compares eliminate half. Two variants: exact match vs lower/upper

```txt
        Binary search ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Why It Matters
- **Key signal:** Binary search reviews fail on boundary conditions

## Sources
- [Wikipedia — Binary search algorithm](https://en.wikipedia.org/wiki/Binary_search_algorithm) — overview
- [CP-Algorithms — Binary search](https://cp-algorithms.com/numerics/binary-search.html) — deep-dive

## Key Concepts
- **Note:** Requires **sorted** array or monotonic predicate

```
sorted: [1,3,5,7,9]  target 7
  L=0 R=4 mid=2 val=5 → go right
  L=3 R=4 mid=3 val=7 → found
```

## Technical Details
### Exact match (classic)

```js
function binarySearch(arr, target) {
  let lo = 0, hi = arr.length - 1;
  while (lo <= hi) {
    const mid = lo + ((hi - lo) >> 1);
    if (arr[mid] === target) return mid;
    if (arr[mid] < target) lo = mid + 1;
    else hi = mid - 1;
  }
  return -1;
}
```

### Lower bound (first >= target)

```js
function lowerBound(arr, target) {
  let lo = 0, hi = arr.length;   // half-open [lo, hi)
  while (lo < hi) {
    const mid = lo + ((hi - lo) >> 1);
    if (arr[mid] < target) lo = mid + 1;
    else hi = mid;
  }
  return lo;
}
```

### Predicate on answer (binary search on answer)

```js
// smallest x such that ok(x) is true, monotonic false→true
let lo = 0, hi = 1e9;
while (lo < hi) {
  const mid = lo + ((hi - lo) >> 1);
  if (ok(mid)) hi = mid;
  else lo = mid + 1;
}
```

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| Infinite loop | `lo`/`hi` update | Use `lo + (hi-lo)/2`; ensure range shrinks |
| Wrong index | `<=` vs `<` | Exact: `lo<=hi`; bound: half-open `[lo,hi)` |
| -1 always | Not sorted | Sort first or binary search on index space |
| Off by one | Post-condition | Verify `lo` at exit equals intended bound |
| TLE on "sorted" | Not monotonic predicate | Prove monotonicity before binary search |

## Mistakes to Avoid
- **Mistake:** `(lo + hi) / 2` overflow

## Pros/Cons or Trade-offs
- **Trade-off:** Don't binary search unsorted data without transformation.
- **Trade-off:** Don't use when n < ~50 — linear scan simpler and cache-friendly.
