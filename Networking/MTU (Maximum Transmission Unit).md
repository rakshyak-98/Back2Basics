[[Packet Fragment]] [[ICMP]] [[TCP]] [[UDP]]

# MTU (Maximum Transmission Unit)

> MTU is the largest IP payload one link accepts without fragmentation — black-hole MTU issues show up as HTTPS that hangs on large responses but works for small pages.

```txt
        MTU (Maximum Trans ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** MTU questions separate people who have debugged tunnels and VPNs from those w…

## Sources
- [RFC 8200 — IPv6 (minimum MTU 1280)](https://www.rfc-editor.org/rfc/rfc8200) — deep-dive
- [RFC 1191 — Path MTU Discovery](https://www.rfc-editor.org/rfc/rfc1191) — deep-dive
- [Wikipedia — Maximum transmission unit](https://en.wikipedia.org/wiki/Maximum_transmission_unit) — overview

## Key Concepts
- **Per-link maximum:** each hop has an MTU → the path MTU is the minimum along the route.
- **Headers eat payload:** IP + transport headers reduce usable application bytes → TCP MSS is negotiate…
- **Fragmentation vs PMTUD:** oversized packets may fragment (IPv4) or fail with "packet too big" → modern …
- **Black holes:** ICMP blocked + DF set → large packets die silently while small ones work.

## Technical Details
| Layer | Typical MTU |
|-------|-------------|
| Ethernet | 1500 bytes (often) |
| PPPoE | 1492 |
| GRE/VPN overlay | 1400 or lower — encap overhead |
| IPv6 minimum | 1280 (RFC 8200) |

- IP header + transport header reduce usable application payload.
- TCP MSS is negotiated in SYN options as roughly MTU − 40 (IPv4) or − 60 (IPv6…

- Routers may fragment IPv4 if DF bit clear; IPv6 routers do **not** fragment
- Lost [[Packet Fragment]] drops the entire datagram.

- Path MTU Discovery (RFC 1191 / RFC 8201): sender sets DF, receives ICMP "pack…

```bash
ping -M do -s 1472 8.8.8.8        # 1472 + 28 = 1500
ip link show eth0 | grep mtu
tracepath example.com
```

| Symptom | Check |
|---------|-------|
| Small OK, large hang | MTU black hole — ICMP blocked |
| VPN flaky | Lower interface MTU on tunnel |
| TCP weird after tunnel | MSS clamping on firewall |

- Firewalls often rewrite TCP MSS in SYN packets to avoid fragmentation through…

```bash
iptables -t mangle -A FORWARD -p tcp --tcp-flags SYN,RST SYN -j TCPMSS --clamp-mss-to-pmtu
```

## Mistakes to Avoid
- **Mistake:** Assuming every path is 1500
- **Mistake:** Blocking ICMP and then blaming "TCP" for large-transfer stalls
- **Mistake:** Tuning only server MTU while client or middlebox MTU still misma…
- **Mistake:** Forgetting IPv6 minimum MTU (1280) and router non-fragmentation …

## Pros/Cons or Trade-offs
- **Pro:** Larger MTU means fewer packets and less header overhead on a given path.
- **Con:** Overlays shrink effective MTU; mismatched MTU without working PMTUD causes hard-to-debug hangs.

## Comparison
- vs [[Packet Fragment]]: MTU is the size limit


### Use cases
- VPN/overlay networks, PPPoE last-mile links, and container/bridge paths with …
