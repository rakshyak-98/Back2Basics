[[critical sections]] [[semaphores]] [[Thread]] [[multi-threaded]] [[context switching]]

# Mutexes

> Mutual-exclusion lock: one holder at a time for a [[critical sections]] — **Kerrisk / concurrent programming canon**.

---

## Mental model

A **mutex** (binary lock) protects shared mutable state. Exactly one thread executes the critical section; others **block** (sleep) or **spin** (burn CPU) waiting.

```txt
Thread A          mutex          Thread B
   │ lock() ──────►[0→1 held]◄──── lock() blocks
   │ critical section
   │ unlock() ────►[1→0 free]────► wakes, acquires
```

**Mutex vs semaphore:** mutex is **ownership** — only the locker may unlock. Counting [[semaphores]] signal resource *pool* size (N connections available).

**Kernel vs userspace:**
- **Pthread mutex** — may use futex: fast path in userspace atomic, syscall only on contention.
- **Go `sync.Mutex`** — similar; don't copy if locked.
- **Java `synchronized` / `ReentrantLock`** — JVM monitors + optional fairness.
- **Spin mutex** — for **very** short sections on multi-core; wrong choice → wasted CPU + cache line bouncing.

**Priority inversion (brief):** high-priority thread waits on mutex held by low-priority thread while medium-priority threads run — high priority starves. Fix: priority inheritance mutex (PI mutex), or reduce lock scope / lock ordering.

---

## Standard config / commands

### POSIX pattern

```c
pthread_mutex_t mu = PTHREAD_MUTEX_INITIALIZER;
pthread_mutex_lock(&mu);
/* critical section — keep tiny */
pthread_mutex_unlock(&mu);
```

```c
// Prefer PI mutex for real-time / mixed-priority workloads
pthread_mutexattr_t attr;
pthread_mutexattr_init(&attr);
pthread_mutexattr_setprotocol(&attr, PTHREAD_PRIO_INHERIT);
pthread_mutex_init(&mu, &attr);
```

### Go / Java (service code)

```go
var mu sync.Mutex
mu.Lock()
defer mu.Unlock()
// Never lock while holding lock and calling foreign code that may callback
```

```java
private final ReentrantLock lock = new ReentrantLock();
lock.lock();
try { /* ... */ } finally { lock.unlock(); }
```

### Debug contention in production

```shell
# Linux: which threads block on futex
perf record -g -p PID -- sleep 30
perf report | grep -i futex

# strace mutex storms (noisy — lab only)
strace -e futex -p PID

# Java
jcmd PID Thread.print
# or async-profiler lock profiling

# Go
go tool pprof http://localhost:6060/debug/pprof/mutex
```

**Lock ordering discipline:** document global order `A → B → C`; violating it causes deadlock. Tools find *contention*, not logic deadlocks — code review + timeouts where appropriate.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Throughput flat despite more cores | `perf top`; mutex profile; CPU in `futex` | Shrink critical section; sharding; lock-free structures; `RWMutex` for read-heavy |
| Latency p99 spikes, low CPU | Blocked threads; lock holder slow I/O inside lock | Never I/O or RPC under mutex; move work outside |
| Rare hang | Deadlock (A waits B, B waits A) | Lock ordering; `tryLock` + timeout; dump stacks |
| CPU 100%, little progress | Spin lock on contended path | Switch to blocking mutex or redesign |
| RT thread misses deadline | Priority inversion | PI mutex; isolate RT threads; reduce sharing |
| After scale-out, worse on many cores | False sharing on mutex cache line | Padding; per-shard locks; `sync.Map` / concurrent maps |

---

## Gotchas

> [!WARNING]
> **False sharing:** mutex internal state sits on one cache line; every lock/unlock invalidates other cores' lines if adjacent hot variables share the line. Separate hot counters from lock metadata (padding).

> [!WARNING]
> **Hold lock across I/O** — classic production bug. DB query inside `synchronized` block freezes all other request threads.

> [!WARNING]
> **Reentrancy:** POSIX default mutex is **not** recursive — double-lock deadlocks self. Java `ReentrantLock` allows re-entry; know your API.

> [!WARNING]
> **`defer unlock` panic path:** Go defer runs on panic — good. C unlock on error branches — easy to forget.

> [!WARNING]
> **Node is mostly single-threaded** — JS mutex is rare; cross-process locks (Redis Redlock) have their own failure modes. Don't port Java locking patterns blindly to event-loop code.

**Connection pools:** pool *is* a semaphore/mutex hybrid — "take connection" blocks like mutex on empty pool.

---

## When NOT to use

- Don't mutex a read-mostly map — use RCU, immutable snapshots, or sharded locks.
- Don't replace DB transactions with app mutexes across processes — use ACID + row locks.
- Don't spin-lock around anything that may take > ~few hundred nanoseconds routinely.

---

## Related

[[semaphores]] [[critical sections]] [[Thread]] [[thread-safe queue]] [[context switching]] [[atomic ring buffer]] [[multi-threaded]]
