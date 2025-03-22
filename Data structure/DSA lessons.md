Overlapping sub-problems cause exponential time complexity `O(2^n)`
- if you see repeated sub-problems, think [[Memoization (Top-Down DP)]]

### Memoization (Optimized recursion)
- store results in a hashmap time `O(n)` and space `O(n)`
- convert naive recursion into [[Memoization (Top-Down DP)]] to optimize.

### Tabulation (Bottom-up DP)
- start from `n=1` and `n=2` and build up using iteration.
- time complexity `O(n)` space `O(n)`
- if recursion was too much space, flip it into [[Bottom-UP DP]]

### Space optimized fibonacci
- instead of storing `O(n)` results, only keep track of the last two values.
- time complexity `O(n)` space complexity `O(1)`
- if a problem follows fibonacci recurrence, reduce it to a two-variable approach.

### Matrix exponentiation
- converts fibonacci relation into matrix multiplication.
- if a recurrence is linear, consider Matrix Exponentiation for `O(log n)` time.