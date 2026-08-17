[[Networking]] [[Egress and Ingress]] [[NAT (Network Address Translation)]] [[network gateway]] [[Egress traffic]]

# outbound ip

> Outbound IP is the address the internet sees when you call out — often a NAT or load-balancer IP, not your private NIC.





## Interview Relevance
Interviewers ask this to see if you know inbound and outbound addresses can differ, and that partner firewalls allowlist the SNAT/egress IP — not the private instance address or the public ALB hostname’s A record alone.

## Sources
- [AWS — NAT gateways](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html) — deep-dive
- [RFC 3022 — Traditional NAT](https://www.rfc-editor.org/rfc/rfc3022) — overview
- [Wikipedia — Network address translation](https://en.wikipedia.org/wiki/Network_address_translation) — overview

## Key Concepts
| Word | Plain meaning | Interview phrasing |
|------|---------------|--------------------|
| **Outbound / egress IP** | Source IP on the wire leaving you | “What SaaS allowlists.” |
| **Inbound IP** | Address clients use to reach you | “Can differ from outbound (LB vs NAT).” |
| **Elastic / static egress** | Stable public IP for leave traffic | “Needed for partner firewalls.” |
| **SNAT** | Source NAT rewrite | “Private → public on the way out.” |

Typical layouts:

| Setup | What peers see |
|-------|----------------|
| Single public server | That server’s public IP |
| Home / corporate NAT | Router’s public IP (shared) |
| AWS NAT Gateway / Cloud NAT | NAT’s IP(s) |
| Egress via proxy | Proxy’s IP |

## Technical Details
```txt
App 10.0.1.5 ──► NAT / egress GW 203.0.113.9 ──► api.example.com
                 (peer sees 203.0.113.9)
```

```bash
# What the internet sees right now
curl -4 https://ifconfig.me
curl -4 https://checkip.amazonaws.com

# From a cloud instance — confirm NAT path
curl -4 https://ifconfig.me
# compare to instance public IP (may differ if forced via NAT)
```

| Knob | Why it matters |
|------|----------------|
| NAT Gateway EIP | Stable allowlist target |
| Multiple NATs | Partners must allow *all* egress IPs |
| HTTP proxy `HTTPS_PROXY` | Overrides “instance IP” with proxy IP |

| Symptom | Check | Fix |
|---------|-------|-----|
| Partner “IP not allowed” | `curl ifconfig.me` from the workload | Give them current egress IP(s); pin Elastic IP |
| Works on laptop, fails in VPC | Different egress path | Align NAT / add VPC endpoint / update allowlist |
| Intermittent allowlist fails | Multi-AZ NAT pool | Whitelist entire egress set |
| Inbound DNS OK, outbound blocked | Confused inbound vs outbound IP | Separate LB address from NAT address in docs |

## Real-World Applications
SaaS webhooks, bank APIs, and partner firewalls that only accept traffic from known source IPs.

**Example:** Production workers sit behind a NAT Gateway with reserved Elastic IPs; the partner’s ACL lists those EIPs, not the Autoscale group’s changing private addresses.

## Pros/Cons or Trade-offs
- **Pro:** One (or few) stable IPs for allowlists and audit logs.
- **Con:** Shared office or multi-tenant egress IP is coarse — many tenants look identical.
- **Con:** NAT rebuild / AZ failover can change egress IP unless you designed for static EIPs.
- **Con:** IP allowlist alone is weak authentication — stealable and shared.

## Comparison
- vs inbound / LB address: clients hit the ALB/NLB; your SNAT address for outbound can be a different EIP.
- vs [[Egress traffic]]: egress is the flow and path; outbound IP is the rewritten source identity.
- vs [[network gateway]]: gateway is the next hop; outbound IP is what appears after that hop NATs you.

## Mistakes to Avoid
- Treating inbound ≠ outbound as the same address — public ALB/NLB is not automatically your SNAT address.
- Assuming instance metadata’s public IP is egress — routing may force a NAT.
- Hard-coding egress in clients — discover via configuration/operations, not compile-time constants.
- Using IP allowlist as the only authentication — prefer tokens and mutual TLS alongside it.
