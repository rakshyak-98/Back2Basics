[[Neovim CLI]] [[crontab]] [[Linux process commands]] [[supervisorctl]] [[renice]]

# tsp cli

> Task Spooler (`tsp`) queues shell jobs on one machine — simple FIFO/batch without a full scheduler.

```txt
        tsp cli ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Shows you can pick a local batch queue for ad-hoc heavy jobs without pretendi…

## Sources
- [Task Spooler home](https://viric.name/soft/ts/) — overview
- [Debian package — task-spooler](https://packages.debian.org/task-spooler) — overview

## Key Concepts
- **Local IPC queue:** one host only — not multi-node fair share.
- **Workers (`TSP_NWORKERS`):** caps parallel jobs.
- **Job id:** `tsp -i` last id; `tsp -c ID` cats output.
- **Dependency (`-D id`):** chain jobs without shell wait hacks.
- **vs cron:** tsp is interactive/ad-hoc batch; [[crontab]] is calendar.

## Technical Details
```txt
tsp cmd… ──► queue ──► worker slots (TSP_NWORKERS)
                 │
                 └─ tsp -c / tsp -o  (cat output)
```

```bash
tsp long_job.sh
tsp -l
tsp -c
tsp -i
tsp -k
TSP_NWORKERS=2 tsp heavy.sh
tsp -D 3 ./step2.sh
```

| Knob | Why it matters |
|------|----------------|
| `TSP_NWORKERS` | Max parallel jobs |
| `TS_SOCKET` | Separate queues per project |

| Symptom | Check | Fix |
|---------|-------|-----|
| Jobs stuck queued | Workers=1 + long job | Raise `TSP_NWORKERS` or kill blocker |
| Output missing | Job still running | `tsp -l`; wait; `tsp -c ID` |
| Wrong queue | Shared socket | Set `TS_SOCKET` per project |
| Command not found | PATH in tsp environment | Use absolute paths |

## Mistakes to Avoid
- **Mistake:** Treating tsp as a durable or multi-host scheduler
- **Mistake:** Relying on relative PATH inside queued jobs — use absolute paths

## Pros/Cons or Trade-offs
- **Pro:** Tiny, interactive, dependency-aware on one machine.
- **Con:** Queue dies on reboot; no multi-host scheduling.

## Comparison
- vs [[crontab]] / systemd timers: calendar vs ad-hoc queue.
- vs Slurm/K8s Jobs: those are for clusters and fair share.


### Use cases
- Queue overnight encodes, dataset transforms, or one-box CI-ish batches when y…
