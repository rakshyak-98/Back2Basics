[[NodeJS]] [[Event Loop]] [[worker threads]] [[Node.js run as a non-privileged user]] [[Express middleware]]

# Node.js Clustering

> Node.js Clustering — node cluster uses cluster module (or PM2) to fork multiple Node processes bound to the same port via SO_REUSEPORT / master handoff. Each

```txt
        Node.js Clustering ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers probe **Node.js Clustering** to see if you understand what it do…

## Sources
- [Node.js — Cluster](https://nodejs.org/api/cluster.html) — deep-dive
- [Wikipedia — clustering](https://en.wikipedia.org/wiki/clustering) — overview

## Key Concepts
- **Node cluster:** Node cluster uses `cluster` module (or PM2) to fork **multiple Node processes…
- **Fixes:** CPU-bound**:** Fixes **CPU-bound** and **event-loop saturation** on multi-cor…


- **Core:** Node cluster uses `cluster` module (or PM2) to fork **multiple Node processes…

## Technical Details
- Node cluster uses `cluster` module (or PM2) to fork **multiple Node processes…
- Each worker is a full V8 isolate — no shared memory between workers.

```
                    ┌─ worker 1 (event loop)
Master (primary) ───┼─ worker 2 (event loop)
                    └─ worker N (event loop)
                           ↑
              OS load-balances incoming connections
```

- Fixes **CPU-bound** and **event-loop saturation** on multi-core machines.
- Does **not** help a single slow request unless you also optimize that handler.

### Minimal cluster module

```javascript
import cluster from 'cluster';
import os from 'os';
import http from 'http';

if (cluster.isPrimary) {
  const cpus = os.cpus().length;
  console.log(`Primary ${process.pid} forking ${cpus} workers`);
  for (let i = 0; i < cpus; i++) cluster.fork();

  cluster.on('exit', (worker, code) => {
    console.log(`Worker ${worker.process.pid} exited (${code}), reforking`);
    cluster.fork();
  });
} else {
  http.createServer((req, res) => {
    res.end(`Worker ${process.pid}\n`);
  }).listen(3000);
}
```

### Production: PM2 cluster mode

```bash
pm2 start app.js -i max              # one worker per CPU
pm2 start app.js -i 4                # explicit count
pm2 reload app                        # zero-downtime reload
```

```javascript
// ecosystem.config.cjs
module.exports = {
  apps: [{
    name: 'api',
    script: 'dist/server.js',
    instances: 'max',
    exec_mode: 'cluster',
    listen_timeout: 10000,
    kill_timeout: 5000,
  }],
};
```

### Sticky sessions (WebSocket / session in memory)

- Default round-robin breaks in-memory session affinity.

- Store session in Redis/DB (preferred)
- `sticky-session` with `@socket.io/sticky` or nginx `ip_hash`
- Don't cluster — single process + vertical scale (limited)

### Graceful shutdown

```javascript
process.on('SIGTERM', () => {
  server.close(() => process.exit(0));
  setTimeout(() => process.exit(1), 10000).unref();
});
```

- Coordinate with K8s `terminationGracePeriodSeconds` and load balancer drain.

## Mistakes to Avoid
- **Mistake:** **In-memory caches are per-worker**
- **Mistake:** **Cluster ≠ threads**
- **Mistake:** **File descriptor limits**
- **Mistake:** **OpenTelemetry/tracing**
- **Mistake:** **Only one core busy:** check `htop`
- **Mistake:** **WebSocket drops on reconnect:** check Different worker each ti…
- **Mistake:** **Memory × N workers:** check Each fork duplicates heap baseline
- **Mistake:** **Port EADDRINUSE on fork:** check Master still holding port inc…
- **Mistake:** **Worker death loop:** check Logs on exit code

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Node.js Clustering — node cluster uses cluster module (or PM2) to fork multiple …).
- **Con / when not:** **I/O-bound API with low CPU**
- **Con / when not:** **Serverless / Lambda**
- **Con / when not:** **Heavy shared state**

## Comparison
- vs [[Event Loop]]: know when each applies


### Use cases
- In production APIs and tooling, **clustering** shows up whenever teams ship N…
