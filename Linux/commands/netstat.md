[[commands]]

# - Network congestion

> One-line: what / why for **- Network congestion** — source TBD.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

Used to inspect connections, listening ports, routing table, interface statistics, and protocol statistics.
```shell
sudo netstat -p; # Show pid of executable
```
```bash
sudo netstat -luntp;
sudo netstat -tulnp | grep :8080
```
```bash
netstat -ant
#
```
```bash
netstat -s
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
