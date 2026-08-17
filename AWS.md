[[IAM]] [[AWS EC2]] [[AWS Networking]] [[Route53]] [[AWS Lambda]] [[AWS ECR]] [[Security group]] [[INDEX]]

# AWS

> Amazon Web Services — cloud building blocks (compute, storage, network, identity) you compose with APIs; misconfigured IAM or security groups usually break first.

```txt
        AWS ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers expect you to separate identity ([[IAM]]), network reachability …

## Sources
- [AWS Documentation](https://docs.aws.amazon.com/) — deep-dive
- [AWS Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html) — overview

## Key Concepts
- **Identity:** Users/roles/policies
- **Compute:** VMs ([[AWS EC2]]), containers (ECS/EKS + [[AWS ECR]]), functions ([[AWS Lambd…
- **Storage:** Block ([[EBS (Elastic Block Store)]]), file ([[AWS EFS (Elastic File System)]…
- **Network:** VPC, subnets, routes, [[Security group]], [[Elastic IP]], DNS ([[Route53]]).
- **Ops:** [[AWS CLI]], billing alarms ([[AWS Billing and cost management]]).


- **Core:** AWS is a global cloud platform of managed services

## Technical Details
```txt
Internet / users
      │
      ▼
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Route 53   │────►│  ELB / ALB   │────►│  EC2 / ECS  │
│  (DNS)      │     │  (optional)  │     │  Lambda     │
└─────────────┘     └──────────────┘     └──────┬──────┘
                                                │
         IAM policies ◄─────────────────────────┤
         Security groups (stateful L4)          │
         EBS / EFS / S3                         ▼
                                         VPC subnets
```

| You need to… | Start here |
|--------------|------------|
| Launch a VM | [[AWS EC2]] → [[AMI (Amazon Machine Image)]] → [[Security group]] |
| Durable disk | [[AWS EBS(Elastic Block Store)]] |
| Shared POSIX files | [[AWS EFS (Elastic File System)]] |
| Serverless code | [[AWS Lambda]] |
| Container images | [[AWS ECR]] |
| DNS / domain | [[Route53]] · [[How to connect Godaddy domain with AWS EC2 instance]] |
| Who can call APIs | [[IAM]] · [[aws STS (Security Token Service)]] |
| CLI ops | [[AWS CLI installation]] · [[AWS CLI]] |

## Mistakes to Avoid
- **Mistake:** Long-lived access keys on laptops or in repositories
- **Mistake:** `0.0.0.0/0` on sensitive ports “temporarily.”
- **Mistake:** Confusing security groups (stateful allow) with network ACLs
- **Mistake:** Ignoring data transfer and idle resource cost

## Pros/Cons or Trade-offs
- **Pro:** Breadth, global regions, mature IAM and networking primitives.
- **Con:** Complexity and cost surprises; easy to over-permission; regional constraints.

## Comparison
- vs bare metal/colocation: faster provisioning, shared responsibility model


### Use cases
- Static site or small API: S3/CloudFront or EC2 + security group + Route 53
