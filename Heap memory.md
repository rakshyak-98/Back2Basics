A heap is a tree-based structure that lets you always get the min and max element in `O(1)` and insert/remove in `O(log n)`.

> [!INFO]
> - min-head -> top (root) is always the smallest element.
> - max-heap -> top is always the largest element.

> [!NOTE]
> Heap (DSA) and Heap memory (Runtime/OS) they are completely different concepts.
> Heap (DSA) -> a tree-based structure (Min/Max heap).
> Heap (Runtime/OS) -> a region of RAM used for dynamic allocation.

> [!INFO]
> heap memory in OS, is a logical memory region, not a physical one.
> logical memory -> it's part of the process's virtual address space. The OS maps it to physical memory under the hood, but the heap itself is just a logical abstraction provided to your program.

```txt
+---------------------+
|     Stack           | ← grows downward (for function calls, locals)
+---------------------+
|     Heap            | ← grows upward (for malloc/new)
+---------------------+
|     BSS             | (uninitialized static/global vars)
+---------------------+
|     Data            | (initialized static/global vars)
+---------------------+
|     Text / Code     | (binary instructions)
+---------------------+
```
