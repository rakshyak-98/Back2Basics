[[AMI (Amazon Machine Image)]] [[AWS EBS(Elastic Block Store)]] [[Security group]] [[Elastic IP]] [[AWS Networking]]

# AWS EC2

> EC2 provides resizable virtual machines in a VPC — you choose an image, instance type, storage, and security groups; the first outage is usually networking or disk, not the hypervisor.

```txt
        AWS EC2 ──┬── Why it matters
               ├── Sources
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Why It Matters
- **Key signal:** EC2 reviews cover instance types, AMIs, EBS vs instance store, security gr…

## Sources
- [Amazon EC2 User Guide](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/concepts.html) — overview
- [Instance types](https://aws.amazon.com/ec2/instance-types/) — overview

## Technical Details
```bash
aws ec2 describe-instances --instance-ids i-0abc123
aws ec2 start-instances --instance-ids i-0abc123
aws ec2 stop-instances --instance-ids i-0abc123
```

```bash
ssh -i ~/.ssh/my-key.pem ec2-user@<public-dns-or-ip>
```

- Default Linux user varies by AMI: `ec2-user` (Amazon Linux), `ubuntu` (Ubuntu…

1. Pick region and AZ for latency and compliance.
2. Select AMI (Amazon Linux, Ubuntu, Windows, or golden image).
3. Size instance for CPU/memory/network — burstable `t*` families accrue CPU credits.
4. Attach security group allowing only required ports (SSH often restricted to bastion CIDR).
5. Place in **private subnet** for app tiers; use load balancer in public subnet for HTTP/S.
6. Enable **detailed monitoring** and **IMDSv2** (`HttpTokens: required`) on the metadata service.

## Mistakes to Avoid
| Symptom | Check |
|---------|-------|
| Cannot SSH | Security group, NACL, wrong key, instance in private subnet without bastion |
| Disk full | [[AWS EBS(Elastic Block Store)]] volume size; expand volume and grow filesystem |
| Status check failed | Instance or underlying hardware — stop/start or replace |
| Metadata access from app | IMDSv2 hop limit when running in containers on EC2 |

## Pros/Cons or Trade-offs
On-Demand, Reserved Instances/Savings Plans, Spot (interruptible), Dedicated Hosts. Right-sizing and stopping dev instances overnight reduce spend — see [[AWS Billing and cost management]].
