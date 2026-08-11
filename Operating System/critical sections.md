[[Operating System]] [[semaphores]] [[mutexes]] [[multi-threaded]] [[Thread]] [[shared memory]]

# critical sections

> A critical section is the short stretch of code that touches shared state — only one thread (or N, by design) may run it at a time.

---

## Mental model

**Say it in one breath:** Shared data is fine; unsynchronized read/write pairs are not — wrap the dangerous window with a lock or make the update atomic.

```txt
  Thread A                 Thread B
     │                        │
     ├─ lock ─┐               │
     │        │ read/modify   │  (blocked)
     │        │ write         │
     ├─ unlock┘               │
     │                        ├─ lock → …
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Critical section** | Code that needs exclusive (or limited) access | “That’s the region I protect with a mutex.” |
| **Race condition** | Outcome depends on timing | “Two writers interleaved → corrupted invariant.” |
| **Mutual exclusion** | At most one thread inside | “Mutex gives me exclusion for this section.” |
| **Atomic operation** | One indivisible CPU/RMW op | “I can skip a lock if the update is a single atomic.” |
| **Invariant** | Rule that must always hold | “The lock protects the invariant, not ‘the variable’.” |
| **Lock scope** | How much code is inside | “Keep sections small — hold locks briefly.” |

### How the story goes (4 steps)

1. **Identify shared mutable state** — heap object, global, mmap, file descriptor offset, …
2. **Define the invariant** — e.g. “balance ≥ 0”, “list is well-linked”.
3. **Choose a guard** — [[mutexes]], [[semaphores]], atomics, single-thread confinement.
4. **Enter → touch → leave** — no blocking I/O while holding the lock if you can avoid it.

---

## Standard config / commands

```c
pthread_mutex_t m = PTHREAD_MUTEX_INITIALIZER;

pthread_mutex_lock(&m);
// critical section — touch shared struct
pthread_mutex_unlock(&m);
```

```go
var mu sync.Mutex
mu.Lock()
// critical section
mu.Unlock()
```

```bash
# See threads stuck on futex / lock
perf trace -e futex:* -p <pid>
gdb -p <pid>   # info threads; thread apply all bt
```

| Knob | Why it matters |
|------|----------------|
| Lock granularity | Coarse = simple but contention; fine = parallel but deadlock risk |
| Lock ordering | Global order across lock types prevents AB-BA deadlock |
| `try_lock` / timeouts | Avoid infinite hang in watchdogs |
| Reader-writer lock | Many readers OR one writer — not a free speedup |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Corrupt data / heisenbug | Missing lock or wrong scope | Protect every write + dependent read |
| Deadlock | Lock order / `thread apply all bt` | Consistent order; avoid lock A→B and B→A |
| High CPU, little progress | Too much work inside lock | Shrink section; copy under lock, work outside |
| Priority inversion | RT thread blocked on low | Use PI mutexes or redesign |
| “Safe” because single-threaded | Then added workers | Audit globals — see [[multi-threaded]] |

---

## Gotchas

> [!WARNING]
> **Checking then acting is a race** — `if (!map.contains) map.put` needs one critical section (or a concurrent map API).

> [!WARNING]
> **Volatile / atomic ≠ full critical section** — they order one variable; multi-field invariants still need a lock.

> [!WARNING]
> **I/O inside a lock** — turns a 1 µs section into a stall for every waiter.

> [!WARNING]
> **Double-checked locking** — easy to get wrong without correct memory barriers / language rules.

---

## When NOT to use

- **Immutable / thread-local data** — no shared mutable state → no critical section.
- **Single-threaded event loop** — confinement is the model; don’t sprinkle locks “just in case” — see [[Single-threaded]].
- **Cross-machine consistency** — OS locks stop at the host; use a distributed protocol.

---

## Related

[[semaphores]] [[mutexes]] [[multi-threaded]] [[Single-threaded]] [[Thread]] [[thread-safe queue]] [[context switching]] [[atomic ring buffer]]
