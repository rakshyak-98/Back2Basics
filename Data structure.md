> [!INFO] 
  Algorithm complexity
> - mostly has to do with the number of times the algorithm needs to access its input data to do its job. 
- an `O(n)` algorithm, which needs to access its input only once.

> [!INFO]
>  `O(n!)`
> - the worst algorithms, however, are the ones with an `O(n!)` running time. 
> - Which makes them almost unusable for inputs with more than 300 elements.

### Logic
- increase the steps

## Array

> [!INFO]
> getting data at a specific index, take the width of the type multiply it by the offset puts it at the memory addressing go in and grab that.

- deleting an element from the array can be done in O(1) by swapping the element to be deleted with the last element in the array and then removing the last element.
- fixed size, contiguous memory allocation.
- direct index access `O(1)`
- insertion/Deletion `O(n)` because of shifting elements.

> [!INFO]
> Getting data at a specific index involves multiplying the width (size in bytes) of the type by the index offset, then adding it to the base memory address to locate the desired element. The system then goes to that calculated address and retrieves the data.

## Sub-array
- a sub-array is a contiguous segment of an array. For an array of size N, a sub-array can start at any index from 0 to N -1. 
- counting sub-array : from each start index i (where i ranges from 0 to N - 1), the sub-array can end at any index j (where j ranges from i to N - 1).
- the number of choices from the ending index j for a given starting index i in N - i.

---
### 1. Difference Between Stack and Queue

**Stack**: Follows LIFO (Last In, First Out).  
**Queue**: Follows FIFO (First In, First Out).

#### Implementation in JavaScript:

- **Stack**: Use an array and `push`/`pop` methods.
- **Queue**: Use an array and `push`/`shift` methods.

#### Use Cases:

- **Stack**: Undo/Redo functionality, parsing expressions.
- **Queue**: Task scheduling, print queues.

---

### 2. Linked List in JavaScript

**Types**: Singly Linked List, Doubly Linked List, Circular Linked List.
- sequence of nodes where each node points to the next.
- Access `O(1)` direct index access.
- insertion/Deletion `O(1)` if pointer is known.

> [!INFO]
> Linked list are useful when frequent insertion/deletion is required without concern for random access.

#### Implementation:

- Node structure: `{value, next}` (Doubly: `{value, next, prev}`).

#### Operations:

- **Insertion**: At head, tail, or specific index.
- **Deletion**: Remove specific node or at index.

---

### 3. Binary Search Tree (BST)

- **Concept**: Hierarchical data structure; left child < parent, right child > parent.
#### Implementation:
- Node structure: `{value, left, right}`.
- Operations: Recursive or iterative for search, insert, delete.
#### Time Complexities:
- **Search/Insert/Delete**: O(log n) average, O(n) worst-case (unbalanced).
---
### 4. Hash Table in JavaScript
**Concept**: Key-value storage with hashing.
#### Collision Resolution:
- Separate Chaining: Linked lists at each bucket.
- Open Addressing: Linear probing, quadratic probing, or double hashing.
#### Dynamic Resizing:
- Expand and rehash when load factor > threshold.

---

### 5. Sorting Algorithms
**Types**: Bubble Sort, Quick Sort, Merge Sort, Heap Sort.
#### Quick Sort:
- Recursive; Pivot-based partitioning.
- Time: O(n log n) avg, O(n²) worst.
- Space: O(log n).
#### Merge Sort:
- Divide and conquer; merge sorted halves.
- Time: O(n log n).
- Space: O(n).

---
### 6. Dynamic Programming
**Concept**: Optimize by storing overlapping subproblems.
#### Knapsack Problem:
- Define DP array: `dp[w]` for max value with weight `w`.
#### Examples:
- Longest Common Subsequence, Fibonacci, Matrix Chain Multiplication.

---
### 7. Graph Traversal
**Concept**: Explore all nodes in a graph.
#### DFS:
- Recursive or stack-based; explore deeper first.
#### BFS:
- Queue-based; explore all neighbors before moving deeper.
#### Use Cases:
- **DFS**: Pathfinding, cycle detection.
- **BFS**: Shortest path, level order traversal.

---

### 8. Detecting Cycles in Directed Graphs
**Algorithms**:
- DFS with a visited stack.
- Kahn's Algorithm (Topological Sort).
#### Implementation:
- Use adjacency list and maintain visited/recursion stack.
---

### 9. Priority Queue and Heap
**Heap**: Binary tree; min-heap or max-heap properties.
#### Implementation:
- Use array and parent/child indices.
- Insert: Bubble-up; Remove: Bubble-down.
#### Use Cases:
- Task scheduling, Dijkstra's shortest path algorithm.

---

### 10. Trie (Prefix Tree)

**Concept**: Tree structure for string storage.
#### Operations:
- Insert, search, and delete words.
#### Use Case:
- Efficient autocomplete and dictionary operations.

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
## Fixed size window size is predetermined
- complexity -> time `O(n)` / space `O(1)`.
### algorithm
- initialize two pointers `left=0` and `right=0`
- expand `right` until the window reaches size `k`.
- compute result `sum` `max` etc.
- slide the window by moving `left` and `right` together.

## Variable size window window expands or shrinks dynamically based on constraints
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