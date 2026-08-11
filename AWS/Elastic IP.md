[[AWS Networking]] [[AWS EC2]] [[Route53]] [[NAT (Network Address Translation)]] [[AWS Billing and cost management]]

# AWS Elastic IP (EIP)

> Elastic IP — static public IPv4 in a region that survives instance stop/start.

---

## Mental model

An Elastic IP is a **regional, static public IPv4** you allocate into your account and **associate** with a network interface (usually an EC2 instance's primary ENI, or a NAT Gateway's ENI). It is **not** tied to an AZ until associated — the ENI's subnet/AZ defines placement.

```
Allocate EIP (regional pool)
       │
       ├── Associate ──► EC2 instance / ENI (public subnet + IGW route)
       │                 └── DNS A record → stable target
       │
       └── Associate ──► NAT Gateway (public subnet) ──► private subnet egress
```

| Concept | Behavior |
|---------|----------|
| **Public IP vs EIP** | Auto-assigned public IP changes on stop/start; EIP persists until released |
| **Association** | 1:1 with an ENI; secondary private IPs on same ENI can each have their own EIP |
| **Stopped instance** | EIP stays associated but **bills** while instance is stopped (see gotchas) |
| **Region** | EIP cannot move regions — release and allocate new in target region |
| **IPv6** | No EIP; use IPv6 CIDR + optional static IPv6 on ENI |

Every EIP needs a **public subnet** route to an **Internet Gateway** for inbound internet reachability. Outbound from the instance still uses the EIP as source when associated.

## Standard config / commands

### When to use EIP

| Use case | Typical target | Alternative |
|----------|----------------|-------------|
| Single EC2 with apex DNS (`@` A record) | Instance primary ENI | ALB + Route53 ALIAS (preferred for prod web) |
| Bastion / fixed allowlist IP | Bastion ENI | SSM Session Manager (no public IP) |
| NAT Gateway public face | Auto-allocated or bring-your-own EIP | NAT instance (legacy); VPC endpoints to cut NAT traffic |
| Third-party IP allowlisting | EIP on egress NAT or app tier | AWS Global Accelerator, fixed egress via NAT |

### Allocate and associate (CLI)

```bash
# 1) Allocate — tags help cost cleanup
aws ec2 allocate-address \
  --domain vpc \
  --tag-specifications 'ResourceType=elastic-ip,Tags=[{Key=Name,Value=app-prod-eip},{Key=Environment,Value=prod}]'

# Returns: AllocationId (eipalloc-xxx), PublicIp (x.x.x.x)

# 2) Associate to a running instance (uses primary ENI)
aws ec2 associate-address \
  --instance-id i-0abc123 \
  --allocation-id eipalloc-0def456

# Or associate to a specific ENI / private IP (secondary IP pattern)
aws ec2 associate-address \
  --allocation-id eipalloc-0def456 \
  --network-interface-id eni-0ghi789 \
  --private-ip-address 10.0.1.50

# 3) Verify
aws ec2 describe-addresses --allocation-ids eipalloc-0def456 \
  --query 'Addresses[].{PublicIp:PublicIp,InstanceId:InstanceId,AssociationId:AssociationId,NetworkInterfaceId:NetworkInterfaceId}'

# 4) Disassociate (EIP remains in account — still may bill if idle)
aws ec2 disassociate-address --association-id eipassoc-0jkl012

# 5) Release (permanent — frees the IP back to AWS pool)
aws ec2 release-address --allocation-id eipalloc-0def456
```

### Console path

```txt
EC2 → Network & Security → Elastic IPs
  Allocate Elastic IP address
    Network border group: default (or Local Zone / Wavelength group if applicable)
    Public IPv4 address pool: Amazon's pool (or BYOIP pool if configured)
  Actions → Associate Elastic IP address
    Resource type: Instance | Network interface
    Instance / ENI → Private IP (optional for secondary)
```

### Configuration knobs

| Setting | Standard prod choice | Why |
|---------|---------------------|-----|
| **Domain** | `vpc` | EC2-Classic is retired; always VPC-scoped |
| **Network border group** | `default` unless edge placement | Pins EIP to a metro/edge; wrong group = can't associate to subnet |
| **Public IPv4 pool** | Amazon pool | Use BYOIP pool only when you own the prefix |
| **Tags** | `Name`, `Environment`, `Owner` | Orphan EIP audits in Cost Explorer |
| **Subnet** | Public tier with `0.0.0.0/0 → igw-xxx` | Private subnet ENI won't get working inbound internet |
| **Auto-assign public IP** | Off on prod app tiers | Prefer ALB or explicit EIP only where needed |
| **IMDS / SG** | SG allows 80/443 from internet if web | EIP alone does not open ports — [[Security group]] still gates traffic |

### DNS (static apex / single VM)

