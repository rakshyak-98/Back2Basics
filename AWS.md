[[IAM]] [[AWS EC2]] [[AWS Networking]] [[Route53]] [[AWS Lambda]] [[AWS ECR]] [[Security group]] [[INDEX]]

# AWS

> Amazon Web Services — cloud building blocks (compute, storage, network, identity) you compose with APIs; misconfigured IAM or security groups usually break first.





## Interview Relevance
Interviewers expect you to separate identity ([[IAM]]), network reachability ([[Security group]], VPC), and data plane (EC2/Lambda/storage). Signal Well-Architected thinking: least privilege, blast radius, cost.

## Sources
- [AWS Documentation](https://docs.aws.amazon.com/) — deep-dive
- [AWS Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html) — overview

## Core Definition
AWS is a global cloud platform of managed services. You authenticate every API call, place resources in regions/VPCs, and pay for what you provision or consume.

## Key Concepts
- **Identity:** Users/roles/policies; prefer roles over long-lived access keys ([[IAM]], [[aws STS (Security Token Service)]], [[ARN (Amazon Resource Name)]]).
- **Compute:** VMs ([[AWS EC2]]), containers (ECS/EKS + [[AWS ECR]]), functions ([[AWS Lambda]]).
- **Storage:** Block ([[EBS (Elastic Block Store)]]), file ([[AWS EFS (Elastic File System)]]), object (S3).
- **Network:** VPC, subnets, routes, [[Security group]], [[Elastic IP]], DNS ([[Route53]]).
- **Ops:** [[AWS cli commands]], billing alarms ([[AWS Billing and cost management]]).

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
| Durable disk | [[EBS (Elastic Block Store)]] |
| Shared POSIX files | [[AWS EFS (Elastic File System)]] |
| Serverless code | [[AWS Lambda]] |
| Container images | [[AWS ECR]] |
| DNS / domain | [[Route53]] · [[How to connect Godaddy domain with AWS EC2 instance]] |
| Who can call APIs | [[IAM]] · [[aws STS (Security Token Service)]] |
| CLI ops | [[AWS cli installation]] · [[AWS cli commands]] |

## Real-World Applications
Static site or small API: S3/CloudFront or EC2 + security group + Route 53. Production service: private subnets, ALB, IAM roles for tasks, no access keys in git.

## Pros/Cons or Trade-offs
- **Pro:** Breadth, global regions, mature IAM and networking primitives.
- **Con:** Complexity and cost surprises; easy to over-permission; regional constraints.

## Comparison
vs bare metal/colocation: faster provisioning, shared responsibility model. vs other clouds: same ideas (identity, VPC, managed DB) with different names. Sibling vault hubs: [[Docker]], [[Terraform]], [[Linux]].

## Mistakes to Avoid
- Long-lived access keys on laptops or in repositories.
- `0.0.0.0/0` on sensitive ports “temporarily.”
- Confusing security groups (stateful allow) with network ACLs.
- Ignoring data transfer and idle resource cost.
