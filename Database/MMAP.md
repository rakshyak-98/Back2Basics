[[Database]]

# MMAP

> MMAP — uses memory mapped files as its storage engine.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

Memory Mapped Storage Engine (MMAP)
- uses memory mapped files as its storage engine.
- allocates memory using power of 2 bytes sizes.
- in place updates are fast.
### Memory-mapped file
is a segment of virtual memory which has been assigned a direct byte-for-byte correlation with some portion of a file.
- delegate the handling of Virtual Memory to the operating system instead of explicitly managing memory itself.
### Determine if the working set is too big
- by looking at the number of page faults over time. If it's rapidly increasing it might mean your Working Set does not fir in memory.

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
