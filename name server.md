A Name Server is a DNS server that stores and serves authoritative DNS records for a domain.
- responsible for resolving domain names into IP addresses and routing clients to the correct DNS zone.

> [!INFO]
> NS records in DNS specify which servers are authoritative for a domain.
> delegates control of a domain (or subdomain) to a specific DNS providers.

```txt
example.com.    3600   IN   NS   ns1.dns-provider.com.
example.com.    3600   IN   NS   ns2.dns-provider.com.
```

```bash
dig +short NS example.com; # check NS records
nslookup -type=NS example.com;
```