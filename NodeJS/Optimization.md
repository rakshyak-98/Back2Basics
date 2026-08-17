[[NodeJS]] [[clustering]] [[worker]] [[Event Loop]] [[node debugger]] [[node inspect]]

# Optimization

> Make Node faster and safer under load — find the bottleneck first (CPU, I/O, GC), then cache, cluster, or compress.

```txt
        Optimization ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers use **Optimization** to check whether you can explain the mechan…

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

## Mistakes to Avoid
- **Mistake:** **Micro-optimizing without a profile** — usually wrong bottleneck
- **Mistake:** **Cache without TTL/invalidation**
- **Mistake:** **High lag, 1 core pegged:** check Sync CPU / JSON
- **Mistake:** **Slow DB:** check Query plans; fix: Indexes; pool; cache
- **Mistake:** **Memory climb:** check Heap snapshot
- **Mistake:** **One box saturated:** check Single process; fix: Cluster + LB

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Make Node faster and safer under load — find the bottleneck first (CPU, I/O, GC)…).
- **Con / when not:** **Premature cluster** — fix the hot path first.
- **Con / when not:** **application-level gzip only**

## Comparison
- vs [[clustering]]: know when each applies


### Use cases
- In production APIs and tooling, **Optimization** shows up whenever teams ship…
