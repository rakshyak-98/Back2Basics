[[non-Routable address]] [[routing table]] [[BGP]] [[autonomous system]] [[address port]] [[NAT (Network Address Translation)]]

# CIDR (Classless Inter-Domain Routing)

> CIDR notation (`203.0.113.0/24`) expresses how many bits are the network prefix — mis-sized subnets are the usual cause of "works on VPN, fails on LAN."

```txt
        CIDR (Classless In ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers ask CIDR to confirm you can size subnets, read masks, and explai…

## Sources
- [RFC 4632 — Classless Inter-domain Routing (CIDR)](https://www.rfc-editor.org/rfc/rfc4632) — deep-dive
- [RFC 1918 — Address Allocation for Private Internets](https://www.rfc-editor.org/rfc/rfc1918) — deep-dive
- [Wikipedia — Classless Inter-Domain Routing](https://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing) — overview

## Key Concepts
- **Prefix length:** the slash counts network bits → longer prefix means a smaller network and a m…
- **Classless addressing:** replaced classful A/B/C → arbitrary boundaries like /26 or /22 are normal.
- **Aggregation:** ISPs advertise large aggregates via [[BGP]] → limits global [[routing table]]…
- **Private space:** RFC 1918 ranges are not globally routable → [[NAT (Network Address Translatio…

## Technical Details
- CIDR (RFC 4632) notation:

| Notation | Mask | Hosts (usable) |
|----------|------|----------------|
| /32 | 255.255.255.255 | 1 (point-to-point) |
| /24 | 255.255.255.0 | 254 |
| /16 | 255.255.0.0 | 65,534 |
| /8 | 255.0.0.0 | ~16M |

- Longer prefix = smaller network (more specific route).
- `/25` is half the addresses of `/24`.

- ISPs advertise aggregates to the global table to limit [[routing table]] grow…
- Your `/24` may be part of a provider's `/20` announcement via [[BGP]].

- Private and special ranges (RFC 1918):

| Range | Use |
|-------|-----|
| 10.0.0.0/8 | Large private networks |
| 172.16.0.0/12 | Private |
| 192.168.0.0/16 | Home/office LAN |

- See [[non-Routable address]]

```bash
ipcalc 203.0.113.50/26
python3 -c "import ipaddress; n=ipaddress.ip_network('10.0.1.0/24'); print(n.network_address, n.broadcast_address, n.num_addresses)"
```

## Mistakes to Avoid
- **Mistake:** Off-by-one host counts
- **Mistake:** Overlapping subnets across VPN and LAN
- **Mistake:** Treating a longer prefix as "bigger network"
- **Mistake:** Advertising private space to the public internet without underst…

## Pros/Cons or Trade-offs
- **Pro:** Flexible subnet sizing and route aggregation; clear longest-prefix-match semantics.
- **Con:** Easy to mis-size (too small → exhaustion; overlapping → ambiguous routing); operators must remember usable host counts exclude network/broadcast on IPv4.

## Comparison
- vs classful addressing: classes fixed /8, /16, /24 boundaries


### Use cases
- VPC subnet design, firewall allow-lists, and BGP prefix announcements. Exampl…
