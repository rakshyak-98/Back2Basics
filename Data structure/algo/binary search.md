[[Data structure/dsa genera formula]] [[Data structure/sliding window]] [[Data structure/Prefix sum]]

# Binary search

> Halve sorted search space each step — O(log n) find/insert boundary; loop invariant is the hard part.

## Mental model

Requires **sorted** array or monotonic predicate. Maintain window `[left, right]` where answer lies. Mid compares eliminate half. Two variants: **exact match** vs **lower/upper bound** (first position where condition holds). Off-by-one on `left <= right` vs `left < right` causes infinite loops or missed answers.

```
sorted: [1,3,5,7,9]  target 7
  L=0 R=4 mid=2 val=5 → go right
  L=3 R=4 mid=3 val=7 → found
```

## Standard config / commands

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

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Infinite loop | `lo`/`hi` update | Use `lo + (hi-lo)/2`; ensure range shrinks |
| Wrong index | `<=` vs `<` | Exact: `lo<=hi`; bound: half-open `[lo,hi)` |
| -1 always | Not sorted | Sort first or binary search on index space |
| Off by one | Post-condition | Verify `lo` at exit equals intended bound |
| TLE on "sorted" | Not monotonic predicate | Prove monotonicity before binary search |

## Gotchas

> [!WARNING]
> **`(lo + hi) / 2` overflow** — use `lo + ((hi - lo) >> 1)` in other languages.
>
> **Duplicates** — lower vs upper bound return different indices.
>
> **Search on rotated array** — modified invariant; don't paste vanilla template.

## When NOT to use

- Don't binary search unsorted data without transformation.
- Don't use when n < ~50 — linear scan simpler and cache-friendly.

## Related

[[Data structure/dsa genera formula]] [[Data structure/algo/greedy algorithm]] [[Data structure/linked list]]
