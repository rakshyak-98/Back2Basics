[[Memory management]] [[Linux cgroup]] [[management/Linux out of memory daemon]] [[process]] [[Error status code]]

# OOM (Linux Out Of Memory)

> The OOM killer terminates processes when the kernel cannot free enough memory after reclaim — on the whole machine or inside a cgroup that hit its limit.

## Interview Relevance
Core SRE signal: distinguish host OOM from cgroup/container OOM, read `dmesg` kill lines, and explain `oom_score_adj` / exit **137** — not just “add more RAM.”

## Sources
- [OOM Killer — kernel admin guide](https://www.kernel.org/doc/html/latest/admin-guide/mm/oom-killer.html) — deep-dive
- [cgroup v2 memory](https://www.kernel.org/doc/html/latest/admin-guide/cgroup-v2.html) — deep-dive

## Core Definition
When reclaim cannot satisfy an allocation, the kernel picks a victim by **oom_score** (biased by **oom_score_adj**). Global OOM hits the host; cgroup OOM hits only tasks under that `memory.max` / systemd `MemoryMax=`.

## Key Concepts
- **Global vs cgroup OOM:** Same kill mechanism, different scope and logs.
- **oom_score / oom_score_adj:** Higher score dies first; adj −1000…+1000 biases choice.
- **Exit 137:** Often `128 + 9` (SIGKILL) after OOM or explicit kill.
- **Reclaim first:** Page cache and reclaimable slabs go before OOM; thrashing may precede a kill.
- **Userspace oomd:** Can kill earlier under pressure — see [[management/Linux out of memory daemon]].

## Technical Details

```bash
dmesg -T | grep -iE 'oom|killed process'
journalctl -k | grep -i oom
cat /sys/fs/cgroup/<slice>/memory.events   # oom, oom_kill

cat /proc/self/oom_score
cat /proc/self/oom_score_adj
echo -100 | sudo tee /proc/<pid>/oom_score_adj
```

Example kernel line:
```
Out of memory: Killed process 12345 (java) total-vm:... anon-rss:...
```

| Layer | Trigger | Fix |
|-------|---------|-----|
| Container `memory.max` | Usage over cgroup cap | Raise limit or fix leak; heap below cap |
| systemd `MemoryMax=` | Slice over unit limit | Adjust unit; see [[Linux cgroup]] |
| Host global | No RAM + swap left | Add RAM, reduce pressure, swap, kill hog |

## Real-World Applications
Kubernetes `OOMKilled` pods, JVM heaps set above container limits, and “mystery” daemon deaths with empty app logs but clear `dmesg` OOM lines.

## Pros/Cons or Trade-offs
- **Pro:** Protects the machine from total lockup by sacrificing a victim.
- **Con:** Victim choice can be surprising; protecting one process can doom others.
- **Trade-off:** Strict cgroup limits fail fast locally; soft overcommit fails later globally.

## Comparison
vs [[Memory management]]: memory management is the whole reclaim/swap story; OOM is the failure path. vs raising swap: delays OOM but can thrash. vs [[management/Linux out of memory daemon]]: userspace can kill under PSI before hard kernel OOM.

## Mistakes to Avoid
- Blaming the app log when the kill was SIGKILL from OOM (no graceful shutdown).
- Setting `oom_score_adj=-1000` on everything “critical” until nothing can be sacrificed.
- Confusing container OOM (exit 137, cgroup events) with host-wide OOM.
