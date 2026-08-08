[[Operating System]]

# handle

> Handle — OS opaque ID for an open resource (file, socket, process) used by syscalls.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

→ [[file descriptors]]
Alias note: **handle** (abstract resource reference) — on Unix/Linux the concrete mechanism is [[file descriptors]] (integer indices into the per-process fd table). Windows uses `HANDLE`; databases use cursor/connection handles — same pattern, different API.

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
