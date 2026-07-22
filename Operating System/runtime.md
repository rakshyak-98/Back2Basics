[[Runtime Environment]] [[interpreter]] [[Heap memory]] [[system call]]

# Runtime

> The executing phase of a program — allocation, calls, I/O, and dynamic dispatch happen here, not at compile/link time.

---

## Mental model

**Compile time** fixes types and layout (mostly). **Runtime** is everything that happens while the process is alive:

```txt
startup → [runtime: heap, stack, syscalls, GC, threads] → exit
              ▲
              └── language runtime (libc, JVM, V8, Go scheduler)
```

Runtime responsibilities vary by stack:

| Runtime piece | Examples |
|---------------|----------|
| **Memory** | `malloc`, GC, arena allocators |
| **Execution** | Interpreter loop, JIT tiers, goroutine scheduler |
| **I/O** | Buffered stdio, async reactor, thread pool |
| **Dynamic linking** | `dlopen`, symbol resolution |
| **Reflection / metadata** | JVM classes, Go interfaces, JS prototypes |

**Service impact:** runtime choices dominate tail latency (GC pauses), memory footprint, and concurrency model — not raw algorithm alone.

---

## Standard config / commands

### Observe runtime behavior

```bash
# Native heap
MALLOC_ARENA_MAX=2 ./app          # glibc arena count (container memory)
LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libjemalloc.so ./app

# JVM
java -XX:+PrintGCDetails -Xmx512m -jar app.jar

# Node/V8
node --max-old-space-size=4096 app.js
NODE_OPTIONS='--trace-gc' node app.js

# Go
GODEBUG=gctrace=1,malloc=1 ./app
```

### Node.js debug breakpoint at runtime start

```bash
node --inspect-brk app.js   # waits for debugger before user code
# Chrome → chrome://inspect
```

**Why `--inspect-brk`:** attach before top-level module side effects run — critical for debugging init-order bugs.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| RSS grows unbounded | Heap profiler (`heaptrack`, `go tool pprof`) | Fix leak; tune pool; cap cache |
| Periodic latency spikes | GC logs, `STW` events | Tune heap; change GC algo; reduce allocation rate |
| Crash only in prod build | `-O2` UB, race | Sanitizers in CI; ThreadSanitizer |
| Slow cold start | Dynamic linking, JIT warmup | Precompile (AOT); class data sharing; smaller deps |

---

## Gotchas

> [!WARNING]
> **"It works in dev"** — dev often disables optimizations, uses smaller data, single-threaded — runtime paths differ.

> [!WARNING]
> **Static linking ≠ no runtime.** You still have libc, pthread, and possibly vDSO.

> [!WARNING]
> **Container CPU limits without runtime awareness** — Go/Java may default `GOMAXPROCS`/GC threads to host CPU count, not cgroup quota.

---

## When NOT to use

"Runtime" is not a knob you configure as one thing — identify the **specific subsystem** (GC, thread pool, allocator) before tuning. Avoid `-XX:+UseEveryFlagYouGoogled` without metrics.

---

## Related

[[Runtime Environment]] [[interpreter]] [[Heap memory]] [[Event Loop]] [[context switching]]
