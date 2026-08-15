[[TCP]] [[POSIX Socket]] [[BSD Socket]] [[NAT (Network Address Translation)]] [[webSocket]] [[MTU (Maximum Transmission Unit)]] [[Packet Fragment]] [[STUN (Session Traversal Utilities for NAT)]]

# UDP

> User Datagram Protocol sends self-contained datagrams with no delivery guarantee — the first pain point is usually application design for loss, reordering, and NAT keepalive.

## Interview Relevance

Interviewers use UDP to test whether you know when reliability belongs in the application (or a protocol on top) versus the transport. Expect questions on datagram boundaries, checksum/fragmentation, NAT idle timers, and why DNS/QUIC/VoIP choose UDP over [[TCP]].

## Sources

- [RFC 768 — User Datagram Protocol](https://www.rfc-editor.org/rfc/rfc768) — deep-dive
- [Wikipedia — User Datagram Protocol](https://en.wikipedia.org/wiki/User_Datagram_Protocol) — overview

## Key Concepts

- **Datagram model:** each `sendto()` produces one datagram (ports + optional checksum on IP) → no connection state, handshake, or retransmission.
- **Boundary preservation:** UDP keeps message edges; TCP is a byte stream → apps must not assume stream framing.
- **Best-effort delivery:** loss, duplication, and reordering are possible → application or layered protocol must handle them.
- **NAT flow tracking:** middleboxes track UDP by 5-tuple with short idle timers → silent sockets lose mappings without keepalives.

## Technical Details

UDP (RFC 768) adds ports and an optional checksum to IP. Theoretical max is ~65 KiB; path [[MTU (Maximum Transmission Unit)]] limits practical size.

```
Application A                    Application B
  │──── datagram (src:port → dst:port) ────►│
  │◄─── reply datagram (optional) ──────────│
```

Properties compared to [[TCP]]:

| | UDP | TCP |
|---|-----|-----|
| Boundaries | Preserved per datagram | Byte stream |
| Reliability | Best-effort | Retransmit + order |
| Overhead | 8-byte header + IP | State + ACKs |
| Use case | DNS, VoIP, QUIC base, gaming | HTTP, SSH, databases |

UDP checksum (RFC 768, updated by RFC 8200 for IPv6) detects corruption. Large datagrams may be fragmented at the IP layer — [[Packet Fragment]] loss drops the whole datagram. Applications often stay under path MTU (~1200–1400 bytes on the public internet).

[[NAT (Network Address Translation)]] devices track UDP "flows" by 5-tuple with short idle timers. Silent UDP sockets lose mappings; [[STUN (Session Traversal Utilities for NAT)]] and application keepalives address this for WebRTC and gaming.

```bash
ss -uan
nc -u host 53                    # DNS-style probe
tcpdump -ni any udp port 53
```

## Real-World Applications

Latency-sensitive media (late data is worthless), simple query/response with application retry (DNS), and protocols built on top (QUIC, WireGuard, custom RPC). Example: a game client sends position updates every 20 ms over UDP and accepts occasional loss rather than waiting on TCP retransmit.

## Pros/Cons or Trade-offs

- **Pro:** Low overhead, no head-of-line blocking from transport retransmit, natural fit for real-time and multiplexed designs (QUIC).
- **Con:** You own reliability, congestion control, and NAT keepalive; firewalls and middleboxes are often harsher on UDP than TCP.

## Comparison

vs [[TCP]]: TCP gives ordered reliable byte streams with connection state; UDP gives independent datagrams and pushes loss/order handling (or a protocol like QUIC) to the layer above.

## Mistakes to Avoid

- Assuming "UDP is unreliable so it always loses packets" — loss rates vary; the point is there is no transport guarantee.
- Sending large datagrams without considering path MTU — one lost fragment kills the whole message.
- Forgetting NAT idle timers on long-lived UDP sessions — mappings expire without keepalives.
- Expecting TCP-style "connection refused" semantics without checking how your stack surfaces ICMP errors on UDP sockets.
