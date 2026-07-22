[[NodeJS]] [[child process]] [[spawn]] [[clustering]]

# fork

> One-line: `child_process.fork()` spawns a **Node.js** child with built-in IPC — use for cluster workers and isolated JS processes; not for arbitrary shell commands.

## Mental model

`fork(modulePath, args, options)` is `spawn('node', [modulePath, ...args])` plus an **`process.send` / `message` IPC channel**. Parent and child both run V8; child gets its own event loop and memory.

```
Master process                    Worker (fork)
      │                                │
      ├── fork('./worker.js') ────────►│ new Node process
      │◄──── message { type, data } ────│
      └── cluster module uses fork internally
```

[[clustering]] uses `fork` under the hood to share server ports via SO_REUSEPORT/scheduling. For non-Node binaries, use [[spawn]].

## Standard config / commands

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

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `channel closed` | Child exited early | Log child stderr; catch bootstrap errors |
| Messages lost | Send before `message` listener | Wait for `'online'` or first ping |
| Memory × N workers | Each fork full V8 heap | Prefer [[worker threads]] for shared process CPU tasks |
| Port EADDRINUSE in cluster | Workers double-bind wrong | Only primary listens or use cluster API |
| Zombie on crash | No refork | Primary `cluster.on('exit')` refork with backoff |
| Serialization error | Non-cloneable object in send | JSON-safe payloads only (structured clone limits) |

## Gotchas

> [!WARNING]
> **IPC messages are not for high throughput** — large payloads copy; use shared storage or [[worker threads]] SharedArrayBuffer.

> [!WARNING]
> **fork ≠ sandbox** — child can access same user permissions and env secrets.

> [!WARNING]
> **Orphaned children on parent SIGKILL** — use process groups or init system to reap.

## When NOT to use

- **External CLI (git, ffmpeg)** — [[spawn]].
- **CPU parallelism inside one request** — [[worker threads]] lighter than process.
- **Horizontal scale across machines** — K8s replicas, not fork on one box only.

## Related

[[child process]] [[spawn]] [[clustering]] [[worker threads]] [[worker]]
