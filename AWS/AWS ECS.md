[[AWS]] [[AWS ECR]] [[IAM]] [[ALB (Application Load Balancer)]] [[AWS Networking]] [[Security group]] [[AWS Lambda]] [[AWS EC2]] [[CloudWatch]]

# AWS ECS

> **Elastic Container Service** — run Docker tasks on **Fargate** (serverless capacity) or **EC2** capacity providers. Two IAM roles (task vs execution) and ALB target groups are where most first deploys fail.

## Mental model

| Concept | Meaning |
|---------|---------|
| **Task definition** | Container image, CPU/mem, env, roles, ports |
| **Task** | Running instantiation |
| **Service** | Keep N tasks healthy; attach load balancer |
| **Cluster** | Logical group; Fargate or EC2 capacity |
| **Execution role** | Pull from ECR, write logs, get secrets **at start** |
| **Task role** | AWS API calls **from app code** (S3, SQS, …) |

```
Service ──► tasks (Fargate ENI in subnet)
               │
               ├── execution role → ECR + Secrets + CW Logs
               └── task role → app AWS calls
               └── ALB target group (ip mode for Fargate)
```

vs [[AWS Lambda]]: long-running, multiple ports, larger images → ECS. vs raw [[AWS EC2]]: less AMI baking, better packing.

## Standard config / commands

### Minimal prod service

| Knob | Choice |
|------|--------|
| Launch type | Fargate |
| Subnets | Private; NAT or VPC endpoints for ECR/Logs/Secrets |
| Assign public IP | OFF in private |
| TG type | `ip` |
| SG | App port from `alb-sg` only |
| Logs | `awslogs` driver → [[CloudWatch]] |

```bash
aws ecs describe-services --cluster app --services api \
  --query 'services[0].{Status:status,Running:runningCount,Desired:desiredCount,Events:events[0:3]}'

aws ecs update-service --cluster app --service api --force-new-deployment
```

### IAM split (critical)

```
executionRoleArn  → ecr:Get*, logs:Create/Put*, secretsmanager:GetSecretValue (+ KMS)
taskRoleArn       → only what the app needs (s3:GetObject, sqs:SendMessage, …)
```

Never put app permissions only on the execution role (or vice versa).

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `CannotPullContainerError` | Execution role ECR; VPC endpoints/NAT | ECR perms; [[AWS ECR]] endpoints |
| Tasks stop immediately | CW logs; essential container exit | Fix entrypoint; see stopped reason |
| ALB unhealthy | TG `ip` mode; SG; container port mapping | Open SG; hostPort irrelevant on Fargate |
| Secrets inject fail | Execution role + KMS | Grant GetSecretValue + decrypt |
| `ResourceInitializationError` | ENI / subnet IP exhaustion | Bigger subnets; scale carefully |
| Deploy stuck draining | Deregistration delay; health | Lower delay; fix health path |

## Gotchas

> [!WARNING]
> **Task role ≠ execution role** — confusing them → either can't pull images or app `AccessDenied`.

> [!WARNING]
> **Fargate in private subnet without NAT/endpoints** — cannot pull ECR or push logs.

> [!WARNING]
> **Hard-coded env secrets in task def** — visible in console/API; use Secrets Manager refs.

> [!WARNING]
> **CPU/memory pair must be valid Fargate combination** — invalid → register fails.

## When NOT to use

- **Tiny event handlers** — [[AWS Lambda]] is simpler.
- **Need full Kubernetes ecosystem** — EKS (out of scope for this leaf).
- **GPU / specialty hardware** — check Fargate limits; often EC2 capacity providers.

## Related

[[AWS ECR]] · [[IAM]] · [[ALB (Application Load Balancer)]] · [[AWS Networking]] · [[Security group]] · [[AWS Lambda]] · [[AWS EC2]] · [[AWS Auto Scaling]] · [[CloudWatch]] · [[AWS Secrets Manager]] · [[AWS]]
