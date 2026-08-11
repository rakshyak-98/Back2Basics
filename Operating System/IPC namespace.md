[[Inter Process Communication]] [[shared memory]] [[UTS namespace]] [[Linux]]

# IPC namespace

> Isolates System V IPC and POSIX message queues — processes in different IPC namespaces cannot see each other's semaphores, shared memory segments, or mq.

---

## Mental model

Linux **IPC namespace** scopes legacy **SysV IPC** (`shmget`, `semget`, `msgget`) and **POSIX mqueues** (`mq_open`):

```txt
Host IPC ns                    Container IPC ns
────────────                   ────────────────
ipcs shows all segments        ipcs shows only container's
/dev/mqueue/* global           separate /dev/mqueue tree
```

Does **not** isolate:
- **Unix domain sockets** (network namespace related for some cases)
- **Pipes** between related processes in same pid namespace
- **Files** on shared mounts

Docker default creates private IPC ns; **`--ipc=host`** shares host SysV — breaks isolation but needed for some legacy SHM apps (Chrome, old DB tooling).

---

## Standard config / commands

### Inspect SysV IPC

```bash
ipcs -a              # all namespaces visible to you
ipcs -m              # shared memory
ipcs -s              # semaphores
ipcs -q              # message queues
```

### Docker / Kubernetes

```bash
docker run --ipc private alpine ipcs -m    # empty
docker run --ipc host alpine ipcs -m       # host segments visible

# K8s: share host IPC (use sparingly)
# securityContext or deprecated pod IPC — prefer explicit volume/socket design
```

### Clean stale segments

```bash
ipcrm -m SHMID
ipcrm -s SEMID
ipcrm -q MSGID
```

### POSIX message queues

```bash
ls /dev/mqueue
mqstat  # if util-linux built with mq support
```

**Why isolation matters:** multi-tenant hosts — leftover SysV keys (`0x00001234`) collide across tenants without namespace separation.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `Invalid argument` on shmget in container | IPC ns + size limits | Increase `shmmax`; `--ipc=host` only if justified |
| Orphan ipcs after crash | `ipcs -m` | Cleanup script; use POSIX `shm_unlink` |
| App works on host, fails in K8s | Expects host SHM | Redesign with memfd/socket; or hostIPC (risk) |
| Key collision | Fixed IPC key in code | Generate unique keys; use `IPC_PRIVATE` |

---

## Gotchas

> [!WARNING]
> **`--ipc=host` is a tenancy hole** — any container can attach to host SysV segments.

> [!WARNING]
> **SysV limits are global per namespace** — `kernel.shmmax`, `shmmni` still apply inside ns.

> [!WARNING]
> **Not all IPC is in IPC ns** — [[shared memory]] via `mmap` of same file works across ns if path shared.

---

## When NOT to use

Greenfield services should prefer **sockets**, **gRPC**, or **memfd** over SysV IPC — IPC namespace exists mainly for legacy compatibility and container isolation.

---

## Related

[[Inter Process Communication]] [[shared memory]] [[UTS namespace]] [[Linux]] [[Docker]]
