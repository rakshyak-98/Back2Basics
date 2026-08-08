[[Networking]]

# BSD

> BSD — communication in Unix-like operating systems.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

Berkeley sockets
- programming interface for network.
- communication in Unix-like operating systems.
- used for [[Inter Process Communication]]
- a client/server architecture is mandatory for BSD sockets.
- allow to add internet communication to products.
>[!NOTE] BSD socket is not stand-alone socket solution, an API relies on other socket communication for data exchange. Thus you always need to add TCP and UDP to project if you wish to use BSD sockets.
BSD stands for Berkeley Software Distribution. It is a version of the Unix operating system developed at the University of California, Berkeley.
- release in 1970s
- broadly refer to the family of operating system that are derived from the original BSD code-base. Example MacOS, base of BSD version called Darwin,
- FreeBSD, NetBSD, OpenBSD operating system. These systems are known for stability, security, and portability.

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
