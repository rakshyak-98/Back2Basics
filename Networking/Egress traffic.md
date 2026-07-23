[[NAT (Network Address Translation)]] [[Egress and Ingress]] [[routing table]] [[AWS]]

# Egress traffic

> Outbound packets leaving your network boundary toward the internet or another VPC — billed, filtered, and NAT'd differently from ingress.

---

## Mental model

**Egress** = source inside, destination outside (relative to trust boundary):

```txt
Private subnet VM ──► NAT GW ──► IGW ──► Internet   (egress)
Internet ──► IGW ──► ALB ──► app                    (ingress)
```

Cloud patterns:
- **Private instances** use **NAT Gateway/instance** for egress — no unsolicited inbound
- **Egress filtering** — security groups (allow outbound?), NACLs, firewall policies
- **Cost** — AWS charges per-GB **processed** by NAT GW + data transfer out to internet

Ingress and egress asymmetry: you control routing tables for both; **return traffic** must match stateful firewall/NAT bindings.

---

## Standard config / commands

### AWS VPC (standard NAT egress)

```txt
Flow: Private Subnet → Route 0.0.0.0/0 → NAT GW → IGW → Internet
```

```bash
# Route table check (AWS CLI)
aws ec2 describe-route-tables --filters Name=vpc-id,Values=vpc-xxx

# NAT GW metrics: CloudWatch BytesOutToDestination
```

### Linux host — policy routing / mark

```bash
ip route get 8.8.8.8 from 10.0.1.5
iptables -t nat -L -n -v
```

### Measure egress volume

```bash
# Host
nload eth0
vnstat -l

# K8s pod (ifmonitoring)
kubectl top pod -A --sort-by=network
```

**Why NAT GW:** gives private RFC1918 hosts outbound internet without public IPs on each VM.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| No outbound internet from private subnet | Route to NAT; NAT in public subnet | 0.0.0.0/0 → nat-id; NAT has EIP |
| Egress works, return fails | SG stateful; asymmetric routing | Allow return on SG; fix multi-homed routes |
| Surprise cloud bill | NAT GW + cross-AZ | VPC endpoints for S3; same-AZ NAT; flow logs |
| Geo-blocked egress | Egress IP is NAT pool | Proxy in allowed region; VPN |

---

## Gotchas

> [!WARNING]
> **NAT GW is AZ-specific** — route in AZ without NAT = black hole for that subnet.

> [!WARNING]
> **Cross-AZ NAT traffic** double-charges on some clouds.

> [!WARNING]
> **DNS egress** — apps calling external APIs leak data; use VPC endpoints where available.

---

## When NOT to use

Don't NAT **everything** if instances need direct inbound (public ALB on app tier) — split tiers: public LB ingress, private app egress via NAT.

---

## Related

[[NAT (Network Address Translation)]] [[Egress and Ingress]] [[routing table]] [[Network error]] [[AWS Networking]]
