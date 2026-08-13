<!-- note-strategy: operational -->
[[Operating System]] [[multi-threaded]] [[Thread]] [[non-blocking]] [[Blocking Vs Non-Blocking]] [[NodeJS]]

# Single-threaded

> Single-threaded means one execution stack runs your logic — concurrency comes from an event loop or child processes, not shared-memory threads.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** One thread runs callbacks/tasks to completion; while it waits on I/O the runtime parks the work and services someone else — no lock for your JS heap, but CPU work blocks everyone.

```txt
Event loop (1 thread)
  │
  ├─ accept ready I/O events
  ├─ run callback until it returns   ← must not busy-spin / heavy CPU
  └─ repeat

Optional: worker_threads / child processes for CPU or isolation
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Single-threaded** | One call stack for app logic | “Node’s JS runs on one thread; libuv has a small pool.” |
| **Event loop** | Queue of ready callbacks | “I never block the loop with sync CPU or sync disk.” |
| **Non-blocking I/O** | Start I/O, continue later | “Concurrency without shared-memory races.” |
| **Cooperative** | Task runs until it yields | “A tight loop starves all other requests.” |
| **Child process** | Separate OS process | “Still allowed — OS process ≠ language threads.” |
| **Worker thread** | Extra thread for CPU | “Offload crypto/image work; don’t pretend the loop is multi-core.” |

> [!INFO]
> Spawning a child process is an **OS** feature. A single-threaded language can still `fork`/`spawn` — that does not make the language multi-threaded.

### How the story goes (4 steps)

1. **Register** — start async I/O / timers; return to the loop.
2. **Wait** — kernel signals readiness ([[Epoll]] under Linux).
3. **Run** — one callback at a time on the main stack.
4. **Offload** — heavy CPU → worker / process pool; keep the loop thin.

---

## Standard config / commands

```bash
# Node — see event-loop lag
node --perf-basic-prof app.js
# or clinic doctor / 0x for flamegraphs

# Prove one JS thread, extra libuv / workers
ps -L -p <pid>
```

```js
// Bad: blocks the single thread
fs.readFileSync('huge.bin')
crypto.pbkdf2Sync(password, salt, 1e6, 64, 'sha512')

// Better: async / worker
await fs.promises.readFile('huge.bin')
await crypto.promises.pbkdf2(password, salt, 1e6, 64, 'sha512')
```

| Knob | Why it matters |
|------|----------------|
| Sync APIs (`*Sync`) | Stall every connection on that process |
| `UV_THREADPOOL_SIZE` | Default 4 — DNS/fs/crypto can queue behind it |
| Cluster / PM2 instances | Scale by **processes**, still single-threaded each |
| Worker threads | Shared ArrayBuffer needs explicit sync |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Latency for all users | One hot sync function / CPU loop | Break work; move to worker |
| High load, one core busy | Expected for single-thread JS | Scale out processes |
| “Random” timeouts under fs load | Thread pool saturation | Raise `UV_THREADPOOL_SIZE` or reduce sync fs |
| Race after adding workers | Shared heap assumptions | Treat workers like multi-thread — see [[multi-threaded]] |
| UI freeze | Long task on main thread | Chunk work; `requestIdleCallback` / web workers |

---

## Gotchas

> [!WARNING]
> **Single-threaded ≠ single process ≠ no concurrency.** Thousands of connections can be in flight; only one JS callback runs at a time.

> [!WARNING]
> **CPU-bound work destroys the model.** Hashing, JSON on huge payloads, image encode — offload or use another service.

> [!WARNING]
> **Hidden thread pools still exist** (libuv, DNS). Blocking them is a multi-thread failure mode inside a “single-threaded” app.

> [!WARNING]
> **Shared globals are “safe” only until you add workers.** Confinement is the feature; don’t give it up casually.

---

## When NOT to use

- **Heavy parallel CPU** — use [[multi-threaded]] runtimes, SIMD, or a job fleet.
- **Hard real-time multi-core** — need OS threads with priorities and PI mutexes.
- **When you already need fine-grained shared mutable state** — you’ll reinvent locks badly.

---

## Related

[[multi-threaded]] [[Thread]] [[non-blocking]] [[Blocking Vs Non-Blocking]] [[Epoll]] [[NodeJS]] [[CPU IO Bound Task]] [[thread pool]]
