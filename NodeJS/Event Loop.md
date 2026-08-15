[[NodeJS]] [[Epoll]] [[clustering]] [[worker threads]] [[Express middleware]] [[child process]] [[Node events driven]]

# Node.js Event Loop

> Node event loop — one JS thread plus libuv; never block it with heavy sync work.

## Interview Relevance

Interviewers use the event loop to test whether you know Node is one JS thread plus libuv, can name the phases, and will not block the loop with sync CPU or huge JSON.parse.


## Sources

- [Node.js — The Node.js Event Loop](https://nodejs.org/en/learn/asynchronous-work/event-loop-timers-and-nexttick) — deep-dive
- [Node.js — monitorEventLoopDelay](https://nodejs.org/api/perf_hooks.html#perf_hooksmonitoreventloopdelayoptions) — overview
- [Wikipedia — Event Loop](https://en.wikipedia.org/wiki/Event_Loop) — overview

## Core Definition

Node runs user JavaScript on **one thread**. libuv handles async I/O (network, fs, timers) via the event loop and a **thread pool** (default 4 workers for sync fs/crypto). When a callback runs, nothing else runs until it returns.

## Key Concepts

- **Single JS thread:** your callbacks run one at a time — a long sync handler stalls every connection.
- **libuv + phases:** timers → pending → poll → check → close; I/O readiness drives the poll phase.
- **Thread pool:** default 4 workers for some fs/crypto/dns — raise `UV_THREADPOOL_SIZE` under load.
- **Microtasks:** `process.nextTick` then Promise jobs run between phases; nextTick can starve I/O.


## Technical Details

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

### Six phases (one "tick")

| Phase | Handles | Senior note |
|-------|---------|-------------|
| **timers** | `setTimeout`, `setInterval` | Min delay ~1ms; starvation if recursive timers |
| **pending callbacks** | Deferred I/O (TCP errors) | Debug `ECONNREFUSED` weirdness here |
| **idle, prepare** | Internal | Ignore unless hacking core |
| **poll** | Incoming I/O, execute poll callbacks | Blocks waiting for events; core of non-blocking |
| **check** | `setImmediate` | Run after poll — good post-I/O batching |

**Microtasks** (outside phases, highest priority): `process.nextTick` runs before Promise callbacks; both run before next phase continues.

Order within tight code:

```javascript
setTimeout(() => console.log('timeout'), 0);
setImmediate(() => console.log('immediate'));
process.nextTick(() => console.log('nextTick'));
Promise.resolve().then(() => console.log('promise'));
// sync first, then nextTick, promise, then timeout/immediate (order of latter two varies by context)
```

## Real-World Applications

In production APIs and tooling, **Event Loop** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **`process.nextTick` starvation** — infinite nextTick prevents I/O phase from running. Prefer `setImmediate` for deferral in loops; **JSON.parse huge payload on main thread** — blocks like CPU work. Stream or worker.

## Pros/Cons or Trade-offs

- **Pro:** Solves the job described above when used in the right layer (Node event loop — one JS thread plus libuv; never block it with heavy sync work.).
- **Con / when not:** **CPU-bound monolith on one Node process** — use workers, Rust sidecar, or different runtime (Go/Rust) for compute-heavy core.
- **Con / when not:** **`setInterval` for critical scheduling** — drift under load; use proper job queue.

## Comparison

vs [[Epoll]]: know when each applies — do not treat them as interchangeable. vs [[clustering]]: know when each applies — do not treat them as interchangeable. vs [[worker threads]]: know when each applies — do not treat them as interchangeable.

## Mistakes to Avoid

- **`process.nextTick` starvation** — infinite nextTick prevents I/O phase from running. Prefer `setImmediate` for deferral in loops.
- **JSON.parse huge payload on main thread** — blocks like CPU work. Stream or worker.
- **"Async" doesn't mean parallel** — `async/await` still runs continuations on main thread.
- **DNS lookup** — `dns.lookup` uses thread pool; `dns.resolve` uses network — different scaling behavior.
- **API latency spikes globally:** check Event loop delay metric; `clinic bubbleprof`; fix: Find sync/blocking handler; move to worker
- **Timeouts "random" under load:** check Single thread saturated; fix: [[clustering]] or horizontal scale
- **`setImmediate` vs `setTimeout(0)` confusion:** check I/O vs non-I/O context; fix: Use `setImmediate` inside I/O callbacks
- **Memory grows, connections hang:** check Missing `close` handlers; fix: Register cleanup in close phase
- **fs ops queue forever:** check Thread pool exhaustion; fix: Increase `UV_THREADPOOL_SIZE`; use async fs
- **Promises never resolve:** check Microtask deadlock patterns; fix: Avoid nextTick recursion flooding
