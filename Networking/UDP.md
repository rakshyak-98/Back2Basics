[[TCP]] [[Berkeley sockets]] [[webSocket]] [[ICMP]]

# UDP

> Connectionless datagram protocol — send without handshake; no delivery, ordering, or congestion guarantees; app owns reliability if needed.

---

## Mental model

**UDP** trades TCP's session state for **minimal overhead**:

```txt
TCP: SYN → SYN-ACK → data → ACK → retransmit…
UDP: datagram → maybe arrives once → maybe not
```

Header: ports + length + checksum (optional on IPv4). Each `sendto` is independent — **no stream boundary** beyond datagram size ([[MTU (Maximum Transmission Unit)]] − headers).

Fit when:
- **Latency > reliability** — VoIP, gaming, live video
- **App-layer retries OK** — DNS, QUIC (over UDP), custom RPC
- **Broadcast/multicast** patterns (limited on modern internet)

Poor fit when:
- Large file transfer without custom protocol
- Need ordered byte stream through NAT middleboxes without ALG

---

## Standard config / commands

### Test UDP reachability

```bash
nc -u -l 9999                    # listener
nc -u localhost 9999             # sender

# socat
socat - UDP4-LISTEN:9999,fork
```

### ss / netstat

```bash
ss -ulnp
ss -u -a state established   # connected UDP sockets
```

### iperf3

```bash
iperf3 -s -p 5201
iperf3 -c host -u -b 100M -l 1400
# Shows loss, jitter, out-of-order
```

### Firewall

```bash
sudo iptables -A INPUT -p udp --dport 53 -j ACCEPT
sudo ufw allow 51820/udp   # WireGuard example
```

**Why DNS uses UDP:** single request/response fits one datagram; truncates to TCP if answer too large.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Works TCP, fails UDP | Firewall/NACL UDP blocked | Open UDP port; stateless rules both directions |
| Packet loss | `iperf3 -u`; switch counters | Reduce rate; fix QoS; MTU/fragmentation |
| Intermittent DNS | MTU black hole | Enable TCP fallback; fix PMTUD |
| NAT binding expires | Idle UDP mapping timeout | Keepalive packets; switch to TCP/TLS |

---

## Gotchas

> [!WARNING]
> **UDP amplification attacks** — open reflectors (Memcached, NTP) — never expose unnecessary UDP services.

> [!WARNING]
> **Datagram size > path MTU** → IP fragmentation → loss kills whole datagram on one fragment drop.

> [!WARNING]
> **"Connected" UDP** (`connect()`) filters ICMP errors — still not reliable delivery.

---

## When NOT to use

Default to **TCP or TLS** for general API traffic unless you measure need for UDP (QUIC, RTP, DNS). Building reliable UDP ≈ reinventing TCP poorly.

---

## Related

[[TCP]] [[Berkeley sockets]] [[ICMP]] [[MTU (Maximum Transmission Unit)]] [[half-open connections]]
