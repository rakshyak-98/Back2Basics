<!-- note-strategy: operational -->
[[NodeJS]] [[Packages/npm packages]] [[clustering]]

# node-cron

> In-process cron schedules — fires JS callbacks on a crontab pattern while the Node process is alive.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** `cron.schedule(expr, fn)` runs in memory — not OS cron. Keep the returned task if you ever need `stop()`.

```txt
process up → schedule('* * * * *', fn) → tick → fn()
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **ScheduledTask** | Handle to stop/start | “Lose the ref ⇒ can’t stop cleanly.” |
| **In-process** | Not systemd/cron | “Dies with the process; duplicates with N replicas.” |

## Standard config / commands

```js
import cron from 'node-cron'

const tasks = []
function register(...args) {
  const t = cron.schedule(...args)
  tasks.push(t)
  return t
}

register('*/5 * * * *', () => console.log('tick'))
// shutdown:
tasks.forEach((t) => t.stop())
```

| Knob | Why it matters |
|------|----------------|
| Timezone option | Avoid UTC surprises |
| Registry array | Stop all on SIGTERM |
| Validate expr | `cron.validate` |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Runs N times | N cluster workers | Leader election or external scheduler |
| Can’t stop | Discarded return value | Keep registry |
| Wrong hour | TZ | Set timezone explicitly |
| Overlap | Long job > interval | Mutex / skip-if-running |

---

## Gotchas

> [!WARNING]
> **Multi-instance apps** — every replica runs the job unless you coordinate.

> [!WARNING]
> **Not durable** — process crash misses ticks; use a queue/scheduler for critical jobs.

---

## When NOT to use

- **Clustered / K8s many pods** — use system cron, Cloud Scheduler, or a lock.
- **Exactly-once billing jobs** — need durable job system.

---

## Related

[[Packages/npm packages]] [[clustering]] [[Node.js run as a non-privileged user]]
