A nameserver is a DNS server that is responsible for answering DNS queries for a particular DNS zone.

> A nameserver is a DNS server that knows the authoritative DNS records for a zone and answers queries about those records.

the nameserver receives an `QUERY` and returns `Answer`. The nameserver loads the zone data and uses ti to answer DNS queries.

`ns1.example.com` is the **hostname of the nameserver.** The actual nameserver is the **DNS service running on a machine/network-endpoint** that responds to DNS queries.

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