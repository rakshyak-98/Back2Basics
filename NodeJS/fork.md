[[NodeJS]] [[child process]] [[spawn]] [[clustering]] [[worker threads]] [[worker]]

# fork

> `child_process.fork()` spawns a **Node.js** child with built-in IPC — use for cluster workers and isolated JS processes; not for arbitrary shell commands.

```txt
        fork ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers probe **fork** to see if you understand what it does operational…

## Sources
- [Node.js — child_process.fork](https://nodejs.org/api/child_process.html#child_processforkmodulepath-args-options) — deep-dive
- [Wikipedia — fork](https://en.wikipedia.org/wiki/fork) — overview

## Key Concepts
- **`fork(modulePath, args:** `fork(modulePath, args, options)` is `spawn('node', [modulePath, ...args])` p…
- **[[clustering]] uses:** [[clustering]] uses `fork` under the hood to share server ports via SO_REUSEP…


- **Core:** `fork(modulePath, args, options)` is `spawn('node', [modulePath, ...args])` p…

## Technical Details
- `fork(modulePath, args, options)` is `spawn('node', [modulePath, ...args])` p…
- Parent and child both run V8; child gets its own event loop and memory.

```
Master process                    Worker (fork)
      │                                │
      ├── fork('./worker.js') ────────►│ new Node process
      │◄──── message { type, data } ────│
      └── cluster module uses fork internally
```

- [[clustering]] uses `fork` under the hood to share server ports via SO_REUSEP…
- For non-Node binaries, use [[spawn]].

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

## Mistakes to Avoid
- **Mistake:** **IPC messages are not for high throughput**
- **Mistake:** **fork ≠ sandbox**
- **Mistake:** **Orphaned children on parent SIGKILL**
- **Mistake:** **`channel closed`:** check Child exited early
- **Mistake:** **Messages lost:** check Send before `message` listener
- **Mistake:** **Memory × N workers:** check Each fork full V8 heap
- **Mistake:** **Port EADDRINUSE in cluster:** check Workers double-bind wrong
- **Mistake:** **Zombie on crash:** check No refork
- **Mistake:** **Serialization error:** check Non-cloneable object in send

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (`child_process.fork()` spawns a **Node.js** child with built-in IPC — use for cl…).
- **Con / when not:** **External CLI (git, ffmpeg)** — [[spawn]].
- **Con / when not:** **CPU parallelism inside one request**
- **Con / when not:** **Horizontal scale across machines**

## Comparison
- vs [[child process]]: know when each applies


### Use cases
- In production APIs and tooling, **fork** shows up whenever teams ship Node/JS…
