- A thread pool is a common pattern in concurrent/multithreaded programming.

- It is a collection (pool) of pre-created, reusable threads that stand ready to execute tasks, instead of creating and destroying a new thread every time you need to run something asynchronously.

**The pool manages everything**
- Keeps a fixed (or dynamic) number of threads alive.
- Has an internal **queue** for pending tasks.
- When a thread finishes a task -> it goes back to the pool (idle) and waits for new work.
- No repeated thread creation/destruction overhead.

## Typical components of a thread pool

1. **Work threads** -> the actual thread sitting idle or executing tasks.
2. **Manager/Executor** -> usually a [[thread-safe queue]].
3. **Thread factory** -> customises how threads are created.

## Why thread pool exist

|Problem without thread pool|How thread pool solves it|
|---|---|
|Creating a thread is relatively expensive (memory, time, OS involvement)|Threads are created only once (or slowly scaled up)|
|Destroying threads also costs resources|Threads are reused → lifetime is long|
|Too many threads → heavy context switching, memory pressure, thrashing|You control the maximum number of concurrent threads|
|Uncontrolled thread creation can crash the system|Pool enforces a limit → safe resource usage|
|Short tasks suffer from thread startup latency|Tasks start almost immediately if a thread is free|