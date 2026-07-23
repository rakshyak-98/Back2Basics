[[AWS Networking]] [[AWS EC2]] [[half-open connections]] [[TLS (Transport Layer Security)]]

# Security Group

> **Stateful virtual firewall** at ENI level — default deny inbound, allow by rule; return traffic automatically permitted. Primary ingress/egress control for EC2, RDS, ELB, Lambda-in-VPC, ElastiCache, etc.

## Mental model

A Security Group (SG) is a **label + rule set** attached to ENIs (instances, load balancers, RDS). Rules are **allow-only** (no deny rules). **Stateful**: if inbound TCP 443 is allowed and connection established, **return packets flow without explicit outbound rule** for that flow.

```
Internet ──► SG(inbound: 443 from 0.0.0.0/0) ──► EC2:443
                │
                └── established reply traffic auto-allowed (stateful)
```

Contrast **NACL** (subnet, stateless, allow/deny). SG is where 90% of "can't connect" tickets are won or lost.

## Standard config / commands

### Tiered SG pattern (prod)

| SG name | Inbound | Outbound |
|---------|---------|----------|
| `alb-public` | 443 from `0.0.0.0/0` | All → `app-sg` on app port |
| `app-private` | app port from `alb-sg` **SG id** | 443 to `0.0.0.0/0` or VPC endpoints only |
| `db-private` | 5432/3306 from `app-sg` **SG id** | none needed (stateful) or restrict |

**Reference SG ids, not CIDR**, for east-west traffic — IPs change; SG membership is stable.

```bash
# Describe SG rules
aws ec2 describe-security-groups --group-ids sg-xxx \
  --query 'SecurityGroups[].{Name:GroupName,Inbound:IpPermissions,Outbound:IpPermissionsEgress}'

# Authorize app ← alb (example)
aws ec2 authorize-security-group-ingress \
  --group-id sg-app \
  --protocol tcp --port 8080 \
  --source-group sg-alb
```

### Rules that survive review

- **No `0.0.0.0/0` on admin ports** (22, 3389) — use SSM Session Manager or bastion with source IP lock.
- **Least privilege ports** — `8080/tcp` not `-1` (all protocols) unless proven necessary.
- **Separate SG per tier** — don't reuse `default` SG.
- **Document why** in SG description tag (`Name`, `Purpose`, `Owner`).

### ELB / target health checks

- ALB health checks come from **ELB nodes** — target SG must allow **traffic from ALB SG** on health check port.
- NLB: clients preserve source IP; rules may need client CIDR or broader inbound on target.

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Connection timeout to EC2/RDS | SG inbound on **destination**; outbound on **source** if non-stateful path | Add SG-to-SG or CIDR rule on correct port |
| Works from one instance, not another | Different SG attachment | Align SG or add missing rule |
| ALB targets unhealthy | Target SG allows ALB SG on app/health port | Open port from `alb-sg` |
| Intermittent after scale-out | New instances missing SG or wrong SG | Launch template SG; ASG verify |
| "SG looks open" but still blocked | **NACL**; route table; app not listening; wrong VPC | SG is necessary not sufficient — check full path ([[AWS Networking]]) |
| IPv6 path broken | Separate IPv6 rules in SG (not implied by IPv4) | Add `::/0` or specific v6 rules explicitly |
| Lambda in VPC can't reach RDS | Lambda SG + RDS SG reciprocal | Lambda SG egress + RDS SG inbound from Lambda SG |

```bash
# Reachability (preferred over guessing)
aws ec2 create-network-insights-path --source sg-xxx --destination sg-yyy ...
# On instance: ss -tlnp | grep :8080  (is anything listening?)
```

## Gotchas

> [!WARNING]
> **Changing SG rules is immediate** — no "apply" delay, but **existing TCP sessions may not pick up new deny** (stateful tracking). Restart connection after rule change.

> [!WARNING]
> **`0.0.0.0/0` outbound on app tier** — common; acceptable if no lateral movement concern, but **VPC endpoints** reduce data exfil surface and NAT cost.

> [!WARNING]
> **Self-referencing rule** (`source-group = same sg`) — valid pattern for cluster mesh; easy to misconfigure into accidental open mesh.

> [!WARNING]
> **Classic Link / peering** — SG can reference peer VPC SG **if** peering + correct account/region setup; cross-region peering **cannot** reference SG by id.

## When NOT to use

- **Subnet-wide block list (deny bad IP)** — SG has no deny; use **NACL** or **AWS Network Firewall** / WAF at edge.
- **Application auth** — SG is network layer; never expose admin API to world because "it's password protected."
- **Replacing IAM** — opening SG to `0.0.0.0/0` on 443 doesn't replace authn/z at app layer.

## Related

[[AWS Networking]] · [[AWS EC2]] · [[half-open connections]] · [[Route53]] · [[NAT (Network Address Translation)]]
