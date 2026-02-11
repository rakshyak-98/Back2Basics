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

