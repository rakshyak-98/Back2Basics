[[NodeJS]] [[Packages/npm packages]] [[clustering]] [[Node.js run as a non-privileged user]]

# node-cron

> In-process cron schedules — fires JS callbacks on a crontab pattern while the Node process is alive.

```txt
        node-cron ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers use **node-cron** to check whether you can explain the mechanism…

## Sources
- [node-cron](https://github.com/node-cron/node-cron) — deep-dive
- [Wikipedia — node-cron](https://en.wikipedia.org/wiki/node-cron) — overview

## Key Concepts
- **ScheduledTask:** Handle to stop/start — Lose the ref ⇒ can’t stop cleanly.
- **In-process:** Not systemd/cron — Dies with the process; duplicates with N replicas.

## Technical Details
```txt
process up → schedule('* * * * *', fn) → tick → fn()
```

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

## Mistakes to Avoid
- **Mistake:** **Multi-instance apps**
- **Mistake:** **Not durable**
- **Mistake:** **Runs N times:** check N cluster workers
- **Mistake:** **Can’t stop:** check Discarded return value; fix: Keep registry
- **Mistake:** **Wrong hour:** check TZ; fix: Set timezone explicitly
- **Mistake:** **Overlap:** check Long job > interval

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (In-process cron schedules — fires JS callbacks on a crontab pattern while the No…).
- **Con / when not:** **Clustered / K8s many pods**
- **Con / when not:** **Exactly-once billing jobs** — need durable job system.

## Comparison
- vs [[Packages/npm packages]]: know when each applies


### Use cases
- In production APIs and tooling, **node-cron** shows up whenever teams ship No…
