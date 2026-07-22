[[NodeJS]] [[Event Loop]] [[worker threads]] [[Node.js run as a non-privileged user]]

# Node.js Clustering

> One-line: fork one process per CPU core to use all cores — each worker has its own event loop; share nothing unless you add Redis/DB.

## Mental model

Node cluster uses `cluster` module (or PM2) to fork **multiple Node processes** bound to the same port via SO_REUSEPORT / master handoff. Each worker is a full V8 isolate — no shared memory between workers.

```
                    ┌─ worker 1 (event loop)
Master (primary) ───┼─ worker 2 (event loop)
                    └─ worker N (event loop)
                           ↑
              OS load-balances incoming connections
```

Fixes **CPU-bound** and **event-loop saturation** on multi-core machines. Does **not** help a single slow request unless you also optimize that handler.

---

## Standard config / commands

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

Default round-robin breaks in-memory session affinity. Options:

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

Coordinate with K8s `terminationGracePeriodSeconds` and load balancer drain.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Only one core busy | `htop` — single node PID hot | Not clustered; use PM2 `-i max` |
| WebSocket drops on reconnect | Different worker each time | Sticky sessions or shared pub/sub (Redis adapter) |
| Memory × N workers | Each fork duplicates heap baseline | Right-size worker count; not always `max` on memory-heavy apps |
| Port EADDRINUSE on fork | Master still holding port incorrectly | Upgrade Node; check custom server.listen logic |
| Worker death loop | Logs on exit code | Fix crash; add refork backoff to avoid fork bomb |

```bash
curl localhost:3000   # repeat — should see different PIDs if clustered
pm2 list
pm2 monit
```

---

## Gotchas

> [!WARNING]
> **In-memory caches are per-worker** — cache hit rate divided by N; use Redis/Memcached.

> [!WARNING]
> **Cluster ≠ threads** — for shared-memory CPU work see [[worker threads]]; cluster is multi-process.

> [!WARNING]
> **File descriptor limits** — N workers × connections each; raise `ulimit -n`.

> [!WARNING]
> **OpenTelemetry/tracing** — propagate trace context; per-process exporters need batching.

---

## When NOT to use

- **I/O-bound API with low CPU** — single process + async I/O may suffice; measure first.
- **Serverless / Lambda** — platform scales instances; cluster inside one invocation is wrong model.
- **Heavy shared state** — redesign for external store before forking.

---

## Related

[[Event Loop]] [[worker threads]] [[Node.js run as a non-privileged user]] [[Express middleware]]
