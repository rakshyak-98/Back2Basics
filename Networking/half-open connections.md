[[TCP]] [[auto-pong]] [[Network error]] [[webSocket]] [[Configuration]]

# half-open connections

> A half-open TCP connection has one side believing the session is alive while the other has closed or crashed — load balancers and NAT idle timers are the usual culprits.





## Interview Relevance
Interviewers ask about half-open connections to see if you distinguish normal TCP half-close (FIN one way) from dead peers, and whether you design keepalives below proxy idle timeouts — especially for long-lived [[webSocket]] or RPC streams.

## Sources
- [RFC 9293 — TCP (connection states)](https://www.rfc-editor.org/rfc/rfc9293) — deep-dive
- [Wikipedia — TCP half-open](https://en.wikipedia.org/wiki/TCP_half-open) — overview

## Key Concepts
- **Half-close vs half-open:** one side can FIN while still receiving (normal) → problematic half-open means one peer thinks ESTABLISHED while the other is gone with no FIN/RST.
- **Silent middlebox drops:** load balancers and NAT idle timers delete state without notifying endpoints → next write hangs or gets RST later.
- **Detection needs activity:** TCP keepalives, application heartbeats, or read timeouts → idle connections look healthy until you probe.
- **Align timeouts:** application ping interval must be shorter than proxy idle timeout → otherwise the proxy wins and the app loses.

## Technical Details
TCP is full-duplex. One side can send FIN (finished sending) while still receiving — a **half-close**. That is normal shutdown semantics, not necessarily an error.

The problematic **half-open** state: one peer thinks the connection is ESTABLISHED; the other is gone (crash, cable pull, middlebox drop) with no FIN/RST.

```
Client: ESTABLISHED  →  sends data  →  black hole (server dead)
Server: (does not exist)
```

Detection:

- **Keepalives** — TCP `SO_KEEPALIVE` (slow defaults on Linux) or application [[auto-pong]] / heartbeats
- **Read timeout** — zero bytes forever
- **`ss` state** — many connections in CLOSE-WAIT or unknown orphans

```bash
ss -tan state established '( dport = :443 )'
ss -o state established '( dport = :443 )'    # timer info
```

AWS ALB/NLB, HAProxy, and corporate NAT often drop idle flows at 60–350 seconds without notifying endpoints. The next write may hang until TCP retransmit exhausts, or succeed into a RST from the load balancer.

Mitigation: application keepalives below the idle threshold; align proxy `timeout` with server settings ([[Configuration]] for Nginx `proxy_read_timeout`).

[[webSocket]] over TCP inherits the same half-open risk — use protocol ping/pong frames on an interval shorter than proxy idle timeout.

## Real-World Applications
Long-lived API streams, database connections through NATs, and WebSocket frontends behind ALB. Example: a chat WebSocket works for two minutes then silently dies — the ALB idle timeout was 60s and the client sent no ping frames.

## Pros/Cons or Trade-offs
- **Pro:** Application-level heartbeats detect dead peers quickly and work across middleboxes that ignore TCP keepalives.
- **Con:** Too-aggressive pinging wastes battery/bandwidth; too-slow pinging leaves half-open sockets until the next write fails.

## Comparison
vs TCP half-close: half-close is intentional one-way FIN while the other direction stays open; half-open (in the failure sense) is asymmetric belief about liveness after a crash or silent drop.

## Mistakes to Avoid
- Confusing half-close with half-open — interview answers should separate the terms.
- Relying only on Linux `SO_KEEPALIVE` defaults — they are often too slow for cloud idle timers.
- Setting WebSocket pings longer than the load balancer idle timeout.
- Ignoring CLOSE-WAIT / orphan piles in `ss` as a signal of application shutdown bugs.
