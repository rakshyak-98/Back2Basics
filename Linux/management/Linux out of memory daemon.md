[[management]] [[OOM (Linux Out Of Memory)]] [[Linux cgroup]] [[systemd]]

# Linux out of memory daemon

> `systemd-oomd` kills cgroups under memory pressure early — before the global OOM killer picks a random victim.

---

## How it works

```txt
memory.pressure high ──► systemd-oomd ──► kill cgroup
                              │
global OOM killer (last resort, whole machine)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **oomd** | Pressure-based killer | “Acts before global OOM.” |
| **memory.pressure** | PSI stalls | “Time spent waiting on memory.” |
| **ManagedOOM** | Unit opt-in | “systemd properties enable monitoring.” |
| **user.slice** | Per-user cgroup | “Common desktop target.” |
| **vs OOM killer** | Scoped vs global | “oomd prefers contained kills.” |

---


## Configuration and commands

```bash
systemctl status systemd-oomd
systemctl cat systemd-oomd
# unit properties
systemctl show user.slice -p ManagedOOMMemoryPressure,ManagedOOMPreference
journalctl -u systemd-oomd -b
# PSI
cat /proc/pressure/memory
```

| Knob | Why it matters |
|------|----------------|
| `ManagedOOMMemoryPressure=` | When to act |
| `ManagedOOMPreference=` | Avoid/kill priority |

---


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| App dies with little free RAM | oomd logs | Raise limits; fix leak; tune pressure |
| oomd inactive | Distro default off | Enable package/unit |
| Kills wrong service | Preference/slice | Set ManagedOOMPreference=avoid |
| Still global OOM | oomd not covering cgroup | Enable ManagedOOM on slice |

---


## Gotchas

> [!WARNING]
> **Not a substitute for limits** — still set `MemoryMax=` for hard caps.

> [!WARNING]
> **Databases** may prefer swap/throttle over sudden kill — tune carefully.

---


## When not to use

- **Tiny embedded** without PSI — won’t work well.
- **When you need deterministic victim** — prefer explicit cgroup `memory.max`.

---


## Related

[[OOM (Linux Out Of Memory)]] [[Linux cgroup]] [[Memory management]] [[systemd]]

## Sources

- [Wikipedia — Linux out of memory daemon](https://en.wikipedia.org/wiki/Linux_out_of_memory_daemon)
