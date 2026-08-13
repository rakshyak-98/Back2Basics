<!-- note-strategy: operational -->
[[Operating System]] [[RAM and Swap memory]] [[OOM (Linux Out Of Memory)]] [[cgroup (Control Group)]]

# Heap memory

> Heap memory is the process region for `malloc` / `new` — grows and shrinks at runtime, unlike the fixed stack frames.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** The heap is where your program parks objects that outlive a single function call; the allocator hands out chunks until the OS or runtime says no.

```txt
high addresses
  ┌─────────────┐
  │   Stack     │  ← grows down (locals, return addresses)
  ├─────────────┤
  │     ↕       │  (gap / mmap region)
  ├─────────────┤
  │   Heap      │  ← grows up (malloc / new / GC nursery)
  ├─────────────┤
  │ BSS / Data  │
  ├─────────────┤
  │ Text / Code │
  └─────────────┘
low addresses
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Heap (OS/runtime)** | Dynamic allocation region | “Long-lived objects live on the heap via malloc/new.” |
| **Heap (DSA)** | Min/max tree | “Different word — priority queue, not process memory.” |
| **malloc / brk / mmap** | How the heap grows | “Small allocs use the heap; big ones often mmap.” |
| **Fragmentation** | Free holes too small to reuse | “RSS stays high even after free if the allocator can’t coalesce.” |
| **OOM / heap limit** | Alloc fails or process dies | “JVM has `-Xmx`; Linux may OOM-kill the whole process.” |
| **Leak** | Allocated, never freed / never unreachable | “RSS climbs under load; heap dump shows retained paths.” |

> [!INFO]
> **DSA heap ≠ heap memory.** Priority-queue “heap” is a tree. Runtime “heap” is a virtual-memory region mapped to RAM (and maybe swap). Same English word, different interviews.

### How the story goes (4 steps)

1. **Request** — code calls `malloc` / `new` / language allocator.
2. **Satisfy** — allocator uses free lists, arenas, or asks the kernel (`brk` / `mmap`).
3. **Use** — pointer lives until `free` / GC / process exit.
4. **Fail** — soft limit (ulimit, `-Xmx`, cgroup) or hard RAM pressure → error or [[OOM (Linux Out Of Memory)]].

---

## Standard config / commands

```bash
# Process virtual map — look for [heap] and large anon regions
cat /proc/self/maps | grep -E 'heap|anon'

# RSS / virtual size while reproducing a leak
ps -o pid,rss,vsz,cmd -p <pid>
smem -P <process-name>   # if installed — proportional set size

# glibc malloc stats (C programs linked with glibc)
export MALLOC_CHECK_=3
# or call malloc_stats() / mallinfo2() from a debug path

# Java heap
java -Xms512m -Xmx2g -XX:+HeapDumpOnOutOfMemoryError -jar app.jar

# Container / cgroup memory ceiling (kills look like "random" OOM)
cat /sys/fs/cgroup/memory.max 2>/dev/null || cat /sys/fs/cgroup/memory/memory.limit_in_bytes
```

| Knob | Why it matters |
|------|----------------|
| `ulimit -v` / `RLIMIT_AS` | Caps address space — malloc fails earlier |
| JVM `-Xmx` / Go `GOMEMLIMIT` | Soft app limit before host OOM |
| cgroup `memory.max` | Hard kill in K8s/Docker even if host has RAM |
| `MALLOC_ARENA_MAX` (glibc) | Too many arenas → RSS bloat on many threads |

Debug: `pprof` (Go), `jcmd <pid> GC.heap_info` (Java), `heapdump` / Chrome DevTools (Node).

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `OutOfMemoryError` / alloc failed | Heap dump; `-Xmx` vs RSS | Raise limit **or** cut retained size; don’t guess |
| RSS climbs, never falls | Heap dump / `pmap -x` | Fix leak; GC alone won’t free native/off-heap |
| Works locally, dies in K8s | cgroup `memory.max` vs process RSS | Align requests/limits; leave headroom for native |
| High RSS after free() | Fragmentation / arenas | Tune allocator; reuse pools; check mmap-backed buffers |
| Process killed, no app exception | `dmesg` / `oom_kill` | Host or cgroup OOM — see [[OOM (Linux Out Of Memory)]] |

---

## Gotchas

> [!WARNING]
> **Virtual size ≠ RAM.** A huge `VIRT` with modest `RSS` is often reserved address space, not “using all the RAM.”

> [!WARNING]
> **Free does not always return pages to the OS.** Allocators keep arenas; RSS can stay high after you “freed” everything.

> [!WARNING]
> **Off-heap still counts.** Direct ByteBuffers, JNI, and `mmap` files sit outside the JVM heap but inside the cgroup.

> [!WARNING]
> **Unbounded input → heap bomb.** Trusting client-supplied sizes (`Content-Length`, unzip bombs) is a classic availability kill.

---

## When NOT to use

- **Tiny, short-lived locals** — stack (or registers) is cheaper; don’t heap-allocate every integer.
- **Fixed-size ring of messages** — prefer a bounded [[buffer]] / pool over unbounded heap growth.
- **Sharing huge read-only blobs across processes** — prefer `mmap` / [[shared memory]], not N heap copies.

---

## Related

[[RAM and Swap memory]] [[OOM (Linux Out Of Memory)]] [[cgroup (Control Group)]] [[Stack Frame]] [[Browser memory]] [[buffer]] [[shared memory]]
