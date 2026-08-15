[[DNS]] [[DNS zone]] [[AWS Networking]] [[AWS EC2]] [[How to connect Godaddy domain with AWS EC2 instance]]

# Route53

> Amazon Route 53 is AWS's authoritative DNS service and domain registrar — you create hosted zones, publish records, and optionally run health-checked routing policies that send traffic only to healthy endpoints.

## Interview Relevance

Route 53 interviews check hosted zones, routing policies, health checks, and DNS failover patterns.

## Sources

- [Amazon Route 53 Developer Guide](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/Welcome.html) — deep-dive
- [Choosing a routing policy](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-policy.html) — overview

## Technical Details

```bash
aws route53 list-hosted-zones
aws route53 change-resource-record-sets --hosted-zone-id Z123 --change-batch file://change.json
```

### Core concepts

| Concept | Meaning |
|---------|---------|
| **Hosted zone** | Container for DNS records for a domain (public or private) |
| **Record set** | Name, type (A, AAAA, CNAME, MX, TXT, …), TTL, value |
| **Registrar vs DNS** | Route 53 can be both; domains bought elsewhere need NS delegation here |
| **Private hosted zone** | Resolvable only inside associated VPCs |
| **Health check** | HTTP/HTTPS/TCP probe for routing decisions |

Route 53 implements standard DNS ([RFC 1035](https://datatracker.ietf.org/doc/html/rfc1035)) with AWS-specific routing policies.

### Routing policies

| Policy | Behavior |
|--------|----------|
| **Simple** | Single value returned |
| **Weighted** | Split traffic by weight (blue/green, canary) |
| **Latency** | Lowest latency region for multi-region |
| **Failover** | Active/passive with health checks |
| **Geolocation** | Route by user geography |
| **Geoproximity** | Route by geographic bias with optional bias adjustments |
| **Multivalue** | Multiple healthy records (not a substitute for load balancer) |

### Common records for [[AWS EC2]]

```
www.example.com.  A     300  203.0.113.10        # Elastic IP or ALB alias target
api.example.com.  ALIAS     dualstack.my-alb-....  # Alias to ALB (no charge for queries to AWS targets)
```

**Alias records** map to AWS resources (ALB, CloudFront, S3 website) without CNAME restrictions at zone apex.

### Private zone pattern

Associate VPCs with a private zone `internal.example.com` for service discovery without exposing names publicly.
