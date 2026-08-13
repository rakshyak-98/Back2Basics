<!-- note-strategy: operational -->
[[Operating System]] [[critical sections]] [[mutexes]] [[Thread]] [[multi-threaded]] [[shared memory]]

# semaphores

> A semaphore is a counter that lets N waiters into a critical section — others sleep until someone signals.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Think of N identical tickets; `wait` takes a ticket (or sleeps), `signal` returns one (and wakes a waiter).

```txt
semaphore = 3   (three slots)

T1 wait → 2
T2 wait → 1
T3 wait → 0
T4 wait → sleep…
T1 signal → 1  (wakes T4)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Semaphore** | Atomic counter + wait queue | “I use it to limit concurrent access to N resources.” |
| **wait / P / down** | Decrement or block | “Acquire a slot; block if count is zero.” |
| **signal / V / up** | Increment; wake one | “Release a slot; wake a waiter if any.” |
| **Binary semaphore** | Count is only 0 or 1 | “Acts like a lock — but check ownership rules.” |
| **Counting semaphore** | Count can be > 1 | “Connection pool of size 10 is a counting semaphore.” |
| **Mutex** | Lock with ownership | “Prefer a mutex when the same thread must unlock.” |

> [!INFO]
> Semaphores coordinate **who runs now**. They do not move bytes — see [[Inter Process Communication]] / [[shared memory]] for data paths.

### How the story goes (4 steps)

1. **initialize** — create with initial count = number of permits (1 for mutual exclusion, N for a pool).
2. **Enter** — `wait` before the [[critical sections|critical section]].
3. **Work** — touch the shared resource under that permit.
4. **Leave** — `signal` exactly once per successful wait (or you leak permits / deadlock).

---

## Standard config / commands

```c
// POSIX counting semaphore (process-shared example sketch)
sem_t sem;
sem_init(&sem, 0, 3);   // 3 permits, threads in this process
sem_wait(&sem);         // P
// critical work
sem_post(&sem);         // V
sem_destroy(&sem);
```

```bash
# Linux: SysV semaphores still show up in legacy IPC
ipcs -s
ipcrm -s <semid>

# Contended locks / futex waits (related symptoms)
perf top
cat /proc/<pid>/stack
```

| Knob | Why it matters |
|------|----------------|
| Initial count | Wrong init → instant deadlock (0) or no exclusion (too high) |
| Process-shared (`pshared=1`) | Needed across `fork` / shm; must live in shared memory |
| Named semaphores (`sem_open`) | Survive unrelated processes; remember `sem_unlink` |
| Interruptible wait | Signals can spuriously wake — loop on `EINTR` |

Languages: `java.util.concurrent.Semaphore`, Go `chan` buffered of size N, Python `threading.Semaphore`.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Hang / all threads blocked | Who should `signal`? lock order | Find missing `post`; detect deadlock cycles |
| Counter drifts up | Extra `signal` or double release | Pair wait/signal; assert invariants |
| Spurious wake / EINTR | Signal handlers | Retry `sem_wait` in a loop |
| Works with 1 thread, dies with N | Race outside the semaphore | Protect **all** shared writes — see [[critical sections]] |
| IPC sem “leaked” after crash | `ipcs -s` | `ipcrm`; prefer robust POSIX + cleanup |

---

## Gotchas

> [!WARNING]
> **Binary semaphore ≠ mutex.** Mutexes have ownership and often priority inheritance; semaphores do not. Don’t “unlock” from another thread unless that is the design.

> [!WARNING]
> **Lost signal / extra wait** — every successful wait needs exactly one signal path, including error/early-return paths.

> [!WARNING]
> **Priority inversion** — low-priority holder + high-priority waiter without PI mutexes → latency spikes.

> [!WARNING]
> **Busy-wait is not a semaphore.** Spinning burns CPU; use real blocking primitives unless the critical section is tiny and proven.

---

## When NOT to use

- **Simple exclusive lock in one process** — use [[mutexes]]; clearer ownership.
- **Single producer/consumer queue** — prefer a condition variable + mutex, or a channel, over raw sem counting.
- **Distributed systems across machines** — OS semaphores are local; use Redis/etcd/DB locks.

---

## Related

[[critical sections]] [[mutexes]] [[Thread]] [[multi-threaded]] [[thread-safe queue]] [[Inter Process Communication]] [[shared memory]] [[ADT (Abstract Data Type)]]