```txt
Route53 hosted zone (or external DNS):
  Type A   yourdomain.com      → <EIP PublicIp>     TTL 300–600
  Type A   www.yourdomain.com  → <EIP PublicIp>     (or CNAME to apex)

Route53 ALIAS (same region):
  Record type A (ALIAS) → Elastic IP allocation — avoids extra hop vs plain A
```

See [[How to connect Godaddy domain with AWS EC2 instance]] for full registrar + HTTPS runbook.

### NAT Gateway EIP

NAT Gateway creation in a **public subnet** automatically allocates and associates an EIP (or you can specify an allocation ID):

```bash
aws ec2 create-nat-gateway \
  --subnet-id subnet-public-az-a \
  --allocation-id eipalloc-nat-az-a \
  --tag-specifications 'ResourceType=natgateway,Tags=[{Key=Name,Value=nat-az-a}]'
```

Private subnet route table: `0.0.0.0/0 → nat-xxx`. One NAT per AZ is the HA pattern; each NAT holds its own EIP.

### Limits and quotas

```bash
# Default: 5 EIPs per Region per account (associated or not)
aws service-quotas get-service-quota \
  --service-code ec2 \
  --quota-code L-0263D0A3

# Request increase via Service Quotas console if bastion + multi-AZ NAT + legacy VMs exceed cap
```

### Cleanup after EC2 terminate

```bash
# Orphan EIPs (no association) — common after terminate
aws ec2 describe-addresses \
  --query 'Addresses[?AssociationId==null].{AllocationId:AllocationId,PublicIp:PublicIp,Tags:Tags}'

# Release each orphan
aws ec2 release-address --allocation-id eipalloc-xxx
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Can't SSH/curl by EIP | [[Security group]] inbound; app bind address; NACL | Open 22/80/443; listen `0.0.0.0`; verify subnet is public + IGW route |
| EIP shows associated but no inbound | Route table on instance subnet → IGW? | Associate subnet with public route table; attach IGW to VPC |
| DNS points to old IP after change | `dig +short domain A`; TTL cache | Lower TTL before migration; update A/ALIAS to new EIP |
| IP changed after stop/start | Was auto public IP, not EIP | Allocate + associate EIP before relying on DNS |
| `AddressLimitExceeded` | `describe-addresses` count in region | Release unused EIPs; request quota increase |
| EIP won't associate to ENI | ENI in public subnet? Same region? | Move ENI to public subnet or pick ENI in correct VPC/region |
| Private instance "has EIP" but no internet in | Expectation mismatch — inbound only via EIP path | Outbound from private subnet needs NAT, not EIP on instance |
| Bill for "EC2-Other" / Elastic IP | EIP unassociated or on **stopped** instance | Start instance, disassociate + release, or associate to running resource |
| NAT works one AZ, not another | Per-AZ NAT + route table association | Each private subnet RT must point to NAT in **same** AZ |
| Association fails after ENI swap | Stale association on old ENI | Disassociate from old ENI; associate to new primary ENI |

## Gotchas

> [!WARNING]
> **Unassociated EIP bills hourly** — and EIPs on **stopped** instances also bill. Free tier: first **one** EIP associated with a **running** instance is free; extras and idle EIPs are not.

> [!WARNING]
> **Terminate EC2 does not release EIP** — allocation persists with `AssociationId=null`. Add release to teardown runbooks ([[AWS EC2]]).

> [!WARNING]
> **EIP is regional** — DR failover to another region requires new allocation, DNS update, and often new AMIs/snapshots in that region.

> [!WARNING]
> **Replacing instance by launch (not stop/start)** — new instance gets new instance id; re-associate the **same** EIP to avoid DNS churn.

> [!WARNING]
> **Secondary private IP + multiple EIPs** on one ENI is advanced — easy to mis-route if app binds only primary IP.

> [!WARNING]
> **Network border group mismatch** — EIP allocated in a Local Zone border group cannot associate to a standard regional subnet.

## When NOT to use

- **Production web behind scaling or blue/green** — use ALB/NLB + Route53 ALIAS; don't pin users to one instance EIP.
- **Private app/database tiers** — no public IP; use internal LB and [[NAT (Network Address Translation)]] for outbound only.
- **IPv6-only workloads** — use IPv6 addressing; EIP is IPv4-only.
- **Avoiding NAT cost by EIP on every instance** — security and ops overhead; prefer VPC endpoints + single NAT per AZ.
- **Cross-region static IP** — use Global Accelerator or DNS-based failover; EIP does not span regions.

## Related

[[AWS Networking]] · [[AWS EC2]] · [[Route53]] · [[Security group]] · [[NAT (Network Address Translation)]] · [[How to connect Godaddy domain with AWS EC2 instance]] · [[AWS Billing and cost management]] · [[Networking/Egress traffic]]
