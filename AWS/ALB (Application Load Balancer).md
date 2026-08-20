[[AWS]] [[AWS Networking]] [[Security group]] [[Route53]] [[AWS EC2]] [[AWS Auto Scaling]] [[connection chrun]] [[load balancer]] [[TLS (Transport Layer Security)]]

# ALB (Application Load Balancer)

> L7 (ALB) and L4 (NLB) front doors in a VPC — health-checked distribution to targets. Idle timeout and SG-to-SG health checks cause most “works locally, 502 in AWS” tickets. Concept algorithms: [[load balancer]].

## Mental model

**ALB** terminates HTTP/HTTPS, routes by host/path, speaks to **target groups** (EC2, IP, Lambda). **NLB** is L4 TCP/UDP/TLS, preserves client IP (with caveats), static per-AZ IPs / EIP. Both need **subnets ≥2 AZs**, security groups (ALB), and correct **health checks**.

```
Client ──► ALB (public subnets) ──► target group ──► app SG / instances
              │
              └── ACM cert; idle timeout 60s default
```

| | ALB | NLB |
|--|-----|-----|
| Layer | HTTP/HTTPS (L7) | TCP/UDP/TLS (L4) |
| Host/path routing | Yes | No |
| Idle timeout | Configurable (default **60s**) | ~350s flow |
| Client IP to target | Via `X-Forwarded-For` | Preserved (TCP) |
| Targets | Instance, IP, Lambda | Instance, IP, ALB |

## Standard config / commands

### Prod web pattern

| Piece | Choice | Why |
|-------|--------|-----|
| Scheme | internet-facing | Public HTTPS |
| Subnets | Public, ≥2 AZ | HA |
| Listener | 443 + ACM cert | Terminate TLS at LB |
| Target group | Instance or IP; HTTP:8080 | App port private |
| Health check | `/health` 200 | Don't use login page |
| SG | `alb-sg` 443 from `0.0.0.0/0`; app SG only from `alb-sg` | No world→app |

```bash
aws elbv2 describe-load-balancers --names app-prod
aws elbv2 describe-target-health --target-group-arn arn:aws:elasticloadbalancing:...
aws elbv2 modify-load-balancer-attributes --load-balancer-arn arn:... \
  --attributes Key=idle_timeout.timeout_seconds,Value=60
```

### DNS

Route53 **ALIAS** A record → ALB dualstack DNS name ([[Route53]]). Do not CNAME apex.

### Idle timeout ladder (critical)

Default ALB idle = **60s**. Node/nginx keepalive must be **>** LB idle or you get 502 churn ([[connection chrun]]):

```
ALB idle 60s  <  Node keepAliveTimeout 65s+  <  upstream idle
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Targets unhealthy | Target SG allows **ALB SG** on health port; path/status | Open SG; fix `/health` |
| 502 Bad Gateway | Target died mid-request; idle mismatch; connection reset | Align timeouts; check app crash |
| 504 Gateway Timeout | App slow; target timeout < ALB idle | Raise TG timeout; fix slow handler |
| HTTPS works, HTTP doesn't | Listener missing; redirect rule | Add :80 → 443 redirect |
| Sticky sessions break scale-out | Cookie stickiness | Prefer stateless app; or enable stickiness knowingly |
| NLB target sees wrong IP | Proxy protocol / target type | Document client-IP expectations |
| Only one AZ works | Subnet mapping; ASG AZ balance | Register targets all AZs |

## Gotchas

> [!WARNING]
> **Health checks come from the ALB nodes** — target SG must allow the **ALB security group**, not your laptop IP.

> [!WARNING]
> **ALB idle 60s vs Node keepAlive ≤60** → intermittent 502 on pooled connections ([[connection chrun]]).

> [!WARNING]
> **Lambda target** — ALB invokes Lambda; payload/size limits differ from API Gateway.

> [!WARNING]
> **Deletion protection** — enable on prod ALBs; Terraform destroy otherwise succeeds.

## When NOT to use

- **Single-instance lab with EIP** — overkill; use EIP until you need HA.
- **WebSockets / long-lived** — raise idle timeout; or NLB / dedicated broker.
- **Non-HTTP protocols** — NLB or Gateway Load Balancer.
- **Global static assets** — [[CloudFront]] in front of S3/ALB.

## Related

[[AWS Networking]] · [[Security group]] · [[Route53]] · [[AWS EC2]] · [[AWS Auto Scaling]] · [[AWS Lambda]] · [[API Gateway]] · [[CloudFront]] · [[connection chrun]] · [[load balancer]] · [[AWS]]
