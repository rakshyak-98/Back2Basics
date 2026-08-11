[[Networking]] [[Egress and Ingress]] [[NAT (Network Address Translation)]] [[network gateway]]

# outbound ip

> Outbound IP is the address the internet sees when you call out — often a NAT or load-balancer IP, not your private NIC.

---

## Mental model

**Say it in one breath:** Remote APIs whitelist and log *your* source IP; behind NAT that source is the gateway’s public address.

```txt
App 10.0.1.5 ──► NAT / egress GW 203.0.113.9 ──► api.example.com
                 (peer sees 203.0.113.9)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Outbound / egress IP** | Source IP on the wire leaving you | “What SaaS allowlists.” |
| **Inbound IP** | Address clients use to reach you | “Can differ from outbound (LB vs NAT).” |
| **Elastic / static egress** | Stable public IP for leave traffic | “Needed for partner firewalls.” |
| **SNAT** | Source NAT rewrite | “Private → public on the way out.” |

### Typical layouts

| Setup | What peers see |
|-------|----------------|
| Single public server | That server’s public IP |
| Home / corp NAT | Router’s public IP (shared) |
| AWS NAT Gateway / Cloud NAT | NAT’s IP(s) |
| Egress via proxy | Proxy’s IP |

---

## Standard config / commands

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

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Partner “IP not allowed” | `curl ifconfig.me` from the workload | Give them current egress IP(s); pin Elastic IP |
| Works on laptop, fails in VPC | Different egress path | Align NAT / add VPC endpoint / update allowlist |
| Intermittent allowlist fails | Multi-AZ NAT pool | Whitelist entire egress set |
| Inbound DNS OK, outbound blocked | Confused inbound vs outbound IP | Separate LB address from NAT address in docs |

---

## Gotchas

> [!WARNING]
> **Inbound ≠ outbound** — a public ALB/NLB address is not automatically your SNAT address.

> [!WARNING]
> **NAT rebuild / AZ failover** — egress IP can change unless you designed for static EIPs.

> [!WARNING]
> **Shared office IP** — many tenants share one egress; IP allowlists are coarse and brittle.

---

## When NOT to use

- **IP allowlist as the only auth** — stealable/shared; use tokens + mTLS.
- **Assuming instance metadata public IP is egress** — routing may force a NAT.
- **Hard-coding egress in clients** — discover via config/ops, not compile-time constants.

---

## Related

[[Networking]] [[Egress and Ingress]] [[NAT (Network Address Translation)]] [[network gateway]] [[address port]]
