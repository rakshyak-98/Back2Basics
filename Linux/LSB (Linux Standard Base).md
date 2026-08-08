[[Linux]]

# LSB (Linux Standard Base)

> LSB (Linux Standard Base) — while it's not a kernel "module" in the way a hardware drive is, it is a core standard (and a corresponding set of

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

While it's not a kernel "module" in the way a hardware drive is, it is a core standard (and a corresponding set of software packages) designed to reduce the differences between individual linux distribution.
> [!INFO]
> Historically, the biggest challenge in the Linux ecosystem was fragmentation. If a developer wrote a software application for Ubuntu, there was no guarantee it would work on Fedora or Arch Linux because the underlying libraries, file locations, and system tools might be slightly different.
- The LSB was created by the Linux Foundation to solve this by defining a standard core system. If a Linux distribution is "LSB compliant" a software develop can write a program targeting the LSB standard, knowing it will run correctly on the distribution. It standardizes things like:
	- The Filesystem Hierarchy Standard (FHS) -> Exactly where certain files and directories (like `/bin` `/etc` or `/usr`) must be located.

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
