[[System Design]] [[orchestration]] [[event-driven]] [[Airflow]]

# autonomous program

> Autonomous program — long-running agent that watches inputs, decides, and acts with little human babysitting (jobs, bots, controllers).

```txt
        autonomous program ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Long-running agent loop: observe → decide → act with idempotency and kill swi…

## Sources
- [Wikipedia — autonomous program](https://en.wikipedia.org/wiki/autonomous_program) — overview

## Key Concepts
- **Observe → decide → act loop:** long-running agent without constant human input.
- **Idempotent actions:** retries and restarts must be safe.
- **Kill switches / budgets:** bound blast radius and spend.
- **Telemetry:** every decision should be auditable.

## Technical Details
### How it works

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

### Configuration and commands

```txt
Hard requirements
[ ] Idempotent actions
[ ] Checkpoint / cursor
[ ] Bounded retries + DLQ
[ ] Circuit breaker on bad deps
[ ] Kill switch / feature flag
```

## Mistakes to Avoid
> [!WARNING]
> **Autonomy without observability** — you won’t know it went rogue.

> [!WARNING]
> **Clock and DST** — cron-like agents misfire; use monotonic schedules.

> [!WARNING]
> **Privileged credentials** — least privilege; short-lived tokens.

---

| Symptom | Check | Fix |
|---------|-------|-----|
| Double actions | Overlap runs | Lease/lock; idempotency |
| Silent stall | No heartbeat metric | Liveness alert; restart |
| Retry storm | No backoff | Jitter; cap attempts |
| Drift from intent | Missing audit | Structured decision logs |
| Unsafe act in prod | No dry-run | Shadow mode first |

---

## Pros/Cons or Trade-offs
- **Human-in-the-loop required by policy** — approval workflows instead.
- **One-shot migrations** — scripts with supervision.
- **Unclear objective** — autonomy amplifies bad goals.

---


- **Pro:** Scales human attention.
- **Con:** Silent wrong actions compound.
- **Trade-off:** autonomy vs mandatory human approval gates.

## Comparison
- vs cron scripts: richer sensing/decision loops vs fixed schedules.
- vs [[event-driven]]: events may trigger autonomous handlers.


### Use cases
- Ops bots, trading agents, and workflow automations that watch queues or metri…
