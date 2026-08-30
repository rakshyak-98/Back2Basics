Parent, Child, Siblings, Leaf, Subtree
Depth, Height, Degree (number of children), Path length (number of traversed edges)

## Tree types
[[Binary Tree]] at most two children
[[Full Binary Tree]] 0 or 2 children
[[Complete Binary tree]] levels filled leftward
[[BST]] ordered by key
[[Heap]] parent satisfies priority property

## Traversal
[[DFS]] explores depth before siblings
[[Inorder]] Left -> Root -> Right
[[Preorder]] Root -> Left -> Right
[[Postorder]] Left -> Right -> Root
[[BFS]] visits nodes level by level

> [!NOTE]
> - Tree operations often depend on **height**
> - Balanced tree ** $height \approx log_2 n$ **
> - Skewed tree **$height \approx n$** 
> - Traversal visits all nodes **O(n)**
> - Shape determines search efficiency

## Application
[[File system]] directories and files
[[Compiler]] syntax trees
[[Database]] B-Trees
[[Priority queue]] heaps
[[AI]] Decision trees