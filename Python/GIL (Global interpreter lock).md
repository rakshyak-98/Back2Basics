[[Python]] [[ASGI]] [[Operating System/context switching]]

# GIL (Global interpreter lock)

> Global Interpreter Lock — CPython mutex so only one thread runs Python bytecode at a time in a process.





## Interview Relevance
Classic Python concurrency question: why `threading` doesn’t speed CPU-bound work, when the GIL is released, and when to use multiprocessing, async I/O, or native extensions instead.

## Sources
- [Python wiki — GlobalInterpreterLock](https://wiki.python.org/moin/GlobalInterpreterLock) — overview
- [CPython internals — GIL](https://docs.python.org/3/c-api/init.html#thread-state-and-the-global-interpreter-lock) — deep-dive
- [Wikipedia — Global interpreter lock](https://en.wikipedia.org/wiki/Global_interpreter_lock) — overview

## Core Definition
In CPython, the GIL protects interpreter state. Threads interleave bytecode execution but do not run Python bytecode truly in parallel on multiple cores. I/O and many C extensions can release the GIL so other threads proceed.

## Key Concepts
- **Bytecode serialization:** one thread holds the GIL while executing Python ops → CPU-bound pure Python scales poorly with threads.
- **I/O release:** blocking I/O typically drops the GIL → threads still help concurrent network/disk waits.
- **Process parallelism:** `multiprocessing` / multiple processes each have their own interpreter and GIL → true multi-core for CPU work (at IPC cost).
- **Free-threaded builds:** experimental/nogil efforts exist in newer CPython lines — don’t assume production defaults have changed until you verify the build.

## Technical Details
```
One process, many threads
┌──────────── CPython ────────────┐
│  Thread A  ─► holds GIL ─► run  │
│  Thread B  ─► waits             │
│  Thread C  ─► waits             │
└─────────────────────────────────┘

CPU-bound → prefer processes / C extensions that release GIL
I/O-bound → threads or asyncio often enough
```

```python
# CPU-bound: threads won't use N cores for pure Python
from concurrent.futures import ProcessPoolExecutor
with ProcessPoolExecutor() as pool:
    list(pool.map(heavy_compute, chunks))
```

| Workload | Prefer |
|----------|--------|
| CPU-bound Python | Processes, vectorized C (NumPy), or a faster runtime section |
| I/O-bound | Threads or [[ASGI]]/asyncio |
| Mixed | Isolate CPU in processes/workers; keep I/O async |

## Real-World Applications
Image thumbnail service: pure-Python pixel loops stayed at ~1 core with a thread pool. Switching to `ProcessPoolExecutor` (or a C library that releases the GIL) saturated the machine.

## Pros/Cons or Trade-offs
- **Pro:** Simpler memory model for extensions historically; many C APIs assume it.
- **Con:** Misleading “just add threads” advice for CPU-bound services.

## Comparison
- vs asyncio: cooperative concurrency on one thread — great for I/O, not a GIL bypass for CPU.
- vs JVM/Go style threads: those runtimes schedule OS threads without a single bytecode mutex like CPython’s GIL.

## Mistakes to Avoid
- Benchmarking only I/O demos to “prove threads scale” for CPU work.
- Sharing mutable state across processes without queues/shared memory discipline.
- Ignoring GIL releases in NumPy/pandas — vectorized C work can parallelize better than Python loops imply.
