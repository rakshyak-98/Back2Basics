**Why dynamically allocated data?**
Because sometimes a program doesn't know at compile time how much data it will need or how long that data must live. That's what "dynamically allocated" means.
- Memory is requested **while the program is running.** base on what the program actually needs.
- Data man need to survive beyond the current method.
"The heap provides a mechanism for objects whose **size and/or lifetime are determined at runtime.**"

> **Dynamic allocation doesn't mean "heap=dynamic, stack=static"**
> - Stack: Organized around thread execution and method calls.
> - Heap: General-purpose runtime storage for objects/data.

**Why not put it all on the stack?**
Because stack memory is primarily designed around **function execution.** When function execution completes the stack frame disappears. The references of the arguments must still exist because the caller has a reference to them, that's where heap allocation becomes useful.

"The heap allows objects to have a lifetime independent of a particular method's stack frame."

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

## Heap out or memory

 >[!INFO]
 >It is a pure resource-exhaustion attack aimed at availability rather than confidentiality or integrity.

Heap out of memory refers to condition in which a program attempts to allocate more memory in the heap region than is available or permitted by the operating system or runtime environment resulting in an allocation failure.

- The heap is the portion of a process's virtual memory used for dynamic allocations (via functions such as `malloc` in c/c++).
- Unlike the stack, which is automatically managed and limited in size, the heap grows as needed until it encounters system-imposed limits (for example, process address space constraints, ulimit settings, or the Java Virtual Machine's configured heap size).
	- When these limits are reached, the program typically raises an error such as `OutOfMemoryError` or `FATAL ERROR: Ineffective mark-compacts near heap limit Allocation failed`

> [!INFO]
> These actions are feasible because many applications trust external input to be well-behaved and do not enforce safeguards such as maximum allocation sizes, timeouts, or memory quotas per operation.kjjkkjjjj