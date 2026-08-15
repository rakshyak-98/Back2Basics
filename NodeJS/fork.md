[[NodeJS]] [[child process]] [[spawn]] [[clustering]] [[worker threads]] [[worker]]

# fork

> `child_process.fork()` spawns a **Node.js** child with built-in IPC — use for cluster workers and isolated JS processes; not for arbitrary shell commands.

## Interview Relevance

Interviewers probe **fork** to see if you understand what it does operationally and when it is the wrong tool — not just the definition.

## Sources

- [Node.js — child_process.fork](https://nodejs.org/api/child_process.html#child_processforkmodulepath-args-options) — deep-dive
- [Wikipedia — fork](https://en.wikipedia.org/wiki/fork) — overview

## Core Definition

`fork(modulePath, args, options)` is `spawn('node', [modulePath, ...args])` plus an **`process.send` / `message` IPC channel**. Parent and child both run V8; child gets its own event loop and memory.

## Key Concepts

- `fork(modulePath, args, options)` is `spawn('node', [modulePath, ...args])` plus an **`process.send` / `message` IPC channel**. Parent and child both run V8; child gets its own …
- [[clustering]] uses `fork` under the hood to share server ports via SO_REUSEPORT/scheduling. For non-Node binaries, use [[spawn]].

## Technical Details

`fork(modulePath, args, options)` is `spawn('node', [modulePath, ...args])` plus an **`process.send` / `message` IPC channel**. Parent and child both run V8; child gets its own event loop and memory.

```
Master process                    Worker (fork)
      │                                │
      ├── fork('./worker.js') ────────►│ new Node process
      │◄──── message { type, data } ────│
      └── cluster module uses fork internally
```

[[clustering]] uses `fork` under the hood to share server ports via SO_REUSEPORT/scheduling. For non-Node binaries, use [[spawn]].

### Basic IPC

```javascript
// master.js
import { fork } from 'node:child_process';

const child = fork('./worker.js');

child.on('message', (msg) => {
  if (msg.type === 'result') console.log(msg.value);
});

child.send({ type: 'compute', n: 42 });

child.on('exit', (code, signal) => {
  console.log(`child exited ${code} ${signal}`);
});
```

```javascript
// worker.js
process.on('message', (msg) => {
  if (msg.type === 'compute') {
    process.send({ type: 'result', value: msg.n * 2 });
  }
});
```

### fork options

```javascript
fork('./worker.js', [], {
  env: { ...process.env, WORKER_ID: '1' },
  execArgv: ['--max-old-space-size=512'],
  stdio: ['inherit', 'inherit', 'inherit', 'ipc'], // ipc channel required
  detached: false,
});
```

### Cluster pattern (HTTP)

```javascript
import cluster from 'node:cluster';
import http from 'node:http';

if (cluster.isPrimary) {
  for (let i = 0; i < require('os').cpus().length; i++) cluster.fork();
  cluster.on('exit', (worker) => {
    console.log(`worker ${worker.process.pid} died; reforking`);
    cluster.fork();
  });
} else {
  http.createServer(handler).listen(3000);
}
```

### Graceful shutdown

```javascript
process.on('SIGTERM', () => {
  child.send({ type: 'shutdown' });
  setTimeout(() => child.kill('SIGKILL'), 10_000);
});
```

## Real-World Applications

In production APIs and tooling, **fork** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **IPC messages are not for high throughput** — large payloads copy; use shared storage or [[worker threads]] SharedArrayBuffer; **fork ≠ sandbox** — child can access same user permissions and env secrets.

## Pros/Cons or Trade-offs

- **Pro:** Solves the job described above when used in the right layer (`child_process.fork()` spawns a **Node.js** child with built-in IPC — use for cl…).
- **Con / when not:** **External CLI (git, ffmpeg)** — [[spawn]].
- **Con / when not:** **CPU parallelism inside one request** — [[worker threads]] lighter than process.
- **Con / when not:** **Horizontal scale across machines** — K8s replicas, not fork on one box only.

## Comparison

vs [[child process]]: know when each applies — do not treat them as interchangeable. vs [[spawn]]: `spawn` runs any executable; `fork` is Node-only with built-in IPC. vs [[clustering]]: know when each applies — do not treat them as interchangeable.

## Mistakes to Avoid

- **IPC messages are not for high throughput** — large payloads copy; use shared storage or [[worker threads]] SharedArrayBuffer.
- **fork ≠ sandbox** — child can access same user permissions and env secrets.
- **Orphaned children on parent SIGKILL** — use process groups or init system to reap.
- **`channel closed`:** check Child exited early; fix: Log child stderr; catch bootstrap errors
- **Messages lost:** check Send before `message` listener; fix: Wait for `'online'` or first ping
- **Memory × N workers:** check Each fork full V8 heap; fix: Prefer [[worker threads]] for shared process CPU tasks
- **Port EADDRINUSE in cluster:** check Workers double-bind wrong; fix: Only primary listens or use cluster API
- **Zombie on crash:** check No refork; fix: Primary `cluster.on('exit')` refork with backoff
- **Serialization error:** check Non-cloneable object in send; fix: JSON-safe payloads only (structured clone limits)
