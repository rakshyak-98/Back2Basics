[[TCP]] [[auto-pong]] [[Network error]] [[webSocket]] [[Configuration]]

# half-open connections

> A half-open TCP connection has one side believing the session is alive while the other has closed or crashed — load balancers and NAT idle timers are the usual culprits.

```txt
        half-open connecti ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers ask about half-open connections to see if you distinguish normal…

## Sources
- [RFC 9293 — TCP (connection states)](https://www.rfc-editor.org/rfc/rfc9293) — deep-dive
- [Wikipedia — TCP half-open](https://en.wikipedia.org/wiki/TCP_half-open) — overview

## Key Concepts
- **Half-close vs half-open:** one side can FIN while still receiving (normal) → problematic half-open means…
- **Silent middlebox drops:** load balancers and NAT idle timers delete state without notifying endpoints →…
- **Detection needs activity:** TCP keepalives, application heartbeats, or read timeouts → idle connections l…
- **Align timeouts:** application ping interval must be shorter than proxy idle timeout → otherwise…

## Technical Details
- TCP is full-duplex.
- One side can send FIN (finished sending) while still receiving
- That is normal shutdown semantics, not necessarily an error.

- The problematic **half-open** state: one peer thinks the connection is ESTABL…

```
Client: ESTABLISHED  →  sends data  →  black hole (server dead)
Server: (does not exist)
```

- Detection:

- **Keepalives:** — TCP `SO_KEEPALIVE` (slow defaults on Linux) or application [[auto-pong]] / …
- **Read timeout:** — zero bytes forever
- **`ss` state:** — many connections in CLOSE-WAIT or unknown orphans

```bash
ss -tan state established '( dport = :443 )'
ss -o state established '( dport = :443 )'    # timer info
```

- AWS ALB/NLB, HAProxy, and corporate NAT often drop idle flows at 60–350 secon…
- The next write may hang until TCP retransmit exhausts, or succeed into a RST …

- Mitigation: application keepalives below the idle threshold

- [[webSocket]] over TCP inherits the same half-open risk

## Mistakes to Avoid
- **Mistake:** Confusing half-close with half-open
- **Mistake:** Relying only on Linux `SO_KEEPALIVE` defaults
- **Mistake:** Setting WebSocket pings longer than the load balancer idle timeo…
- **Mistake:** Ignoring CLOSE-WAIT / orphan piles in `ss` as a signal of applic…

## Pros/Cons or Trade-offs
- **Pro:** Application-level heartbeats detect dead peers quickly and work across middleboxes that ignore TCP keepalives.
- **Con:** Too-aggressive pinging wastes battery/bandwidth; too-slow pinging leaves half-open sockets until the next write fails.

## Comparison
- vs TCP half-close: half-close is intentional one-way FIN while the other dire…


### Use cases
- Long-lived API streams, database connections through NATs, and WebSocket fron…
