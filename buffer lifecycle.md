 buffer in the kernel go through the following lifecycle
 1. Allocation: Buffers are allocated from free memory on demand when needed.
 2. Queuing: Newly allocated buffers are added to the incoming queue of the buffer cache.
 3. Filling: For read requests, the buffer is filled with data from disk. For writes, the user data is copied int.
 4. Dequeueing: after being filled, the buffer moves to the outgoing queue.
 5. Writeback: dirty buffers are periodically written back to disk by the kernel's pdflush threads.
 6. Eviction: clean buffers are evicted from the cache when memory is scarce to free up space.

also read
[[buffer flags]]