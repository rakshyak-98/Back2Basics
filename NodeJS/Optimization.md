[[NodeJS]] [[clustering]] [[worker]] [[Event Loop]] [[node debugger]]

# Optimization

> Make Node faster and safer under load — find the bottleneck first (CPU, I/O, GC), then cache, cluster, or compress.

---

## Mental model

**Say it in one breath:** Profile before tuning. Event-loop delay ⇒ CPU/sync work; high latency with idle CPU ⇒ I/O/DB; multi-core idle ⇒ scale out processes.

```txt
measure → locate (loop / DB / GC) → fix (async, cache, cluster, CDN)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Event-loop lag** | JS thread busy | “Sync work or huge JSON kills p99.” |
| **Cluster / LB** | Multi-process | “One loop ≈ one core.” |
| **Cache** | Skip repeat work | “Redis/HTTP cache before rewriting code.” |

## Standard config / commands

```bash
node --prof app.js
npx clinic doctor -- node app.js
npx autocannon -c 100 -d 20 http://localhost:3000
```

```js
// gzip at reverse proxy or app
app.use(compression())
```

| Knob | Why it matters |
|------|----------------|
| clinic / `--prof` | Find hot functions |
| [[clustering]] / PM2 | Use cores |
| Redis / HTTP cache | Cut DB and origin load |
| Nginx gzip | Smaller responses |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| High lag, 1 core pegged | Sync CPU / JSON | Async; [[worker]]; stream |
| Slow DB | Query plans | Indexes; pool; cache |
| Memory climb | Heap snapshot | Bound caches; fix leaks |
| One box saturated | Single process | Cluster + LB |

---

## Gotchas

> [!WARNING]
> **Micro-optimizing without a profile** — usually wrong bottleneck.

> [!WARNING]
> **Cache without TTL/invalidation** — serves stale or grows forever.

---

## When NOT to use

- **Premature cluster** — fix the hot path first.
- **application-level gzip only** — often better at the edge/proxy.

---

## Related

[[clustering]] [[worker]] [[Event Loop]] [[node inspect]]
