[[runtime]] [[file descriptors]] [[Heap memory]]

# Take snapshot

> Capture process memory or execution state at a point in time — for debugging, profiling, or checkpoint/restore.

---

## Mental model

A **snapshot** freezes state so you can inspect offline or resume later:

```txt
live process ──snapshot──► artifact (core dump, heap dump, VM snapshot, disk image)
                                    │
                                    └── analyze without reproducing prod traffic
```

Common snapshot types:

| Type | Artifact | Use case |
|------|----------|----------|
| **Core dump** | `core` file | Post-mortem C/C++/Go crash |
| **Heap dump** | `.heapsnapshot`, HPROF | Memory leak in Node/Java |
| **Debugger pause** | live inspection | Break at init (`--inspect-brk`) |
| **VM / container snapshot** | CRIU, VM save | Fast restart, migration |
| **DB snapshot** | LVM/ZFS/EBS snapshot | Point-in-time recovery |

Snapshots trade **disk space and pause time** for **debuggability**.

---

## Standard config / commands

### Node.js — break before runtime executes user code

```bash
node --inspect-brk app.js
# Debugger attaches → then resumes into main
```

### Node.js — heap snapshot

```bash
kill -USR2 PID    # if --heapsnapshot-near-heap-limit or programmatic API
# Or Chrome DevTools → Memory → Take snapshot
```

### Linux core dumps

```bash
ulimit -c unlimited
echo '/tmp/core.%e.%p' | sudo tee /proc/sys/kernel/core_pattern
# Reproduce crash → gdb ./app /tmp/core.app.PID
```

```bash
# systemd service
# [Service] LimitCORE=infinity
```

### CRIU (process checkpoint)

```bash
criu dump -t PID -D /snap/dir --shell-job
criu restore -D /snap/dir
```

### Block storage snapshot (DB on disk)

```bash
# LVM
lvcreate -L1G -s -n db_snap /vg/db_lv
# AWS: EBS snapshot via console/CLI — crash-consistent unless app quiesced
```

**Why quiesce:** file-system snapshot without `fsync`/DB freeze may be **crash-consistent** but not **transaction-consistent**.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Empty or truncated core | `ulimit -c`; `core_pattern` | Raise limit; writable path; `/apport` intercept on Ubuntu |
| Heap snapshot OOMs the process | Snapshot size ≈ heap | Take from replica; use sampling profilers |
| CRIU restore fails | TCP connections, devices | `--tcp-established`; avoid GPU/inotify-heavy apps |
| DB corrupt after restore | No flush before snap | Use DB-native backup + WAL; freeze writes |

---

## Gotchas

> [!WARNING]
> **Heap snapshots contain secrets** — tokens, PII in strings. Treat like production data; redact before sharing.

> [!WARNING]
> **Stop-the-world pauses** — large heapsnapshot or full GC for HPROF stalls the service.

> [!WARNING]
> **EBS/LVM snapshot ≠ SQL backup** — replay WAL or use `pg_basebackup` / native tools for logical consistency.

---

## When NOT to use

Do not snapshot instead of proper logging/metrics for routine ops. Snapshots are for **incidents**, capacity planning, or migration — not continuous telemetry.

---

## Related

[[runtime]] [[Heap memory]] [[file descriptors]] [[fsync]] [[Persistent Block Storage]]
