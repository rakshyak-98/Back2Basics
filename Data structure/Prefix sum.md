[[sliding window]] [[Data structure]] [[Algorithm]]

# Prefix sum

> Precomputed cumulative totals — answer any fixed-range sum query in O(1) after O(n) preprocess; foundation for range queries, subarray counts, and difference arrays.

## Mental model

Build array `P` where `P[i]` = sum of `arr[0..i]` (0-indexed). Range sum `[l, r]` = `P[r] - P[l-1]` (define `P[-1] = 0`).

```
arr:     2   4   1   3
P:     2   6   7  10

sum(1..2) = P[2] - P[0] = 7 - 2 = 5  (4 + 1)
```

Extensions:
- **2D prefix sum** — rectangle query in O(1).
- **Prefix sum + hash map** — count subarrays with sum `k` (handles negatives).
- **Difference array** — inverse of prefix sum for range updates.

## Standard config / commands

### 1D build and query

```js
function buildPrefix(arr) {
  const P = new Array(arr.length);
  P[0] = arr[0];
  for (let i = 1; i < arr.length; i++) P[i] = P[i - 1] + arr[i];
  return P;
}

function rangeSum(P, l, r) {
  return P[r] - (l > 0 ? P[l - 1] : 0);
}
```

### Count subarrays with sum exactly k (with negatives)

```js
function subarraySum(nums, k) {
  const freq = new Map([[0, 1]]); // prefix sum → count
  let sum = 0, count = 0;
  for (const x of nums) {
    sum += x;
    count += freq.get(sum - k) ?? 0;
    freq.set(sum, (freq.get(sum) ?? 0) + 1);
  }
  return count;
}
```

### Prefix + binary search (non-negative arrays)

```js
// Smallest subarray length with sum >= target — also solvable via [[sliding window]]
// Binary search on prefix when monotonic
```

### 2D prefix (grid)

```js
// P[r][c] = sum of rectangle (0,0) to (r,c)
// Query (r1,c1)-(r2,c2) in O(1) with inclusion-exclusion
```

### Difference array (range add)

```js
// Add v to [l, r]: diff[l] += v; diff[r+1] -= v
// Apply prefix sum to diff → final array after all range updates
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Off-by-one on range | 0-index vs 1-index; inclusive bounds | Use `P[r] - P[l-1]` with `l=0` base case |
| Integer overflow | Large sums in JS BigInt / other langs | Use BigInt or modulo if problem requires |
| Wrong subarray count | Missing initial `{0:1}` in hash map | Empty prefix represents sum before index 0 |
| 2D query wrong | Inclusion-exclusion order | Draw rectangle diagram; verify four corners |
| TLE with many queries | Rebuilding prefix per query | Preprocess once; each query O(1) |
| Sliding window used on negatives | Monotonic assumption | Switch to prefix + hash map |

## Gotchas

> [!WARNING]
> **Empty subarray** — count problems often need `prefix 0` seeded once in the map.

> [!WARNING]
> **Modulo arithmetic** — `(P[r] - P[l-1]) % MOD` can go negative; add MOD before final `%`. See [[dsa modular arithmetics]].

> [!WARNING]
> **Immutable vs mutable array** — if source array updates, prefix must rebuild or use Fenwick/segment tree for dynamic queries.

> [!WARNING]
> **"Elements ≤ value" queries** — often sort + prefix on sorted array, not raw prefix on unsorted.

## When NOT to use

- **Non-contiguous subsequence sums** — prefix sum assumes contiguous ranges.
- **Dynamic point/range updates with interleaved queries** — use Fenwick tree or segment tree.
- **Only single full-array sum** — plain loop is simpler; don't over-engineer.

## Related

[[sliding window]] [[dsa genera formula]] [[dsa modular arithmetics]] [[Data structure]]
