[[NodeJS]] [[HTTP module]] [[expressjs]] [[Optimization]]

# agent (http.Agent)

> Connection pool for outbound HTTP — keep-alive sockets, max sockets per host, and fewer TCP/TLS handshakes.

```txt
        agent (http.Agent) ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers use **agent (http.Agent)** to check whether you can explain the …

## Sources
- [Node.js — http.Agent](https://nodejs.org/api/http.html#class-httpagent) — deep-dive
- [Wikipedia — agent](https://en.wikipedia.org/wiki/agent) — overview

## Key Concepts
- **keepAlive:** Reuse TCP/TLS — Critical for chatty microservices.
- **maxSockets:** Cap per host — Protect yourself and the peer.
- **free sockets:** Idle pool — `maxFreeSockets` bounds memory.

## Technical Details
```txt
request → Agent → idle socket? reuse : connect
```

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

## Mistakes to Avoid
- **Mistake:** **`agent: false`** disables pooling for that request

> [!WARNING]
> **fetch/undici** — separate pooling story from classic `http.Agent`.
- **Mistake:** **Latency high to same host:** check New conn each time
- **Mistake:** **ECONNRESET storms:** check Peer closed idle
- **Mistake:** **FD exhaustion:** check maxSockets too high; fix: Lower caps
- **Mistake:** **Hang forever:** check No timeout

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Connection pool for outbound HTTP — keep-alive sockets, max sockets per host, an…).
- **Con / when not:** **One-off scripts** — defaults fine.
- **Con / when not:** **Mis-tuning maxSockets to “unlimited”**

## Comparison
- vs [[HTTP module]]: know when each applies


### Use cases
- In production APIs and tooling, **agent** shows up whenever teams ship Node/J…
