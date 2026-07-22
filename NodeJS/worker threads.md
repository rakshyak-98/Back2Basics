[[NodeJS]] [[Event Loop]] [[clustering]] [[child process]]

# Node.js Worker Threads

> One-line: true OS threads inside one Node process for CPU-heavy work — share memory optionally via `SharedArrayBuffer`; don't replace cluster for HTTP scaling.

## Mental model

Worker threads run JavaScript (or wasm) **in parallel** with the main thread's event loop. Message passing is default; shared memory is opt-in.

```
Main thread (event loop)  ←postMessage→  Worker thread(s)
        │                                        │
        └── SharedArrayBuffer + Atomics (optional)
```

Unlike [[clustering]] (multi-process), workers share the same process address space (with isolated JS heaps unless shared buffers).

Browser analogue: Web Workers — but Node workers are heavier and can access some Node APIs (`fs`, `crypto` in worker).

---

## Standard config / commands

### Basic worker

```javascript
// main.js
import { Worker } from 'worker_threads';

const worker = new Worker('./worker.js', {
  workerData: { input: largePayload },
});

worker.on('message', (msg) => {
  if (msg.type === 'result') console.log(msg.data);
});
worker.on('error', (err) => console.error(err));
worker.on('exit', (code) => { if (code !== 0) console.error(`Worker stopped ${code}`); });

worker.postMessage({ type: 'compute', data: someData });
```

```javascript
// worker.js
import { parentPort, workerData } from 'worker_threads';

parentPort.on('message', (message) => {
  if (message.type === 'compute') {
    const result = performComputation(message.data);
    parentPort.postMessage({ type: 'result', data: result });
  }
});
```

### Worker pool pattern (CPU tasks)

```javascript
import { Worker } from 'worker_threads';
import os from 'os';

const poolSize = os.cpus().length - 1 || 1;
const workers = [];
const queue = [];

function runTask(data) {
  return new Promise((resolve, reject) => {
    queue.push({ data, resolve, reject });
    dispatch();
  });
}

function dispatch() {
  const idle = workers.find(w => !w.busy);
  const job = queue.shift();
  if (!idle || !job) return;
  idle.busy = true;
  idle.worker.once('message', (msg) => {
    idle.busy = false;
    job.resolve(msg);
    dispatch();
  });
  idle.worker.postMessage(job.data);
}

for (let i = 0; i < poolSize; i++) {
  const w = new Worker('./worker.js');
  workers.push({ worker: w, busy: false });
}
```

### SharedArrayBuffer (high-throughput numeric work)

```javascript
const sab = new SharedArrayBuffer(1024);
const arr = new Int32Array(sab);
// pass sab to worker; synchronize with Atomics.wait / Atomics.notify
```

Requires `--experimental-worker` flags only on very old Node; modern Node is stable. HTTP headers may need `Cross-Origin-Opener-Policy` if serving SAB to browsers — N/A for pure backend.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Worker exits immediately | Uncaught exception in worker | `worker.on('error')`; wrap worker bootstrap in try/catch |
| Main thread still blocks | Heavy work still on main | Move computation into worker file entirely |
| Memory doubles | Large messages copied | Transfer ArrayBuffers; use SharedArrayBuffer |
| `ERR_WORKER_OUT_OF_MEMORY` | Worker heap limit | Split work; increase `--max-old-space-size` sparingly |
| Slower than expected | Worker startup cost | Pool workers; amortize over batch |
| Can't access DOM/db conn | By design | Pass serializable data; use connection pool on main |

---

## Gotchas

> [!WARNING]
> **`postMessage` clones most objects** — expensive for MB payloads. Use transferable `ArrayBuffer` list.

> [!WARNING]
> **Not for every `async` function** — thread overhead ~ms; tiny tasks lose.

> [!WARNING]
> **One crashed worker doesn't kill process** — handle `error`/`exit`; refork in pool.

> [!WARNING]
> **Prisma/native DB drivers** — often main-thread only; don't share connections across threads.

> [!WARNING]
> **vs child_process** — workers lighter than fork; child_process better for isolation (untrusted code).

---

## When NOT to use

- **HTTP request scaling** — use [[clustering]] or horizontal pods.
- **I/O-bound work** — event loop + async I/O is simpler and faster.
- **Untrusted user code** — use separate process/container sandbox, not worker alone.

---

## Related

[[Event Loop]] [[clustering]] [[child process]] [[worker]]
