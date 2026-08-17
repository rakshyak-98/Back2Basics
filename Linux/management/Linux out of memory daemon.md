[[OOM (Linux Out Of Memory)]] [[Linux cgroup]] [[Memory management]] [[systemd]] [[services/systemd]]

# Linux out of memory daemon

> `systemd-oomd` kills cgroups under memory pressure early — before the global OOM killer picks a blunt victim.

```txt
        Linux out of memor ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Distinguish PSI/`systemd-oomd` (scoped, pressure-based) from the classic glob…

## Sources
- [systemd-oomd(8)](https://www.freedesktop.org/software/systemd/man/latest/systemd-oomd.service.html) — deep-dive
- [PSI — kernel pressure stall information](https://docs.kernel.org/accounting/psi.html) — deep-dive

## Key Concepts
- **memory.pressure (PSI):** time spent stalling on memory.
- **ManagedOOM* properties:** unit/slice opt-in for monitoring and preference.
- **Scoped kills:** prefer killing a cgroup over random global victim.
- **Not a substitute for limits:** still set `MemoryMax=`.

## Technical Details
```txt
memory.pressure high ──► systemd-oomd ──► kill cgroup
                              │
global OOM killer (last resort, whole machine)
```

```bash
systemctl status systemd-oomd
systemctl cat systemd-oomd
systemctl show user.slice -p ManagedOOMMemoryPressure,ManagedOOMPreference
journalctl -u systemd-oomd -b
cat /proc/pressure/memory
```

| Knob | Why it matters |
|------|----------------|
| `ManagedOOMMemoryPressure=` | When to act |
| `ManagedOOMPreference=` | avoid/kill priority |

| Symptom | Check | Fix |
|---------|-------|-----|
| App dies with little free RAM | oomd logs | Raise limits; fix leak; tune pressure |
| oomd inactive | Distro default off | Enable package/unit |
| Kills wrong service | Preference/slice | `ManagedOOMPreference=avoid` |
| Still global OOM | Coverage gap | Enable ManagedOOM on the right slice |

## Mistakes to Avoid
- **Mistake:** Relying on oomd instead of setting memory limits
- **Mistake:** Enabling without reading which slices are covered
- **Mistake:** Expecting it on tiny embedded kernels without PSI

## Pros/Cons or Trade-offs
- **Pro:** Earlier, more contained kills using PSI.
- **Con:** Databases may prefer throttle/swap over sudden kill — tune carefully.

## Comparison
- vs [[OOM (Linux Out Of Memory)]]: global last resort vs pressure-triggered scoped daemon.
- vs hard `memory.max`: deterministic cgroup OOM vs heuristic pressure policy.


### Use cases
- On developer workstations, oomd targets `user.slice` under pressure so one br…
