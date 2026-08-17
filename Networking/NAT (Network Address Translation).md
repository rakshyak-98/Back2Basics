[[NAT Traversal]] [[non-Routable address]] [[CIDR (Classless Inter-Domain Routing)]] [[STUN (Session Traversal Utilities for NAT)]] [[Egress traffic]]

# NAT (Network Address Translation)

> NAT rewrites addresses and ports so many private hosts share one public IP — expired UDP mappings and broken inbound connections are the daily failure mode.

```txt
        NAT (Network Addre ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers ask about NAT to see if you understand private addressing, trans…

## Sources
- [RFC 3022 — Traditional IP Network Address Translator](https://www.rfc-editor.org/rfc/rfc3022) — deep-dive
- [RFC 1918 — Private Address Space](https://www.rfc-editor.org/rfc/rfc1918) — overview
- [Wikipedia — Network address translation](https://en.wikipedia.org/wiki/Network_address_translation) — overview

## Key Concepts
- **Translation table:** inside IP:port ↔ outside IP:port → return packets find the right host.
- **SNAT / masquerade:** many inside → one outside IP → IPv4 sharing at the edge.
- **DNAT / port forward:** outside:port → specific inside host → deliberate inbound.
- **Hairpin NAT:** inside host reaches another via the public IP → same-LAN “public” access.
- **Idle timeouts:** TCP tracks connection state


- **Core:** NAT (often meaning NAPT) maintains a translation table that rewrites packet a…

## Technical Details
```
Inside 192.168.1.50:54321  →  Outside 203.0.113.10:40001
Inside 192.168.1.51:54321  →  Outside 203.0.113.10:40002
```

- Outbound packets get source rewritten
- Carrier-grade NAT (CGNAT) adds another layer

```bash
# iptables MASQUERADE (simplified)
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
conntrack -L | head
```

## Mistakes to Avoid
- **Mistake:** Assuming inbound connections “just work” to a private host witho…
- **Mistake:** Ignoring UDP idle timers for VoIP, gaming, and WebRTC
- **Mistake:** Confusing firewall policy with NAT

## Pros/Cons or Trade-offs
- **Pro:** Eased IPv4 exhaustion; simple private LAN addressing.
- **Con:** Broke end-to-end transparency; inbound and P2P need extra machinery.
- **Con:** CGNAT / double NAT makes debugging and traversal harder.

## Comparison
- vs pure [[CIDR (Classless Inter-Domain Routing)]] routing: CIDR forwards without rewriting
- vs IPv6: end-to-end addresses reduce need for address sharing; firewall policy still required.
- Related: [[NAT Traversal]], [[STUN (Session Traversal Utilities for NAT)]], [[Egress traffic]].


### Use cases
- Home routers, cloud VPC egress, and mobile carrier networks all NAT outbound …

- **Example:** WebRTC call fails on UDP after ~60s of silence
