[[NodeJS]] [[Epoll]] [[clustering]] [[worker threads]] [[Express middleware]] [[child process]] [[Node events driven]]

# Node.js Event Loop

> Node event loop — one JS thread plus libuv; never block it with heavy sync work.

```txt
        Node.js Event Loop ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers use the event loop to test whether you know Node is one JS threa…

## Sources
- [Node.js — The Node.js Event Loop](https://nodejs.org/en/learn/asynchronous-work/event-loop-timers-and-nexttick) — deep-dive
- [Node.js — monitorEventLoopDelay](https://nodejs.org/api/perf_hooks.html#perf_hooksmonitoreventloopdelayoptions) — overview
- [Wikipedia — Event Loop](https://en.wikipedia.org/wiki/Event_Loop) — overview

## Key Concepts
- **Single JS thread:** your callbacks run one at a time
- **libuv + phases:** timers → pending → poll → check → close; I/O readiness drives the poll phase.
- **Thread pool:** default 4 workers for some fs/crypto/dns
- **Microtasks:** `process.nextTick` then Promise jobs run between phases


- **Core:** Node runs user JavaScript on **one thread**

## Technical Details
- Node runs user JavaScript on **one thread**.
- libuv handles async I/O (network, fs, timers) via the event loop and a **thre…
- When a callback runs, nothing else runs until it returns.

```
┌─────────────┐     poll OS (epoll)     ┌──────────────┐
│  Event Loop │ ◄────────────────────── │    libuv     │
│  (6 phases) │ ──► run JS callbacks ──►│ thread pool  │
└─────────────┘                         └──────────────┘
       ▲
       └── microtasks (nextTick, Promises) between phases
```

- **Concurrency is cooperative:** — long handlers delay every connection.
- Throughput ≠ parallel CPU.

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

- Break long sync loops:

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

- **Microtasks:** (outside phases, highest priority): `process.nextTick` runs be…

- Order within tight code:

```javascript
setTimeout(() => console.log('timeout'), 0);
setImmediate(() => console.log('immediate'));
process.nextTick(() => console.log('nextTick'));
Promise.resolve().then(() => console.log('promise'));
// sync first, then nextTick, promise, then timeout/immediate (order of latter two varies by context)
```

## Mistakes to Avoid
- **Mistake:** **`process.nextTick` starvation**
- **Mistake:** **JSON.parse huge payload on main thread**
- **Mistake:** **"Async" doesn't mean parallel**
- **Mistake:** **DNS lookup**
- **Mistake:** **API latency spikes globally:** check Event loop delay metric
- **Mistake:** **Timeouts "random" under load:** check Single thread saturated
- **Mistake:** **`setImmediate` vs `setTimeout(0)` confusion:** check I/O vs no…
- **Mistake:** **Memory grows, connections hang:** check Missing `close` handle…
- **Mistake:** **fs ops queue forever:** check Thread pool exhaustion
- **Mistake:** **Promises never resolve:** check Microtask deadlock patterns

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Node event loop — one JS thread plus libuv; never block it with heavy sync work.).
- **Con / when not:** **CPU-bound monolith on one Node process**
- **Con / when not:** **`setInterval` for critical scheduling**

## Comparison
- vs [[Epoll]]: know when each applies


### Use cases
- In production APIs and tooling, **Event Loop** shows up whenever teams ship N…
