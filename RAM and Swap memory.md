RAM -> Primary working memory
- RAM is your "active workspace" it holds the data and instruction for every application you have open right now.

Swap -> backup storage for RAM pages that are not currently needed.
- Swap is a dedicated area on your hard drive or SSD that acts as an extension of your RAM. it is virtual memory. It Prevent your system from crashing why you run out of physical RAM.

OS manages both automatically.
- The OS manages this process through a mechanism called **Paging**.
	- Prioritization -> OS keeps the most frequently and recently used data in Physical RAM.
	- The Eviction process -> When you open a new, memory-hungry application (like a heavy IDE) and your RAM is full, the OS looks for "cold" data, information that hasn't been accessed for a while.
	- Swapping out -> The OS moves that "cold" data from your RAM to the Swap partition on your disk. This frees up space in your fast RAM for the new task.
	- Swapping IN -> if you click back on the application that was moved to Swap, the OS must move that data to the RAM (often moving other data out to make room). This causes a brief delay, which is why your computer might feel "leggy" if you are low on RAM.

Process requests memory -> OS gives virtual memory (not physical RAM immediately)

Memory is divided into pages. Each page can live in RAM or Swap.

> [!INFO]
> Memory management (How data is stored/moved) and Process Synchronization (how task coordinate). While memory management (RAM/Swap) handles where the data lives, **Semaphores** handle the order and safety of process trying to access that data.