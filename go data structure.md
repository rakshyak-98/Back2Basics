### Binary tree
- data structure where underneath each node there exist _at most_ two other nodes.
- the node can be connected to one, two, or no other nodes.
 
 depth of tree -> also called height of a tree, is defined as the longest path from the root to a node, wheres the **depth of a node ** is the number of edges from the node to the root of the tree.
 
a leaf -> is a node with no children.

a balanced tree -> when the longest length from the root node to a leaf is at most one more than the shortest such length.

> [!INFO] balancing a tree might be a difficult and slow operation
> - so it is better to keep your tree balanced from the beginning rather than trying to balance it after you have created it.

> [!INFO] Advantages of binary tree
> - if the tree is not balanced, then the performance of the tree will be unpredictable.
> - used for represent hierarchical data, trees are extensively used when the compiler of a programming language parses a computer program.
> - putting an element into the correct place keeps them ordered. However, deleting an element from a tree is not always trivial because of the way that trees are constructed.
- if a binary tree is balanced, its search, insert, and delete operations take about `log(n)` steps, where `n` is the total number of elements that the tree holds.
- disadvantage of binary trees is that the shape of the tree depends on the order in which its elements were inserted.

#### Implementing a binary tree
```go
package main

import (
	"fmt"
	"time"
)

// defination of the node of the tree
type Tree struct {
	Left *Tree
	Value int
	Right *Tree
}

func traverse(t *Tree) {
	if t == nil {
		return
	}
	traverse(t.Left)
	fmt.Print(t.Value, " ")
	traverse(t.Right)
}

func create(n int) *Tree {
	var t *Tree
	rand.Seed(time.Now().Unix())
	for i := 0; i < 2*n; i+=1 {
		temp := rand.Intn(n * 2)
		t = insert(t, temp)
	}
	return t
}

func insert(t *Tree, v int) *Tree {
	// checks wheater we are dealing with an empty tree or not
	if t === nil {
		return &Tree(nil, v, nil) // if it is an empty tree, then the new node will be the root of the tree.
	}

	// check wheather the value to insert already exists in the binary tree or not.
	if v === t.Value {
		t.Left = insert(t.Left, v)
		return t
	}
	
	/*
	 weather the value you are trying to insert will go on the left or right of the node.
	*/
	
	if v < t.Value {
		t.Left = insert(t.Left, v)
		return t
	}
	
	t.Right = insert(t.Right, v)
	return t
}

```

> [!INFO] Searching in binary tree
> when searching for an element on a binary tree, you check whether the value of the element that you are looking for is bigger or smaller than the value of the current node and use that decision to choose which part of the tree you will go down next.