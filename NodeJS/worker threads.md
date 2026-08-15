[[NodeJS]] [[Event Loop]] [[clustering]] [[child process]] [[worker]]

# Node.js Worker Threads

> true OS threads inside one Node process for CPU-heavy work — share memory optionally via `SharedArrayBuffer`; don't replace cluster for HTTP scaling.

## Interview Relevance

Interviewers probe **Node.js Worker Threads** to see if you understand what it does operationally and when it is the wrong tool — not just the definition.

## Sources

- [Node.js — Worker threads](https://nodejs.org/api/worker_threads.html) — deep-dive
- [Wikipedia — worker threads](https://en.wikipedia.org/wiki/worker_threads) — overview

## Core Definition

Worker threads run JavaScript (or wasm) **in parallel** with the main thread's event loop. Message passing is default; shared memory is opt-in.

## Key Concepts

- Worker threads run JavaScript (or wasm) **in parallel** with the main thread's event loop. Message passing is default; shared memory is opt-in.
- Unlike [[clustering]] (multi-process), workers share the same process address space (with isolated JS heaps unless shared buffers).
- Browser analogue: Web Workers — but Node workers are heavier and can access some Node APIs (`fs`, `crypto` in worker).

## Technical Details

Worker threads run JavaScript (or wasm) **in parallel** with the main thread's event loop. Message passing is default; shared memory is opt-in.

```
Main thread (event loop)  ←postMessage→  Worker thread(s)
        │                                        │
        └── SharedArrayBuffer + Atomics (optional)
```

Unlike [[clustering]] (multi-process), workers share the same process address space (with isolated JS heaps unless shared buffers).

Browser analogue: Web Workers — but Node workers are heavier and can access some Node APIs (`fs`, `crypto` in worker).

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

## Real-World Applications

In production APIs and tooling, **worker threads** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **`postMessage` clones most objects** — expensive for MB payloads. Use transferable `ArrayBuffer` list; **Not for every `async` function** — thread overhead ~ms; tiny tasks lose.

## Pros/Cons or Trade-offs

- **Pro:** Solves the job described above when used in the right layer (true OS threads inside one Node process for CPU-heavy work — share memory option…).
- **Con / when not:** **HTTP request scaling** — use [[clustering]] or horizontal pods.
- **Con / when not:** **I/O-bound work** — event loop + async I/O is simpler and faster.
- **Con / when not:** **Untrusted user code** — use separate process/container sandbox, not worker alone.

## Comparison

vs [[Event Loop]]: know when each applies — do not treat them as interchangeable. vs [[clustering]]: Workers share process/memory options inside one OS process; cluster forks processes for multi-core HTTP. vs [[child process]]: Child process = separate memory/OS process; worker_threads share some memory via SharedArrayBuffer/MessageChannel.

## Mistakes to Avoid

- **`postMessage` clones most objects** — expensive for MB payloads. Use transferable `ArrayBuffer` list.
- **Not for every `async` function** — thread overhead ~ms; tiny tasks lose.
- **One crashed worker doesn't kill process** — handle `error`/`exit`; refork in pool.
- **Prisma/native DB drivers** — often main-thread only; don't share connections across threads.
- **vs child_process** — workers lighter than fork; child_process better for isolation (untrusted code).
- **Worker exits immediately:** check Uncaught exception in worker; fix: `worker.on('error')`; wrap worker bootstrap in try/catch
- **Main thread still blocks:** check Heavy work still on main; fix: Move computation into worker file entirely
- **Memory doubles:** check Large messages copied; fix: Transfer ArrayBuffers; use SharedArrayBuffer
- **`ERR_WORKER_OUT_OF_MEMORY`:** check Worker heap limit; fix: Split work; increase `--max-old-space-size` sparingly
- **Slower than expected:** check Worker startup cost; fix: Pool workers; amortize over batch
- **Can't access DOM/db conn:** check By design; fix: Pass serializable data; use connection pool on main
