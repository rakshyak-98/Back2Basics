[[AWS EC2]] [[AWS Networking]] [[Security group]] [[Route53]]

# Elastic IP

> An Elastic IP is a static public IPv4 address you allocate to your account and associate with an instance or network interface — it survives stop/start but costs money when allocated and not attached.

```txt
        Elastic IP ──┬── Interview
               ├── Sources
               ├── Mechanism
               └── Use cases
```

## Interview Relevance
- **Interview probes:** Elastic IP questions cover public addressing, costs when unattached, and alte…

## Sources
- [Elastic IP addresses](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/elastic-ip-addresses-eip.html) — overview
- [AWS EC2 pricing — Elastic IP](https://aws.amazon.com/ec2/pricing/on-demand/) — overview

## Technical Details
### Behavior

- **Regional:** resource tied to your VPC-capable account.
- **Reassociable:** — move between instances or ENIs without changing the public address clients …
- **Default limit:** — five EIPs per region (increase via support ticket).
- **Billing:** — charged when allocated to your account and not associated with a running in…

### Associate

```bash
aws ec2 allocate-address --domain vpc
aws ec2 associate-address --instance-id i-0abc --allocation-id eipalloc-0abc
```

- Disassociate before terminating the instance if you need to preserve the addr…

### IPv6 note

- Elastic IPs apply to **IPv4**.
- IPv6 addresses on VPC subnets are separate CIDR allocations

## Real-World Applications
| Use | Alternative |
|-----|-------------|
| Legacy server needs fixed public IP | Application Load Balancer + [[Route53]] |
| NAT instance (uncommon) | Managed NAT Gateway |
| Quick demo / single EC2 | Often unnecessary — use instance public DNS |

- **Note:** For production HTTP services, prefer a load balancer with health checks rathe…
