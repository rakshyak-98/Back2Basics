[[UDP]] [[BSD Socket]] [[POSIX Socket]] [[half-open connections]] [[MTU (Maximum Transmission Unit)]] [[ICMP]]

# TCP

> Transmission Control Protocol delivers a reliable, ordered byte stream between two endpoints — the first thing that breaks under load is usually flow control, congestion, or a middlebox idle timeout.

## What TCP guarantees

TCP (RFC 9293, successor to RFC 793) sits above IP and provides:

| Property | Mechanism |
|----------|-----------|
| Reliable delivery | Sequence numbers, acknowledgements, retransmission |
| Ordered delivery | Receiver buffers out-of-order segments until gaps fill |
| Flow control | Receiver window (`rwnd`) limits in-flight data |
| Congestion control | Congestion window (`cwnd`) adapts to packet loss |
| Connection-oriented | Four-tuple (source IP, source port, destination IP, destination port) identifies each connection |

Unlike [[UDP]], TCP does **not** preserve message boundaries. One `write()` may become several segments; several `read()` calls may consume one segment. Applications must define framing (HTTP `Content-Length`, length-prefix, delimiters).

## Connection lifecycle

```
Client                          Server
  │──── SYN (seq=x) ─────────────►│
  │◄── SYN-ACK (seq=y, ack=x+1) ──│
  │──── ACK (ack=y+1) ────────────►│   ← three-way handshake
  │◄══════ data transfer ═════════►│
  │──── FIN ──────────────────────►│   ← four-way close (each direction)
  │◄─── FIN ──────────────────────│
```

After close, the side that sent the first FIN enters **TIME-WAIT** (typically 2× MSL) to catch late duplicates — this can block port reuse on busy servers.

## Congestion and performance

Modern Linux defaults include CUBIC or BBR congestion control. Loss triggers retransmission (RTO or fast retransmit after three duplicate ACKs). **Head-of-line blocking** means one lost segment stalls the entire byte stream — a motivation for QUIC/HTTP/3 over [[UDP]].

**Nagle's algorithm** batches small writes; combined with delayed ACK it can add latency for chatty protocols. `TCP_NODELAY` disables Nagle when needed.

## Operations

```bash
ss -tan state established
ss -ti dst :443                    # RTT, cwnd, retrans count
tcpdump -ni any 'tcp[tcpflags] & tcp-syn != 0'
sysctl net.ipv4.tcp_fin_timeout
sysctl net.core.somaxconn
```

| Symptom | Likely cause |
|---------|--------------|
| SYN-SENT hang | Firewall, routing, or server not listening |
| Zero window stall | Application not reading fast enough |
| RST after idle | Load balancer or NAT timeout |
| Garbled messages | Missing application-level framing |

## When to choose something else

Live audio/video with loss tolerance, DNS-style request/response, multicast discovery, and gaming often prefer [[UDP]] with application-level reliability where needed.

## Sources

- [RFC 9293 — Transmission Control Protocol (TCP)](https://www.rfc-editor.org/rfc/rfc9293)
- [Wikipedia — Transmission Control Protocol](https://en.wikipedia.org/wiki/Transmission_Control_Protocol)
