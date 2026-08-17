[[NodeJS/Event Loop]] [[Operating System/Blocking Vs Non-Blocking]] [[javascript/web workers]] [[NodeJS/worker threads]]

# JavaScript concurrency

> JavaScript concurrency — javaScript runtimes (browser, Node) run user code on one thread. "Concurrency" means the runtime interleaves callbacks while waiting on I/O — not parallel

```txt
        JavaScript concurr ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Why It Matters
- **Key signal:** JS concurrency reviews check event loop vs threads

## Sources
- [MDN Web Docs](https://developer.mozilla.org/) — overview

## Key Concepts
- **Note:** JavaScript runtimes (browser, Node) run **user code on one thread**. "Concurr…

```
Main thread:  [JS][JS][  wait I/O  ][JS][microtasks][JS]
                    ↑                    ↑
              long sync loop here     blocks everything
```

| Mechanism | Parallel? | DOM / shared memory |
|-----------|-----------|---------------------|
| **Event loop + async I/O** | No (interleaved) | Main thread only (browser) |
| **Web Workers** | Yes (separate thread) | No DOM; `postMessage` |
| **Worker threads (Node)** | Yes | Shared `ArrayBuffer` optional |
| **`Promise.all` + fetch** | Concurrent I/O, not CPU | Still one JS thread |

- **Note:** Any code that must stay "concurrent" must **yield**

## Technical Details
### Non-blocking I/O pattern (Node)

```javascript
// Good — loop free while DNS + TCP happen in kernel/libuv
const data = await fs.promises.readFile('config.json', 'utf8');

// Bad — freezes event loop for entire read
const data = fs.readFileSync('config.json', 'utf8');
```

### Offload CPU (Node worker_threads)

```javascript
import { Worker } from 'worker_threads';

function runJob(payload) {
  return new Promise((resolve, reject) => {
    const w = new Worker('./heavy.js', { workerData: payload });
    w.on('message', resolve);
    w.on('error', reject);
  });
}
```

### Browser: Web Worker

```javascript
const worker = new Worker('/hash-worker.js');
worker.postMessage(largeBuffer);
worker.onmessage = (e) => console.log(e.data);
```

### Measure event-loop lag (Node)

```javascript
const { monitorEventLoopDelay } = require('perf_hooks');
const h = monitorEventLoopDelay({ resolution: 20 });
h.enable();
setInterval(() => { console.log('p99 ms', h.percentile(99) / 1e6); h.reset(); }, 5000);
```

## Mistakes to Avoid
> [!WARNING]
> `Promise.all` with 10 000 concurrent HTTP calls is "concurrent" but will exhaust sockets and memory — concurrency ≠ unbounded parallelism.

- **Mistake:** **`setTimeout(0)` is not instant**
- **Mistake:** **Microtasks starve I/O:** infinite `Promise.resolve().then(...)…
- **Mistake:** **Node `cluster`:** multi-process for CPU
- **Mistake:** **Atomics / SharedArrayBuffer:** real shared memory

| Symptom | Check | Fix |
|---------|-------|-----|
| API timeouts under load | Event loop blocked | Profile sync fs/crypto/json.parse on huge payloads |
| UI jank / frozen tab | Long task on main thread | Move work to Web Worker; chunk with `requestIdleCallback` |
| `UnhandledPromiseRejection` | Missing `await` / `.catch()` | Always handle async errors |
| High CPU, low throughput | Busy-wait loop | Backoff, queue, or worker pool |
| Works locally, stalls in prod | Larger prod payloads | Stream instead of buffering entire body |

## Pros/Cons or Trade-offs
- CPU-bound parallel pipelines
- Replacing proper backpressure — `async` does not throttle producers.
