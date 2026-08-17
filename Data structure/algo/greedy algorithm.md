[[Data structure/algo/binary search]] [[Data structure/dsa genera formula]] [[Data structure/sliding window]]

# Greedy algorithm

> Locally optimal choice at each step — works when problem has **greedy choice property** and **optimal substructure**; otherwise wrong answer with confidence.

```txt
        Greedy algorithm ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Why It Matters
- **Key signal:** Greedy questions test whether you can prove a local choice is safe

## Sources
- [Wikipedia — Greedy algorithm](https://en.wikipedia.org/wiki/Greedy_algorithm) — overview
- [CLRS — Greedy algorithms](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/) — deep-dive

## Key Concepts
- **Note:** At each step, pick the best-looking option now without backtracking

```
- **Note:** Sort/preprocess → for each step pick max profit / min finish time / closest f…
```

## Technical Details
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

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| Wrong on hidden tests | Counterexample | Switch to DP; prove greedy first |
| TLE | Wrong sort key | Greedy usually O(n log n); avoid nested scan |
| Suboptimal path | Graph negative edges | Dijkstra fails — Bellman-Ford |
| Interval bug | Sort by wrong endpoint | Activity: sort by **finish** time |
| Knapsack wrong | Fractional vs 0/1 | Fractional greedy by value/weight; 0/1 needs DP |

## Mistakes to Avoid
- **Mistake:** Coin change — greedy only for canonical systems

## Pros/Cons or Trade-offs
- **Trade-off:** Don't greedy 0/1 knapsack or general coin change without proof.
- **Trade-off:** Don't skip proof in review — state why greedy safe or pivot to DP.
