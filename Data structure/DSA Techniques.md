> [!INFO] Overlapping sub-problems cause exponential time complexity `O(2^n)`
> - if you see repeated sub-problems, think [[Memoization (Top-Down DP)]] 

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

# Sliding window
useful for solving problems involving contiguous subarray or sub-strings efficiently by avoiding redundant computations. Instead of using a brute-force `O(n^2)` approach, it efficiently slides a window over the input to achieve `O(n)` complexity.
## Fixed size window -> size is predetermined
- complexity -> time `O(n)` / space `O(1)`.
### algorithm
- initialize two pointers `left=0` and `right=0`
- expand `right` until the window reaches size `k`.
- compute result `sum` `max` etc.
- slide the window by moving `left` and `right` together.

## Variable size window -> window expands or shrinks dynamically based on constraints
- used when the window size is not fixed and depends on conditions
### algorithm
- expand `right` until the condition is met. 
- contract `left` while the condition remains valid.
- keep track of the best answer.

## Dynamic sliding window (Two Pointers)
used when the window must be adjusted dynamically based on a condition. (Find the longest substring without repeating characters)
### algorithm
- expand `right` and store characters in a hashmap.
- if a duplicate exists, shrink `left` until it's valid.
- track the longest valid window.

## Sliding window with frequency count
used when dealing with counting elements inside a dynamic window (anagram matching).