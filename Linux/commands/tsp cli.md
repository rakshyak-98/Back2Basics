[[commands]] [[crontab]] [[Linux process commands]]

# tsp cli

> `tsp` (Task Spooler) queues shell jobs on a single machine — simple FIFO/batch without full job schedulers.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** enqueue commands; tsp runs N at a time; `tsp -l` shows queue; outputs land in tsp’s log files.

```txt
tsp cmd… ──► queue ──► worker slots (TSP_NWORKERS)
                 │
                 └─ tsp -c / tsp -o  (cat output)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **tsp** | Local job queue | “Poor man’s batch on one box.” |
| **slot / workers** | Parallelism cap | “`TSP_NWORKERS=2` limits concurrency.” |
| **job id** | Queue handle | “`tsp -i` last id; `tsp -c ID`.” |
| **dependency** | `-D id` wait | “Chain jobs without shell & wait hacks.” |
| **vs cron** | Ad-hoc vs schedule | “tsp is interactive batch; cron is calendar.” |

---

## Standard config / commands

```bash
tsp long_job.sh
tsp -l
tsp -c          # cat last job output
tsp -i          # last job id
tsp -k          # kill last
TSP_NWORKERS=2 tsp heavy.sh
tsp -D 3 ./step2.sh   # after job 3
```

| Knob | Why it matters |
|------|----------------|
| `TSP_NWORKERS` | Max parallel jobs |
| `TS_SOCKET` | Separate queues per project |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Jobs stuck queued | Workers=1 + long job | Raise `TSP_NWORKERS` or kill blocker |
| Output missing | Job still running | `tsp -l`; wait; `tsp -c ID` |
| Wrong queue | Shared socket | Set `TS_SOCKET` per project |
| Command not found | PATH in tsp env | Use absolute paths |

---

## Gotchas

> [!WARNING]
> **Not multi-host** — tsp is local IPC; don’t treat it as Slurm/K8s.

> [!WARNING]
> **Machine reboot clears the queue** — not a durable scheduler.

---

## When NOT to use

- **Cluster / multi-user fair share** — use Slurm, K8s Jobs, or systemd.
- **Calendar schedules** — [[crontab]] / systemd timers.

---

## Related

[[crontab]] [[Linux process commands]] [[supervisorctl]] [[renice]]
