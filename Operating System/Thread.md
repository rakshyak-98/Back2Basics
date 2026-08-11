[[Operating System]] [[process]] [[multi-threaded]] [[mutexes]] [[context switching]]

# Thread

> A thread is one schedulable flow of execution inside a process — threads share memory, processes usually do not.

---

## Mental model

**Say it in one breath:** Same address space, shared fds and heap; each thread has its own stack, registers, and scheduling identity (TID).

```txt
Process (PID)
├─ shared: VA space, fds, cwd, signal dispositions (mostly)
├─ Thread TID 1  stack₁  (main)
├─ Thread TID 2  stack₂
└─ Thread TID 3  stack₃
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Thread** | Schedulable execution context | “Cheapest concurrency that shares memory.” |
| **Process** | Isolation boundary + resources | “Separate VA space — talk via IPC.” |
| **TID** | Thread id (`gettid`) | “Linux schedules tasks; `top -H` shows TIDs.” |
| **Data race** | Unsynchronized shared write/read | “Undefined behavior — use mutex/atomic.” |
| **Mutex / lock** | Exclusive critical section | “Protect shared mutable state.” |
| **N:M / 1:1** | User threads vs kernel tasks | “Linux pthreads are 1:1 tasks today.” |

### Threads vs processes (say this)

| | Threads | Processes |
|--|---------|-----------|
| Memory | Shared by default | Separate (unless shm) |
| Crash blast radius | One bad pointer can kill all | Isolated |
| Create cost | Lower | Higher (still COW-cheap fork) |
| Sync | Locks, atomics | IPC + maybe locks on shm |
| Use when | Parallelism inside one app | Isolation, security, blast radius |

> [!INFO]
> Sharing memory without rules → races. You need [[mutexes]], [[semaphores]], atomics, or ownership discipline. Bugs are often nondeterministic.

---

## Standard config / commands

```bash
# Threads of a PID
ps -L -p <pid> -o pid,tid,psr,stat,pcpu,cmd
top -H -p <pid>
ls /proc/<pid>/task

# Limits
ulimit -u
cat /proc/<pid>/status | grep -E 'Threads|NSpid'

# Contended locks (Linux)
perf top
# futex waits: see [[mutexes]]
```

```c
// pthread sketch
pthread_t t;
pthread_create(&t, NULL, worker, arg);
pthread_join(t, NULL);
```

| Knob | Why it matters |
|------|----------------|
| Thread pool size | Too many → oversubscribe CPUs / mem |
| `GOMAXPROCS` / pool sizes | Runtime mapping to OS threads |
| Stack size (`pthread_attr_setstacksize`) | Overflow vs RSS waste |
| CPU affinity | Cache locality vs flexibility |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| One core hot, others idle | `top -H` / `psr` column | Parallelize or fix global lock |
| All cores hot, no progress | Lock convoy / deadlock | `perf`, thread dump, lock order |
| Random corruption | Shared mutable state | Mutex/atomic; thread sanitizer |
| Memory grows with threads | Stacks + thread-local caches | Cap pool; shrink stack; reuse workers |
| `fork` after threads hang | Only forking thread survives | `exec` soon or `posix_spawn`; no fork in threaded servers |
| Latency spikes | [[context switching]], futex | Fewer threads; batch work; avoid chatty locks |

---

## Gotchas

> [!WARNING]
> **Threads share the heap** — “no IPC needed” also means “no isolation.” One `SIGSEGV` can take down the process.

> [!WARNING]
> **`fork` + threads is a trap** — other threads vanish; held locks stay held. Classic production landmine.

> [!WARNING]
> **More threads ≠ more speed** — past CPU count + blocking I/O needs, you pay contention and switches.

> [!WARNING]
> **Language “threads” differ** — Go goroutines and Java virtual threads multiplex; still grounded on OS threads underneath.

---

## When NOT to use

- **Don’t thread-per-connection at huge C10k** without care — prefer [[Epoll]] / async or a bounded [[thread pool]].
- **Don’t use threads when you need fault isolation** — use processes/containers.
- **Don’t share mutable structures “temporarily” without sync** — temporary becomes prod data races.

---

## Related

[[process]] [[Linux Process Theory]] [[multi-threaded]] [[Single-threaded]] [[thread pool]] [[mutexes]] [[semaphores]] [[critical sections]] [[context switching]] [[Inter Process Communication]] [[SMT threads]] [[Blocking]] [[Epoll]]
