[[non-Routable address]] [[routing table]] [[BGP]] [[autonomous system]] [[address port]]

# CIDR (Classless Inter-Domain Routing)

> CIDR notation (`203.0.113.0/24`) expresses how many bits are the network prefix — mis-sized subnets are the usual cause of "works on VPN, fails on LAN."

## Prefix notation

CIDR (RFC 4632) replaced classful A/B/C addressing. A slash suffix counts **network bits**:

| Notation | Mask | Hosts (usable) |
|----------|------|----------------|
| /32 | 255.255.255.255 | 1 (point-to-point) |
| /24 | 255.255.255.0 | 254 |
| /16 | 255.255.0.0 | 65,534 |
| /8 | 255.0.0.0 | ~16M |

Longer prefix = smaller network (more specific route). `/25` is half the addresses of `/24`.

## Aggregation

ISPs advertise aggregates to the global table to limit [[routing table]] growth. Your `/24` may be part of a provider's `/20` announcement via [[BGP]].

## Private and special ranges (RFC 1918)

| Range | Use |
|-------|-----|
| 10.0.0.0/8 | Large private networks |
| 172.16.0.0/12 | Private |
| 192.168.0.0/16 | Home/office LAN |

See [[non-Routable address]] — not globally routable; [[NAT (Network Address Translation)]] maps them to public space.

## Quick calculations

```bash
ipcalc 203.0.113.50/26
python3 -c "import ipaddress; n=ipaddress.ip_network('10.0.1.0/24'); print(n.network_address, n.broadcast_address, n.num_addresses)"
```

## Sources

- [RFC 4632 — Classless Inter-domain Routing (CIDR)](https://www.rfc-editor.org/rfc/rfc4632)
- [RFC 1918 — Address Allocation for Private Internets](https://www.rfc-editor.org/rfc/rfc1918)
- [Wikipedia — Classless Inter-Domain Routing](https://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing)
