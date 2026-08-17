[[Route53]] [[AWS EC2]] [[Elastic IP]] [[AWS Networking]] [[DNS]]

# How to connect Godaddy domain with AWS EC2 instance

> Pointing a GoDaddy-registered domain at an EC2 instance means delegating DNS to Route 53 (or updating A records at GoDaddy) so your hostname resolves to the instance's public IP or load balancer.

```txt
        How to connect God ──┬── Interview
               ├── Sources
               └── Mechanism
```

## Interview Relevance
- **Interview probes:** Interviewers ask about How to connect Godaddy domain with AWS EC2 instance to…

## Sources
- [Making Amazon Route 53 the DNS service for a domain](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/migrate-dns-domain-in-use.html) — overview
- [GoDaddy — Change nameservers for domains](https://www.godaddy.com/help/change-nameservers-for-my-domains-664) — overview

## Technical Details
### Recommended path: Route 53 as DNS

- GoDaddy remains **registrar**; AWS becomes **DNS host**.
- This unlocks alias records to ALB and health-checked failover.

### Steps

1. **Launch [[AWS EC2]]** with [[Security group]] allowing HTTP/HTTPS (and SSH from your IP only).
2. **Allocate [[Elastic IP]]** and associate with the instance (or use an Application Load Balancer instead).
3. **Create hosted zone** in [[Route53]] for `example.com`.
4. Copy the four **NS records** Route 53 assigns to the zone.
5. In **GoDaddy DNS management**, change nameservers to the Route 53 NS set (not mixed with GoDaddy parking NS).
6. In Route 53, create records:
- `www.example.com` → A record → Elastic IP, or ALIAS to ALB
- `example.com` (apex) → ALIAS to ALB or A to Elastic IP
7. Wait for DNS propagation (minutes to 48 hours; usually under an hour).

```bash
dig +short www.example.com A
curl -I http://www.example.com
```

### Alternative: keep DNS at GoDaddy

- Create **A record** at GoDaddy pointing `@` and `www` to your Elastic IP.
- Works for simple setups but lacks Route 53 alias features and advanced routin…

### Production hardening

| Instead of… | Use… |
|-------------|------|
| EIP on single EC2 | Application Load Balancer + Auto Scaling |
| HTTP only | ACM certificate on ALB or CloudFront |
| Direct SSH from internet | Bastion or SSM Session Manager |

- See [[aws host website]] if the site is static

### TLS

- Use **AWS Certificate Manager** with ALB or CloudFront.
- GoDaddy sells certificates but ACM integration is smoother inside AWS.

### Troubleshooting

| Symptom | Check |
|---------|-------|
| NXDOMAIN | Nameserver delegation incomplete at registrar |
| Wrong IP | Stale A record at GoDaddy after moving to Route 53 |
| Connection timeout | Security group, instance stopped, wrong Elastic IP association |
| SSL errors | Certificate SAN must cover hostname |
