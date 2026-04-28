[169 majority-element](https://leetcode.com/problems/majority-element/)
- pair different elements and discard them.
- only the majority element can remain at the end, because it's more frequent than all others combined.
- Boyer-Moore Majority Vote Algorithm.

---

[3494 Find the Minimum Amount of Time to Brew Potions](https://leetcode.com/problems/find-the-minimum-amount-of-time-to-brew-potions)

---

[977 Squares of sorted array](https://leetcode.com/problems/squares-of-a-sorted-array/description/)
- fill backward(end), two pointers start and end.
- if array is not sorted two pointers approach breaks - because it assumes order around 0.

---

[118 Pascal's Triangle](https://leetcode.com/problems/pascals-triangle/)

---

[2273 Find Resultant Array After Removing Anagrams](https://leetcode.com/problems/find-resultant-array-after-removing-anagrams)

---

[15 3Sum](https://leetcode.com/problems/3sum/)
- Now it’s the **2-Sum** problem with target `-a`.  
- Known trick: sort + two-pointer
- Reduce to 2-sum -> `b + c = -a`
- Outer loop fix `i`  
- Inner while find pairs via 2-pointer

---

[Game of Life](https://leetcode.com/problems/game-of-life/description/)
- the eight coordinate pairs represent all possible moves from a cell in a grid.
	- they enumerate exactly 8 directions around a cell.

---

[Contiguous Array](https://leetcode.com/problems/contiguous-array/description/)
- Given a binary array `nums`, return _the maximum length of a contiguous subarray with an equal number of_ `0` _and_ `1`.

- What we need to know is. Same prefix sum at two indices = balanced subarray between them
- Longest subarray with target sum -> prefix sum + hash map.

---

[Longest common prefix](https://leetcode.com/problems/longest-common-prefix/submissions/1894187919/?envType=problem-list-v2&envId=wrdcuh52)

- The longest common prefix can never be longer then the shortest string in the array.
- Think of the strings as columns in a table. We're checking if each "row" has all the identical values.

---

[Remove duplicate from sorted array](https://leetcode.com/problems/remove-duplicates-from-sorted-array/description/?envType=problem-list-v2&envId=wrdcuh52)

- Slow pointer (i) -> Tracks where to place the next unique element.
- Fast pointer (j) -> Scans through the array looking for new unique element.
- Compare with the last unique element we kept.

---

[Search Insert Position](https://leetcode.com/problems/search-insert-position/?envType=problem-list-v2&envId=wrdcuh52)

- Binary search -> Sorted array + `O(logn)` complexity

[Contains Duplicate II](https://leetcode.com/problems/contains-duplicate-ii/description/?envType=problem-list-v2&envId=wrdcuh52)

- find if there are duplicate values in the array that are close enough to each other.
- you need to check if any number appears twice in the array, and those two occurrence are at most `k` position apart.

- Maintain a sliding window of the last `k` element using a Set
- For Each element, check if it's already in the window (duplicate withing distance k)
- Add the current element to the window
- Remove the oldest element if the window exceeds size `k`

---

[Maximum product of three number](https://leetcode.com/problems/maximum-product-of-three-numbers/submissions/1923224246/?envType=problem-list-v2&envId=wrdcuh52)

- the maximum product of three numbers doesn't have to be from consecutive elements.

---

[Find All Numbers Disappeared in an Array](https://leetcode.com/problems/find-all-numbers-disappeared-in-an-array/?envType=problem-list-v2&envId=wrdcuh52)

> [!NOTE]
> Mark all the position negative by the `nums` array element. After that what ever the position is positive that are the missing number.

- `nums[i]` Gets the current number (could be positive or negative)
- `Math.abs(nums[i])` -> Gets the absolute value (removes the negative sing if present). Without this when we encounter a number that's already been marked negative, we'd get the wrong index.

```js
// WITHOUT Math.abs() - WRONG!
nums[2] = -2
const index = -2 - 1;  // index = -3 ❌ (negative index!)

// WITH Math.abs() - CORRECT!
nums[2] = -2
const index = Math.abs(-2) - 1;  // index = 1 ✓
```


**Why subtract 1:**

The problem uses numbers from **1 to n**, but array indices are **0 to n-1**:

```js
// Number 1 should mark index 0
Math.abs(1) - 1 = 0 ✓

// Number 4 should mark index 3
Math.abs(4) - 1 = 3 ✓

// Number 8 should mark index 7
Math.abs(8) - 1 = 7 ✓
```

[two sum](https://leetcode.com/problems/two-sum/?envType=problem-list-v2&envId=wrdcuh52)

- the problem gives you equation: `x + y = target` you are looking for `x` and `y`. When you are standing at any number `x` in the array, you don't need to search for `y`. You already know exactly what `y` must be.

>[!NOTE]
> To get below `O(n)^2`, I need to remember what I've seen. A Hash Map provides `O(1)` average time lookups.

- Common implementation Error
	- **The `0` Index Trap:** If you use a plain object `{}` instead of `Map`, and you check `if (seen[complement])`, it will fail if the index is `0` because `0` is **falsy** in JavaScript.

---

[Longest Common Prefix](https://leetcode.com/problems/longest-common-prefix/?envType=problem-list-v2&envId=wrdcuh52)

- 

---

Given an array of positive integers arr[], return the second largest element from the array. If the second largest element doesn't exist then return -1.

Note: The second largest element should not be equal to the largest element.

Examples:

Input: arr[] = [12, 35, 1, 10, 34, 1]
Output: 34
Explanation: The largest element of the array is 35 and the second largest element is 34.

Input: arr[] = [10, 5, 10]
Output: 5
Explanation: The largest element of the array is 10 and the second largest element is 5.

Input: arr[] = [10, 10, 10]
Output: -1
Explanation: The largest element of the array is 10 and the second largest element does not exist.

---
Given an array **arr[]**. Push all the zeros of the given array to the right end of the array while maintaining the order of non-zero elements. Do the mentioned change in the **array in place**.

**Examples:**

**Input:** arr[] = [1, 2, 0, 4, 3, 0, 5, 0]
**Output:** [1, 2, 4, 3, 5, 0, 0, 0]
**Explanation:** There are three 0s that are moved to the end.

**Input:** arr[] = [10, 20, 30]
**Output:** [10, 20, 30]
**Explanation:** No change in array as there are no 0s.

**Input:** arr[] = [0, 0]
**Output:** [0, 0]
**Explanation:** No change in array as there are all 0s.

**Constraints:**  
1 ≤ arr.size() ≤ 105  
0 ≤ arr[i] ≤ 105

---
You are given an array of integers **arr[]**. Your task is to **reverse** the given array.

**Examples:  
**

**Input:** arr = [1, 4, 3, 2, 6, 5]
**Output:** [5, 6, 2, 3, 4, 1]  
**Explanation:** The elements of the array are 1 4 3 2 6 5. After reversing the array, the first element goes to the last position, the second element goes to the second last position and so on. Hence, the answer is 5 6 2 3 4 1.

**Input**: arr = [4, 5, 2]
**Output:** [2, 5, 4]  
**Explanation:** The elements of the array are 4 5 2. The reversed array will be 2 5 4.  

**Input**: arr = [1]
**Output:** [1]  
**Explanation:** The array has only single element, hence the reversed array is same as the original.

**Constraints:  
**1<=arr.size()<=105  
0<=arr[i]<=105

---
Given an unsorted array _arr[]__**.**_ Rotate the array to the left (counter-clockwise direction) by _d_ steps, where _d_ is a positive integer. Do the mentioned change in the **array in place**.

Note: Consider the array as circular.

**Examples :  
**

**Input:** arr[] = [1, 2, 3, 4, 5], d = 2
**Output:** [3, 4, 5, 1, 2]
**Explanation:** when rotated by 2 elements, it becomes 3 4 5 1 2.

**Input:** arr[] = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20], d = 3
**Output:** [8, 10, 12, 14, 16, 18, 20, 2, 4, 6]
**Explanation:** when rotated by 3 elements, it becomes 8 10 12 14 16 18 20 2 4 6.  

**Input:** arr[] = [7, 3, 9, 1], d = 9
**Output:** [3, 9, 1, 7]
**Explanation:** when we rotate 9 times, we'll get 3 9 1 7 as resultant array.

**Constraints:**  
1 <= arr.size(), d <= 105  
0 <= arr[i] <= 105

---
Given an array of integers **arr[]** representing a permutation, implement the **next permutation** that rearranges the numbers into the lexicographically next greater permutation. If no such permutation exists, rearrange the numbers into the lowest possible order (i.e., sorted in ascending order). 

Note - A permutation of an array of integers refers to a specific arrangement of its elements in a sequence or linear order.

**Examples:**

**Input:** arr = [2, 4, 1, 7, 5, 0]
**Output:** [2, 4, 5, 0, 1, 7]
**Explanation:** The next permutation of the given array is {2, 4, 5, 0, 1, 7}.

**Input:** arr = [3, 2, 1]
**Output:** [1, 2, 3]
**Explanation:** As arr[] is the last permutation, the next permutation is the lowest one.  

**Input:** arr = [3, 4, 2, 5, 1]
**Output:** [3, 4, 5, 1, 2]
**Explanation:** The next permutation of the given array is {3, 4, 5, 1, 2}.

**Constraints:**  
1 ≤ arr.size() ≤ 105  
0 ≤ arr[i] ≤ 105

---

You are given an array of integer **arr[]** where each number represents a vote to a candidate. Return the candidates that have votes greater than **one-third** of the total votes, If there's **not** a majority vote, return an empty array. 

**Note:** The answer should be returned in an increasing format.

**Examples:**

**Input:** arr[] = [2, 1, 5, 5, 5, 5, 6, 6, 6, 6, 6]
**Output:** [5, 6]
**Explanation:** 5 and 6 occur more n/3 times.

**Input:** arr[] = [1, 2, 3, 4, 5]
**Output:** []  
**Explanation:** o candidate occur more than n/3 times.

**Constraint:**  
1 <= arr.size() <= 106  
-109 <= arr[i] <= 109

---

[pascal triangle 2](https://leetcode.com/problems/pascals-triangle-ii/?envType=problem-list-v2&envId=wrdcuh52)

- each interior element = sum of two element above it `triangle[i][j] = triangle[i-1][j-1] + triangle[i-1][j]`
- Pascal triangle is often taught as a 2D structure, but to solve it in `O(k)` space, you must treat it as a single array that updates itself in-place.

> [!NOTE]
> - **The "In-Place" Constraint:** If you update the array from left to right, you will overwrite the values you need for the next calculation.

> [!WARNING]
> If you build the whole triangle and just return the last row. That's `O(k^2)` space.

---

[Home many Numbers are smaller than the current number](https://leetcode.com/problems/how-many-numbers-are-smaller-than-the-current-number/description/)

- when we sort an array, we lose track of where element originally were
- Track original indices -> `const sorted = nums.map((num, idx) => [num, idx])`

- `[ [ 1, 2 ], [ 1, 4 ], [ 2, 1 ], [ 4, 3 ], [ 8, 0 ] ]` position in sorted array = count of smaller numbers

- Handling the duplicate correctly sort and keep the track of original index -> `row[originalIdx] = sorted[i-1][1]`


```js
// When duplicate found, copy result from first occurrence
if (i > 0 && sorted[i][0] === sorted[i-1][0]) {
    result[originalIdx] = result[sorted[i-1][1]];
}
```

### For Documentation:

> **Duplicate Handling Strategy:**  
> In a sorted array with index tracking, when a duplicate value is detected, the algorithm retrieves the result from the previous occurrence's original position rather than recalculating, ensuring consistency across all instances of the same value.

> "Since we're sorting but need results in original order, we track indices. For duplicates, we don't recalculate—we just copy what we already computed for the first instance of that value."

---

[Best time to buy and sell stock II](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-ii/?source=submission-ac)

- **The Signal:** "Single day to buy" and "different day in the future to sell."
- **The Logic:** As you walk through the array, at any given day, your best possible profit is:

```text
Current Price−Lowest Price Seen Previously
```

---

[island perimeter](https://leetcode.com/problems/island-perimeter/?envType=problem-list-v2&envId=wrdcuh52)

- this is [[Matrix Connectivity]] problem.
- When you see a grid and a "perimeter", stop thinking about maps and start thinking about Overlap logic.

- Each land cell(1) has 4 sides. But if a side touches another land cell, we don't count it. If you simply counted all lands cells and multiplied by 4, you would over-count because land cells share edges.

`Perimeter = (Total Land Cells x 4) - (Shared Edges x 2)`

Why multiply shared edges by 2?
Because a shared edge is "internal" to two different cells. You must subtract that edge from both cells.

The shared Edge Rule: I will iterate through every cell (1):
- if the current cell is `1`:
	- Add 4 to the perimeter
	- Check if the neighbor above is `1`. If yes, subtract 2.
	- Check if the neighbor to the left is `1`. If yes, subtract 2.

---

[next greater element 1](https://leetcode.com/problems/next-greater-element-i/description/?envType=problem-list-v2&envId=wrdcuh52)

- Monotonic stack problem
- For each element, use stack to find next greater element. Stack maintains element in decreasing order (bottom -> top) Monotonic stack mechanism. Element remain in stack until they find their next greater. Decreasing order ensures we catch all valid pairs.
- Store result in HashMap: element -> next greater. Element still in stack never found a larger element to their right.
- Query map for each element to lookup answer from HashMap and return precomputed result. This works because one is sub set of other.

---

[array_partition](https://leetcode.com/problems/array-partition/?envType=problem-list-v2&envId=wrdcuh52)

- bad pairing and good pairing
- put big cookies with big cookies, small cookies with small cookies. This way you don't waste big cookies by pairing them with tiny ones.

> [!NOTE]
> - If order doesn't matter in input and output doesn't depend on original indices -> sort first.
> Sorting cookies from small to big, pairing them with their neighbors, keeping every other cookie (this 1st, 3rd, 5th...) will give you the answer.

```text
[1, 4, 3, 2]

// bad pairing
1 with 4
	you keep 1
	you lose 4 (the big one)

// sort the array
[1, 2, 3, 4]

// good pairing
1 with 2
	you keep 1
	you only lose 2 (not so big)
	
3 with 4
	you keep 3
	you only lose 4

[1, 2] -> 1
[3, 4] -> 4

// you can keep sum of every other number
[1, 2, 3, 4]
1 + 3 => 4

```

> [!NOTE]
> - Look for problems where making the best choice at each step leads to best overall result.
> - Sorting data -> time complexity often dominated by O(n log n) sort, not the solution logic

---

[Distribute Candies](https://leetcode.com/problems/distribute-candies/?envType=problem-list-v2&envId=wrdcuh52)

> [!INFO]
> in the candy problem, recognizing it as a "maximize unique elements under a constraint" problem immediately points toward `Sets + Math.min`

- The key insight is that Alice can eat `n/2` candies, and we want to maximize the number of different she gets.
- **Identify the "Limit" Signal:** The doctor’s advice is a hard cap. It doesn't matter if there are 1,000 types of candies; if I can only eat 5, the answer is 5.
- **Floating Point Pitfalls:** While n is guaranteed to be even here, in other allocation problems, developers forget that `/ 2` can return a float in JS. Always use `Math.floor()` or bitwise `>> 1` if there is any chance of an odd n to avoid index errors or logic bugs. 
- **Memory Exhaustion (DoS Risk):** Creating a `Set` of 105 elements (the constraint limit) consumes significant heap memory. If this were a high-throughput production API, a senior dev might suggest **sorting in-place** (O(1) space, O(nlogn) time) instead of a `Set` (O(n) space, O(n) time) to prevent the process from crashing under memory pressure. 

**Constraints**
- she can only eat `n/2` candies so she can't have more than `n/2` different types.

> [!NOTE]
> This problem tests your ability to recognize a **Lower Bound**. You are looking for min(uniques,capacity). Candidates fail here when they try to actually "simulate" picking candies (using loops or sorting), which turns an O(n) problem into a complex `O(nlogn)` or `O(n2)` mess.

---

[Longest Harmonious Substring](https://leetcode.com/problems/longest-harmonious-subsequence/description/?envType=problem-list-v2&envId=wrdcuh52)

- Find the most frequent pair of numbers that differ by exactly 1, return their combined count.
- It's a subsequence element don't need to be adjacent.
- Counting occurrences -> Map, then check `num + 1` exists.

---

[Find All Numbers Disappeared in an Array](https://leetcode.com/problems/find-all-numbers-disappeared-in-an-array/)

> [!NOTE]
> Mapping value to an address. By using the sign (positive/negative) as a boolean flag, you preserve the original magnitude of the data while adding a new layer of "metadata" (the "seen" status) without allocating new memory.

- This problem is introduces a high-level concept: The array as its own Hash Map.
- Numbers are in range [1, N] and Array length is n.
- Every number has a home (as index) waiting for it in the array. if n = 8, the numbers should be 1 through 8. If we find a 4, it "belongs" at index 3 (zero based).

> [!INFO]
> Use the input array as hash map.

The marking strategy: How do I "mark" that a number has been seen without deleting the data already at that index?
- Negation. if I see the number 4, I go to index 3 and make whatever value is there negative.
- Any index that still has a positive number means its corresponding value (index + 1) was never "seen".

---

[merge sorted array](https://leetcode.com/problems/merge-sorted-array/?envType=problem-list-v2&envId=wrdcuh52)

- in-place array Manipulation. the trick is to stop looking at the beginning of the arrays and start looking at the end

- if you merge from the front (index 0) you will overwrite the elements that hasn't compared yet.
- Since the largest elements are at the back of both sorted arrays, and the "empty space" (the zeros), you should merge from right to left.

> [!NOTE]
> This build Backwards Reasoning. In many "In-place" problems (like replacing spaces in a string or merging arrays) the "empty space" or "buffer" is at end. Working from the back allows you to use that buffer without destroying your input data, achieving `O(1)` space complexity.

--- 

[Range Addition 2](https://leetcode.com/problems/range-addition-ii/description/?envType=problem-list-v2&envId=wrdcuh52)

---

[image smoother](https://leetcode.com/problems/image-smoother/description/?envType=problem-list-v2&envId=wrdcuh52)

- This is the sliding window on a 2D grid pattern, also called a **convolution kernel** in image processing.
- which neighbors are valid -> bounds checking
- what's the floored average -> sum / count

---

[Degree of an Array](https://leetcode.com/problems/degree-of-an-array/description/)

- look for the span of the most frequent elements
- the degree is just the maximum frequency of any number.

> [!INFO]
> If `1` appears 10 times but is spread across the whole array (index 0 to 1000), and `2` appears 10 times but is bunched together (index 5 to 20), the "bunched" one gives you the shortest subarray.

> [!NOTE]
> - To maintain the frequency of a number `x` in a contiguous subarray, that subarray must start at the first occurrence of `x` and end at the last occurrence of `x`.

Beginners often loop once to find the degree, then again to find the numbers, then again to find indices.
- The performance fix: You can track `first` `last` `count` simultaneously. With `N = 50,000` constant factor optimizations matter for cache locality.

```text
**Find the "Span" for the Degree-making number:**

- Where is the **first** `2`? Index **1**.
    
- Where is the **last** `2`? Index **6**.
    
- The shortest subarray containing all three `2`s **must** start at index 1 and end at index 6.
    
- **Length:** 6−1+1=6.
```

Why to use three Maps
- to calculate that Length. We need three specific facts about every number we encounter:
	- Count -> How many times have I seen this? (To find the Degree).
	- First -> Where did I first see this (This never changes once set).
	- Last -> Where did I just see this (This updates every time we see the number)

---

[Can Place Flowers](https://leetcode.com/problems/can-place-flowers/?envType=problem-list-v2&envId=wrdcuh52)

To plant a flower at index `i`, three conditions must be met:
1. `flowerbed[i]` must be `0`.
2. The spot to the **left** (`i-1`) must be `0` (or it's the start of the bed).
3. The spot to the **right** (`i+1`) must be `0` (or it's the end of the bed).

Logic if `i===0`, the left is effectively `0`. If `i===length - 1` the right is effectively `0`

> [!NOTE]
> ask if you can modify the input. If not, you either need to copy the array `O(n)` space or just use logic to keep track of where the virtual flowers are.

**Inefficient Bounds Checking:** Writing `if (flowerbed[i-1] == 0 || i == 0)`.
- **The Error:** In many languages, if `i == 0` is checked second, `flowerbed[i-1]` will throw an Out of Bounds error. In JS, it returns `undefined`. Always put the boundary check (`i === 0`) **first** so the logical OR short-circuits.

--- 

[Find Pivot in Index](https://leetcode.com/problems/find-pivot-index/)

- you need to use the prefix sum to solve a balance equation.
- you don't need a second loop to find the right sum. If you know the Total sum of the array, then at any point

```text
Right sum = Total sum - Left sum - current number;
```

The goal is to find the first index i where:

```text
Left Sum = (Total sum - Left sum - nums[i])
```

> [!NOTE]
> Instead of calculating two separate things (Left and Right), you calculate the whole and subtract the know part.
> - you only need the current prefix sum. Storing it in an array uses `O(n) space`, using a single variable `O(1)` space.
> - The pivot index itself is never part of the left or right sum.

---

[Majority Element](https://leetcode.com/problems/majority-element/?envType=problem-list-v2&envId=wrdcuh52&)

- This is the **Boyer-Moore Voting Algorithm** problem. While most developers reach for a Hash Map (which takes `O(n)`) space

- If you have a majority element, it appears more often than all other elements combined.

---

[Min Cost Climbing Stairs](https://leetcode.com/problems/min-cost-climbing-stairs/?envType=problem-list-v2&envId=wrdcuh52)

- At any step `i`, you could have arrived from either `i - 1` (one step) or `i - 2` (two steps).
- You want the minimum of those two options, plus the cost of the step you are currently on.

---

[Largest number at least twice of others](https://leetcode.com/problems/largest-number-at-least-twice-of-others/description/?envType=problem-list-v2&envId=wrdcuh52)

- don't need to check every number against the winner, you only need to check the winner against the runner-up.
- If the largest number is at least twice as big as the second-largest number, it is automatically at least twice as big as everything else.

---

[minimum operations to equalise array](https://leetcode.com/problems/minimum-operations-to-equalize-array/description/?envType=problem-list-v2&envId=wrdcuh52)


---

[find closest number to zero](https://leetcode.com/problems/find-closest-number-to-zero/?envType=problem-list-v2&envId=wrdcuh52)

- distance from zero is defined by the absolute value `|x|`.
- Correctly identify that absolute value (|x|) is the bridge between a position and distance. Find the proximity and then reintroduced the sign for the comparison.

---

[remove one element to make the array strictly increasing](https://leetcode.com/problems/remove-one-element-to-make-the-array-strictly-increasing/description/)

- determine which element to remove, and whether that removal actually fixes the sequence

- When you find a "violation" (where nums[i]≤nums[i−1]), you have two choices to fix it: remove the **current** element (nums[i]) or the **previous** element (nums[i−1]). In a sequence like `[1, 2, 10, 5, 7]`, which one should you remove, and how does your code decide?
- Edge case -> Look at the edge case `[10, 20, 30, 5, 25]`. At index 3 (value 5), there is a dip. If you remove `5`, is the array strictly increasing? If you remove `30`, is it strictly increasing?
- Your current `if` condition checks `i > 1` and looks at `nums[i-2]`. Why is it important to look **two steps back** rather than just one?

### Implementation

The trick is to realise that when `nums[i]≤nums[i−1]` we must "virtually" remove one. If removing the current element is necessary because it's too small (smaller than the one two steps back), we simulate its removal by updating its value to match the previous one, so the _next_ iteration compares against a valid "last seen" height.

### Common implementation errors

- In-place mutation vulnerability -> mutating the `nums` array can be dangerous. If this function is part of a large utility library, an unsuspecting developer might pass an array they need later, only to find their data has been modified. **A safer approach would be to track the previous valid value in a variable** 

> [!INFO]
> To transition fro mutating the array to using a variable, you essentially need a *phantom* pointer that remembers the last number that was part of a strictly increasing sequence.

---

[Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/)

- Usually, we map `Number -> Frequency`. What if we created an array where the index represents the `Frequency` and the value is a list of `Numbers` that hit that frequency? This is called Bucket Sort.

> [!NOTE]
> If two numbers have the same frequency, they simply share the same "bucket". 
> - think of each index in your bucket array as a container (like a nested array). if both the number appear exactly same times, they both get pushed into the bucket at same index.

> [!INFO]
> This approach achieves `O(n)` time complexity because we only iterate through the input array and the bucket array once.

> [!WARNING]
> Mapping frequency with index
> - memory exhaustion, in environments with strict memory limits, creating a large sparse array based on input size can be risky.

---

[Valid anagram](https://leetcode.com/problems/valid-anagram/description/)
- you can apply frequency count logic to raise a count and decrease the count with other string and if the counts is 0 that means same number of frequency character are present in both the string.

---

[Group anagram](https://leetcode.com/problems/group-anagrams/)
- normalize each string so that all anagrams produce the exact same key.

- If you have "eat" and "tea", what operation could you perform ob both string to make them identical?
	- we can do better then sorting both the word by using a frequency array to reach `O(n . k)`
	- since the constraints limit us to lowercase English letters, a fixed-size array of 26 is the most efficient way to generate a "fingerprint" for each string.

> [!INFO]
> We take the word "eat" and "tea". We count the letters in each. Both result in: `{a: 1, e: 1, t: 1}`. No matter what the sequence of character is the index of count will be the same that can be used as a key to group the similar anagram words.

---

[Longest Consecutive Sequence](https://leetcode.com/problems/longest-consecutive-sequence/)
- Look up neighbors in constant time.

---

[Valid Sudoku](https://leetcode.com/problems/valid-sudoku/)
- Since we have 9 rows, 9 columns, and 9 sub-boxes, we need to track seen digits for each.
- Sub-box identification -> If your are at a specific cell (r, c) how can you mathematically determine which of the nine `3 x 3` sub-boxes it belong to?
- **Iteration Efficiency:** We could iterate over the board three times (once for rows, once for columns, once for boxes), but is it possible to validate all three constraints in a **single pass** of the 9×9 grid?

---

[Fair Candy Swap](https://leetcode.com/problems/fair-candy-swap/description/?envType=problem-list-v2&envId=wrdcuh52)
- This is a "balance" problem. The logic "strips down" to finding two variables that satisfy a linear equation.

---

[Surface Area of 3D Shapes](https://leetcode.com/problems/surface-area-of-3d-shapes/?envType=problem-list-v2&envId=wrdcuh52)
- Need to think about how surface area is created, and more importantly, how it is lost, when cubes are stacked or placed next to each other.

---

[X of a Kind in a Deck of Cards](https://leetcode.com/problems/x-of-a-kind-in-a-deck-of-cards/?envType=problem-list-v2&envId=wrdcuh52)
- This is a [[Frequency Counting]] and [[Greatest Common Divisor (GCD)]] problem.
- Commonality Requirement It's not enough for each group to have some size `x > 1` every single group in the entire partition must have the same size. Therefore, x must be a common divisor of all card counts.

---

[Sign of the product of an array](https://leetcode.com/problems/sign-of-the-product-of-an-array/?envType=problem-list-v2&envId=wrdcuh52)

We don't actually need to calculate the product of the entire array. Since multiplying large number can lead to integer overflow.
- If any number is the array is 0, the entire product will be 0.
- If there are no zeros, the sign of the product depends entirely on the count of negative numbers

---

[Longest Subsequence With Limited Sum](https://leetcode.com/problems/longest-subsequence-with-limited-sum/description/?envType=weekly-question&envId=2026-04-22)

- this problem lies in the definition of a subsequence. Because we only care about the size of the subsequence and its total sum, the original order of the element doesn't actually matter.
- Picking any subset of elements will always form a valid subsequence if we just pick them in their original relative order.

> [!INFO]
> To maximize the number of elements we can pick without exceeding the target sum `queries[i]`, we should greedily pick the smallest numbers available.