[[commands]]

# Linux process commands

> Linux process commands — c → Toggle full command path

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#`top`]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

…

## Standard config / commands

…

## `top`

#### **Navigation & Display**
- `h` → Help menu
- `q` → Quit `top`
- `Space` → Refresh display
- `c` → Toggle full command path
- `1` → Show all CPU cores

#### **Sorting & Filtering**
- `Shift+P` → Sort by **CPU** usage
- `Shift+T` → Sort by **Running Time**
- `Shift+N` → Sort by **PID**
- `o` → Set custom sort field

#### **Process Management**

- `k` → Kill process (Enter PID)
- `r` → Renice process (Change priority)
- `d` or `s` → Change refresh interval

#### **CPU & Memory Views**
- `Shift+I` → Toggle Irix mode (CPU usage)
- `m` → Toggle memory info
- `t` → Toggle CPU time display

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| … | … | … |

## Gotchas

> [!WARNING]
> …

## When NOT to use

…

## Related

[[…]]
