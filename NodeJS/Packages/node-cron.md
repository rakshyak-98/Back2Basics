[[NodeJS]] [[Packages/npm packages]] [[clustering]] [[Node.js run as a non-privileged user]]

# node-cron

> In-process cron schedules — fires JS callbacks on a crontab pattern while the Node process is alive.

## Interview Relevance

Interviewers use **node-cron** to check whether you can explain the mechanism in plain words and apply it under failure. Expect follow-ups on **ScheduledTask**, **In-process**.

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

## Real-World Applications

In production APIs and tooling, **node-cron** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **Multi-instance apps** — every replica runs the job unless you coordinate; **Not durable** — process crash misses ticks; use a queue/scheduler for critical jobs.

## Pros/Cons or Trade-offs

- **Pro:** Solves the job described above when used in the right layer (In-process cron schedules — fires JS callbacks on a crontab pattern while the No…).
- **Con / when not:** **Clustered / K8s many pods** — use system cron, Cloud Scheduler, or a lock.
- **Con / when not:** **Exactly-once billing jobs** — need durable job system.

## Comparison

vs [[Packages/npm packages]]: know when each applies — do not treat them as interchangeable. vs [[clustering]]: know when each applies — do not treat them as interchangeable. vs [[Node.js run as a non-privileged user]]: know when each applies — do not treat them as interchangeable.

## Mistakes to Avoid

- **Multi-instance apps** — every replica runs the job unless you coordinate.
- **Not durable** — process crash misses ticks; use a queue/scheduler for critical jobs.
- **Runs N times:** check N cluster workers; fix: Leader election or external scheduler
- **Can’t stop:** check Discarded return value; fix: Keep registry
- **Wrong hour:** check TZ; fix: Set timezone explicitly
- **Overlap:** check Long job > interval; fix: Mutex / skip-if-running
