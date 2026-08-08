[[Operating System]]

# Buffer cache

> Buffer cache — the buffer cache is a kernel subsystem that manages buffers in memory to optimize disk I/O performance.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

- The buffer cache is a [[kernel subsystem]] that manages buffers in memory to optimize disk I/O performance.
####  Some key points about the buffer cache
- It maintains a set of buffer heads describing the buffers in the cache.
- it uses a hash table to quickly find the [[buffer head]] for a given device and block number.
- Buffers are allocated on demand from free memory when needed.
- Dirty buffers (modified in memory) are written to disk at regular intervals to minimize I/O impact on user processes.

## Standard config / commands

…

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
