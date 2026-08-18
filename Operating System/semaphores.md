- A way for threads/processes to share a resource safely without corrupting data.
- Uses a counter and atomic `wait()` / `signal()` calls.
- Stops **race conditions** and enforces **mutual exclusion** when needed.

> [!INFO]
> - Counter starts at N (permits available).
> - `wait()` — take a permit; block if counter is 0.
> - `signal()` — return a permit; wake a waiting thread.

- A semaphore is a variable or [[ADT (Abstract Data Type)]] that limits how many threads can use a resource at once.

> **Before use:** call `wait()`. If counter > 0, take a permit and continue. If 0, block until someone calls `signal()`.
> **After use:** call `signal()` to release the permit and wake a waiter.

### Binary semaphores
- used to implement locks

## Operations

- **`wait()` (historically `P()` or `down`):** This operation decrements the semaphore's value. If the value becomes zero (or is already zero), the calling thread is blocked and put to sleep until the resource becomes available.

- **`signal()` (historically `V()` or `up`):** This operation increments the semaphore's value. If there are other threads blocked and waiting, this operation wakes one of them up so it can proceed into the critical section.

### Types of Semaphores

- **Counting Semaphore:** The internal counter can be any positive integer. This is used when you have a pool of identical resources available (like a database connection pool that can handle 10 concurrent connections).
- **Binary Semaphore:** The internal counter can only be `0` or `1`. This acts as a simple gatekeeper to ensure that only a single thread can access a specific piece of data or code at a time.