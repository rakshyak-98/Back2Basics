[[NodeJS]] [[Event Loop]] [[clustering]] [[child process]] [[worker]]

# Node.js Worker Threads

> true OS threads inside one Node process for CPU-heavy work — share memory optionally via `SharedArrayBuffer`; don't replace cluster for HTTP scaling.

```txt
        Node.js Worker Thr ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers probe **Node.js Worker Threads** to see if you understand what i…

## Sources
- [Node.js — Worker threads](https://nodejs.org/api/worker_threads.html) — deep-dive
- [Wikipedia — worker threads](https://en.wikipedia.org/wiki/worker_threads) — overview

## Key Concepts
- **Worker threads:** Worker threads run JavaScript (or wasm) **in parallel** with the main thread'…
- **Unlike [[clustering]]:** Unlike [[clustering]] (multi-process), workers share the same process address…
- **Browser analogue:** Browser analogue: Web Workers


- **Core:** Worker threads run JavaScript (or wasm) **in parallel** with the main thread'…

## Technical Details
- Worker threads run JavaScript (or wasm) **in parallel** with the main thread'…
- Message passing is default; shared memory is opt-in.

```
Main thread (event loop)  ←postMessage→  Worker thread(s)
        │                                        │
        └── SharedArrayBuffer + Atomics (optional)
```

- Unlike [[clustering]] (multi-process), workers share the same process address…

- Browser analogue: Web Workers

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

- Requires `--experimental-worker` flags only on very old Node
- HTTP headers may need `Cross-Origin-Opener-Policy` if serving SAB to browsers

## Mistakes to Avoid
- **Mistake:** **`postMessage` clones most objects**
- **Mistake:** **Not for every `async` function**
- **Mistake:** **One crashed worker doesn't kill process**
- **Mistake:** **Prisma/native DB drivers**
- **Mistake:** **vs child_process**
- **Mistake:** **Worker exits immediately:** check Uncaught exception in worker
- **Mistake:** **Main thread still blocks:** check Heavy work still on main
- **Mistake:** **Memory doubles:** check Large messages copied
- **Mistake:** **`ERR_WORKER_OUT_OF_MEMORY`:** check Worker heap limit
- **Mistake:** **Slower than expected:** check Worker startup cost
- **Mistake:** **Can't access DOM/db conn:** check By design

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (true OS threads inside one Node process for CPU-heavy work — share memory option…).
- **Con / when not:** **HTTP request scaling**
- **Con / when not:** **I/O-bound work**
- **Con / when not:** **Untrusted user code**

## Comparison
- vs [[Event Loop]]: know when each applies


### Use cases
- In production APIs and tooling, **worker threads** shows up whenever teams sh…
