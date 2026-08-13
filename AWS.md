[[IAM]] · [[AWS EC2]] · [[AWS Networking]] · [[Route53]] · [[AWS Lambda]] · [[AWS ECR]]

# AWS

> Amazon Web Services is a cloud platform where compute, storage, networking, and identity are separate services you compose with APIs — misconfigured IAM or security groups are usually what breaks first.

---

## What lives here

This folder collects operational notes for core AWS building blocks: virtual machines ([[AWS EC2]]), block and file storage ([[EBS (Elastic Block Store)]], [[AWS EFS (Elastic File System)]]), containers ([[AWS ECR]]), serverless ([[AWS Lambda]]), networking ([[AWS Networking]], [[Security group]], [[Elastic IP]], [[Route53]]), identity ([[IAM]], [[aws STS (Security Token Service)]], [[ARN (Amazon Resource Name)]]), and day-two tasks ([[AWS cli commands]], [[AWS Billing and cost management]]).

## Routing by job

| You need to… | Start here |
|--------------|------------|
| Launch a virtual machine | [[AWS EC2]] → [[AMI (Amazon Machine Image)]] → [[Security group]] |
| Attach durable disk to an instance | [[EBS (Elastic Block Store)]] |
| Share POSIX files across instances | [[AWS EFS (Elastic File System)]] |
| Run code without managing servers | [[AWS Lambda]] |
| Store and pull container images | [[AWS ECR]] |
| Point a domain at infrastructure | [[Route53]] · [[How to connect Godaddy domain with AWS EC2 instance]] |
| Control who can call which API | [[IAM]] · [[aws STS (Security Token Service)]] |
| Operate from a terminal | [[AWS cli installation]] · [[AWS CLI commands]] |
| Host a static site cheaply | [[aws host website]] |
| Understand spend | [[AWS Billing and cost management]] |

## How AWS pieces connect

```
Internet / users
      │
      ▼
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Route 53   │────►│  ELB / ALB   │────►│  EC2 / ECS  │
│  (DNS)      │     │  (optional)  │     │  Lambda     │
└─────────────┘     └──────────────┘     └──────┬──────┘
                                                │
         IAM policies ◄─────────────────────────┤
         Security groups (L4 firewall)          │
         EBS / EFS (data)                       ▼
                                         VPC subnets
```

Every API call is authenticated and authorized through [[IAM]]. Network reachability is a separate layer: [[Security group]] rules, route tables, and whether the resource has a public [[Elastic IP]] or sits behind a load balancer.

## Recall

- What is the difference between an identity policy, a resource policy, and a service control policy?
- Why do production workloads prefer IAM roles over long-lived access keys?
- Which layer blocks traffic first: security group or network ACL?

## Sources

- [AWS Documentation](https://docs.aws.amazon.com/)
- [AWS Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html)
