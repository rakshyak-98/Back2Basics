[[commands]]

# GDB : The GNU Project Debugger

> GDB : The GNU Project Debugger — GDB : allows you to see what is going on inside another program while it executed, or what another program was

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

[GDB](https://www.sourceware.org/gdb/) : allows you to see what is going on inside another program while it executed, or what another program was doing at the moment it crashed.
- programs might be executing on the same machine as GDB, on another machine, or on a simulator.
- can run on UNIX and Microsoft Windows, macOS.
**Attach `gdb` to the running process**
```bash
gdb -p <pid>;
```
```bash(gdb)
info proc mappings; #see the memory map, including the stack region.
x/32xg $rsp; # examine the contents of the stack pointer register and the memory it points to.
```

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
