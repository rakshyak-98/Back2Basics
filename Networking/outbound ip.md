[[Networking]]

# outbound ip

> One-line: what / why for **outbound ip** — source TBD.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

- IP address used by server/device when sending traffic out to the internet.
Direction -> outgoing (engress) traffic from local network -> internet.
Usage -> identifies your system to external server.
> [!INFO]
> When your server calls an API, the remote service sees your outbound IP.
> - Inbound IP handles incoming (ingress) requests.
1. single server -> outbound IP = same as server's public IP.
2. Behind NAT or load balancer -> outbound IP = public IP of gateway/router.
3. Cloud (AWS/GCP/Azure) -> outbound IP = NAT gateway or egress IP assigned.

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
