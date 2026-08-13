[[NAT Traversal]] [[non-Routable address]] [[CIDR (Classless Inter-Domain Routing)]] [[STUN (Session Traversal Utilities for NAT)]] [[Egress traffic]]

# NAT (Network Address Translation)

> NAT rewrites addresses and ports so many private hosts share one public IP — the failure mode you see daily is expired UDP mappings and broken inbound connections.

## Mechanism

NAT (standardized behavior in RFC 3022 for NAPT; colloquial "NAT" often means NAPT) maintains a translation table:

```
Inside 192.168.1.50:54321  →  Outside 203.0.113.10:40001
Inside 192.168.1.51:54321  →  Outside 203.0.113.10:40002
```

Outbound packets get source IP/port rewritten; return traffic is demultiplexed by the table entry. [[non-Routable address]] space (RFC 1918) stays local; only the public side needs global routes.

## Types

| Type | Behavior |
|------|----------|
| SNAT / masquerade | Many inside → one outside IP |
| DNAT / port forward | Outside:port → specific inside host |
| Hairpin NAT | Inside host reaches another via public IP |

## Timeouts and state

TCP entries track connection state; UDP entries are idle-timer based (often 30–120 seconds). Silent peers lose mappings — critical for VoIP, gaming, and WebRTC ([[NAT Traversal]], [[STUN (Session Traversal Utilities for NAT)]], [[TURN server (Traversal Using Relays around NAT)]].

## Linux example

```bash
# iptables MASQUERADE (simplified)
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
conntrack -L | head
```

## Trade-offs

NAT broke end-to-end transparency but eased IPv4 exhaustion. IPv6 reduces need for address sharing; firewall policy still required. Carrier-grade NAT (CGNAT) stacks another layer — double NAT complicates [[NAT Traversal]] further.

## Sources

- [RFC 3022 — Traditional IP Network Address Translator](https://www.rfc-editor.org/rfc/rfc3022)
- [RFC 1918 — Private Address Space](https://www.rfc-editor.org/rfc/rfc1918)
- [Wikipedia — Network address translation](https://en.wikipedia.org/wiki/Network_address_translation)
