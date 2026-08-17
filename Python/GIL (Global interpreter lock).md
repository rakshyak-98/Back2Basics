[[Python]] [[ASGI]] [[Operating System/context switching]]

# GIL (Global interpreter lock)

> Global Interpreter Lock — CPython mutex so only one thread runs Python bytecode at a time in a process.

```txt
        GIL (Global interp ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Classic Python concurrency question: why `threading` doesn’t speed CPU-bound …

## Sources
- [Python wiki — GlobalInterpreterLock](https://wiki.python.org/moin/GlobalInterpreterLock) — overview
- [CPython internals — GIL](https://docs.python.org/3/c-api/init.html#thread-state-and-the-global-interpreter-lock) — deep-dive
- [Wikipedia — Global interpreter lock](https://en.wikipedia.org/wiki/Global_interpreter_lock) — overview

## Key Concepts
- **Bytecode serialization:** one thread holds the GIL while executing Python ops → CPU-bound pure Python s…
- **I/O release:** blocking I/O typically drops the GIL → threads still help concurrent network/…
- **Process parallelism:** `multiprocessing` / multiple processes each have their own interpreter and GI…
- **Free-threaded builds:** experimental/nogil efforts exist in newer CPython lines


- **Core:** In CPython, the GIL protects interpreter state

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

## Mistakes to Avoid
- **Mistake:** Benchmarking only I/O demos to “prove threads scale” for CPU work
- **Mistake:** Sharing mutable state across processes without queues/shared mem…
- **Mistake:** Ignoring GIL releases in NumPy/pandas

## Pros/Cons or Trade-offs
- **Pro:** Simpler memory model for extensions historically; many C APIs assume it.
- **Con:** Misleading “just add threads” advice for CPU-bound services.

## Comparison
- vs asyncio: cooperative concurrency on one thread — great for I/O, not a GIL bypass for CPU.
- vs JVM/Go style threads: those runtimes schedule OS threads without a single bytecode mutex like …


### Use cases
- Image thumbnail service: pure-Python pixel loops stayed at ~1 core with a thr…
