- A thread-safe queue (also called a concurrent queue or synchronised queue) is a queue data structure that can be safely used (enqueued and dequeued) by multiple threads at the same time without causing data corruption, race conditions, lost updates, or crashes.

> [!INFO]
> It is a queue that has build-in synchronisation so you don't need to manually add locks/mutexes every time you call `put()` or `get()`


> [!INFO]
> - A thread-safe queue is the safest and most idiomatic way to pass data between threads without writing error-prone locking code yourself.
