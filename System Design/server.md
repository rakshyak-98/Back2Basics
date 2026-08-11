[[concurrent connection]] [[System design]] [[Event Loop]] [[Authentication web application]]

# Server

> Long-lived process accepting client requests — **connection model + state strategy** define scale and failure modes.

---

## Mental model

A **server** listens on a **port**, accepts **connections** or **requests**, executes **handlers**, returns responses. Design choices: **thread vs event loop**, **stateless vs session**, **HTTP vs WebSocket/SSE**. Scale = **many concurrent connections** without exhausting **file descriptors** or **memory** ([[concurrent connection]]).

```txt
Client ──► load balancer ──► server pool
                              │
                    accept → handler → DB/cache
                              │
              stateless (JWT) vs session sticky
```

| Model | Examples | Strength |
|-------|----------|----------|
| **Thread-per-request** | Classic Java servlet | Simple blocking I/O |
| **Event loop** | Node, nginx, Go netpoll | High concurrency, low memory |
| **Process pool** | uWSGI, prefork Apache | Isolation |
| **Serverless** | Lambda | No idle cost; cold start |

**Server can upgrade HTTP to SSE** for server-push notifications — one long-lived response stream per client.

---

## Standard config / commands

### Node HTTP server (minimal)

```javascript
const http = require('http');
const server = http.createServer((req, res) => {
  if (req.url === '/health') { res.writeHead(200); return res.end('ok'); }
  // ...
});
server.listen(3000);
```

### Express behind reverse proxy

```javascript
app.set('trust proxy', 1);  // X-Forwarded-For from [[Configuration]] nginx
app.get('/api/user', authMiddleware, handler);
```

### SSE (server-sent events) pattern

```javascript
app.get('/events', (req, res) => {
  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.flushHeaders();
  const interval = setInterval(() => res.write(`data: ${Date.now()}\n\n`), 5000);
  req.on('close', () => clearInterval(interval));
});
```

One-way server→client; for bidirectional use [[webSocket]].

### Session vs stateless

```txt
Stateless: JWT in Authorization header — any server instance ([[stateless]])
Session:   server-side store + session cookie — needs sticky LB or shared Redis
Prefer stateless for horizontal scale unless strong server-side revoke needed
```

### Capacity knobs

```bash
ulimit -n                    # file descriptors — raise for high concurrency
ss -s                        # socket summary
sysctl net.core.somaxconn    # listen backlog
```

### Health checks (load balancer)

```txt
GET /health → 200 quickly (no DB) or /ready → DB ping
Separate liveness vs readiness (Kubernetes pattern)
```

### Graceful shutdown

```txt
SIGTERM → stop accept → drain in-flight → close DB pool → exit
Kubernetes preStop hook + terminationGracePeriodSeconds
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Connection refused | Process down; wrong port | systemd status; bind 0.0.0.0 |
| 502 from LB | Backend unhealthy | /ready failing; OOM kill |
| Slow under load | FD exhaustion | ulimit; connection leak fix |
| Memory climb | Session leak | TTL sessions; stateless JWT |
| SSE duplicates | Multiple tabs | Client reconnect with Last-Event-ID |
| Sticky session miss | LB config | Cookie affinity or shared session store |
| CPU pegged | Sync crypto/blocking | Offload; async I/O ([[Event Loop]]) |

---

## Gotchas

> [!WARNING]
> **Blocking the event loop** — one sync bcrypt stalls all Node clients.

> [!WARNING]
> **Default ulimit 1024** — fine for dev, death for prod traffic spikes.

> [!WARNING]
> **Session in memory** — multi-instance logout/login weirdness.

> [!WARNING]
> **SSE through buffering proxy** — disable nginx `proxy_buffering` for `/events`.

> [!WARNING]
> **Trust proxy misconfig** — IP spoofing on rate limits.

---

## When NOT to use

- **Pure static site** — object storage + CDN, no app server.
- **Heavy GPU transcode** — worker process, not HTTP request thread ([[Encoding]]).
- **Long batch ETL** — job queue worker, not synchronous HTTP server.

---

## Related

[[concurrent connection]] [[System design]] [[Event Loop]] [[stateless]] [[webSocket]] [[Configuration]] [[backpressure]]
