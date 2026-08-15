[[AWS EC2]] [[AWS Networking]] [[IAM]] [[AWS cli commands]]

# Security group

> A security group is a stateful virtual firewall on an EC2 ENI (or other VPC resources) — if you allow inbound TCP 443, return traffic is permitted automatically without an explicit outbound rule.

## Interview Relevance

Security group interviews check stateful allow-lists, distinction from NACLs, and least-privilege ingress/egress.

## Sources

- [Security groups for your VPC](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-groups.html) — overview
- [Security group rules](https://docs.aws.amazon.com/vpc/latest/userguide/security-group-rules.html) — overview

## Technical Details

```bash
aws ec2 describe-security-groups --group-ids sg-0abc123
aws ec2 authorize-security-group-ingress \
  --group-id sg-0abc123 \
  --protocol tcp --port 443 \
  --cidr 10.0.0.0/8
```

### Rules model

Each rule specifies:

- **Direction** — inbound or outbound (default: allow all outbound)
- **Protocol** — TCP, UDP, ICMP, or all
- **Port range**
- **Source/destination** — CIDR (`10.0.0.0/8`), another security group ID, or prefix list

**Stateful behavior:** response traffic for allowed connections is automatically permitted. Contrast with **network ACLs** (stateless, subnet-level).

```
Client ──► SG inbound allow :443 ──► Instance
         ◄── return traffic allowed (stateful) ◄──
```

### Common patterns

| Pattern | Inbound |
|---------|---------|
| Web server | TCP 80/443 from ALB security group or `0.0.0.0/0` |
| App tier | TCP app port from web tier SG only |
| Bastion | TCP 22 from corporate CIDR |
| Database | TCP 5432 from app tier SG only |

Reference **security group IDs** instead of CIDR when possible — instances can change IP addresses; groups scale with autoscaling.

### Debugging connectivity

1. Confirm instance ENI has expected security groups attached.
2. Check **both** source and destination groups (database must allow app SG).
3. Verify **network ACL** and route table if SG looks correct.
4. Use **VPC Reachability Analyzer** for path validation.

### Limits and gotchas

- Default **deny all inbound** on new groups.
- Cannot block specific IP within an allowed CIDR using SG alone — use NACL or AWS WAF on load balancer.
- **Quotas** on rules per group; use prefix lists for large IP sets.
