[[TCP]] [[POSIX Socket]] [[BSD Socket]] [[NAT (Network Address Translation)]] [[webSocket]] [[MTU (Maximum Transmission Unit)]] [[Packet Fragment]] [[STUN (Session Traversal Utilities for NAT)]]

# UDP

> User Datagram Protocol sends self-contained datagrams with no delivery guarantee — the first pain point is usually application design for loss, reordering, and NAT keepalive.

```txt
        UDP ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers use UDP to test whether you know when reliability belongs in the…

## Sources
- [RFC 768 — User Datagram Protocol](https://www.rfc-editor.org/rfc/rfc768) — deep-dive
- [Wikipedia — User Datagram Protocol](https://en.wikipedia.org/wiki/User_Datagram_Protocol) — overview

## Key Concepts
- **Datagram model:** each `sendto()` produces one datagram (ports + optional checksum on IP) → no …
- **Boundary preservation:** UDP keeps message edges
- **Best-effort delivery:** loss, duplication, and reordering are possible → application or layered proto…
- **NAT flow tracking:** middleboxes track UDP by 5-tuple with short idle timers → silent sockets lose…

## Technical Details
- UDP (RFC 768) adds ports and an optional checksum to IP.
- Theoretical max is ~65 KiB

```
Application A                    Application B
  │──── datagram (src:port → dst:port) ────►│
  │◄─── reply datagram (optional) ──────────│
```

- Properties compared to [[TCP]]:

| | UDP | TCP |
|---|-----|-----|
| Boundaries | Preserved per datagram | Byte stream |
| Reliability | Best-effort | Retransmit + order |
| Overhead | 8-byte header + IP | State + ACKs |
| Use case | DNS, VoIP, QUIC base, gaming | HTTP, SSH, databases |

- UDP checksum (RFC 768, updated by RFC 8200 for IPv6) detects corruption.
- Large datagrams may be fragmented at the IP layer
- Applications often stay under path MTU (~1200–1400 bytes on the public intern…

- [[NAT (Network Address Translation)]] devices track UDP "flows" by 5-tuple wi…
- Silent UDP sockets lose mappings

```bash
ss -uan
nc -u host 53                    # DNS-style probe
tcpdump -ni any udp port 53
```

## Mistakes to Avoid
- **Mistake:** Assuming "UDP is unreliable so it always loses packets"
- **Mistake:** Sending large datagrams without considering path MTU
- **Mistake:** Forgetting NAT idle timers on long-lived UDP sessions
- **Mistake:** Expecting TCP-style "connection refused" semantics without check…

## Pros/Cons or Trade-offs
- **Pro:** Low overhead, no head-of-line blocking from transport retransmit, natural fit for real-time and multiplexed designs (QUIC).
- **Con:** You own reliability, congestion control, and NAT keepalive; firewalls and middleboxes are often harsher on UDP than TCP.

## Comparison
- vs [[TCP]]: TCP gives ordered reliable byte streams with connection state


### Use cases
- Latency-sensitive media (late data is worthless), simple query/response with …
