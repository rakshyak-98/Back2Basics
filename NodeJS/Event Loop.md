[[NodeJS]] [[Epoll]] [[clustering]] [[worker threads]] [[Express middleware]]

# Node.js Event Loop

> One-line: single-threaded JS + libuv thread pool — non-blocking I/O until you block the thread with CPU or sync I/O.

## Mental model

Node runs user JavaScript on **one thread**. libuv handles async I/O (network, fs, timers) via the event loop and a **thread pool** (default 4 workers for sync fs/crypto). When a callback runs, nothing else runs until it returns.

```
┌─────────────┐     poll OS (epoll)     ┌──────────────┐
│  Event Loop │ ◄────────────────────── │    libuv     │
│  (6 phases) │ ──► run JS callbacks ──►│ thread pool  │
└─────────────┘                         └──────────────┘
       ▲
       └── microtasks (nextTick, Promises) between phases
```

**Concurrency is cooperative** — long handlers delay every connection. Throughput ≠ parallel CPU.

---

## Six phases (one "tick")

| Phase | Handles | Senior note |
|-------|---------|-------------|
| **timers** | `setTimeout`, `setInterval` | Min delay ~1ms; starvation if recursive timers |
| **pending callbacks** | Deferred I/O (TCP errors) | Debug `ECONNREFUSED` weirdness here |
| **idle, prepare** | Internal | Ignore unless hacking core |
| **poll** | Incoming I/O, execute poll callbacks | Blocks waiting for events; core of non-blocking |
| **check** | `setImmediate` | Run after poll — good post-I/O batching |
| **close callbacks** | `socket.on('close')` | Missing cleanup → FD leaks → OOM |

**Microtasks** (outside phases, highest priority): `process.nextTick` runs before Promise callbacks; both run before next phase continues.

Order within tight code:

```javascript
setTimeout(() => console.log('timeout'), 0);
setImmediate(() => console.log('immediate'));
process.nextTick(() => console.log('nextTick'));
Promise.resolve().then(() => console.log('promise'));
// sync first, then nextTick, promise, then timeout/immediate (order of latter two varies by context)
```

---

## Standard config / commands

### Detect event loop lag

```javascript
const { monitorEventLoopDelay } = require('perf_hooks');
const h = monitorEventLoopDelay({ resolution: 10 });
h.enable();
setInterval(() => {
  console.log('p99 loop delay ms:', h.percentile(99) / 1e6);
  h.reset();
}, 5000);
```

```bash
node --trace-gc app.js                 # GC pauses masquerading as loop block
clinic doctor -- node app.js           # clinic.js flame + delay
```

### Fix blocking work

```javascript
// BAD — blocks entire server
app.get('/hash', (req, res) => {
  const hash = bcrypt.hashSync(req.body.password, 12);
  res.send(hash);
});

// GOOD — offload
const { Worker } = require('worker_threads');
// or: bcrypt.hash(..., cb)  — uses thread pool
// or: cluster / worker_threads for CPU farms
```

Break long sync loops:

```javascript
async function processChunk(items) {
  for (const item of items) {
    doWork(item);
    await new Promise(setImmediate);  // yield to loop
  }
}
```

### libuv thread pool size

```bash
UV_THREADPOOL_SIZE=16 node app.js      # default 4 — raise for heavy sync fs/crypto
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| API latency spikes globally | Event loop delay metric; `clinic bubbleprof` | Find sync/blocking handler; move to worker |
| Timeouts "random" under load | Single thread saturated | [[clustering]] or horizontal scale |
| `setImmediate` vs `setTimeout(0)` confusion | I/O vs non-I/O context | Use `setImmediate` inside I/O callbacks |
| Memory grows, connections hang | Missing `close` handlers | Register cleanup in close phase |
| fs ops queue forever | Thread pool exhaustion | Increase `UV_THREADPOOL_SIZE`; use async fs |
| Promises never resolve | Microtask deadlock patterns | Avoid nextTick recursion flooding |

---

## Gotchas

> [!WARNING]
> **`process.nextTick` starvation** — infinite nextTick prevents I/O phase from running. Prefer `setImmediate` for deferral in loops.

> [!WARNING]
> **JSON.parse huge payload on main thread** — blocks like CPU work. Stream or worker.

> [!WARNING]
> **"Async" doesn't mean parallel** — `async/await` still runs continuations on main thread.

> [!WARNING]
> **DNS lookup** — `dns.lookup` uses thread pool; `dns.resolve` uses network — different scaling behavior.

---

## When NOT to use

- **CPU-bound monolith on one Node process** — use workers, Rust sidecar, or different runtime (Go/Rust) for compute-heavy core.
- **`setInterval` for critical scheduling** — drift under load; use proper job queue.

---

## Related

[[clustering]] [[worker threads]] [[child process]] [[Epoll]] [[Express middleware]] [[Node events driven]]
