[[Networking]]

# CIDR (Classless Inter-Domain Routing)

> One-line: what / why for **CIDR (Classless Inter-Domain Routing)** — source TBD.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

It is the modern way to write IP addresses and their network masks in a compact form — instead of the old "Class A/B/C" system.
```text
192.168.1.0/24
203.0.113.50/32
10.0.0.0/16
172.16.0.0/12
```
CIDR is a method for allocating IP addresses and routing that replaced the older class-based system (Class A/B/C).
Format : `<IP address>/<prefix length>` e.g., `192.168.1.0/24`
- the IP address specifies the network base.
- the prefix length (0-32 for IP4) specifies how many leading bits are fixed as the network portion; remaining bits are host addresses.

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
