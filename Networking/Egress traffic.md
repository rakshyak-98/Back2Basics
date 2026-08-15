[[NAT (Network Address Translation)]] [[Egress and Ingress]] [[routing table]] [[outbound ip]] [[Network error]]

# Egress traffic

> Outbound packets leaving your network boundary toward the internet or another VPC — billed, filtered, and NAT'd differently from ingress.

## Interview Relevance

Interviewers use egress to test whether you separate outbound paths (NAT, filtering, cost) from inbound (load balancer, security groups) and can debug “private subnet has no internet” without opening inbound.

## Sources

- [AWS — NAT gateways](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html) — deep-dive
- [AWS — NAT gateway basics](https://docs.aws.amazon.com/vpc/latest/userguide/nat-gateway-basics.html) — overview
- [Wikipedia — Egress filtering](https://en.wikipedia.org/wiki/Egress_filtering) — overview

## Key Concepts

- **Egress vs ingress:** source inside, destination outside (relative to the trust boundary) → opposite of inbound client traffic.
- **NAT egress:** private hosts reach the internet without public IPs → return traffic only for established flows.
- **Egress filtering:** security groups, NACLs, firewall policies on outbound → reduce data exfiltration and unwanted callbacks.
- **Cost asymmetry:** cloud often bills NAT processing and data transfer out → egress volume shows up on the invoice.

## Technical Details

```txt
Private subnet VM ──► NAT GW ──► IGW ──► Internet   (egress)
Internet ──► IGW ──► ALB ──► app                    (ingress)
```

Cloud patterns:

- **Private instances** use a NAT Gateway or NAT instance for egress — no unsolicited inbound.
- **Return traffic** must match stateful firewall/NAT bindings; you control both directions via route tables.
- **Why NAT GW:** gives private RFC1918 hosts outbound internet without a public IP on each VM.

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

# K8s pod (if monitoring)
kubectl top pod -A --sort-by=network
```

| Symptom | Check | Fix |
|---------|-------|-----|
| No outbound internet from private subnet | Route to NAT; NAT in public subnet | `0.0.0.0/0` → nat-id; NAT has EIP |
| Egress works, return fails | SG stateful; asymmetric routing | Allow return on SG; fix multi-homed routes |
| Surprise cloud bill | NAT GW + cross-AZ | VPC endpoints for S3; same-AZ NAT; flow logs |
| Geo-blocked egress | Egress IP is NAT pool | Proxy in allowed region; VPN |

## Real-World Applications

Private application tiers that pull packages, call external APIs, or push metrics while remaining unreachable from the public internet.

**Example:** API pods in a private subnet route `0.0.0.0/0` to a NAT Gateway; partners allowlist the NAT’s Elastic IP(s), not each pod IP.

## Pros/Cons or Trade-offs

- **Pro:** Outbound-only internet for private workloads without exposing each host.
- **Pro:** Central place to filter and observe outbound traffic.
- **Con:** NAT Gateway cost and AZ placement complexity; cross-AZ traffic can double-charge.
- **Con:** Shared egress IPs couple many services to one allowlist surface.

## Comparison

- vs [[Egress and Ingress]]: that note frames both directions; this leaf is outbound-only detail.
- vs [[outbound ip]]: egress is the flow; outbound IP is the source address peers see after SNAT.
- vs public subnet + IGW: direct egress with public IPs — simpler routing, weaker isolation.

## Mistakes to Avoid

- Routing a private subnet’s default route to a NAT that lives only in another AZ — AZ-local black hole when that NAT fails or is missing.
- NAT’ing everything when the tier needs direct inbound — split tiers: public LB for ingress, private app egress via NAT.
- Ignoring DNS and API egress as a data-leak path — prefer VPC endpoints for cloud APIs where available.
- Assuming inbound load-balancer IPs are your egress allowlist targets.
