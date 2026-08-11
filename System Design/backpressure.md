[[System Design]] [[Throughput]] [[race condition]] [[Token bucket]]

# backpressure

> Backpressure — slow consumers force producers to pause, drop, or queue with limits so buffers don’t explode.

---

## Mental model

**Say it in one breath:** Every producer→consumer link needs a policy when the consumer is slower: block, bounded queue, sample/drop, or reject (`429` / `503`).

```txt
Producer → [bounded queue] → Consumer
               ↑ full?
         wait | drop | 429
```

| Strategy | Effect |
|----------|--------|
| Blocking | Simple; can deadlock chains |
| Bounded queue | Absorbs bursts; then policy |
| Load shed | Protect core; degrade UX |
| Credit / window | TCP-like; reactive streams |

---

## Standard config / commands

```js
// Node: respect stream backpressure
const ok = writable.write(chunk)
if (!ok) await once(writable, 'drain')
```

```nginx
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
limit_req zone=api burst=20 nodelay;
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| OOM / huge lag | Unbounded queue | Cap queue; drop/reject |
| Timeouts upstream | Blocked producers | Shed load; scale consumers |
| Uneven pipes | One slow stage | Isolate pools; circuit break |
| `429` storms | Clients retry sync | Jittered backoff |
| Lost messages | Drop policy silent | Metric + DLQ for durables |

---

## Gotchas

> [!WARNING]
> **Infinite Kafka lag “buffering”** — disk is a queue; still backpressure ops (alert, scale, pause producers).

> [!WARNING]
> **Async without limits** — `Promise.all` 1M tasks is a self-DDoS.

> [!WARNING]
> **TCP backpressure ≠ app backpressure** — app can still buffer in user space.

---

## When NOT to use

- **Tiny offline batch** — finish-or-fail is enough.
- **Lossy metrics telemetry** — deliberate sampling is fine.
- **UI animations** — different problem domain.

---

## Related

[[Throughput]] [[Token bucket]] [[race condition]] [[Scaling Throughput in High-load system]]
