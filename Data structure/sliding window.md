[[Prefix sum]] [[Data structure]] [[Algorithm]]

# Sliding window

> Two-pointer technique over a contiguous subarray/substring — turn O(n²) brute force into O(n) by expanding/shrinking one window instead of restarting from every index.

## Mental model

Maintain indices `left` and `right` defining window `[left, right]`. Advance `right` to grow; advance `left` to shrink when a **validity invariant** breaks (sum too large, duplicate char seen, etc.).

```
arr:  [ 2, 1, 5, 1, 3, 2 ]     target sum ≤ 7
           L     R
      expand R → sum grows
      if invalid → increment L until valid again
      track best answer at each valid step
```

Two flavors:
- **Fixed-size window** — length `k` given; slide `L` and `R` together.
- **Variable-size window** — maximize/minimize length subject to constraint.

Works when the problem asks: *longest/shortest subarray/substring such that …* or *count subarrays where …* (sometimes needs prefix sum + hash map instead).

## Standard config / commands

### Template — variable window (longest substring without repeating char)

```js
function lengthOfLongestSubstring(s) {
  const last = new Map();
  let left = 0, best = 0;

  for (let right = 0; right < s.length; right++) {
    const ch = s[right];
    if (last.has(ch) && last.get(ch) >= left) {
      left = last.get(ch) + 1; // shrink from left
    }
    last.set(ch, right);
    best = Math.max(best, right - left + 1);
  }
  return best;
}
```

### Fixed window size k (max sum of k elements)

```js
function maxSumSubarray(arr, k) {
  let windowSum = 0;
  for (let i = 0; i < k; i++) windowSum += arr[i];
  let best = windowSum;

  for (let right = k; right < arr.length; right++) {
    windowSum += arr[right] - arr[right - k]; // slide
    best = Math.max(best, windowSum);
  }
  return best;
}
```

### Monotonic contribution (sum / count constraint)

```js
// Smallest subarray with sum >= target (positive integers)
function minSubArrayLen(target, nums) {
  let left = 0, sum = 0, best = Infinity;
  for (let right = 0; right < nums.length; right++) {
    sum += nums[right];
    while (sum >= target) {
      best = Math.min(best, right - left + 1);
      sum -= nums[left++];
    }
  }
  return best === Infinity ? 0 : best;
}
```

### When window doesn't apply — use [[Prefix sum]]

```js
// Count subarrays with sum exactly k (can include negatives)
// Prefix sum + hash map frequency — not sliding window
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Wrong answer on edge cases | Empty array, all negatives, single element | Handle `n === 0`; pick correct algorithm (window vs prefix sum) |
| Off-by-one length | Inclusive `[L,R]` vs half-open `[L,R)` | Standardize: length = `R - L + 1` for inclusive |
| Infinite loop on shrink | `left` not advancing when invalid | Ensure `left++` each shrink iteration |
| TLE on large input | Nested loops resetting `left` to 0 each `right` | `left` only moves forward — total O(n) |
| Works for positives, fails with negatives | Monotonic shrink assumption broken | Switch to prefix sum + hash map |
| Count subarrays off by one | Count at shrink vs expand step | Define whether each valid window counted once |

## Gotchas

> [!WARNING]
> **Non-negative numbers assumption** — "minimum window with sum ≥ target" needs positive values (or non-decreasing contribution). Negative values break monotonic shrink.

> [!WARNING]
> **`left` never goes backward** — except rare jump tricks (character map). If you reset `left = 0` every time, you're back to O(n²).

> [!WARNING]
> **Distinct vs at-most-k** — "at most 2 distinct" uses shrink-on-invalid; "exactly 2 distinct" often needs `atMost(k) - atMost(k-1)`.

> [!WARNING]
> **String vs array indexing** — same logic; watch Unicode code points vs UTF-16 code units for emoji substrings.

## When NOT to use

- **Subsequence (non-contiguous)** — window requires contiguous segment; use DP or two-pointer on sorted arrays differently.
- **Arbitrary numeric targets with negatives** — use [[Prefix sum]] + hash map.
- **Global optimization without contiguous constraint** — e.g. max subarray sum with one deletion — may need Kadane variant, not pure window.

## Related

[[Prefix sum]] [[Data structure]] [[Algorithm]] [[dsa genera formula]]
