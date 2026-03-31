- time complexity grows linearly with two independent factors, multiply them to get the overall time complexity.

independent factors -> if you have two independent parts (outer loop and inner loop) of an algorithm, and each part has a linear time complexity, you multiply their complexity.

### Linear growth
if you you increase the input size by a factor, the execution time increases by the same factor.

Example -> you have an array of size N, and for each element in the array, you need to perform an operation that takes K steps. That's N operations, and each of those N operations takes K steps. The total number of steps is then `N * K`.

### LPS Array (in KMP) Longest Prefix Suffix
for each position `i` in the patterns, `LPS[i]` stores the length of the longest proper prefix that is also a suffix of the sub-string ``

### Recursion
- return address, return value, stack trace
- pre-operation (something done before recursion), Recursion (actual function call), Post-operation (something done after recursion).
- base case

> [!INFO]
> recursive function terminates by reaching a base case, where the function no longer calls itself and instead returns a specific value or performs a final operation.

> [!INFO]
> The call stack grows downward as recursive calls are made, then unwinds upward as each function returns its calculated value, with each function adding its own computation to the final result.

[pivot index](https://leetcode.com/problems/find-pivot-index/)
- pre-compute the total sum
- `lhs === total sum - lhs - nums[i]`

### Prefix sum balance checking
- Find index where left part = right part
- split array evenly
- find equilibrium point
- this trick is always: pre computer total, then compare with running prefix.

## Cancellation trick
- When you need to find an element that dominates, you can cancel out minority elements until only the dominant remains.


## **Floyd's Tortoise and Hare** algorithm.

In a circular racing track. If two people start running at the same point, but one runs twice as fact as the other, the faster runner will eventually 'lap' the slower open. They will meet again at some point on the track.

> [!INFO]
> We use same logic to find loops (cycles) in data.

We use two pointers to move through a sequence (like an array or a linked list):
	- the tortoise : move 1 step at a time.
	- the hare : move 2 steps at a time.

Phase 1 : finding the collision
If there is a loop, the Hare will eventually enter it and start running in circle. Since the Hare is faster, it will eventually catch up to the Tortoise from behind. The moment they land on the same spot, we know for a fact that a cycle exists.

Phase 2 : Finding the entrance
Once they collide, we need to find exactly where the loop starts (the entrance is the duplicate number).

## Dutch National Flag algorithm
since we only have three distinct values (0, 1, and 2) we can sort them in a single pass by partitioning the array into three sections.

- The **Dutch National Flag algorithm**, proposed by Edsger Dijkstra, is a three-way partitioning technique.
- It efficiently sorts an array containing three distinct values (typically represented as red, white, and blue) into three ordered groups.
- It completes the partitioning in **a single pass** through the array.
- It operates in **linear time complexity (O(n))** with **constant extra space (O(1))**.

> [!INFO]
> The dutch national Flag algorithm works for any scenario where you need to partition data into three distinct category that have a logical order (small, medium, large).