[[NAT (Network Address Translation)]] [[Egress and Ingress]] [[routing table]] [[outbound ip]] [[Network error]]

# Egress traffic

> Outbound packets leaving your network boundary toward the internet or another VPC — billed, filtered, and NAT'd differently from ingress.

```txt
        Egress traffic ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers use egress to test whether you separate outbound paths (NAT, fil…

## Sources
- [AWS — NAT gateways](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html) — deep-dive
- [AWS — NAT gateway basics](https://docs.aws.amazon.com/vpc/latest/userguide/nat-gateway-basics.html) — overview
- [Wikipedia — Egress filtering](https://en.wikipedia.org/wiki/Egress_filtering) — overview

## Key Concepts
- **Egress vs ingress:** source inside, destination outside (relative to the trust boundary) → opposit…
- **NAT egress:** private hosts reach the internet without public IPs → return traffic only for…
- **Egress filtering:** security groups, NACLs, firewall policies on outbound → reduce data exfiltrat…
- **Cost asymmetry:** cloud often bills NAT processing and data transfer out → egress volume shows …

## Technical Details
```txt
Private subnet VM ──► NAT GW ──► IGW ──► Internet   (egress)
Internet ──► IGW ──► ALB ──► app                    (ingress)
```

- Cloud patterns:

- **Private instances:** use a NAT Gateway or NAT instance for egress — no unsolicited inbound.
- **Return traffic:** must match stateful firewall/NAT bindings
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

## Mistakes to Avoid
- **Mistake:** Routing a private subnet’s default route to a NAT that lives onl…
- **Mistake:** NAT’ing everything when the tier needs direct inbound
- **Mistake:** Ignoring DNS and API egress as a data-leak path
- **Mistake:** Assuming inbound load-balancer IPs are your egress allowlist tar…

## Pros/Cons or Trade-offs
- **Pro:** Outbound-only internet for private workloads without exposing each host.
- **Pro:** Central place to filter and observe outbound traffic.
- **Con:** NAT Gateway cost and AZ placement complexity; cross-AZ traffic can double-charge.
- **Con:** Shared egress IPs couple many services to one allowlist surface.

## Comparison
- vs [[Egress and Ingress]]: that note frames both directions; this leaf is outbound-only detail.
- vs [[outbound ip]]: egress is the flow; outbound IP is the source address peers see after SNAT.
- vs public subnet + IGW: direct egress with public IPs — simpler routing, weaker isolation.


### Use cases
- Private application tiers that pull packages, call external APIs, or push met…

- **Example:** API pods in a private subnet route `0.0.0.0/0` to a NAT Gateway
