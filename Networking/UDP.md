[[TCP]] [[POSIX Socket]] [[BSD Socket]] [[NAT (Network Address Translation)]] [[webSocket]]

# UDP

> User Datagram Protocol sends self-contained datagrams with no delivery guarantee — the first pain point is usually application design for loss, reordering, and NAT keepalive.

## Datagram model

UDP (RFC 768) adds ports and an optional checksum to IP. Each `sendto()` produces one datagram (up to ~65 KiB theoretically; path [[MTU (Maximum Transmission Unit)]] limits practical size). There is no connection state, no handshake, and no retransmission.

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

## Checksum and fragmentation

UDP checksum (RFC 768, updated by RFC 8200 for IPv6) detects corruption. Large datagrams may be fragmented at the IP layer — [[Packet Fragment]] loss drops the whole datagram. Applications often stay under path MTU (~1200–1400 bytes on the public internet).

## NAT and session tracking

[[NAT (Network Address Translation)]] devices track UDP "flows" by 5-tuple with short idle timers. Silent UDP sockets lose mappings; [[STUN (Session Traversal Utilities for NAT)]] and application keepalives address this for WebRTC and gaming.

## Operations

```bash
ss -uan
nc -u host 53                    # DNS-style probe
tcpdump -ni any udp port 53
```

## When UDP fits

- Latency-sensitive media where late data is worthless
- Simple query/response (DNS) with application retry
- Building protocols on top (QUIC, WireGuard, custom RPC)

## Sources

- [RFC 768 — User Datagram Protocol](https://www.rfc-editor.org/rfc/rfc768)
- [Wikipedia — User Datagram Protocol](https://en.wikipedia.org/wiki/User_Datagram_Protocol)
