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

**Say it in one breath:** Reverse Proxy — plain job, how I run it, how I know it’s broken.


A reverse proxy is used by the server-side to accept request from clients on behalf of the actual server, hiding the server's identity. The response from the back-end server is sent back to the client through the reverse proxy.
A reverse proxy is used by the server to handle incoming traffic from multiple clients and distribute it to the back-end servers.
- it is typically used to protect the actual server's infrastructure and load balance traffic.

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Reverse Proxy** | Core idea of this note | “I can explain Reverse Proxy without jargon.” |
| **mental model** | How it works in one line | “Explain it without jargon first.” |
| **failure mode** | How it breaks | “Say what you check first.” |

---

## Standard config / commands

```bash
# reproduce with minimal input
# compare working vs broken env
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Unexpected result | inputs / versions | Reproduce minimal case |
| Works on one machine | env drift | Diff config and versions |
| Silent failure | logs / metrics | Add checks and alerts |

---

## Gotchas

> [!WARNING]
> Prefer simple words you can say in an interview.

---

## When NOT to use

- Skip it when a simpler existing tool already fits.

---

## Related

[[Proxy]]
