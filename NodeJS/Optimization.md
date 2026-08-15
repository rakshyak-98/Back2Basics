[[NodeJS]] [[clustering]] [[worker]] [[Event Loop]] [[node debugger]] [[node inspect]]

# Optimization

> Make Node faster and safer under load — find the bottleneck first (CPU, I/O, GC), then cache, cluster, or compress.

## Interview Relevance

Interviewers use **Optimization** to check whether you can explain the mechanism in plain words and apply it under failure. Expect follow-ups on **Event-loop lag**, **Cluster / LB**, **Cache**.

## Sources

- [Node.js — Diagnostics / profiling](https://nodejs.org/en/learn/diagnostics/) — overview
- [clinic.js](https://clinicjs.org/) — overview

## Key Concepts

- **Event-loop lag:** JS thread busy — Sync work or huge JSON kills p99.
- **Cluster / LB:** Multi-process — One loop ≈ one core.
- **Cache:** Skip repeat work — Redis/HTTP cache before rewriting code.

## Technical Details

```txt
measure → locate (loop / DB / GC) → fix (async, cache, cluster, CDN)
```

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

## Real-World Applications

In production APIs and tooling, **Optimization** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **Micro-optimizing without a profile** — usually wrong bottleneck; **Cache without TTL/invalidation** — serves stale or grows forever.

## Pros/Cons or Trade-offs

- **Pro:** Solves the job described above when used in the right layer (Make Node faster and safer under load — find the bottleneck first (CPU, I/O, GC)…).
- **Con / when not:** **Premature cluster** — fix the hot path first.
- **Con / when not:** **application-level gzip only** — often better at the edge/proxy.

## Comparison

vs [[clustering]]: know when each applies — do not treat them as interchangeable. vs [[worker]]: know when each applies — do not treat them as interchangeable. vs [[Event Loop]]: know when each applies — do not treat them as interchangeable.

## Mistakes to Avoid

- **Micro-optimizing without a profile** — usually wrong bottleneck.
- **Cache without TTL/invalidation** — serves stale or grows forever.
- **High lag, 1 core pegged:** check Sync CPU / JSON; fix: Async; [[worker]]; stream
- **Slow DB:** check Query plans; fix: Indexes; pool; cache
- **Memory climb:** check Heap snapshot; fix: Bound caches; fix leaks
- **One box saturated:** check Single process; fix: Cluster + LB
