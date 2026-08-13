<!-- note-strategy: operational -->
[[Proxy]]

# Reverse Proxy

> Reverse Proxy — a reverse proxy is used by the server-side to accept request from clients on behalf of the actual server, hiding the server's identity. The…

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Reverse Proxy — a reverse proxy is used by the server-side to accept request from clients on behalf of the actual server, hiding the server's identity. The…

A reverse proxy is used by the server-side to accept request from clients on behalf of the actual server, hiding the server's identity. The response from the back-end server is sent back to the client through the reverse proxy.
A reverse proxy is used by the server to handle incoming traffic from multiple clients and distribute it to the back-end servers.
- it is typically used to protect the actual server's infrastructure and load balance traffic.


---

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

[[Proxy]]
