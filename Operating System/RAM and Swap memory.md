[[Operating System]] [[Heap memory]] [[OOM (Linux Out Of Memory)]] [[Memory management]] [[cgroup (Control Group)]]

# RAM and Swap memory

> RAM is fast working memory for live pages; swap is disk-backed overflow so the machine can keep running when RAM is full — slowly.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** The OS gives processes virtual pages; hot pages stay in RAM, cold ones may go to swap, and when RAM is gone the OOM killer or alloc failures take over.

```txt
Process thinks:        Reality:
  virtual pages   →    RAM (fast)  or  Swap (disk, slow)
                              │
                              └─ under pressure: reclaim → swap out → OOM
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **RAM** | Physical DRAM holding live pages | “Working set must fit in RAM for latency.” |
| **Swap** | Disk space used as overflow for pages | “Swap prevents instant death; it does not make more RAM.” |
| **Page** | Fixed-size chunk (often 4 KiB) | “The unit the kernel moves between RAM and swap.” |
| **Working set** | Pages you actually touch | “If working set > RAM, you thrash.” |
| **Anonymous memory** | Heap/stack — not file-backed | “Anon pages go to swap; file pages can be dropped and reread.” |
| **OOM killer** | Kernel picks a process to kill | “Last resort when reclaim cannot free enough.” |

> [!INFO]
> Memory placement ([[RAM and Swap memory]]) is not synchronization ([[semaphores]]). One answers “where does the page live?”; the other answers “who may touch shared state now?”

### How the story goes (4 steps)

1. **Fault** — process touches a virtual address; kernel maps a physical page (or allocates one).
2. **Pressure** — free RAM drops; reclaim starts (drop clean file cache first).
3. **Swap out** — cold anonymous pages written to swap device/file.
4. **Swap in / OOM** — touch again → read from disk (lag), or kill if still stuck — [[OOM (Linux Out Of Memory)]].

---

## Standard config / commands

```bash
free -h
swapon --show
cat /proc/meminfo | egrep 'MemTotal|MemAvailable|SwapTotal|SwapFree|Dirty|Cached'

# Who is using RAM / swap
smem -tk 2>/dev/null || ps aux --sort=-rss | head
grep VmSwap /proc/*/status 2>/dev/null | sort -k2 -n | tail

# Kernel reclaim / swap activity
vmstat 1
sar -B 1 5          # paging stats if sysstat installed
cat /proc/sys/vm/swappiness   # 0–100; higher → more eager to swap

# Add a swap file (lab / emergency — prefer sized disk for prod)
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

| Knob | Why it matters |
|------|----------------|
| `vm.swappiness` | Bias toward reclaiming file cache vs swapping anon |
| Swap size | Too small → earlier OOM; too large → long thrash before death |
| cgroup `memory.max` | Container “RAM” ceiling — swap may be separate (`memory.swap.max`) |
| `MemAvailable` | Better “can I start another job?” signal than free alone |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| System “laggy”, disk busy | `vmstat` si/so columns climbing | Add RAM or cut working set; swap is a symptom |
| Alloc fails / process killed | `dmesg` OOM; `free -h` | Raise memory, lower limits, or fix leak |
| Swap full, RAM not | Huge anon caches / leaks | Find `VmSwap` offenders; restart or patch |
| Container OOM, host fine | cgroup memory.max | Raise limit or shrink app — see [[cgroup (Control Group)]] |
| After deploy, cache dropped | Large streaming reads | Expected; watch `MemAvailable`, not just free |

---

## Gotchas

> [!WARNING]
> **Swap is not capacity planning.** It buys time and avoids hard fails; latency collapses once you thrash.

> [!WARNING]
> **`free` looks “used” because of page cache.** Prefer `MemAvailable`. Cache is reclaimable; anon+swap pressure is not free lunch.

> [!WARNING]
> **Disabled swap + tight cgroup** → sharp OOM kills with little warning. Some prod setups still prefer no swap for predictability — know the trade.

> [!WARNING]
> **Hibernation needs swap ≥ RAM** on many setups. Unrelated to “performance swap,” but ops tickets confuse the two.

---

## When NOT to use

- **Latency-critical in-memory services** — size RAM for the working set; do not “fix with swap.”
- **As a substitute for fixing leaks** — swap hides the leak until the box is unusable.
- **Tiny embedded / real-time** — often no swap device by design.

---

## Related

[[Heap memory]] [[OOM (Linux Out Of Memory)]] [[Memory management]] [[cgroup (Control Group)]] [[Buffer cache]] [[Linux out of memory daemon]]
