[[System Design]] [[orchestration]] [[event-driven]] [[Airflow]]

# autonomous program

> Autonomous program — long-running agent that watches inputs, decides, and acts with little human babysitting (jobs, bots, controllers).

---

## How it works

```txt
loop:
  read signals (queue, sensors, API)
  decide (rules / model)
  act (API, actuators)
  checkpoint + metrics
```

| Kind | Example |
|------|---------|
| Batch worker | Queue consumer |
| Controller | Autoscaler, reconciler (K8s operator) |
| Bot | Alert triage assistant |

---


## Configuration and commands

```txt
Hard requirements
[ ] Idempotent actions
[ ] Checkpoint / cursor
[ ] Bounded retries + DLQ
[ ] Circuit breaker on bad deps
[ ] Kill switch / feature flag
```

---


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| Double actions | Overlap runs | Lease/lock; idempotency |
| Silent stall | No heartbeat metric | Liveness alert; restart |
| Retry storm | No backoff | Jitter; cap attempts |
| Drift from intent | Missing audit | Structured decision logs |
| Unsafe act in prod | No dry-run | Shadow mode first |

---


## Gotchas

> [!WARNING]
> **Autonomy without observability** — you won’t know it went rogue.

> [!WARNING]
> **Clock and DST** — cron-like agents misfire; use monotonic schedules.

> [!WARNING]
> **Privileged credentials** — least privilege; short-lived tokens.

---


## When not to use

- **Human-in-the-loop required by policy** — approval workflows instead.
- **One-shot migrations** — scripts with supervision.
- **Unclear objective** — autonomy amplifies bad goals.

---


## Related

[[orchestration]] [[event-driven]] [[Airflow]] [[backpressure]]

## Sources

- [Wikipedia — autonomous program](https://en.wikipedia.org/wiki/autonomous_program)
