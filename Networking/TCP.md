<!-- note-strategy: operational -->
[[Networking]] [[Byte stream]] [[UDP]] [[SSH]]

# TCP

> TCP is a reliable ordered byte stream between two hosts — handshake, acks, retransmit; not message frames.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** TCP gives you a pipe of bytes that arrive in order. Your application must split messages; the kernel splits packets.

```txt
App write("HELLO") write("WORLD")
        │
   TCP send buffer → segments (SEQ/ACK) → IP packets
        │
   Peer TCP reorders / buffers → App read() sees a byte stream
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Byte stream** | No message boundaries | “TCP won’t preserve my write() sizes.” |
| **3-way handshake** | SYN → SYN-ACK → ACK | “We sync sequence numbers before data.” |
| **SEQ / ACK** | Byte offsets | “ACKs say how far the receiver got.” |
| **rwnd** | Receiver window | “Flow control stops me overrunning the peer.” |
| **cwnd** | Congestion window | “Congestion control slows me on loss.” |
| **Retransmit** | Resend lost data | “Loss triggers RTO or fast retransmit.” |
| **4-tuple** | src IP/port + dst IP/port | “That uniquely IDs the connection.” |
| **Half-close** | FIN one direction | “I can stop sending and still receive.” |

### Reliability in plain steps

1. **Connect** — three-way handshake builds shared state.
2. **Send** — data gets SEQ numbers; peer ACKs contiguous bytes.
3. **Recover** — loss → retransmit; reorder → hold until gap fills.
4. **Pace** — `rwnd` (peer buffer) + `cwnd` (network) limit in-flight data.
5. **Close** — each side FIN/ACKs (four-way); TIME-WAIT holds the old tuple.

versus [[UDP]]: UDP keeps datagram edges, no connect state, no delivery guarantee — better for latency-sensitive media when the application handles loss.

---

## Standard config / commands

```bash
ss -tan | head
ss -ti dst :443          # TCP info: rtt, cwnd, retrans
tcpdump -ni any tcp port 443
# Kernel knobs (careful in prod)
sysctl net.ipv4.tcp_fin_timeout
sysctl net.core.somaxconn
```

application framing examples: HTTP `Content-Length` / chunked; length-prefix RPC; newline JSON lines.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Connect hangs | SYN dropped / firewall | Path MTU, SG rules, `ss -tan` SYN-SENT |
| Stall under load | Zero window / buffer full | Raise buffers; fix slow consumer |
| High latency after loss | Retrans / CUBIC vs BBR | Tune CC; check wifi loss |
| Message parse errors | Assumed write==read sizes | Add framing on the stream |
| Port reuse fails | TIME-WAIT | `SO_REUSEADDR`; shorter workloads |
| Reset (RST) | Peer closed / wrong state | Check crash, idle LB timeout |

---

## Gotchas

> [!WARNING]
> **Nagle + delayed ACK** — small writes can feel laggy; batch writes or `TCP_NODELAY` when needed.

> [!WARNING]
> **Head-of-line blocking** — one lost packet blocks later bytes in that stream (HTTP/2 pain → HTTP/3/QUIC).

> [!WARNING]
> **Load balancer idle timeout** — silent middlebox close; use app keepalives.

---

## When NOT to use

- **Live A/V with loss tolerance** — often [[UDP]] + codec concealment (WebRTC).
- **Tiny request/response where UDP + application retry is enough** — DNS-like patterns (with care).
- **Multicast discovery** — TCP is point-to-point.

---

## Related

[[UDP]] [[Byte stream]] [[BSD Socket]] [[POSIX Socket]] [[SSH]] [[ICMP]] [[MTU (Maximum Transmission Unit)]] [[half-open connections]]
