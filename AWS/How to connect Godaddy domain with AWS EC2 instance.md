[[Route53]] [[DNS]] [[DNS zone]] [[NAT (Network Address Translation)]] [[certbot (letsencrypt)]] [[CORS (Cross Origin Request Sharing)]]

# Connect GoDaddy domain to AWS EC2

> Runbook: point a GoDaddy-registered domain at an EC2 instance with correct DNS, networking, and HTTPS — **Route53 vs GoDaddy NS decision first**.

---

## Mental model

Registration and DNS hosting are **separate**. GoDaddy holds the domain registration; **whoever hosts the nameservers** controls A/CNAME/ALIAS records.

```txt
Option A — GoDaddy DNS (simplest for one VM)
  Registrar: GoDaddy
  Nameservers: GoDaddy default
  A record @ ──► Elastic IP (EC2)

Option B — Route53 authoritative (AWS-native)
  Registrar: GoDaddy
  Nameservers: ns-xxx.awsdns-xx.com (delegated at GoDaddy)
  ALIAS/A in hosted zone ──► Elastic IP or ALB
```

| Record | Use | Gotcha |
|--------|-----|--------|
| **A** | `@` (apex) → IPv4 | Must be static IP — use **Elastic IP** |
| **CNAME** | `www` → apex or ALB hostname | **Cannot** CNAME apex `@` per DNS RFC |
| **ALIAS** (Route53 only) | Apex → ALB/CloudFront/EIP | Solves apex + AWS target without CNAME hack |
| **AAAA** | IPv6 | Only if instance has IPv6 |

**Without Elastic IP:** stop/start changes public IP → DNS breaks until TTL expires.

---

## Standard config / commands

### Step 0 — EC2 baseline

```txt
1. Launch EC2 (Amazon Linux / Ubuntu)
2. Allocate + Associate Elastic IP to instance
3. Security group inbound:
     22/tcp   — your IP only (SSH)
     80/tcp   — 0.0.0.0/0 (HTTP — certbot + redirect)
     443/tcp  — 0.0.0.0/0 (HTTPS)
4. App listens 0.0.0.0:80/443 (not 127.0.0.1 only)
5. Nginx/Apache vhost with server_name yourdomain.com www.yourdomain.com
```

```shell
# Verify from outside
dig +short yourdomain.com A
curl -I http://yourdomain.com
curl -I https://yourdomain.com
```

### Option A — GoDaddy DNS panel

```txt
DNS Management → Records:
  Type A    Host @     Points to <Elastic IP>    TTL 600
  Type A    Host www   Points to <Elastic IP>    TTL 600
  (or CNAME www → yourdomain.com if preferred)
```

Propagation: usually 5–30 min; TTL controls stale cache duration.

### Option B — Route53 hosted zone

```shell
# AWS Console: Route53 → Create hosted zone → yourdomain.com
# Copy 4 NS records → GoDaddy → Nameservers → Custom → paste all 4

# Record in hosted zone:
# A or ALIAS  yourdomain.com  →  Elastic IP (or ALIAS to ALB)
# A or CNAME  www.yourdomain.com  →  same target
```

Route53 ALIAS to ALB example: target = dualstack.my-alb-xxxxx.region.elb.amazonaws.com, type A.

### HTTPS path (Let's Encrypt on EC2)

```shell
sudo apt install certbot python3-certbot-nginx   # or certbot-apache
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
# HTTP-01 challenge needs port 80 open and vhost serving .well-known

sudo certbot renew --dry-run
# cron/systemd timer handles auto-renew
```

For ALB termination: ACM cert in **us-east-1** if CloudFront; regional ACM for ALB. No certbot on instance.

### Upgrade path (when one VM isn't enough)

```txt
EC2 + EIP  →  ALB + target group  →  Route53 ALIAS
              ACM cert on ALB
              EC2 SG: only ALB SG on 80/443, not 0.0.0.0/0
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Domain doesn't resolve | `dig yourdomain.com NS` + `A` | Wrong NS delegation; A record still pointing at old IP |
| Resolves but connection timeout | SG rules; `ss -tlnp \| grep :80` | Open 80/443; app not listening on public interface |
| Works by IP, not domain | `curl -H 'Host: yourdomain.com' http://<EIP>` | DNS not updated; vhost `server_name` mismatch |
| HTTPS cert error | `certbot certificates`; expiry | Renew; ensure port 80 open for HTTP-01 |
| Intermittent after reboot | EIP disassociated? | Re-associate Elastic IP; use ENI/EIP automation |
| www works, apex doesn't | Apex CNAME attempt | Use A/ALIAS at apex, not CNAME |
| Slow cutover | Old TTL 86400 | Lower TTL 24h before migration |

```shell
dig +trace yourdomain.com
whois yourdomain.com | grep -i 'name server'
curl -v https://yourdomain.com 2>&1 | grep -i 'subject\|issuer\|SSL'
```

---

## Gotchas

> [!WARNING]
> **GoDaddy "Forwarding" vs DNS A record** — URL forwarding masks DNS; breaks certbot and API clients. Use DNS records only.

> [!WARNING]
> **Parking page** — GoDaddy default landing page means A record not set or wrong host (`@` vs blank).

> [!WARNING]
> **Elastic IP on stopped instance** — you pay for unattached EIP. Release if tearing down.

> [!WARNING]
> **Reverse DNS (PTR)** — EC2 default PTR is `ec2-xx-xx-xx-xx.compute.amazonaws.com`. Matters for **outbound email**, not website hosting.

> [!WARNING]
> **Mixed NS** — editing GoDaddy records while nameservers point to Route53 has no effect. Always check NS first.

---

## When NOT to use

- **Bare EC2 + manual DNS** at scale — move to ALB + Route53 + ACM.
- **CNAME apex** — use Route53 ALIAS or ANAME provider feature.
- **certbot on instance behind TLS-only ALB** — terminate at ALB with ACM; use DNS-01 if needed.

---

## Related

[[Route53]] [[DNS]] [[DNS zone]] [[certbot (letsencrypt)]] [[certbot error]] [[NAT (Network Address Translation)]] [[nginx SPA deployment]]
