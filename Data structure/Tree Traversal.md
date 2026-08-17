[[Data structure/Data structure]] [[dsa intuition]] [[DSA algorithms]]

# Tree Traversal

> Tree traversal is the ordered visit of every node in a tree — depth-first (pre/in/post-order) or breadth-first (level-order) — each order answers different questions about structure, sorting, or serialization.

```txt
        Tree Traversal ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Comparison
```

## Why It Matters
- **Key signal:** Pick the right traversal for the problem: in-order for BST sorted output, BFS…

## Sources
- [Wikipedia — Tree traversal](https://en.wikipedia.org/wiki/Tree_traversal) — overview
- MIT OpenCourseWare 6.006 — tree algorithms — deep-dive

## Key Concepts
- **Core:** A traversal is a total order over nodes respecting parent/child reachability.…

## Technical Details
1. **Pre-order (DFS)** — visit root, then left subtree, then right subtree. Use: copy tree, prefix expressions.
2. **In-order (DFS)** — left subtree, root, right subtree. On BST: yields sorted keys.
3. **Post-order (DFS)** — left, right, root. Use: delete nodes, evaluate postfix/AST.
4. **Level-order (BFS)** — queue holds frontier; dequeue node, visit, enqueue children. Use: shortest depth, print by level.

```txt
        1
       / \
      2   3
     / \
    4   5

Pre-order:  1 2 4 5 3
In-order:  4 2 5 1 3
Post-order: 4 5 2 3 1
Level-order: 1 2 3 4 5
```

```python
def inorder(node):
    if not node:
        return
    inorder(node.left)
    visit(node)
    inorder(node.right)

from collections import deque

def level_order(root):
    q = deque([root])
    while q:
        node = q.popleft()
        visit(node)
        if node.left:
            q.append(node.left)
        if node.right:
            q.append(node.right)
```

### Level-order from array serialization

- When nodes are given as a level-order array with `null` gaps, keep two pointe…

1. **Array index** — which value to consume next.
2. **Queue** — which parent receives that value as left or right child.

- The array is read sequentially, but attachment order follows the queue

## Mistakes to Avoid
- **Mistake:** Using DFS for unweighted shortest path (use BFS)
- **Mistake:** Forgetting null children in level-order deserialization
- **Mistake:** Stack overflow on deep trees — prefer iterative DFS or BFS

## Comparison
- vs graph traversal: trees have no cycles; visited set optional.
- vs [[dsa intuition]] sorting: in-order on BST only works when BST invariant holds.


### Use cases
- DOM walks, filesystem directory listing, expression evaluation, and reconstru…
