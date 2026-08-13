[[Operating System]] [[multi-threaded]] [[Single-threaded]] [[context switching]] [[mutexes]] [[process]]

# Thread

> A thread is the unit of CPU scheduling inside a [[process]] — own stack and registers, shared address space and file descriptors with siblings.

Created with `pthread_create`, `clone`, or language threads (Java, Go goroutines mapped to OS threads). The kernel scheduler assigns threads to cores → [[context switching]] when blocked or preempted.

Synchronize shared mutable state with [[mutexes]], [[semaphores]], or atomics — otherwise data races corrupt [[Heap memory]] structures.

## Sources

- Silberschatz — threads and concurrency
- Linux `pthread(7)`, `clone(2)` manual pages
- Wikipedia: [Thread (computing)](https://en.wikipedia.org/wiki/Thread_(computing))
