## Whey does swap exist?
Imagine you have `RAM=16GB` but processes collectively need more memory. The OS can move some relatively inactive memory pages from RAM to disk. Later, if the process accesses one of those swapped-out pages, the OS has to bring it back into RAM. This is called **page fault.**

```txt
			 CPU MEMORY SYSTEM
							│
		┌─────────┴─────────┐
		│                   │
CPU-managed          OS-managed
 caches              memory
		│                   │
 L1/L2/L3              RAM
												│
												↓
										 Swap
```

"Swap exists primarily to allow the OS to manage memory when RAM is insufficient or when it wants to reclaim RAM."