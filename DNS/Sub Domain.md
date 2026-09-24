**You might have configured**
```txt
api.example.com    → 194.195.119.168
stage.example.com  → 194.195.119.168
prod.example.com   → 194.195.119.168
test.example.com   → 194.195.119.168
```
this is a single zone `example.com zone` or they could point to completely different IPs

```txt
api.example.com    → 10.0.0.10
stage.example.com  → 10.0.0.20
prod.example.com   → 10.0.0.30
test.example.com   → 10.0.0.40
```

**Creating the subdomain does not create a new nameserver or zone.** When you are creating these subdomains, you are essentially creating **DNS names that can have records in the `example.com` zone.**

> [!NOTE]
> You can even create the name and then have no useful DNS record associated with it yet.

> `example.com` is the zone, and `api` `stage` `prod` (subdomains) are names within that zone to which you can attach DNS records.