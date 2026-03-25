`top` = real-time process monitor (CPU, RAM, load)

---

## Core layout (mental model)

- **Header** → system stats (load avg, CPU %, RAM)
    
- **Process table** → per-process metrics
    

---

## Navigation (interactive keys)

### Process control

- `k` → kill process (enter PID)
    
- `r` → renice (change priority)
    

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