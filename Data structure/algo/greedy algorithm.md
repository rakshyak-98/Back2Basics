[[Data structure/algo/binary search]] [[Data structure/dsa genera formula]]

# Greedy algorithm

> Locally optimal choice at each step — works when problem has **greedy choice property** and **optimal substructure**; otherwise wrong answer with confidence.

## Mental model

At each step, pick the best-looking option now without backtracking. Fast (often O(n log n) from sorting). Proof burden is on you: exchange argument or matroid. Classic wins: interval scheduling, Huffman, Dijkstra (non-negative weights), activity selection.

```
Sort/preprocess → for each step pick max profit / min finish time / closest fit
```

## Standard config / commands

### Activity selection (max non-overlapping intervals)

```js
function maxActivities(intervals) {
  intervals.sort((a, b) => a[1] - b[1]); // earliest finish
  let count = 0, end = -Infinity;
  for (const [s, e] of intervals) {
    if (s >= end) { count++; end = e; }
  }
  return count;
}
```

### Coin change (when greedy works — canonical denominations)

```js
const coins = [25, 10, 5, 1]; // US coins — greedy OK
function minCoins(amount) {
  let n = 0;
  for (const c of coins) {
    n += Math.floor(amount / c);
    amount %= c;
  }
  return amount === 0 ? n : -1;
}
```

### When greedy fails (use DP)

```js
// coins [1, 3, 4], amount 6 → greedy gives 4+1+1=3 coins; optimal 3+3=2
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Wrong on hidden tests | Counterexample | Switch to DP; prove greedy first |
| TLE | Wrong sort key | Greedy usually O(n log n); avoid nested scan |
| Suboptimal path | Graph negative edges | Dijkstra fails — Bellman-Ford |
| Interval bug | Sort by wrong endpoint | Activity: sort by **finish** time |
| Knapsack wrong | Fractional vs 0/1 | Fractional greedy by value/weight; 0/1 needs DP |

## Gotchas

> [!WARNING]
> **Coin change** — greedy only for canonical systems; general case is NP-hard (DP).
>
> **Looks right on samples** — greedy failures need crafted cases in review.
>
> **Stable sort matters** — tie-breaking can change interval results.

## When NOT to use

- Don't greedy 0/1 knapsack or general coin change without proof.
- Don't skip proof in interview — state why greedy safe or pivot to DP.

## Related

[[Data structure/algo/binary search]] [[Data structure/dsa genera formula]] [[Data structure/sliding window]]
