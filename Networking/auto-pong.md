[[Networking]]

# auto-pong

> One-line: what / why for **auto-pong** — source TBD.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

in networking, auto-pong typically refers to an automatic response mechanism where a system or protocol sends a pong reply when it receives a ping request.
> [!INFO] used for connection health checks, latency measurement, and keep-alive mechanisms.
- A [[webSocket]] server/client can automatically send a pong frame when it receives a ping frame, ensuring the connection is alive.
- A system receiving an ICMP Echo Request (ping) can auto-respond with an [[ICMP]] Echo Reply (pong).
- Some protocols implement auto-pong to verify connectivity without requiring manual intervention.

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
