[[UDP]] [[BSD Socket]] [[POSIX Socket]] [[half-open connections]] [[MTU (Maximum Transmission Unit)]] [[ICMP]]

# TCP

> Transmission Control Protocol delivers a reliable, ordered byte stream between two endpoints — under load, flow control, congestion, or middlebox idle timeouts usually break first.

```txt
        TCP ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers use TCP to check whether you understand reliability mechanisms (…

## Sources
- [RFC 9293 — Transmission Control Protocol (TCP)](https://www.rfc-editor.org/rfc/rfc9293) — deep-dive
- [Wikipedia — Transmission Control Protocol](https://en.wikipedia.org/wiki/Transmission_Control_Protocol) — overview

## Key Concepts
- **Reliability:** sequence numbers, acknowledgements, retransmission → lost segments recover wi…
- **Ordered delivery:** receiver buffers out-of-order segments → apps see a contiguous stream (and pa…
- **Flow control (`rwnd`):** receiver window limits in-flight data → protects a slow reader.
- **Congestion control (`cwnd`):** adapts to loss → protects the shared network.
- **No message boundaries:** one `write()` may become many segments → apps must frame (length prefix, deli…


- **Core:** TCP sits above IP and turns an unreliable packet path into a connection-orien…

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

- After close, the side that sent the first FIN enters **TIME-WAIT** (typically…

- Modern Linux defaults include CUBIC or BBR.
- Loss triggers retransmission (RTO or fast retransmit after three duplicate AC…
- **Nagle's algorithm:** batches small writes; with delayed ACK it can add laten…

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

## Mistakes to Avoid
- **Mistake:** Treating TCP as message-oriented
- **Mistake:** Ignoring middlebox idle timeouts
- **Mistake:** Enabling Nagle on latency-sensitive chatty protocols without mea…

## Pros/Cons or Trade-offs
- **Pro:** Built-in reliability and ordering — correct for most request/response and file transfer.
- **Con:** Head-of-line blocking — one lost segment stalls the whole stream (motivation for QUIC/HTTP/3 over [[UDP]]).
- **Con:** Connection setup and TIME-WAIT cost matter at high churn.

## Comparison
- vs [[UDP]]: UDP is datagram, unordered, no congestion by default — apps own reliability.
- vs QUIC/HTTP/3: multiplexed streams over UDP with independent loss recovery.


### Use cases
- HTTPS, databases, SSH, and most request/response APIs run over TCP.

- **Example:** An API behind a load balancer sees random RST after idle
