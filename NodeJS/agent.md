[[NodeJS]] [[HTTP module]] [[expressjs]] [[Optimization]]

# agent (http.Agent)

> Connection pool for outbound HTTP — keep-alive sockets, max sockets per host, and fewer TCP/TLS handshakes.

## Interview Relevance

Interviewers use **agent (http.Agent)** to check whether you can explain the mechanism in plain words and apply it under failure. Expect follow-ups on **keepAlive**, **maxSockets**, **free sockets**.

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

## Real-World Applications

In production APIs and tooling, **agent** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **`agent: false`** disables pooling for that request — sometimes needed, usually slower.

## Pros/Cons or Trade-offs

- **Pro:** Solves the job described above when used in the right layer (Connection pool for outbound HTTP — keep-alive sockets, max sockets per host, an…).
- **Con / when not:** **One-off scripts** — defaults fine.
- **Con / when not:** **Mis-tuning maxSockets to “unlimited”** — you can DoS the dependency.

## Comparison

vs [[HTTP module]]: know when each applies — do not treat them as interchangeable. vs [[expressjs]]: know when each applies — do not treat them as interchangeable. vs [[Optimization]]: know when each applies — do not treat them as interchangeable.

## Mistakes to Avoid

- **`agent: false`** disables pooling for that request — sometimes needed, usually slower.

> [!WARNING]
> **fetch/undici** — separate pooling story from classic `http.Agent`.
- **Latency high to same host:** check New conn each time; fix: `keepAlive: true`
- **ECONNRESET storms:** check Peer closed idle; fix: Tune timeouts; refresh
- **FD exhaustion:** check maxSockets too high; fix: Lower caps
- **Hang forever:** check No timeout; fix: Set agent/request timeouts
