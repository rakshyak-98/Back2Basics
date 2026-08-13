[[NodeJS]] [[HTTP module]] [[expressjs]]

# agent (http.Agent)

> Connection pool for outbound HTTP — keep-alive sockets, max sockets per host, and fewer TCP/TLS handshakes.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Without keep-alive, every `http.request` pays handshake cost. An `Agent` reuses sockets up to configured limits.

```txt
request → Agent → idle socket? reuse : connect
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **keepAlive** | Reuse TCP/TLS | “Critical for chatty microservices.” |
| **maxSockets** | Cap per host | “Protect yourself and the peer.” |
| **free sockets** | Idle pool | “`maxFreeSockets` bounds memory.” |

## Standard config / commands

```js
import http from 'node:http'

const agent = new http.Agent({ keepAlive: true, maxSockets: 50 })
http.get('http://example.com', { agent }, (res) => res.resume())

// undici/fetch often has its own pool — prefer that in modern Node
```

| Knob | Why it matters |
|------|----------------|
| `keepAlive` | Enable reuse |
| `timeout` | Kill stuck sockets |
| Global agent | Default shared — tune carefully |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Latency high to same host | New conn each time | `keepAlive: true` |
| ECONNRESET storms | Peer closed idle | Tune timeouts; refresh |
| FD exhaustion | maxSockets too high | Lower caps |
| Hang forever | No timeout | Set agent/request timeouts |

---

## Gotchas

> [!WARNING]
> **`agent: false`** disables pooling for that request — sometimes needed, usually slower.

> [!WARNING]
> **fetch/undici** — separate pooling story from classic `http.Agent`.

---

## When NOT to use

- **One-off scripts** — defaults fine.
- **Mis-tuning maxSockets to “unlimited”** — you can DoS the dependency.

---

## Related

[[HTTP module]] [[Optimization]] [[expressjs]]
