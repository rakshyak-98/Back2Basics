[[Prefix sum]] [[sliding window]] [[dsa modular arithmetics]] [[Algorithm]]

# DSA combinatorics formulas

> High-frequency counting formulas for interviews and complexity sanity checks — not a substitute for understanding *why* the formula applies.

## Mental model

Many DSA problems reduce to **counting objects** (subarrays, pairs, paths) or **bounding work** (max operations). These closed forms avoid brute-force enumeration.

```
Substrings in string length n:     n(n+1)/2     (choose start × end)
Pairs from n items:                n(n-1)/2     (unordered)
Subsets of n elements:             2^n
Permutations of n distinct:        n!
```

Always verify: **distinct vs identical**, **ordered vs unordered**, **contiguous vs any subsequence**.

## Standard config / commands

### Subarrays / substrings (contiguous)

| Object | Count | Notes |
|--------|-------|-------|
| Subarrays of array length `n` | `n(n+1)/2` | Includes length 1..n |
| Substrings of string length `n` | `n(n+1)/2` | Same formula |
| Subarrays of fixed length `k` | `n - k + 1` | Slide window |
| Subarrays with sum property | Often `prefix + hash map`, not closed form | See [[Prefix sum]] |

### Pairs and combinations

| Object | Count |
|--------|-------|
| Unordered pairs from `n` | `n(n-1)/2` |
| Ordered pairs | `n²` |
| Choose `k` from `n` | `C(n,k) = n! / (k!(n-k)!)` |
| Anagrams with repeats | `n! / (f1! f2! …)` — `fi` = freq of char i |

### Binary / decision trees

| Object | Count |
|--------|-------|
| Subsets of `n` elements | `2^n` |
| Bitmasks 0..2^n-1 | Iterate `for (mask = 0; mask < 1<<n; mask++)` |
| Nodes in full binary tree height `h` | `2^(h+1) - 1` |

### Graph basics

| Object | Formula |
|--------|---------|
| Handshaking lemma (undirected) | `sum(deg) = 2|E|` |
| Max edges simple undirected | `n(n-1)/2` |
| Tree edges | `n - 1` for connected tree |

### Complexity shortcuts

| Pattern | Typical complexity |
|---------|-------------------|
| Nested loops `i`, `j=i..n` | O(n²) — triangular number n(n+1)/2 iterations |
| Sort + two pointers | O(n log n) |
| [[sliding window]] | O(n) — each pointer moves ≤ n |
| Binary search on answer | O(n log W) or O(log n × cost(check)) |
| Dijkstra | O((V+E) log V) with binary heap |

### Modular counts

When output is mod `10^9+7`:

```js
// (n choose k) mod MOD — use precomputed fact/modinv, not raw factorial
// See [[dsa modular arithmetics]]
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Formula gives huge number vs expected | Ordered vs unordered confused | Re-derive with n=3 example |
| Off by 1 on subarray count | Empty subarray included/excluded? | Problem usually excludes empty |
| 2^n TLE | n > 20–22 | Need DP or math closed form, not bitmask枚举 |
| n! overflow | n > 20 in 64-bit | Use BigInt or modular factorial |
| C(n,k) wrong for large n,k | Cancel before multiply | Use multiplicative formula with mod inverse |

## Gotchas

> [!WARNING]
> **`n(n+1)/2` is substrings, not subsequences** — subsequence count is exponential (2^n) for binary choice per position.

> [!WARNING]
> **Duplicate elements** — distinct substring count ≠ n(n+1)/2; need suffix structures or rolling hash with set.

> [!WARNING]
> **Interview "formula" questions** — state assumptions aloud (distinct? contiguous?) before plugging numbers.

## When NOT to use

- **Problem has constraint structure** — e.g. "subarrays with sum divisible by k" needs prefix mod + frequency, not n(n+1)/2.
- **Replacing proof with memorization** — formulas are sanity checks; derive from small n on whiteboard if unsure.

## Related

[[Prefix sum]] [[sliding window]] [[dsa modular arithmetics]] [[Algorithm]] [[Data structure]]
