> [!INFO]  Algorithm complexity
> - algorithm is judged by its computational complexity, which mostly has to do with the number of times the algorithm needs to access its input data to do its job.
- an `O(n)` algorithm, which needs to access its input only once.

> [!INFO] `O(n!)`
> - the worst algorithms, however, are the ones with an `O(n!)` running time. 
> - Which makes them almost unusable for inputs with more than 300 elements.

### Logic
- increase the steps

## Array
- deleting an element from the array can be done in O(1) by swapping the element to be deleted with the last element in the array and then removing the last element.
### Sub-array
- a sub-array is a contiguous segment of an array. For an array of size N, a sub-array can start at any index from 0 to N -1. 
- counting sub-array : from each start index i (where i ranges from 0 to N - 1), the sub-array can end at any index j (where j ranges from i to N - 1).
- the number of choices from the ending index j for a given starting index i in N - i.
### Prefix sum
- allow for quick calculations of the sum of elements within a specific range of an array.
- Efficient Range queries : sum(L, R) = prefix[R] - prefix[L-1]. This is significantly faster than recalculating the sum from scratch, which would take O(n) time for each query.
- used in algorithms for finding the number of elements less than or equal to a given value.
### Sliding window
1. Maximum Sum Sub-array of Size K 


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