[[Security]]

# TURN server (Traversal Using Relays around NAT)

> One-line: what / why for **TURN server (Traversal Using Relays around NAT)** — source TBD.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

- is a protocol designed to help devices behind restrictive NAT's or firewall communicate by relaying their traffic through a server.
Unlike [[STUN (Session Traversal Utilities for NAT)]], which enables direct peer-to-peer connections, TURN is used when a direct connection is not possible, such as with [[Symmetric NAT]] or firewall blocking incoming connections.
- TURN acts as a [[Relay server]].
- All data between peers is sent through the TURN server instead of directly between devices.
- Necessary in [[Symmetric NAT]] or highly restrictive firewalls where direct connection (hole punching) is impossible.
- Often used as a fallback after STUN fails.
Traffic relaying -> The TURN server forwards all data between two peers because they cannot communicate directly.
Relay -> A relay is an intermediate node that receives data and forwards it.

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
