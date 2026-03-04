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

Given an integer `rowIndex`, return the `rowIndexth` (**0-indexed**) row of the **Pascal's triangle**.

In **Pascal's triangle**, each number is the sum of the two numbers directly above it as shown:

![](https://upload.wikimedia.org/wikipedia/commons/0/0d/PascalTriangleAnimated2.gif)

**Example 1:**

**Input:** rowIndex = 3
**Output:** [1,3,3,1]

**Example 2:**

**Input:** rowIndex = 0
**Output:** [1]

**Example 3:**

**Input:** rowIndex = 1
**Output:** [1,1]

**Constraints:**

- `0 <= rowIndex <= 33`

**Follow up:** Could you optimize your algorithm to use only `O(rowIndex)` extra space?

- each interior element = sum of two element above it `triangle[i][j] = triangle[i-1][j-1] + triangle[i-1][j]`

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

```text
prices = [7, 1, 5, 3, 6, 4]
         i=0  1  2  3  4  5

i=0: prices[0]=7, prices[-1]=undefined → skip
i=1: 1 > 7? No → skip
i=2: 5 > 1? Yes → profit += (5-1) = 4
i=3: 3 > 5? No → skip
i=4: 6 > 3? Yes → profit += (6-3) = 7
i=5: 4 > 6? No → skip

Total profit = 7
```

- Capture every upward movement. Because we can buy and Sell multiple times.

> [!NOTE]
> Why checking consecutive days gives the same result as waiting for future peaks.
> - Buying at valley and selling at future peak = Sum of all daily increase between them.

```text
Prices: [1, 2, 3, 5, 4]
         ↑           ↑
       valley      peak

Method 1: Wait for peak (what you're suggesting)
Buy at day 0 (price=1), sell at day 3 (price=5)
Profit = 5 - 1 = 4

Method 2: Consecutive day gains (the algorithm)
Day 0→1: 2 - 1 = 1
Day 1→2: 3 - 2 = 1  
Day 2→3: 5 - 3 = 2
Total = 1 + 1 + 2 = 4

SAME RESULT! ✓
```

**Why?** Because mathematically:
```
(2-1) + (3-2) + (5-3) 
= 2 - 1 + 3 - 2 + 5 - 3    // Expand
= 5 - 1                     // Middle terms cancel!
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