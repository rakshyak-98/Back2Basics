`top` = real-time process monitor (CPU, RAM, load)

```bash
top -bn1 | grep "%Cpu"
mpstat 1; # only view cpu usage every 1s
vmstat;
```

---

## Core layout (mental model)
- **Header** → system stats (load avg, CPU %, RAM)
- **Process table** → per-process metrics

---

## Navigation (interactive keys)

### Process control

- `k` → kill process (enter PID)
- `r` → [[renice]] (change priority)

### Sorting (most important)

- `P` → sort by CPU
- `M` → sort by memory
- `N` → sort by PID
- `T` → sort by runtime
### View tuning

- `c` → toggle full command vs program name
- `t` → toggle CPU stats view
- `m` → toggle memory stats
- `l` → toggle load avg

### Refresh / exit

- `q` → quit
- `d` → change refresh interval (seconds)
- `space` → manual refresh

---

## Filtering (important for real usage)

- `u` → show processes by user
- `o` → add filter (advanced)
- `O` → manage fields

---

## Threads / hierarchy

- `H` → show threads
- `V` → tree view (parent-child)

---

## Fields (must know)

- `PID` → process id
- `USER` → owner
- `%CPU` → CPU usage
- `%MEM` → memory usage
- `RES` → actual RAM used
- `VIRT` → total allocated memory
- `TIME+` → CPU time consumed
- `COMMAND` → process name

---

## Practical workflow (how engineers use it)

### 1. Find high CPU process

```
top → press P
```

### 2. Find memory leak

```
top → press M
```

### 3. Kill stuck process

```
top → k → enter PID → 9
```

### 4. Inspect full command

```
press c
```

---

## Optimization tricks

- Use `htop` instead → better UX
    
- Combine with:
    

```
ps aux --sort=-%mem | head
ps aux --sort=-%cpu | head
```

---

## Edge cases / gotchas

- `%CPU > 100` → multi-core usage
    
- `load avg` ≠ CPU % → includes waiting tasks
    
- zombie process (`Z`) → already dead, waiting parent cleanup
    
- high `VIRT` ≠ actual memory issue → check `RES`
    

---

## Mental shortcut

- CPU issue → `P`
- Memory issue → `M`
- Kill → `k`
- Inspect → `c`

---

If you want, I can give:
- `top` vs `htop` vs `atop` comparison
- or real debugging scenarios (production-level usage)

## Check system load

Run:

```bash
top
```

### CPU usage

Look at the `%Cpu(s)` line:

```text
%Cpu(s):  5.2 us, 2.1 sy, 0.0 ni, 91.8 id, 0.5 wa, 0.0 hi, 0.1 si, 0.0 st
```

- `us` → User processes
    
- `sy` → Kernel/system
    
- `id` → Idle (higher = less CPU load)
    
- `wa` → Waiting for I/O (high value may indicate disk bottleneck)
    

**CPU utilization = `100 - id`**

---

### RAM usage

Look at the `MiB Mem` (or `GiB Mem`) line:

```text
MiB Mem :  15884.0 total, 1200.0 free, 6200.0 used, 8484.0 buff/cache
```

Important values:

- `total` → Total RAM
    
- `used` → RAM in use
    
- `free` → Completely free RAM
    
- `buff/cache` → Linux cache (can be reclaimed if needed)
    

---

### Load Average

Top-right corner:

```text
load average: 0.45, 0.60, 0.72
```

These are the average system load over:

- 1 minute
    
- 5 minutes
    
- 15 minutes
    

Compare the load to your CPU core count.

Check core count:

```bash
nproc
```

Example:

- `nproc` → `8`
    
- Load `2.5` → Light load
    
- Load `8.0` → Fully utilized
    
- Load `12.0` → Overloaded (more runnable tasks than CPU cores)
    

---

### Sort processes

While `top` is running:

- `P` → Sort by CPU usage
    
- `M` → Sort by RAM usage
    
- `T` → Sort by CPU time
    
- `1` → Show usage for each CPU core
    
- `q` → Quit
    

---

### Summary

| What                  | Where in `top`         |
| --------------------- | ---------------------- |
| CPU usage             | `%Cpu(s)` (`100 - id`) |
| RAM usage             | `MiB Mem` / `GiB Mem`  |
| System load           | `load average`         |
| Per-core CPU          | Press `1`              |
| Top CPU processes     | Press `P`              |
| Top RAM processes<br> | Press `M`              |
|                       |                        |

## How analyze cpu utilization

`top` breaks CPU time into categories. The CPU is always spending **100% of its time** doing something.

Example:

```text
%Cpu(s):  12.5 us, 5.0 sy, 0.0 ni, 80.0 id, 2.5 wa, 0.0 hi, 0.0 si, 0.0 st
```

Meaning:

- `us` = 12.5% → Running user programs
    
- `sy` = 5.0% → Running kernel/system code
    
- `id` = 80.0% → CPU is idle
    
- `wa` = 2.5% → Waiting for disk/network I/O
    
- Others = Interrupts, virtualization, etc.
    

These add up to **100%**.

### Why `100 - id`?

`id` is the percentage of time the CPU is **doing nothing**.

So:

```
CPU usage = 100 - idle
```

Example:

| `id` | CPU usage |
| ---- | --------- |
| 95%  | 5% busy   |
| 80%  | 20% busy  |
| 50%  | 50% busy  |
| 5%   | 95% busy  |

### Example 1 (Mostly idle)

```text
%Cpu(s): 2.0 us, 1.0 sy, 96.5 id, 0.5 wa
```

```
CPU usage = 100 - 96.5 = 3.5%
```

### Example 2 (Busy)

```text
%Cpu(s): 70.0 us, 20.0 sy, 10.0 id
```

```
CPU usage = 100 - 10 = 90%
```

### Multi-core systems

If you have **8 cores**, then `id = 50%` means **half of the total CPU capacity is idle**. It does **not** mean one core is at 50%.

Press **`1`** in `top` to see each core separately:

```
%Cpu0 : 100.0 us, 0.0 id
%Cpu1 :  10.0 us, 90.0 id
%Cpu2 :   0.0 us,100.0 id
...
```

This shows which individual cores are busy.