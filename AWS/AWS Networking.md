[[Security group]] [[Elastic IP]] [[Route53]] [[AWS EC2]] [[IAM]]

# AWS Networking

> AWS networking is VPC-centric: you define IP ranges, subnets per Availability Zone, route tables, gateways, and firewalls — most "cannot connect" incidents are routing or security group mistakes, not broken cables.

```txt
        AWS Networking ──┬── Interview
               ├── Sources
               └── Mechanism
```

## Interview Relevance
- **Interview probes:** Interviewers ask about AWS Networking to see whether you can design and opera…

## Sources
- [What is Amazon VPC?](https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html) — overview
- [VPC with public and private subnets](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Scenario2.html) — overview

## Technical Details
### VPC building blocks

```
                    Internet
                        │
                   Internet Gateway (IGW)
                        │
              ┌─────────┴─────────┐
              │   Public subnet   │  route 0.0.0.0/0 → IGW
              │   (ALB, bastion)  │
              └─────────┬─────────┘
                        │
              ┌─────────┴─────────┐
              │  Private subnet   │  route 0.0.0.0/0 → NAT Gateway
              │  (app, workers) │
              └─────────┬─────────┘
                        │
              ┌─────────┴─────────┐
              │  Isolated subnet  │  no default route to internet
              │  (database)     │
              └─────────────────┘
```

| Component | Role |
|-----------|------|
| **VPC** | Private IPv4/IPv6 network (`10.0.0.0/16`, etc.) |
| **Subnet** | AZ-scoped slice; public if route to IGW exists |
| **Route table** | Per-subnet forwarding rules |
| **Internet Gateway** | Bidirectional internet for public subnets |
| **NAT Gateway / NAT instance** | Outbound-only internet from private subnets |
| **[[Security group]]** | Stateful ENI firewall |
| **Network ACL** | Stateless subnet firewall (allow/deny lists) |
| **VPC endpoints** | Private connectivity to AWS APIs (S3, DynamoDB, etc.) |
| **Peering / Transit Gateway** | Connect VPCs or on-premises networks |

### DNS inside VPC

- Enable **DNS hostnames** and **DNS resolution** on the VPC.
- Instances receive internal DNS names like `ip-10-0-1-5.ec2.internal`.
- Public hosted zones use [[Route53]].

### Hybrid connectivity

- **Site-to-Site VPN:** — IPsec over internet
- **Direct Connect:** — dedicated circuit to AWS
- **Transit Gateway:** — hub for many VPCs and VPN/DX attachments

### Debugging checklist

1. **Route table** — does the subnet have a path to the destination?
2. **Security group** — inbound on server, outbound on client if restricted
3. **NACL** — ephemeral port return traffic allowed?
4. **Source/destination check** — disabled on NAT instances only when required
5. **VPC Flow Logs** — accept/reject evidence

### CLI snapshot

```bash
aws ec2 describe-vpcs
aws ec2 describe-subnets --filters Name=vpc-id,Values=vpc-0abc
aws ec2 describe-route-tables --filters Name=vpc-id,Values=vpc-0abc
```
