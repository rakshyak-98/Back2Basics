[[NAT Traversal]] [[non-Routable address]] [[CIDR (Classless Inter-Domain Routing)]] [[STUN (Session Traversal Utilities for NAT)]] [[Egress traffic]]

# NAT (Network Address Translation)

> NAT rewrites addresses and ports so many private hosts share one public IP — expired UDP mappings and broken inbound connections are the daily failure mode.





## Interview Relevance
Interviewers ask about NAT to see if you understand private addressing, translation tables, and why inbound/P2P connectivity needs [[NAT Traversal]] (STUN/TURN/ICE) — not just “NAT saves IPv4.”

## Sources
- [RFC 3022 — Traditional IP Network Address Translator](https://www.rfc-editor.org/rfc/rfc3022) — deep-dive
- [RFC 1918 — Private Address Space](https://www.rfc-editor.org/rfc/rfc1918) — overview
- [Wikipedia — Network address translation](https://en.wikipedia.org/wiki/Network_address_translation) — overview

## Core Definition
NAT (often meaning NAPT) maintains a translation table that rewrites packet addresses/ports on the way out and demultiplexes return traffic on the way in so [[non-Routable address]] space stays local.

## Key Concepts
- **Translation table:** inside IP:port ↔ outside IP:port → return packets find the right host.
- **SNAT / masquerade:** many inside → one outside IP → IPv4 sharing at the edge.
- **DNAT / port forward:** outside:port → specific inside host → deliberate inbound.
- **Hairpin NAT:** inside host reaches another via the public IP → same-LAN “public” access.
- **Idle timeouts:** TCP tracks connection state; UDP is timer-based (often 30–120s) → silent peers lose mappings.

## Technical Details
```
Inside 192.168.1.50:54321  →  Outside 203.0.113.10:40001
Inside 192.168.1.51:54321  →  Outside 203.0.113.10:40002
```

Outbound packets get source rewritten; only the public side needs global routes. Carrier-grade NAT (CGNAT) adds another layer — double NAT complicates traversal further.

```bash
# iptables MASQUERADE (simplified)
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
conntrack -L | head
```

## Real-World Applications
Home routers, cloud VPC egress, and mobile carrier networks all NAT outbound traffic.

**Example:** WebRTC call fails on UDP after ~60s of silence — NAT mapping expired; keepalives or a [[TURN server (Traversal Using Relays around NAT)]] relay fix it.

## Pros/Cons or Trade-offs
- **Pro:** Eased IPv4 exhaustion; simple private LAN addressing.
- **Con:** Broke end-to-end transparency; inbound and P2P need extra machinery.
- **Con:** CGNAT / double NAT makes debugging and traversal harder.

## Comparison
- vs pure [[CIDR (Classless Inter-Domain Routing)]] routing: CIDR forwards without rewriting; NAT rewrites.
- vs IPv6: end-to-end addresses reduce need for address sharing; firewall policy still required.
- Related: [[NAT Traversal]], [[STUN (Session Traversal Utilities for NAT)]], [[Egress traffic]].

## Mistakes to Avoid
- Assuming inbound connections “just work” to a private host without DNAT or traversal.
- Ignoring UDP idle timers for VoIP, gaming, and WebRTC.
- Confusing firewall policy with NAT — they often sit together but solve different problems.
