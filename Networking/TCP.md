[[UDP]] [[BSD Socket]] [[POSIX Socket]] [[half-open connections]] [[MTU (Maximum Transmission Unit)]] [[ICMP]]

# TCP

> Transmission Control Protocol delivers a reliable, ordered byte stream between two endpoints — under load, flow control, congestion, or middlebox idle timeouts usually break first.





## Interview Relevance
Interviewers use TCP to check whether you understand reliability mechanisms (seq/ack, windows, congestion) versus “TCP just works,” and when you would pick [[UDP]] or QUIC instead.

## Sources
- [RFC 9293 — Transmission Control Protocol (TCP)](https://www.rfc-editor.org/rfc/rfc9293) — deep-dive
- [Wikipedia — Transmission Control Protocol](https://en.wikipedia.org/wiki/Transmission_Control_Protocol) — overview

## Core Definition
TCP sits above IP and turns an unreliable packet path into a connection-oriented, ordered byte stream identified by a four-tuple (source IP, source port, destination IP, destination port).

## Key Concepts
- **Reliability:** sequence numbers, acknowledgements, retransmission → lost segments recover without the app reinventing them.
- **Ordered delivery:** receiver buffers out-of-order segments → apps see a contiguous stream (and pay head-of-line blocking).
- **Flow control (`rwnd`):** receiver window limits in-flight data → protects a slow reader.
- **Congestion control (`cwnd`):** adapts to loss → protects the shared network.
- **No message boundaries:** one `write()` may become many segments → apps must frame (length prefix, delimiters, HTTP `Content-Length`).

## Technical Details
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

Modern Linux defaults include CUBIC or BBR. Loss triggers retransmission (RTO or fast retransmit after three duplicate ACKs). **Nagle's algorithm** batches small writes; with delayed ACK it can add latency — `TCP_NODELAY` disables Nagle when needed.

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

## Real-World Applications
HTTPS, databases, SSH, and most request/response APIs run over TCP.

**Example:** An API behind a load balancer sees random RST after idle — the LB or [[NAT (Network Address Translation)]] UDP/TCP idle timer expired; enable keepalives or shorten idle.

## Pros/Cons or Trade-offs
- **Pro:** Built-in reliability and ordering — correct for most request/response and file transfer.
- **Con:** Head-of-line blocking — one lost segment stalls the whole stream (motivation for QUIC/HTTP/3 over [[UDP]]).
- **Con:** Connection setup and TIME-WAIT cost matter at high churn.

## Comparison
- vs [[UDP]]: UDP is datagram, unordered, no congestion by default — apps own reliability.
- vs QUIC/HTTP/3: multiplexed streams over UDP with independent loss recovery.

## Mistakes to Avoid
- Treating TCP as message-oriented — without framing, `read()` boundaries are not application messages.
- Ignoring middlebox idle timeouts — long-lived quiet connections die without keepalives.
- Enabling Nagle on latency-sensitive chatty protocols without measuring.
