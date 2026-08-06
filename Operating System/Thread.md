[[Operating System]]

# Thread

> One-line: what / why for **Thread** — source TBD.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

- [thread](https://en.wikipedia.org/wiki/Thread_(computing)) is the smallest sequence of programmed instructions that can be managed independently by a scheduler, which is typically a part of the operating system.
- in many cases a thread is a component of a process.
- the implementation of threads and processes differs between operating systems.
- thread in the same process share the same address space. This allows concurrently running code to couple tightly and conveniently exchange data without the overhead or complexity of an [[Inter Process Communication]].
-  thread based networking is relatively inefficient and very difficult to use.
> [!INFO]
> - Need synchronisation (mutex, semaphore, atomic, memory barriers).
> - Bugs are nondeterministic and hard to reproduce.
> - Data races, Race conditions.

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
