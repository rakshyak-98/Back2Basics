[[AMI (Amazon Machine Image)]] · [[EBS (Elastic Block Store)]] · [[Security group]] · [[Elastic IP]] · [[AWS Networking]]

# AWS EC2

> EC2 provides resizable virtual machines in a VPC — you choose an image, instance type, storage, and security groups; the first outage is usually networking or disk, not the hypervisor.

---

## What you provision

| Choice | Effect |
|--------|--------|
| [[AMI (Amazon Machine Image)]] | Operating system, bootstrap, baked software |
| Instance type | vCPU, memory, network bandwidth, optional GPU |
| [[EBS (Elastic Block Store)]] root volume | Persistent boot disk; snapshot for backups |
| [[Security group]] | Stateful layer-4 firewall on the ENI |
| Subnet | Availability Zone placement; public vs private routing |
| [[Elastic IP]] | Static public IPv4 (optional; costs money when unattached) |
| Key pair | SSH access to Linux (install your public key at launch) |
| IAM instance profile | Role credentials via instance metadata |

An **Elastic Network Interface (ENI)** attaches the instance to a subnet. Multiple ENIs enable multi-homed or management-network patterns.

## Instance lifecycle

```
pending → running → stopping → stopped → shutting-down → terminated
```

**Stop** preserves EBS root volume; **terminate** deletes instance and optionally volumes per launch settings.

## Launch checklist

1. Pick region and AZ for latency and compliance.
2. Select AMI (Amazon Linux, Ubuntu, Windows, or golden image).
3. Size instance for CPU/memory/network — burstable `t*` families accrue CPU credits.
4. Attach security group allowing only required ports (SSH often restricted to bastion CIDR).
5. Place in **private subnet** for app tiers; use load balancer in public subnet for HTTP/S.
6. Enable **detailed monitoring** and **IMDSv2** (`HttpTokens: required`) on the metadata service.

## Operations

```bash
aws ec2 describe-instances --instance-ids i-0abc123
aws ec2 start-instances --instance-ids i-0abc123
aws ec2 stop-instances --instance-ids i-0abc123
```

Connect:

```bash
ssh -i ~/.ssh/my-key.pem ec2-user@<public-dns-or-ip>
```

Default Linux user varies by AMI: `ec2-user` (Amazon Linux), `ubuntu` (Ubuntu), `admin` (Debian).

## Common failure modes

| Symptom | Check |
|---------|-------|
| Cannot SSH | Security group, NACL, wrong key, instance in private subnet without bastion |
| Disk full | [[EBS (Elastic Block Store)]] volume size; expand volume and grow filesystem |
| Status check failed | Instance or underlying hardware — stop/start or replace |
| Metadata access from app | IMDSv2 hop limit when running in containers on EC2 |

## Pricing levers

On-Demand, Reserved Instances/Savings Plans, Spot (interruptible), Dedicated Hosts. Right-sizing and stopping dev instances overnight reduce spend — see [[AWS Billing and cost management]].

## Recall

- What is lost on `stop` vs `terminate`?
- Why should application servers usually live in private subnets?

## Sources

- [Amazon EC2 User Guide](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/concepts.html)
- [Instance types](https://aws.amazon.com/ec2/instance-types/)
