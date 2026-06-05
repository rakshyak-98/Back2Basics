- synchronisation mechanism for managing access to shared resources by multiple threads or processes in concurrent systems (threads/processes).
- act as a signaling system to prevent race conditions and ensure that data is not corrupted when multiple parts of a program run at the same time.

> [!INFO]
> - integer variable used as a signal mechanism
> - Controlled by atomic operations `wait()` and `signal()`
> - Prevents race conditions, ensures mutual exclusion (mutex) or process coordination.

- a semaphore is a variable or [[ADT (Abstract Data Type)]] 
- used to *control access* to a common resource by multiple threads and avoid [[critical sections]] problems in a concurrent system such as a multitasking operating system.

### Binary semaphores
- used to implement locks


## Operations

- **`wait()` (historically `P()` or `down`):** This operation decrements the semaphore's value. If the value becomes zero (or is already zero), the calling thread is blocked and put to sleep until the resource becomes available.

- **`signal()` (historically `V()` or `up`):** This operation increments the semaphore's value. If there are other threads blocked and waiting, this operation wakes one of them up so it can proceed into the critical section.

### Types of Semaphores

- **Counting Semaphore:** The internal counter can be any positive integer. This is used when you have a pool of identical resources available (like a database connection pool that can handle 10 concurrent connections).
- **Binary Semaphore:** The internal counter can only be `0` or `1`. This acts as a simple gatekeeper to ensure that only a single thread can access a specific piece of data or code at a time.