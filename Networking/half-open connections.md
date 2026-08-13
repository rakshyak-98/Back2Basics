[[TCP]] [[auto-pong]] [[Network error]] [[webSocket]]

# half-open connections

> A half-open TCP connection has one side believing the session is alive while the other has closed or crashed — load balancers and NAT idle timers are the usual culprits.

## TCP half-close

TCP is full-duplex. One side can send FIN (finished sending) while still receiving — a **half-close**. That is normal shutdown semantics, not necessarily an error.

The problematic **half-open** state: one peer thinks the connection is ESTABLISHED; the other is gone (crash, cable pull, middlebox drop) with no FIN/RST.

```
Client: ESTABLISHED  →  sends data  →  black hole (server dead)
Server: (does not exist)
```

## Detection

- **Keepalives** — TCP `SO_KEEPALIVE` (slow defaults on Linux) or application [[auto-pong]] / heartbeats
- **Read timeout** — zero bytes forever
- **`ss` state** — many connections in CLOSE-WAIT or unknown orphans

```bash
ss -tan state established '( dport = :443 )'
ss -o state established '( dport = :443 )'    # timer info
```

## Middlebox idle timeouts

AWS ALB/NLB, HAProxy, and corporate NAT often drop idle flows at 60–350 seconds without notifying endpoints. The next write may hang until TCP retransmit exhausts, or succeed into a RST from the load balancer.

Mitigation: application keepalives below the idle threshold; align proxy `timeout` with server settings ([[Configuration]] for Nginx `proxy_read_timeout`).

## Related to WebSockets

[[webSocket]] over TCP inherits the same half-open risk — use protocol ping/pong frames on an interval shorter than proxy idle timeout.

## Sources

- [RFC 9293 — TCP (connection states)](https://www.rfc-editor.org/rfc/rfc9293)
- [Wikipedia — TCP half-open](https://en.wikipedia.org/wiki/TCP_half-open)
