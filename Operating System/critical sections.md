A code block which prevent race condition to access shared resource.

> [!INFO]
> A critical section in concurrent programming is a specific block of code when a thread or process accesses and modifies a shared resource. Such as a variable, data structure, file or memory location. Because multiple thread running simultaneously might try to read and write to this shared resource at the exact same time, the critical section must be protected to prevent race conditions and data corruption.

> [!NOTE]
>  To visualize this, imagine a single-occupancy restroom in a busy office:
> - The **shared resource** is the restroom itself.
> - The **critical section** is the act of being inside and using the restroom.
> - If two people (threads) try to enter and use it at the exact same time, chaos ensues. To prevent this, there is a lock on the door (a synchronization mechanism like a semaphore or mutex).
